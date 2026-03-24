"""Tests for cli/state.py — state.json reader/writer."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Ensure repo root is on sys.path so `cli` is importable
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.state import load, write  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_STATE: dict = {
    "current_brick": "Brick 2 - state.json Reader/Writer",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": ["Brick 1 - CLI Scaffold"],
    "next_action": "implement state module",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
        "failed_nodeids": [],
    },
}


def _write_state(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "state.json"
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Happy path: load a known state.json
# ---------------------------------------------------------------------------


def test_load_returns_all_schema_fields(tmp_path: Path) -> None:
    """load() returns dict with all required top-level fields."""
    p = _write_state(tmp_path, VALID_STATE)
    result = load(p)
    for field in (
        "current_brick",
        "status",
        "loop_count",
        "last_gate_failed",
        "completed_bricks",
        "next_action",
        "last_test_run",
    ):
        assert field in result, f"Missing field: {field}"


def test_load_values_match(tmp_path: Path) -> None:
    """load() returns values matching what was written."""
    p = _write_state(tmp_path, VALID_STATE)
    result = load(p)
    assert result["current_brick"] == "Brick 2 - state.json Reader/Writer"
    assert result["loop_count"] == 0
    assert result["completed_bricks"] == ["Brick 1 - CLI Scaffold"]


# ---------------------------------------------------------------------------
# Write update: change one field, reload, assert persisted
# ---------------------------------------------------------------------------


def test_write_update_persists(tmp_path: Path) -> None:
    """write() merges a field update; reloading reflects the change."""
    p = _write_state(tmp_path, VALID_STATE)
    write(p, {"status": "COMPLETED", "loop_count": 1})
    result = load(p)
    assert result["status"] == "COMPLETED"
    assert result["loop_count"] == 1


def test_write_preserves_other_fields(tmp_path: Path) -> None:
    """write() does not overwrite fields not in updates."""
    p = _write_state(tmp_path, VALID_STATE)
    write(p, {"next_action": "run skeptic gate"})
    result = load(p)
    assert result["next_action"] == "run skeptic gate"
    assert result["current_brick"] == VALID_STATE["current_brick"]
    assert result["completed_bricks"] == VALID_STATE["completed_bricks"]


def test_write_partial_nested_update_preserves_siblings(tmp_path: Path) -> None:
    """write() with a partial last_test_run dict deep-merges; sibling keys survive."""
    p = _write_state(tmp_path, VALID_STATE)
    write(p, {"last_test_run": {"exit_code": 1}})
    result = load(p)
    assert result["last_test_run"]["exit_code"] == 1
    assert result["last_test_run"]["command"] == VALID_STATE["last_test_run"]["command"]
    assert result["last_test_run"]["status"] == VALID_STATE["last_test_run"]["status"]


# ---------------------------------------------------------------------------
# Invalid schema: missing required field → ValueError
# ---------------------------------------------------------------------------


def test_write_missing_required_field_raises(tmp_path: Path) -> None:
    """write() with a state missing a required field raises ValueError."""
    p = tmp_path / "state.json"  # fresh file — no pre-existing state
    bad = {k: v for k, v in VALID_STATE.items() if k != "status"}
    with pytest.raises(ValueError, match="status"):
        write(p, bad)


def test_write_missing_last_test_run_raises(tmp_path: Path) -> None:
    """write() with state missing last_test_run raises ValueError."""
    bad = {k: v for k, v in VALID_STATE.items() if k != "last_test_run"}
    p = tmp_path / "state.json"
    # Write raw (bypass our write()) so the file has no last_test_run
    p.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="last_test_run"):
        write(p, {})


# ---------------------------------------------------------------------------
# Invalid schema: wrong type → ValueError
# ---------------------------------------------------------------------------


def test_write_wrong_type_loop_count_raises(tmp_path: Path) -> None:
    """write() where loop_count is a string raises ValueError."""
    p = _write_state(tmp_path, VALID_STATE)
    with pytest.raises(ValueError, match="loop_count"):
        write(p, {"loop_count": "zero"})


def test_write_wrong_type_completed_bricks_raises(tmp_path: Path) -> None:
    """write() where completed_bricks is not a list raises ValueError."""
    p = _write_state(tmp_path, VALID_STATE)
    with pytest.raises(ValueError, match="completed_bricks"):
        write(p, {"completed_bricks": "Brick 1"})


# ---------------------------------------------------------------------------
# Missing state.json: load → FileNotFoundError
# ---------------------------------------------------------------------------


def test_load_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    """load() on nonexistent path raises FileNotFoundError."""
    missing = tmp_path / "nonexistent" / "state.json"
    with pytest.raises(FileNotFoundError):
        load(missing)


def test_load_missing_file_error_has_path(tmp_path: Path) -> None:
    """FileNotFoundError message includes the missing path."""
    missing = tmp_path / "state.json"
    with pytest.raises(FileNotFoundError, match=str(missing)):
        load(missing)
