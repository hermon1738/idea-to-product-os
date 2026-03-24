"""Pause command: write HANDOFF.json and .continue-here.md for session handoff."""

from __future__ import annotations

import datetime
import json
import re
import subprocess as _subprocess
from pathlib import Path
from typing import Any

import typer

STATE_RELPATH = "bricklayer/state.json"
HANDOFF_RELPATH = "HANDOFF.json"
CONTINUE_RELPATH = ".continue-here.md"

_NEXT_COMMAND_ROUTING: dict[str, str] = {
    "snapshot_init": "bricklayer build --snapshot",
    "verify": "bricklayer build --verify",
    "tests_passed": "bricklayer build --skeptic-packet",
    "skeptic_packet_ready": "bricklayer build --verdict PASS|FAIL",
    "brick_complete": "bricklayer next",
}


def _get_current_branch(root: Path) -> str:
    proc = _subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return proc.stdout.strip()
    return "unknown"


def _parse_brick(current_brick: str) -> tuple[str, str]:
    """Return (brick_number, brick_name) from 'Brick N - name' string."""
    m = re.match(r"Brick\s+([\d.]+)\s*[-\u2013]\s*(.*)", current_brick, re.IGNORECASE)
    if m:
        return m.group(1), m.group(2).strip()
    return "?", current_brick


def _next_command(next_action: str) -> str:
    return _NEXT_COMMAND_ROUTING.get(
        next_action, f"bricklayer next  # {next_action}"
    )


def _build_handoff(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    current_brick = state.get("current_brick", "")
    brick_num, brick_name = _parse_brick(current_brick)
    next_action = str(state.get("next_action", ""))
    branch = _get_current_branch(root)
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "project": root.name,
        "brick": brick_num,
        "brick_name": brick_name,
        "last_action": next_action,
        "loop_count": state.get("loop_count", 0),
        "current_branch": branch,
        "timestamp": ts,
        "next_command": _next_command(next_action),
    }


def _build_continue_md(handoff: dict[str, Any]) -> str:
    lines = [
        f"Last session ended: {handoff['timestamp']}",
        f"Project: {handoff['project']}",
        f"Branch: {handoff['current_branch']}",
        f"Current brick: Brick {handoff['brick']} — {handoff['brick_name']}",
        f"Last action: {handoff['last_action']}",
        f"Next command: {handoff['next_command']}",
        "Blockers: none",
    ]
    return "\n".join(lines) + "\n"


def run_pause(root: Path) -> int:
    """Write HANDOFF.json and .continue-here.md. Returns 0 on success, 1 on error."""
    state_path = root / STATE_RELPATH
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: state.json is corrupt — {exc}", err=True)
        return 1

    handoff = _build_handoff(root, state)
    continue_md = _build_continue_md(handoff)

    handoff_path = root / HANDOFF_RELPATH
    continue_path = root / CONTINUE_RELPATH

    # Write HANDOFF.json first. If the second write fails, remove it so
    # neither file is left in a partial state.
    try:
        handoff_path.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        typer.echo(f"error: could not write {HANDOFF_RELPATH}: {exc}", err=True)
        return 1

    try:
        continue_path.write_text(continue_md, encoding="utf-8")
    except OSError as exc:
        typer.echo(f"error: could not write {CONTINUE_RELPATH}: {exc}", err=True)
        handoff_path.unlink(missing_ok=True)
        return 1

    typer.echo(f"written: {HANDOFF_RELPATH}")
    typer.echo(f"written: {CONTINUE_RELPATH}")
    return 0
