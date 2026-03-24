"""Close-phase command: merge current phase/* branch into parent feature/* branch.

WHY THIS EXISTS:
    A phase groups a set of bricks that together achieve one vertical slice of
    a feature. Once all bricks in the phase are merged up from brick/* to
    phase/*, the phase must be merged into the feature branch so its work
    becomes part of the feature. Without this command, developers would need
    to do the merge manually, skipping the state.json update that sets
    current_phase to None. A non-null current_phase after the phase is closed
    would cause the next phase's bricks to merge into the old (now deleted)
    phase branch.

DESIGN DECISIONS:
- Read the merge target (current_feature) from state.json rather than from
  the git branch name. Alternative was parsing the phase branch name and
  inferring the feature (e.g. stripping ``phase/1-scaffold`` → look up
  ``feature/reddit-monitor``). Rejected because there is no reliable mapping
  from a phase name to a feature name in the branch name alone — two different
  features can have a phase with the same number and name.
- Enforce that the command is run from a ``phase/*`` branch. Alternative was
  inferring the phase branch from state.json and checking it out automatically.
  Rejected because auto-checkout is a silent action that could leave the user
  on an unexpected branch after the command finishes.
"""

from __future__ import annotations

import json
import subprocess as _subprocess
from pathlib import Path

import typer

from cli.state import write as state_write

# Relative path to state.json from the repo root.
STATE_RELPATH = "bricklayer/state.json"


def _get_current_branch(root: Path) -> str | None:
    """Return the current git branch name, or None if git fails or is absent.

    Why it exists: close-phase must verify it is running from a phase/* branch
    before attempting the merge. Without this check, the command could
    silently merge the wrong branch into the feature.

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
        # git is not on PATH — return None so the caller surfaces a clean
        # error rather than a raw FileNotFoundError traceback.
        return None
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def _merge_no_ff(root: Path, branch: str, target: str) -> tuple[int, str]:
    """Checkout target, merge branch with --no-ff, delete branch.

    Why it exists: The checkout-merge-delete sequence needs to happen as one
    logical operation. Inlining it in run_close_phase would make the function
    body hard to follow and difficult to test in isolation.

    Args:
        root: Repo root directory used as the git working directory.
        branch: Fully-qualified name of the phase branch to merge
                (e.g. ``"phase/1-scaffold"``).
        target: Feature branch name to merge into
                (e.g. ``"feature/reddit-monitor"``).

    Returns:
        Tuple of (exit_code, message). exit_code is 0 on success. message
        describes the outcome for both success and failure.
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

    # Best-effort branch deletion after a successful merge.
    _subprocess.run(
        ["git", "branch", "-d", branch],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
        check=False,
    )
    return 0, f"Merged {branch} → {target}. Branch deleted."


def run_close_phase(root: Path) -> int:
    """Merge current phase/* branch into its parent feature/* branch.

    Reads the merge target from state.json ``current_feature`` rather than
    inferring it from the branch name (see DESIGN DECISIONS). On success,
    clears ``current_phase`` in state.json so the next phase can start fresh.

    Why it exists: See module docstring. The key value-add over a raw
    ``git merge`` is the state.json update — without setting current_phase
    to None, the next brick created on the new phase would route its
    --verdict PASS merge to the closed (deleted) old phase branch.

    Args:
        root: Repo root directory (contains bricklayer.yaml).

    Returns:
        0 on success. 1 if not on a phase/* branch, if state.json is missing
        or corrupt, if current_feature is not set, or if the merge fails.
    """
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

    # current_feature is set by ``bricklayer branch --feature`` and must be
    # present for the merge to have a valid target.
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

    # Clear current_phase after a successful merge so the next phase created
    # on this feature does not inherit the closed phase's name as its target.
    state_write(state_path, {"current_branch": target, "current_phase": None})
    typer.echo(f"Phase merged to {target}. Start next phase with: bricklayer branch --phase N name")
    return 0
