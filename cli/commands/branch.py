"""Branch command: create and checkout brick/N-name or feature/name branches."""

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
) -> int:
    """Create and checkout a brick/N-name or feature/name branch."""
    if feature:
        # --feature: first positional arg is the feature name
        feature_name = name or number
        if not feature_name:
            typer.echo("error: name required (usage: bricklayer branch --feature name)", err=True)
            return 1
        branch_name = f"feature/{_slugify(feature_name)}"
    else:
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
        state_write(state_path, {"current_branch": branch_name})

    typer.echo(f"branch: {branch_name}")
    return 0
