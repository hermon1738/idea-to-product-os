"""Tests for Brick 9 — bricklayer pause command."""

from __future__ import annotations

import datetime
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

from cli.commands.pause import (  # noqa: E402
    _build_continue_md,
    _build_handoff,
    _next_command,
    _parse_brick,
    run_pause,
)
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_STATE: dict = {
    "current_brick": "Brick 9 - bricklayer pause",
    "status": "IN_PROGRESS",
    "loop_count": 2,
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


def _make_project(tmp_path: Path, state: dict | None = None) -> Path:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    s = state if state is not None else _BASE_STATE
    (brick_dir / "state.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
    return tmp_path


def _fake_git_branch(name: str):
    """Return a subprocess.run side_effect that reports a given branch name."""
    from unittest.mock import MagicMock

    def _side_effect(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = name + "\n"
        return m

    return _side_effect


# ---------------------------------------------------------------------------
# _parse_brick
# ---------------------------------------------------------------------------


def test_parse_brick_extracts_number_and_name() -> None:
    assert _parse_brick("Brick 9 - bricklayer pause") == ("9", "bricklayer pause")


def test_parse_brick_decimal_number() -> None:
    num, name = _parse_brick("Brick 8.5 - git fixes")
    assert num == "8.5"
    assert name == "git fixes"


def test_parse_brick_unknown_format_returns_question_mark() -> None:
    num, name = _parse_brick("no match here")
    assert num == "?"
    assert name == "no match here"


# ---------------------------------------------------------------------------
# _next_command
# ---------------------------------------------------------------------------


def test_next_command_known_action() -> None:
    assert _next_command("skeptic_packet_ready") == "bricklayer build --verdict PASS|FAIL"


def test_next_command_unknown_action_returns_fallback() -> None:
    result = _next_command("some_unknown_step")
    assert "bricklayer next" in result
    assert "some_unknown_step" in result


# ---------------------------------------------------------------------------
# _build_handoff
# ---------------------------------------------------------------------------


def test_build_handoff_all_fields_present(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9-test")):
        handoff = _build_handoff(root, _BASE_STATE)

    required = {"project", "brick", "brick_name", "last_action",
                "loop_count", "current_branch", "timestamp", "next_command"}
    assert required == set(handoff.keys())


def test_build_handoff_brick_number(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        handoff = _build_handoff(root, _BASE_STATE)
    assert handoff["brick"] == "9"


def test_build_handoff_brick_name(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        handoff = _build_handoff(root, _BASE_STATE)
    assert handoff["brick_name"] == "bricklayer pause"


def test_build_handoff_last_action_matches_next_action(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        handoff = _build_handoff(root, _BASE_STATE)
    assert handoff["last_action"] == _BASE_STATE["next_action"]


def test_build_handoff_loop_count(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        handoff = _build_handoff(root, _BASE_STATE)
    assert handoff["loop_count"] == 2


def test_build_handoff_current_branch(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9-bricklayer-pause")):
        handoff = _build_handoff(root, _BASE_STATE)
    assert handoff["current_branch"] == "brick/9-bricklayer-pause"


def test_build_handoff_timestamp_is_iso8601(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        handoff = _build_handoff(root, _BASE_STATE)
    # Must parse without error
    ts = datetime.datetime.fromisoformat(handoff["timestamp"])
    assert ts.tzinfo is not None  # must be timezone-aware


def test_build_handoff_project_is_root_name(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        handoff = _build_handoff(root, _BASE_STATE)
    assert handoff["project"] == tmp_path.name


# ---------------------------------------------------------------------------
# _build_continue_md
# ---------------------------------------------------------------------------


def _sample_handoff(tmp_path: Path) -> dict:
    return {
        "project": "bricklayer-cli",
        "brick": "9",
        "brick_name": "bricklayer pause",
        "last_action": "skeptic_packet_ready",
        "loop_count": 2,
        "current_branch": "brick/9-bricklayer-pause",
        "timestamp": "2026-03-24T10:00:00+00:00",
        "next_command": "bricklayer build --verdict PASS|FAIL",
    }


def test_build_continue_md_contains_all_required_lines(tmp_path: Path) -> None:
    md = _build_continue_md(_sample_handoff(tmp_path))
    assert "Last session ended:" in md
    assert "Project:" in md
    assert "Branch:" in md
    assert "Current brick:" in md
    assert "Last action:" in md
    assert "Next command:" in md


def test_build_continue_md_timestamp_matches_handoff(tmp_path: Path) -> None:
    h = _sample_handoff(tmp_path)
    md = _build_continue_md(h)
    assert h["timestamp"] in md


def test_build_continue_md_branch_matches_handoff(tmp_path: Path) -> None:
    h = _sample_handoff(tmp_path)
    md = _build_continue_md(h)
    assert h["current_branch"] in md


def test_build_continue_md_next_command_matches_handoff(tmp_path: Path) -> None:
    h = _sample_handoff(tmp_path)
    md = _build_continue_md(h)
    assert h["next_command"] in md


def test_build_continue_md_contains_blockers_none(tmp_path: Path) -> None:
    md = _build_continue_md(_sample_handoff(tmp_path))
    assert "Blockers: none" in md


# ---------------------------------------------------------------------------
# run_pause — happy path
# ---------------------------------------------------------------------------


def test_run_pause_returns_zero(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        result = run_pause(root)
    assert result == 0


def test_run_pause_writes_handoff_json(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        run_pause(root)
    assert (root / "HANDOFF.json").exists()


def test_run_pause_writes_continue_md(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        run_pause(root)
    assert (root / ".continue-here.md").exists()


def test_run_pause_handoff_json_is_valid_json(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        run_pause(root)
    data = json.loads((root / "HANDOFF.json").read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_run_pause_handoff_json_fields_correct(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9-bricklayer-pause")):
        run_pause(root)
    data = json.loads((root / "HANDOFF.json").read_text(encoding="utf-8"))
    assert data["brick"] == "9"
    assert data["brick_name"] == "bricklayer pause"
    assert data["last_action"] == "skeptic_packet_ready"
    assert data["loop_count"] == 2
    assert data["current_branch"] == "brick/9-bricklayer-pause"
    assert data["next_command"] == "bricklayer build --verdict PASS|FAIL"


def test_run_pause_continue_md_values_match_handoff(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        run_pause(root)
    handoff = json.loads((root / "HANDOFF.json").read_text(encoding="utf-8"))
    md = (root / ".continue-here.md").read_text(encoding="utf-8")
    assert handoff["timestamp"] in md
    assert handoff["current_branch"] in md
    assert handoff["next_command"] in md


# ---------------------------------------------------------------------------
# run_pause — missing state.json
# ---------------------------------------------------------------------------


def test_run_pause_missing_state_exits_one(tmp_path: Path) -> None:
    # No state.json created
    result = run_pause(tmp_path)
    assert result == 1


def test_run_pause_missing_state_no_files_written(tmp_path: Path) -> None:
    run_pause(tmp_path)
    assert not (tmp_path / "HANDOFF.json").exists()
    assert not (tmp_path / ".continue-here.md").exists()


def test_run_pause_missing_state_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_pause(tmp_path)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_pause — corrupt state.json
# ---------------------------------------------------------------------------


def test_run_pause_corrupt_state_exits_one(tmp_path: Path) -> None:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir()
    (brick_dir / "state.json").write_text("{bad json,,,", encoding="utf-8")
    result = run_pause(tmp_path)
    assert result == 1


def test_run_pause_corrupt_state_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir()
    (brick_dir / "state.json").write_text("{bad json,,,", encoding="utf-8")
    run_pause(tmp_path)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


def test_run_pause_corrupt_state_no_files_written(tmp_path: Path) -> None:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir()
    (brick_dir / "state.json").write_text("{bad json", encoding="utf-8")
    run_pause(tmp_path)
    assert not (tmp_path / "HANDOFF.json").exists()


# ---------------------------------------------------------------------------
# run_pause — partial write safety
# ---------------------------------------------------------------------------


def test_run_pause_second_write_failure_removes_handoff(tmp_path: Path) -> None:
    """If .continue-here.md write fails, HANDOFF.json is cleaned up too."""
    root = _make_project(tmp_path)
    call_count = [0]
    original_write = Path.write_text

    def failing_second_write(self, content, **kwargs):
        call_count[0] += 1
        if call_count[0] == 2:
            raise OSError("Simulated write failure on second file")
        return original_write(self, content, **kwargs)

    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        with patch.object(Path, "write_text", failing_second_write):
            result = run_pause(root)

    assert result == 1
    assert not (root / "HANDOFF.json").exists()
    assert not (root / ".continue-here.md").exists()


def test_run_pause_second_write_failure_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    root = _make_project(tmp_path)
    call_count = [0]
    original_write = Path.write_text

    def failing_second_write(self, content, **kwargs):
        call_count[0] += 1
        if call_count[0] == 2:
            raise OSError("Simulated write failure")
        return original_write(self, content, **kwargs)

    with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
        with patch.object(Path, "write_text", failing_second_write):
            run_pause(root)

    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_setup(tmp_path: Path) -> None:
    _make_project(tmp_path)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )


def test_cli_pause_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer pause` exits 0."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
            result = cli_runner.invoke(app, ["pause"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_pause_writes_both_files(tmp_path: Path) -> None:
    """CliRunner: both HANDOFF.json and .continue-here.md are written."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
            cli_runner.invoke(app, ["pause"])
    finally:
        os.chdir(old_cwd)
    assert (tmp_path / "HANDOFF.json").exists()
    assert (tmp_path / ".continue-here.md").exists()


def test_cli_pause_handoff_json_correct_content(tmp_path: Path) -> None:
    """CliRunner: HANDOFF.json contains all 8 fields with correct values."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
            cli_runner.invoke(app, ["pause"])
    finally:
        os.chdir(old_cwd)
    data = json.loads((tmp_path / "HANDOFF.json").read_text(encoding="utf-8"))
    required = {"project", "brick", "brick_name", "last_action",
                "loop_count", "current_branch", "timestamp", "next_command"}
    assert required.issubset(set(data.keys()))
    assert data["brick"] == "9"
    assert data["last_action"] == "skeptic_packet_ready"


def test_cli_pause_continue_md_correct_content(tmp_path: Path) -> None:
    """CliRunner: .continue-here.md contains all required lines."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.pause._subprocess.run", side_effect=_fake_git_branch("brick/9")):
            cli_runner.invoke(app, ["pause"])
    finally:
        os.chdir(old_cwd)
    md = (tmp_path / ".continue-here.md").read_text(encoding="utf-8")
    for label in ["Last session ended:", "Project:", "Branch:",
                  "Current brick:", "Last action:", "Next command:"]:
        assert label in md
