"""Tests for cli/commands/next.py — bricklayer next command."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.next import run_next  # noqa: E402
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_BASE_STATE: dict = {
    "current_brick": "Brick 4 - bricklayer next command",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": [],
    "next_action": "",  # overridden per test
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}


def _make_state(tmp_path: Path, next_action: str) -> Path:
    """Write state.json with the given next_action. Returns repo root."""
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    state = {**_BASE_STATE, "next_action": next_action}
    (brick_dir / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# Routing — known last_action values
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "next_action,expected_command",
    [
        ("snapshot_init", "bricklayer build --verify"),
        ("verify", "bricklayer build --test"),
        ("tests_passed", "bricklayer build --skeptic-packet"),
        ("skeptic_packet_ready", "bricklayer build --verdict PASS|FAIL"),
        ("brick_complete", "bricklayer build"),
    ],
)
def test_routing_known_actions(
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    next_action: str,
    expected_command: str,
) -> None:
    """run_next() maps each known next_action to the correct CLI command."""
    root = _make_state(tmp_path, next_action)
    exit_code = run_next(root)
    assert exit_code == 0
    out = capsys.readouterr().out.strip()
    assert out == expected_command


# ---------------------------------------------------------------------------
# Passthrough — unknown next_action
# ---------------------------------------------------------------------------


def test_unknown_next_action_passthrough(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Unknown next_action is printed as-is, exit 0."""
    root = _make_state(tmp_path, "Select and prepare next brick")
    exit_code = run_next(root)
    assert exit_code == 0
    out = capsys.readouterr().out.strip()
    assert out == "Select and prepare next brick"


# ---------------------------------------------------------------------------
# Missing state.json — clear error, exit 1, no traceback
# ---------------------------------------------------------------------------


def test_missing_state_json_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_next() returns 1 when state.json is absent."""
    exit_code = run_next(tmp_path)
    assert exit_code == 1


def test_missing_state_json_clear_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Error output mentions state.json and contains no raw traceback."""
    run_next(tmp_path)
    err = capsys.readouterr().err
    assert "state.json" in err
    assert "Traceback" not in err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

runner = CliRunner()


def _cli_invoke(tmp_path: Path, next_action: str | None = None) -> object:
    """Write project files and invoke `bricklayer next` via CliRunner."""
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )
    if next_action is not None:
        _make_state(tmp_path, next_action)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = runner.invoke(app, ["next"])
    finally:
        os.chdir(old_cwd)
    return result


def test_cli_runner_known_state_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer next` exits 0 for a known next_action."""
    result = _cli_invoke(tmp_path, next_action="snapshot_init")
    assert result.exit_code == 0


def test_cli_runner_known_state_correct_output(tmp_path: Path) -> None:
    """CliRunner: output is the routed command for snapshot_init."""
    result = _cli_invoke(tmp_path, next_action="snapshot_init")
    assert "bricklayer build --verify" in result.output


def test_cli_runner_missing_state_json_exits_one(tmp_path: Path) -> None:
    """CliRunner: `bricklayer next` exits 1 when state.json is absent."""
    result = _cli_invoke(tmp_path, next_action=None)
    assert result.exit_code == 1
