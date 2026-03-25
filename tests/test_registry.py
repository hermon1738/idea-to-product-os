"""Tests for Brick 21 — agent registry module."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from cli.registry import (
    REGISTRY_RELPATH,
    REQUIRED_FIELDS,
    add,
    get,
    load,
    update_status,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REGISTRY_PATH = Path(__file__).parent.parent / "context" / "agents" / "registry.yaml"

_VALID_AGENT: dict = {
    "id": "test-agent-01",
    "name": "Test Agent",
    "project": "test-project",
    "role": "tester",
    "runtime": "raw-python",
    "status": "stopped",
    "trigger": "!test in Discord",
    "location": "~/ai-agents/agents/test-agent/",
}


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
# load() — live registry (uses the actual registry.yaml in the repo)
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).parent.parent


def test_load_returns_list() -> None:
    agents = load(_REPO_ROOT)
    assert isinstance(agents, list)


def test_load_returns_three_agents() -> None:
    agents = load(_REPO_ROOT)
    assert len(agents) == 3


def test_load_all_required_fields_present() -> None:
    agents = load(_REPO_ROOT)
    for agent in agents:
        missing = REQUIRED_FIELDS - set(agent.keys())
        assert not missing, f"Agent {agent.get('id')} missing: {missing}"


def test_load_scribe_agent_present() -> None:
    ids = [a["id"] for a in load(_REPO_ROOT)]
    assert "idea-os-scribe-01" in ids


def test_load_formatter_agent_present() -> None:
    ids = [a["id"] for a in load(_REPO_ROOT)]
    assert "idea-os-formatter-01" in ids


def test_load_dispatcher_agent_present() -> None:
    ids = [a["id"] for a in load(_REPO_ROOT)]
    assert "idea-os-dispatcher-01" in ids


def test_load_all_agents_have_live_status() -> None:
    for agent in load(_REPO_ROOT):
        assert agent["status"] == "live", f"{agent['id']} not live"


# ---------------------------------------------------------------------------
# load() — edge cases
# ---------------------------------------------------------------------------


def test_load_missing_registry_returns_empty_list(tmp_path: Path) -> None:
    assert load(tmp_path) == []


def test_load_missing_registry_no_crash(tmp_path: Path) -> None:
    # Should not raise any exception
    result = load(tmp_path)
    assert isinstance(result, list)


def test_load_malformed_yaml_raises_value_error(tmp_path: Path) -> None:
    _make_malformed_registry(tmp_path)
    with pytest.raises(ValueError):
        load(tmp_path)


def test_load_malformed_yaml_error_message(tmp_path: Path) -> None:
    _make_malformed_registry(tmp_path)
    with pytest.raises(ValueError, match="malformed"):
        load(tmp_path)


def test_load_empty_registry_returns_empty_list(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[])
    assert load(tmp_path) == []


# ---------------------------------------------------------------------------
# get()
# ---------------------------------------------------------------------------


def test_get_known_id_returns_dict() -> None:
    result = get(_REPO_ROOT, "idea-os-scribe-01")
    assert result is not None
    assert isinstance(result, dict)


def test_get_scribe_correct_name() -> None:
    agent = get(_REPO_ROOT, "idea-os-scribe-01")
    assert agent is not None
    assert agent["name"] == "Session Scribe"


def test_get_scribe_correct_role() -> None:
    agent = get(_REPO_ROOT, "idea-os-scribe-01")
    assert agent is not None
    assert agent["role"] == "scribe"


def test_get_formatter_correct_name() -> None:
    agent = get(_REPO_ROOT, "idea-os-formatter-01")
    assert agent is not None
    assert agent["name"] == "Org Schema Formatter"


def test_get_dispatcher_correct_trigger() -> None:
    agent = get(_REPO_ROOT, "idea-os-dispatcher-01")
    assert agent is not None
    assert "!dispatch" in agent["trigger"]


def test_get_unknown_id_returns_none(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    assert get(tmp_path, "nonexistent-agent") is None


def test_get_unknown_id_no_crash(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    result = get(tmp_path, "ghost")
    assert result is None


# ---------------------------------------------------------------------------
# add()
# ---------------------------------------------------------------------------


def test_add_valid_agent_appended(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    add(tmp_path, _VALID_AGENT)
    agents = load(tmp_path)
    assert any(a["id"] == "test-agent-01" for a in agents)


def test_add_increases_count(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[{**_VALID_AGENT, "id": "existing-01"}])
    before = len(load(tmp_path))
    add(tmp_path, _VALID_AGENT)
    assert len(load(tmp_path)) == before + 1


def test_add_all_fields_persisted(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    add(tmp_path, _VALID_AGENT)
    agent = get(tmp_path, "test-agent-01")
    assert agent is not None
    for field in REQUIRED_FIELDS:
        assert field in agent


def test_add_missing_required_field_raises(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    bad = {k: v for k, v in _VALID_AGENT.items() if k != "role"}
    with pytest.raises(ValueError):
        add(tmp_path, bad)


def test_add_missing_field_file_not_modified(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    path = tmp_path / REGISTRY_RELPATH
    mtime_before = path.stat().st_mtime
    bad = {k: v for k, v in _VALID_AGENT.items() if k != "status"}
    with pytest.raises(ValueError):
        add(tmp_path, bad)
    assert path.stat().st_mtime == mtime_before


def test_add_missing_field_error_names_field(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    bad = {k: v for k, v in _VALID_AGENT.items() if k != "trigger"}
    with pytest.raises(ValueError, match="trigger"):
        add(tmp_path, bad)


def test_add_duplicate_id_raises(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    add(tmp_path, _VALID_AGENT)
    with pytest.raises(ValueError):
        add(tmp_path, _VALID_AGENT)


def test_add_duplicate_id_file_not_modified(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    add(tmp_path, _VALID_AGENT)
    path = tmp_path / REGISTRY_RELPATH
    mtime_before = path.stat().st_mtime
    with pytest.raises(ValueError):
        add(tmp_path, _VALID_AGENT)
    assert path.stat().st_mtime == mtime_before


def test_add_duplicate_id_count_unchanged(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    add(tmp_path, _VALID_AGENT)
    before = len(load(tmp_path))
    with pytest.raises(ValueError):
        add(tmp_path, _VALID_AGENT)
    assert len(load(tmp_path)) == before


def test_add_creates_registry_dir_if_absent(tmp_path: Path) -> None:
    # No context/agents/ directory yet
    add(tmp_path, _VALID_AGENT)
    assert (tmp_path / REGISTRY_RELPATH).exists()


def test_add_atomic_write_leaves_no_tmp_file(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    add(tmp_path, _VALID_AGENT)
    tmp = (tmp_path / REGISTRY_RELPATH).with_suffix(".tmp")
    assert not tmp.exists()


# ---------------------------------------------------------------------------
# update_status()
# ---------------------------------------------------------------------------


def test_update_status_persists(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_VALID_AGENT)])
    update_status(tmp_path, "test-agent-01", "stopped")
    agent = get(tmp_path, "test-agent-01")
    assert agent is not None
    assert agent["status"] == "stopped"


def test_update_status_live_to_stopped(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[{**_VALID_AGENT, "status": "live"}])
    update_status(tmp_path, "test-agent-01", "stopped")
    assert get(tmp_path, "test-agent-01")["status"] == "stopped"


def test_update_status_stopped_to_live(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[{**_VALID_AGENT, "status": "stopped"}])
    update_status(tmp_path, "test-agent-01", "live")
    assert get(tmp_path, "test-agent-01")["status"] == "live"


def test_update_status_unknown_id_raises(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    with pytest.raises(ValueError):
        update_status(tmp_path, "ghost-agent", "live")


def test_update_status_unknown_id_error_names_id(tmp_path: Path) -> None:
    _make_registry(tmp_path)
    with pytest.raises(ValueError, match="ghost-agent"):
        update_status(tmp_path, "ghost-agent", "live")


def test_update_status_only_updates_target(tmp_path: Path) -> None:
    other = {**_VALID_AGENT, "id": "other-01", "status": "live"}
    _make_registry(tmp_path, agents=[dict(_VALID_AGENT), other])
    update_status(tmp_path, "test-agent-01", "error")
    assert get(tmp_path, "other-01")["status"] == "live"


def test_update_status_atomic_no_tmp_file(tmp_path: Path) -> None:
    _make_registry(tmp_path, agents=[dict(_VALID_AGENT)])
    update_status(tmp_path, "test-agent-01", "error")
    tmp = (tmp_path / REGISTRY_RELPATH).with_suffix(".tmp")
    assert not tmp.exists()
