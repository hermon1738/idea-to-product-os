"""Tests for Brick 19 — bricklayer new-project command."""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from cli.commands.new_project import (
    PROJECTS_RELPATH,
    _build_decision_log,
    _build_state_json,
    _build_state_md,
    _validate_name,
    run_new_project,
)
from cli.main import app

cli_runner = CliRunner()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REQUIRED_STATE_JSON_KEYS = {
    "project",
    "current_brick",
    "last_action",
    "loop_count",
    "current_branch",
    "current_feature",
    "current_phase",
    "last_test_run",
}

_REQUIRED_LAST_TEST_RUN_KEYS = {"command", "status", "exit_code", "artifact"}


def _setup_repo(tmp_path: Path) -> Path:
    """Create a minimal bricklayer.yaml so CliRunner commands can find the repo."""
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )
    return tmp_path


def _project_dir(root: Path, name: str) -> Path:
    return root / PROJECTS_RELPATH / name


# ---------------------------------------------------------------------------
# _validate_name
# ---------------------------------------------------------------------------


def test_validate_name_simple_alpha() -> None:
    assert _validate_name("myproject") is None


def test_validate_name_kebab() -> None:
    assert _validate_name("reddit-monitor") is None


def test_validate_name_underscore() -> None:
    assert _validate_name("my_project") is None


def test_validate_name_alphanumeric() -> None:
    assert _validate_name("project123") is None


def test_validate_name_mixed_kebab_underscore() -> None:
    assert _validate_name("my-project_v2") is None


def test_validate_name_invalid_space() -> None:
    assert _validate_name("my project") is not None


def test_validate_name_invalid_slash() -> None:
    assert _validate_name("my/project") is not None


def test_validate_name_invalid_backslash() -> None:
    assert _validate_name("my\\project") is not None


def test_validate_name_invalid_dot() -> None:
    assert _validate_name("my.project") is not None


def test_validate_name_invalid_at() -> None:
    assert _validate_name("my@project") is not None


def test_validate_name_invalid_exclamation() -> None:
    assert _validate_name("project!") is not None


def test_validate_name_empty() -> None:
    assert _validate_name("") is not None


def test_validate_name_returns_string_on_invalid() -> None:
    result = _validate_name("bad name")
    assert isinstance(result, str)
    assert len(result) > 0


# ---------------------------------------------------------------------------
# _build_state_md
# ---------------------------------------------------------------------------


def test_build_state_md_contains_name() -> None:
    content = _build_state_md("reddit-monitor", "2026-03-25")
    assert "reddit-monitor" in content


def test_build_state_md_contains_created_date() -> None:
    content = _build_state_md("reddit-monitor", "2026-03-25")
    assert "2026-03-25" in content


def test_build_state_md_contains_required_fields() -> None:
    content = _build_state_md("reddit-monitor", "2026-03-25")
    assert "Current brick: none" in content
    assert "Last action: none" in content
    assert "Next command: bricklayer status" in content
    assert "Blockers: none" in content


def test_build_state_md_heading_format() -> None:
    content = _build_state_md("myapp", "2026-03-25")
    assert content.startswith("# myapp — Project State")


# ---------------------------------------------------------------------------
# _build_decision_log
# ---------------------------------------------------------------------------


def test_build_decision_log_contains_name() -> None:
    content = _build_decision_log("reddit-monitor")
    assert "reddit-monitor" in content


def test_build_decision_log_has_table_header() -> None:
    content = _build_decision_log("reddit-monitor")
    assert "| Date | Component | Decision Made | Status | Next Action |" in content


def test_build_decision_log_has_separator_row() -> None:
    content = _build_decision_log("reddit-monitor")
    assert "|------|" in content


def test_build_decision_log_heading_format() -> None:
    content = _build_decision_log("myapp")
    assert "# myapp — Decision Log" in content


# ---------------------------------------------------------------------------
# _build_state_json
# ---------------------------------------------------------------------------


def test_build_state_json_has_all_required_keys() -> None:
    data = _build_state_json("myapp")
    assert _REQUIRED_STATE_JSON_KEYS <= set(data.keys())


def test_build_state_json_project_name() -> None:
    data = _build_state_json("reddit-monitor")
    assert data["project"] == "reddit-monitor"


def test_build_state_json_loop_count_zero() -> None:
    data = _build_state_json("myapp")
    assert data["loop_count"] == 0


def test_build_state_json_nulls_for_optional_fields() -> None:
    data = _build_state_json("myapp")
    assert data["current_brick"] is None
    assert data["last_action"] is None
    assert data["current_branch"] is None
    assert data["current_feature"] is None
    assert data["current_phase"] is None


def test_build_state_json_last_test_run_has_all_keys() -> None:
    data = _build_state_json("myapp")
    assert _REQUIRED_LAST_TEST_RUN_KEYS <= set(data["last_test_run"].keys())


def test_build_state_json_last_test_run_nulls() -> None:
    data = _build_state_json("myapp")
    ltr = data["last_test_run"]
    assert ltr["command"] is None
    assert ltr["status"] is None
    assert ltr["exit_code"] is None
    assert ltr["artifact"] is None


def test_build_state_json_serializable() -> None:
    data = _build_state_json("myapp")
    raw = json.dumps(data)
    parsed = json.loads(raw)
    assert parsed["project"] == "myapp"


# ---------------------------------------------------------------------------
# run_new_project — happy path
# ---------------------------------------------------------------------------


def test_run_new_project_returns_zero(tmp_path: Path) -> None:
    assert run_new_project(tmp_path, "myapp") == 0


def test_run_new_project_creates_project_directory(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    assert _project_dir(tmp_path, "myapp").is_dir()


def test_run_new_project_creates_state_md(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    assert (_project_dir(tmp_path, "myapp") / "STATE.md").exists()


def test_run_new_project_creates_decision_log(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    assert (_project_dir(tmp_path, "myapp") / "decision-log.md").exists()


def test_run_new_project_creates_state_json(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    assert (_project_dir(tmp_path, "myapp") / "state.json").exists()


def test_run_new_project_state_md_content(tmp_path: Path) -> None:
    run_new_project(tmp_path, "reddit-monitor")
    content = (_project_dir(tmp_path, "reddit-monitor") / "STATE.md").read_text()
    assert "reddit-monitor — Project State" in content
    assert "Current brick: none" in content
    assert "Next command: bricklayer status" in content


def test_run_new_project_state_md_created_date(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    content = (_project_dir(tmp_path, "myapp") / "STATE.md").read_text()
    today = datetime.date.today().isoformat()
    assert today in content


def test_run_new_project_decision_log_content(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    content = (_project_dir(tmp_path, "myapp") / "decision-log.md").read_text()
    assert "myapp — Decision Log" in content
    assert "| Date | Component | Decision Made | Status | Next Action |" in content


def test_run_new_project_state_json_valid_json(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    raw = (_project_dir(tmp_path, "myapp") / "state.json").read_text()
    data = json.loads(raw)
    assert isinstance(data, dict)


def test_run_new_project_state_json_all_fields(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    raw = (_project_dir(tmp_path, "myapp") / "state.json").read_text()
    data = json.loads(raw)
    assert _REQUIRED_STATE_JSON_KEYS <= set(data.keys())


def test_run_new_project_state_json_project_name(tmp_path: Path) -> None:
    run_new_project(tmp_path, "reddit-monitor")
    raw = (_project_dir(tmp_path, "reddit-monitor") / "state.json").read_text()
    data = json.loads(raw)
    assert data["project"] == "reddit-monitor"


def test_run_new_project_prints_success(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    run_new_project(tmp_path, "myapp")
    out = capsys.readouterr().out
    assert "Project created:" in out
    assert "myapp" in out


def test_run_new_project_creates_projects_dir_if_absent(tmp_path: Path) -> None:
    # context/projects/ does NOT exist yet in tmp_path
    assert not (tmp_path / "context" / "projects").exists()
    run_new_project(tmp_path, "myapp")
    assert (tmp_path / "context" / "projects").is_dir()


def test_run_new_project_kebab_name_valid(tmp_path: Path) -> None:
    assert run_new_project(tmp_path, "reddit-monitor") == 0
    assert _project_dir(tmp_path, "reddit-monitor").is_dir()


def test_run_new_project_underscore_name_valid(tmp_path: Path) -> None:
    assert run_new_project(tmp_path, "my_project") == 0
    assert _project_dir(tmp_path, "my_project").is_dir()


# ---------------------------------------------------------------------------
# run_new_project — duplicate
# ---------------------------------------------------------------------------


def test_run_new_project_duplicate_returns_one(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    assert run_new_project(tmp_path, "myapp") == 1


def test_run_new_project_duplicate_prints_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_new_project(tmp_path, "myapp")
    capsys.readouterr()  # clear first call output
    run_new_project(tmp_path, "myapp")
    err = capsys.readouterr().err
    assert "already exists" in err


def test_run_new_project_duplicate_no_new_files(tmp_path: Path) -> None:
    run_new_project(tmp_path, "myapp")
    state_md = _project_dir(tmp_path, "myapp") / "STATE.md"
    mtime_before = state_md.stat().st_mtime
    run_new_project(tmp_path, "myapp")
    mtime_after = state_md.stat().st_mtime
    assert mtime_before == mtime_after


# ---------------------------------------------------------------------------
# run_new_project — invalid names
# ---------------------------------------------------------------------------


def test_run_new_project_invalid_space_returns_one(tmp_path: Path) -> None:
    assert run_new_project(tmp_path, "my project") == 1


def test_run_new_project_invalid_space_no_dir(tmp_path: Path) -> None:
    run_new_project(tmp_path, "my project")
    assert not _project_dir(tmp_path, "my project").exists()


def test_run_new_project_invalid_slash_returns_one(tmp_path: Path) -> None:
    assert run_new_project(tmp_path, "my/project") == 1


def test_run_new_project_invalid_dot_returns_one(tmp_path: Path) -> None:
    assert run_new_project(tmp_path, "my.project") == 1


def test_run_new_project_invalid_backslash_returns_one(tmp_path: Path) -> None:
    assert run_new_project(tmp_path, "my\\project") == 1


def test_run_new_project_invalid_prints_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_new_project(tmp_path, "bad name")
    err = capsys.readouterr().err
    assert "error:" in err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------


def test_cli_new_project_exit_zero(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["new-project", "myapp"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_new_project_prints_created(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["new-project", "myapp"])
    finally:
        os.chdir(old_cwd)
    assert "Project created:" in result.output


def test_cli_new_project_all_files_exist(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        cli_runner.invoke(app, ["new-project", "myapp"])
    finally:
        os.chdir(old_cwd)
    proj = _project_dir(tmp_path, "myapp")
    assert (proj / "STATE.md").exists()
    assert (proj / "decision-log.md").exists()
    assert (proj / "state.json").exists()


def test_cli_new_project_state_json_content(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        cli_runner.invoke(app, ["new-project", "reddit-monitor"])
    finally:
        os.chdir(old_cwd)
    raw = (_project_dir(tmp_path, "reddit-monitor") / "state.json").read_text()
    data = json.loads(raw)
    assert data["project"] == "reddit-monitor"
    assert _REQUIRED_STATE_JSON_KEYS <= set(data.keys())


def test_cli_new_project_duplicate_exit_one(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        cli_runner.invoke(app, ["new-project", "myapp"])
        result = cli_runner.invoke(app, ["new-project", "myapp"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_new_project_invalid_name_exit_one(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["new-project", "bad name"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_new_project_output_contains_path(tmp_path: Path) -> None:
    _setup_repo(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["new-project", "reddit-monitor"])
    finally:
        os.chdir(old_cwd)
    assert "context/projects/reddit-monitor" in result.output
