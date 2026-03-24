"""Next command: read next_action from state.json and print the next CLI command.

WHY THIS EXISTS:
    A developer resuming mid-brick needs to know the exact command to run next
    without reading state.json manually and translating a next_action string
    into a command. Without this command, every session restart requires the
    developer to remember the mapping between next_action values and CLI
    flags, and any mistake sends the pipeline into an invalid state.

DESIGN DECISIONS:
- Map next_action strings to CLI commands in a dict rather than an if/elif
  chain. Alternative was a series of if statements. Rejected because a dict
  is easier to extend (adding a new pipeline step is one line) and easier
  to inspect in isolation during testing.
- Fall back to echoing the next_action value unchanged when it is not in the
  routing table. Alternative was exiting 1 on unknown values. Rejected because
  the bricklayer tools (update_state.py) may write custom next_action values
  that are not yet in the routing table — falling back gracefully means the
  user still gets some information rather than a cryptic error.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer

from cli.state import load

# Relative path to state.json from the repo root.
STATE_JSON_RELPATH = "bricklayer/state.json"

# Maps each next_action identifier to the CLI command the user should run.
# The keys correspond to values written by _run_flag_tool(), run_skeptic_packet(),
# and update_state.py --complete. Any next_action not in this table is echoed
# verbatim (see DESIGN DECISIONS).
_ROUTING: dict[str, str] = {
    "snapshot_init": "bricklayer build --verify",
    "verify": "bricklayer build --test",
    "tests_passed": "bricklayer build --skeptic-packet",
    "skeptic_packet_ready": "bricklayer build --verdict PASS|FAIL",
    "brick_complete": "bricklayer build",
}


def run_next(root: Path) -> int:
    """Read next_action from state.json and print the corresponding CLI command.

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

    next_action: str = state["next_action"]
    # If next_action is not in the routing table (e.g. a custom value written
    # by a tool script), echo it unchanged so the user still sees something
    # useful rather than nothing.
    command = _ROUTING.get(next_action, next_action)
    typer.echo(command)
    return 0
