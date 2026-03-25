"""Tests for Brick 20 — bricklayer context command."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from cli.commands.context import (
    DIVIDER,
    PROJECTS_RELPATH,
    _load_project_state,
    _read_last_decisions,
    _read_next_command,
    _resolve_project_name,
    run_context,
)
from cli.main import app

cli_runner = CliRunner()

# ---------------------------------------------------------------------------
# Helpers / shared fixtures
# ---------------------------------------------------------------------------

_SAMPLE_STATE = {
    "project": "reddit-monitor",
    "current_brick": "Brick 20 - context",
    "last_action": "verify",
    "loop_count": 1,
    "current_branch": "brick/20-bricklayer-context",
    "current_feature": "feature/phase-4",
    "current_phase": "phase/2-context",
    "last_test_run": {"command": None, "status": None, "exit_code": None, "artifact": None},
}

_DECISION_HEADER = (
    "| Date | Component | Decision Made | Status | Next Action |\n"
    "|------|-----------|--------------|--------|-------------|\n"
)

_DECISION_ROW_1 = "| 2026-03-23 | auth | use JWT | DONE | deploy |"
_DECISION_ROW_2 = "| 2026-03-24 | db | use postgres | DONE | migrate |"
_DECISION_ROW_3 = "| 2026-03-25 | api | REST not gRPC | DONE | document |"
_DECISION_ROW_4 = "| 2026-03-26 | cache | use redis | DONE | configure |"


def _make_project(
    root: Path,
    name: str,
    state: dict | None = None,
    decisions: list[str] | None = None,
    next_cmd: str | None = None,
    malformed_state: bool = False,
) -> Path:
    """Create a full project directory at context/projects/<name>/."""
    proj = root / PROJECTS_RELPATH / name
    proj.mkdir(parents=True, exist_ok=True)

    # state.json
    if malformed_state:
        (proj / "state.json").write_text("{bad json,,", encoding="utf-8")
    else:
        data = state if state is not None else {**_SAMPLE_STATE, "project": name}
        (proj / "state.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    # decision-log.md
    rows = decisions if decisions is not None else []
    log_content = f"# {name} — Decision Log\n" + _DECISION_HEADER
    for row in rows:
        log_content += row + "\n"
    (proj / "decision-log.md").write_text(log_content, encoding="utf-8")

    # STATE.md
    cmd = next_cmd or "bricklayer status"
    (proj / "STATE.md").write_text(
        f"# {name} — Project State\n"
        f"Created: 2026-03-25\n"
        f"Current brick: none\n"
        f"Last action: none\n"
        f"Next command: {cmd}\n"
        f"Blockers: none\n",
        encoding="utf-8",
    )
    return proj


def _make_bricklayer_state(root: Path, project: str | None = "reddit-monitor") -> None:
    """Write bricklayer/state.json with the given project field."""
    bl_dir = root / "bricklayer"
    bl_dir.mkdir(exist_ok=True)
    (bl_dir / "state.json").write_text(
        json.dumps({"project": project, "current_brick": None, "status": "COMPLETED"}),
        encoding="utf-8",
    )


def _setup_repo(root: Path) -> None:
    """Write a minimal bricklayer.yaml for CliRunner tests."""
    (root / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# _load_project_state
# ---------------------------------------------------------------------------


def test_load_project_state_returns_dict(tmp_path: Path) -> None:
    proj = _make_project(tmp_path, "myapp")
    result = _load_project_state(proj)
    assert result is not None
    assert result["project"] == "myapp"


def test_load_project_state_missing_returns_none(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    result = _load_project_state(tmp_path / "nonexistent")
    assert result is None
    assert "error" in capsys.readouterr().err


def test_load_project_state_malformed_returns_none(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    proj = _make_project(tmp_path, "myapp", malformed_state=True)
    result = _load_project_state(proj)
    assert result is None
    assert "error" in capsys.readouterr().err


def test_load_project_state_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    proj = _make_project(tmp_path, "myapp", malformed_state=True)
    _load_project_state(proj)
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# _read_last_decisions
# ---------------------------------------------------------------------------


def test_read_last_decisions_returns_rows(tmp_path: Path) -> None:
    proj = _make_project(tmp_path, "myapp", decisions=[_DECISION_ROW_1, _DECISION_ROW_2])
    rows = _read_last_decisions(proj)
    assert len(rows) == 2
    assert _DECISION_ROW_1 in rows
    assert _DECISION_ROW_2 in rows


def test_read_last_decisions_limit_to_3(tmp_path: Path) -> None:
    proj = _make_project(
        tmp_path, "myapp",
        decisions=[_DECISION_ROW_1, _DECISION_ROW_2, _DECISION_ROW_3, _DECISION_ROW_4],
    )
    rows = _read_last_decisions(proj)
    assert len(rows) == 3


def test_read_last_decisions_returns_last_3(tmp_path: Path) -> None:
    proj = _make_project(
        tmp_path, "myapp",
        decisions=[_DECISION_ROW_1, _DECISION_ROW_2, _DECISION_ROW_3, _DECISION_ROW_4],
    )
    rows = _read_last_decisions(proj)
    assert _DECISION_ROW_4 in rows
    assert _DECISION_ROW_1 not in rows


def test_read_last_decisions_empty_log(tmp_path: Path) -> None:
    proj = _make_project(tmp_path, "myapp", decisions=[])
    rows = _read_last_decisions(proj)
    assert rows == []


def test_read_last_decisions_missing_file(tmp_path: Path) -> None:
    proj = tmp_path / "proj"
    proj.mkdir()
    rows = _read_last_decisions(proj)
    assert rows == []


def test_read_last_decisions_skips_header(tmp_path: Path) -> None:
    proj = _make_project(tmp_path, "myapp", decisions=[_DECISION_ROW_1])
    rows = _read_last_decisions(proj)
    assert not any("Date" in r for r in rows)


def test_read_last_decisions_skips_separator(tmp_path: Path) -> None:
    proj = _make_project(tmp_path, "myapp", decisions=[_DECISION_ROW_1])
    rows = _read_last_decisions(proj)
    assert not any(r.startswith("|---") for r in rows)


# ---------------------------------------------------------------------------
# _read_next_command
# ---------------------------------------------------------------------------


def test_read_next_command_returns_value(tmp_path: Path) -> None:
    proj = _make_project(tmp_path, "myapp", next_cmd="bricklayer build --snapshot")
    assert _read_next_command(proj) == "bricklayer build --snapshot"


def test_read_next_command_default_on_missing_file(tmp_path: Path) -> None:
    proj = tmp_path / "proj"
    proj.mkdir()
    assert _read_next_command(proj) == "bricklayer status"


def test_read_next_command_default_on_missing_field(tmp_path: Path) -> None:
    proj = tmp_path / "proj"
    proj.mkdir()
    (proj / "STATE.md").write_text("# no next command field here\n", encoding="utf-8")
    assert _read_next_command(proj) == "bricklayer status"


# ---------------------------------------------------------------------------
# _resolve_project_name
# ---------------------------------------------------------------------------


def test_resolve_project_name_with_arg(tmp_path: Path) -> None:
    assert _resolve_project_name(tmp_path, "myapp") == "myapp"


def test_resolve_project_name_from_bricklayer_state(tmp_path: Path) -> None:
    _make_bricklayer_state(tmp_path, project="reddit-monitor")
    assert _resolve_project_name(tmp_path, None) == "reddit-monitor"


def test_resolve_project_name_missing_state_returns_none(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    result = _resolve_project_name(tmp_path, None)
    assert result is None
    assert "error" in capsys.readouterr().err


def test_resolve_project_name_no_project_field_returns_none(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    bl_dir = tmp_path / "bricklayer"
    bl_dir.mkdir()
    (bl_dir / "state.json").write_text(
        json.dumps({"current_brick": None}), encoding="utf-8"
    )
    result = _resolve_project_name(tmp_path, None)
    assert result is None
    assert "error" in capsys.readouterr().err


def test_resolve_project_name_strips_brick_prefix(tmp_path: Path) -> None:
    _make_bricklayer_state(tmp_path, project="Brick 20 - myapp")
    result = _resolve_project_name(tmp_path, None)
    assert result == "myapp"


# ---------------------------------------------------------------------------
# run_context — happy path
# ---------------------------------------------------------------------------


def test_run_context_returns_zero(tmp_path: Path) -> None:
    _make_project(tmp_path, "myapp")
    assert run_context(tmp_path, "myapp") == 0


def test_run_context_prints_divider(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _make_project(tmp_path, "myapp")
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert DIVIDER in out


def test_run_context_prints_project_name(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _make_project(tmp_path, "reddit-monitor")
    run_context(tmp_path, "reddit-monitor")
    out = capsys.readouterr().out
    assert "PROJECT CONTEXT: reddit-monitor" in out


def test_run_context_prints_state_file_path(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _make_project(tmp_path, "myapp")
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "context/projects/myapp/state.json" in out


def test_run_context_prints_current_brick(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    state = {**_SAMPLE_STATE, "project": "myapp", "current_brick": "Brick 5 - auth"}
    _make_project(tmp_path, "myapp", state=state)
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "Brick 5 - auth" in out


def test_run_context_prints_last_action(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    state = {**_SAMPLE_STATE, "project": "myapp", "last_action": "snapshot_init"}
    _make_project(tmp_path, "myapp", state=state)
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "snapshot_init" in out


def test_run_context_prints_loop_count(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    state = {**_SAMPLE_STATE, "project": "myapp", "loop_count": 2}
    _make_project(tmp_path, "myapp", state=state)
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "Loop count:    2" in out


def test_run_context_prints_branch(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    state = {**_SAMPLE_STATE, "project": "myapp", "current_branch": "brick/5-auth"}
    _make_project(tmp_path, "myapp", state=state)
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "brick/5-auth" in out


def test_run_context_prints_next_command(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _make_project(tmp_path, "myapp", next_cmd="bricklayer build --test")
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "bricklayer build --test" in out


def test_run_context_prints_decisions(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _make_project(tmp_path, "myapp", decisions=[_DECISION_ROW_1, _DECISION_ROW_2])
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "2026-03-23" in out
    assert "auth" in out


def test_run_context_null_fields_show_none(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    state = {**_SAMPLE_STATE, "project": "myapp", "current_brick": None, "last_action": None}
    _make_project(tmp_path, "myapp", state=state)
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "Current brick: none" in out
    assert "Last action:   none" in out


# ---------------------------------------------------------------------------
# run_context — empty / no decisions
# ---------------------------------------------------------------------------


def test_run_context_no_decisions_prints_placeholder(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _make_project(tmp_path, "myapp", decisions=[])
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "No decisions logged yet" in out


def test_run_context_only_3_decisions_shown(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _make_project(
        tmp_path, "myapp",
        decisions=[_DECISION_ROW_1, _DECISION_ROW_2, _DECISION_ROW_3, _DECISION_ROW_4],
    )
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert _DECISION_ROW_1 not in out  # oldest excluded
    assert _DECISION_ROW_4 in out      # most recent included


# ---------------------------------------------------------------------------
# run_context — no --project (reads bricklayer/state.json)
# ---------------------------------------------------------------------------


def test_run_context_no_project_arg_reads_state(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _make_bricklayer_state(tmp_path, project="reddit-monitor")
    _make_project(tmp_path, "reddit-monitor")
    result = run_context(tmp_path, None)
    assert result == 0
    out = capsys.readouterr().out
    assert "PROJECT CONTEXT: reddit-monitor" in out


def test_run_context_no_project_no_state_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    # No bricklayer/state.json, no --project
    result = run_context(tmp_path, None)
    assert result == 1
    assert "error" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# run_context — error paths
# ---------------------------------------------------------------------------


def test_run_context_project_not_found_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    # context/projects/ exists but project doesn't
    (tmp_path / PROJECTS_RELPATH).mkdir(parents=True)
    result = run_context(tmp_path, "nonexistent")
    assert result == 1
    assert "error" in capsys.readouterr().err


def test_run_context_project_not_found_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    (tmp_path / PROJECTS_RELPATH).mkdir(parents=True)
    run_context(tmp_path, "nonexistent")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


def test_run_context_projects_dir_missing_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    result = run_context(tmp_path, "myapp")
    assert result == 1


def test_run_context_projects_dir_missing_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_context(tmp_path, "myapp")
    err = capsys.readouterr().err
    assert "No projects found" in err or "not found" in err


def test_run_context_malformed_state_json_returns_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _make_project(tmp_path, "myapp", malformed_state=True)
    result = run_context(tmp_path, "myapp")
    assert result == 1


def test_run_context_malformed_state_json_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _make_project(tmp_path, "myapp", malformed_state=True)
    run_context(tmp_path, "myapp")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


def test_run_context_malformed_state_json_error_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _make_project(tmp_path, "myapp", malformed_state=True)
    run_context(tmp_path, "myapp")
    assert "error" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# run_context — all 6 sections present
# ---------------------------------------------------------------------------


def test_run_context_all_six_sections(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _make_project(tmp_path, "myapp", decisions=[_DECISION_ROW_1])
    run_context(tmp_path, "myapp")
    out = capsys.readouterr().out
    # Section 1: header divider
    assert DIVIDER in out
    # Section 2: project name
    assert "PROJECT CONTEXT:" in out
    # Section 3: state fields
    assert "State file:" in out
    assert "Current brick:" in out
    assert "Last action:" in out
    assert "Loop count:" in out
    assert "Branch:" in out
    # Section 4: last 3 decisions
    assert "Last 3 decisions:" in out
    # Section 5: next command
    assert "Next command:" in out
    # Multiple dividers (at least 4)
    assert out.count(DIVIDER) >= 4


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------


def test_cli_context_exit_zero(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    _make_project(tmp_path, "myapp")
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["context", "--project", "myapp"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_context_output_has_project_name(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    _make_project(tmp_path, "reddit-monitor")
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["context", "--project", "reddit-monitor"])
    finally:
        os.chdir(old_cwd)
    assert "PROJECT CONTEXT: reddit-monitor" in result.output


def test_cli_context_output_has_all_six_sections(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    _make_project(tmp_path, "myapp", decisions=[_DECISION_ROW_1])
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["context", "--project", "myapp"])
    finally:
        os.chdir(old_cwd)
    out = result.output
    assert "PROJECT CONTEXT:" in out
    assert "State file:" in out
    assert "Last 3 decisions:" in out
    assert "Next command:" in out
    assert out.count(DIVIDER) >= 4


def test_cli_context_no_decisions(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    _make_project(tmp_path, "myapp", decisions=[])
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["context", "--project", "myapp"])
    finally:
        os.chdir(old_cwd)
    assert "No decisions logged yet" in result.output


def test_cli_context_project_not_found_exits_one(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    (tmp_path / PROJECTS_RELPATH).mkdir(parents=True)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["context", "--project", "ghost"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_context_no_flag_uses_bricklayer_state(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    _make_bricklayer_state(tmp_path, project="reddit-monitor")
    _make_project(tmp_path, "reddit-monitor")
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["context"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0
    assert "PROJECT CONTEXT: reddit-monitor" in result.output
