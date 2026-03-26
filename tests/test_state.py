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
# Missing state.json — parent absent: load → FileNotFoundError
# ---------------------------------------------------------------------------


def test_load_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    """load() raises FileNotFoundError when parent directory also doesn't exist.

    Auto-create only fires when the parent directory exists. When the parent
    is also absent there is no safe place to write defaults, so the function
    must still raise rather than silently creating nested directories.
    """
    missing = tmp_path / "nonexistent" / "state.json"
    with pytest.raises(FileNotFoundError):
        load(missing)


# ---------------------------------------------------------------------------
# Missing state.json — parent exists: auto-create with defaults (Brick 26)
# ---------------------------------------------------------------------------


def test_load_autocreate_returns_valid_dict(tmp_path: Path) -> None:
    """load() returns a valid dict when state.json is missing but parent exists.

    The returned dict must contain all required schema fields so callers
    (e.g. ``bricklayer status``) can operate on a fresh project without any
    manual bootstrap step.
    """
    state_path = tmp_path / "state.json"
    result = load(state_path)
    assert isinstance(result, dict)
    for field in ("current_brick", "status", "loop_count", "last_test_run",
                  "completed_bricks", "next_action", "last_gate_failed"):
        assert field in result, f"Auto-created state missing required field: {field}"


def test_load_autocreate_creates_file_on_disk(tmp_path: Path) -> None:
    """load() writes state.json to disk when it auto-creates.

    The file must exist after the call so that a second load() reads from
    disk rather than auto-creating again (idempotent after first creation).
    """
    state_path = tmp_path / "state.json"
    assert not state_path.exists()
    load(state_path)
    assert state_path.exists()


def test_load_autocreate_project_name_from_repo_root(tmp_path: Path) -> None:
    """Auto-created state derives project name from the repo root directory.

    state.json lives at <repo-root>/bricklayer/state.json. The project name
    is expected to be <repo-root>.name — two levels above state.json.
    """
    bricklayer_dir = tmp_path / "bricklayer"
    bricklayer_dir.mkdir()
    state_path = bricklayer_dir / "state.json"
    result = load(state_path)
    # tmp_path.name is the repo root directory name in this test layout
    assert result["project"] == tmp_path.name


def test_load_autocreate_passes_schema_validation(tmp_path: Path) -> None:
    """Auto-created state passes schema validation (i.e. load() can reload it).

    Ensures that auto-created defaults are not just internally consistent but
    also survive the same _validate() gate that every normal state.json must
    pass. A second load() on the written file is the easiest way to confirm.
    """
    state_path = tmp_path / "state.json"
    load(state_path)  # auto-create
    reloaded = load(state_path)  # read from disk — must not raise
    assert isinstance(reloaded, dict)


def test_load_autocreate_prints_warning_to_stderr(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Auto-create prints a warning to stderr naming the created path.

    The message must be on stderr (not stdout) and must include the file path
    so the user knows exactly where the defaults were written.
    """
    state_path = tmp_path / "state.json"
    load(state_path)
    captured = capsys.readouterr()
    assert str(state_path) in captured.err
    assert "state.json not found" in captured.err
    assert "created with defaults" in captured.err


def test_load_autocreate_default_current_brick_is_empty_string(tmp_path: Path) -> None:
    """Auto-created state has current_brick == '' (not null).

    A null current_brick would fail schema validation for any subsequent
    state_write call — the auto-create default must be the empty string so
    close-phase and close-feature can run on a fresh project without crashing.
    """
    state_path = tmp_path / "state.json"
    result = load(state_path)
    assert result["current_brick"] == ""


def test_load_autocreate_is_idempotent(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Second load() on auto-created state reads from disk, no second warning.

    Ensures the warning only fires on first creation, not on every subsequent
    call. Two warnings in a row would confuse users who call ``bricklayer``
    commands back-to-back on a fresh project.
    """
    state_path = tmp_path / "state.json"
    load(state_path)  # creates file + prints warning
    capsys.readouterr()  # drain captured output
    load(state_path)  # reads from disk
    captured = capsys.readouterr()
    assert captured.err == ""  # no second warning
