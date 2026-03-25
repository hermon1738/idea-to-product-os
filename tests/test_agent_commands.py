"""Tests for Brick 22 — agent list and status commands."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml
from typer.testing import CliRunner

from cli.commands.agent import (
    _format_detail,
    _format_row,
    run_agent_list,
    run_agent_status,
)
from cli.main import app

# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

_RUNNER = CliRunner()

_SCRIBE: dict = {
    "id": "idea-os-scribe-01",
    "name": "Session Scribe",
    "project": "idea-to-product-os",
    "role": "scribe",
    "runtime": "raw-python",
    "status": "live",
    "trigger": "!scribe in Discord",
    "discord_channel": "session-scribe",
    "location": "~/ai-agents/agents/session-scribe/",
}

_FORMATTER: dict = {
    "id": "idea-os-formatter-01",
    "name": "Org Schema Formatter",
    "project": "idea-to-product-os",
    "role": "formatter",
    "runtime": "raw-python",
    "status": "live",
    "trigger": "!schema in Discord",
    "discord_channel": "org-schema-formatter",
    "location": "~/ai-agents/agents/org-schema-formatter/",
}

_DISPATCHER: dict = {
    "id": "idea-os-dispatcher-01",
    "name": "Assignment Dispatcher",
    "project": "idea-to-product-os",
    "role": "dispatcher",
    "runtime": "raw-python",
    "status": "live",
    "trigger": "!dispatch in Discord",
    "discord_channel": "assignment-dispatcher",
    "location": "~/ai-agents/agents/assignment-dispatcher/",
}

_REPO_ROOT = Path(__file__).parent.parent


def _make_registry(tmp_path: Path, agents: list[dict] | None = None) -> Path:
    """Write a registry.yaml to tmp_path with the given agents."""
    registry_dir = tmp_path / "context" / "agents"
    registry_dir.mkdir(parents=True)
    data = {"agents": agents if agents is not None else []}
    (registry_dir / "registry.yaml").write_text(
        yaml.dump(data, default_flow_style=False), encoding="utf-8"
    )
    return tmp_path


def _make_malformed_registry(tmp_path: Path) -> Path:
    registry_dir = tmp_path / "context" / "agents"
    registry_dir.mkdir(parents=True)
    (registry_dir / "registry.yaml").write_text(
        "agents:\n  - id: foo\n    bad yaml: [\n", encoding="utf-8"
    )
    return tmp_path


# ---------------------------------------------------------------------------
# _format_row() unit tests
# ---------------------------------------------------------------------------


def test_format_row_contains_id() -> None:
    assert _SCRIBE["id"] in _format_row(_SCRIBE)


def test_format_row_contains_name() -> None:
    assert "Session Scribe" in _format_row(_SCRIBE)


def test_format_row_contains_runtime() -> None:
    assert "raw-python" in _format_row(_SCRIBE)


def test_format_row_contains_status() -> None:
    assert "live" in _format_row(_SCRIBE)


def test_format_row_missing_key_renders_empty() -> None:
    row = _format_row({"id": "test-01"})
    assert "test-01" in row


# ---------------------------------------------------------------------------
# _format_detail() unit tests
# ---------------------------------------------------------------------------


def test_format_detail_contains_agent_label() -> None:
    assert "Agent:" in _format_detail(_SCRIBE)


def test_format_detail_contains_id() -> None:
    assert "idea-os-scribe-01" in _format_detail(_SCRIBE)


def test_format_detail_contains_name() -> None:
    assert "Session Scribe" in _format_detail(_SCRIBE)


def test_format_detail_contains_project() -> None:
    assert "idea-to-product-os" in _format_detail(_SCRIBE)


def test_format_detail_contains_role() -> None:
    assert "scribe" in _format_detail(_SCRIBE)


def test_format_detail_contains_runtime() -> None:
    assert "raw-python" in _format_detail(_SCRIBE)


def test_format_detail_contains_status() -> None:
    assert "live" in _format_detail(_SCRIBE)


def test_format_detail_contains_trigger() -> None:
    assert "!scribe in Discord" in _format_detail(_SCRIBE)


def test_format_detail_contains_channel() -> None:
    assert "session-scribe" in _format_detail(_SCRIBE)


def test_format_detail_contains_location() -> None:
    assert "~/ai-agents/agents/session-scribe/" in _format_detail(_SCRIBE)


# ---------------------------------------------------------------------------
# run_agent_list() — live registry
# ---------------------------------------------------------------------------


def test_run_agent_list_returns_zero() -> None:
    assert run_agent_list(_REPO_ROOT) == 0


def test_run_agent_list_prints_scribe(capsys) -> None:
    run_agent_list(_REPO_ROOT)
    assert "idea-os-scribe-01" in capsys.readouterr().out


def test_run_agent_list_prints_formatter(capsys) -> None:
    run_agent_list(_REPO_ROOT)
    assert "idea-os-formatter-01" in capsys.readouterr().out


def test_run_agent_list_prints_dispatcher(capsys) -> None:
    run_agent_list(_REPO_ROOT)
    assert "idea-os-dispatcher-01" in capsys.readouterr().out


def test_run_agent_list_prints_header(capsys) -> None:
    run_agent_list(_REPO_ROOT)
    out = capsys.readouterr().out
    assert "ID" in out
    assert "NAME" in out
    assert "RUNTIME" in out
    assert "STATUS" in out


def test_run_agent_list_prints_divider(capsys) -> None:
    run_agent_list(_REPO_ROOT)
    assert "─" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# run_agent_list() — edge cases
# ---------------------------------------------------------------------------


def test_run_agent_list_empty_registry_returns_zero(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert run_agent_list(tmp_path) == 0


def test_run_agent_list_empty_registry_prints_prompt(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_list(tmp_path)
    out = capsys.readouterr().out
    assert "No agents registered" in out


def test_run_agent_list_empty_registry_prints_new_command(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_list(tmp_path)
    out = capsys.readouterr().out
    assert "bricklayer agent new" in out


def test_run_agent_list_missing_registry_returns_zero(tmp_path: Path) -> None:
    # No registry.yaml at all — treated same as empty.
    assert run_agent_list(tmp_path) == 0


def test_run_agent_list_missing_registry_prints_prompt(capsys, tmp_path: Path) -> None:
    run_agent_list(tmp_path)
    assert "No agents registered" in capsys.readouterr().out


def test_run_agent_list_malformed_registry_returns_one(tmp_path: Path) -> None:
    _make_malformed_registry(tmp_path)
    assert run_agent_list(tmp_path) == 1


def test_run_agent_list_malformed_registry_no_traceback(capsys, tmp_path: Path) -> None:
    _make_malformed_registry(tmp_path)
    run_agent_list(tmp_path)
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_list_single_agent_shows_in_table(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE])
    run_agent_list(tmp_path)
    assert "Session Scribe" in capsys.readouterr().out


def test_run_agent_list_all_three_in_output(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE, _FORMATTER, _DISPATCHER])
    run_agent_list(tmp_path)
    out = capsys.readouterr().out
    assert "idea-os-scribe-01" in out
    assert "idea-os-formatter-01" in out
    assert "idea-os-dispatcher-01" in out


# ---------------------------------------------------------------------------
# run_agent_status() — live registry
# ---------------------------------------------------------------------------


def test_run_agent_status_known_id_returns_zero() -> None:
    assert run_agent_status(_REPO_ROOT, "idea-os-scribe-01") == 0


def test_run_agent_status_prints_id(capsys) -> None:
    run_agent_status(_REPO_ROOT, "idea-os-scribe-01")
    assert "idea-os-scribe-01" in capsys.readouterr().out


def test_run_agent_status_prints_name(capsys) -> None:
    run_agent_status(_REPO_ROOT, "idea-os-scribe-01")
    assert "Session Scribe" in capsys.readouterr().out


def test_run_agent_status_prints_all_labels(capsys) -> None:
    run_agent_status(_REPO_ROOT, "idea-os-scribe-01")
    out = capsys.readouterr().out
    for label in ("Agent:", "Name:", "Project:", "Role:", "Runtime:", "Status:", "Trigger:", "Location:"):
        assert label in out, f"Missing label: {label}"


def test_run_agent_status_formatter_correct_name(capsys) -> None:
    run_agent_status(_REPO_ROOT, "idea-os-formatter-01")
    assert "Org Schema Formatter" in capsys.readouterr().out


def test_run_agent_status_dispatcher_trigger(capsys) -> None:
    run_agent_status(_REPO_ROOT, "idea-os-dispatcher-01")
    assert "!dispatch" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# run_agent_status() — edge cases
# ---------------------------------------------------------------------------


def test_run_agent_status_unknown_id_returns_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert run_agent_status(tmp_path, "ghost-agent") == 1


def test_run_agent_status_unknown_id_error_message(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_status(tmp_path, "ghost-agent")
    assert "Agent not found: ghost-agent" in capsys.readouterr().err


def test_run_agent_status_unknown_id_no_traceback(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path)
    run_agent_status(tmp_path, "ghost-agent")
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_status_missing_registry_returns_one(tmp_path: Path) -> None:
    # No registry.yaml — get() returns None → exit 1.
    assert run_agent_status(tmp_path, "any-agent") == 1


def test_run_agent_status_missing_registry_no_traceback(capsys, tmp_path: Path) -> None:
    run_agent_status(tmp_path, "any-agent")
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_status_malformed_registry_returns_one(tmp_path: Path) -> None:
    _make_malformed_registry(tmp_path)
    assert run_agent_status(tmp_path, "any-agent") == 1


def test_run_agent_status_malformed_registry_no_traceback(capsys, tmp_path: Path) -> None:
    _make_malformed_registry(tmp_path)
    run_agent_status(tmp_path, "any-agent")
    assert "Traceback" not in capsys.readouterr().err


def test_run_agent_status_known_id_in_tmp_registry(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE])
    assert run_agent_status(tmp_path, "idea-os-scribe-01") == 0


def test_run_agent_status_channel_in_output(capsys, tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE])
    run_agent_status(tmp_path, "idea-os-scribe-01")
    assert "session-scribe" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# CliRunner integration — agent list
# ---------------------------------------------------------------------------


def test_cli_agent_list_exit_zero(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE])
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "list"])
    assert result.exit_code == 0


def test_cli_agent_list_output_contains_id(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE])
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "list"])
    assert "idea-os-scribe-01" in result.output


def test_cli_agent_list_empty_exits_zero(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[])
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "list"])
    assert result.exit_code == 0


def test_cli_agent_list_empty_shows_prompt(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[])
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "list"])
    assert "No agents registered" in result.output


def test_cli_agent_list_no_yaml_exits_one() -> None:
    with patch("cli.config.find_yaml", return_value=None):
        result = _RUNNER.invoke(app, ["agent", "list"])
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# CliRunner integration — agent status
# ---------------------------------------------------------------------------


def test_cli_agent_status_known_id_exits_zero(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE])
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "status", "idea-os-scribe-01"])
    assert result.exit_code == 0


def test_cli_agent_status_output_contains_name(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[_SCRIBE])
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "status", "idea-os-scribe-01"])
    assert "Session Scribe" in result.output


def test_cli_agent_status_unknown_id_exits_one(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "status", "nonexistent"])
    assert result.exit_code == 1


def test_cli_agent_status_unknown_id_error_in_output(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    with patch("cli.config.find_yaml") as mock_find:
        mock_find.return_value = tmp_path / "bricklayer.yaml"
        (tmp_path / "bricklayer.yaml").write_text("", encoding="utf-8")
        result = _RUNNER.invoke(app, ["agent", "status", "nonexistent"])
    assert "Agent not found" in result.output


def test_cli_agent_status_no_yaml_exits_one() -> None:
    with patch("cli.config.find_yaml", return_value=None):
        result = _RUNNER.invoke(app, ["agent", "status", "any-id"])
    assert result.exit_code == 1
