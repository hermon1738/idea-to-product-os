"""cli/commands/agent.py — Read-only agent subcommands: list and status.

WHY THIS EXISTS:
    Phase 6 introduces a managed agent layer. Operators need to inspect the
    agent registry from the terminal without opening YAML directly.
    `bricklayer agent list` gives a quick overview; `bricklayer agent status
    <id>` gives the full detail for a specific agent. Without this module,
    there is no human-readable CLI surface for the registry built in Brick 21.

DESIGN DECISIONS:
- Typer subapp (``agent_app``) registered on the top-level app in main.py.
  Alternative was flattening to ``bricklayer agent-list`` and
  ``bricklayer agent-status``. Rejected because the subcommand group
  (`agent list`, `agent status`, `agent new`, `agent deploy`) reads as a
  natural namespace and matches the Phase 6 roadmap.
- Both commands take ``root`` as a Path argument to their run_* handlers
  rather than detecting it internally. Alternative was calling find_yaml()
  inside the handler. Rejected for the same reason as every other command:
  keeping root detection in main.py makes the handlers unit-testable with
  a tmp_path fixture.
- run_agent_list() returns int (exit code) so that the Typer wrapper can
  raise typer.Exit(code=exit_code). Alternative was calling raise typer.Exit
  inside the handler. Rejected because Typer raises in handlers break tests
  that call run_* directly without CliRunner.
- Column widths are constants so the table is consistent regardless of
  agent names. Alternative was computing widths dynamically. Rejected as
  premature complexity — the three current agents fit the fixed widths, and
  any agent with a longer name will wrap gracefully rather than corrupt the
  table.
- Missing registry (no registry.yaml) is treated identically to an empty
  registry for `agent list`. Alternative was raising an error. Rejected
  because a missing registry is a valid initial state (no agents registered
  yet); the empty-registry prompt already tells the user what to do next.
- `agent status` returns exit 1 for an unknown ID — this is an operator
  error, not a state that should be treated as success. Consistent with how
  other CLI tools (git, kubectl) signal "object not found".
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer

from cli.registry import load, get

# ---------------------------------------------------------------------------
# Table layout constants (fixed column widths for consistent output).
# ---------------------------------------------------------------------------

# Width of the ID column — longest current ID is 21 chars ("idea-os-dispatcher-01").
_COL_ID: int = 24

# Width of the NAME column — longest current name is "Assignment Dispatcher" (21 chars).
_COL_NAME: int = 22

# Width of the RUNTIME column — "raw-python" is 10 chars.
_COL_RUNTIME: int = 12

# Width of the STATUS column — "live" / "stopped" / "error".
_COL_STATUS: int = 8

# Header divider line, spans all four columns plus separating spaces.
_DIVIDER: str = "─" * (_COL_ID + _COL_NAME + _COL_RUNTIME + _COL_STATUS + 3)

# Field labels for the detail block, padded to align values.
_LABEL_WIDTH: int = 10


# ---------------------------------------------------------------------------
# Typer subapp
# ---------------------------------------------------------------------------

agent_app = typer.Typer(
    name="agent",
    help="Manage agents in the registry.",
    no_args_is_help=True,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _format_row(agent: dict[str, Any]) -> str:
    """Format one agent dict as a fixed-width table row.

    Why it exists: Both the header and data rows need the same column widths.
    Centralising the formatting avoids duplicating the ljust constants.

    Args:
        agent: Agent dict with at least ``id``, ``name``, ``runtime``, and
               ``status`` keys. Missing keys render as empty strings.

    Returns:
        A single line string (no trailing newline) with columns space-separated.
    """
    return (
        agent.get("id", "").ljust(_COL_ID)
        + agent.get("name", "").ljust(_COL_NAME)
        + agent.get("runtime", "").ljust(_COL_RUNTIME)
        + agent.get("status", "")
    )


def _format_detail(agent: dict[str, Any]) -> str:
    """Format one agent dict as a labelled detail block.

    Why it exists: ``agent status`` needs a multi-line human-readable view
    of all fields, not just the four table columns. Extracting this keeps
    ``run_agent_status`` short and the format testable in isolation.

    Args:
        agent: Agent dict. All recognised field keys are rendered; unrecognised
               extra keys (e.g. ``container_name``) are silently ignored.

    Returns:
        Multi-line string (no trailing newline) with each field on its own line.
    """
    def _label(key: str) -> str:
        # Left-justify the label so all values align.
        return f"{key}:".ljust(_LABEL_WIDTH)

    lines = [
        f"{_label('Agent')}{agent.get('id', '')}",
        f"{_label('Name')}{agent.get('name', '')}",
        f"{_label('Project')}{agent.get('project', '')}",
        f"{_label('Role')}{agent.get('role', '')}",
        f"{_label('Runtime')}{agent.get('runtime', '')}",
        f"{_label('Status')}{agent.get('status', '')}",
        f"{_label('Trigger')}{agent.get('trigger', '')}",
        f"{_label('Channel')}{agent.get('discord_channel', '')}",
        f"{_label('Location')}{agent.get('location', '')}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Run handlers (called by Typer wrappers and directly by tests)
# ---------------------------------------------------------------------------


def run_agent_list(root: Path) -> int:
    """Print all agents from registry.yaml as a formatted table.

    Why it exists: Operators need a quick overview of every registered agent
    without opening YAML. This is the primary daily-use command for the
    agent layer.

    Args:
        root: Repo root directory (parent of context/).

    Returns:
        0 always — empty or missing registry is not an error for list.

    Raises:
        Never raises. ValueError from a malformed registry is caught and
        printed to stderr; exit code 1 is returned.
    """
    try:
        agents = load(root)
    except ValueError as exc:
        # Malformed registry.yaml — surface the error without a traceback.
        typer.echo(f"error: {exc}", err=True)
        return 1

    if not agents:
        # Missing or empty registry is a valid initial state.
        typer.echo("No agents registered. Run:")
        typer.echo("  bricklayer agent new")
        return 0

    # Print header.
    header = (
        "ID".ljust(_COL_ID)
        + "NAME".ljust(_COL_NAME)
        + "RUNTIME".ljust(_COL_RUNTIME)
        + "STATUS"
    )
    typer.echo(header)
    typer.echo(_DIVIDER)

    for agent in agents:
        typer.echo(_format_row(agent))

    return 0


def run_agent_status(root: Path, agent_id: str) -> int:
    """Print the full detail block for a single agent by ID.

    Why it exists: ``agent list`` shows four columns; operators need all fields
    (trigger, channel, location, etc.) when debugging or setting up a new
    agent. This command is the per-agent deep-dive.

    Args:
        root: Repo root directory (parent of context/).
        agent_id: The ``id`` field of the agent to look up.

    Returns:
        0 if the agent was found and printed.
        1 if the agent ID does not exist in the registry.
        1 if registry.yaml is malformed (error printed to stderr).

    Raises:
        Never raises. All errors are caught and printed to stderr.
    """
    try:
        agent = get(root, agent_id)
    except ValueError as exc:
        # Malformed registry.yaml.
        typer.echo(f"error: {exc}", err=True)
        return 1

    if agent is None:
        typer.echo(f"Agent not found: {agent_id}", err=True)
        return 1

    typer.echo(_format_detail(agent))
    return 0


# ---------------------------------------------------------------------------
# Typer command wrappers
# ---------------------------------------------------------------------------


@agent_app.command(name="list")
def agent_list() -> None:
    """List all agents from registry.yaml in a formatted table."""
    # Import here to avoid circular dependency; find_yaml is only needed at
    # CLI invocation time, not during unit tests that call run_agent_list directly.
    from cli.config import find_yaml

    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_agent_list(yaml_path.parent))


@agent_app.command(name="status")
def agent_status(
    agent_id: str = typer.Argument(..., help="Agent ID to inspect."),
) -> None:
    """Print the full detail block for a single agent by ID."""
    from cli.config import find_yaml

    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_agent_status(yaml_path.parent, agent_id))
