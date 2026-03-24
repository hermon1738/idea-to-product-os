"""Branch command: create and checkout brick/phase/feature branches."""

from __future__ import annotations

import re
import subprocess as _subprocess
from pathlib import Path
from typing import Optional

import typer

from cli.state import write as state_write

STATE_RELPATH = "bricklayer/state.json"


def _slugify(name: str) -> str:
    """Convert name to lowercase-hyphenated slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


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


def _git_create_checkout(root: Path, branch_name: str) -> tuple[int, str]:
    """Run git checkout -b <branch_name>. Returns (exit_code, output)."""
    proc = _subprocess.run(
        ["git", "checkout", "-b", branch_name],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        text=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip()


def run_branch(
    root: Path,
    number: Optional[str],
    name: Optional[str],
    feature: bool = False,
    phase: bool = False,
) -> int:
    """Create and checkout a brick/phase/feature branch with parent validation."""
    current = _get_current_branch(root)

    if feature:
        # --feature: must be on main
        if current != "main":
            typer.echo(
                f"error: --feature branches must be created from main "
                f"(currently on '{current}')",
                err=True,
            )
            return 1
        feature_name = name or number
        if not feature_name:
            typer.echo(
                "error: name required (usage: bricklayer branch --feature name)", err=True
            )
            return 1
        branch_name = f"feature/{_slugify(feature_name)}"

    elif phase:
        # --phase N name: must be on a feature/* branch
        if current is None or not current.startswith("feature/"):
            typer.echo(
                f"error: --phase branches must be created from a feature/* branch "
                f"(currently on '{current}')",
                err=True,
            )
            return 1
        if number is None:
            typer.echo(
                "error: phase number required (usage: bricklayer branch --phase N name)",
                err=True,
            )
            return 1
        if name is None:
            typer.echo(
                "error: phase name required (usage: bricklayer branch --phase N name)",
                err=True,
            )
            return 1
        branch_name = f"phase/{number}-{_slugify(name)}"

    else:
        # Brick branch: must be on a phase/* branch
        if current is None or not current.startswith("phase/"):
            typer.echo(
                f"error: brick branches must be created from a phase/* branch "
                f"(currently on '{current}')",
                err=True,
            )
            return 1
        if number is None:
            typer.echo(
                "error: brick number required (usage: bricklayer branch N name)", err=True
            )
            return 1
        if name is None:
            typer.echo(
                "error: brick name required (usage: bricklayer branch N name)", err=True
            )
            return 1
        branch_name = f"brick/{number}-{_slugify(name)}"

    code, output = _git_create_checkout(root, branch_name)
    if code != 0:
        typer.echo(f"error: {output}", err=True)
        return 1

    state_path = root / STATE_RELPATH
    if state_path.exists():
        if feature:
            state_write(state_path, {
                "current_branch": branch_name,
                "current_feature": branch_name,
                "current_phase": None,
            })
        elif phase:
            state_write(state_path, {
                "current_branch": branch_name,
                "current_phase": branch_name,
            })
        else:
            state_write(state_path, {"current_branch": branch_name})

    typer.echo(f"branch: {branch_name}")
    return 0
