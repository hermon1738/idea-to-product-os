"""Tests for Brick 8 — bricklayer build --verdict PASS|FAIL."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.build import run_verdict  # noqa: E402
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_STATE: dict = {
    "current_brick": "Brick 8 - build --verdict",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": [],
    "next_action": "skeptic_packet_ready",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}

_CONFIG_WITH_STATE: dict = {
    "tools": {"state": "bricklayer/tools/update_state.py"}
}


def _make_project(
    tmp_path: Path,
    next_action: str = "skeptic_packet_ready",
    loop_count: int = 0,
    omit_loop_count: bool = False,
) -> Path:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    state = {**_BASE_STATE, "next_action": next_action, "loop_count": loop_count}
    if omit_loop_count:
        del state["loop_count"]
        # Write raw to bypass schema validation
        (brick_dir / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    else:
        (brick_dir / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    return tmp_path


def _read_state(root: Path) -> dict:
    return json.loads((root / "bricklayer/state.json").read_text(encoding="utf-8"))


def _verdict_path(root: Path) -> Path:
    return root / "bricklayer" / "skeptic_verdict.md"


# ---------------------------------------------------------------------------
# PASS path
# ---------------------------------------------------------------------------


def test_pass_writes_verdict_file(tmp_path: Path) -> None:
    """PASS writes skeptic_verdict.md with 'Verdict: PASS'."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
        run_verdict(root, _CONFIG_WITH_STATE, "PASS")
    assert _verdict_path(root).exists()
    assert _verdict_path(root).read_text(encoding="utf-8") == "Verdict: PASS\n"


def test_pass_calls_update_state(tmp_path: Path) -> None:
    """PASS calls run_tool with --complete."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")) as mock_tool:
        run_verdict(root, _CONFIG_WITH_STATE, "PASS")
    call_args = mock_tool.call_args
    assert "--complete" in call_args[0][1]


def test_pass_exits_zero(tmp_path: Path) -> None:
    """PASS returns 0 when update_state tool exits 0."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
        result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")
    assert result == 0


def test_pass_tool_failure_returns_one(tmp_path: Path) -> None:
    """PASS returns 1 when update_state tool exits non-zero."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(1, "REJECTED\n")):
        result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")
    assert result == 1


# ---------------------------------------------------------------------------
# FAIL path — normal increment
# ---------------------------------------------------------------------------


def test_fail_increments_loop_count(tmp_path: Path) -> None:
    """FAIL increments loop_count by 1."""
    root = _make_project(tmp_path, loop_count=1)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert _read_state(root)["loop_count"] == 2


def test_fail_next_action_unchanged(tmp_path: Path) -> None:
    """FAIL does not advance next_action."""
    root = _make_project(tmp_path, loop_count=1)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert _read_state(root)["next_action"] == "skeptic_packet_ready"


def test_fail_exits_one(tmp_path: Path) -> None:
    """FAIL always returns 1."""
    root = _make_project(tmp_path, loop_count=0)
    result = run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert result == 1


def test_fail_prints_blocker_message(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """FAIL below threshold prints normal blocker message."""
    root = _make_project(tmp_path, loop_count=1)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    out = capsys.readouterr().out
    assert "FAIL" in out
    assert "2" in out


# ---------------------------------------------------------------------------
# FAIL path — RESCOPE triggered (loop_count reaches 3)
# ---------------------------------------------------------------------------


def test_fail_loop_count_2_increments_to_3(tmp_path: Path) -> None:
    """loop_count=2 increments to 3 on FAIL."""
    root = _make_project(tmp_path, loop_count=2)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert _read_state(root)["loop_count"] == 3


def test_fail_loop_count_2_prints_rescope(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """loop_count reaches 3 → RESCOPE message printed."""
    root = _make_project(tmp_path, loop_count=2)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    out = capsys.readouterr().out
    assert "RESCOPE" in out


def test_fail_loop_count_2_exits_one(tmp_path: Path) -> None:
    """loop_count reaches 3 → still exits 1."""
    root = _make_project(tmp_path, loop_count=2)
    result = run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert result == 1


# ---------------------------------------------------------------------------
# FAIL path — already at loop_count=3 (hard stop)
# ---------------------------------------------------------------------------


def test_fail_loop_count_already_3_exits_one(tmp_path: Path) -> None:
    """loop_count=3 already → hard stop, exit 1."""
    root = _make_project(tmp_path, loop_count=3)
    result = run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert result == 1


def test_fail_loop_count_already_3_state_unchanged(tmp_path: Path) -> None:
    """loop_count=3 hard stop → state.json not modified."""
    root = _make_project(tmp_path, loop_count=3)
    before = _read_state(root)["loop_count"]
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert _read_state(root)["loop_count"] == before


def test_fail_loop_count_already_3_prints_rescope(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """loop_count=3 hard stop → RESCOPE printed."""
    root = _make_project(tmp_path, loop_count=3)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert "RESCOPE" in capsys.readouterr().out


def test_fail_loop_count_already_3_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """loop_count=3 hard stop → no raw traceback."""
    root = _make_project(tmp_path, loop_count=3)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# Guard — wrong next_action
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("wrong_action", ["verify", "tests_passed", "brick_complete", ""])
def test_guard_wrong_next_action_exits_one(
    tmp_path: Path, wrong_action: str
) -> None:
    """Guard fires for any next_action other than skeptic_packet_ready."""
    root = _make_project(tmp_path, next_action=wrong_action)
    result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")
    assert result == 1


def test_guard_does_not_write_verdict_file(tmp_path: Path) -> None:
    """Guard fires → skeptic_verdict.md is NOT written."""
    root = _make_project(tmp_path, next_action="tests_passed")
    run_verdict(root, _CONFIG_WITH_STATE, "PASS")
    assert not _verdict_path(root).exists()


def test_guard_no_traceback(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Guard fires → no raw traceback in any output."""
    root = _make_project(tmp_path, next_action="verify")
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# Missing loop_count key → fallback to 0
# ---------------------------------------------------------------------------


def test_missing_loop_count_key_fallback(tmp_path: Path) -> None:
    """Missing loop_count key treated as 0; FAIL increments to 1."""
    root = _make_project(tmp_path, omit_loop_count=True)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    assert _read_state(root)["loop_count"] == 1


def test_missing_loop_count_key_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Missing loop_count key → no raw traceback."""
    root = _make_project(tmp_path, omit_loop_count=True)
    run_verdict(root, _CONFIG_WITH_STATE, "FAIL")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# Invalid verdict value
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bad_value", ["pass", "fail", "YES", "NO", ""])
def test_invalid_verdict_value_exits_one(tmp_path: Path, bad_value: str) -> None:
    """Invalid verdict string (not PASS or FAIL) → exit 1."""
    root = _make_project(tmp_path)
    result = run_verdict(root, _CONFIG_WITH_STATE, bad_value)
    assert result == 1


def test_invalid_verdict_no_traceback(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Invalid verdict string → no raw traceback."""
    root = _make_project(tmp_path)
    run_verdict(root, _CONFIG_WITH_STATE, "maybe")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_setup(tmp_path: Path, next_action: str = "skeptic_packet_ready", loop_count: int = 0) -> None:
    _make_project(tmp_path, next_action=next_action, loop_count=loop_count)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools:\n  state: bricklayer/tools/update_state.py\nagents: {}\n",
        encoding="utf-8",
    )
    tools_dir = tmp_path / "bricklayer" / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    (tools_dir / "update_state.py").write_text("", encoding="utf-8")


def test_cli_pass_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build --verdict PASS` exits 0."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
            result = cli_runner.invoke(app, ["build", "--verdict", "PASS"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_pass_writes_verdict_file(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build --verdict PASS` writes skeptic_verdict.md."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
            cli_runner.invoke(app, ["build", "--verdict", "PASS"])
    finally:
        os.chdir(old_cwd)
    assert _verdict_path(tmp_path).exists()
    assert "Verdict: PASS" in _verdict_path(tmp_path).read_text(encoding="utf-8")


def test_cli_fail_exits_one(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build --verdict FAIL` exits 1."""
    _cli_setup(tmp_path, loop_count=0)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["build", "--verdict", "FAIL"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_fail_increments_loop_count(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build --verdict FAIL` increments loop_count."""
    _cli_setup(tmp_path, loop_count=1)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        cli_runner.invoke(app, ["build", "--verdict", "FAIL"])
    finally:
        os.chdir(old_cwd)
    assert _read_state(tmp_path)["loop_count"] == 2
