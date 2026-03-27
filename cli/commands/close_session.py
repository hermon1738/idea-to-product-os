"""Close-session command: sprint review via Groq, writes session-log.md and STATE.md.

WHY THIS EXISTS:
    At the end of a working session, the developer needs a structured review
    of what was accomplished (which bricks passed, which failed, what the loop
    counts were). Without this command, that review happens in the developer's
    head — inconsistently, incompletely, and without a written record. This
    command offloads the review to a Groq LLM using the sprint-brain.md system
    prompt, then persists the output so the next session starts with a written
    summary of the previous session's outcomes. After the local write, it also
    syncs a decision-log row and pipeline-status.md to DOCS_PATH (the ai-agents
    clone), then auto-pushes those docs to GitHub — replacing the manual !scribe
    Discord ritual for CLI sessions.

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
- Docs sync (DOCS_PATH) is always a soft operation: DOCS_PATH not set or
  directory missing both print a message and continue without returning 1.
  Reason: the ai-agents clone may not be locally mounted; close-session
  should not fail because of a remote path that is legitimately absent on the
  local machine.
- Auto-push (git add/commit/push in DOCS_PATH) is also always soft — push
  failure never causes return 1. Docs are written locally before the push
  attempt, so session data is preserved even when the remote is unreachable.
  Alternative was making push failure fatal. Rejected because a transient
  network error at session-close would block the developer from moving on.
  All git operations inside _push_docs are wrapped in try/except to handle
  subprocess.TimeoutExpired (network hang), FileNotFoundError (git not in
  PATH), and any other unexpected exception — all emit a warning to stderr
  and return gracefully.
- _is_git_repo uses ``git rev-parse --is-inside-work-tree`` rather than
  checking for a ``.git`` directory. Alternative was ``Path.exists(".git")``.
  Rejected because git worktrees have no ``.git`` directory in subdirectories
  but are still valid repos; rev-parse handles all cases correctly.
- GROQ_HEAVY_MODEL (llama-3.3-70b-versatile) is used for structured JSON
  extraction from the sprint review output. The 8b model produces conversational
  prose; extracting component/decision/status/next_action from that prose needs
  better instruction-following. The main sprint review stays on 8b for speed.
- _extract_structured_data falls back to state-derived defaults if the heavy
  model call fails or returns non-JSON. This prevents a crash when the
  extraction call is unavailable. Making the fallback smarter is tracked as
  v2 debt in DEBT.md (D-011).
- _sanitize_pipe replaces ``|`` with ``-`` in every field written into a
  markdown table cell. Without this, LLM-generated pipe characters silently
  corrupt the decision-log.md table structure.
"""

from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import typer
import yaml
from groq import Groq

from cli.config import _load_dotenv

# Relative paths from repo root.
STATE_RELPATH = "bricklayer/state.json"
SESSION_LOG_RELPATH = "session-log.md"
STATE_MD_RELPATH = "STATE.md"

# Default LLM configuration — used when no llm: section is present in
# bricklayer.yaml. Kept as named constants so they are easy to locate and so
# tests can assert on specific values without hardcoding strings.
DEFAULT_LLM_PROVIDER: str = "groq"
DEFAULT_LLM_MODEL: str = "llama-3.1-8b-instant"
DEFAULT_LLM_HEAVY_MODEL: str = "llama-3.3-70b-versatile"
DEFAULT_LLM_API_KEY_ENV: str = "GROQ_API_KEY"

# Backwards-compatible aliases — existing tests import these names directly.
GROQ_MODEL: str = DEFAULT_LLM_MODEL
GROQ_HEAVY_MODEL: str = DEFAULT_LLM_HEAVY_MODEL

GROQ_TIMEOUT: float = 30.0

# Supported providers — any value not in this set exits 1 with a clear message.
_SUPPORTED_PROVIDERS: frozenset[str] = frozenset({"groq"})

# System prompt sent to GROQ_HEAVY_MODEL to extract structured data from the
# sprint review prose. Kept as a module constant so tests can inspect it and
# so it is easy to tune without hunting through function bodies.
_EXTRACTION_SYSTEM_PROMPT = (
    "You are a data extractor. Given a sprint review, return ONLY a JSON object "
    "with exactly these four keys: "
    '"component" (what was worked on, concise noun phrase), '
    '"decision" (the main outcome or decision made, one sentence max 80 chars), '
    '"status" (one of: DONE, IN PROGRESS, BLOCKED, QUEUED), '
    '"next_action" (the immediate next step, one short phrase). '
    "No markdown fences, no explanation — raw JSON only."
)

# Decision-log header — must match what Session Scribe writes so both tools
# produce consistent entries in the same file.
_DECISION_LOG_HEADER = (
    "# Decision Log — Idea-to-Product OS\n"
    "| Date | Component | Decision Made | Status | Next Action |\n"
    "|------|-----------|--------------|--------|-------------|\n"
)

# Commit message template for auto-push to GitHub. Format uses UTC timestamp
# so git log reads chronologically and is unambiguous across timezones.
_DOCS_COMMIT_FMT: str = "sync: session docs {dt}"

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


def _read_llm_config(yaml_path: Path) -> dict[str, str]:
    """Read LLM configuration from the llm: section of bricklayer.yaml.

    Why it exists: Hardcoding Groq constants in close_session.py meant that
    switching providers or models required a code change. Reading from
    bricklayer.yaml llm: section lets each project configure its own provider
    without touching the CLI source.

    Fallback: if llm: section is absent, returns Groq defaults and emits a
    deprecation warning to stderr so users know to add the section. This avoids
    a hard break for projects created before Brick 25.

    Args:
        yaml_path: Absolute path to bricklayer.yaml.

    Returns:
        Dict with keys: provider, model, heavy_model, api_key_env.

    Raises:
        SystemExit(1): If the declared provider is not in _SUPPORTED_PROVIDERS.
    """
    try:
        config = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
    except (yaml.YAMLError, OSError):
        # If we cannot parse the yaml at all, fall back to defaults.
        config = {}

    llm = config.get("llm") or {}
    if not llm:
        typer.echo(
            "warning: llm: section missing from bricklayer.yaml — "
            "using Groq defaults. Add an llm: section to suppress this warning.",
            err=True,
        )
        return {
            "provider": DEFAULT_LLM_PROVIDER,
            "model": DEFAULT_LLM_MODEL,
            "heavy_model": DEFAULT_LLM_HEAVY_MODEL,
            "api_key_env": DEFAULT_LLM_API_KEY_ENV,
        }

    provider = (llm.get("provider") or DEFAULT_LLM_PROVIDER).strip()
    if provider not in _SUPPORTED_PROVIDERS:
        typer.echo(
            f"error: Provider {provider} not yet supported. "
            f"Supported providers: {', '.join(sorted(_SUPPORTED_PROVIDERS))}",
            err=True,
        )
        sys.exit(1)

    return {
        "provider": provider,
        "model": (llm.get("model") or DEFAULT_LLM_MODEL).strip(),
        "heavy_model": (llm.get("heavy_model") or DEFAULT_LLM_HEAVY_MODEL).strip(),
        "api_key_env": (llm.get("api_key_env") or DEFAULT_LLM_API_KEY_ENV).strip(),
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


def _call_groq(
    api_key: str,
    system_prompt: str,
    user_message: str,
    model: str = GROQ_MODEL,
) -> str | None:
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
            model=model,
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


def _sanitize_pipe(text: str) -> str:
    """Replace pipe characters with dashes so they cannot corrupt markdown tables.

    Why it exists: LLM output may contain ``|`` characters in any field. A
    single unescaped pipe inside a table cell breaks every column to its right,
    silently corrupting decision-log.md for all future reads.

    Args:
        text: Any string that will be written into a markdown table cell.

    Returns:
        The input string with every ``|`` replaced by ``-``.
    """
    return text.replace("|", "-")


def _extract_structured_data(
    api_key: str,
    groq_output: str,
    state: dict[str, Any],
    heavy_model: str = GROQ_HEAVY_MODEL,
) -> dict[str, str]:
    """Call GROQ_HEAVY_MODEL to extract structured JSON from sprint review prose.

    Why it exists: The 8b sprint review model produces free-form prose. Naively
    splitting on the first line captures conversational filler. GROQ_HEAVY_MODEL
    (70b) reliably extracts component/decision/status/next_action as JSON.

    Falls back to state-derived defaults if the call fails or the response is
    not valid JSON. Making the fallback smarter is tracked as D-011 in DEBT.md.

    Args:
        api_key: Groq API key.
        groq_output: Sprint review prose from the first (8b) Groq call.
        state: Parsed state.json dict — used for fallback values only.

    Returns:
        Dict with keys: component, decision, status, next_action. All strings.
        Never raises.
    """
    try:
        client = Groq(api_key=api_key, timeout=GROQ_TIMEOUT)
        completion = client.chat.completions.create(
            model=heavy_model,
            messages=[
                {"role": "system", "content": _EXTRACTION_SYSTEM_PROMPT},
                {"role": "user", "content": groq_output},
            ],
        )
        raw = completion.choices[0].message.content.strip()
        # Strip optional ```json ... ``` wrapper that some models emit.
        if raw.startswith("```"):
            parts = raw.split("```")
            raw = parts[1].lstrip("json").strip() if len(parts) > 1 else raw
        return json.loads(raw)
    except Exception:  # noqa: BLE001 — fallback path, see DESIGN DECISIONS
        current_brick = state.get("current_brick") or "unknown"
        component = (
            current_brick.split(" - ", 1)[1].strip()
            if " - " in current_brick
            else current_brick
        )
        return {
            "component": component,
            "decision": "sprint review completed",
            "status": state.get("status") or "unknown",
            "next_action": state.get("next_action") or "unknown",
        }


def _build_decision_log_row(extracted: dict[str, str]) -> str:
    """Build one sanitized pipe-delimited decision-log row from extracted data.

    Why it exists: The decision-log row format must match what Session Scribe
    writes exactly so both tools produce consistent entries. Isolating the
    builder makes it testable independently.

    Args:
        extracted: Dict from _extract_structured_data with keys component,
                   decision, status, next_action.

    Returns:
        A markdown table row string:
        ``| YYYY-MM-DD | component | decision | STATUS | next_action |``
        All LLM-supplied fields are pipe-sanitized.
    """
    date = datetime.date.today().isoformat()
    component = _sanitize_pipe((extracted.get("component") or "unknown")[:80])
    decision = _sanitize_pipe((extracted.get("decision") or "sprint review completed")[:80])
    status = _sanitize_pipe(extracted.get("status") or "unknown")
    next_action = _sanitize_pipe((extracted.get("next_action") or "unknown")[:80])
    return f"| {date} | {component} | {decision} | {status} | {next_action} |"


def _append_decision_log(docs_path: Path, row: str) -> None:
    """Append one row to decision-log.md, creating the file with header if absent.

    Why it exists: Isolating append logic keeps _sync_docs readable and makes
    the file-creation branch easy to test independently.

    Args:
        docs_path: Directory containing (or to contain) decision-log.md.
        row: Pipe-delimited row string to append.
    """
    log_file = docs_path / "decision-log.md"
    if not log_file.exists():
        log_file.write_text(_DECISION_LOG_HEADER, encoding="utf-8")
    with log_file.open("a", encoding="utf-8") as f:
        f.write(row + "\n")


def _build_pipeline_status(state: dict[str, Any], groq_output: str) -> str:
    """Build pipeline-status.md content from current state and sprint review.

    Why it exists: The status file needs to be human-readable and reflect the
    current session outcome. Isolating the builder makes it testable.

    Args:
        state: Parsed state.json dict.
        groq_output: Sprint review text returned by the Groq API.

    Returns:
        Markdown string suitable for writing to pipeline-status.md.
    """
    date = datetime.date.today().isoformat()
    # Sanitize table cell values — LLM-produced bricks names shouldn't contain
    # pipes, but state values are untrusted strings so guard here too.
    current_brick = _sanitize_pipe(state.get("current_brick") or "unknown")
    status = _sanitize_pipe(state.get("status") or "unknown")
    next_action = _sanitize_pipe(state.get("next_action") or "unknown")
    completed = state.get("completed_bricks") or []
    completed_list = "\n".join(f"- {b}" for b in completed) if completed else "- none"

    return (
        f"# Pipeline Status\n"
        f"Last updated: {date}\n\n"
        f"## Current State\n\n"
        f"| Field | Value |\n"
        f"|-------|-------|\n"
        f"| Current brick | {current_brick} |\n"
        f"| Status | {status} |\n"
        f"| Next action | {next_action} |\n\n"
        f"## Completed Bricks\n\n"
        f"{completed_list}\n\n"
        f"## Sprint Review\n\n"
        f"{groq_output}\n"
    )


def _is_git_repo(path: Path) -> bool:
    """Return True if path is inside a git repository.

    Why it exists: Before running git add/commit/push in DOCS_PATH, we need
    to confirm it is actually a git repo. Passing a non-repo path to git
    produces cryptic fatal errors; this explicit check lets _push_docs print
    a clear warning and skip the push instead of surfacing a confusing git
    error message.

    Uses ``git rev-parse --is-inside-work-tree`` rather than checking for a
    ``.git`` directory — see module DESIGN DECISIONS for the rationale.

    Args:
        path: Directory to check.

    Returns:
        True if git reports this path is inside a work tree, False otherwise.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=path,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    return result.returncode == 0


def _push_docs(docs_path: Path) -> None:
    """Run git add / commit / push in DOCS_PATH to sync session docs to GitHub.

    Why it exists: Closes the gap between local doc writes and the remote
    repository. Without this step, docs accumulate locally and must be pushed
    manually — which was the previous "!scribe" Discord ritual this command is
    designed to eliminate. GitHub becomes the single source of truth immediately
    after every session.

    Always a soft operation — no step here causes run_close_session to return
    1. Session docs are written locally before this is called, so the session
    summary is preserved even when the push fails or the repo is unavailable.

    Exception handling:
    - subprocess.TimeoutExpired: git hung on network I/O → warn, skip
    - FileNotFoundError: git not in PATH → warn, skip
    - Exception: any other unexpected error → warn with message, skip

    Args:
        docs_path: Directory that was written to by _sync_docs. Must be the
                   root or a subdirectory of the git repository to push.

    Returns:
        None. Warnings are echoed to stderr; no exceptions propagate.
    """
    if not _is_git_repo(docs_path):
        # Not a git repo — cannot push. Warn and continue; docs are still
        # written locally so no session data is lost.
        typer.echo(
            f"warning: DOCS_PATH {docs_path} is not a git repo — skipping push",
            err=True,
        )
        return

    dt = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
    commit_msg = _DOCS_COMMIT_FMT.format(dt=dt)

    try:
        # Stage docs/ only — not the full repo. Safe even if DOCS_PATH contains
        # unrelated untracked files in other subdirectories.
        subprocess.run(
            ["git", "add", "docs/"],
            cwd=docs_path,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # Commit — capture_output keeps git's commit summary out of bricklayer's
        # stdout. check=False because "nothing to commit" exits 1 on some git
        # versions and that is not an error we want to surface.
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=docs_path,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        # Push — failure is non-fatal: docs are already written locally.
        # Print a warning so the user knows to push manually if needed.
        push_result = subprocess.run(
            ["git", "push"],
            cwd=docs_path,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        if push_result.returncode != 0:
            typer.echo(
                "warning: git push failed — docs written locally but not pushed to GitHub. "
                f"Run 'git push' in {docs_path} to sync manually.",
                err=True,
            )
            return

        typer.echo("Docs pushed to GitHub")

    except subprocess.TimeoutExpired:
        # Network hung beyond the timeout — push is skipped but docs are safe.
        typer.echo(
            "warning: git push timed out, skipping — docs written locally.",
            err=True,
        )
    except FileNotFoundError:
        # git binary not found in PATH on this machine — push is impossible.
        typer.echo(
            "warning: git not found in PATH, skipping push — docs written locally.",
            err=True,
        )
    except Exception as exc:  # noqa: BLE001 — all push failures are soft
        # Catch-all so an unexpected error never crashes close-session.
        typer.echo(
            f"warning: docs push failed: {exc}, skipping — docs written locally.",
            err=True,
        )


def _sync_docs(
    api_key: str,
    state: dict[str, Any],
    groq_output: str,
    heavy_model: str = GROQ_HEAVY_MODEL,
) -> None:
    """Sync decision-log.md and pipeline-status.md to DOCS_PATH if set, then push.

    Why it exists: Replaces the manual !scribe Discord ritual for CLI sessions.
    After a successful Groq sprint review, this writes the structured summary
    to the local ai-agents clone and then auto-pushes to GitHub so the remote
    is always current after every session. Always a soft operation — missing or
    unset DOCS_PATH is not a failure (clone may not be present locally).

    Args:
        api_key: Groq API key — forwarded to _extract_structured_data.
        state: Parsed state.json dict.
        groq_output: Sprint review text returned by the first (8b) Groq call.
        heavy_model: Model name for _extract_structured_data heavy call.
    """
    docs_path_str = os.environ.get("DOCS_PATH")
    if not docs_path_str:
        typer.echo("DOCS_PATH not set, skipping docs sync")
        return

    docs_path = Path(docs_path_str)
    if not docs_path.exists():
        typer.echo(
            f"warning: DOCS_PATH {docs_path} does not exist, skipping docs sync"
        )
        return

    # Second Groq call — structured extraction using the heavy model.
    extracted = _extract_structured_data(api_key, groq_output, state, heavy_model=heavy_model)
    row = _build_decision_log_row(extracted)
    _append_decision_log(docs_path, row)

    status_content = _build_pipeline_status(state, groq_output)
    (docs_path / "pipeline-status.md").write_text(status_content, encoding="utf-8")

    typer.echo(f"Docs synced to {docs_path}")

    # Auto-push to GitHub — always soft, never causes return 1.
    _push_docs(docs_path)


def run_close_session(root: Path, yaml_path: Path) -> int:
    """Sprint review via Groq; write session-log.md, STATE.md, and sync VPS docs.

    Steps (all must succeed; failure at any step returns 1 with no partial
    files written for that step):
    1. Check GROQ_API_KEY is set.
    2. Load state.json.
    3. Load sprint-brain.md via bricklayer.yaml.
    4. Call Groq API.
    5. Write session-log.md.
    6. Write STATE.md; roll back session-log.md on failure.
    7. Sync docs to DOCS_PATH (soft — never returns 1).

    Why it exists: See module docstring.

    Args:
        root: Repo root directory (contains bricklayer.yaml).
        yaml_path: Absolute path to bricklayer.yaml (needed to locate
                   sprint-brain.md).

    Returns:
        0 on success. 1 on any failure (specific error echoed to stderr).
    """
    # 0. Load .env alongside bricklayer.yaml so secrets are available before
    # any other check (e.g. api_key_env lookup below).
    _load_dotenv(yaml_path.parent)

    # 0b. Read LLM config from bricklayer.yaml llm: section; exits 1 if
    # provider is unsupported.
    llm_config = _read_llm_config(yaml_path)

    # 1. Check API key before doing any file I/O or network calls.
    api_key_env = llm_config["api_key_env"]
    api_key = os.environ.get(api_key_env)
    if not api_key:
        typer.echo(f"error: {api_key_env} not set in environment", err=True)
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
    groq_output = _call_groq(api_key, sprint_brain, user_message, model=llm_config["model"])
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

    # 7. Sync docs to DOCS_PATH — soft operation, never causes return 1.
    _sync_docs(api_key, state, groq_output, heavy_model=llm_config["heavy_model"])

    typer.echo("Session closed. Next session:")
    typer.echo("  bricklayer resume")
    return 0
