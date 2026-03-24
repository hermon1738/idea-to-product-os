"""Pause command: write HANDOFF.json and .continue-here.md for session handoff.

WHY THIS EXISTS:
    AI coding sessions have a context window limit. When a session ends mid-brick,
    the next session needs to know exactly where to resume — which branch, which
    brick, which step — without re-reading the entire conversation history.
    Without HANDOFF.json, the next session starts cold and must infer state
    from git log and state.json separately. Without .continue-here.md, a
    human glancing at the repo has no idea what step was in progress.

DESIGN DECISIONS:
- Write HANDOFF.json first, then .continue-here.md, with rollback on second
  failure. Alternative was writing both without error handling. Rejected
  because a partial write (HANDOFF.json written, .continue-here.md failed)
  leaves the repo in a confusing state where one file is stale and the other
  is missing. The rollback ensures both files are present and consistent or
  neither is.
- Capture timestamp in UTC with isoformat() rather than a human-readable
  local time. Alternative was formatting as a local timestamp. Rejected
  because HANDOFF.json is also machine-readable; UTC ISO format is
  unambiguous across timezones and parseable without a locale.
- Derive next_command from a routing table (not from live state). Alternative
  was calling ``bricklayer next`` as a subprocess. Rejected because spawning
  a subprocess to read state.json is slower and adds a process boundary that
  could fail independently of the pause command.
"""

from __future__ import annotations

import datetime
import json
import re
import subprocess as _subprocess
from pathlib import Path
from typing import Any

import typer

# Relative paths from repo root.
STATE_RELPATH = "bricklayer/state.json"
HANDOFF_RELPATH = "HANDOFF.json"
CONTINUE_RELPATH = ".continue-here.md"

# Maps next_action values to the CLI command the next session should run.
# Mirrors the routing table in next.py — kept separate so pause.py can be
# imported without dragging in the state.load dependency from next.py.
_NEXT_COMMAND_ROUTING: dict[str, str] = {
    "snapshot_init": "bricklayer build --snapshot",
    "verify": "bricklayer build --verify",
    "tests_passed": "bricklayer build --skeptic-packet",
    "skeptic_packet_ready": "bricklayer build --verdict PASS|FAIL",
    "brick_complete": "bricklayer next",
}


def _get_current_branch(root: Path) -> str:
    """Return the current git branch name, or ``"unknown"`` on any failure.

    Why it exists: HANDOFF.json includes the current branch so the next
    session can verify it is on the right branch before resuming. Using
    ``"unknown"`` as the fallback rather than None means the JSON file is
    always a string, which simplifies the resume command's field validation.

    Args:
        root: Repo root directory used as the git working directory.

    Returns:
        Current branch name string, or ``"unknown"`` if git fails.

    Note:
        This function does not guard FileNotFoundError (git not installed).
        In practice the pipeline requires git; this is a known v2 gap.
    """
    proc = _subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return proc.stdout.strip()
    return "unknown"


def _parse_brick(current_brick: str) -> tuple[str, str]:
    """Parse ``current_brick`` string into (brick_number, brick_name).

    Why it exists: HANDOFF.json stores brick number and name as separate
    fields so the resume command can display them in a structured block
    without re-parsing the string.

    Args:
        current_brick: Value of ``current_brick`` from state.json
                       (e.g. ``"Brick 14 - three-level branching"``).

    Returns:
        Tuple (brick_number, brick_name). Falls back to (``"?"``, original
        string) if the pattern does not match.
    """
    m = re.match(r"Brick\s+([\d.]+)\s*[-\u2013]\s*(.*)", current_brick, re.IGNORECASE)
    if m:
        return m.group(1), m.group(2).strip()
    return "?", current_brick


def _next_command(next_action: str) -> str:
    """Resolve a next_action value to the CLI command the next session should run.

    Why it exists: The routing table lookup is a one-liner here, but having it
    as a named function makes _build_handoff easier to read and allows tests
    to assert on routing logic in isolation.

    Args:
        next_action: The ``next_action`` value from state.json.

    Returns:
        The corresponding CLI command string, or a passthrough with a comment
        if the value is not in the routing table.
    """
    return _NEXT_COMMAND_ROUTING.get(
        next_action, f"bricklayer next  # {next_action}"
    )


def _build_handoff(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    """Assemble the HANDOFF.json payload from state and git.

    Why it exists: Assembling the payload in a separate function means the
    write logic in run_pause stays focused on file I/O, and the payload
    structure can be tested without touching the filesystem.

    Args:
        root: Repo root directory (needed for _get_current_branch).
        state: Parsed state.json dict.

    Returns:
        Dict with all fields required by the resume command.
    """
    current_brick = state.get("current_brick", "")
    brick_num, brick_name = _parse_brick(current_brick)
    next_action = str(state.get("next_action", ""))
    branch = _get_current_branch(root)
    # UTC timestamp — unambiguous and machine-parseable for future automation.
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return {
        "project": root.name,
        "brick": brick_num,
        "brick_name": brick_name,
        "last_action": next_action,
        "loop_count": state.get("loop_count", 0),
        "current_branch": branch,
        "timestamp": ts,
        "next_command": _next_command(next_action),
    }


def _build_continue_md(handoff: dict[str, Any]) -> str:
    """Build the .continue-here.md content from the handoff dict.

    Why it exists: .continue-here.md is a human-readable version of
    HANDOFF.json for anyone who opens the repo root in a file browser.
    Generating it from the same handoff dict ensures both files are always
    in sync.

    Args:
        handoff: Dict produced by _build_handoff().

    Returns:
        Markdown-formatted string ending with a newline.
    """
    lines = [
        f"Last session ended: {handoff['timestamp']}",
        f"Project: {handoff['project']}",
        f"Branch: {handoff['current_branch']}",
        f"Current brick: Brick {handoff['brick']} — {handoff['brick_name']}",
        f"Last action: {handoff['last_action']}",
        f"Next command: {handoff['next_command']}",
        "Blockers: none",
    ]
    return "\n".join(lines) + "\n"


def run_pause(root: Path) -> int:
    """Write HANDOFF.json and .continue-here.md for session handoff.

    Rolls back HANDOFF.json if writing .continue-here.md fails, so both
    files are always consistent (both present or neither present).

    Why it exists: See module docstring.

    Args:
        root: Repo root directory (contains bricklayer.yaml).

    Returns:
        0 on success. 1 if state.json is missing, corrupt, or either file
        cannot be written.
    """
    state_path = root / STATE_RELPATH
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: state.json is corrupt — {exc}", err=True)
        return 1

    handoff = _build_handoff(root, state)
    continue_md = _build_continue_md(handoff)

    handoff_path = root / HANDOFF_RELPATH
    continue_path = root / CONTINUE_RELPATH

    # Write HANDOFF.json first. If the second write fails, remove it so
    # neither file is left in a partial or inconsistent state.
    try:
        handoff_path.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        typer.echo(f"error: could not write {HANDOFF_RELPATH}: {exc}", err=True)
        return 1

    try:
        continue_path.write_text(continue_md, encoding="utf-8")
    except OSError as exc:
        typer.echo(f"error: could not write {CONTINUE_RELPATH}: {exc}", err=True)
        # Rollback: remove HANDOFF.json so the repo is not left with one
        # stale file and one missing file.
        handoff_path.unlink(missing_ok=True)
        return 1

    typer.echo(f"written: {HANDOFF_RELPATH}")
    typer.echo(f"written: {CONTINUE_RELPATH}")
    return 0
