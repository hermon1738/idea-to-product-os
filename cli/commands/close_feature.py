"""Close-feature command: merge current feature/* branch into main."""

from __future__ import annotations

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


def run_close_feature(root: Path) -> int:
    """Merge current feature/* branch to main. Returns 0/1."""
    current = _get_current_branch(root)
    if current is None or not current.startswith("feature/"):
        typer.echo(
            f"error: close-feature must be run from a feature/* branch "
            f"(currently on '{current}')",
            err=True,
        )
        return 1

    code, msg = _merge_no_ff(root, current, "main")
    typer.echo(msg)
    if code != 0:
        return 1

    state_path = root / STATE_RELPATH
    if state_path.exists():
        state_write(state_path, {
            "current_branch": "main",
            "current_feature": None,
            "current_phase": None,
        })

    typer.echo("Feature merged to main. Branch deleted.")
    return 0
