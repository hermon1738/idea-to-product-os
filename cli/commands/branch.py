"""Branch command: create and checkout brick/phase/feature branches.

WHY THIS EXISTS:
    The three-level branch hierarchy (feature → phase → brick) only provides
    safety guarantees if every branch is created from the correct parent.
    Without this command, developers could create a brick branch directly from
    main, bypassing the phase layer entirely — the merge routing in
    ``bricklayer build --verdict PASS`` would then silently merge to a stale
    or null target. This command enforces the parent-branch contract at
    creation time, not at merge time.

DESIGN DECISIONS:
- Enforce parent branch at creation rather than at merge time. Alternative
  was warning (not failing) when a branch is created from the wrong parent.
  Rejected because a warning is ignored under pressure; an exit 1 at creation
  forces the developer to fix the issue before any work is done on the branch.
- Use the branch prefix as the contract (``feature/``, ``phase/``, ``brick/``).
  Alternative was a separate config file mapping branch names to levels.
  Rejected because the prefix is self-documenting and works with standard
  git tooling without any extra config.
- Write state.json updates (current_feature, current_phase, current_branch)
  on branch creation. Alternative was writing them at merge time. Rejected
  because build --verdict PASS reads these fields to determine the merge
  target — if they are not set at creation, the first --verdict PASS call
  on a new branch would always fail with a null target error.
- Slugify branch name automatically. Alternative was requiring the user to
  supply a pre-slugified name. Rejected because a branch name with spaces
  would cause git to split the name into multiple arguments.
"""

from __future__ import annotations

import re
import subprocess as _subprocess
from pathlib import Path
from typing import Optional

import typer

from cli.state import write as state_write

# Relative path to state.json from the repo root.
STATE_RELPATH = "bricklayer/state.json"


def _slugify(name: str) -> str:
    """Convert a human-readable name to a lowercase-hyphenated git branch slug.

    Why it exists: Git branch names cannot contain spaces or most special
    characters. Without this function, a name like "Reddit Monitor" would
    create a branch named "feature/reddit monitor", which git would reject or
    misparse.

    Args:
        name: Raw name string (may contain spaces, uppercase, punctuation).

    Returns:
        Lowercase string with non-alphanumeric runs replaced by hyphens,
        with leading/trailing hyphens stripped.

    Example:
        ``_slugify("Reddit Monitor v2!")`` → ``"reddit-monitor-v2"``
    """
    slug = name.lower().strip()
    # Replace any run of characters that are not lowercase letters or digits
    # with a single hyphen — this normalises spaces, underscores, and
    # punctuation in one pass.
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def _get_current_branch(root: Path) -> str | None:
    """Return the current git branch name, or None if git fails or is absent.

    Why it exists: Parent-branch enforcement requires knowing the current
    branch before creating a new one. Without this, the branch command cannot
    detect that a brick branch is being created from main instead of a phase.

    Args:
        root: Repo root directory used as the git working directory.

    Returns:
        Current branch name string, or None if git is not installed
        (FileNotFoundError) or the command fails (non-zero exit).
    """
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
        # git is not on PATH — treat as unknown branch so callers can
        # surface a clean "cannot determine branch" error rather than a
        # raw FileNotFoundError traceback.
        return None
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def _git_create_checkout(root: Path, branch_name: str) -> tuple[int, str]:
    """Run ``git checkout -b <branch_name>`` and return (exit_code, output).

    Why it exists: Centralises the git create-and-checkout call so tests can
    mock it at a single point rather than patching subprocess.run globally and
    risking interference with unrelated subprocess calls in the same test.

    Args:
        root: Repo root directory used as the git working directory.
        branch_name: Fully-qualified branch name to create
                     (e.g. ``"brick/14-three-level-branching"``).

    Returns:
        Tuple of (exit_code, combined_output). output is stdout+stderr merged.
    """
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
    """Create and checkout a branch at the correct hierarchy level.

    Enforces the three-level parent contract:
    - ``--feature``: must be on ``main``
    - ``--phase``: must be on a ``feature/*`` branch
    - brick (no flag): must be on a ``phase/*`` branch

    Updates state.json fields (current_feature, current_phase, current_branch)
    on success so that ``bricklayer build --verdict PASS`` can route merges
    automatically.

    Why it exists: Without parent-branch enforcement, a developer (or AI) can
    accidentally create a brick branch from main, skipping the phase layer.
    The merge routing in build --verdict PASS would then read a null
    current_phase and exit 1 mid-merge — after the commit has already been
    made, leaving the branch in a detached state.

    Args:
        root: Repo root directory (contains bricklayer.yaml).
        number: Brick or phase number string (e.g. ``"14"``).
        name: Human-readable branch name (will be slugified).
        feature: If True, create a ``feature/`` branch from ``main``.
        phase: If True, create a ``phase/`` branch from a ``feature/*`` branch.

    Returns:
        0 on success, 1 on any error (wrong parent, missing args, git failure).
    """
    current = _get_current_branch(root)

    if feature:
        # --feature branches must originate from main so that feature/* is
        # always a direct child of main — this is required for close-feature
        # to merge feature/* back to main without conflicts from other features.
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
        # --phase branches must originate from a feature/* branch so that
        # phase/* is always a direct child of one feature — close-phase reads
        # current_feature from state.json to determine the merge target, and
        # that field is only set when a feature/* branch is active.
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
        # Brick branches must originate from a phase/* branch so that brick/*
        # is always a direct child of one phase — build --verdict PASS reads
        # current_phase from state.json to determine the merge target, and
        # that field is only set when a phase/* branch is active.
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

    # Update state.json after a successful branch creation so that subsequent
    # commands (build --verdict PASS, close-phase, close-feature) can read the
    # current hierarchy context without inspecting git directly.
    state_path = root / STATE_RELPATH
    if state_path.exists():
        if feature:
            # A new feature branch resets both phase and feature context —
            # there is no active phase yet.
            state_write(state_path, {
                "current_branch": branch_name,
                "current_feature": branch_name,
                "current_phase": None,
            })
        elif phase:
            # A new phase branch updates current_phase but preserves
            # current_feature — the feature context was set when the feature
            # branch was created and must not be clobbered.
            state_write(state_path, {
                "current_branch": branch_name,
                "current_phase": branch_name,
            })
        else:
            # A brick branch updates only current_branch — both current_feature
            # and current_phase remain set from when their branches were created.
            state_write(state_path, {"current_branch": branch_name})

    typer.echo(f"branch: {branch_name}")
    return 0
