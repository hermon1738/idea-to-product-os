"""Close-session command: sprint review via Groq, writes session-log.md and STATE.md."""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any

import typer
import yaml
from groq import Groq

STATE_RELPATH = "bricklayer/state.json"
SESSION_LOG_RELPATH = "session-log.md"
STATE_MD_RELPATH = "STATE.md"
GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_TIMEOUT = 30.0

_NEXT_COMMAND_ROUTING: dict[str, str] = {
    "snapshot_init": "bricklayer build --snapshot",
    "verify": "bricklayer build --verify",
    "tests_passed": "bricklayer build --skeptic-packet",
    "skeptic_packet_ready": "bricklayer build --verdict PASS|FAIL",
    "brick_complete": "bricklayer next",
}


def _load_state(root: Path) -> dict[str, Any] | None:
    """Load state.json. Returns None and echoes error on failure."""
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
    """Load sprint-brain.md from phases.review in bricklayer.yaml."""
    try:
        config = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001
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
    """Build the user message summarising current state for the sprint review."""
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
    """Call Groq API. Returns response text or None on error."""
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
    except Exception as exc:  # noqa: BLE001
        typer.echo(f"error: Groq call failed — {exc}", err=True)
        return None


def _write_session_log(root: Path, state: dict[str, Any], groq_output: str) -> bool:
    """Write session-log.md. Returns True on success."""
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
    """Write STATE.md. Returns True on success."""
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
    """Sprint review via Groq; write session-log.md and STATE.md. Returns 0/1."""
    # 1. Check API key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        typer.echo("error: GROQ_API_KEY not set in environment", err=True)
        return 1

    # 2. Load state.json
    state = _load_state(root)
    if state is None:
        return 1

    # 3. Load sprint-brain.md via bricklayer.yaml
    sprint_brain = _load_sprint_brain(root, yaml_path)
    if sprint_brain is None:
        return 1

    # 4. Call Groq
    user_message = _build_user_message(state)
    groq_output = _call_groq(api_key, sprint_brain, user_message)
    if groq_output is None:
        return 1

    # 5. Write session-log.md
    if not _write_session_log(root, state, groq_output):
        return 1

    # 6. Write STATE.md; roll back session-log.md on failure
    if not _write_state_md(root, state):
        (root / SESSION_LOG_RELPATH).unlink(missing_ok=True)
        return 1

    # 7. Print success
    typer.echo("Session closed. Next session:")
    typer.echo("  bricklayer resume")
    return 0
