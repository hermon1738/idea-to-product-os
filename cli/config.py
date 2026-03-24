"""YAML loader and path validation for bricklayer.yaml.

WHY THIS EXISTS:
    Every bricklayer command needs the project root and the paths to pipeline
    tools before it can do anything useful. Without a single, shared loader
    that walks upward from the current directory, every command would
    duplicate the traversal logic, and any inconsistency between copies would
    produce different error messages for the same root cause. This module
    provides one function that any command calls to get a fully-validated
    config dict.

DESIGN DECISIONS:
- Walk upward to find bricklayer.yaml rather than requiring cwd == repo root.
  Alternative was to hard-require the user to cd to the repo root first.
  Rejected because developers constantly invoke CLI tools from subdirectories;
  forcing root-only use is a UX failure that defeats the purpose of a CLI.
- Validate all declared paths at startup and exit 1 immediately if any are
  missing. Alternative was lazy validation (validate only when a command
  actually uses that path). Rejected because lazy validation means a typo in
  bricklayer.yaml only surfaces mid-command, potentially after irreversible
  side effects (file writes, git commits) have already run.
- Use typer.echo(err=True) for all error output so messages go to stderr.
  Alternative was print() (stdout). Rejected because POSIX convention and CI
  pipelines monitor stderr for failures; printing errors to stdout means
  automated tools that capture stdout (e.g. ``bricklayer run | jq``) would
  silently mix error messages into the data stream.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import typer
import yaml

YAML_FILENAME = "bricklayer.yaml"


def find_yaml(start: Path | None = None) -> Path | None:
    """Walk upward from start until bricklayer.yaml is found.

    Why it exists: Commands need the repo root to resolve relative tool paths.
    Without upward traversal, the user must always invoke bricklayer from the
    exact directory containing bricklayer.yaml — an unreliable assumption.

    Args:
        start: Directory to begin the search. Defaults to cwd if None.

    Returns:
        Absolute Path to the first bricklayer.yaml found, or None if the
        filesystem root is reached without finding it.
    """
    current = (start or Path.cwd()).resolve()
    while True:
        candidate = current / YAML_FILENAME
        if candidate.exists():
            return candidate
        parent = current.parent
        # Reaching filesystem root means parent == current; stop to avoid
        # an infinite loop on POSIX where "/" is its own parent.
        if parent == current:
            return None
        current = parent


def load_and_validate(yaml_path: Path | None = None) -> dict[str, Any]:
    """Load bricklayer.yaml, resolve all declared paths, exit 1 on any failure.

    Why it exists: Every command needs a validated config dict before running.
    Without this function, missing tool paths would only surface mid-command,
    after side effects (commits, merges) may have already occurred.

    Args:
        yaml_path: Explicit path to bricklayer.yaml. If None, find_yaml()
                   is used to discover it by walking upward from cwd.

    Returns:
        Parsed config dict. All declared paths in phases/tools/agents are
        guaranteed to exist on disk.

    Raises:
        SystemExit(1): If yaml_path is None/missing, YAML cannot be parsed,
                       or any declared path does not exist.
    """
    if yaml_path is None:
        yaml_path = find_yaml()

    if yaml_path is None or not yaml_path.exists():
        typer.echo("bricklayer.yaml not found at repo root", err=True)
        sys.exit(1)

    try:
        raw = yaml_path.read_text(encoding="utf-8")
        config: dict[str, Any] = yaml.safe_load(raw) or {}
    except (yaml.YAMLError, OSError) as exc:
        # YAMLError covers parse failures; OSError covers permission/IO errors.
        typer.echo(f"bricklayer.yaml could not be parsed: {exc}", err=True)
        sys.exit(1)

    base = yaml_path.parent
    missing: list[str] = []

    for section_key in ("phases", "tools", "agents"):
        section = config.get(section_key) or {}
        if not isinstance(section, dict):
            # Non-dict section values (e.g. a scalar) cannot contain path
            # entries; skip rather than crash with an AttributeError.
            continue
        for _name, rel_path in section.items():
            if rel_path is None:
                # Explicit null in YAML means "not configured"; skip.
                continue
            p = Path(rel_path)
            if not p.is_absolute():
                # Relative paths are resolved against the YAML file's directory,
                # not cwd, so the config works regardless of where bricklayer
                # is invoked from.
                p = base / p
            if not p.exists():
                missing.append(str(rel_path))

    if missing:
        # Report ALL missing paths before exiting — the user should not need to
        # run the command N times to discover N missing files one at a time.
        for m in missing:
            typer.echo(f"Missing: {m} — check bricklayer.yaml", err=True)
        sys.exit(1)

    return config
