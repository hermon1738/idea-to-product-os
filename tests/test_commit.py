"""Tests for Brick 11 — bricklayer commit command."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.commit import (  # noqa: E402
    _build_message,
    _check_staged,
    _parse_brick,
    run_commit,
)
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_STATE: dict = {
    "current_brick": "Brick 11 - bricklayer commit",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": [],
    "next_action": "verify",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}


def _make_project(tmp_path: Path, state: dict | None = None) -> Path:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    s = state if state is not None else _BASE_STATE
    (brick_dir / "state.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
    return tmp_path


def _mock_staged(files: list[str]):
    """Return a side_effect for subprocess.run that reports staged files."""
    def _side(cmd, **kwargs):
        m = MagicMock()
        if cmd[:4] == ["git", "diff", "--cached", "--name-only"]:
            m.returncode = 0
            m.stdout = "\n".join(files) + ("\n" if files else "")
        elif cmd[:2] == ["git", "commit"]:
            m.returncode = 0
            m.stdout = "[brick/11 abc1234] feat(brick-11): test\n 1 file changed"
        else:
            m.returncode = 0
            m.stdout = ""
        return m
    return _side


def _mock_nothing_staged():
    def _side(cmd, **kwargs):
        m = MagicMock()
        if cmd[:4] == ["git", "diff", "--cached", "--name-only"]:
            m.returncode = 0
            m.stdout = ""
        else:
            m.returncode = 0
            m.stdout = ""
        return m
    return _side


# ---------------------------------------------------------------------------
# _parse_brick
# ---------------------------------------------------------------------------


def test_parse_brick_extracts_number_and_name() -> None:
    assert _parse_brick("Brick 11 - bricklayer commit") == ("11", "bricklayer commit")


def test_parse_brick_decimal() -> None:
    num, name = _parse_brick("Brick 8.5 - git fixes")
    assert num == "8.5"
    assert name == "git fixes"


def test_parse_brick_unknown_format() -> None:
    num, name = _parse_brick("no match")
    assert num == "?"


# ---------------------------------------------------------------------------
# _build_message
# ---------------------------------------------------------------------------


def test_build_message_subject_format() -> None:
    msg = _build_message("11", "bricklayer commit", "add deep merge fix")
    first_line = msg.splitlines()[0]
    assert first_line == "feat(brick-11): add deep merge fix"


def test_build_message_body_contains_brick_line() -> None:
    msg = _build_message("11", "bricklayer commit", "add deep merge fix")
    assert "Brick: 11" in msg
    assert "bricklayer commit" in msg


def test_build_message_trailer_present() -> None:
    msg = _build_message("11", "bricklayer commit", "add deep merge fix")
    assert "Co-Authored-By: Claude Sonnet 4.6" in msg


def test_build_message_blank_line_after_subject() -> None:
    lines = _build_message("11", "bricklayer commit", "test").splitlines()
    assert lines[1] == ""


# ---------------------------------------------------------------------------
# _check_staged
# ---------------------------------------------------------------------------


def test_check_staged_returns_files(tmp_path: Path) -> None:
    with patch("cli.commands.commit._subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="file.py\nother.py\n")
        result = _check_staged(tmp_path)
    assert result == ["file.py", "other.py"]


def test_check_staged_returns_empty_when_nothing(tmp_path: Path) -> None:
    with patch("cli.commands.commit._subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        result = _check_staged(tmp_path)
    assert result == []


def test_check_staged_returns_empty_on_file_not_found(tmp_path: Path) -> None:
    with patch("cli.commands.commit._subprocess.run", side_effect=FileNotFoundError):
        result = _check_staged(tmp_path)
    assert result == []


# ---------------------------------------------------------------------------
# run_commit — happy path
# ---------------------------------------------------------------------------


def test_run_commit_returns_zero(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.commit._subprocess.run", side_effect=_mock_staged(["file.py"])):
        result = run_commit(root, "add deep merge fix")
    assert result == 0


def test_run_commit_calls_git_commit(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    commit_calls = []

    def recorder(cmd, **kwargs):
        if cmd[:2] == ["git", "commit"]:
            commit_calls.append(cmd)
        m = MagicMock()
        m.returncode = 0
        m.stdout = "file.py\n" if cmd[:4] == ["git", "diff", "--cached", "--name-only"] else "[abc] msg\n"
        return m

    with patch("cli.commands.commit._subprocess.run", side_effect=recorder):
        run_commit(root, "add deep merge fix")

    assert len(commit_calls) == 1


def test_run_commit_message_has_correct_subject(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    captured_msg = []

    def recorder(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        if cmd[:4] == ["git", "diff", "--cached", "--name-only"]:
            m.stdout = "file.py\n"
        elif cmd[:2] == ["git", "commit"]:
            captured_msg.append(cmd[cmd.index("-m") + 1])
            m.stdout = "[abc] feat(brick-11): add deep merge fix\n"
        else:
            m.stdout = ""
        return m

    with patch("cli.commands.commit._subprocess.run", side_effect=recorder):
        run_commit(root, "add deep merge fix")

    assert captured_msg
    assert captured_msg[0].startswith("feat(brick-11): add deep merge fix")


def test_run_commit_message_has_brick_body(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    captured_msg = []

    def recorder(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        if cmd[:4] == ["git", "diff", "--cached", "--name-only"]:
            m.stdout = "file.py\n"
        elif cmd[:2] == ["git", "commit"]:
            captured_msg.append(cmd[cmd.index("-m") + 1])
            m.stdout = "[abc] msg\n"
        else:
            m.stdout = ""
        return m

    with patch("cli.commands.commit._subprocess.run", side_effect=recorder):
        run_commit(root, "add deep merge fix")

    assert captured_msg
    assert "Brick: 11" in captured_msg[0]
    assert "bricklayer commit" in captured_msg[0]


def test_run_commit_message_has_coauthor_trailer(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    captured_msg = []

    def recorder(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        if cmd[:4] == ["git", "diff", "--cached", "--name-only"]:
            m.stdout = "file.py\n"
        elif cmd[:2] == ["git", "commit"]:
            captured_msg.append(cmd[cmd.index("-m") + 1])
            m.stdout = "[abc] msg\n"
        else:
            m.stdout = ""
        return m

    with patch("cli.commands.commit._subprocess.run", side_effect=recorder):
        run_commit(root, "add deep merge fix")

    assert "Co-Authored-By: Claude Sonnet 4.6" in captured_msg[0]


def test_run_commit_prints_output(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.commit._subprocess.run", side_effect=_mock_staged(["file.py"])):
        run_commit(root, "add deep merge fix")
    assert capsys.readouterr().out.strip() != ""


# ---------------------------------------------------------------------------
# run_commit — nothing staged
# ---------------------------------------------------------------------------


def test_run_commit_nothing_staged_exits_one(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.commit._subprocess.run", side_effect=_mock_nothing_staged()):
        result = run_commit(root, "test message")
    assert result == 1


def test_run_commit_nothing_staged_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.commit._subprocess.run", side_effect=_mock_nothing_staged()):
        run_commit(root, "test message")
    assert "Nothing staged" in capsys.readouterr().err


def test_run_commit_nothing_staged_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    root = _make_project(tmp_path)
    with patch("cli.commands.commit._subprocess.run", side_effect=_mock_nothing_staged()):
        run_commit(root, "test message")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_commit — empty message
# ---------------------------------------------------------------------------


def test_run_commit_empty_message_exits_one(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    result = run_commit(root, "")
    assert result == 1


def test_run_commit_empty_message_whitespace_exits_one(tmp_path: Path) -> None:
    root = _make_project(tmp_path)
    result = run_commit(root, "   ")
    assert result == 1


def test_run_commit_empty_message_error_text(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    root = _make_project(tmp_path)
    run_commit(root, "")
    assert "Commit message cannot be empty" in capsys.readouterr().err


# ---------------------------------------------------------------------------
# run_commit — missing state.json
# ---------------------------------------------------------------------------


def test_run_commit_missing_state_exits_one(tmp_path: Path) -> None:
    result = run_commit(tmp_path, "test message")
    assert result == 1


def test_run_commit_missing_state_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    run_commit(tmp_path, "test message")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# run_commit — git commit fails
# ---------------------------------------------------------------------------


def test_run_commit_git_failure_exits_one(tmp_path: Path) -> None:
    root = _make_project(tmp_path)

    def side_effect(cmd, **kwargs):
        m = MagicMock()
        if cmd[:4] == ["git", "diff", "--cached", "--name-only"]:
            m.returncode = 0
            m.stdout = "file.py\n"
        else:
            m.returncode = 1
            m.stdout = "error: something went wrong"
        return m

    with patch("cli.commands.commit._subprocess.run", side_effect=side_effect):
        result = run_commit(root, "test")
    assert result == 1


def test_run_commit_git_failure_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    root = _make_project(tmp_path)

    def side_effect(cmd, **kwargs):
        m = MagicMock()
        if cmd[:4] == ["git", "diff", "--cached", "--name-only"]:
            m.returncode = 0
            m.stdout = "file.py\n"
        else:
            m.returncode = 1
            m.stdout = "error: something went wrong"
        return m

    with patch("cli.commands.commit._subprocess.run", side_effect=side_effect):
        run_commit(root, "test")
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# CliRunner — no -m flag
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_setup(tmp_path: Path) -> None:
    _make_project(tmp_path)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools: {}\nagents: {}\n", encoding="utf-8"
    )


def test_cli_commit_no_m_exits_one(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["commit"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_commit_no_m_prints_usage(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["commit"])
    finally:
        os.chdir(old_cwd)
    assert "bricklayer commit -m" in result.output
    assert "Traceback" not in result.output


def test_cli_commit_no_m_no_traceback(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["commit"])
    finally:
        os.chdir(old_cwd)
    assert "Traceback" not in result.output


# ---------------------------------------------------------------------------
# CliRunner — happy path with mocked git
# ---------------------------------------------------------------------------


def test_cli_commit_with_message_exits_zero(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.commit._subprocess.run",
                   side_effect=_mock_staged(["file.py"])):
            result = cli_runner.invoke(app, ["commit", "-m", "add deep merge fix"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_commit_output_contains_commit_info(tmp_path: Path) -> None:
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.commit._subprocess.run",
                   side_effect=_mock_staged(["file.py"])):
            result = cli_runner.invoke(app, ["commit", "-m", "add deep merge fix"])
    finally:
        os.chdir(old_cwd)
    # git output (mocked as "[brick/11 abc1234] feat...") should be echoed
    assert result.exit_code == 0
    assert result.output.strip() != ""


# ---------------------------------------------------------------------------
# CliRunner — integration with real git repo
# ---------------------------------------------------------------------------


def _make_real_git_repo(tmp_path: Path) -> Path:
    """Create a minimal real git repo for integration testing."""
    subprocess.run(["git", "init"], cwd=str(tmp_path), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.email", "test@test.com"],
                   cwd=str(tmp_path), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.name", "Test"],
                   cwd=str(tmp_path), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Initial commit so HEAD exists
    (tmp_path / "README.md").write_text("init\n")
    subprocess.run(["git", "add", "README.md"], cwd=str(tmp_path), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "init"], cwd=str(tmp_path), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmp_path


def test_cli_commit_real_git_creates_commit(tmp_path: Path) -> None:
    """Integration: real git repo — bricklayer commit creates a correctly tagged commit."""
    _make_real_git_repo(tmp_path)
    # Set up bricklayer project on top
    _cli_setup(tmp_path)
    # Stage a file
    (tmp_path / "staged.txt").write_text("some change\n")
    subprocess.run(["git", "add", "staged.txt"], cwd=str(tmp_path), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["commit", "-m", "add deep merge fix"])
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 0

    # Verify git log has the correctly formatted commit
    log = subprocess.run(
        ["git", "log", "--format=%B", "-1"],
        cwd=str(tmp_path),
        stdout=subprocess.PIPE, text=True, check=True,
    ).stdout
    assert "feat(brick-11): add deep merge fix" in log
    assert "Brick: 11" in log
    assert "bricklayer commit" in log
    assert "Co-Authored-By: Claude Sonnet 4.6" in log


def test_cli_commit_real_git_nothing_staged_exits_one(tmp_path: Path) -> None:
    """Integration: nothing staged → exit 1."""
    _make_real_git_repo(tmp_path)
    _cli_setup(tmp_path)

    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = cli_runner.invoke(app, ["commit", "-m", "should fail"])
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 1
    assert "Nothing staged" in result.output
