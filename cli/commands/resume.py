"""Resume command: read HANDOFF.json and print a formatted session context block.

WHY THIS EXISTS:
    Starting a new AI session mid-brick requires the builder to re-establish
    context: which branch, which brick, which step, and what is next. Without
    this command, every session restart requires manually reading HANDOFF.json
    and state.json and mentally assembling that context. The formatted block
    produced here is designed to be pasted directly into an AI conversation
    as the first message, giving the builder a complete picture in one read.

DESIGN DECISIONS:
- Print a warning (not exit 1) when the current branch does not match the
  handoff branch. Alternative was exiting 1 on mismatch. Rejected because a
  branch mismatch is common during debugging or manual git operations — the
  user deserves to see the handoff context even when they are on the wrong
  branch, so they can decide whether to switch.
- Validate that all required fields are present in HANDOFF.json before
  formatting. Alternative was using .get() with fallback strings. Rejected
  because a corrupt HANDOFF.json (missing fields) would produce a formatted
  block with silent empty values, which is harder to debug than an explicit
  "missing field" error.
- Use a fixed-width separator line (38 characters) for the output block.
  Alternative was a dynamic separator based on terminal width. Rejected
  because the separator is primarily used when the output is pasted into a
  chat window, where terminal width is irrelevant.
"""

from __future__ import annotations

import json
import subprocess as _subprocess
from pathlib import Path
from typing import Any

import typer

# Relative path to HANDOFF.json from the repo root.
HANDOFF_RELPATH = "HANDOFF.json"

# All keys that must be present in HANDOFF.json for the resume block to be
# meaningful. Missing any of these would produce a confusing partial block.
_REQUIRED_FIELDS = (
    "project",
    "brick",
    "brick_name",
    "last_action",
    "loop_count",
    "current_branch",
    "timestamp",
    "next_command",
)

# Separator line used to visually bound the resume block.
# 38 characters chosen so the block fits comfortably in an 80-column terminal.
_RULE = "━" * 38


def _get_current_branch(root: Path) -> str | None:
    """Return the current git branch name, or None if git fails or is absent.

    Why it exists: The resume command compares the current branch against the
    branch recorded in HANDOFF.json to detect a mismatch. Without this check,
    a developer who switched branches manually between sessions would see
    a resume block pointing at the wrong branch with no warning.

    Args:
        root: Repo root directory used as the git working directory.

    Returns:
        Current branch name string, or None if git is not installed
        (FileNotFoundError) or returns a non-zero exit code.
    """
    try:
        proc = _subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(root),
            stdout=_subprocess.PIPE,
            stderr=_subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # git is not on PATH — return None so the branch-mismatch check is
        # skipped rather than raising an unhandled traceback.
        return None
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def _format_block(h: dict[str, Any]) -> str:
    """Format the handoff dict into the resume context block string.

    Why it exists: Keeping the format in one place means changing the visual
    layout only requires editing this function, not hunting for f-strings
    across run_resume.

    Args:
        h: Handoff dict with all _REQUIRED_FIELDS present.

    Returns:
        Multi-line string with separator lines and labelled fields, ending
        without a trailing newline (typer.echo adds one).
    """
    lines = [
        _RULE,
        "RESUMING SESSION",
        _RULE,
        f"Project:      {h['project']}",
        f"Branch:       {h['current_branch']}",
        f"Brick:        {h['brick']} — {h['brick_name']}",
        f"Last action:  {h['last_action']}",
        f"Loop count:   {h['loop_count']}",
        f"Paused at:    {h['timestamp']}",
        _RULE,
        f"Next command: {h['next_command']}",
        _RULE,
    ]
    return "\n".join(lines)


def run_resume(root: Path) -> int:
    """Read HANDOFF.json and print a formatted session context block.

    Validates all required fields before formatting. Emits a non-fatal
    warning if the current git branch does not match the handoff branch.

    Why it exists: See module docstring.

    Args:
        root: Repo root directory (contains HANDOFF.json when present).

    Returns:
        0 on success. 1 if HANDOFF.json is missing, malformed, or missing
        any required field.
    """
    handoff_path = root / HANDOFF_RELPATH

    if not handoff_path.exists():
        # Not an error state — the user may not have paused the previous
        # session. Direct them to the command they need.
        typer.echo(
            "No session to resume. Run bricklayer pause first.", err=True
        )
        return 1

    try:
        handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: HANDOFF.json is malformed — {exc}", err=True)
        return 1

    # Validate all required fields before formatting to avoid a partial block
    # with silent empty values.
    for field in _REQUIRED_FIELDS:
        if field not in handoff:
            typer.echo(
                f"error: HANDOFF.json is missing required field '{field}'", err=True
            )
            return 1

    typer.echo(_format_block(handoff))

    # Branch mismatch check — non-fatal because the user may have switched
    # branches intentionally (e.g. to investigate an issue) and still needs
    # to see the handoff context.
    expected = handoff["current_branch"]
    current = _get_current_branch(root)
    if current is not None and current != expected:
        typer.echo(
            f"Warning: you are on {current} but session was paused on {expected}."
            f" Switch with: git checkout {expected}"
        )

    return 0
