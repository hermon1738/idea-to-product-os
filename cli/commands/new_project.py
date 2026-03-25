"""New-project command: scaffold context/projects/<name>/ with initial state files.

WHY THIS EXISTS:
    Phase 4 of the Bricklayer pipeline introduces multi-project support. Every
    project tracked by the CLI needs three files to exist before any build
    commands can run against it: STATE.md (human-readable current state),
    decision-log.md (append-only audit trail of decisions), and state.json
    (machine-readable position for the CLI to read and update). Without this
    command, a developer would have to create all three by hand, using the
    correct format, every time they start a new project — an error-prone step
    that the CLI should automate.

DESIGN DECISIONS:
- Project directory lives at context/projects/<name>/ rather than the repo
  root. Alternative was creating the project at the repo root. Rejected
  because multi-project repos would produce dozens of top-level directories.
  context/projects/ keeps all tracked projects in one predictable location.
- Name validation uses a strict allowlist regex (^[a-zA-Z0-9_-]+$) rather
  than a blocklist. Alternative was rejecting only known bad characters.
  Rejected because a blocklist will always have gaps; an allowlist guarantees
  the name is safe to use as a directory name on all target platforms.
- Duplicate detection checks for directory existence, not file existence.
  Alternative was checking for state.json specifically. Rejected because the
  directory is the canonical source of truth — a partial creation that left
  no state.json should still be treated as already-exists.
- state.json uses null for all optional fields rather than omitting them.
  Alternative was omitting unset fields. Rejected because the downstream
  `bricklayer context` command (Brick 20) needs to know all fields exist, even
  when empty, to avoid KeyError on first read.
- All three files are written before printing success. Alternative was
  printing "created" after each file. Rejected because partial success
  messages would confuse users if a later write fails. The success message
  is only shown when all three files are on disk.
"""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path
from typing import Any

import typer

# Path from repo root to the projects directory.
PROJECTS_RELPATH = Path("context") / "projects"

# Only alphanumeric characters, hyphens, and underscores are allowed in
# project names. This ensures the name is safe as a directory name on
# Linux, macOS, and Windows without any escaping.
_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")


def _validate_name(name: str) -> str | None:
    """Return an error message if name is invalid, else None.

    Why it exists: Centralising validation makes it testable independently
    of the filesystem operations and avoids duplicating the regex.

    Args:
        name: Candidate project name supplied by the user.

    Returns:
        None if the name is valid. An error string if it is not.
    """
    if not name:
        return "Project name cannot be empty"
    if not _NAME_PATTERN.match(name):
        return (
            f"Invalid project name '{name}': "
            "use only letters, digits, hyphens (-), and underscores (_)"
        )
    return None


def _build_state_md(name: str, created: str) -> str:
    """Build initial STATE.md content for a new project.

    Args:
        name: Project name slug.
        created: ISO date string for the Created field.

    Returns:
        Markdown string suitable for writing to STATE.md.
    """
    return (
        f"# {name} — Project State\n"
        f"Created: {created}\n"
        f"Current brick: none\n"
        f"Last action: none\n"
        f"Next command: bricklayer status\n"
        f"Blockers: none\n"
    )


def _build_decision_log(name: str) -> str:
    """Build initial decision-log.md content for a new project.

    Args:
        name: Project name slug (used in the heading).

    Returns:
        Markdown string with header row and separator only — no data rows.
    """
    return (
        f"# {name} — Decision Log\n"
        "| Date | Component | Decision Made | Status | Next Action |\n"
        "|------|-----------|--------------|--------|-------------|\n"
    )


def _build_state_json(name: str) -> dict[str, Any]:
    """Build initial state.json content for a new project.

    Args:
        name: Project name slug stored in the project field.

    Returns:
        Dict ready for json.dumps with all required fields present.
    """
    return {
        "project": name,
        "current_brick": None,
        "last_action": None,
        "loop_count": 0,
        "current_branch": None,
        "current_feature": None,
        "current_phase": None,
        "last_test_run": {
            "command": None,
            "status": None,
            "exit_code": None,
            "artifact": None,
        },
    }


def run_new_project(root: Path, name: str) -> int:
    """Scaffold a new project directory with STATE.md, decision-log.md, state.json.

    Why it exists: See module docstring.

    Args:
        root: Repo root directory (contains bricklayer.yaml).
        name: Project name slug supplied by the user.

    Returns:
        0 on success. 1 on validation failure or duplicate name (error echoed
        to stderr).
    """
    # 1. Validate name before touching the filesystem.
    error = _validate_name(name)
    if error:
        typer.echo(f"error: {error}", err=True)
        return 1

    # 2. Resolve project directory; check for duplicate.
    projects_dir = root / PROJECTS_RELPATH
    project_dir = projects_dir / name
    if project_dir.exists():
        typer.echo(
            f"error: project '{name}' already exists at {project_dir}", err=True
        )
        return 1

    # 3. Create context/projects/ if absent, then the project subdirectory.
    project_dir.mkdir(parents=True, exist_ok=True)

    # 4. Write all three files. All writes must succeed before printing success.
    created = datetime.date.today().isoformat()

    (project_dir / "STATE.md").write_text(
        _build_state_md(name, created), encoding="utf-8"
    )
    (project_dir / "decision-log.md").write_text(
        _build_decision_log(name), encoding="utf-8"
    )
    (project_dir / "state.json").write_text(
        json.dumps(_build_state_json(name), indent=2), encoding="utf-8"
    )

    # 5. Print relative path for a clean, copy-pasteable success message.
    rel = PROJECTS_RELPATH / name
    typer.echo(f"Project created: {rel}/")
    return 0
