"""Tests for Brick 24 — bricklayer agent deploy and agent live commands."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, call, patch

import pytest
import yaml
from typer.testing import CliRunner

from cli.commands.agent import (
    _print_deploy_ready,
    _run_git,
    run_agent_deploy,
    run_agent_live,
)
from cli.main import app
from cli.registry import load as registry_load

# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

_RUNNER = CliRunner()

_AGENT_ID = "idea-os-monitor-01"
_PROJECT = "idea-to-product-os"
_ROLE = "monitor"

_REGISTRY_ENTRY: dict[str, Any] = {
    "id": _AGENT_ID,
    "name": "Monitor",
    "project": _PROJECT,
    "role": _ROLE,
    "runtime": "raw-python",
    "status": "stopped",
    "trigger": "!monitor in Discord",
    "location": f"context/agents/{_AGENT_ID}/",
    "discord_channel": _AGENT_ID,
    "container_name": _AGENT_ID,
}

# Patch target for the git helper — all git calls go through this.
_PATCH_GIT = "cli.commands.agent._run_git"


def _make_registry(tmp_path: Path, agents: list[dict] | None = None) -> None:
    """Write registry.yaml to tmp_path."""
    registry_dir = tmp_path / "context" / "agents"
    registry_dir.mkdir(parents=True, exist_ok=True)
    data = {"agents": agents if agents is not None else []}
    (registry_dir / "registry.yaml").write_text(
        yaml.dump(data, default_flow_style=False), encoding="utf-8"
    )


def _make_agent_dir(tmp_path: Path, agent_id: str = _AGENT_ID) -> Path:
    """Create a minimal agent scaffold dir under context/agents/<id>/."""
    agent_dir = tmp_path / "context" / "agents" / agent_id
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "agent.py").write_text(f'AGENT_ID = "{agent_id}"\n', encoding="utf-8")
    (agent_dir / "Dockerfile").write_text("FROM python:3.11-slim\n", encoding="utf-8")
    (agent_dir / "requirements.txt").write_text("discord.py==2.3.2\n", encoding="utf-8")
    (agent_dir / "agent.yaml").write_text(
        yaml.dump({"id": agent_id, "runtime": "raw-python"}, default_flow_style=False),
        encoding="utf-8",
    )
    return agent_dir


def _make_deploy_repo(tmp_path: Path) -> Path:
    """Create a bare directory to use as the deploy repo (not a real git repo)."""
    deploy_repo = tmp_path / "deploy-repo"
    deploy_repo.mkdir()
    (deploy_repo / "agents").mkdir()
    return deploy_repo


def _git_success(stdout: str = "", stderr: str = "") -> MagicMock:
    """Return a mock CompletedProcess indicating git success."""
    m = MagicMock(spec=subprocess.CompletedProcess)
    m.returncode = 0
    m.stdout = stdout
    m.stderr = stderr
    return m


def _git_failure(stderr: str = "fatal: error") -> MagicMock:
    """Return a mock CompletedProcess indicating git failure."""
    m = MagicMock(spec=subprocess.CompletedProcess)
    m.returncode = 128
    m.stdout = ""
    m.stderr = stderr
    return m


# ---------------------------------------------------------------------------
# _run_git() unit test
# ---------------------------------------------------------------------------


def test_run_git_returns_completed_process(tmp_path: Path) -> None:
    # Run a real git command (version) to verify _run_git works.
    result = _run_git(["--version"], tmp_path)
    assert result.returncode == 0
    assert "git" in result.stdout.lower()


# ---------------------------------------------------------------------------
# _print_deploy_ready() unit tests
# ---------------------------------------------------------------------------


def test_print_deploy_ready_contains_agent_id(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert _AGENT_ID in capsys.readouterr().out


def test_print_deploy_ready_contains_deploy_ready(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "DEPLOY READY" in capsys.readouterr().out


def test_print_deploy_ready_contains_docker_build(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "docker build" in capsys.readouterr().out


def test_print_deploy_ready_contains_docker_run(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "docker run" in capsys.readouterr().out


def test_print_deploy_ready_contains_env_file(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "--env-file" in capsys.readouterr().out


def test_print_deploy_ready_contains_restart_unless_stopped(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "--restart unless-stopped" in capsys.readouterr().out


def test_print_deploy_ready_contains_docker_logs(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "docker logs" in capsys.readouterr().out


def test_print_deploy_ready_contains_bricklayer_agent_live(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "bricklayer agent live" in capsys.readouterr().out


def test_print_deploy_ready_contains_git_pull(capsys, tmp_path: Path) -> None:
    _print_deploy_ready(_AGENT_ID, tmp_path)
    assert "git pull" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# run_agent_deploy() — happy path
# ---------------------------------------------------------------------------


def test_run_agent_deploy_returns_zero(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()):
        result = run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert result == 0


def test_run_agent_deploy_copies_files(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert (deploy_repo / "agents" / _AGENT_ID / "agent.py").exists()


def test_run_agent_deploy_copies_dockerfile(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert (deploy_repo / "agents" / _AGENT_ID / "Dockerfile").exists()


def test_run_agent_deploy_registry_updated_to_deployed(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    agents = registry_load(tmp_path)
    agent = next(a for a in agents if a["id"] == _AGENT_ID)
    assert agent["status"] == "deployed"


def test_run_agent_deploy_calls_git_add(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()) as mock_git:
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    called_args = [c.args[0] for c in mock_git.call_args_list]
    assert any("add" in args for args in called_args)


def test_run_agent_deploy_calls_git_commit(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()) as mock_git:
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    called_args = [c.args[0] for c in mock_git.call_args_list]
    assert any("commit" in args for args in called_args)


def test_run_agent_deploy_calls_git_push(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()) as mock_git:
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    called_args = [c.args[0] for c in mock_git.call_args_list]
    assert any("push" in args for args in called_args)


def test_run_agent_deploy_prints_deploy_ready(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert "DEPLOY READY" in capsys.readouterr().out


def test_run_agent_deploy_prints_docker_commands(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_success()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    out = capsys.readouterr().out
    assert "docker build" in out
    assert "--env-file" in out
    assert "--restart unless-stopped" in out


# ---------------------------------------------------------------------------
# run_agent_deploy() — error cases
# ---------------------------------------------------------------------------


def test_run_agent_deploy_agent_not_in_registry_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    _make_deploy_repo(tmp_path)
    assert run_agent_deploy(tmp_path, _AGENT_ID, tmp_path / "deploy-repo") == 1


def test_run_agent_deploy_agent_not_in_registry_error_message(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    _make_deploy_repo(tmp_path)
    run_agent_deploy(tmp_path, _AGENT_ID, tmp_path / "deploy-repo")
    assert "not found" in capsys.readouterr().err


def test_run_agent_deploy_agent_not_in_registry_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_deploy(tmp_path, _AGENT_ID, tmp_path / "deploy-repo")
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_deploy_agent_dir_missing_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    deploy_repo = _make_deploy_repo(tmp_path)
    # No agent directory created.
    with patch(_PATCH_GIT, return_value=_git_success()):
        assert run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo) == 1


def test_run_agent_deploy_agent_dir_missing_error_has_path(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    deploy_repo = _make_deploy_repo(tmp_path)
    with patch(_PATCH_GIT, return_value=_git_success()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)
    assert _AGENT_ID in capsys.readouterr().err


def test_run_agent_deploy_deploy_repo_not_dir_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    nonexistent = tmp_path / "does-not-exist"
    assert run_agent_deploy(tmp_path, _AGENT_ID, nonexistent) == 1


def test_run_agent_deploy_deploy_repo_not_dir_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    run_agent_deploy(tmp_path, _AGENT_ID, tmp_path / "does-not-exist")
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_deploy_not_git_repo_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_failure("not a git repo")):
        assert run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo) == 1


def test_run_agent_deploy_not_git_repo_error_message(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_failure()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert "not a git repository" in capsys.readouterr().err


def test_run_agent_deploy_not_git_repo_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    with patch(_PATCH_GIT, return_value=_git_failure()):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_deploy_push_fails_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def git_side_effect(args: list[str], cwd: Path) -> MagicMock:
        if args[0] == "push":
            return _git_failure("error: failed to push some refs")
        return _git_success()

    with patch(_PATCH_GIT, side_effect=git_side_effect):
        result = run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert result == 1


def test_run_agent_deploy_push_fails_registry_not_updated(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def git_side_effect(args: list[str], cwd: Path) -> MagicMock:
        if args[0] == "push":
            return _git_failure("error: failed to push")
        return _git_success()

    with patch(_PATCH_GIT, side_effect=git_side_effect):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    agents = registry_load(tmp_path)
    agent = next(a for a in agents if a["id"] == _AGENT_ID)
    # Status must remain "stopped" — push failed, registry must not be updated.
    assert agent["status"] == "stopped"


def test_run_agent_deploy_push_fails_prints_git_error(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def git_side_effect(args: list[str], cwd: Path) -> MagicMock:
        if args[0] == "push":
            return _git_failure("error: permission denied")
        return _git_success()

    with patch(_PATCH_GIT, side_effect=git_side_effect):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert "error" in capsys.readouterr().err.lower()


def test_run_agent_deploy_push_fails_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def git_side_effect(args: list[str], cwd: Path) -> MagicMock:
        if args[0] == "push":
            return _git_failure()
        return _git_success()

    with patch(_PATCH_GIT, side_effect=git_side_effect):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_deploy_git_timeout_returns_one(tmp_path: Path) -> None:
    """TimeoutExpired from subprocess.run must surface as exit 1, not a traceback.

    Why this test exists: _run_git wraps subprocess.run — if git push hangs
    past _GIT_TIMEOUT seconds, subprocess raises TimeoutExpired. Without the
    try/except in _run_git the exception propagates as a raw traceback.
    This test patches subprocess.run directly (not _run_git) so the real
    timeout-handling path in _run_git is exercised.
    """
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def subprocess_side_effect(*args: object, **kwargs: object) -> None:
        # Simulate git push hanging past the timeout.
        cmd = args[0] if args else kwargs.get("args", [])
        if isinstance(cmd, list) and "push" in cmd:
            raise subprocess.TimeoutExpired(cmd=cmd, timeout=60)
        # All other git calls (rev-parse, add, commit) succeed normally.
        m = MagicMock(spec=subprocess.CompletedProcess)
        m.returncode = 0
        m.stdout = ""
        m.stderr = ""
        return m

    with patch("subprocess.run", side_effect=subprocess_side_effect):
        result = run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert result == 1


def test_run_agent_deploy_git_timeout_no_traceback(capsys, tmp_path: Path) -> None:
    """Confirm no raw traceback appears in stderr when git push times out."""
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def subprocess_side_effect(*args: object, **kwargs: object) -> None:
        cmd = args[0] if args else kwargs.get("args", [])
        if isinstance(cmd, list) and "push" in cmd:
            raise subprocess.TimeoutExpired(cmd=cmd, timeout=60)
        m = MagicMock(spec=subprocess.CompletedProcess)
        m.returncode = 0
        m.stdout = ""
        m.stderr = ""
        return m

    with patch("subprocess.run", side_effect=subprocess_side_effect):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    err = capsys.readouterr().err
    assert "Traceback" not in err
    assert "timed out" in err


# ---------------------------------------------------------------------------
# deploy — "nothing to commit" (idempotent re-deploy)
# ---------------------------------------------------------------------------


def test_run_agent_deploy_nothing_to_commit_returns_zero(tmp_path: Path) -> None:
    """Re-deploying unchanged agent files must exit 0, not abort."""
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def git_side_effect(args: list[str], cwd: Path) -> MagicMock:
        if args[0] == "commit":
            m = MagicMock(spec=subprocess.CompletedProcess)
            m.returncode = 1
            m.stdout = "nothing to commit, working tree clean"
            m.stderr = ""
            return m
        return _git_success()

    with patch(_PATCH_GIT, side_effect=git_side_effect):
        result = run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert result == 0


def test_run_agent_deploy_nothing_to_commit_prints_up_to_date(
    capsys, tmp_path: Path
) -> None:
    """Operator must see a clear message when nothing was pushed."""
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def git_side_effect(args: list[str], cwd: Path) -> MagicMock:
        if args[0] == "commit":
            m = MagicMock(spec=subprocess.CompletedProcess)
            m.returncode = 1
            m.stdout = "nothing to commit, working tree clean"
            m.stderr = ""
            return m
        return _git_success()

    with patch(_PATCH_GIT, side_effect=git_side_effect):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    assert "already up to date" in capsys.readouterr().out


def test_run_agent_deploy_nothing_to_commit_still_prints_vps_commands(
    capsys, tmp_path: Path
) -> None:
    """VPS docker commands must still be printed even when nothing was pushed."""
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    deploy_repo = _make_deploy_repo(tmp_path)

    def git_side_effect(args: list[str], cwd: Path) -> MagicMock:
        if args[0] == "commit":
            m = MagicMock(spec=subprocess.CompletedProcess)
            m.returncode = 1
            m.stdout = "nothing added to commit but untracked files present"
            m.stderr = ""
            return m
        return _git_success()

    with patch(_PATCH_GIT, side_effect=git_side_effect):
        run_agent_deploy(tmp_path, _AGENT_ID, deploy_repo)

    out = capsys.readouterr().out
    assert "docker build" in out
    assert "DEPLOY READY" in out


# ---------------------------------------------------------------------------
# run_agent_live() — happy path
# ---------------------------------------------------------------------------


def test_run_agent_live_returns_zero(tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "deployed"}
    _make_registry(tmp_path, agents=[entry])
    assert run_agent_live(tmp_path, _AGENT_ID) == 0


def test_run_agent_live_updates_status_to_live(tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "deployed"}
    _make_registry(tmp_path, agents=[entry])
    run_agent_live(tmp_path, _AGENT_ID)
    agents = registry_load(tmp_path)
    agent = next(a for a in agents if a["id"] == _AGENT_ID)
    assert agent["status"] == "live"


def test_run_agent_live_prints_confirmation(capsys, tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "deployed"}
    _make_registry(tmp_path, agents=[entry])
    run_agent_live(tmp_path, _AGENT_ID)
    assert "marked as live" in capsys.readouterr().out


def test_run_agent_live_agent_id_in_output(capsys, tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "deployed"}
    _make_registry(tmp_path, agents=[entry])
    run_agent_live(tmp_path, _AGENT_ID)
    assert _AGENT_ID in capsys.readouterr().out


# ---------------------------------------------------------------------------
# run_agent_live() — already live (idempotent)
# ---------------------------------------------------------------------------


def test_run_agent_live_already_live_returns_zero(tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "live"}
    _make_registry(tmp_path, agents=[entry])
    assert run_agent_live(tmp_path, _AGENT_ID) == 0


def test_run_agent_live_already_live_prints_message(capsys, tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "live"}
    _make_registry(tmp_path, agents=[entry])
    run_agent_live(tmp_path, _AGENT_ID)
    assert "already live" in capsys.readouterr().out


def test_run_agent_live_already_live_status_unchanged(tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "live"}
    _make_registry(tmp_path, agents=[entry])
    run_agent_live(tmp_path, _AGENT_ID)
    agents = registry_load(tmp_path)
    agent = next(a for a in agents if a["id"] == _AGENT_ID)
    assert agent["status"] == "live"


# ---------------------------------------------------------------------------
# run_agent_live() — error cases
# ---------------------------------------------------------------------------


def test_run_agent_live_unknown_id_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert run_agent_live(tmp_path, "ghost-agent-01") == 1


def test_run_agent_live_unknown_id_error_message(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_live(tmp_path, "ghost-agent-01")
    assert "not found" in capsys.readouterr().err


def test_run_agent_live_unknown_id_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_live(tmp_path, "ghost-agent-01")
    assert "Traceback" not in capsys.readouterr().err


# ---------------------------------------------------------------------------
# CliRunner integration — agent deploy
# ---------------------------------------------------------------------------


def _cli_deploy(
    tmp_path: Path,
    agent_id: str = _AGENT_ID,
    deploy_repo: Path | None = None,
    git_mock_return: MagicMock | None = None,
) -> object:
    """Invoke bricklayer agent deploy via CliRunner with mocked git."""
    if deploy_repo is None:
        deploy_repo = _make_deploy_repo(tmp_path)
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")
    env = {"DEPLOY_REPO_PATH": str(deploy_repo)}
    git_return = git_mock_return or _git_success()

    with patch("cli.config.find_yaml") as mock_find, \
         patch(_PATCH_GIT, return_value=git_return):
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        return _RUNNER.invoke(app, ["agent", "deploy", "--id", agent_id], env=env)


def test_cli_agent_deploy_exits_zero(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    result = _cli_deploy(tmp_path)
    assert result.exit_code == 0


def test_cli_agent_deploy_output_contains_deploy_ready(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_REGISTRY_ENTRY)])
    _make_agent_dir(tmp_path)
    result = _cli_deploy(tmp_path)
    assert "DEPLOY READY" in result.output


def test_cli_agent_deploy_no_env_var_exits_one() -> None:
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = Path("/fake/bricklayer.yaml")
        result = _RUNNER.invoke(app, ["agent", "deploy", "--id", _AGENT_ID], env={})
    assert result.exit_code == 1


def test_cli_agent_deploy_no_env_var_error_message() -> None:
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = Path("/fake/bricklayer.yaml")
        result = _RUNNER.invoke(app, ["agent", "deploy", "--id", _AGENT_ID], env={})
    assert "DEPLOY_REPO_PATH" in result.output


def test_cli_agent_deploy_no_yaml_exits_one() -> None:
    with patch("cli.config.find_yaml", return_value=None):
        result = _RUNNER.invoke(
            app, ["agent", "deploy", "--id", _AGENT_ID],
            env={"DEPLOY_REPO_PATH": "/tmp/fake"},
        )
    assert result.exit_code == 1


def test_cli_agent_deploy_agent_missing_exits_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)  # empty registry
    result = _cli_deploy(tmp_path)
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# CliRunner integration — agent live
# ---------------------------------------------------------------------------


def test_cli_agent_live_exits_zero(tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "deployed"}
    _make_registry(tmp_path, agents=[entry])
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")

    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        result = _RUNNER.invoke(app, ["agent", "live", "--id", _AGENT_ID])

    assert result.exit_code == 0


def test_cli_agent_live_output_contains_marked_live(tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "deployed"}
    _make_registry(tmp_path, agents=[entry])
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")

    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        result = _RUNNER.invoke(app, ["agent", "live", "--id", _AGENT_ID])

    assert "live" in result.output.lower()


def test_cli_agent_live_unknown_id_exits_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")

    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        result = _RUNNER.invoke(app, ["agent", "live", "--id", "ghost-agent-01"])

    assert result.exit_code == 1


def test_cli_agent_live_no_yaml_exits_one() -> None:
    with patch("cli.config.find_yaml", return_value=None):
        result = _RUNNER.invoke(app, ["agent", "live", "--id", _AGENT_ID])
    assert result.exit_code == 1


def test_cli_agent_live_already_live_exits_zero(tmp_path: Path) -> None:
    entry = {**_REGISTRY_ENTRY, "status": "live"}
    _make_registry(tmp_path, agents=[entry])
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")

    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        result = _RUNNER.invoke(app, ["agent", "live", "--id", _AGENT_ID])

    assert result.exit_code == 0
