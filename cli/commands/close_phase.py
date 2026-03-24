"""Close-phase command: merge current phase/* branch into parent feature/* branch."""

from __future__ import annotations

import json
import subprocess as _subprocess
from pathlib import Path

import typer

from cli.state import write as state_write

STATE_RELPATH = "bricklayer/state.json"


def _get_current_branch(root: Path) -> str | None:
    """Return the current git branch name, or None on failure."""
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


def _merge_no_ff(root: Path, branch: str, target: str) -> tuple[int, str]:
    """Checkout target, merge branch with --no-ff, delete branch."""
    checkout = _subprocess.run(
        ["git", "checkout", target],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        text=True,
        check=False,
    )
    if checkout.returncode != 0:
        return checkout.returncode, (
            f"error: git checkout {target} failed: {checkout.stdout.strip()}"
        )

    merge = _subprocess.run(
        ["git", "merge", "--no-ff", branch],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        text=True,
        check=False,
    )
    if merge.returncode != 0:
        return merge.returncode, (
            f"error: git merge --no-ff {branch} failed: {merge.stdout.strip()}"
        )

    _subprocess.run(
        ["git", "branch", "-d", branch],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
        check=False,
    )
    return 0, f"Merged {branch} → {target}. Branch deleted."


def run_close_phase(root: Path) -> int:
    """Merge current phase/* branch to its parent feature/* branch. Returns 0/1."""
    current = _get_current_branch(root)
    if current is None or not current.startswith("phase/"):
        typer.echo(
            f"error: close-phase must be run from a phase/* branch "
            f"(currently on '{current}')",
            err=True,
        )
        return 1

    state_path = root / STATE_RELPATH
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1

    try:
        raw_state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: state.json is corrupt — {exc}", err=True)
        return 1

    target = raw_state.get("current_feature")
    if not target:
        typer.echo(
            "error: current_feature not set in state.json — cannot determine merge target",
            err=True,
        )
        return 1

    code, msg = _merge_no_ff(root, current, target)
    typer.echo(msg)
    if code != 0:
        return 1

    state_write(state_path, {"current_branch": target, "current_phase": None})
    typer.echo(f"Phase merged to {target}. Start next phase with: bricklayer branch --phase N name")
    return 0
