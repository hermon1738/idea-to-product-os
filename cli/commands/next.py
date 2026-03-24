"""Next command: reads next_action from state.json and prints the next CLI command."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer

from cli.state import load

STATE_JSON_RELPATH = "bricklayer/state.json"

# Maps the current next_action step identifier to the next CLI command to run.
_ROUTING: dict[str, str] = {
    "snapshot_init": "bricklayer build --verify",
    "verify": "bricklayer build --test",
    "tests_passed": "bricklayer build --skeptic-packet",
    "skeptic_packet_ready": "bricklayer build --verdict PASS|FAIL",
    "brick_complete": "bricklayer build",
}


def run_next(root: Path) -> int:
    """Print the next CLI command. Returns 0 on success, 1 on error."""
    state_path = root / STATE_JSON_RELPATH

    try:
        state: dict[str, Any] = load(state_path)
    except FileNotFoundError:
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1

    next_action: str = state["next_action"]
    command = _ROUTING.get(next_action, next_action)
    typer.echo(command)
    return 0
