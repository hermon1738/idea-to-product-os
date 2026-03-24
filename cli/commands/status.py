"""Status command: print current brick, last test result, and next action.

WHY THIS EXISTS:
    A developer (or AI) picking up a session needs to know the pipeline state
    at a glance without opening state.json and STATE.md manually. Without this
    command, the "what is happening right now?" question requires reading two
    files and mentally merging them. This command assembles the answer into
    five labelled lines that can be read in under five seconds.

DESIGN DECISIONS:
- Read both state.json (for pipeline data) and STATE.md (for project/phase
  labels). Alternative was reading state.json only. Rejected because the
  project name and phase label are written by close-session into STATE.md and
  are not duplicated in state.json — they are needed for a complete status
  line.
- Return ``_FALLBACK`` (not an error) when STATE.md is missing. Alternative
  was exiting 1 if STATE.md is absent. Rejected because STATE.md is generated
  by close-session (an optional step), and its absence should not block a
  developer from checking pipeline status.
- Parse STATE.md as ``key: value`` lines rather than a structured format.
  Alternative was JSON or YAML. Rejected because STATE.md is also read by
  humans — plain ``key: value`` is readable without a parser and writable
  by the Groq sprint review output.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer

from cli.state import load

# Relative path to state.json from the repo root.
STATE_JSON_RELPATH = "bricklayer/state.json"

# Filename of the project-state markdown file written by close-session.
STATE_MD_FILENAME = "STATE.md"

# Value shown when STATE.md is missing — tells the user why the field is
# empty rather than leaving it blank.
_FALLBACK = "(STATE.md not found)"


def _parse_state_md(root: Path) -> dict[str, str]:
    """Parse STATE.md into a key → value dict.

    Why it exists: run_status needs project and phase labels that are stored
    in STATE.md, not in state.json. Without this parser, run_status would need
    to open and parse STATE.md inline, mixing I/O with display logic.

    Args:
        root: Repo root directory (STATE.md is expected at root level).

    Returns:
        Dict of lowercased key → stripped value for each ``key: value`` line
        in STATE.md. Returns empty dict if STATE.md does not exist.
    """
    p = root / STATE_MD_FILENAME
    if not p.exists():
        # STATE.md is optional — only present after close-session has run.
        return {}
    result: dict[str, str] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            # Lowercase the key for case-insensitive lookup (STATE.md keys
            # are written in Title Case by _write_state_md in close_session.py).
            result[key.strip().lower()] = value.strip()
    return result


def run_status(root: Path) -> int:
    """Print five pipeline status fields to stdout.

    Combines data from state.json (pipeline state) and STATE.md (project
    labels) into a single aligned status block.

    Why it exists: See module docstring.

    Args:
        root: Repo root directory (contains bricklayer/state.json).

    Returns:
        0 on success. 1 if state.json is not found or fails schema validation.
    """
    state_path = root / STATE_JSON_RELPATH

    try:
        state: dict[str, Any] = load(state_path)
    except FileNotFoundError:
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1

    md = _parse_state_md(root)

    project = md.get("project", _FALLBACK)
    phase = md.get("phase", _FALLBACK)
    brick = state["current_brick"]
    last_run = state["last_test_run"]
    # Combine test status and exit code into a single readable line rather
    # than printing two separate fields that require mental assembly.
    last_action = f"Tests {last_run['status']} (exit {last_run['exit_code']})"
    next_cmd = state["next_action"]

    typer.echo(f"project:     {project}")
    typer.echo(f"phase:       {phase}")
    typer.echo(f"brick:       {brick}")
    typer.echo(f"last action: {last_action}")
    typer.echo(f"next:        {next_cmd}")

    return 0
