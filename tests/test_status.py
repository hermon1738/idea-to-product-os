"""Tests for cli/commands/status.py — bricklayer status command."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.status import run_status  # noqa: E402
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_STATE: dict = {
    "current_brick": "Brick 3 - bricklayer status command",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": ["Brick 1 - CLI Scaffold", "Brick 2 - state.json Reader/Writer"],
    "next_action": "implement status command",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}

STATE_MD_CONTENT = "project: bricklayer-cli\nphase: Foundation\n"


def _make_project(tmp_path: Path, with_state_md: bool = True) -> Path:
    """Create a minimal project tree under tmp_path. Returns the root."""
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir()
    state_json = brick_dir / "state.json"
    state_json.write_text(json.dumps(VALID_STATE, indent=2), encoding="utf-8")
    if with_state_md:
        (tmp_path / "STATE.md").write_text(STATE_MD_CONTENT, encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# Happy path: valid state.json + STATE.md
# ---------------------------------------------------------------------------


def test_happy_path_all_five_fields_printed(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_status() prints all 5 labeled fields and returns 0."""
    root = _make_project(tmp_path)
    exit_code = run_status(root)
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "project:" in out
    assert "phase:" in out
    assert "brick:" in out
    assert "last action:" in out
    assert "next:" in out


def test_happy_path_values_correct(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """run_status() prints values sourced from the correct files."""
    root = _make_project(tmp_path)
    run_status(root)
    out = capsys.readouterr().out
    assert "bricklayer-cli" in out
    assert "Foundation" in out
    assert "Brick 3 - bricklayer status command" in out
    assert "PASS" in out
    assert "implement status command" in out


# ---------------------------------------------------------------------------
# Missing STATE.md: fallback message, exit 0
# ---------------------------------------------------------------------------


def test_missing_state_md_exits_zero(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """When STATE.md is absent, exit code is still 0."""
    root = _make_project(tmp_path, with_state_md=False)
    exit_code = run_status(root)
    assert exit_code == 0


def test_missing_state_md_fallback_message(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """When STATE.md is absent, project and phase show fallback text, not blank."""
    root = _make_project(tmp_path, with_state_md=False)
    run_status(root)
    out = capsys.readouterr().out
    # Both fields must still appear with non-empty values (the fallback string)
    lines = {line.split(":")[0].strip(): line for line in out.splitlines() if ":" in line}
    assert "project" in lines
    assert "phase" in lines
    project_val = lines["project"].partition(":")[2].strip()
    phase_val = lines["phase"].partition(":")[2].strip()
    assert project_val != ""
    assert phase_val != ""


# ---------------------------------------------------------------------------
# Missing state.json: auto-create with defaults (Brick 26)
# ---------------------------------------------------------------------------


def test_missing_state_json_autocreates(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """When state.json is absent, run_status() auto-creates it and exits 0.

    Brick 26: load() uses mkdir(parents=True) so fresh-repo users get defaults
    on first invocation without pre-creating bricklayer/.
    """
    exit_code = run_status(tmp_path)  # bricklayer/state.json doesn't exist
    assert exit_code == 0


def test_missing_state_json_clear_error(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Error message is human-readable and contains 'state.json'."""
    run_status(tmp_path)
    err = capsys.readouterr().err
    assert "state.json" in err
    assert "Traceback" not in err


# ---------------------------------------------------------------------------
# CliRunner integration tests
# ---------------------------------------------------------------------------

runner = CliRunner()


def test_cli_runner_happy_path(tmp_path: Path) -> None:
    """CliRunner: status exits 0 and all 5 field labels appear in output."""
    _make_project(tmp_path)
    # Write a minimal bricklayer.yaml so find_yaml() resolves to tmp_path
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )
    result = runner.invoke(app, ["status"], catch_exceptions=False, env={"PWD": str(tmp_path)})
    # run_status is called with yaml_path.parent = tmp_path
    # We invoke directly via monkeypatching the working dir approach:
    # Since find_yaml walks from cwd, change cwd inside the runner invocation
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = runner.invoke(app, ["status"], catch_exceptions=False)
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 0
    for label in ("project:", "phase:", "brick:", "last action:", "next:"):
        assert label in result.output


def test_cli_runner_missing_state_json_autocreates(tmp_path: Path) -> None:
    """CliRunner: status exits 0 when state.json is absent (auto-create)."""
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )
    import os
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = runner.invoke(app, ["status"])
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 0
