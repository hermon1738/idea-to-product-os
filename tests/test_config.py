"""Tests for cli/config.py — YAML loader and path validation."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure repo root is on sys.path so `cli` is importable
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.config import load_and_validate  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_yaml(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "bricklayer.yaml"
    p.write_text(content, encoding="utf-8")
    return p


def _make_file(tmp_path: Path, rel: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Happy path — all paths valid
# ---------------------------------------------------------------------------


def test_happy_path_all_paths_valid(tmp_path: Path) -> None:
    """All declared paths exist → load_and_validate returns config dict."""
    _make_file(tmp_path, "system-prompts/plan.md")
    _make_file(tmp_path, "tools/verify.py")

    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  plan: system-prompts/plan.md\n"
        "tools:\n  verify: tools/verify.py\n"
        "agents: {}\n",
    )

    result = load_and_validate(yaml_path)
    assert isinstance(result, dict)
    assert "phases" in result
    assert "tools" in result


def test_happy_path_empty_sections(tmp_path: Path) -> None:
    """Empty sections are valid — no files to check."""
    yaml_path = _write_yaml(tmp_path, "phases: {}\ntools: {}\nagents: {}\n")
    result = load_and_validate(yaml_path)
    assert result == {"phases": {}, "tools": {}, "agents": {}}


# ---------------------------------------------------------------------------
# Missing path → error message + exit 1
# ---------------------------------------------------------------------------


def test_missing_path_prints_error_and_exits(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """One path declared but absent → human-readable error, exit 1."""
    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  plan: system-prompts/nonexistent.md\n"
        "tools: {}\nagents: {}\n",
    )

    with pytest.raises(SystemExit) as exc_info:
        load_and_validate(yaml_path)

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "Missing: system-prompts/nonexistent.md" in err
    assert "check bricklayer.yaml" in err


def test_missing_path_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Error output must not contain 'Traceback'."""
    yaml_path = _write_yaml(
        tmp_path,
        "tools:\n  missing_tool: tools/ghost.py\n"
        "phases: {}\nagents: {}\n",
    )

    with pytest.raises(SystemExit):
        load_and_validate(yaml_path)

    err = capsys.readouterr().err
    assert "Traceback" not in err


def test_multiple_missing_paths_all_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """All missing paths are reported, not just the first one."""
    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  a: missing/a.md\n  b: missing/b.md\n"
        "tools: {}\nagents: {}\n",
    )

    with pytest.raises(SystemExit) as exc_info:
        load_and_validate(yaml_path)

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "missing/a.md" in err
    assert "missing/b.md" in err


# ---------------------------------------------------------------------------
# Missing YAML file entirely → exit 1
# ---------------------------------------------------------------------------


def test_missing_yaml_file_exits_with_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """No bricklayer.yaml → human-readable message, exit 1."""
    yaml_path = tmp_path / "bricklayer.yaml"  # does NOT exist

    with pytest.raises(SystemExit) as exc_info:
        load_and_validate(yaml_path)

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "bricklayer.yaml not found at repo root" in err


def test_missing_yaml_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Missing yaml error must not include 'Traceback'."""
    yaml_path = tmp_path / "bricklayer.yaml"

    with pytest.raises(SystemExit):
        load_and_validate(yaml_path)

    err = capsys.readouterr().err
    assert "Traceback" not in err
