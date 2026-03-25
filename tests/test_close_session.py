"""Tests for Brick 12 / Brick 18 — bricklayer close-session command."""

from __future__ import annotations

import datetime
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

from cli.commands.close_session import (  # noqa: E402
    GROQ_HEAVY_MODEL,
    SESSION_LOG_RELPATH,
    STATE_MD_RELPATH,
    _append_decision_log,
    _build_decision_log_row,
    _build_pipeline_status,
    _build_user_message,
    _call_groq,
    _extract_structured_data,
    _load_sprint_brain,
    _load_state,
    _sanitize_pipe,
    _sync_docs,
    _write_session_log,
    _write_state_md,
    run_close_session,
)
from cli.main import app  # noqa: E402

# ---------------------------------------------------------------------------
# Shared fixtures / helpers
# ---------------------------------------------------------------------------

_SAMPLE_STATE: dict = {
    "current_brick": "Brick 12 - bricklayer close-session",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": ["Brick 11 - bricklayer commit"],
    "next_action": "skeptic_packet_ready",
    "last_test_run": {"status": "PASS", "exit_code": 0},
}

_SPRINT_BRAIN_CONTENT = "# SPRINT-BRAIN\nYou are a senior engineer running a sprint review."
_GROQ_RESPONSE = "Sprint review: all bricks passed, pipeline is healthy."


def _write_state(root: Path, data: dict | None = None) -> None:
    (root / "bricklayer").mkdir(exist_ok=True)
    (root / "bricklayer" / "state.json").write_text(
        json.dumps(data if data is not None else _SAMPLE_STATE, indent=2),
        encoding="utf-8",
    )


def _write_yaml(root: Path, review_path: str | None = "system-prompts/sprint-brain.md") -> None:
    if review_path is not None:
        content = f"phases:\n  review: {review_path}\ntools: {{}}\nagents: {{}}\n"
    else:
        content = "phases: {}\ntools: {}\nagents: {}\n"
    (root / "bricklayer.yaml").write_text(content, encoding="utf-8")


def _write_sprint_brain(root: Path, path: str = "system-prompts/sprint-brain.md") -> None:
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(_SPRINT_BRAIN_CONTENT, encoding="utf-8")


def _full_setup(tmp_path: Path) -> None:
    _write_state(tmp_path)
    _write_yaml(tmp_path)
    _write_sprint_brain(tmp_path)


def _mock_groq_success():
    mock = MagicMock()
    mock.choices[0].message.content = _GROQ_RESPONSE
    return mock


# ---------------------------------------------------------------------------
# _load_state
# ---------------------------------------------------------------------------


def test_load_state_returns_dict(tmp_path: Path) -> None:
    _write_state(tmp_path)
    result = _load_state(tmp_path)
    assert result is not None
    assert result["current_brick"] == "Brick 12 - bricklayer close-session"


def test_load_state_missing_returns_none(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    result = _load_state(tmp_path)
    assert result is None
    assert "error" in capsys.readouterr().err.lower()


def test_load_state_corrupt_returns_none(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    (tmp_path / "bricklayer").mkdir()
    (tmp_path / "bricklayer" / "state.json").write_text("{bad json,,", encoding="utf-8")
    result = _load_state(tmp_path)
    assert result is None
    assert "error" in capsys.readouterr().err.lower()


# ---------------------------------------------------------------------------
# _load_sprint_brain
# ---------------------------------------------------------------------------


def test_load_sprint_brain_returns_content(tmp_path: Path) -> None:
    _write_yaml(tmp_path)
    _write_sprint_brain(tmp_path)
    result = _load_sprint_brain(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == _SPRINT_BRAIN_CONTENT


def test_load_sprint_brain_missing_review_key(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _write_yaml(tmp_path, review_path=None)
    result = _load_sprint_brain(tmp_path, tmp_path / "bricklayer.yaml")
    assert result is None
    err = capsys.readouterr().err
    assert "phases.review" in err


def test_load_sprint_brain_file_not_found(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    _write_yaml(tmp_path, review_path="system-prompts/sprint-brain.md")
    # Do NOT write the sprint-brain file
    result = _load_sprint_brain(tmp_path, tmp_path / "bricklayer.yaml")
    assert result is None
    err = capsys.readouterr().err
    assert "sprint-brain.md" in err
    assert "system-prompts/sprint-brain.md" in err


# ---------------------------------------------------------------------------
# _build_user_message
# ---------------------------------------------------------------------------


def test_build_user_message_contains_current_brick() -> None:
    msg = _build_user_message(_SAMPLE_STATE)
    assert "Brick 12 - bricklayer close-session" in msg


def test_build_user_message_contains_completed_bricks() -> None:
    msg = _build_user_message(_SAMPLE_STATE)
    assert "Brick 11 - bricklayer commit" in msg


def test_build_user_message_contains_status() -> None:
    msg = _build_user_message(_SAMPLE_STATE)
    assert "IN_PROGRESS" in msg


def test_build_user_message_null_current_brick() -> None:
    state = {**_SAMPLE_STATE, "current_brick": None}
    msg = _build_user_message(state)
    assert "unknown" in msg


def test_build_user_message_empty_completed_bricks() -> None:
    state = {**_SAMPLE_STATE, "completed_bricks": []}
    msg = _build_user_message(state)
    assert "none recorded" in msg


# ---------------------------------------------------------------------------
# _call_groq — happy path (mocked)
# ---------------------------------------------------------------------------


def test_call_groq_returns_text() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        result = _call_groq("fake-key", "sys prompt", "user msg")
    assert result == _GROQ_RESPONSE


def test_call_groq_passes_model() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        _call_groq("fake-key", "sys", "user")
        call_kwargs = client.chat.completions.create.call_args
        assert call_kwargs.kwargs.get("model") == "llama-3.1-8b-instant"


def test_call_groq_passes_system_and_user_messages() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        _call_groq("fake-key", "my-system-prompt", "my-user-message")
        messages = client.chat.completions.create.call_args.kwargs["messages"]
        roles = {m["role"]: m["content"] for m in messages}
        assert roles["system"] == "my-system-prompt"
        assert roles["user"] == "my-user-message"


def test_call_groq_uses_timeout() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        _call_groq("fake-key", "sys", "user")
        init_kwargs = MockGroq.call_args.kwargs
        assert "timeout" in init_kwargs
        assert init_kwargs["timeout"] > 0


def test_call_groq_exception_returns_none(capsys: pytest.CaptureFixture) -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("HTTP 503")
        result = _call_groq("fake-key", "sys", "user")
    assert result is None
    err = capsys.readouterr().err
    assert "error" in err.lower()
    assert "Groq" in err or "groq" in err.lower()


def test_call_groq_exception_no_traceback(capsys: pytest.CaptureFixture) -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = Exception("connection refused")
        _call_groq("fake-key", "sys", "user")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# _write_session_log
# ---------------------------------------------------------------------------


def test_write_session_log_creates_file(tmp_path: Path) -> None:
    assert _write_session_log(tmp_path, _SAMPLE_STATE, _GROQ_RESPONSE)
    assert (tmp_path / SESSION_LOG_RELPATH).exists()


def test_write_session_log_contains_timestamp(tmp_path: Path) -> None:
    _write_session_log(tmp_path, _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / SESSION_LOG_RELPATH).read_text()
    # ISO 8601 timestamps contain "T" and "+"
    assert "Session Log" in content
    assert "T" in content  # timestamp contains ISO T separator


def test_write_session_log_contains_brick_status(tmp_path: Path) -> None:
    _write_session_log(tmp_path, _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / SESSION_LOG_RELPATH).read_text()
    assert "Brick 12 - bricklayer close-session" in content


def test_write_session_log_contains_groq_output(tmp_path: Path) -> None:
    _write_session_log(tmp_path, _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / SESSION_LOG_RELPATH).read_text()
    assert _GROQ_RESPONSE in content


def test_write_session_log_contains_completed_bricks(tmp_path: Path) -> None:
    _write_session_log(tmp_path, _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / SESSION_LOG_RELPATH).read_text()
    assert "Brick 11 - bricklayer commit" in content


# ---------------------------------------------------------------------------
# _write_state_md
# ---------------------------------------------------------------------------


def test_write_state_md_creates_file(tmp_path: Path) -> None:
    assert _write_state_md(tmp_path, _SAMPLE_STATE)
    assert (tmp_path / STATE_MD_RELPATH).exists()


def test_write_state_md_contains_project(tmp_path: Path) -> None:
    _write_state_md(tmp_path, _SAMPLE_STATE)
    content = (tmp_path / STATE_MD_RELPATH).read_text()
    assert f"Project: {tmp_path.name}" in content


def test_write_state_md_contains_current_brick(tmp_path: Path) -> None:
    _write_state_md(tmp_path, _SAMPLE_STATE)
    content = (tmp_path / STATE_MD_RELPATH).read_text()
    assert "Brick 12 - bricklayer close-session" in content


def test_write_state_md_contains_last_action(tmp_path: Path) -> None:
    _write_state_md(tmp_path, _SAMPLE_STATE)
    content = (tmp_path / STATE_MD_RELPATH).read_text()
    assert "skeptic_packet_ready" in content


def test_write_state_md_contains_next_command(tmp_path: Path) -> None:
    _write_state_md(tmp_path, _SAMPLE_STATE)
    content = (tmp_path / STATE_MD_RELPATH).read_text()
    assert "Next command:" in content
    assert "bricklayer build --verdict PASS|FAIL" in content


def test_write_state_md_all_four_fields_present(tmp_path: Path) -> None:
    _write_state_md(tmp_path, _SAMPLE_STATE)
    content = (tmp_path / STATE_MD_RELPATH).read_text()
    assert "Project:" in content
    assert "Current brick:" in content
    assert "Last action:" in content
    assert "Next command:" in content


# ---------------------------------------------------------------------------
# run_close_session — happy path
# ---------------------------------------------------------------------------


def test_run_close_session_returns_zero(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 0


def test_run_close_session_writes_session_log(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert (tmp_path / SESSION_LOG_RELPATH).exists()


def test_run_close_session_writes_state_md(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert (tmp_path / STATE_MD_RELPATH).exists()


def test_run_close_session_prints_next_session(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    out = capsys.readouterr().out
    assert "Session closed" in out
    assert "bricklayer resume" in out


# ---------------------------------------------------------------------------
# run_close_session — missing GROQ_API_KEY
# ---------------------------------------------------------------------------


def test_run_close_session_missing_api_key_returns_one(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    env = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
    with patch.dict(os.environ, env, clear=True):
        result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 1


def test_run_close_session_missing_api_key_error_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _full_setup(tmp_path)
    env = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
    with patch.dict(os.environ, env, clear=True):
        run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert "GROQ_API_KEY" in capsys.readouterr().err


def test_run_close_session_missing_api_key_no_files_written(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    env = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
    with patch.dict(os.environ, env, clear=True):
        run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert not (tmp_path / SESSION_LOG_RELPATH).exists()
    assert not (tmp_path / STATE_MD_RELPATH).exists()


def test_run_close_session_missing_api_key_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _full_setup(tmp_path)
    env = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
    with patch.dict(os.environ, env, clear=True):
        run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_close_session — missing state.json
# ---------------------------------------------------------------------------


def test_run_close_session_missing_state_returns_one(tmp_path: Path) -> None:
    _write_yaml(tmp_path)
    _write_sprint_brain(tmp_path)
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
        result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 1


def test_run_close_session_missing_state_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_yaml(tmp_path)
    _write_sprint_brain(tmp_path)
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
        run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_close_session — Groq call fails
# ---------------------------------------------------------------------------


def test_run_close_session_groq_fails_returns_one(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("HTTP 503")
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 1


def test_run_close_session_groq_fails_no_session_log(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("HTTP 503")
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert not (tmp_path / SESSION_LOG_RELPATH).exists()


def test_run_close_session_groq_fails_no_state_md(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("HTTP 503")
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert not (tmp_path / STATE_MD_RELPATH).exists()


def test_run_close_session_groq_fails_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _full_setup(tmp_path)
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = Exception("connection error")
        with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
            run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_close_session — missing sprint-brain.md path
# ---------------------------------------------------------------------------


def test_run_close_session_missing_sprint_brain_returns_one(tmp_path: Path) -> None:
    _write_state(tmp_path)
    _write_yaml(tmp_path, review_path="system-prompts/sprint-brain.md")
    # Do NOT write sprint-brain.md
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
        result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 1


def test_run_close_session_missing_sprint_brain_names_path(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    _write_yaml(tmp_path, review_path="system-prompts/sprint-brain.md")
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
        run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    err = capsys.readouterr().err
    assert "sprint-brain.md" in err


def test_run_close_session_missing_review_key_names_key(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _write_state(tmp_path)
    _write_yaml(tmp_path, review_path=None)
    with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
        run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    err = capsys.readouterr().err
    assert "phases.review" in err


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_setup(tmp_path: Path) -> None:
    _full_setup(tmp_path)


def test_cli_close_session_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            client.chat.completions.create.return_value = _mock_groq_success()
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                result = cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_close_session_writes_session_log(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            client.chat.completions.create.return_value = _mock_groq_success()
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    assert (tmp_path / SESSION_LOG_RELPATH).exists()


def test_cli_close_session_writes_state_md(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            client.chat.completions.create.return_value = _mock_groq_success()
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    assert (tmp_path / STATE_MD_RELPATH).exists()


def test_cli_close_session_state_md_content(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            client.chat.completions.create.return_value = _mock_groq_success()
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    content = (tmp_path / STATE_MD_RELPATH).read_text()
    assert "Project:" in content
    assert "Current brick:" in content
    assert "Last action:" in content
    assert "Next command:" in content
    assert "Brick 12 - bricklayer close-session" in content


def test_cli_close_session_output_contains_resume(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            client.chat.completions.create.return_value = _mock_groq_success()
            with patch.dict(os.environ, {"GROQ_API_KEY": "fake-key"}):
                result = cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    assert "bricklayer resume" in result.output


def test_cli_close_session_missing_key_exits_one(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        env = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
        with patch.dict(os.environ, env, clear=True):
            result = cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# GROQ_HEAVY_MODEL constant
# ---------------------------------------------------------------------------


def test_groq_heavy_model_constant_value() -> None:
    assert GROQ_HEAVY_MODEL == "llama-3.3-70b-versatile"


# ---------------------------------------------------------------------------
# _sanitize_pipe
# ---------------------------------------------------------------------------


def test_sanitize_pipe_replaces_pipe_with_dash() -> None:
    assert _sanitize_pipe("foo|bar") == "foo-bar"


def test_sanitize_pipe_multiple_pipes() -> None:
    assert _sanitize_pipe("a|b|c") == "a-b-c"


def test_sanitize_pipe_no_pipe_unchanged() -> None:
    assert _sanitize_pipe("no pipes here") == "no pipes here"


def test_sanitize_pipe_empty_string() -> None:
    assert _sanitize_pipe("") == ""


def test_sanitize_pipe_only_pipe() -> None:
    assert _sanitize_pipe("|") == "-"


# ---------------------------------------------------------------------------
# _extract_structured_data
# ---------------------------------------------------------------------------

_EXTRACTED: dict = {
    "component": "bricklayer close-session",
    "decision": "sprint review passed, all bricks green",
    "status": "DONE",
    "next_action": "bricklayer resume",
}

_EXTRACTED_JSON = (
    '{"component": "bricklayer close-session", '
    '"decision": "sprint review passed, all bricks green", '
    '"status": "DONE", '
    '"next_action": "bricklayer resume"}'
)


def test_extract_structured_data_returns_dict() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        mock = MagicMock()
        mock.choices[0].message.content = _EXTRACTED_JSON
        client.chat.completions.create.return_value = mock
        result = _extract_structured_data("fake-key", _GROQ_RESPONSE, _SAMPLE_STATE)
    assert result["component"] == "bricklayer close-session"
    assert result["decision"] == "sprint review passed, all bricks green"
    assert result["status"] == "DONE"
    assert result["next_action"] == "bricklayer resume"


def test_extract_structured_data_uses_heavy_model() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        mock = MagicMock()
        mock.choices[0].message.content = _EXTRACTED_JSON
        client.chat.completions.create.return_value = mock
        _extract_structured_data("fake-key", _GROQ_RESPONSE, _SAMPLE_STATE)
        call_kwargs = client.chat.completions.create.call_args
        assert call_kwargs.kwargs.get("model") == GROQ_HEAVY_MODEL


def test_extract_structured_data_strips_markdown_fence() -> None:
    fenced = f"```json\n{_EXTRACTED_JSON}\n```"
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        mock = MagicMock()
        mock.choices[0].message.content = fenced
        client.chat.completions.create.return_value = mock
        result = _extract_structured_data("fake-key", _GROQ_RESPONSE, _SAMPLE_STATE)
    assert result["status"] == "DONE"


def test_extract_structured_data_fallback_on_invalid_json() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        mock = MagicMock()
        mock.choices[0].message.content = "not valid json at all"
        client.chat.completions.create.return_value = mock
        result = _extract_structured_data("fake-key", _GROQ_RESPONSE, _SAMPLE_STATE)
    # Fallback uses state values
    assert "component" in result
    assert "decision" in result
    assert "status" in result
    assert "next_action" in result


def test_extract_structured_data_fallback_on_groq_failure() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("timeout")
        result = _extract_structured_data("fake-key", _GROQ_RESPONSE, _SAMPLE_STATE)
    assert result["component"] == "bricklayer close-session"
    assert result["status"] == "IN_PROGRESS"


def test_extract_structured_data_fallback_component_strips_brick_prefix() -> None:
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("fail")
        result = _extract_structured_data("fake-key", _GROQ_RESPONSE, _SAMPLE_STATE)
    # "Brick 12 - bricklayer close-session" → "bricklayer close-session"
    assert result["component"] == "bricklayer close-session"


def test_extract_structured_data_fallback_no_brick_prefix() -> None:
    state = {**_SAMPLE_STATE, "current_brick": "unknown"}
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("fail")
        result = _extract_structured_data("fake-key", _GROQ_RESPONSE, state)
    assert result["component"] == "unknown"


# ---------------------------------------------------------------------------
# _build_decision_log_row
# ---------------------------------------------------------------------------


def test_build_decision_log_row_contains_date() -> None:
    row = _build_decision_log_row(_EXTRACTED)
    today = datetime.date.today().isoformat()
    assert today in row


def test_build_decision_log_row_contains_component() -> None:
    row = _build_decision_log_row(_EXTRACTED)
    assert "bricklayer close-session" in row


def test_build_decision_log_row_contains_status() -> None:
    row = _build_decision_log_row(_EXTRACTED)
    assert "DONE" in row


def test_build_decision_log_row_contains_next_action() -> None:
    row = _build_decision_log_row(_EXTRACTED)
    assert "bricklayer resume" in row


def test_build_decision_log_row_pipe_format() -> None:
    row = _build_decision_log_row(_EXTRACTED)
    assert row.count("|") >= 5
    assert row.startswith("|")
    assert row.endswith("|")


def test_build_decision_log_row_decision_truncated_to_80() -> None:
    extracted = {**_EXTRACTED, "decision": "x" * 100}
    row = _build_decision_log_row(extracted)
    cells = [c.strip() for c in row.split("|")]
    decision_cell = cells[3]  # date | component | decision | status | next
    assert len(decision_cell) <= 80


def test_build_decision_log_row_sanitizes_pipe_in_component() -> None:
    extracted = {**_EXTRACTED, "component": "foo|bar"}
    row = _build_decision_log_row(extracted)
    # The pipe in "foo|bar" must become a dash — no raw pipe inside the cell.
    cells = [c.strip() for c in row.split("|")]
    assert "foo-bar" in cells[2]


def test_build_decision_log_row_sanitizes_pipe_in_decision() -> None:
    extracted = {**_EXTRACTED, "decision": "passed|failed"}
    row = _build_decision_log_row(extracted)
    cells = [c.strip() for c in row.split("|")]
    assert "passed-failed" in cells[3]


def test_build_decision_log_row_sanitizes_pipe_in_status() -> None:
    extracted = {**_EXTRACTED, "status": "IN|PROGRESS"}
    row = _build_decision_log_row(extracted)
    cells = [c.strip() for c in row.split("|")]
    assert "IN-PROGRESS" in cells[4]


def test_build_decision_log_row_sanitizes_pipe_in_next_action() -> None:
    extracted = {**_EXTRACTED, "next_action": "do|this"}
    row = _build_decision_log_row(extracted)
    cells = [c.strip() for c in row.split("|")]
    assert "do-this" in cells[5]


# ---------------------------------------------------------------------------
# _append_decision_log
# ---------------------------------------------------------------------------


def test_append_decision_log_creates_file_if_missing(tmp_path: Path) -> None:
    row = "| 2026-03-25 | test | decision | DONE | next |"
    _append_decision_log(tmp_path, row)
    assert (tmp_path / "decision-log.md").exists()


def test_append_decision_log_creates_header_if_missing(tmp_path: Path) -> None:
    row = "| 2026-03-25 | test | decision | DONE | next |"
    _append_decision_log(tmp_path, row)
    content = (tmp_path / "decision-log.md").read_text()
    assert "| Date | Component | Decision Made | Status | Next Action |" in content


def test_append_decision_log_appends_row(tmp_path: Path) -> None:
    row = "| 2026-03-25 | test | decision | DONE | next |"
    _append_decision_log(tmp_path, row)
    content = (tmp_path / "decision-log.md").read_text()
    assert row in content


def test_append_decision_log_appends_to_existing_file(tmp_path: Path) -> None:
    existing = "# Decision Log\n| Date | Component | Decision Made | Status | Next Action |\n"
    (tmp_path / "decision-log.md").write_text(existing, encoding="utf-8")
    row = "| 2026-03-25 | new | new decision | DONE | next |"
    _append_decision_log(tmp_path, row)
    content = (tmp_path / "decision-log.md").read_text()
    assert existing.strip() in content
    assert row in content


def test_append_decision_log_multiple_rows(tmp_path: Path) -> None:
    row1 = "| 2026-03-25 | comp1 | dec1 | DONE | n1 |"
    row2 = "| 2026-03-26 | comp2 | dec2 | DONE | n2 |"
    _append_decision_log(tmp_path, row1)
    _append_decision_log(tmp_path, row2)
    content = (tmp_path / "decision-log.md").read_text()
    assert row1 in content
    assert row2 in content


# ---------------------------------------------------------------------------
# _build_pipeline_status
# ---------------------------------------------------------------------------


def test_build_pipeline_status_contains_current_brick() -> None:
    content = _build_pipeline_status(_SAMPLE_STATE, _GROQ_RESPONSE)
    assert "Brick 12 - bricklayer close-session" in content


def test_build_pipeline_status_contains_status() -> None:
    content = _build_pipeline_status(_SAMPLE_STATE, _GROQ_RESPONSE)
    assert "IN_PROGRESS" in content


def test_build_pipeline_status_contains_next_action() -> None:
    content = _build_pipeline_status(_SAMPLE_STATE, _GROQ_RESPONSE)
    assert "skeptic_packet_ready" in content


def test_build_pipeline_status_contains_groq_output() -> None:
    content = _build_pipeline_status(_SAMPLE_STATE, _GROQ_RESPONSE)
    assert _GROQ_RESPONSE in content


def test_build_pipeline_status_contains_date() -> None:
    content = _build_pipeline_status(_SAMPLE_STATE, _GROQ_RESPONSE)
    today = datetime.date.today().isoformat()
    assert today in content


def test_build_pipeline_status_contains_completed_bricks() -> None:
    content = _build_pipeline_status(_SAMPLE_STATE, _GROQ_RESPONSE)
    assert "Brick 11 - bricklayer commit" in content


# ---------------------------------------------------------------------------
# _sync_docs
# ---------------------------------------------------------------------------

# Helper: patch _extract_structured_data to return a known value so _sync_docs
# tests don't depend on Groq network calls for extraction.
_PATCH_EXTRACT = "cli.commands.close_session._extract_structured_data"


def test_sync_docs_docs_path_not_set_prints_skip(capsys: pytest.CaptureFixture) -> None:
    env = {k: v for k, v in os.environ.items() if k != "DOCS_PATH"}
    with patch.dict(os.environ, env, clear=True):
        _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    out = capsys.readouterr().out
    assert "DOCS_PATH not set" in out
    assert "skipping docs sync" in out


def test_sync_docs_docs_path_not_set_exits_cleanly(capsys: pytest.CaptureFixture) -> None:
    """_sync_docs returns None (no exception) when DOCS_PATH is not set."""
    env = {k: v for k, v in os.environ.items() if k != "DOCS_PATH"}
    with patch.dict(os.environ, env, clear=True):
        result = _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    assert result is None


def test_sync_docs_docs_path_missing_dir_prints_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    missing = str(tmp_path / "nonexistent")
    with patch.dict(os.environ, {"DOCS_PATH": missing}):
        _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    out = capsys.readouterr().out
    assert "warning" in out.lower() or "does not exist" in out


def test_sync_docs_docs_path_missing_dir_no_files_written(tmp_path: Path) -> None:
    missing = str(tmp_path / "nonexistent")
    with patch.dict(os.environ, {"DOCS_PATH": missing}):
        _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    assert not (tmp_path / "nonexistent" / "decision-log.md").exists()


def test_sync_docs_happy_path_writes_decision_log(tmp_path: Path) -> None:
    with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    assert (tmp_path / "decision-log.md").exists()


def test_sync_docs_happy_path_writes_pipeline_status(tmp_path: Path) -> None:
    with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    assert (tmp_path / "pipeline-status.md").exists()


def test_sync_docs_happy_path_decision_log_has_row(tmp_path: Path) -> None:
    with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / "decision-log.md").read_text()
    today = datetime.date.today().isoformat()
    assert today in content


def test_sync_docs_happy_path_pipeline_status_has_brick(tmp_path: Path) -> None:
    with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / "pipeline-status.md").read_text()
    assert "Brick 12 - bricklayer close-session" in content


def test_sync_docs_happy_path_prints_synced(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    out = capsys.readouterr().out
    assert "Docs synced to" in out


def test_sync_docs_creates_decision_log_header_if_missing(tmp_path: Path) -> None:
    with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / "decision-log.md").read_text()
    assert "| Date | Component | Decision Made | Status | Next Action |" in content


def test_sync_docs_calls_extract_with_api_key(tmp_path: Path) -> None:
    with patch(_PATCH_EXTRACT, return_value=_EXTRACTED) as mock_extract:
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("my-api-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    mock_extract.assert_called_once()
    call_args = mock_extract.call_args
    assert call_args.args[0] == "my-api-key"


def test_sync_docs_uses_extracted_component_in_row(tmp_path: Path) -> None:
    extracted = {**_EXTRACTED, "component": "custom component"}
    with patch(_PATCH_EXTRACT, return_value=extracted):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / "decision-log.md").read_text()
    assert "custom component" in content


def test_sync_docs_pipe_in_extracted_field_sanitized(tmp_path: Path) -> None:
    extracted = {**_EXTRACTED, "decision": "foo|bar"}
    with patch(_PATCH_EXTRACT, return_value=extracted):
        with patch.dict(os.environ, {"DOCS_PATH": str(tmp_path)}):
            _sync_docs("fake-key", _SAMPLE_STATE, _GROQ_RESPONSE)
    content = (tmp_path / "decision-log.md").read_text()
    assert "foo-bar" in content
    # Raw pipe from LLM must not appear inside a table row
    rows = [l for l in content.splitlines() if l.startswith("|") and "foo" in l]
    assert rows, "expected a row containing sanitized value"


# ---------------------------------------------------------------------------
# run_close_session — docs sync integration
# ---------------------------------------------------------------------------


def test_run_close_session_with_docs_path_writes_decision_log(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
            with patch.dict(
                os.environ,
                {"GROQ_API_KEY": "fake-key", "DOCS_PATH": str(docs_dir)},
            ):
                result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 0
    assert (docs_dir / "decision-log.md").exists()


def test_run_close_session_with_docs_path_writes_pipeline_status(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
            with patch.dict(
                os.environ,
                {"GROQ_API_KEY": "fake-key", "DOCS_PATH": str(docs_dir)},
            ):
                run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert (docs_dir / "pipeline-status.md").exists()


def test_run_close_session_no_docs_path_exits_zero(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    env = {k: v for k, v in os.environ.items() if k not in ("GROQ_API_KEY", "DOCS_PATH")}
    env["GROQ_API_KEY"] = "fake-key"
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch.dict(os.environ, env, clear=True):
            result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 0


def test_run_close_session_no_docs_path_prints_skip(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    _full_setup(tmp_path)
    env = {k: v for k, v in os.environ.items() if k not in ("GROQ_API_KEY", "DOCS_PATH")}
    env["GROQ_API_KEY"] = "fake-key"
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch.dict(os.environ, env, clear=True):
            run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    out = capsys.readouterr().out
    assert "DOCS_PATH not set" in out


def test_run_close_session_docs_path_missing_dir_exits_zero(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    missing = str(tmp_path / "nonexistent_docs")
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.return_value = _mock_groq_success()
        with patch.dict(
            os.environ,
            {"GROQ_API_KEY": "fake-key", "DOCS_PATH": missing},
        ):
            result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 0


def test_run_close_session_groq_fails_no_docs_written(tmp_path: Path) -> None:
    _full_setup(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    with patch("cli.commands.close_session.Groq") as MockGroq:
        client = MockGroq.return_value
        client.chat.completions.create.side_effect = RuntimeError("HTTP 503")
        with patch.dict(
            os.environ,
            {"GROQ_API_KEY": "fake-key", "DOCS_PATH": str(docs_dir)},
        ):
            result = run_close_session(tmp_path, tmp_path / "bricklayer.yaml")
    assert result == 1
    assert not (docs_dir / "decision-log.md").exists()
    assert not (docs_dir / "pipeline-status.md").exists()


# ---------------------------------------------------------------------------
# CliRunner integration — docs sync
# ---------------------------------------------------------------------------


def test_cli_close_session_with_docs_path(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            client.chat.completions.create.return_value = _mock_groq_success()
            with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
                with patch.dict(
                    os.environ,
                    {"GROQ_API_KEY": "fake-key", "DOCS_PATH": str(docs_dir)},
                ):
                    result = cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0
    assert (docs_dir / "decision-log.md").exists()
    assert (docs_dir / "pipeline-status.md").exists()


def test_cli_close_session_docs_synced_message(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            client.chat.completions.create.return_value = _mock_groq_success()
            with patch(_PATCH_EXTRACT, return_value=_EXTRACTED):
                with patch.dict(
                    os.environ,
                    {"GROQ_API_KEY": "fake-key", "DOCS_PATH": str(docs_dir)},
                ):
                    result = cli_runner.invoke(app, ["close-session"])
    finally:
        os.chdir(old_cwd)
    assert "Docs synced to" in result.output
