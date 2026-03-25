"""Agent registry: read and write context/agents/registry.yaml.

WHY THIS EXISTS:
    Phase 6 introduces a managed agent layer. Every agent in the system needs
    a canonical record — its ID, runtime, status, trigger, and location — so
    that CLI commands (agent list, agent new, agent deploy) have a single source
    of truth to read from and write to. Without this module, each command would
    parse the YAML itself, duplicating logic and diverging over time. This module
    owns all reads and writes to registry.yaml.

DESIGN DECISIONS:
- All four public functions take ``root`` (repo root Path) rather than a
  registry path. Alternative was accepting the path directly. Rejected because
  callers (CLI commands) know the repo root, not the registry path; centralising
  the path derivation here means only this module needs updating if the location
  changes.
- load() returns [] for a missing registry file rather than raising. Alternative
  was raising FileNotFoundError. Rejected because a missing registry is a valid
  initial state (registry not yet created); callers should not need try/except
  just to handle the empty case.
- load() raises ValueError for malformed YAML rather than returning []. Alternative
  was returning [] silently. Rejected because malformed YAML is a user error that
  should surface explicitly — silently returning an empty list would cause add()
  and get() to behave as if the registry is empty, destroying existing data on
  the next write.
- add() and update_status() write atomically using tmp-file + rename. Alternative
  was writing directly. Rejected for the same reason as state.py: a crash or
  interrupt mid-write must not corrupt the registry.
- Required fields are enforced as a frozenset constant so the validation list
  is visible at module level and easy to extend without touching function bodies.
- Duplicate ID detection in add() prevents silent overwrites. Alternative was
  allowing duplicate IDs (last-write wins). Rejected because a duplicate ID
  makes get() non-deterministic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Path from repo root to the registry file.
REGISTRY_RELPATH = Path("context") / "agents" / "registry.yaml"

# Fields every agent entry must have.
REQUIRED_FIELDS: frozenset[str] = frozenset({
    "id", "name", "project", "role", "runtime", "status", "trigger", "location"
})


def _registry_path(root: Path) -> Path:
    return root / REGISTRY_RELPATH


def _read_raw(root: Path) -> dict[str, Any]:
    """Read and parse registry.yaml, returning the raw dict.

    Why it exists: Both load() and the write helpers need the full document
    (not just the agents list) so that non-agents keys are preserved on write.

    Returns:
        Parsed YAML dict (may have an "agents" key with a list, or be empty).

    Raises:
        ValueError: If the file exists but cannot be parsed as valid YAML.
    """
    path = _registry_path(root)
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"registry.yaml is malformed — {exc}") from exc


def _write_atomic(root: Path, data: dict[str, Any]) -> None:
    """Write registry data atomically using a temp file and rename.

    Why it exists: A crash mid-write must not leave registry.yaml half-written.
    The rename is atomic on POSIX systems; on Windows it is the closest
    equivalent available without a third-party library.

    Args:
        root: Repo root directory.
        data: Full registry dict to serialise and write.
    """
    path = _registry_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True), encoding="utf-8")
    tmp.rename(path)


def load(root: Path) -> list[dict[str, Any]]:
    """Return all agents from registry.yaml as a list of dicts.

    Args:
        root: Repo root directory.

    Returns:
        List of agent dicts. Empty list if registry.yaml does not exist.

    Raises:
        ValueError: If registry.yaml exists but cannot be parsed.
    """
    data = _read_raw(root)
    agents = data.get("agents") or []
    return list(agents)


def get(root: Path, agent_id: str) -> dict[str, Any] | None:
    """Return a single agent dict by ID, or None if not found.

    Args:
        root: Repo root directory.
        agent_id: The ``id`` field value to look up.

    Returns:
        Agent dict, or None if no agent with that ID exists.

    Raises:
        ValueError: If registry.yaml is malformed.
    """
    for agent in load(root):
        if agent.get("id") == agent_id:
            return agent
    return None


def add(root: Path, agent: dict[str, Any]) -> None:
    """Append a new agent to the registry.

    Validates required fields and checks for duplicate IDs before writing.

    Args:
        root: Repo root directory.
        agent: Dict representing the new agent. Must contain all REQUIRED_FIELDS.

    Raises:
        ValueError: If any required field is missing, or if the agent ID already
                    exists in the registry. The registry file is not modified on
                    either error.
    """
    # Validate required fields before any read/write.
    missing = REQUIRED_FIELDS - set(agent.keys())
    if missing:
        raise ValueError(
            f"Agent is missing required fields: {', '.join(sorted(missing))}"
        )

    data = _read_raw(root)
    agents: list[dict[str, Any]] = list(data.get("agents") or [])

    # Duplicate ID check.
    new_id = agent["id"]
    for existing in agents:
        if existing.get("id") == new_id:
            raise ValueError(f"Agent with id '{new_id}' already exists in registry")

    agents.append(agent)
    data["agents"] = agents
    _write_atomic(root, data)


def update_status(root: Path, agent_id: str, status: str) -> None:
    """Update the status field of an existing agent.

    Args:
        root: Repo root directory.
        agent_id: ID of the agent to update.
        status: New status string (e.g. "live", "stopped", "error").

    Raises:
        ValueError: If no agent with agent_id exists. The registry file is not
                    modified.
    """
    data = _read_raw(root)
    agents: list[dict[str, Any]] = list(data.get("agents") or [])

    for agent in agents:
        if agent.get("id") == agent_id:
            agent["status"] = status
            data["agents"] = agents
            _write_atomic(root, data)
            return

    raise ValueError(f"Agent '{agent_id}' not found in registry")
