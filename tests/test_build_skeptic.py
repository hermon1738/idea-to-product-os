"""Tests for Brick 7 (revision) — bricklayer build --skeptic-packet flag handler."""

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

from cli.commands.build import run_skeptic_packet  # noqa: E402
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_STATE: dict = {
    "current_brick": "Brick 7 - build --skeptic-packet",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": [],
    "next_action": "tests_passed",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}

_CONFIG_WITH_SKEPTIC: dict = {
    "tools": {"skeptic": "bricklayer/tools/make_skeptic_packet.py"}
}
_CONFIG_NO_SKEPTIC: dict = {"tools": {}}


def _make_project(
    tmp_path: Path,
    next_action: str = "tests_passed",
    omit_next_action_key: bool = False,
    with_packet: bool = False,
) -> Path:
    """Write bricklayer/state.json (and optionally skeptic_packet/) under tmp_path."""
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    state: dict = {**_BASE_STATE, "next_action": next_action}
    if omit_next_action_key:
        del state["next_action"]
        # state.load() validates schema, so write raw JSON to bypass it
        (brick_dir / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    else:
        (brick_dir / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    if with_packet:
        packet_dir = brick_dir / "skeptic_packet"
        packet_dir.mkdir(exist_ok=True)
        (packet_dir / "test_output.txt").write_text("PASS\n", encoding="utf-8")
    return tmp_path


def _read_next_action(root: Path) -> str:
    data = json.loads((root / "bricklayer/state.json").read_text(encoding="utf-8"))
    return data["next_action"]


# ---------------------------------------------------------------------------
# Happy path (FIX 2: packet dir must exist and be non-empty)
# ---------------------------------------------------------------------------


def test_happy_path_returns_zero(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_skeptic_packet returns 0 when guard passes, tool exits 0, packet dir exists."""
    root = _make_project(tmp_path, "tests_passed", with_packet=True)
    with patch("cli.commands.build.run_tool", return_value=(0, "Skeptic packet updated\n")):
        result = run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert result == 0


def test_happy_path_updates_state(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_skeptic_packet sets next_action to 'skeptic_packet_ready' on success."""
    root = _make_project(tmp_path, "tests_passed", with_packet=True)
    with patch("cli.commands.build.run_tool", return_value=(0, "Skeptic packet updated\n")):
        run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert _read_next_action(root) == "skeptic_packet_ready"


def test_happy_path_prints_packet_path(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_skeptic_packet prints the packet directory path on success."""
    root = _make_project(tmp_path, "tests_passed", with_packet=True)
    with patch("cli.commands.build.run_tool", return_value=(0, "Skeptic packet updated\n")):
        run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    out = capsys.readouterr().out
    assert "skeptic_packet" in out


# ---------------------------------------------------------------------------
# FIX 2 — Packet directory confirmation after tool exits 0
# ---------------------------------------------------------------------------


def test_fix2_missing_packet_dir_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Tool exits 0 but packet dir is missing → exit 1, state not updated."""
    root = _make_project(tmp_path, "tests_passed", with_packet=False)
    with patch("cli.commands.build.run_tool", return_value=(0, "output\n")):
        result = run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert result == 1


def test_fix2_missing_packet_dir_state_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """State is not updated when packet dir is missing after tool exit 0."""
    root = _make_project(tmp_path, "tests_passed", with_packet=False)
    with patch("cli.commands.build.run_tool", return_value=(0, "output\n")):
        run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert _read_next_action(root) == "tests_passed"


def test_fix2_empty_packet_dir_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Tool exits 0 but packet dir is empty → exit 1, state not updated."""
    root = _make_project(tmp_path, "tests_passed", with_packet=False)
    # Create the dir but leave it empty
    (root / "bricklayer" / "skeptic_packet").mkdir(parents=True)
    with patch("cli.commands.build.run_tool", return_value=(0, "output\n")):
        result = run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert result == 1


def test_fix2_empty_packet_dir_state_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """State not updated when packet dir is empty."""
    root = _make_project(tmp_path, "tests_passed", with_packet=False)
    (root / "bricklayer" / "skeptic_packet").mkdir(parents=True)
    with patch("cli.commands.build.run_tool", return_value=(0, "output\n")):
        run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert _read_next_action(root) == "tests_passed"


# ---------------------------------------------------------------------------
# Guard — wrong next_action
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("wrong_action", ["verify", "snapshot_init", "brick_complete", ""])
def test_guard_wrong_next_action_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture, wrong_action: str
) -> None:
    """Guard fires for any next_action other than tests_passed → exit 1."""
    root = _make_project(tmp_path, wrong_action)
    result = run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert result == 1


def test_guard_prints_run_tests_first(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Guard message tells user to run tests first."""
    root = _make_project(tmp_path, "verify")
    run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    out = capsys.readouterr().out
    assert "Run tests first" in out
    assert "bricklayer build --test" in out


def test_guard_does_not_update_state(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Guard does not mutate state.json."""
    root = _make_project(tmp_path, "verify")
    run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert _read_next_action(root) == "verify"


def test_guard_no_traceback(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Guard output contains no raw Python traceback."""
    root = _make_project(tmp_path, "snapshot_init")
    run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# FIX 3 — Missing next_action key in state.json
# ---------------------------------------------------------------------------


def test_fix3_missing_next_action_key_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """state.json present but next_action key absent → guard fires, exit 1."""
    root = _make_project(tmp_path, omit_next_action_key=True)
    result = run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert result == 1


def test_fix3_missing_next_action_key_guard_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Missing next_action key prints the guard message (not a KeyError traceback)."""
    root = _make_project(tmp_path, omit_next_action_key=True)
    run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err
    assert "Run tests first" in combined.out


# ---------------------------------------------------------------------------
# Tool failure
# ---------------------------------------------------------------------------


def test_tool_failure_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_skeptic_packet returns 1 when tool exits non-zero."""
    root = _make_project(tmp_path, "tests_passed")
    with patch("cli.commands.build.run_tool", return_value=(1, "error output\n")):
        result = run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert result == 1


def test_tool_failure_does_not_update_state(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Tool failure leaves state.json unchanged."""
    root = _make_project(tmp_path, "tests_passed")
    with patch("cli.commands.build.run_tool", return_value=(1, "error\n")):
        run_skeptic_packet(root, _CONFIG_WITH_SKEPTIC)
    assert _read_next_action(root) == "tests_passed"


# ---------------------------------------------------------------------------
# Missing tool key
# ---------------------------------------------------------------------------


def test_missing_tool_key_returns_one(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Returns 1 when skeptic key absent from config."""
    root = _make_project(tmp_path, "tests_passed")
    result = run_skeptic_packet(root, _CONFIG_NO_SKEPTIC)
    assert result == 1


def test_missing_tool_key_clear_error(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Error message mentions 'skeptic', no traceback."""
    root = _make_project(tmp_path, "tests_passed")
    run_skeptic_packet(root, _CONFIG_NO_SKEPTIC)
    err = capsys.readouterr().err
    assert "skeptic" in err
    assert "Traceback" not in err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_invoke(
    tmp_path: Path,
    next_action: str = "tests_passed",
    tool_exit: int = 0,
    flags: list[str] | None = None,
    with_packet: bool = True,
) -> object:
    """Set up project, mock run_tool, invoke `bricklayer build [flags]`."""
    _make_project(tmp_path, next_action, with_packet=with_packet)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools:\n  skeptic: bricklayer/tools/make_skeptic_packet.py\n"
        "agents: {}\n",
        encoding="utf-8",
    )
    tools_dir = tmp_path / "bricklayer" / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    (tools_dir / "make_skeptic_packet.py").write_text("", encoding="utf-8")

    invoke_flags = flags if flags is not None else ["--skeptic-packet"]
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch(
            "cli.commands.build.run_tool",
            return_value=(tool_exit, "Skeptic packet updated\n"),
        ):
            result = cli_runner.invoke(app, ["build"] + invoke_flags)
    finally:
        os.chdir(old_cwd)
    return result


def test_cli_happy_path_exits_zero(tmp_path: Path) -> None:
    """CliRunner: --skeptic-packet exits 0 when guard passes and packet dir exists."""
    result = _cli_invoke(tmp_path, next_action="tests_passed", tool_exit=0, with_packet=True)
    assert result.exit_code == 0


def test_cli_happy_path_updates_state(tmp_path: Path) -> None:
    """CliRunner: state.json next_action=skeptic_packet_ready after success."""
    _cli_invoke(tmp_path, next_action="tests_passed", tool_exit=0, with_packet=True)
    assert _read_next_action(tmp_path) == "skeptic_packet_ready"


def test_cli_guard_exits_one(tmp_path: Path) -> None:
    """CliRunner: --skeptic-packet exits 1 when next_action != tests_passed."""
    result = _cli_invoke(tmp_path, next_action="verify", tool_exit=0)
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# FIX 4 — Mutual exclusivity via CliRunner
# ---------------------------------------------------------------------------


def test_fix4_two_flags_exits_one(tmp_path: Path) -> None:
    """CliRunner: passing --test and --skeptic-packet together exits 1."""
    result = _cli_invoke(tmp_path, flags=["--test", "--skeptic-packet"])
    assert result.exit_code == 1


def test_fix4_two_flags_prints_mutex_error(tmp_path: Path) -> None:
    """CliRunner: mutex error message printed when two flags passed."""
    result = _cli_invoke(tmp_path, flags=["--test", "--skeptic-packet"])
    assert "Only one flag at a time" in result.output
