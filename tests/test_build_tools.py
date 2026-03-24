"""Tests for Brick 6 — bricklayer build --snapshot/--verify/--test flag handlers."""

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

from cli.commands.build import run_snapshot, run_verify, run_test  # noqa: E402
from cli.runner import get_tool_path  # noqa: E402
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_STATE: dict = {
    "current_brick": "Brick 6 - build tool wrappers",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": [],
    "next_action": "snapshot_init",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}

_CONFIG: dict = {
    "tools": {
        "verify": "bricklayer/tools/verify_files_touched.py",
        "test": "bricklayer/tools/run_tests_and_capture.py",
    }
}


def _make_project(tmp_path: Path) -> Path:
    """Write bricklayer/ dir + state.json. Returns repo root."""
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    (brick_dir / "state.json").write_text(
        json.dumps(_BASE_STATE, indent=2), encoding="utf-8"
    )
    return tmp_path


def _read_next_action(root: Path) -> str:
    data = json.loads((root / "bricklayer/state.json").read_text(encoding="utf-8"))
    return data["next_action"]


# ---------------------------------------------------------------------------
# get_tool_path unit tests
# ---------------------------------------------------------------------------


def test_get_tool_path_found(tmp_path: Path) -> None:
    """get_tool_path returns resolved Path when key is present."""
    config = {"tools": {"verify": "bricklayer/tools/verify_files_touched.py"}}
    result = get_tool_path(config, "verify", tmp_path)
    assert result == tmp_path / "bricklayer/tools/verify_files_touched.py"


def test_get_tool_path_missing_key_returns_none(tmp_path: Path) -> None:
    """get_tool_path returns None when the key is not in tools:."""
    config = {"tools": {}}
    result = get_tool_path(config, "missing_tool", tmp_path)
    assert result is None


def test_get_tool_path_missing_tools_section_returns_none(tmp_path: Path) -> None:
    """get_tool_path returns None when tools: section is absent entirely."""
    result = get_tool_path({}, "verify", tmp_path)
    assert result is None


# ---------------------------------------------------------------------------
# --snapshot flag handler
# ---------------------------------------------------------------------------


def test_snapshot_success_returns_zero(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_snapshot returns 0 on tool exit 0."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "SNAPSHOT_INIT_OK\n")):
        result = run_snapshot(root, _CONFIG)
    assert result == 0


def test_snapshot_success_updates_state(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_snapshot sets next_action to 'snapshot_init' on success."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "SNAPSHOT_INIT_OK\n")):
        run_snapshot(root, _CONFIG)
    assert _read_next_action(root) == "snapshot_init"


def test_snapshot_failure_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_snapshot returns 1 on non-zero tool exit."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(1, "error output\n")):
        result = run_snapshot(root, _CONFIG)
    assert result == 1


def test_snapshot_failure_does_not_update_state(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_snapshot leaves state.json unchanged on tool failure."""
    root = _make_project(tmp_path)
    original = _read_next_action(root)
    with patch("cli.commands.build.run_tool", return_value=(1, "error\n")):
        run_snapshot(root, _CONFIG)
    assert _read_next_action(root) == original


# ---------------------------------------------------------------------------
# --verify flag handler
# ---------------------------------------------------------------------------


def test_verify_success_returns_zero(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_verify returns 0 on tool exit 0."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "OK: all touched files...\n")):
        result = run_verify(root, _CONFIG)
    assert result == 0


def test_verify_success_updates_state(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_verify sets next_action to 'verify' on success."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "OK\n")):
        run_verify(root, _CONFIG)
    assert _read_next_action(root) == "verify"


def test_verify_failure_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_verify returns 1 on non-zero tool exit."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(1, "OUT OF SCOPE\n")):
        result = run_verify(root, _CONFIG)
    assert result == 1


def test_verify_failure_does_not_update_state(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_verify leaves state.json unchanged on tool failure."""
    root = _make_project(tmp_path)
    original = _read_next_action(root)
    with patch("cli.commands.build.run_tool", return_value=(1, "OUT OF SCOPE\n")):
        run_verify(root, _CONFIG)
    assert _read_next_action(root) == original


# ---------------------------------------------------------------------------
# --test flag handler
# ---------------------------------------------------------------------------


def test_run_test_success_returns_zero(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_test returns 0 on tool exit 0."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "PASS\n")):
        result = run_test(root, _CONFIG)
    assert result == 0


def test_run_test_success_updates_state(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_test sets next_action to 'tests_passed' on success."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(0, "PASS\n")):
        run_test(root, _CONFIG)
    assert _read_next_action(root) == "tests_passed"


def test_run_test_failure_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_test returns 1 on non-zero tool exit (test suite failure)."""
    root = _make_project(tmp_path)
    with patch("cli.commands.build.run_tool", return_value=(1, "FAIL\n1 failed\n")):
        result = run_test(root, _CONFIG)
    assert result == 1


def test_run_test_failure_does_not_update_state(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_test leaves state.json unchanged on test failure."""
    root = _make_project(tmp_path)
    original = _read_next_action(root)
    with patch("cli.commands.build.run_tool", return_value=(1, "FAIL\n")):
        run_test(root, _CONFIG)
    assert _read_next_action(root) == original


# ---------------------------------------------------------------------------
# Missing tool path → clear error, no traceback
# ---------------------------------------------------------------------------


def test_missing_tool_key_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Flag handler returns 1 when tool key absent from config."""
    root = _make_project(tmp_path)
    result = run_verify(root, {"tools": {}})  # no 'verify' key
    assert result == 1


def test_missing_tool_key_error_message(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Error message mentions the missing tool key, no traceback."""
    root = _make_project(tmp_path)
    run_verify(root, {"tools": {}})
    err = capsys.readouterr().err
    assert "verify" in err
    assert "Traceback" not in err


# ---------------------------------------------------------------------------
# CliRunner integration (tool subprocess mocked)
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_invoke(tmp_path: Path, flag: str, tool_output: str = "OK\n") -> object:
    """Set up project, mock run_tool, invoke bricklayer build <flag>."""
    _make_project(tmp_path)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools:\n  verify: bricklayer/tools/verify_files_touched.py\n"
        "  test: bricklayer/tools/run_tests_and_capture.py\nagents: {}\n",
        encoding="utf-8",
    )
    # Create stub tool files so load_and_validate doesn't exit
    tools_dir = tmp_path / "bricklayer" / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    (tools_dir / "verify_files_touched.py").write_text("", encoding="utf-8")
    (tools_dir / "run_tests_and_capture.py").write_text("", encoding="utf-8")

    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build.run_tool", return_value=(0, tool_output)):
            result = cli_runner.invoke(app, ["build", flag])
    finally:
        os.chdir(old_cwd)
    return result


def test_cli_snapshot_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build --snapshot` exits 0."""
    result = _cli_invoke(tmp_path, "--snapshot")
    assert result.exit_code == 0


def test_cli_snapshot_updates_state(tmp_path: Path) -> None:
    """CliRunner: next_action='snapshot_init' after --snapshot."""
    _cli_invoke(tmp_path, "--snapshot")
    assert _read_next_action(tmp_path) == "snapshot_init"


def test_cli_verify_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build --verify` exits 0."""
    result = _cli_invoke(tmp_path, "--verify")
    assert result.exit_code == 0


def test_cli_verify_updates_state(tmp_path: Path) -> None:
    """CliRunner: next_action='verify' after --verify."""
    _cli_invoke(tmp_path, "--verify")
    assert _read_next_action(tmp_path) == "verify"


def test_cli_test_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build --test` exits 0."""
    result = _cli_invoke(tmp_path, "--test")
    assert result.exit_code == 0


def test_cli_test_updates_state(tmp_path: Path) -> None:
    """CliRunner: next_action='tests_passed' after --test."""
    _cli_invoke(tmp_path, "--test")
    assert _read_next_action(tmp_path) == "tests_passed"
