"""Context command: print a compact project context block for AI session start.

WHY THIS EXISTS:
    At the start of every AI session, the developer has to manually assemble
    context — current brick, last action, recent decisions, next command —
    from several files in context/projects/<name>/. This is slow and error-prone.
    This command reads those files once and emits a single copy-pasteable block
    that orients any AI tool instantly. It is the CLI equivalent of !status in
    Discord.

DESIGN DECISIONS:
- Reads from context/projects/<name>/ rather than bricklayer/state.json.
  Alternative was reading the single bricklayer/state.json. Rejected because
  Phase 4 introduces per-project state files; the global state.json tracks
  which project is active but the project files hold the detail.
- Falls back to bricklayer/state.json "project" field when --project is not
  supplied. Alternative was requiring --project always. Rejected because the
  common case (one active project) should not require a flag.
- Reads only the last 3 decision-log rows rather than the full history.
  Alternative was printing all rows. Rejected because context blocks are pasted
  into AI chat; printing dozens of rows floods the context window for minimal
  gain.
- Reads "Next command" from STATE.md rather than computing it from state.json.
  Alternative was duplicating the routing logic from pause.py. Rejected because
  STATE.md is already the canonical human-readable source of next-command and
  is written by close-session. Reading from it avoids a second routing table.
- Uses typer.echo for all output so CliRunner captures it correctly in tests.
  Alternative was print(). Rejected for the same reason as other commands in
  this codebase: typer.echo is patchable and runner-friendly.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

# Path from repo root to the projects directory — must match new_project.py.
PROJECTS_RELPATH = Path("context") / "projects"

# Divider line used in the context block output.
DIVIDER = "━" * 38

# Path to the global bricklayer state (tracks active project).
_BRICKLAYER_STATE_RELPATH = "bricklayer/state.json"


def _load_project_state(project_dir: Path) -> dict[str, Any] | None:
    """Load and parse state.json from a project directory.

    Why it exists: Centralising the load+parse keeps run_context readable
    and makes the error path testable independently.

    Args:
        project_dir: Path to context/projects/<name>/.

    Returns:
        Parsed dict, or None if the file is missing or corrupt (error echoed
        to stderr).
    """
    state_path = project_dir / "state.json"
    if not state_path.exists():
        typer.echo(
            f"error: state.json not found in {project_dir}", err=True
        )
        return None
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(
            f"error: state.json in {project_dir.name} is corrupt — {exc}", err=True
        )
        return None


def _read_last_decisions(project_dir: Path, n: int = 3) -> list[str]:
    """Return the last n data rows from decision-log.md.

    Why it exists: Only data rows (not header or separator) are relevant for
    context. Isolating extraction here keeps run_context readable and makes
    the 3-row limit easy to test.

    Args:
        project_dir: Path to context/projects/<name>/.
        n: Maximum number of rows to return (most recent first at the end).

    Returns:
        List of pipe-delimited row strings (may be empty if no decisions logged
        or file is missing).
    """
    log_file = project_dir / "decision-log.md"
    if not log_file.exists():
        return []
    rows = []
    for line in log_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        # Keep lines that look like table data rows:
        # - start with "|"
        # - not the separator row (|---...)
        # - not the header row (contains "Date" in a pipe-delimited context)
        if (
            stripped.startswith("|")
            and not stripped.startswith("|---")
            and "Date" not in stripped.split("|")[1]  # header cell is "Date"
        ):
            rows.append(stripped)
    return rows[-n:]


def _read_next_command(project_dir: Path) -> str:
    """Extract "Next command:" value from STATE.md.

    Why it exists: STATE.md is the canonical source of the next command for a
    project (written by close-session). Reading it here avoids duplicating the
    routing table from pause.py.

    Args:
        project_dir: Path to context/projects/<name>/.

    Returns:
        The next command string, or "bricklayer status" if STATE.md is missing
        or the field is absent.
    """
    state_md = project_dir / "STATE.md"
    if not state_md.exists():
        return "bricklayer status"
    for line in state_md.read_text(encoding="utf-8").splitlines():
        if line.startswith("Next command:"):
            return line[len("Next command:"):].strip()
    return "bricklayer status"


def _resolve_project_name(root: Path, project_arg: str | None) -> str | None:
    """Return the project name to use, reading bricklayer/state.json if needed.

    Why it exists: When --project is omitted, the command falls back to the
    "project" field in bricklayer/state.json. Isolating this logic keeps
    run_context clean and makes the fallback testable independently.

    Args:
        root: Repo root directory.
        project_arg: Value of the --project flag, or None if not supplied.

    Returns:
        Project name string, or None if the fallback also fails (error echoed
        to stderr).
    """
    if project_arg:
        return project_arg

    state_path = root / _BRICKLAYER_STATE_RELPATH
    if not state_path.exists():
        typer.echo(
            "error: no --project given and bricklayer/state.json not found",
            err=True,
        )
        return None
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: bricklayer/state.json is corrupt — {exc}", err=True)
        return None

    name = data.get("project") or data.get("current_brick")
    if not name:
        typer.echo(
            "error: no --project given and 'project' field not set in "
            "bricklayer/state.json",
            err=True,
        )
        return None
    # If the stored value looks like "Brick N - name", strip to bare name.
    if " - " in name:
        name = name.split(" - ", 1)[1].strip()
    return name


def run_context(root: Path, project_arg: str | None) -> int:
    """Print a compact context block for a project.

    Why it exists: See module docstring.

    Args:
        root: Repo root directory.
        project_arg: Project name from --project flag, or None to use
                     the active project from bricklayer/state.json.

    Returns:
        0 on success. 1 on any error (message already echoed to stderr).
    """
    # 1. Resolve project name.
    name = _resolve_project_name(root, project_arg)
    if name is None:
        return 1

    # 2. Check that context/projects/ exists at all.
    projects_dir = root / PROJECTS_RELPATH
    if not projects_dir.exists():
        typer.echo(
            "No projects found. Run:\n  bricklayer new-project <name>", err=True
        )
        return 1

    # 3. Check that the specific project directory exists.
    project_dir = projects_dir / name
    if not project_dir.exists():
        typer.echo(
            f"error: project '{name}' not found at {project_dir}", err=True
        )
        return 1

    # 4. Load project state.json.
    state = _load_project_state(project_dir)
    if state is None:
        return 1

    # 5. Read decision log and next command (soft reads — missing files degrade
    # gracefully rather than causing a hard failure).
    decisions = _read_last_decisions(project_dir)
    next_cmd = _read_next_command(project_dir)

    # 6. Emit the context block.
    rel_state = PROJECTS_RELPATH / name / "state.json"
    current_brick = state.get("current_brick") or "none"
    last_action = state.get("last_action") or "none"
    loop_count = state.get("loop_count", 0)
    branch = state.get("current_branch") or "none"

    typer.echo(DIVIDER)
    typer.echo(f"PROJECT CONTEXT: {name}")
    typer.echo(DIVIDER)
    typer.echo(f"State file:    {rel_state}")
    typer.echo(f"Current brick: {current_brick}")
    typer.echo(f"Last action:   {last_action}")
    typer.echo(f"Loop count:    {loop_count}")
    typer.echo(f"Branch:        {branch}")
    typer.echo(DIVIDER)
    typer.echo("Last 3 decisions:")
    if decisions:
        for row in decisions:
            typer.echo(row)
    else:
        typer.echo("No decisions logged yet")
    typer.echo(DIVIDER)
    typer.echo(f"Next command: {next_cmd}")
    typer.echo(DIVIDER)

    return 0
