"""Commit command: git commit wrapper with auto-tagged brick ID message."""

from __future__ import annotations

import json
import re
import subprocess as _subprocess
from pathlib import Path

import typer

STATE_RELPATH = "bricklayer/state.json"
_COAUTHOR = "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"


def _parse_brick(current_brick: str) -> tuple[str, str]:
    """Return (brick_number, brick_name) from 'Brick N - name' string."""
    m = re.match(r"Brick\s+([\d.]+)\s*[-\u2013]\s*(.*)", current_brick, re.IGNORECASE)
    if m:
        return m.group(1), m.group(2).strip()
    return "?", current_brick


def _check_staged(root: Path) -> list[str]:
    """Return list of staged files. Empty list if nothing staged or git error."""
    try:
        proc = _subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=str(root),
            stdout=_subprocess.PIPE,
            stderr=_subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return []
    return [f for f in proc.stdout.splitlines() if f.strip()]


def _build_message(brick_num: str, brick_name: str, user_msg: str) -> str:
    return (
        f"feat(brick-{brick_num}): {user_msg}\n\n"
        f"Brick: {brick_num} \u2014 {brick_name}\n"
        f"{_COAUTHOR}"
    )


def _do_commit(root: Path, message: str) -> tuple[int, str]:
    """Run git commit -m <message>. Returns (exit_code, output)."""
    try:
        proc = _subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(root),
            stdout=_subprocess.PIPE,
            stderr=_subprocess.STDOUT,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 1, "error: git executable not found"
    return proc.returncode, proc.stdout.strip()


def run_commit(root: Path, message: str) -> int:
    """Stage-aware git commit with auto-tagged brick ID. Returns 0/1."""
    if not message.strip():
        typer.echo("Commit message cannot be empty", err=True)
        return 1

    state_path = root / STATE_RELPATH
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: state.json is corrupt — {exc}", err=True)
        return 1

    brick_num, brick_name = _parse_brick(state.get("current_brick", ""))

    staged = _check_staged(root)
    if not staged:
        typer.echo("Nothing staged. Use git add first.", err=True)
        return 1

    full_msg = _build_message(brick_num, brick_name, message.strip())
    code, output = _do_commit(root, full_msg)
    if code != 0:
        typer.echo(f"error: git commit failed: {output}", err=True)
        return 1

    typer.echo(output)
    return 0
