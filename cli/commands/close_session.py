"""Close-session command: sprint review via Groq, writes session-log.md and STATE.md.

WHY THIS EXISTS:
    At the end of a working session, the developer needs a structured review
    of what was accomplished (which bricks passed, which failed, what the loop
    counts were). Without this command, that review happens in the developer's
    head — inconsistently, incompletely, and without a written record. This
    command offloads the review to a Groq LLM using the sprint-brain.md system
    prompt, then persists the output so the next session starts with a written
    summary of the previous session's outcomes.

DESIGN DECISIONS:
- Import Groq at module level rather than inside _call_groq. Alternative was
  a lazy import inside the function body. Rejected because a lazy import is
  not patchable from tests — ``from groq import Groq`` inside a function
  body cannot be intercepted by ``unittest.mock.patch``. Module-level import
  means tests can patch ``cli.commands.close_session.Groq`` directly.
- Write session-log.md first, then STATE.md; roll back session-log.md on
  STATE.md failure. Alternative was writing both without rollback. Rejected
  because a partial write (session-log written, STATE.md failed) leaves the
  repo with a session log that has no corresponding state update — the next
  session's ``bricklayer resume`` would show stale data.
- Load sprint-brain.md path from ``bricklayer.yaml phases.review`` rather than
  hardcoding the path. Alternative was a hardcoded relative path like
  ``system-prompts/sprint-brain.md``. Rejected because hardcoding couples the
  CLI to the project layout — different projects may place system prompts in
  different directories.
- Use ``except Exception as exc:`` in _call_groq rather than specific Groq
  exception types. The Groq Python SDK raises a hierarchy of exception classes
  (APIError, AuthenticationError, APITimeoutError, etc.) that are not all
  importable at the top level. Catching Exception covers all of them plus any
  network-level errors, at the cost of also catching unexpected bugs. This is
  an intentional tradeoff documented here rather than using a ``# noqa`` comment.
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any

import typer
import yaml
from groq import Groq

# Relative paths from repo root.
STATE_RELPATH = "bricklayer/state.json"
SESSION_LOG_RELPATH = "session-log.md"
STATE_MD_RELPATH = "STATE.md"

# Groq model and timeout — named constants so they are easy to find and
# change without hunting through function bodies.
GROQ_MODEL: str = "llama-3.1-8b-instant"
GROQ_TIMEOUT: float = 30.0

# Maps next_action values to CLI commands for STATE.md — mirrors the routing
# table in pause.py. Kept here rather than imported to avoid coupling
# close_session to the pause module's internals.
_NEXT_COMMAND_ROUTING: dict[str, str] = {
    "snapshot_init": "bricklayer build --snapshot",
    "verify": "bricklayer build --verify",
    "tests_passed": "bricklayer build --skeptic-packet",
    "skeptic_packet_ready": "bricklayer build --verdict PASS|FAIL",
    "brick_complete": "bricklayer next",
}


def _load_state(root: Path) -> dict[str, Any] | None:
    """Load state.json and return the parsed dict, or None on any failure.

    Why it exists: run_close_session needs early exit on state.json failure
    before invoking the Groq API — no point calling the API if the input
    data is unavailable.

    Args:
        root: Repo root directory (contains bricklayer/state.json).

    Returns:
        Parsed state dict, or None if the file is missing or corrupt (error
        message already echoed to stderr).
    """
    state_path = root / STATE_RELPATH
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return None
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: state.json is corrupt — {exc}", err=True)
        return None


def _load_sprint_brain(root: Path, yaml_path: Path) -> str | None:
    """Load the sprint-brain.md system prompt from the path declared in bricklayer.yaml.

    Why it exists: The Groq call needs a system prompt that tells the LLM how
    to conduct a sprint review. Storing the prompt path in bricklayer.yaml
    rather than hardcoding it lets projects customise the review criteria
    without modifying the CLI.

    Args:
        root: Repo root directory. Relative paths in bricklayer.yaml are
              resolved against this.
        yaml_path: Absolute path to bricklayer.yaml.

    Returns:
        The sprint-brain.md file content as a string, or None on any failure
        (error message already echoed to stderr).
    """
    try:
        config = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError) as exc:
        # YAMLError covers malformed YAML; OSError covers permission/IO errors.
        typer.echo(f"error: could not parse bricklayer.yaml — {exc}", err=True)
        return None

    phases = config.get("phases") or {}
    rel_path = phases.get("review")
    if not rel_path:
        typer.echo(
            "error: phases.review not found in bricklayer.yaml — sprint-brain.md path missing",
            err=True,
        )
        return None

    sprint_brain_path = root / rel_path
    if not sprint_brain_path.exists():
        typer.echo(
            f"error: sprint-brain.md not found at {rel_path} — check bricklayer.yaml",
            err=True,
        )
        return None

    return sprint_brain_path.read_text(encoding="utf-8")


def _build_user_message(state: dict[str, Any]) -> str:
    """Build the Groq user message from current state.json data.

    Why it exists: The LLM receives the current pipeline state as a structured
    markdown message. Without a dedicated builder, the message format could
    drift between invocations, producing inconsistent review output.

    Args:
        state: Parsed state.json dict.

    Returns:
        Markdown-formatted string summarising the current session state.
    """
    current_brick = state.get("current_brick") or "unknown"
    status = state.get("status") or "unknown"
    loop_count = state.get("loop_count", 0)
    next_action = state.get("next_action") or "unknown"
    completed = state.get("completed_bricks") or []
    last_test = state.get("last_test_run") or {}

    lines = [
        "## Session State",
        f"Current brick: {current_brick}",
        f"Status: {status}",
        f"Loop count: {loop_count}",
        f"Next action: {next_action}",
        f"Last test run: {last_test.get('status', 'N/A')}",
        "",
        "## Completed Bricks This Session",
    ]
    if completed:
        for brick in completed:
            lines.append(f"- {brick}")
    else:
        lines.append("- none recorded")

    return "\n".join(lines)


def _call_groq(api_key: str, system_prompt: str, user_message: str) -> str | None:
    """Call the Groq API and return the response text, or None on any failure.

    Why it exists: Isolating the Groq call here means tests can patch
    ``cli.commands.close_session.Groq`` at module level — the module-level
    import makes this possible (see DESIGN DECISIONS).

    Args:
        api_key: Groq API key string from the environment.
        system_prompt: System prompt text (sprint-brain.md content).
        user_message: User message text (current session state summary).

    Returns:
        Response text string, or None if the API call fails for any reason
        (error message already echoed to stderr).

    Note:
        Uses ``except Exception`` intentionally — see DESIGN DECISIONS for
        the rationale. The Groq SDK raises a hierarchy of exception types
        that are not all importable at module level.
    """
    try:
        client = Groq(api_key=api_key, timeout=GROQ_TIMEOUT)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return completion.choices[0].message.content
    except Exception as exc:  # noqa: BLE001 — see module DESIGN DECISIONS
        typer.echo(f"error: Groq call failed — {exc}", err=True)
        return None


def _write_session_log(root: Path, state: dict[str, Any], groq_output: str) -> bool:
    """Write session-log.md with brick status and Groq sprint review.

    Why it exists: The session log is a human-readable record of what happened
    this session. Without it, the sprint review output from Groq is ephemeral —
    lost when the terminal closes.

    Args:
        root: Repo root directory.
        state: Parsed state.json dict.
        groq_output: Sprint review text returned by the Groq API.

    Returns:
        True on success, False if the file cannot be written (error echoed
        to stderr).
    """
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    current_brick = state.get("current_brick") or "unknown"
    completed = state.get("completed_bricks") or []

    lines = [
        f"# Session Log — {ts}",
        "",
        "## Brick Status",
        f"Current brick: {current_brick}",
        "",
        "## Bricks Attempted This Session",
    ]
    if completed:
        for brick in completed:
            lines.append(f"- {brick}")
    else:
        lines.append("- none recorded")

    lines += [
        "",
        "## Sprint Review",
        "",
        groq_output,
        "",
    ]

    log_path = root / SESSION_LOG_RELPATH
    try:
        log_path.write_text("\n".join(lines), encoding="utf-8")
        return True
    except OSError as exc:
        typer.echo(f"error: could not write {SESSION_LOG_RELPATH}: {exc}", err=True)
        return False


def _write_state_md(root: Path, state: dict[str, Any]) -> bool:
    """Write STATE.md with project name, current brick, and next command.

    Why it exists: STATE.md is the human-readable project state file read by
    ``bricklayer status`` to show the project and phase labels. Without it,
    status output would show ``(STATE.md not found)`` after every session.

    Args:
        root: Repo root directory.
        state: Parsed state.json dict.

    Returns:
        True on success, False if the file cannot be written (error echoed
        to stderr).
    """
    project = root.name
    current_brick = state.get("current_brick") or "unknown"
    last_action = state.get("next_action") or "unknown"
    next_command = _NEXT_COMMAND_ROUTING.get(
        last_action, f"bricklayer next  # {last_action}"
    )

    lines = [
        "# Project State",
        "",
        f"Project: {project}",
        f"Current brick: {current_brick}",
        f"Last action: {last_action}",
        f"Next command: {next_command}",
        "",
    ]

    state_md_path = root / STATE_MD_RELPATH
    try:
        state_md_path.write_text("\n".join(lines), encoding="utf-8")
        return True
    except OSError as exc:
        typer.echo(f"error: could not write {STATE_MD_RELPATH}: {exc}", err=True)
        return False


def run_close_session(root: Path, yaml_path: Path) -> int:
    """Sprint review via Groq; write session-log.md and STATE.md.

    Steps (all must succeed; failure at any step returns 1 with no partial
    files written for that step):
    1. Check GROQ_API_KEY is set.
    2. Load state.json.
    3. Load sprint-brain.md via bricklayer.yaml.
    4. Call Groq API.
    5. Write session-log.md.
    6. Write STATE.md; roll back session-log.md on failure.

    Why it exists: See module docstring.

    Args:
        root: Repo root directory (contains bricklayer.yaml).
        yaml_path: Absolute path to bricklayer.yaml (needed to locate
                   sprint-brain.md).

    Returns:
        0 on success. 1 on any failure (specific error echoed to stderr).
    """
    # 1. Check API key before doing any file I/O or network calls.
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        typer.echo("error: GROQ_API_KEY not set in environment", err=True)
        return 1

    # 2. Load state.json — provides the user message content for the review.
    state = _load_state(root)
    if state is None:
        return 1

    # 3. Load sprint-brain.md — provides the system prompt for the Groq call.
    sprint_brain = _load_sprint_brain(root, yaml_path)
    if sprint_brain is None:
        return 1

    # 4. Call Groq API — no files are written before this point so a failure
    # here leaves the repo in a clean state.
    user_message = _build_user_message(state)
    groq_output = _call_groq(api_key, sprint_brain, user_message)
    if groq_output is None:
        return 1

    # 5. Write session-log.md — first file write; rollback handled in step 6.
    if not _write_session_log(root, state, groq_output):
        return 1

    # 6. Write STATE.md; roll back session-log.md on failure so neither file
    # is left in a partial or inconsistent state.
    if not _write_state_md(root, state):
        (root / SESSION_LOG_RELPATH).unlink(missing_ok=True)
        return 1

    typer.echo("Session closed. Next session:")
    typer.echo("  bricklayer resume")
    return 0
