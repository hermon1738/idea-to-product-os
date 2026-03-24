"""Tests for cli/commands/build.py — bricklayer build (print contract)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.build import parse_spec, run_build, _NO_GATE_MSG  # noqa: E402
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Sample spec text
# ---------------------------------------------------------------------------

FULL_SPEC = """\
BRICK: Brick 5 - test

WHAT:
  Read spec.md and print it.

INPUT:
  bricklayer/spec.md

OUTPUT:
  Formatted contract, 6 fields.

GATE:
  RUNS — prints contract, exit 0.

BLOCKER:
  Bricks 6-8.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/build.py
"""

SPEC_NO_GATE = """\
BRICK: Brick 5 - test

WHAT:
  Read spec.md and print it.

INPUT:
  bricklayer/spec.md

OUTPUT:
  Formatted contract, 6 fields.

BLOCKER:
  Bricks 6-8.

WAVE:
  SEQUENTIAL
"""

SPEC_EMPTY_GATE = """\
BRICK: Brick 5 - test

WHAT:
  Read spec.md and print it.

INPUT:
  bricklayer/spec.md

OUTPUT:
  Formatted contract, 6 fields.

GATE:

BLOCKER:
  Bricks 6-8.

WAVE:
  SEQUENTIAL
"""


def _write_spec(tmp_path: Path, content: str) -> Path:
    """Write bricklayer/spec.md under tmp_path. Returns repo root."""
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    (brick_dir / "spec.md").write_text(content, encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# parse_spec unit tests
# ---------------------------------------------------------------------------


def test_parse_spec_returns_all_six_fields() -> None:
    """parse_spec() extracts all 6 CONTRACT_FIELDS from a full spec."""
    result = parse_spec(FULL_SPEC)
    for field in ("WHAT", "INPUT", "OUTPUT", "GATE", "BLOCKER", "WAVE"):
        assert field in result, f"Missing field: {field}"
        assert result[field].strip() != "", f"Field {field} is empty"


def test_parse_spec_values_match() -> None:
    """parse_spec() returns the correct content for each field."""
    result = parse_spec(FULL_SPEC)
    assert "Read spec.md" in result["WHAT"]
    assert "bricklayer/spec.md" in result["INPUT"]
    assert "RUNS" in result["GATE"]
    assert "SEQUENTIAL" in result["WAVE"]


def test_parse_spec_missing_gate_returns_empty() -> None:
    """parse_spec() returns no GATE key (or empty string) when absent."""
    result = parse_spec(SPEC_NO_GATE)
    assert result.get("GATE", "").strip() == ""


def test_parse_spec_empty_gate_returns_empty_string() -> None:
    """parse_spec() returns empty string for a blank GATE section."""
    result = parse_spec(SPEC_EMPTY_GATE)
    assert result.get("GATE", "").strip() == ""


# ---------------------------------------------------------------------------
# run_build — happy path
# ---------------------------------------------------------------------------


def test_run_build_happy_path_exits_zero(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_build() returns 0 for a valid spec.md."""
    root = _write_spec(tmp_path, FULL_SPEC)
    exit_code = run_build(root)
    assert exit_code == 0


def test_run_build_happy_path_all_six_labels(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_build() prints all 6 field labels."""
    root = _write_spec(tmp_path, FULL_SPEC)
    run_build(root)
    out = capsys.readouterr().out
    for label in ("what:", "input:", "output:", "gate:", "blocker:", "wave:"):
        assert label in out, f"Missing label: {label}"


# ---------------------------------------------------------------------------
# run_build — missing Gate
# ---------------------------------------------------------------------------


def test_run_build_missing_gate_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_build() returns 1 when GATE is absent."""
    root = _write_spec(tmp_path, SPEC_NO_GATE)
    exit_code = run_build(root)
    assert exit_code == 1


def test_run_build_missing_gate_prints_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_build() prints the no-gate message when GATE is absent."""
    root = _write_spec(tmp_path, SPEC_NO_GATE)
    run_build(root)
    out = capsys.readouterr().out
    assert _NO_GATE_MSG in out


def test_run_build_missing_gate_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """No raw Python traceback on missing Gate."""
    root = _write_spec(tmp_path, SPEC_NO_GATE)
    run_build(root)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_build — empty Gate
# ---------------------------------------------------------------------------


def test_run_build_empty_gate_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_build() returns 1 when GATE is present but blank."""
    root = _write_spec(tmp_path, SPEC_EMPTY_GATE)
    exit_code = run_build(root)
    assert exit_code == 1


def test_run_build_empty_gate_prints_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_build() prints the no-gate message when GATE is blank."""
    root = _write_spec(tmp_path, SPEC_EMPTY_GATE)
    run_build(root)
    out = capsys.readouterr().out
    assert _NO_GATE_MSG in out


# ---------------------------------------------------------------------------
# run_build — missing spec.md
# ---------------------------------------------------------------------------


def test_run_build_missing_spec_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """run_build() returns 1 when spec.md is absent."""
    exit_code = run_build(tmp_path)
    assert exit_code == 1


def test_run_build_missing_spec_clear_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Error output mentions spec.md and contains no raw traceback."""
    run_build(tmp_path)
    err = capsys.readouterr().err
    assert "spec.md" in err
    assert "Traceback" not in err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

runner = CliRunner()


def _cli_invoke(tmp_path: Path, spec_content: str | None = FULL_SPEC) -> object:
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )
    if spec_content is not None:
        _write_spec(tmp_path, spec_content)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = runner.invoke(app, ["build"])
    finally:
        os.chdir(old_cwd)
    return result


def test_cli_runner_valid_spec_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build` exits 0 for a valid spec.md."""
    result = _cli_invoke(tmp_path)
    assert result.exit_code == 0


def test_cli_runner_valid_spec_all_labels(tmp_path: Path) -> None:
    """CliRunner: output contains all 6 field labels."""
    result = _cli_invoke(tmp_path)
    for label in ("what:", "input:", "output:", "gate:", "blocker:", "wave:"):
        assert label in result.output, f"Missing label: {label}"


def test_cli_runner_missing_gate_exits_one(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build` exits 1 when GATE is absent."""
    result = _cli_invoke(tmp_path, spec_content=SPEC_NO_GATE)
    assert result.exit_code == 1
