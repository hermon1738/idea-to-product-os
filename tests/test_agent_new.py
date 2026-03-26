"""Tests for Brick 23 — bricklayer agent new command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from typer.testing import CliRunner

from cli.commands.agent import (
    VALID_RUNTIMES,
    _build_placeholder_map,
    _build_registry_entry,
    _get_template_path,
    _replace_placeholders,
    _scaffold_nanobot,
    _scaffold_raw_python,
    _validate_agent_id,
    run_agent_new,
)
from cli.main import app
from cli.registry import load as registry_load

# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

_RUNNER = CliRunner()

_VALID_ID = "idea-os-monitor-01"
_PROJECT = "idea-to-product-os"
_ROLE = "monitor"
_EMPTY_CONFIG: dict = {}


def _make_registry(tmp_path: Path, agents: list[dict] | None = None) -> None:
    """Create registry.yaml in tmp_path with the given agents."""
    registry_dir = tmp_path / "context" / "agents"
    registry_dir.mkdir(parents=True, exist_ok=True)
    data = {"agents": agents if agents is not None else []}
    (registry_dir / "registry.yaml").write_text(
        yaml.dump(data, default_flow_style=False), encoding="utf-8"
    )


def _make_nanobot_template(tmp_path: Path) -> Path:
    """Create a minimal nanobot-template directory under tmp_path."""
    template_dir = tmp_path / "agents" / "nanobot-template"
    workspace = template_dir / "workspace"
    workspace.mkdir(parents=True)

    (template_dir / "agent.yaml").write_text(
        "id: __AGENT_ID__\n"
        "name: __AGENT_NAME__\n"
        "project: __PROJECT__\n"
        "role: __ROLE__\n"
        "runtime: nanobot\n"
        "status: stopped\n"
        "trigger: '!__ROLE__ in Discord'\n"
        "location: context/agents/__AGENT_ID__/\n"
        "discord_channel: __DISCORD_CHANNEL__\n"
        "container_name: __CONTAINER_NAME__\n",
        encoding="utf-8",
    )
    (workspace / "SOUL.md").write_text(
        "# __AGENT_NAME__ — Soul\nProject: __PROJECT__\nRole: __ROLE__\n",
        encoding="utf-8",
    )
    (workspace / "AGENTS.md").write_text(
        "# Agents for __PROJECT__\n- __AGENT_ID__\n",
        encoding="utf-8",
    )
    (workspace / "USER.md").write_text(
        "# User context\nAgent: __AGENT_ID__\nSequence: __SEQUENCE__\n",
        encoding="utf-8",
    )
    return template_dir


# ---------------------------------------------------------------------------
# _validate_agent_id()
# ---------------------------------------------------------------------------


def test_validate_valid_id_returns_none() -> None:
    assert _validate_agent_id("idea-os-monitor-01") is None


def test_validate_valid_id_complex_slug() -> None:
    assert _validate_agent_id("reddit-monitor-poller-01") is None


def test_validate_valid_id_two_segment() -> None:
    assert _validate_agent_id("monitor-agent-99") is None


def test_validate_invalid_spaces_returns_error() -> None:
    result = _validate_agent_id("my agent 01")
    assert result is not None
    assert "Invalid" in result


def test_validate_invalid_uppercase_returns_error() -> None:
    result = _validate_agent_id("AGENT-01")
    assert result is not None
    assert "Invalid" in result


def test_validate_invalid_missing_sequence_returns_error() -> None:
    # No trailing two-digit sequence.
    result = _validate_agent_id("idea-os-monitor")
    assert result is not None


def test_validate_invalid_single_digit_seq_returns_error() -> None:
    result = _validate_agent_id("idea-os-monitor-1")
    assert result is not None


def test_validate_error_contains_format_hint() -> None:
    result = _validate_agent_id("BAD ID")
    assert result is not None
    assert "Examples:" in result or "format" in result.lower()


def test_validate_invalid_slash_returns_error() -> None:
    assert _validate_agent_id("idea/os/monitor-01") is not None


def test_validate_invalid_dot_returns_error() -> None:
    assert _validate_agent_id("idea.os.monitor-01") is not None


# ---------------------------------------------------------------------------
# _get_template_path()
# ---------------------------------------------------------------------------


def test_get_template_path_default(tmp_path: Path) -> None:
    path = _get_template_path(tmp_path, {})
    assert path == tmp_path / "agents" / "nanobot-template"


def test_get_template_path_from_config(tmp_path: Path) -> None:
    config = {"agents": {"nanobot_template": "custom/templates/nanobot"}}
    path = _get_template_path(tmp_path, config)
    assert path == tmp_path / "custom" / "templates" / "nanobot"


def test_get_template_path_empty_agents_dict(tmp_path: Path) -> None:
    path = _get_template_path(tmp_path, {"agents": {}})
    assert path == tmp_path / "agents" / "nanobot-template"


def test_get_template_path_agents_none(tmp_path: Path) -> None:
    path = _get_template_path(tmp_path, {"agents": None})
    assert path == tmp_path / "agents" / "nanobot-template"


# ---------------------------------------------------------------------------
# _build_placeholder_map()
# ---------------------------------------------------------------------------


def test_build_placeholder_map_agent_id() -> None:
    m = _build_placeholder_map("idea-os-monitor-01", "idea-to-product-os", "monitor")
    assert m["__AGENT_ID__"] == "idea-os-monitor-01"


def test_build_placeholder_map_project() -> None:
    m = _build_placeholder_map("idea-os-monitor-01", "idea-to-product-os", "monitor")
    assert m["__PROJECT__"] == "idea-to-product-os"


def test_build_placeholder_map_role() -> None:
    m = _build_placeholder_map("idea-os-monitor-01", "idea-to-product-os", "monitor")
    assert m["__ROLE__"] == "monitor"


def test_build_placeholder_map_sequence() -> None:
    m = _build_placeholder_map("idea-os-monitor-01", "idea-to-product-os", "monitor")
    assert m["__SEQUENCE__"] == "01"


def test_build_placeholder_map_discord_channel() -> None:
    m = _build_placeholder_map("idea-os-monitor-01", "idea-to-product-os", "monitor")
    assert m["__DISCORD_CHANNEL__"] == "idea-os-monitor-01"


def test_build_placeholder_map_container_name() -> None:
    m = _build_placeholder_map("idea-os-monitor-01", "idea-to-product-os", "monitor")
    assert m["__CONTAINER_NAME__"] == "idea-os-monitor-01"


# ---------------------------------------------------------------------------
# _replace_placeholders()
# ---------------------------------------------------------------------------


def test_replace_placeholders_substitutes_tokens(tmp_path: Path) -> None:
    f = tmp_path / "test.yaml"
    f.write_text("id: __AGENT_ID__\nproject: __PROJECT__\n", encoding="utf-8")
    _replace_placeholders(f, {"__AGENT_ID__": "my-agent-01", "__PROJECT__": "my-proj"})
    assert f.read_text(encoding="utf-8") == "id: my-agent-01\nproject: my-proj\n"


def test_replace_placeholders_missing_file_no_crash(tmp_path: Path) -> None:
    # Should not raise for a missing file.
    _replace_placeholders(tmp_path / "nonexistent.md", {"__X__": "y"})


def test_replace_placeholders_no_match_unchanged(tmp_path: Path) -> None:
    f = tmp_path / "test.md"
    f.write_text("no tokens here\n", encoding="utf-8")
    _replace_placeholders(f, {"__AGENT_ID__": "x"})
    assert f.read_text(encoding="utf-8") == "no tokens here\n"


# ---------------------------------------------------------------------------
# _scaffold_nanobot()
# ---------------------------------------------------------------------------


def test_scaffold_nanobot_creates_directory(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    _make_registry(tmp_path)
    template = tmp_path / "agents" / "nanobot-template"
    code, target = _scaffold_nanobot(tmp_path, _VALID_ID, _PROJECT, _ROLE, template)
    assert code == 0
    assert target is not None
    assert target.exists()


def test_scaffold_nanobot_agent_yaml_id_replaced(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    template = tmp_path / "agents" / "nanobot-template"
    _scaffold_nanobot(tmp_path, _VALID_ID, _PROJECT, _ROLE, template)
    agent_yaml = (tmp_path / "context" / "agents" / _VALID_ID / "agent.yaml").read_text(encoding="utf-8")
    assert _VALID_ID in agent_yaml
    assert "__AGENT_ID__" not in agent_yaml


def test_scaffold_nanobot_agent_yaml_project_replaced(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    template = tmp_path / "agents" / "nanobot-template"
    _scaffold_nanobot(tmp_path, _VALID_ID, _PROJECT, _ROLE, template)
    agent_yaml = (tmp_path / "context" / "agents" / _VALID_ID / "agent.yaml").read_text(encoding="utf-8")
    assert _PROJECT in agent_yaml
    assert "__PROJECT__" not in agent_yaml


def test_scaffold_nanobot_soul_md_replaced(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    template = tmp_path / "agents" / "nanobot-template"
    _scaffold_nanobot(tmp_path, _VALID_ID, _PROJECT, _ROLE, template)
    soul = (tmp_path / "context" / "agents" / _VALID_ID / "workspace" / "SOUL.md").read_text(encoding="utf-8")
    assert "__AGENT_NAME__" not in soul
    assert "__PROJECT__" not in soul


def test_scaffold_nanobot_user_md_sequence_replaced(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    template = tmp_path / "agents" / "nanobot-template"
    _scaffold_nanobot(tmp_path, _VALID_ID, _PROJECT, _ROLE, template)
    user_md = (tmp_path / "context" / "agents" / _VALID_ID / "workspace" / "USER.md").read_text(encoding="utf-8")
    assert "01" in user_md
    assert "__SEQUENCE__" not in user_md


def test_scaffold_nanobot_missing_template_returns_one(tmp_path: Path) -> None:
    template = tmp_path / "agents" / "nanobot-template"  # does not exist
    code, target = _scaffold_nanobot(tmp_path, _VALID_ID, _PROJECT, _ROLE, template)
    assert code == 1
    assert target is None


def test_scaffold_nanobot_missing_template_no_traceback(capsys, tmp_path: Path) -> None:
    template = tmp_path / "agents" / "nanobot-template"
    _scaffold_nanobot(tmp_path, _VALID_ID, _PROJECT, _ROLE, template)
    assert "Traceback" not in capsys.readouterr().err


# ---------------------------------------------------------------------------
# _scaffold_raw_python()
# ---------------------------------------------------------------------------


def test_scaffold_raw_python_creates_directory(tmp_path: Path) -> None:
    code, target = _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    assert code == 0
    assert target is not None
    assert target.exists()


def test_scaffold_raw_python_creates_agent_py(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "agent.py").exists()


def test_scaffold_raw_python_agent_py_contains_agent_id(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    content = (tmp_path / "context" / "agents" / _VALID_ID / "agent.py").read_text(encoding="utf-8")
    assert _VALID_ID in content


def test_scaffold_raw_python_agent_py_constant(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    content = (tmp_path / "context" / "agents" / _VALID_ID / "agent.py").read_text(encoding="utf-8")
    assert "AGENT_ID" in content


def test_scaffold_raw_python_creates_dockerfile(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "Dockerfile").exists()


def test_scaffold_raw_python_creates_requirements_txt(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "requirements.txt").exists()


def test_scaffold_raw_python_requirements_has_groq(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    req = (tmp_path / "context" / "agents" / _VALID_ID / "requirements.txt").read_text(encoding="utf-8")
    assert "groq" in req


def test_scaffold_raw_python_requirements_has_discord(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    req = (tmp_path / "context" / "agents" / _VALID_ID / "requirements.txt").read_text(encoding="utf-8")
    assert "discord.py" in req


def test_scaffold_raw_python_creates_agent_yaml(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "agent.yaml").exists()


def test_scaffold_raw_python_agent_yaml_id_correct(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    data = yaml.safe_load(
        (tmp_path / "context" / "agents" / _VALID_ID / "agent.yaml").read_text(encoding="utf-8")
    )
    assert data["id"] == _VALID_ID


def test_scaffold_raw_python_agent_yaml_status_stopped(tmp_path: Path) -> None:
    _scaffold_raw_python(tmp_path, _VALID_ID, _PROJECT, _ROLE)
    data = yaml.safe_load(
        (tmp_path / "context" / "agents" / _VALID_ID / "agent.yaml").read_text(encoding="utf-8")
    )
    assert data["status"] == "stopped"


# ---------------------------------------------------------------------------
# _build_registry_entry()
# ---------------------------------------------------------------------------


def test_build_registry_entry_id() -> None:
    e = _build_registry_entry(_VALID_ID, _PROJECT, _ROLE, "nanobot")
    assert e["id"] == _VALID_ID


def test_build_registry_entry_status_stopped() -> None:
    e = _build_registry_entry(_VALID_ID, _PROJECT, _ROLE, "nanobot")
    assert e["status"] == "stopped"


def test_build_registry_entry_runtime() -> None:
    e = _build_registry_entry(_VALID_ID, _PROJECT, _ROLE, "raw-python")
    assert e["runtime"] == "raw-python"


def test_build_registry_entry_project() -> None:
    e = _build_registry_entry(_VALID_ID, _PROJECT, _ROLE, "nanobot")
    assert e["project"] == _PROJECT


# ---------------------------------------------------------------------------
# run_agent_new() — nanobot runtime
# ---------------------------------------------------------------------------


def test_run_agent_new_nanobot_returns_zero(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    _make_registry(tmp_path)
    config = {"agents": {"nanobot_template": "agents/nanobot-template"}}
    assert run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, config) == 0


def test_run_agent_new_nanobot_directory_created(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    _make_registry(tmp_path)
    config = {"agents": {"nanobot_template": "agents/nanobot-template"}}
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, config)
    assert (tmp_path / "context" / "agents" / _VALID_ID).exists()


def test_run_agent_new_nanobot_registered(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    _make_registry(tmp_path)
    config = {"agents": {"nanobot_template": "agents/nanobot-template"}}
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, config)
    agents = registry_load(tmp_path)
    ids = [a["id"] for a in agents]
    assert _VALID_ID in ids


def test_run_agent_new_nanobot_registered_status_stopped(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    _make_registry(tmp_path)
    config = {"agents": {"nanobot_template": "agents/nanobot-template"}}
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, config)
    agents = registry_load(tmp_path)
    agent = next(a for a in agents if a["id"] == _VALID_ID)
    assert agent["status"] == "stopped"


def test_run_agent_new_nanobot_placeholders_replaced(tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    _make_registry(tmp_path)
    config = {"agents": {"nanobot_template": "agents/nanobot-template"}}
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, config)
    agent_yaml = (tmp_path / "context" / "agents" / _VALID_ID / "agent.yaml").read_text(encoding="utf-8")
    assert "__AGENT_ID__" not in agent_yaml
    assert _VALID_ID in agent_yaml


def test_run_agent_new_nanobot_prints_success(capsys, tmp_path: Path) -> None:
    _make_nanobot_template(tmp_path)
    _make_registry(tmp_path)
    config = {"agents": {"nanobot_template": "agents/nanobot-template"}}
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, config)
    out = capsys.readouterr().out
    assert "Agent scaffolded" in out
    assert _VALID_ID in out


# ---------------------------------------------------------------------------
# run_agent_new() — raw-python runtime
# ---------------------------------------------------------------------------


def test_run_agent_new_raw_python_returns_zero(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG) == 0


def test_run_agent_new_raw_python_directory_created(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert (tmp_path / "context" / "agents" / _VALID_ID).exists()


def test_run_agent_new_raw_python_agent_py_created(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "agent.py").exists()


def test_run_agent_new_raw_python_dockerfile_created(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "Dockerfile").exists()


def test_run_agent_new_raw_python_requirements_created(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "requirements.txt").exists()


def test_run_agent_new_raw_python_agent_yaml_created(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert (tmp_path / "context" / "agents" / _VALID_ID / "agent.yaml").exists()


def test_run_agent_new_raw_python_registered(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    ids = [a["id"] for a in registry_load(tmp_path)]
    assert _VALID_ID in ids


def test_run_agent_new_raw_python_agent_py_has_agent_id_constant(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    content = (tmp_path / "context" / "agents" / _VALID_ID / "agent.py").read_text(encoding="utf-8")
    assert f'AGENT_ID: str = "{_VALID_ID}"' in content


# ---------------------------------------------------------------------------
# run_agent_new() — error cases
# ---------------------------------------------------------------------------


def test_run_agent_new_invalid_id_spaces_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert run_agent_new(tmp_path, "my agent 01", "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG) == 1


def test_run_agent_new_invalid_id_uppercase_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert run_agent_new(tmp_path, "AGENT-01", "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG) == 1


def test_run_agent_new_invalid_id_error_has_format_hint(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, "BAD ID", "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    err = capsys.readouterr().err
    assert "error:" in err


def test_run_agent_new_unknown_runtime_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert run_agent_new(tmp_path, _VALID_ID, "langchain", _PROJECT, _ROLE, _EMPTY_CONFIG) == 1


def test_run_agent_new_unknown_runtime_lists_valid(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "langchain", _PROJECT, _ROLE, _EMPTY_CONFIG)
    err = capsys.readouterr().err
    assert "nanobot" in err
    assert "raw-python" in err


def test_run_agent_new_unknown_runtime_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "bad-runtime", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_new_duplicate_id_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG) == 1


def test_run_agent_new_duplicate_id_no_second_directory(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    count_before = len(list((tmp_path / "context" / "agents").iterdir()))
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert len(list((tmp_path / "context" / "agents").iterdir())) == count_before


def test_run_agent_new_duplicate_id_registry_unchanged(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    count_before = len(registry_load(tmp_path))
    run_agent_new(tmp_path, _VALID_ID, "raw-python", _PROJECT, _ROLE, _EMPTY_CONFIG)
    assert len(registry_load(tmp_path)) == count_before


def test_run_agent_new_nanobot_template_missing_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    config: dict = {}  # no nanobot_template set; default path won't exist
    assert run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, config) == 1


def test_run_agent_new_nanobot_template_missing_error_has_path(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, {})
    err = capsys.readouterr().err
    assert "nanobot-template" in err


def test_run_agent_new_nanobot_template_missing_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, {})
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_new_nanobot_template_missing_no_directory_created(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, {})
    assert not (tmp_path / "context" / "agents" / _VALID_ID).exists()


def test_run_agent_new_nanobot_template_missing_registry_unchanged(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    before = len(registry_load(tmp_path))
    run_agent_new(tmp_path, _VALID_ID, "nanobot", _PROJECT, _ROLE, {})
    assert len(registry_load(tmp_path)) == before


# ---------------------------------------------------------------------------
# CliRunner integration — agent new
# ---------------------------------------------------------------------------


def _cli_agent_new(tmp_path: Path, extra_args: list[str] | None = None) -> object:
    """Helper: invoke bricklayer agent new with standard flags via CliRunner."""
    (tmp_path / "bricklayer.yaml").write_text(
        "agents:\n  nanobot_template: agents/nanobot-template\n", encoding="utf-8"
    )
    _make_registry(tmp_path)
    _make_nanobot_template(tmp_path)
    args = [
        "agent", "new",
        "--id", _VALID_ID,
        "--runtime", "nanobot",
        "--project", _PROJECT,
        "--role", _ROLE,
    ]
    if extra_args:
        args += extra_args
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        return _RUNNER.invoke(app, args)


def test_cli_agent_new_nanobot_exits_zero(tmp_path: Path) -> None:
    result = _cli_agent_new(tmp_path)
    assert result.exit_code == 0


def test_cli_agent_new_nanobot_directory_created(tmp_path: Path) -> None:
    _cli_agent_new(tmp_path)
    assert (tmp_path / "context" / "agents" / _VALID_ID).exists()


def test_cli_agent_new_nanobot_registered_in_registry(tmp_path: Path) -> None:
    _cli_agent_new(tmp_path)
    ids = [a["id"] for a in registry_load(tmp_path)]
    assert _VALID_ID in ids


def test_cli_agent_new_raw_python_exits_zero(tmp_path: Path) -> None:
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")
    _make_registry(tmp_path)
    args = [
        "agent", "new",
        "--id", _VALID_ID,
        "--runtime", "raw-python",
        "--project", _PROJECT,
        "--role", _ROLE,
    ]
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        result = _RUNNER.invoke(app, args)
    assert result.exit_code == 0


def test_cli_agent_new_raw_python_directory_created(tmp_path: Path) -> None:
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")
    _make_registry(tmp_path)
    args = [
        "agent", "new",
        "--id", _VALID_ID,
        "--runtime", "raw-python",
        "--project", _PROJECT,
        "--role", _ROLE,
    ]
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        _RUNNER.invoke(app, args)
    assert (tmp_path / "context" / "agents" / _VALID_ID).exists()


def test_cli_agent_new_invalid_id_exits_one(tmp_path: Path) -> None:
    (tmp_path / "bricklayer.yaml").write_text("agents: {}\n", encoding="utf-8")
    _make_registry(tmp_path)
    args = [
        "agent", "new",
        "--id", "INVALID ID",
        "--runtime", "raw-python",
        "--project", _PROJECT,
        "--role", _ROLE,
    ]
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        result = _RUNNER.invoke(app, args)
    assert result.exit_code == 1


def test_cli_agent_new_no_yaml_exits_one() -> None:
    with patch("cli.config.find_yaml", return_value=None):
        result = _RUNNER.invoke(app, [
            "agent", "new",
            "--id", _VALID_ID, "--runtime", "raw-python",
            "--project", _PROJECT, "--role", _ROLE,
        ])
    assert result.exit_code == 1
