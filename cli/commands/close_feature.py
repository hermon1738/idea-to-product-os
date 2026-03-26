"""Close-feature command: merge current feature/* branch into main.

WHY THIS EXISTS:
    A feature represents a complete, releasable body of work. Once all its
    phases are done, the feature branch must be merged to main so the work
    becomes the new stable baseline. Without this command, the merge step
    would be done manually with raw git, bypassing the state.json cleanup
    (clearing current_feature and current_phase) that the rest of the pipeline
    depends on. A stale current_feature value in state.json would then cause
    the next feature's close-phase to merge into the wrong target.

DESIGN DECISIONS:
- Enforce that the command only runs from a ``feature/*`` branch. Alternative
  was silently inferring the feature branch from state.json. Rejected because
  inference is invisible — the user could be on an unexpected branch and have
  no idea why the merge went to the wrong place.
- Clear both current_feature and current_phase in state.json on success.
  Alternative was clearing only current_feature. Rejected because a leftover
  current_phase value from the closed feature could cause the next feature's
  first --verdict PASS to merge a brick into a phase from the old feature.
- Deduplicate the _get_current_branch and _merge_no_ff helpers here rather
  than importing from build.py. Alternative was importing those functions from
  build.py. Considered but rejected to keep the close-feature module
  independently loadable — importing from build.py would drag in the entire
  build command dependency tree, which includes heavier imports like the
  spec parser.
- Explicitly write ``current_brick: ""`` in the post-merge state_write.
  Alternative was omitting it and letting deep-merge preserve the existing
  value. Rejected because the existing value may be null when all bricks in
  the feature's final phase were closed before close-feature runs. A null
  current_brick fails schema validation and crashes the state write after the
  git merge already succeeded, leaving state inconsistent (D-038, Brick 26).
"""

from __future__ import annotations

import subprocess as _subprocess
from pathlib import Path

import typer

from cli.state import write as state_write

# Relative path to state.json from the repo root.
STATE_RELPATH = "bricklayer/state.json"


def _get_current_branch(root: Path) -> str | None:
    """Return the current git branch name, or None if git fails or is absent.

    Why it exists: close-feature must verify it is running from a feature/*
    branch before attempting the merge. Without this check, running it from
    main or a brick branch would try to merge main into itself or merge an
    incomplete brick into main.

    Args:
        root: Repo root directory used as the git working directory.

    Returns:
        Current branch name string, or None if git is not installed
        (FileNotFoundError) or returns a non-zero exit code.
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
        # git is not on PATH — return None so the caller can surface a clean
        # error message rather than an unhandled traceback.
        return None
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def _merge_no_ff(root: Path, branch: str, target: str) -> tuple[int, str]:
    """Checkout target, merge branch with --no-ff, delete branch.

    Why it exists: The checkout-merge-delete sequence must be done atomically
    from the caller's perspective. Inlining it in run_close_feature would make
    the function hard to read and hard to test in isolation.

    Args:
        root: Repo root directory used as the git working directory.
        branch: Fully-qualified name of the branch to merge
                (e.g. ``"feature/reddit-monitor"``).
        target: Name of the branch to merge into (e.g. ``"main"``).

    Returns:
        Tuple of (exit_code, message). exit_code is 0 on success. message
        describes what happened for both success and failure.
    """
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

    # Best-effort branch deletion after a successful merge. If deletion fails
    # (rare, e.g. file lock on Windows), the merge is still complete and the
    # user can delete the branch manually.
    _subprocess.run(
        ["git", "branch", "-d", branch],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
        check=False,
    )
    return 0, f"Merged {branch} → {target}. Branch deleted."


def run_close_feature(root: Path) -> int:
    """Merge current feature/* branch into main and clear feature context.

    Enforces that the command is run from a feature/* branch. On success,
    clears current_feature and current_phase in state.json so the pipeline
    state reflects that no feature is active.

    Why it exists: See module docstring. The key behaviour beyond a raw
    ``git merge`` is the state.json cleanup — without it, subsequent commands
    would target stale feature/phase branches.

    Args:
        root: Repo root directory (contains bricklayer.yaml).

    Returns:
        0 on success. 1 if not on a feature/* branch, if git fails, or if
        the merge conflicts.
    """
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

    # Clear all feature/phase context from state.json so the next feature
    # starts from a clean slate. Leaving stale values would cause close-phase
    # on the next feature to merge into the old feature branch, which has
    # already been deleted.
    # current_brick is coerced to "" for the same reason as close_phase: the
    # existing state may have null there, which fails schema validation and
    # crashes the state write after the merge already succeeded (D-038,
    # fixed in Brick 26).
    state_path = root / STATE_RELPATH
    if state_path.exists():
        state_write(state_path, {
            "current_branch": "main",
            "current_feature": None,
            "current_phase": None,
            "current_brick": "",
        })

    typer.echo("Feature merged to main. Branch deleted.")
    return 0
