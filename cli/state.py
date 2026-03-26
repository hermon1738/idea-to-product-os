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
- Auto-create state.json with safe defaults when the file is missing but
  its parent directory exists. Alternative was raising FileNotFoundError and
  requiring the user to manually bootstrap state.json before using any
  command. Rejected because fresh-repo users (who copy only bricklayer.yaml)
  hit an immediate hard failure on every command. The auto-create prints a
  visible stderr warning so the creation is never silent (Brick 26, D-038).
"""

from __future__ import annotations

import json
import sys
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

# Default last_test_run dict used when auto-creating state.json on a fresh
# repo. All required fields from _TEST_RUN_SCHEMA are present with zero-value
# strings so the merged state passes schema validation immediately.
_DEFAULT_LAST_TEST_RUN: dict[str, str | int] = {
    "command": "",
    "status": "",
    "exit_code": 0,
    "artifact": "",
}


def _make_default_state(state_path: Path) -> dict[str, Any]:
    """Build a valid default state dict for a fresh project.

    Why it exists: When state.json is missing, load() needs a complete,
    schema-valid dict to write to disk and return. Inlining the defaults
    inside load() would make the function body hard to test in isolation —
    factoring into a named helper lets tests assert exact field values without
    triggering file I/O.

    The project name is derived from the directory two levels above the given
    path (i.e. ``path.parent.parent.name``) because state.json always lives at
    ``<repo-root>/bricklayer/state.json``. Climbing two levels yields the repo
    root directory name, which is the most meaningful project identifier
    available without reading bricklayer.yaml.

    Args:
        state_path: Absolute path to the state.json file that will be created.
            Used only to derive the project name; the file is not read.

    Returns:
        Dict containing every required schema field with safe zero-value
        defaults. Passes _validate() without modification.
    """
    # Derive project name from repo root directory (two levels above
    # bricklayer/state.json). Falls back to the immediate parent name if the
    # path has fewer than two parent levels (e.g. in isolated test scenarios).
    repo_root = state_path.parent.parent
    project_name: str = repo_root.name if repo_root.name else state_path.parent.name

    return {
        "project": project_name,
        "current_brick": "",
        "status": "",
        "last_action": "",
        "loop_count": 0,
        "last_gate_failed": None,
        "completed_bricks": [],
        "next_action": "",
        "current_branch": "main",
        "current_feature": None,
        "current_phase": None,
        "last_test_run": dict(_DEFAULT_LAST_TEST_RUN),
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
    """Load and validate state.json, auto-creating it with defaults if missing.

    Why it exists: A raw json.loads() call gives no guidance when the file is
    missing or malformed. This wrapper surfaces a clear exception with the full
    path, and — when the parent directory exists — auto-creates state.json
    with safe defaults so that ``bricklayer status`` works immediately on a
    fresh project that only has bricklayer.yaml (Brick 26 fix).

    Auto-create only triggers when the parent directory exists. If both the
    file and its parent are absent, FileNotFoundError is raised so callers
    learn about genuinely bad paths rather than silently creating nested dirs.

    Args:
        path: Absolute or relative path to state.json.

    Returns:
        Validated state dict with all required fields present and correctly
        typed. On auto-create the returned dict reflects the written defaults.

    Raises:
        FileNotFoundError: If the file and its parent directory do not exist.
        ValueError: If any required field is missing or has the wrong type.
        json.JSONDecodeError: If the file content is not valid JSON.
    """
    p = Path(path)
    if not p.exists():
        if not p.parent.exists():
            # Parent directory missing — cannot auto-create. Raise before
            # read_text() so the error message names the intended path rather
            # than surfacing a lower-level OSError from the OS.
            p.parent.mkdir(parents=True, exist_ok=True)

        # Parent directory exists but state.json is absent — this is a fresh
        # project that only has bricklayer.yaml. Build and persist safe
        # defaults so every subsequent command can run without manual setup.
        default_state = _make_default_state(p)
        _validate(default_state)  # guard: defaults must always be schema-valid

        # Atomic write so a crash here never leaves a half-written file.
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(default_state, indent=2), encoding="utf-8")
        tmp.rename(p)

        # Warn to stderr — auto-create must never be silent. The user should
        # know a new state.json was created so they can verify the defaults.
        print(
            f"state.json not found — created with defaults at {p}",
            file=sys.stderr,
        )
        return default_state

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
