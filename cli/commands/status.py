"""Status command: reads state.json + STATE.md, prints 5 fields."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer

from cli.state import load

STATE_MD_FILENAME = "STATE.md"
STATE_JSON_RELPATH = "bricklayer/state.json"

_FALLBACK = "(STATE.md not found)"


def _parse_state_md(root: Path) -> dict[str, str]:
    """Parse STATE.md key: value lines. Returns {} if file is missing."""
    p = root / STATE_MD_FILENAME
    if not p.exists():
        return {}
    result: dict[str, str] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip().lower()] = value.strip()
    return result


def run_status(root: Path) -> int:
    """Print the 5 status fields. Returns 0 on success, 1 on error."""
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
    last_action = f"Tests {last_run['status']} (exit {last_run['exit_code']})"
    next_cmd = state["next_action"]

    typer.echo(f"project:     {project}")
    typer.echo(f"phase:       {phase}")
    typer.echo(f"brick:       {brick}")
    typer.echo(f"last action: {last_action}")
    typer.echo(f"next:        {next_cmd}")

    return 0
