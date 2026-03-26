"""cli/commands/agent.py — Agent subcommands: list, status, new, deploy, live.

WHY THIS EXISTS:
    Phase 6 introduces a managed agent layer. Operators need to inspect the
    agent registry from the terminal without opening YAML directly, and to
    scaffold new agents without manually copying template files and editing
    registry.yaml.
    `bricklayer agent list` gives a quick overview; `bricklayer agent status
    <id>` gives the full detail for a specific agent; `bricklayer agent new`
    scaffolds a new agent directory and registers it; `bricklayer agent deploy`
    copies the scaffold to the ai-agents repo and pushes; `bricklayer agent
    live` marks an agent as live after VPS confirmation.
    Without this module there is no human-readable or scriptable CLI surface
    for the agent registry built in Brick 21.

DESIGN DECISIONS:
- Typer subapp (``agent_app``) registered on the top-level app in main.py.
  Alternative was flattening to ``bricklayer agent-list`` etc. Rejected
  because the subcommand group reads as a natural namespace and matches the
  Phase 6 roadmap (list, status, new, deploy).
- run_* handlers take ``root`` as a Path rather than detecting it internally.
  Alternative was calling find_yaml() inside the handler. Rejected because
  keeping root detection in main.py makes the handlers unit-testable with a
  tmp_path fixture.
- run_* handlers return int (exit code). Alternative was raising typer.Exit
  inside the handler. Rejected because Typer raises break tests that call
  run_* directly without CliRunner.
- Column widths are constants so the table is consistent regardless of agent
  names. Dynamic widths were rejected as premature complexity.
- Missing registry is treated identically to empty for ``agent list``.
  Rejected raising an error: missing registry is a valid initial state.
- ``agent status`` returns exit 1 for an unknown ID — consistent with how
  git/kubectl signal "object not found".
- ``agent new`` for --runtime nanobot resolves the template path from
  bricklayer.yaml agents.nanobot_template, defaulting to
  agents/nanobot-template/ relative to the repo root. Alternative was
  hardcoding the path. Rejected because the nanobot-template lives in a
  separate directory (~/ai-agents/) that varies by deployment.
- Placeholder tokens use ``__UPPER_SNAKE__`` convention (e.g. ``__AGENT_ID__``)
  so they are visually distinct inside YAML/Markdown files and unlikely to
  collide with real content.
- On any failure mid-scaffold (e.g. registry add() raises), the partially
  created directory is removed before returning exit 1 — no half-baked agent
  directories left on disk. Atomic from the operator's perspective.
- Registry entry is constructed from CLI args rather than reading back the
  scaffolded agent.yaml. Alternative was parsing the scaffolded file.
  Rejected because it introduces a YAML-parse step that could fail for
  nanobot templates with unusual formatting.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import yaml
import typer

from cli.registry import add as registry_add
from cli.registry import get, load, update_status

# ---------------------------------------------------------------------------
# Agent-new constants
# ---------------------------------------------------------------------------

# ID must be all-lowercase letters/numbers/hyphens and end with exactly two
# digits after the final hyphen.  Examples: idea-os-scribe-01, monitor-01.
_ID_PATTERN: re.Pattern[str] = re.compile(
    r"^[a-z][a-z0-9-]*-[a-z][a-z0-9-]*-\d{2}$"
)

# Recognised runtime values (kept as frozenset for O(1) lookup and easy
# extension — add "langchain" here when that runtime lands).
VALID_RUNTIMES: frozenset[str] = frozenset({"nanobot", "raw-python"})

# Files inside the nanobot template that contain __PLACEHOLDER__ tokens.
# Paths are relative to the copied agent directory root.
_TEMPLATE_FILES_TO_PATCH: tuple[str, ...] = (
    "agent.yaml",
    "workspace/SOUL.md",
    "workspace/AGENTS.md",
    "workspace/USER.md",
)

# Default template location relative to the repo root when bricklayer.yaml
# does not specify agents.nanobot_template.
_DEFAULT_TEMPLATE_RELPATH: str = "agents/nanobot-template"

# Minimal requirements for raw-python agents — pinned so scaffolded agents
# do not silently pick up a breaking library version.
_RAW_PYTHON_REQUIREMENTS: str = (
    "groq==0.11.0\n"
    "httpx==0.27.2\n"
    "discord.py==2.3.2\n"
)

# Human-readable format hint shown when the agent ID fails validation.
_ID_FORMAT_HINT: str = (
    "Required format: lowercase letters, numbers, hyphens; "
    "ends with -NN (two digits).\n"
    "Examples: idea-os-scribe-01, reddit-monitor-poller-01"
)

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
# agent new — helpers
# ---------------------------------------------------------------------------


def _validate_agent_id(agent_id: str) -> str | None:
    """Return an error message if ``agent_id`` fails format validation, else None.

    Why it exists: The registry and filesystem both use the agent ID as a
    primary key and directory name. Accepting IDs with spaces, uppercase, or
    missing sequence numbers would produce ambiguous registry entries and
    non-portable directory names.

    Args:
        agent_id: The proposed agent ID string.

    Returns:
        None if the ID is valid.
        A human-readable error string (no trailing newline) if invalid.
    """
    if not _ID_PATTERN.match(agent_id):
        return (
            f"Invalid agent ID: '{agent_id}'\n"
            + _ID_FORMAT_HINT
        )
    return None


def _get_template_path(root: Path, config: dict[str, Any]) -> Path:
    """Resolve the nanobot template directory path.

    Why it exists: The template lives outside the bricklayer-cli repo (in
    ~/ai-agents/agents/nanobot-template/ by default). Rather than hardcoding
    that path, this reads it from bricklayer.yaml so different deployments
    can point to different template locations.

    Args:
        root: Repo root directory.
        config: Parsed bricklayer.yaml dict.

    Returns:
        Absolute Path to the nanobot template directory (may not exist).
    """
    agents_config = (config.get("agents") or {})
    # Handle the case where bricklayer.yaml has ``agents: {}`` (empty dict).
    if not isinstance(agents_config, dict):
        agents_config = {}
    template_rel = agents_config.get("nanobot_template", _DEFAULT_TEMPLATE_RELPATH)
    return root / template_rel


def _build_placeholder_map(
    agent_id: str, project: str, role: str
) -> dict[str, str]:
    """Build the token→value map used to patch template files.

    Why it exists: Template files contain ``__UPPER_SNAKE__`` tokens that
    must be replaced with real values after the template is copied. Defining
    the map in one place means new tokens can be added without hunting for
    every call site.

    Args:
        agent_id: Full agent ID (e.g. ``idea-os-monitor-01``).
        project:  Project slug (e.g. ``idea-to-product-os``).
        role:     Agent role slug (e.g. ``monitor``).

    Returns:
        Dict mapping placeholder tokens to replacement strings.
    """
    # Sequence is the two-digit suffix at the end of the ID.
    sequence = agent_id.rsplit("-", 1)[-1]
    # Derive a human-readable name from the role slug.
    name = role.replace("-", " ").title()
    return {
        "__AGENT_ID__":       agent_id,
        "__PROJECT__":        project,
        "__ROLE__":           role,
        "__SEQUENCE__":       sequence,
        "__AGENT_NAME__":     name,
        "__DISCORD_CHANNEL__": agent_id,
        "__CONTAINER_NAME__": agent_id,
    }


def _replace_placeholders(path: Path, placeholder_map: dict[str, str]) -> None:
    """Replace all placeholder tokens in a file in place.

    Why it exists: copytree() copies bytes; placeholders must be patched
    after the copy. This helper is called once per template file and handles
    missing files gracefully (nanobot templates may omit AGENTS.md etc.).

    Args:
        path: Absolute path to the file to patch.
        placeholder_map: Token→value dict from ``_build_placeholder_map``.

    Raises:
        Never raises. Missing files are silently skipped.
    """
    if not path.exists():
        # Not all nanobot templates include every workspace file.
        return
    text = path.read_text(encoding="utf-8")
    for token, value in placeholder_map.items():
        text = text.replace(token, value)
    path.write_text(text, encoding="utf-8")


def _scaffold_nanobot(
    root: Path,
    agent_id: str,
    project: str,
    role: str,
    template_path: Path,
) -> tuple[int, Path | None]:
    """Copy nanobot template and replace all placeholder tokens.

    Why it exists: The nanobot scaffold involves a full directory copy plus
    multi-file text replacement. Isolating this in its own function keeps
    ``run_agent_new`` under 40 lines and makes the scaffold step independently
    testable.

    Args:
        root:          Repo root directory.
        agent_id:      Agent ID for the new agent.
        project:       Project slug.
        role:          Agent role slug.
        template_path: Absolute path to the nanobot-template directory.

    Returns:
        (0, target_dir) on success.
        (1, None) on failure (error printed to stderr before return).
    """
    if not template_path.exists():
        typer.echo(
            f"error: nanobot-template not found at {template_path}\n"
            "Set agents.nanobot_template in bricklayer.yaml to override the path.",
            err=True,
        )
        return 1, None

    target_dir = root / "context" / "agents" / agent_id
    # Copy entire template tree into the target directory.
    shutil.copytree(str(template_path), str(target_dir))

    placeholder_map = _build_placeholder_map(agent_id, project, role)
    for rel in _TEMPLATE_FILES_TO_PATCH:
        _replace_placeholders(target_dir / rel, placeholder_map)

    return 0, target_dir


def _scaffold_raw_python(
    root: Path,
    agent_id: str,
    project: str,
    role: str,
) -> tuple[int, Path | None]:
    """Create a minimal raw-python Discord bot scaffold.

    Why it exists: Raw-python agents share a common boilerplate
    (agent.py, Dockerfile, requirements.txt, agent.yaml). Centralising the
    scaffold logic here means the file contents are versioned in one place
    and any future changes apply to all new raw-python agents.

    Args:
        root:     Repo root directory.
        agent_id: Agent ID for the new agent.
        project:  Project slug.
        role:     Agent role slug.

    Returns:
        (0, target_dir) on success.
        (1, None) on failure (error printed to stderr before return).
    """
    target_dir = root / "context" / "agents" / agent_id
    target_dir.mkdir(parents=True, exist_ok=False)

    # agent.py — minimal Discord bot with AGENT_ID constant.
    agent_py = (
        f'"""Agent: {agent_id}\n'
        f"Project: {project}\n"
        f'Role: {role}\n"""\n'
        "import os\n\n"
        "import discord\n"
        "from discord.ext import commands\n\n"
        f'AGENT_ID: str = "{agent_id}"\n'
        f'AGENT_ROLE: str = "{role}"\n\n'
        'DISCORD_TOKEN: str = os.environ["DISCORD_TOKEN"]\n\n'
        "intents = discord.Intents.default()\n"
        "intents.message_content = True\n"
        'bot = commands.Bot(command_prefix="!", intents=intents)\n\n\n'
        "@bot.event\n"
        "async def on_ready() -> None:\n"
        '    """Log to stdout when the bot connects."""\n'
        "    print(f\"{AGENT_ID} ready\")\n\n\n"
        'if __name__ == "__main__":\n'
        "    bot.run(DISCORD_TOKEN)\n"
    )
    (target_dir / "agent.py").write_text(agent_py, encoding="utf-8")

    # Dockerfile — standard Python 3.11 slim image.
    dockerfile = (
        "FROM python:3.11-slim\n"
        "WORKDIR /app\n"
        "COPY requirements.txt .\n"
        "RUN pip install --no-cache-dir -r requirements.txt\n"
        "COPY . .\n"
        'CMD ["python", "agent.py"]\n'
    )
    (target_dir / "Dockerfile").write_text(dockerfile, encoding="utf-8")

    # requirements.txt — pinned versions from Brick 23 spec.
    (target_dir / "requirements.txt").write_text(
        _RAW_PYTHON_REQUIREMENTS, encoding="utf-8"
    )

    # agent.yaml — metadata for this agent.
    agent_yaml_data: dict[str, Any] = {
        "id": agent_id,
        "name": role.replace("-", " ").title(),
        "project": project,
        "role": role,
        "runtime": "raw-python",
        "status": "stopped",
        "trigger": f"!{role} in Discord",
        "location": f"context/agents/{agent_id}/",
        "discord_channel": agent_id,
        "container_name": agent_id,
    }
    (target_dir / "agent.yaml").write_text(
        yaml.dump(agent_yaml_data, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )

    return 0, target_dir


def _build_registry_entry(
    agent_id: str, project: str, role: str, runtime: str
) -> dict[str, Any]:
    """Build the registry dict for a newly scaffolded agent.

    Why it exists: The registry entry is constructed from CLI args rather
    than reading back the scaffolded agent.yaml to avoid a YAML-parse step
    that could fail for nanobot templates with unusual formatting.

    Args:
        agent_id: Full agent ID.
        project:  Project slug.
        role:     Role slug.
        runtime:  Runtime string (``nanobot`` or ``raw-python``).

    Returns:
        Dict with all REQUIRED_FIELDS populated.
    """
    return {
        "id": agent_id,
        "name": role.replace("-", " ").title(),
        "project": project,
        "role": role,
        "runtime": runtime,
        "status": "stopped",           # new agents are stopped until deployed
        "trigger": f"!{role} in Discord",
        "location": f"context/agents/{agent_id}/",
        "discord_channel": agent_id,
        "container_name": agent_id,
    }


# ---------------------------------------------------------------------------
# agent new — run handler
# ---------------------------------------------------------------------------


def run_agent_new(
    root: Path,
    agent_id: str,
    runtime: str,
    project: str,
    role: str,
    config: dict[str, Any],
) -> int:
    """Scaffold a new agent directory and register it in registry.yaml.

    Validates the agent ID and runtime, creates the scaffold, then appends
    the agent to registry.yaml with status ``stopped``. On any failure the
    registry is not modified and any partially created directory is removed.

    Args:
        root:     Repo root directory (parent of context/).
        agent_id: New agent ID; must match ``_ID_PATTERN``.
        runtime:  Either ``nanobot`` or ``raw-python``.
        project:  Project slug to embed in the scaffold and registry entry.
        role:     Role slug to embed in the scaffold and registry entry.
        config:   Parsed bricklayer.yaml dict (used to resolve template path).

    Returns:
        0 on success.
        1 on any validation or scaffold error (message printed to stderr).

    Raises:
        Never raises. All error paths return 1.
    """
    # --- 1. Validate ID format ---
    id_error = _validate_agent_id(agent_id)
    if id_error:
        typer.echo(f"error: {id_error}", err=True)
        return 1

    # --- 2. Validate runtime ---
    if runtime not in VALID_RUNTIMES:
        typer.echo(
            f"error: unknown runtime '{runtime}'. "
            f"Valid options: {', '.join(sorted(VALID_RUNTIMES))}",
            err=True,
        )
        return 1

    # --- 3. Duplicate ID check (registry) ---
    try:
        existing = get(root, agent_id)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        return 1

    if existing is not None:
        typer.echo(
            f"error: agent '{agent_id}' already exists in registry", err=True
        )
        return 1

    # --- 4. Duplicate directory check ---
    target_dir = root / "context" / "agents" / agent_id
    if target_dir.exists():
        typer.echo(
            f"error: directory already exists: context/agents/{agent_id}/\n"
            "Remove it or choose a different ID.",
            err=True,
        )
        return 1

    # --- 5. Scaffold ---
    created_dir: Path | None = None
    try:
        if runtime == "nanobot":
            template_path = _get_template_path(root, config)
            exit_code, created_dir = _scaffold_nanobot(
                root, agent_id, project, role, template_path
            )
        else:
            # raw-python
            exit_code, created_dir = _scaffold_raw_python(
                root, agent_id, project, role
            )

        if exit_code != 0:
            # Scaffold helper already printed the error.
            return 1

        # --- 6. Register in registry.yaml ---
        entry = _build_registry_entry(agent_id, project, role, runtime)
        registry_add(root, entry)

    except Exception as exc:  # noqa: BLE001 — clean up on unexpected errors
        # Remove any partially created directory so the operator can retry.
        if created_dir is not None and created_dir.exists():
            shutil.rmtree(str(created_dir))
        typer.echo(f"error: {exc}", err=True)
        return 1

    # --- 7. Success message ---
    typer.echo(f"Agent scaffolded: context/agents/{agent_id}/")
    typer.echo("Next: edit workspace/ files, then bricklayer agent deploy")
    return 0


# ---------------------------------------------------------------------------
# agent deploy + live — constants and helpers
# ---------------------------------------------------------------------------

# Divider printed around the deploy-ready block (38 chars, matches context.py).
_DEPLOY_DIVIDER: str = "━" * 38

# Git subprocess timeout in seconds — enough for a push over a slow connection.
_GIT_TIMEOUT: int = 60


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a git subcommand in ``cwd`` with a fixed timeout.

    Why it exists: All git calls share the same flags (capture_output, text,
    no shell). Centralising them makes the timeout and flags consistent and
    makes the git operations mockable in tests via a single patch target
    (``cli.commands.agent._run_git``).

    Args:
        args: Git subcommand and arguments, e.g. ``["push"]`` or
              ``["add", "agents/foo/"]``. The ``git`` prefix is prepended here.
        cwd:  Directory in which to run the command.

    Returns:
        CompletedProcess with ``returncode``, ``stdout``, and ``stderr``.

    Raises:
        RuntimeError: If the git command exceeds ``_GIT_TIMEOUT`` seconds.
            Raised instead of propagating ``subprocess.TimeoutExpired`` so
            that callers receive a clean, human-readable message rather than
            a raw traceback. The message names the timed-out command so Tony
            knows which step stalled.
    """
    cmd = ["git"] + args
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT,
            check=False,
            cwd=str(cwd),
        )
    except subprocess.TimeoutExpired:
        # Convert to RuntimeError so run_agent_deploy's generic except block
        # prints the message cleanly without a traceback (D-001 pattern).
        raise RuntimeError(
            f"Git operation timed out after {_GIT_TIMEOUT}s: {cmd[1]} {cmd[2] if len(cmd) > 2 else ''}"
        )


def _print_deploy_ready(agent_id: str, deploy_repo: Path) -> None:
    """Print the deploy-ready block with VPS docker commands.

    Why it exists: Tony runs the VPS commands manually after reviewing
    this output. Centralising the block keeps the formatting testable
    and ensures every deploy prints the same instructions.

    Args:
        agent_id:    The agent ID that was deployed.
        deploy_repo: Path to the local ai-agents repo clone.
    """
    typer.echo(_DEPLOY_DIVIDER)
    typer.echo(f"DEPLOY READY: {agent_id}")
    typer.echo(_DEPLOY_DIVIDER)
    typer.echo(f"Pushed to: {deploy_repo}")
    typer.echo("")
    typer.echo("Run on VPS:")
    typer.echo("  cd ~/ai-agents")
    typer.echo("  git pull")
    typer.echo(f"  docker build -t {agent_id} agents/{agent_id}/")
    typer.echo(f"  docker run -d \\")
    typer.echo(f"    --name {agent_id} \\")
    typer.echo(f"    --restart unless-stopped \\")
    typer.echo(f"    --env-file ~/ai-agents/.env \\")
    typer.echo(f"    {agent_id}")
    typer.echo(f"  docker logs {agent_id}")
    typer.echo("")
    typer.echo("After confirming live:")
    typer.echo(f"  bricklayer agent live --id {agent_id}")
    typer.echo(_DEPLOY_DIVIDER)


# ---------------------------------------------------------------------------
# agent deploy — run handler
# ---------------------------------------------------------------------------


def run_agent_deploy(root: Path, agent_id: str, deploy_repo: Path) -> int:
    """Copy a scaffolded agent to the deploy repo, push, and print VPS commands.

    Validates the agent exists in registry and on disk, copies the scaffold
    directory to ``deploy_repo/agents/<id>/``, commits and pushes via git,
    then updates the registry status to ``deployed``. The registry is NOT
    updated if the push fails.

    Args:
        root:        Repo root directory (parent of context/).
        agent_id:    ID of the agent to deploy.
        deploy_repo: Absolute path to the local clone of hermon1738/ai-agents.

    Returns:
        0 on success (files copied, committed, pushed, registry updated).
        1 on any error (message printed to stderr before return).

    Raises:
        Never raises. All error paths return 1.
    """
    # --- 1. Validate agent is in registry ---
    try:
        agent = get(root, agent_id)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        return 1

    if agent is None:
        typer.echo(f"error: agent '{agent_id}' not found in registry", err=True)
        return 1

    # --- 2. Validate source directory exists ---
    source_dir = root / "context" / "agents" / agent_id
    if not source_dir.exists():
        typer.echo(
            f"error: agent directory not found: context/agents/{agent_id}/\n"
            f"Run: bricklayer agent new --id {agent_id} --runtime ...",
            err=True,
        )
        return 1

    # --- 3. Validate deploy_repo is a real git repo ---
    if not deploy_repo.is_dir():
        typer.echo(
            f"error: deploy repo not found: {deploy_repo}\n"
            "Set DEPLOY_REPO_PATH to a local git clone of hermon1738/ai-agents.",
            err=True,
        )
        return 1

    rev_parse = _run_git(["rev-parse", "--git-dir"], deploy_repo)
    if rev_parse.returncode != 0:
        typer.echo(
            f"error: {deploy_repo} is not a git repository\n"
            "Set DEPLOY_REPO_PATH to a local git clone of hermon1738/ai-agents.",
            err=True,
        )
        return 1

    # --- 4. Copy agent directory to deploy repo (clean slate on every deploy) ---
    target_dir = deploy_repo / "agents" / agent_id
    # Delete-then-copy rather than dirs_exist_ok=True: files removed from
    # context/agents/<id>/ would otherwise persist as ghosts in the deploy repo
    # across re-deploys (D-027-adjacent concern for deploy).
    if target_dir.exists():
        shutil.rmtree(str(target_dir))
    shutil.copytree(str(source_dir), str(target_dir))

    # --- 5‒7. git add / commit / push — wrapped so TimeoutExpired from
    #          _run_git surfaces as a clean error rather than a raw traceback.
    try:
        git_add = _run_git(["add", f"agents/{agent_id}/"], deploy_repo)
        if git_add.returncode != 0:
            typer.echo(f"error: git add failed:\n{git_add.stderr}", err=True)
            return 1

        # --- 6. git commit ---
        runtime = agent.get("runtime", "unknown")
        project = agent.get("project", "unknown")
        commit_msg = (
            f"feat: add {agent_id}\n\n"
            f"- runtime: {runtime}\n"
            f"- project: {project}"
        )
        git_commit = _run_git(["commit", "-m", commit_msg], deploy_repo)
        if git_commit.returncode != 0:
            # "nothing to commit" means the agent files are unchanged since the
            # last deploy. Treat this as success — skip push and fall through to
            # print VPS commands so the operator still gets the docker block.
            combined = git_commit.stdout + git_commit.stderr
            if "nothing to commit" in combined or "nothing added to commit" in combined:
                typer.echo(
                    "No changes to push — agent already up to date in deploy repo"
                )
            else:
                typer.echo(f"error: git commit failed:\n{git_commit.stderr}", err=True)
                return 1
        else:
            # --- 7. git push — registry status NOT updated on failure ---
            git_push = _run_git(["push"], deploy_repo)
            if git_push.returncode != 0:
                typer.echo(
                    f"error: git push failed. Check your remote and credentials.\n"
                    f"{git_push.stderr}",
                    err=True,
                )
                return 1

    except RuntimeError as exc:
        # _run_git raises RuntimeError when subprocess.TimeoutExpired is caught.
        # Printing to stderr keeps the message clean — no raw traceback.
        typer.echo(f"error: {exc}", err=True)
        return 1

    # --- 8. Update registry status: stopped → deployed ---
    try:
        update_status(root, agent_id, "deployed")
    except ValueError as exc:
        # Registry update failed after a successful push — log but don't fail.
        # The agent is deployed; operator can manually update the registry.
        typer.echo(f"warning: registry update failed: {exc}", err=True)

    # --- 9. Print VPS commands ---
    _print_deploy_ready(agent_id, deploy_repo)
    return 0


# ---------------------------------------------------------------------------
# agent live — run handler
# ---------------------------------------------------------------------------


def run_agent_live(root: Path, agent_id: str) -> int:
    """Mark a deployed agent as live in the registry.

    Intended for manual invocation after Tony confirms the agent is running
    on the VPS (docker logs look good). Updates registry status from
    ``deployed`` to ``live``. If the agent is already ``live`` the command
    is idempotent and exits 0 with a message.

    Args:
        root:     Repo root directory (parent of context/).
        agent_id: ID of the agent to mark as live.

    Returns:
        0 on success or if already live.
        1 if the agent is not found or the registry is malformed.

    Raises:
        Never raises. All error paths return 1.
    """
    try:
        agent = get(root, agent_id)
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        return 1

    if agent is None:
        typer.echo(f"error: agent '{agent_id}' not found in registry", err=True)
        return 1

    if agent.get("status") == "live":
        # Idempotent — re-marking as live is not an error.
        typer.echo(f"Agent {agent_id} is already live")
        return 0

    try:
        update_status(root, agent_id, "live")
    except ValueError as exc:
        typer.echo(f"error: {exc}", err=True)
        return 1

    typer.echo(f"Agent {agent_id} marked as live")
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


@agent_app.command(name="new")
def agent_new(
    agent_id: str = typer.Option(..., "--id", help="Agent ID (e.g. idea-os-monitor-01)."),
    runtime: str = typer.Option(..., "--runtime", help="Runtime: nanobot or raw-python."),
    project: str = typer.Option(..., "--project", help="Project slug."),
    role: str = typer.Option(..., "--role", help="Role slug (e.g. monitor)."),
) -> None:
    """Scaffold a new agent directory and register it in registry.yaml."""
    # Import find_yaml here to keep it out of module-level scope — avoids
    # filesystem side-effects during unit test collection.
    from cli.config import find_yaml

    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)

    # Load bricklayer.yaml to resolve the nanobot template path.
    try:
        config: dict[str, Any] = yaml.safe_load(
            yaml_path.read_text(encoding="utf-8")
        ) or {}
    except yaml.YAMLError as exc:
        typer.echo(f"error: bricklayer.yaml is malformed — {exc}", err=True)
        raise typer.Exit(code=1)

    raise typer.Exit(
        code=run_agent_new(yaml_path.parent, agent_id, runtime, project, role, config)
    )


@agent_app.command(name="deploy")
def agent_deploy(
    agent_id: str = typer.Option(..., "--id", help="Agent ID to deploy."),
) -> None:
    """Copy agent to the ai-agents repo, push, and print VPS docker commands."""
    from cli.config import find_yaml

    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)

    # DEPLOY_REPO_PATH must be set by the operator before running deploy.
    deploy_repo_str = os.environ.get("DEPLOY_REPO_PATH")
    if not deploy_repo_str:
        typer.echo(
            "error: DEPLOY_REPO_PATH is not set.\n"
            "Set it to your local clone of hermon1738/ai-agents:\n"
            "  export DEPLOY_REPO_PATH=~/ai-agents",
            err=True,
        )
        raise typer.Exit(code=1)

    raise typer.Exit(
        code=run_agent_deploy(yaml_path.parent, agent_id, Path(deploy_repo_str))
    )


@agent_app.command(name="live")
def agent_live(
    agent_id: str = typer.Option(..., "--id", help="Agent ID to mark as live."),
) -> None:
    """Mark a deployed agent as live after VPS confirmation."""
    from cli.config import find_yaml

    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)

    raise typer.Exit(code=run_agent_live(yaml_path.parent, agent_id))
