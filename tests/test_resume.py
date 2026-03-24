"""Tests for Brick 10 — bricklayer resume command."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.resume import _format_block, _RULE, run_resume  # noqa: E402
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_SAMPLE_HANDOFF: dict = {
    "project": "bricklayer-cli",
    "brick": "10",
    "brick_name": "bricklayer resume",
    "last_action": "skeptic_packet_ready",
    "loop_count": 0,
    "current_branch": "brick/10-bricklayer-resume",
    "timestamp": "2026-03-24T10:00:00+00:00",
    "next_command": "bricklayer build --verdict PASS|FAIL",
}


def _write_handoff(root: Path, data: dict | None = None) -> None:
    h = data if data is not None else _SAMPLE_HANDOFF
    (root / "HANDOFF.json").write_text(json.dumps(h, indent=2), encoding="utf-8")


def _fake_git(branch: str):
    def _side(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = branch + "\n"
        return m
    return _side


# ---------------------------------------------------------------------------
# _format_block
# ---------------------------------------------------------------------------


def test_format_block_contains_rule_lines() -> None:
    out = _format_block(_SAMPLE_HANDOFF)
    assert out.count(_RULE) == 4


def test_format_block_contains_resuming_session() -> None:
    assert "RESUMING SESSION" in _format_block(_SAMPLE_HANDOFF)


def test_format_block_contains_project() -> None:
    assert "bricklayer-cli" in _format_block(_SAMPLE_HANDOFF)


def test_format_block_contains_branch() -> None:
    assert "brick/10-bricklayer-resume" in _format_block(_SAMPLE_HANDOFF)


def test_format_block_contains_brick_number_and_name() -> None:
    out = _format_block(_SAMPLE_HANDOFF)
    assert "10" in out
    assert "bricklayer resume" in out


def test_format_block_contains_last_action() -> None:
    assert "skeptic_packet_ready" in _format_block(_SAMPLE_HANDOFF)


def test_format_block_contains_loop_count() -> None:
    assert "0" in _format_block(_SAMPLE_HANDOFF)


def test_format_block_contains_timestamp() -> None:
    assert "2026-03-24T10:00:00" in _format_block(_SAMPLE_HANDOFF)


def test_format_block_contains_next_command() -> None:
    assert "bricklayer build --verdict PASS|FAIL" in _format_block(_SAMPLE_HANDOFF)


# ---------------------------------------------------------------------------
# run_resume — happy path
# ---------------------------------------------------------------------------


def test_run_resume_returns_zero(tmp_path: Path) -> None:
    _write_handoff(tmp_path)
    with patch("cli.commands.resume._subprocess.run", side_effect=_fake_git("brick/10-bricklayer-resume")):
        result = run_resume(tmp_path)
    assert result == 0


def test_run_resume_prints_all_fields(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _write_handoff(tmp_path)
    with patch("cli.commands.resume._subprocess.run", side_effect=_fake_git("brick/10-bricklayer-resume")):
        run_resume(tmp_path)
    out = capsys.readouterr().out
    assert "bricklayer-cli" in out
    assert "brick/10-bricklayer-resume" in out
    assert "10" in out
    assert "bricklayer resume" in out
    assert "skeptic_packet_ready" in out
    assert "2026-03-24T10:00:00" in out
    assert "bricklayer build --verdict PASS|FAIL" in out


def test_run_resume_output_contains_divider_lines(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_handoff(tmp_path)
    with patch("cli.commands.resume._subprocess.run", side_effect=_fake_git("brick/10-bricklayer-resume")):
        run_resume(tmp_path)
    out = capsys.readouterr().out
    assert _RULE in out


# ---------------------------------------------------------------------------
# run_resume — branch match (no warning)
# ---------------------------------------------------------------------------


def test_run_resume_branch_match_no_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_handoff(tmp_path)
    with patch(
        "cli.commands.resume._subprocess.run",
        side_effect=_fake_git("brick/10-bricklayer-resume"),
    ):
        run_resume(tmp_path)
    out = capsys.readouterr().out
    assert "Warning" not in out


# ---------------------------------------------------------------------------
# run_resume — branch mismatch (warning, still exit 0)
# ---------------------------------------------------------------------------


def test_run_resume_branch_mismatch_exits_zero(tmp_path: Path) -> None:
    _write_handoff(tmp_path)
    with patch("cli.commands.resume._subprocess.run", side_effect=_fake_git("main")):
        result = run_resume(tmp_path)
    assert result == 0


def test_run_resume_branch_mismatch_prints_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_handoff(tmp_path)
    with patch("cli.commands.resume._subprocess.run", side_effect=_fake_git("main")):
        run_resume(tmp_path)
    out = capsys.readouterr().out
    assert "Warning" in out
    assert "main" in out
    assert "brick/10-bricklayer-resume" in out


def test_run_resume_branch_mismatch_warning_includes_checkout_hint(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_handoff(tmp_path)
    with patch("cli.commands.resume._subprocess.run", side_effect=_fake_git("some-other-branch")):
        run_resume(tmp_path)
    out = capsys.readouterr().out
    assert "git checkout" in out
    assert "brick/10-bricklayer-resume" in out


# ---------------------------------------------------------------------------
# run_resume — missing HANDOFF.json
# ---------------------------------------------------------------------------


def test_run_resume_missing_handoff_exits_one(tmp_path: Path) -> None:
    result = run_resume(tmp_path)
    assert result == 1


def test_run_resume_missing_handoff_correct_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_resume(tmp_path)
    err = capsys.readouterr().err
    assert "No session to resume" in err
    assert "bricklayer pause" in err


def test_run_resume_missing_handoff_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_resume(tmp_path)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_resume — malformed HANDOFF.json
# ---------------------------------------------------------------------------


def test_run_resume_malformed_json_exits_one(tmp_path: Path) -> None:
    (tmp_path / "HANDOFF.json").write_text("{bad json,,,", encoding="utf-8")
    result = run_resume(tmp_path)
    assert result == 1


def test_run_resume_malformed_json_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    (tmp_path / "HANDOFF.json").write_text("{bad json", encoding="utf-8")
    run_resume(tmp_path)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


def test_run_resume_malformed_json_prints_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    (tmp_path / "HANDOFF.json").write_text("{bad json", encoding="utf-8")
    run_resume(tmp_path)
    assert "error" in capsys.readouterr().err.lower()


# ---------------------------------------------------------------------------
# run_resume — missing required field
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("missing_field", [
    "project", "brick", "brick_name", "last_action",
    "loop_count", "current_branch", "timestamp", "next_command",
])
def test_run_resume_missing_field_exits_one(tmp_path: Path, missing_field: str) -> None:
    data = {k: v for k, v in _SAMPLE_HANDOFF.items() if k != missing_field}
    _write_handoff(tmp_path, data)
    result = run_resume(tmp_path)
    assert result == 1


@pytest.mark.parametrize("missing_field", [
    "project", "brick", "last_action", "next_command",
])
def test_run_resume_missing_field_names_field_in_error(
    tmp_path: Path, capsys: pytest.CaptureFixture, missing_field: str
) -> None:
    data = {k: v for k, v in _SAMPLE_HANDOFF.items() if k != missing_field}
    _write_handoff(tmp_path, data)
    run_resume(tmp_path)
    assert missing_field in capsys.readouterr().err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_setup(tmp_path: Path, handoff: dict | None = None) -> None:
    _write_handoff(tmp_path, handoff)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )


def test_cli_resume_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.resume._subprocess.run",
                   side_effect=_fake_git("brick/10-bricklayer-resume")):
            result = cli_runner.invoke(app, ["resume"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_resume_output_contains_all_fields(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.resume._subprocess.run",
                   side_effect=_fake_git("brick/10-bricklayer-resume")):
            result = cli_runner.invoke(app, ["resume"])
    finally:
        os.chdir(old_cwd)
    out = result.output
    assert "RESUMING SESSION" in out
    assert "bricklayer-cli" in out
    assert "brick/10-bricklayer-resume" in out
    assert "10" in out
    assert "bricklayer resume" in out
    assert "skeptic_packet_ready" in out
    assert "bricklayer build --verdict PASS|FAIL" in out


def test_cli_resume_missing_handoff_exits_one(tmp_path: Path) -> None:
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["resume"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_resume_branch_mismatch_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.resume._subprocess.run",
                   side_effect=_fake_git("wrong-branch")):
            result = cli_runner.invoke(app, ["resume"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0
    assert "Warning" in result.output
