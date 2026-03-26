"""Tests for Brick 26 fixes — null current_brick on close-phase/close-feature.

WHY THIS EXISTS:
    close-phase and close-feature call state_write() after a successful merge.
    If current_brick in state.json is null (JSON null → Python None), the
    deep-merge preserves the null and the schema validator raises ValueError
    because current_brick must be a str. The merge already happened in git —
    a ValueError here leaves the repo in an inconsistent state where the merge
    is real but state.json still shows the old phase/feature as open.

    These tests verify that:
    1. Adding ``current_brick: ""`` to the state_write call in both commands
       prevents the ValueError on any state where current_brick is null.
    2. Commands that already have a valid string current_brick see no behavior
       change (non-regression).

DESIGN DECISIONS:
- Simulate the merge with a real temporary git repo rather than mocking
  subprocess. Alternative was patching _merge_no_ff to return (0, "ok").
  Rejected because that approach bypasses the git operations entirely — it
  cannot catch regressions where a change to the git call signature breaks
  the merge before the state write even runs.
- Write state.json with null current_brick directly via json.dumps() rather
  than via cli.state.write(). Alternative was using state.write() with
  {"current_brick": None}. Rejected because state.write() validates the
  merged result before writing — it would reject the null itself, making it
  impossible to set up the pre-fix failure condition in a test.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.close_phase import run_close_phase  # noqa: E402
from cli.commands.close_feature import run_close_feature  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Minimal state.json with null current_brick — the exact failure condition
# logged in D-038. JSON null maps to Python None, which fails the str check
# in _validate(). The rest of the fields are valid so the only fault is the
# null current_brick.
_NULL_BRICK_STATE: dict = {
    "current_brick": None,          # ← the bug trigger (null in JSON)
    "status": "COMPLETED",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": ["Brick 1"],
    "next_action": "close phase",
    "current_branch": "phase/1-test",
    "current_feature": "feature/test-flow",
    "current_phase": "phase/1-test",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}

_VALID_BRICK_STATE: dict = {
    **_NULL_BRICK_STATE,
    "current_brick": "Brick 1 - scaffold",   # ← valid string
}


def _git(args: list[str], cwd: Path) -> None:
    """Run a git command in ``cwd``, raise on non-zero exit code.

    Why it exists: Every helper that calls git needs consistent error handling.
    A bare subprocess.run(..., check=True) gives an unreadable CalledProcessError
    — this wrapper re-raises with a message that names the failing command and
    its stderr output so test failures are immediately actionable.

    Args:
        args: git sub-command and arguments (without the leading "git").
        cwd: Directory in which to run the command.

    Raises:
        RuntimeError: If git returns a non-zero exit code.
    """
    result = subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed in {cwd}:\n{result.stderr.strip()}"
        )


def _make_phase_repo(
    tmp_path: Path,
    state: dict,
    phase_branch: str = "phase/1-test",
    feature_branch: str = "feature/test-flow",
) -> Path:
    """Initialise a temporary git repo checked out on a phase/* branch.

    Sets up main → feature/* → phase/* branch hierarchy with state.json
    written directly (bypassing schema validation so tests can inject null
    current_brick).

    Args:
        tmp_path: Base directory for the repo (pytest tmp_path or sub-dir).
        state: Dict to write directly as state.json content.
        phase_branch: Name of the phase branch to check out at the end.
        feature_branch: Name of the feature branch (parent of phase).

    Returns:
        Path to the repo root (tmp_path).
    """
    _git(["init", "-b", "main"], tmp_path)
    _git(["config", "user.email", "test@test.com"], tmp_path)
    _git(["config", "user.name", "Test"], tmp_path)

    # Commit something to main so branches have a common ancestor.
    readme = tmp_path / "README.md"
    readme.write_text("test repo\n", encoding="utf-8")
    _git(["add", "README.md"], tmp_path)
    _git(["commit", "-m", "init"], tmp_path)

    # Create the bricklayer directory and write state.json directly (bypass
    # cli.state.write so we can inject null current_brick without validation).
    bl_dir = tmp_path / "bricklayer"
    bl_dir.mkdir()
    state_path = bl_dir / "state.json"
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    # Commit state.json to main so it exists on all branches.
    _git(["add", "bricklayer/state.json"], tmp_path)
    _git(["commit", "-m", "add state"], tmp_path)

    # Build the branch hierarchy: main → feature → phase.
    # Each branch is distinct — passing the same name for both would cause
    # git checkout -b to fail with "branch already exists".
    _git(["checkout", "-b", feature_branch], tmp_path)
    _git(["checkout", "-b", phase_branch], tmp_path)

    return tmp_path


def _make_feature_repo(
    tmp_path: Path,
    state: dict,
    feature_branch: str = "feature/test-flow",
) -> Path:
    """Initialise a temporary git repo checked out on a feature/* branch.

    Used for close-feature tests, which must run from a feature/* branch
    (not a phase branch). Does not create a phase branch.

    Args:
        tmp_path: Base directory for the repo (pytest tmp_path or sub-dir).
        state: Dict to write directly as state.json content.
        feature_branch: Name of the feature branch to check out.

    Returns:
        Path to the repo root (tmp_path).
    """
    _git(["init", "-b", "main"], tmp_path)
    _git(["config", "user.email", "test@test.com"], tmp_path)
    _git(["config", "user.name", "Test"], tmp_path)

    readme = tmp_path / "README.md"
    readme.write_text("test repo\n", encoding="utf-8")
    _git(["add", "README.md"], tmp_path)
    _git(["commit", "-m", "init"], tmp_path)

    bl_dir = tmp_path / "bricklayer"
    bl_dir.mkdir()
    state_path = bl_dir / "state.json"
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    _git(["add", "bricklayer/state.json"], tmp_path)
    _git(["commit", "-m", "add state"], tmp_path)

    # One level of branching only — feature/* directly from main.
    _git(["checkout", "-b", feature_branch], tmp_path)

    return tmp_path


# ---------------------------------------------------------------------------
# Fix 1 — close-phase: null current_brick → no crash
# ---------------------------------------------------------------------------


def test_close_phase_null_current_brick_exits_zero(tmp_path: Path) -> None:
    """close-phase with null current_brick exits 0 after a successful merge.

    Before the fix, state_write raised ValueError because the deep-merge
    preserved the null from the existing state. The merge itself had already
    succeeded — the ValueError only appeared in the state update step.
    """
    repo = _make_phase_repo(tmp_path, _NULL_BRICK_STATE)
    exit_code = run_close_phase(repo)
    assert exit_code == 0, "Expected exit 0 — ValueError from null current_brick?"


def test_close_phase_null_current_brick_state_updated(tmp_path: Path) -> None:
    """After close-phase, current_phase is None and current_brick is '' in state.

    Verifies that the state write completed — not just that the command exited 0.
    If the state was not written, the next phase would inherit the closed phase
    name as its merge target.
    """
    repo = _make_phase_repo(tmp_path, _NULL_BRICK_STATE)
    run_close_phase(repo)
    state_path = repo / "bricklayer" / "state.json"
    written = json.loads(state_path.read_text(encoding="utf-8"))
    assert written["current_phase"] is None
    assert written["current_brick"] == ""


def test_close_phase_valid_current_brick_unchanged_behavior(tmp_path: Path) -> None:
    """close-phase with a valid string current_brick exits 0 (non-regression).

    Ensures the fix does not break the normal (non-null) case.
    """
    repo = _make_phase_repo(tmp_path, _VALID_BRICK_STATE)
    exit_code = run_close_phase(repo)
    assert exit_code == 0


# ---------------------------------------------------------------------------
# Fix 1 — close-feature: null current_brick → no crash
# ---------------------------------------------------------------------------

# State for close-feature tests: current_branch points to the feature branch
# because close-feature enforces that the command runs from a feature/* branch.
_NULL_BRICK_FEATURE_STATE: dict = {
    **_NULL_BRICK_STATE,
    "current_branch": "feature/test-flow",
}


def test_close_feature_null_current_brick_exits_zero(tmp_path: Path) -> None:
    """close-feature with null current_brick exits 0 after a successful merge.

    Same root cause as close-phase: the deep-merge preserves null, which
    then fails schema validation in state_write. The git merge succeeded
    but the state write crashed, leaving current_feature stale in state.json.
    """
    repo = _make_feature_repo(tmp_path, _NULL_BRICK_FEATURE_STATE)
    exit_code = run_close_feature(repo)
    assert exit_code == 0, "Expected exit 0 — ValueError from null current_brick?"


def test_close_feature_null_current_brick_state_cleared(tmp_path: Path) -> None:
    """After close-feature, current_feature/phase are None and current_brick is ''.

    Confirms the state write completed so the pipeline slate is clean for the
    next feature.
    """
    repo = _make_feature_repo(tmp_path, _NULL_BRICK_FEATURE_STATE)
    run_close_feature(repo)
    state_path = repo / "bricklayer" / "state.json"
    written = json.loads(state_path.read_text(encoding="utf-8"))
    assert written["current_feature"] is None
    assert written["current_phase"] is None
    assert written["current_brick"] == ""
