"""state.json reader/writer with schema enforcement.

WHY THIS EXISTS:
    state.json is the single source of truth for pipeline progress. Without a
    dedicated module that validates every read and write against a schema,
    individual commands could write partial or incorrectly-typed fields and
    corrupt the pipeline state silently. A corrupt state.json would then
    produce confusing errors at a completely different command — not the one
    that caused the corruption. This module acts as a schema checkpoint:
    nothing enters or leaves state.json without passing validation.

DESIGN DECISIONS:
- Deep-merge updates rather than full-replace on write. Alternative was to
  require callers to supply the complete state dict every time. Rejected
  because commands only know their own fields; forcing them to read and
  re-supply every unrelated field means every command must understand the
  entire state schema, and any command that misses a field silently deletes
  it.
- Validate the merged result before writing, not just the update dict.
  Alternative was validating only the incoming ``updates`` dict. Rejected
  because a partial update can invalidate the merged result even when the
  update dict itself looks fine (e.g. setting loop_count to a string that
  was already present in the base).
- Atomic write via .tmp + rename for the final file write. Alternative was
  a direct Path.write_text() call. Rejected because a process crash or
  KeyboardInterrupt mid-write leaves a half-written JSON file that fails
  to parse on the next command, breaking the entire pipeline until the
  file is repaired manually. Path.rename() is atomic on POSIX when both
  paths are on the same filesystem.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Required top-level fields and their expected Python types.
# Any field NOT in this dict is treated as an extra (e.g. current_feature)
# and is preserved through merge without type-checking — this lets Brick 14's
# three-level branch tracking coexist with the original schema.
_TOP_LEVEL_SCHEMA: dict[str, type | tuple[type, ...]] = {
    "current_brick": str,
    "status": str,
    "loop_count": int,
    "last_gate_failed": (str, type(None)),
    "completed_bricks": list,
    "next_action": str,
    "last_test_run": dict,
}

# Required fields inside last_test_run — validated separately because
# last_test_run is itself a nested dict within the top-level schema.
_TEST_RUN_SCHEMA: dict[str, type | tuple[type, ...]] = {
    "command": str,
    "status": str,
    "exit_code": int,
    "artifact": str,
}


def _validate(data: dict[str, Any]) -> None:
    """Raise ValueError if data does not satisfy the state schema.

    Why it exists: Prevents malformed state from ever reaching disk. Without
    this gate, a typo in any command's state_write() call would silently
    corrupt the pipeline — the error would only surface at a later command
    that reads the wrong field type.

    Args:
        data: Merged state dict to validate.

    Raises:
        ValueError: If any required field is missing or has the wrong type.
    """
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
    """Load and validate state.json, returning the parsed dict.

    Why it exists: A raw json.loads() call gives no guidance when the file is
    missing or malformed. This wrapper surfaces a clear exception with the
    full path so callers can produce a targeted error message.

    Args:
        path: Absolute or relative path to state.json.

    Returns:
        Validated state dict with all required fields present and correctly
        typed.

    Raises:
        FileNotFoundError: If the file does not exist at ``path``.
        ValueError: If any required field is missing or has the wrong type.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    p = Path(path)
    if not p.exists():
        # Raise before read_text() so the error message names the intended
        # path rather than surfacing a lower-level OSError.
        raise FileNotFoundError(f"state.json not found at: {p}")
    data: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    _validate(data)
    return data


def _deep_merge(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge updates into base; nested dicts are merged, not replaced.

    Why it exists: A shallow dict.update() would replace the entire
    last_test_run dict when a command only needs to update one field inside
    it (e.g. exit_code). Deep merge lets commands write surgical updates
    without knowing or supplying unrelated sibling keys.

    Args:
        base: The existing state dict (read from disk).
        updates: The partial dict of changes to apply.

    Returns:
        New dict combining both, with nested dicts recursively merged.
        Neither argument is modified.
    """
    result = dict(base)
    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Both sides are dicts — recurse so inner keys are merged rather
            # than the inner dict being wholesale replaced.
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def write(path: Path | str, updates: dict[str, Any]) -> None:
    """Deep-merge updates into state.json, validate, and persist atomically.

    Why it exists: Commands need to update individual fields without knowing
    the full state schema. This function handles read-merge-validate-write as
    one atomic operation so the file on disk is never left in a partial state.

    Args:
        path: Path to state.json. The file is created if it does not exist,
              but the merged result must still pass schema validation.
        updates: Partial dict of fields to update. Nested dicts are merged
                 rather than replaced (see _deep_merge).

    Raises:
        ValueError: If the merged result fails schema validation.
        json.JSONDecodeError: If the existing file content is not valid JSON.
    """
    p = Path(path)
    if p.exists():
        existing: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    else:
        existing = {}
    merged = _deep_merge(existing, updates)

    # Validate before touching disk — fail fast rather than writing a corrupt
    # file that will cause a confusing error on the next command.
    _validate(merged)

    # Atomic write: write to a sibling .tmp file first, then rename into place.
    # Path.rename() is atomic on POSIX when src and dst are on the same
    # filesystem — a crash between write_text and rename leaves the .tmp
    # file behind (harmless) rather than a half-written state.json
    # (pipeline-breaking).
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    tmp.rename(p)
