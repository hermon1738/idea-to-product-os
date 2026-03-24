"""state.json reader/writer with schema enforcement."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Required top-level fields and their expected Python types
_TOP_LEVEL_SCHEMA: dict[str, type | tuple[type, ...]] = {
    "current_brick": str,
    "status": str,
    "loop_count": int,
    "last_gate_failed": (str, type(None)),
    "completed_bricks": list,
    "next_action": str,
    "last_test_run": dict,
}

# Required fields inside last_test_run
_TEST_RUN_SCHEMA: dict[str, type | tuple[type, ...]] = {
    "command": str,
    "status": str,
    "exit_code": int,
    "artifact": str,
}


def _validate(data: dict[str, Any]) -> None:
    """Raise ValueError if data does not satisfy the state schema."""
    for field, expected_type in _TOP_LEVEL_SCHEMA.items():
        if field not in data:
            raise ValueError(f"state.json missing required field: '{field}'")
        if not isinstance(data[field], expected_type):
            actual = type(data[field]).__name__
            if isinstance(expected_type, tuple):
                expected_name = " | ".join(t.__name__ for t in expected_type)
            else:
                expected_name = expected_type.__name__
            raise ValueError(
                f"state.json field '{field}' must be {expected_name}, got {actual}"
            )

    test_run = data.get("last_test_run", {})
    if isinstance(test_run, dict):
        for field, expected_type in _TEST_RUN_SCHEMA.items():
            if field not in test_run:
                raise ValueError(
                    f"state.json last_test_run missing required field: '{field}'"
                )
            if not isinstance(test_run[field], expected_type):
                actual = type(test_run[field]).__name__
                if isinstance(expected_type, tuple):
                    expected_name = " | ".join(t.__name__ for t in expected_type)
                else:
                    expected_name = expected_type.__name__
                raise ValueError(
                    f"state.json last_test_run.'{field}' must be {expected_name}, got {actual}"
                )


def load(path: Path | str) -> dict[str, Any]:
    """Load and validate state.json. Raises FileNotFoundError or ValueError on failure."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"state.json not found at: {p}")
    data: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    _validate(data)
    return data


def _deep_merge(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge updates into base. Nested dicts are merged, not replaced."""
    result = dict(base)
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def write(path: Path | str, updates: dict[str, Any]) -> None:
    """Deep-merge updates into state.json and persist. Validates schema before writing."""
    p = Path(path)
    if p.exists():
        existing: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    else:
        existing = {}
    merged = _deep_merge(existing, updates)
    _validate(merged)
    p.write_text(json.dumps(merged, indent=2), encoding="utf-8")
