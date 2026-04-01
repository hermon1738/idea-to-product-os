"""Tests for _write_context_txt — automatic context.txt generation from bricklayer.yaml.

These tests exercise the function directly (not through the full CLI) so they
run fast and stay isolated from filesystem side effects in other tests.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.config import _write_context_txt  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_context(tmp_path: Path) -> str:
    return (tmp_path / "bricklayer" / "context.txt").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_writes_correct_content(tmp_path: Path) -> None:
    """Correct LANGUAGE and TEST_COMMAND lines are written when test: section exists."""
    config = {
        "test": {
            "language": "Python",
            "command": "python3 -m pytest -v ../tests/",
        }
    }
    _write_context_txt(tmp_path, config)
    content = _read_context(tmp_path)
    assert content == "LANGUAGE: Python\nTEST_COMMAND: python3 -m pytest -v ../tests/\n"


def test_writes_with_v_flag(tmp_path: Path) -> None:
    """context.txt contains -v when test.command contains -v."""
    config = {
        "test": {
            "language": "Python",
            "command": "python3 -m pytest -v ../proxy/tests/",
        }
    }
    _write_context_txt(tmp_path, config)
    content = _read_context(tmp_path)
    assert "-v" in content
    assert "TEST_COMMAND: python3 -m pytest -v ../proxy/tests/" in content


def test_missing_test_section_leaves_existing_context_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """When test: is absent, existing context.txt is left untouched and a warning is printed."""
    bricklayer_dir = tmp_path / "bricklayer"
    bricklayer_dir.mkdir()
    context_path = bricklayer_dir / "context.txt"
    original = "LANGUAGE: Go\nTEST_COMMAND: go test ./...\n"
    context_path.write_text(original, encoding="utf-8")

    config: dict = {}  # no test: section
    _write_context_txt(tmp_path, config)

    # File unchanged
    assert context_path.read_text(encoding="utf-8") == original
    # Warning emitted to stderr
    captured = capsys.readouterr()
    assert "warning" in captured.err
    assert "test:" in captured.err


def test_missing_test_section_no_existing_context_does_not_create_file(
    tmp_path: Path,
) -> None:
    """When test: is absent and no context.txt exists, no file is created."""
    config: dict = {}
    _write_context_txt(tmp_path, config)
    assert not (tmp_path / "bricklayer" / "context.txt").exists()


def test_missing_command_field_exits_with_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """test: section present but command missing → sys.exit(1) with clear error."""
    config = {"test": {"language": "Python"}}  # command absent
    with pytest.raises(SystemExit) as exc_info:
        _write_context_txt(tmp_path, config)
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "error" in captured.err
    assert "command" in captured.err


def test_creates_bricklayer_directory_if_missing(tmp_path: Path) -> None:
    """bricklayer/ directory is created if it doesn't exist."""
    config = {
        "test": {
            "language": "Python",
            "command": "python3 -m pytest -q ../tests/",
        }
    }
    assert not (tmp_path / "bricklayer").exists()
    _write_context_txt(tmp_path, config)
    assert (tmp_path / "bricklayer" / "context.txt").exists()


def test_write_is_atomic(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Write goes through a tempfile + os.replace, not a direct open() call."""
    replaced: list[tuple[str, str]] = []
    original_replace = os.replace

    def spy_replace(src: str, dst: str) -> None:
        replaced.append((src, str(dst)))
        original_replace(src, dst)

    monkeypatch.setattr(os, "replace", spy_replace)

    config = {
        "test": {
            "language": "Python",
            "command": "python3 -m pytest -v ../tests/",
        }
    }
    _write_context_txt(tmp_path, config)

    assert len(replaced) == 1
    src, dst = replaced[0]
    # Source is a tempfile (has a .tmp suffix per our implementation)
    assert src.endswith(".tmp")
    # Destination is the actual context.txt
    assert dst.endswith("context.txt")


def test_language_defaults_to_python_if_omitted(tmp_path: Path) -> None:
    """If language is not in the test: section, LANGUAGE defaults to Python."""
    config = {"test": {"command": "python3 -m pytest -q ../tests/"}}
    _write_context_txt(tmp_path, config)
    content = _read_context(tmp_path)
    assert content.startswith("LANGUAGE: Python\n")


def test_overwrites_existing_context_txt(tmp_path: Path) -> None:
    """Running _write_context_txt twice overwrites with the latest values."""
    bricklayer_dir = tmp_path / "bricklayer"
    bricklayer_dir.mkdir()
    (bricklayer_dir / "context.txt").write_text(
        "LANGUAGE: Go\nTEST_COMMAND: go test ./...\n", encoding="utf-8"
    )
    config = {
        "test": {
            "language": "Python",
            "command": "python3 -m pytest -v ../tests/",
        }
    }
    _write_context_txt(tmp_path, config)
    content = _read_context(tmp_path)
    assert "LANGUAGE: Python" in content
    assert "go test" not in content
