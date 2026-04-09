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

import os
import sys
import tempfile
from pathlib import Path
from typing import Any

import typer
import yaml

YAML_FILENAME = "bricklayer.yaml"


def _load_dotenv(directory: Path) -> None:
    """Load a .env file from directory into os.environ (non-overwriting).

    Why it exists: API keys and secrets are stored in .env files at the
    project root. Without auto-loading, every developer must manually source
    .env before running bricklayer close-session — a step that is easy to
    forget and produces confusing "API key not set" errors. Auto-loading at
    startup makes the experience seamless without requiring python-dotenv.

    Rules:
    - .env absent → silent skip, no error.
    - Blank lines and lines starting with ``#`` → silently skipped.
    - Lines without ``=`` → skipped with a warning to stderr; remaining lines
      still load. This prevents a single typo from silently breaking all vars.
    - Surrounding single or double quotes stripped from values.
    - Existing os.environ keys are NOT overwritten — the shell always wins.

    Args:
        directory: Directory to look for a ``.env`` file in. Typically the
                   directory that contains bricklayer.yaml.
    """
    env_path = directory / ".env"
    if not env_path.exists():
        return
    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            typer.echo(
                f"warning: .env line {i} malformed (no '='), skipping: {stripped!r}",
                err=True,
            )
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip()
        # Strip surrounding matching quotes (e.g. KEY="value" or KEY='value').
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


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


def _write_context_txt(root: Path, config: dict[str, Any]) -> None:
    """Write bricklayer/context.txt from the test: section of bricklayer.yaml.

    WHY THIS EXISTS:
        context.txt stores LANGUAGE and TEST_COMMAND so bricklayer build tools
        know how to run the test suite without hard-coding anything. Before this
        function existed, context.txt was edited by hand, which meant it would
        silently drift whenever someone changed test.command in bricklayer.yaml
        without remembering to also update context.txt. Writing it automatically
        on every startup means the two can never diverge.

    Rules:
    - test: section absent → warning to stderr, return without touching context.txt.
    - test.command absent → exit 1 with a clear error message.
    - bricklayer/ directory absent → create it before writing.
    - Write is atomic: content goes to a tempfile in the same directory, then
      os.replace() swaps it in. Prevents a partial write from leaving a
      truncated context.txt if the process is interrupted mid-write.

    Args:
        root: Project root (directory that contains bricklayer.yaml).
        config: Parsed bricklayer.yaml config dict (already validated).
    """
    test_section = config.get("test")
    if test_section is None:
        typer.echo(
            "warning: no test: section in bricklayer.yaml — context.txt not updated",
            err=True,
        )
        return

    command: str | None = test_section.get("command") if isinstance(test_section, dict) else None
    if not command:
        typer.echo(
            "error: test: section is missing required field 'command'",
            err=True,
        )
        sys.exit(1)

    language: str = (
        test_section.get("language", "Python")
        if isinstance(test_section, dict)
        else "Python"
    )

    context_dir = root / "bricklayer"
    context_dir.mkdir(parents=True, exist_ok=True)
    context_path = context_dir / "context.txt"

    content = f"LANGUAGE: {language}\nTEST_COMMAND: {command}\n"

    # Atomic write: write to a tempfile in the same directory, then rename.
    # Same-directory tempfile ensures os.replace is a rename, not a cross-device copy.
    fd, tmp_path_str = tempfile.mkstemp(dir=context_dir, prefix=".context_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_path_str, context_path)
    except Exception:
        # Clean up the tempfile if anything went wrong before the rename.
        try:
            os.unlink(tmp_path_str)
        except OSError:
            pass
        raise


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

    # Load .env before path validation so secrets (e.g. GROQ_API_KEY) are
    # available immediately for any command that runs after startup.
    _load_dotenv(yaml_path.parent)

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
            rel_path = os.path.expandvars(rel_path)
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

    _write_context_txt(base, config)

    return config
