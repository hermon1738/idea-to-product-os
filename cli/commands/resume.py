"""Resume command: read HANDOFF.json and print formatted session context."""

from __future__ import annotations

import json
import subprocess as _subprocess
from pathlib import Path

import typer

HANDOFF_RELPATH = "HANDOFF.json"

_REQUIRED_FIELDS = (
    "project",
    "brick",
    "brick_name",
    "last_action",
    "loop_count",
    "current_branch",
    "timestamp",
    "next_command",
)

_RULE = "━" * 38


def _get_current_branch(root: Path) -> str | None:
    try:
        proc = _subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(root),
            stdout=_subprocess.PIPE,
            stderr=_subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def _format_block(h: dict) -> str:
    lines = [
        _RULE,
        "RESUMING SESSION",
        _RULE,
        f"Project:      {h['project']}",
        f"Branch:       {h['current_branch']}",
        f"Brick:        {h['brick']} — {h['brick_name']}",
        f"Last action:  {h['last_action']}",
        f"Loop count:   {h['loop_count']}",
        f"Paused at:    {h['timestamp']}",
        _RULE,
        f"Next command: {h['next_command']}",
        _RULE,
    ]
    return "\n".join(lines)


def run_resume(root: Path) -> int:
    """Read HANDOFF.json and print session context. Returns 0 on success, 1 on error."""
    handoff_path = root / HANDOFF_RELPATH

    if not handoff_path.exists():
        typer.echo(
            "No session to resume. Run bricklayer pause first.", err=True
        )
        return 1

    try:
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: HANDOFF.json is malformed — {exc}", err=True)
        return 1

    for field in _REQUIRED_FIELDS:
        if field not in handoff:
            typer.echo(
                f"error: HANDOFF.json is missing required field '{field}'", err=True
            )
            return 1

    typer.echo(_format_block(handoff))

    # Branch mismatch warning (non-fatal)
    expected = handoff["current_branch"]
    current = _get_current_branch(root)
    if current is not None and current != expected:
        typer.echo(
            f"Warning: you are on {current} but session was paused on {expected}."
            f" Switch with: git checkout {expected}"
        )

    return 0
