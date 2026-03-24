"""Tests for Brick 14 — three-level branching (feature/phase/brick)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.branch import run_branch  # noqa: E402
from cli.commands.close_feature import run_close_feature  # noqa: E402
from cli.commands.close_phase import run_close_phase  # noqa: E402
from cli.main import app  # noqa: E402

cli_runner = CliRunner()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_BASE_STATE: dict[str, Any] = {
    "current_brick": "Brick 14 - three-level-branching",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": [],
    "next_action": "snapshot_init",
    "last_test_run": {
        "command": "pytest",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "test_output.txt",
    },
}


def _write_state(root: Path, extra: dict | None = None) -> Path:
    (root / "bricklayer").mkdir(exist_ok=True)
    state = {**_BASE_STATE, **(extra or {})}
    path = root / "bricklayer" / "state.json"
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    return path


def _read_state(root: Path) -> dict:
    return json.loads((root / "bricklayer" / "state.json").read_text(encoding="utf-8"))


def _fake_git_current(branch: str):
    """Side-effect that returns the given branch for rev-parse calls."""
    def _side(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = branch + "\n"
        return m
    return _side


def _fake_checkout_ok(branch: str):
    """Side-effect: checkout succeeds, subsequent calls succeed."""
    def _side(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = f"Switched to branch '{branch}'\n"
        return m
    return _side


# ---------------------------------------------------------------------------
# branch.py — feature branch creation
# ---------------------------------------------------------------------------


def test_feature_branch_created_from_main(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="main"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")) as mock_git:
        result = run_branch(tmp_path, None, "my-feature", feature=True)
    assert result == 0
    mock_git.assert_called_once_with(tmp_path, "feature/my-feature")


def test_feature_branch_slugifies_name(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="main"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")) as mock_git:
        run_branch(tmp_path, None, "My Feature Name", feature=True)
    mock_git.assert_called_once_with(tmp_path, "feature/my-feature-name")


def test_feature_branch_updates_state(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="main"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
        run_branch(tmp_path, None, "my-feature", feature=True)
    state = _read_state(tmp_path)
    assert state["current_branch"] == "feature/my-feature"
    assert state.get("current_feature") == "feature/my-feature"
    assert state.get("current_phase") is None


def test_feature_branch_from_non_main_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="some-other-branch"):
        result = run_branch(tmp_path, None, "my-feature", feature=True)
    assert result == 1
    assert "main" in capsys.readouterr().err


def test_feature_branch_from_phase_branch_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="phase/1-scaffold"):
        result = run_branch(tmp_path, None, "my-feature", feature=True)
    assert result == 1


def test_feature_branch_from_brick_branch_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="brick/14-foo"):
        result = run_branch(tmp_path, None, "my-feature", feature=True)
    assert result == 1


def test_feature_branch_no_name_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="main"):
        result = run_branch(tmp_path, None, None, feature=True)
    assert result == 1
    assert "name required" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# branch.py — phase branch creation
# ---------------------------------------------------------------------------


def test_phase_branch_created_from_feature(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")) as mock_git:
        result = run_branch(tmp_path, "1", "scaffold", phase=True)
    assert result == 0
    mock_git.assert_called_once_with(tmp_path, "phase/1-scaffold")


def test_phase_branch_updates_state(tmp_path: Path) -> None:
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.branch._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
        run_branch(tmp_path, "1", "scaffold", phase=True)
    state = _read_state(tmp_path)
    assert state["current_branch"] == "phase/1-scaffold"
    assert state.get("current_phase") == "phase/1-scaffold"
    # current_feature must be preserved
    assert state.get("current_feature") == "feature/my-feature"


def test_phase_branch_from_main_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="main"):
        result = run_branch(tmp_path, "1", "scaffold", phase=True)
    assert result == 1
    err = capsys.readouterr().err
    assert "feature/" in err


def test_phase_branch_from_brick_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="brick/14-foo"):
        result = run_branch(tmp_path, "1", "scaffold", phase=True)
    assert result == 1


def test_phase_branch_missing_number_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="feature/foo"):
        result = run_branch(tmp_path, None, "scaffold", phase=True)
    assert result == 1
    assert "number required" in capsys.readouterr().err


def test_phase_branch_missing_name_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="feature/foo"):
        result = run_branch(tmp_path, "1", None, phase=True)
    assert result == 1
    assert "name required" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# branch.py — brick branch creation
# ---------------------------------------------------------------------------


def test_brick_branch_created_from_phase(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")) as mock_git:
        result = run_branch(tmp_path, "14", "three-level-branching")
    assert result == 0
    mock_git.assert_called_once_with(tmp_path, "brick/14-three-level-branching")


def test_brick_branch_updates_state(tmp_path: Path) -> None:
    _write_state(tmp_path, {
        "current_feature": "feature/my-feature",
        "current_phase": "phase/1-scaffold",
    })
    with patch("cli.commands.branch._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
        run_branch(tmp_path, "14", "three-level-branching")
    state = _read_state(tmp_path)
    assert state["current_branch"] == "brick/14-three-level-branching"
    # feature and phase must be preserved
    assert state.get("current_feature") == "feature/my-feature"
    assert state.get("current_phase") == "phase/1-scaffold"


def test_brick_branch_from_main_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="main"):
        result = run_branch(tmp_path, "14", "foo")
    assert result == 1
    assert "phase/" in capsys.readouterr().err


def test_brick_branch_from_feature_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="feature/foo"):
        result = run_branch(tmp_path, "14", "foo")
    assert result == 1


def test_brick_branch_missing_number_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="phase/1-scaffold"):
        result = run_branch(tmp_path, None, "foo")
    assert result == 1


def test_brick_branch_missing_name_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.branch._get_current_branch", return_value="phase/1-scaffold"):
        result = run_branch(tmp_path, "14", None)
    assert result == 1


# ---------------------------------------------------------------------------
# close_phase.py
# ---------------------------------------------------------------------------


def _subprocess_side_effects(*calls):
    """Return a side_effect list for sequential subprocess.run calls."""
    return list(calls)


def _mock_proc(returncode: int, stdout: str = "") -> MagicMock:
    m = MagicMock()
    m.returncode = returncode
    m.stdout = stdout
    return m


def test_close_phase_merges_to_feature(tmp_path: Path) -> None:
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.close_phase._subprocess.run", side_effect=[
             _mock_proc(0),  # checkout feature/my-feature
             _mock_proc(0),  # merge --no-ff phase/1-scaffold
             _mock_proc(0),  # branch -d phase/1-scaffold
         ]):
        result = run_close_phase(tmp_path)
    assert result == 0


def test_close_phase_updates_state(tmp_path: Path) -> None:
    _write_state(tmp_path, {
        "current_feature": "feature/my-feature",
        "current_phase": "phase/1-scaffold",
    })
    with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.close_phase._subprocess.run", side_effect=[
             _mock_proc(0),
             _mock_proc(0),
             _mock_proc(0),
         ]):
        run_close_phase(tmp_path)
    state = _read_state(tmp_path)
    assert state.get("current_phase") is None
    assert state["current_branch"] == "feature/my-feature"


def test_close_phase_prints_next_hint(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.close_phase._subprocess.run", side_effect=[
             _mock_proc(0), _mock_proc(0), _mock_proc(0),
         ]):
        run_close_phase(tmp_path)
    out = capsys.readouterr().out
    assert "bricklayer branch --phase" in out


def test_close_phase_from_main_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.close_phase._get_current_branch", return_value="main"):
        result = run_close_phase(tmp_path)
    assert result == 1
    assert "phase/" in capsys.readouterr().err


def test_close_phase_from_feature_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.close_phase._get_current_branch", return_value="feature/foo"):
        result = run_close_phase(tmp_path)
    assert result == 1


def test_close_phase_from_brick_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.close_phase._get_current_branch", return_value="brick/14-foo"):
        result = run_close_phase(tmp_path)
    assert result == 1


def test_close_phase_missing_current_feature_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)  # no current_feature
    with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"):
        result = run_close_phase(tmp_path)
    assert result == 1
    assert "current_feature" in capsys.readouterr().err


def test_close_phase_git_checkout_fail_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.close_phase._subprocess.run", return_value=_mock_proc(1, "conflict")):
        result = run_close_phase(tmp_path)
    assert result == 1
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


def test_close_phase_git_merge_fail_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.close_phase._subprocess.run", side_effect=[
             _mock_proc(0),    # checkout ok
             _mock_proc(1, "merge conflict"),  # merge fails
         ]):
        result = run_close_phase(tmp_path)
    assert result == 1
    assert "Traceback" not in capsys.readouterr().err


# ---------------------------------------------------------------------------
# close_feature.py
# ---------------------------------------------------------------------------


def test_close_feature_merges_to_main(tmp_path: Path) -> None:
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.close_feature._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.close_feature._subprocess.run", side_effect=[
             _mock_proc(0),  # checkout main
             _mock_proc(0),  # merge --no-ff
             _mock_proc(0),  # branch -d
         ]):
        result = run_close_feature(tmp_path)
    assert result == 0


def test_close_feature_updates_state(tmp_path: Path) -> None:
    _write_state(tmp_path, {
        "current_feature": "feature/my-feature",
        "current_phase": None,
    })
    with patch("cli.commands.close_feature._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.close_feature._subprocess.run", side_effect=[
             _mock_proc(0), _mock_proc(0), _mock_proc(0),
         ]):
        run_close_feature(tmp_path)
    state = _read_state(tmp_path)
    assert state.get("current_feature") is None
    assert state.get("current_phase") is None
    assert state["current_branch"] == "main"


def test_close_feature_prints_success(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.close_feature._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.close_feature._subprocess.run", side_effect=[
             _mock_proc(0), _mock_proc(0), _mock_proc(0),
         ]):
        run_close_feature(tmp_path)
    out = capsys.readouterr().out
    assert "Feature merged to main" in out


def test_close_feature_from_main_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.close_feature._get_current_branch", return_value="main"):
        result = run_close_feature(tmp_path)
    assert result == 1
    assert "feature/" in capsys.readouterr().err


def test_close_feature_from_phase_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.close_feature._get_current_branch", return_value="phase/1-scaffold"):
        result = run_close_feature(tmp_path)
    assert result == 1


def test_close_feature_from_brick_exits_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.close_feature._get_current_branch", return_value="brick/14-foo"):
        result = run_close_feature(tmp_path)
    assert result == 1


def test_close_feature_git_fail_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    with patch("cli.commands.close_feature._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.close_feature._subprocess.run", return_value=_mock_proc(1, "error")):
        result = run_close_feature(tmp_path)
    assert result == 1
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# build.py — verdict PASS routing
# ---------------------------------------------------------------------------


def _write_state_for_verdict(root: Path, extra: dict | None = None) -> None:
    """Write state.json with next_action=skeptic_packet_ready."""
    state = {
        **_BASE_STATE,
        "next_action": "skeptic_packet_ready",
        **(extra or {}),
    }
    (root / "bricklayer").mkdir(exist_ok=True)
    (root / "bricklayer" / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    (root / "bricklayer" / "spec.md").write_text(
        "BRICK: Brick 14 - test\nFILES:\n- bricklayer/spec.md\n", encoding="utf-8"
    )
    (root / "bricklayer" / "skeptic_verdict.md").write_text("Verdict: PASS\n", encoding="utf-8")


def _fake_run_tool(exit_code=0, output="COMPLETED\n"):
    """Patch run_tool and get_tool_path so verdict can complete without real tools."""
    from unittest.mock import patch as _patch
    from contextlib import ExitStack

    class _Stack:
        def __enter__(self):
            self._stack = ExitStack()
            self._stack.__enter__()
            self._stack.enter_context(
                _patch("cli.commands.build.run_tool", return_value=(exit_code, output))
            )
            self._stack.enter_context(
                _patch("cli.commands.build.get_tool_path", return_value=Path("/fake/tool.py"))
            )
            return self

        def __exit__(self, *args):
            return self._stack.__exit__(*args)

    return _Stack()


def test_verdict_pass_on_brick_merges_to_phase(tmp_path: Path) -> None:
    _write_state_for_verdict(tmp_path, {"current_phase": "phase/1-scaffold"})
    with patch("cli.commands.build._get_current_branch", return_value="brick/14-foo"), \
         patch("cli.commands.build._git_commit_spec", return_value=(0, "[ok]")), \
         patch("cli.commands.build._merge_branch_to", return_value=(0, "Merged ok")) as mock_merge, \
         _fake_run_tool():
        from cli.commands.build import run_verdict
        result = run_verdict(tmp_path, {}, "PASS")
    assert result == 0
    mock_merge.assert_called_once_with(tmp_path, "brick/14-foo", "phase/1-scaffold")


def test_verdict_pass_on_brick_missing_phase_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state_for_verdict(tmp_path)  # no current_phase
    with patch("cli.commands.build._get_current_branch", return_value="brick/14-foo"), \
         patch("cli.commands.build._git_commit_spec", return_value=(0, "")):
        from cli.commands.build import run_verdict
        result = run_verdict(tmp_path, {}, "PASS")
    assert result == 1
    assert "current_phase" in capsys.readouterr().err


def test_verdict_pass_on_phase_merges_to_feature(tmp_path: Path) -> None:
    _write_state_for_verdict(tmp_path, {"current_feature": "feature/my-feature"})
    with patch("cli.commands.build._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.build._git_commit_spec", return_value=(0, "[ok]")), \
         patch("cli.commands.build._merge_branch_to", return_value=(0, "Merged ok")) as mock_merge, \
         _fake_run_tool():
        from cli.commands.build import run_verdict
        result = run_verdict(tmp_path, {}, "PASS")
    assert result == 0
    mock_merge.assert_called_once_with(tmp_path, "phase/1-scaffold", "feature/my-feature")


def test_verdict_pass_on_phase_missing_feature_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state_for_verdict(tmp_path)  # no current_feature
    with patch("cli.commands.build._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.build._git_commit_spec", return_value=(0, "")):
        from cli.commands.build import run_verdict
        result = run_verdict(tmp_path, {}, "PASS")
    assert result == 1
    assert "current_feature" in capsys.readouterr().err


def test_verdict_pass_on_feature_merges_to_main(tmp_path: Path) -> None:
    _write_state_for_verdict(tmp_path)
    with patch("cli.commands.build._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.build._git_commit_spec", return_value=(0, "[ok]")), \
         patch("cli.commands.build._merge_branch_to", return_value=(0, "Merged ok")) as mock_merge, \
         _fake_run_tool():
        from cli.commands.build import run_verdict
        result = run_verdict(tmp_path, {}, "PASS")
    assert result == 0
    mock_merge.assert_called_once_with(tmp_path, "feature/my-feature", "main")


def test_verdict_pass_merge_fail_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state_for_verdict(tmp_path, {"current_phase": "phase/1-scaffold"})
    with patch("cli.commands.build._get_current_branch", return_value="brick/14-foo"), \
         patch("cli.commands.build._git_commit_spec", return_value=(0, "")), \
         patch("cli.commands.build._merge_branch_to", return_value=(1, "error: conflict")):
        from cli.commands.build import run_verdict
        result = run_verdict(tmp_path, {}, "PASS")
    assert result == 1
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# State tracking through full three-level flow
# ---------------------------------------------------------------------------


def test_full_flow_state_tracking(tmp_path: Path) -> None:
    """Simulate: feature branch → phase branch → brick branch → state fields."""
    _write_state(tmp_path)

    # 1. Create feature branch
    with patch("cli.commands.branch._get_current_branch", return_value="main"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
        run_branch(tmp_path, None, "my-feature", feature=True)
    state = _read_state(tmp_path)
    assert state["current_branch"] == "feature/my-feature"
    assert state["current_feature"] == "feature/my-feature"
    assert state.get("current_phase") is None

    # 2. Create phase branch
    with patch("cli.commands.branch._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
        run_branch(tmp_path, "1", "scaffold", phase=True)
    state = _read_state(tmp_path)
    assert state["current_branch"] == "phase/1-scaffold"
    assert state["current_feature"] == "feature/my-feature"  # preserved
    assert state["current_phase"] == "phase/1-scaffold"

    # 3. Create brick branch
    with patch("cli.commands.branch._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
        run_branch(tmp_path, "14", "three-level-branching")
    state = _read_state(tmp_path)
    assert state["current_branch"] == "brick/14-three-level-branching"
    assert state["current_feature"] == "feature/my-feature"  # preserved
    assert state["current_phase"] == "phase/1-scaffold"      # preserved


def test_close_phase_then_close_feature_state(tmp_path: Path) -> None:
    """After close-phase + close-feature, all branch fields are cleared."""
    _write_state(tmp_path, {
        "current_feature": "feature/my-feature",
        "current_phase": "phase/1-scaffold",
    })

    # close-phase
    with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"), \
         patch("cli.commands.close_phase._subprocess.run", side_effect=[
             _mock_proc(0), _mock_proc(0), _mock_proc(0),
         ]):
        run_close_phase(tmp_path)
    state = _read_state(tmp_path)
    assert state.get("current_phase") is None
    assert state.get("current_feature") == "feature/my-feature"

    # close-feature
    with patch("cli.commands.close_feature._get_current_branch", return_value="feature/my-feature"), \
         patch("cli.commands.close_feature._subprocess.run", side_effect=[
             _mock_proc(0), _mock_proc(0), _mock_proc(0),
         ]):
        run_close_feature(tmp_path)
    state = _read_state(tmp_path)
    assert state.get("current_feature") is None
    assert state.get("current_phase") is None
    assert state["current_branch"] == "main"


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------


def _cli_setup(tmp_path: Path) -> None:
    _write_state(tmp_path)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )


def test_cli_branch_feature_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._get_current_branch", return_value="main"), \
             patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
            result = cli_runner.invoke(app, ["branch", "--feature", "my-feature"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_branch_feature_wrong_parent_exits_one(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._get_current_branch", return_value="brick/foo"):
            result = cli_runner.invoke(app, ["branch", "--feature", "my-feature"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_branch_phase_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._get_current_branch", return_value="feature/my-feature"), \
             patch("cli.commands.branch._git_create_checkout", return_value=(0, "")):
            result = cli_runner.invoke(app, ["branch", "--phase", "1", "scaffold"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_branch_phase_wrong_parent_exits_one(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._get_current_branch", return_value="main"):
            result = cli_runner.invoke(app, ["branch", "--phase", "1", "scaffold"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_close_phase_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    _write_state(tmp_path, {"current_feature": "feature/my-feature"})
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_phase._get_current_branch", return_value="phase/1-scaffold"), \
             patch("cli.commands.close_phase._subprocess.run", side_effect=[
                 _mock_proc(0), _mock_proc(0), _mock_proc(0),
             ]):
            result = cli_runner.invoke(app, ["close-phase"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_close_phase_wrong_branch_exits_one(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_phase._get_current_branch", return_value="main"):
            result = cli_runner.invoke(app, ["close-phase"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_close_feature_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_feature._get_current_branch", return_value="feature/my-feature"), \
             patch("cli.commands.close_feature._subprocess.run", side_effect=[
                 _mock_proc(0), _mock_proc(0), _mock_proc(0),
             ]):
            result = cli_runner.invoke(app, ["close-feature"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_close_feature_wrong_branch_exits_one(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_feature._get_current_branch", return_value="phase/1-scaffold"):
            result = cli_runner.invoke(app, ["close-feature"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1
