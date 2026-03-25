"""Bricklayer CLI entry point — wires typer commands to run_* handlers.

WHY THIS EXISTS:
    Typer requires a central ``app`` object where all commands are registered.
    Without this module, there is no CLI surface — the run_* handler functions
    in individual command modules cannot be invoked from the terminal. This
    module is intentionally thin: its only job is to find bricklayer.yaml,
    validate it once, then delegate to the appropriate handler. No business
    logic lives here.

DESIGN DECISIONS:
- One find_yaml() call per command rather than a single global call at import
  time. Alternative was finding the YAML once at module level and caching the
  result. Rejected because module-level side effects break unit tests that
  patch the filesystem; per-command calls keep each command independently
  testable.
- Exit via raise typer.Exit(code=N) rather than sys.exit(N). Alternative was
  calling sys.exit() directly. Rejected because typer.Exit is caught by
  Typer's CliRunner in tests, allowing exit-code assertions without the test
  process actually terminating.
- Import _get_current_branch from build.py for the main-branch guard on the
  build command. Alternative was re-implementing it here. Rejected because
  duplicating the same git rev-parse call risks the two copies diverging.
"""

from __future__ import annotations

from typing import Optional

import typer

from cli.config import find_yaml, load_and_validate
from cli.commands.branch import run_branch
from cli.commands.commit import run_commit
from cli.commands.build import (
    _get_current_branch,
    run_build,
    run_skeptic_packet,
    run_snapshot,
    run_verify,
    run_test,
    run_verdict,
)
from cli.commands.close_feature import run_close_feature
from cli.commands.close_phase import run_close_phase
from cli.commands.close_session import run_close_session
from cli.commands.new_project import run_new_project
from cli.commands.next import run_next
from cli.commands.pause import run_pause
from cli.commands.resume import run_resume
from cli.commands.status import run_status

app = typer.Typer(
    name="bricklayer",
    help="Bricklayer — Idea-to-Product OS pipeline runner.",
    no_args_is_help=True,
)


def _validate() -> None:
    """Load and validate bricklayer.yaml; exits 1 on any failure.

    Why it exists: The ``run`` command needs a quick way to confirm the config
    is intact without running a full pipeline step. Calling load_and_validate()
    directly here keeps the run command body a single line.
    """
    load_and_validate()


@app.command()
def status() -> None:
    """Show current brick, last test result, and next action from state.json."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    exit_code = run_status(yaml_path.parent)
    raise typer.Exit(code=exit_code)


@app.command()
def commit(
    message: Optional[str] = typer.Option(None, "-m", "--message", help="Commit message."),
) -> None:
    """Commit staged files with auto-tagged brick ID message."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    if message is None:
        typer.echo(
            "Commit message required: bricklayer commit -m 'your message'", err=True
        )
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_commit(yaml_path.parent, message))


@app.command()
def branch(
    number: Optional[str] = typer.Argument(None, help="Brick/phase number."),
    name: Optional[str] = typer.Argument(None, help="Branch name slug."),
    feature: bool = typer.Option(False, "--feature", help="Create a feature/ branch."),
    phase: bool = typer.Option(False, "--phase", help="Create a phase/ branch."),
) -> None:
    """Create and checkout a brick/phase/feature branch with parent enforcement."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_branch(yaml_path.parent, number, name, feature, phase))


@app.command()
def build(
    snapshot: bool = typer.Option(False, "--snapshot", help="Run snapshot-init tool."),
    verify: bool = typer.Option(False, "--verify", help="Run verify-files tool."),
    test: bool = typer.Option(False, "--test", help="Run test suite tool."),
    skeptic_packet: bool = typer.Option(False, "--skeptic-packet", help="Run skeptic packet tool."),
    verdict: Optional[str] = typer.Option(None, "--verdict", help="Record verdict: PASS or FAIL."),
) -> None:
    """Print brick contract, or run a build pipeline step with a flag."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    root = yaml_path.parent

    # Guard against running pipeline steps on main — main is for completed
    # bricks only. All active work must happen on a feature/phase/brick branch.
    current_branch = _get_current_branch(root)
    if current_branch == "main":
        typer.echo("You are on main. Create a branch first:")
        typer.echo("  bricklayer branch [N] [name]")
        raise typer.Exit(code=1)

    has_verdict = verdict is not None
    # Count how many mutually-exclusive flags were supplied.
    active = sum([snapshot, verify, test, skeptic_packet]) + (1 if has_verdict else 0)

    if active > 0:
        # Enforce mutual exclusivity — running two pipeline steps in one
        # invocation is never valid; the steps must be run in order.
        if active > 1:
            typer.echo("Only one flag at a time. Usage: bricklayer build --<flag>")
            raise typer.Exit(code=1)
        config = load_and_validate(yaml_path)
        if snapshot:
            raise typer.Exit(code=run_snapshot(root, config))
        if verify:
            raise typer.Exit(code=run_verify(root, config))
        if test:
            raise typer.Exit(code=run_test(root, config))
        if skeptic_packet:
            raise typer.Exit(code=run_skeptic_packet(root, config))
        if has_verdict:
            raise typer.Exit(code=run_verdict(root, config, verdict))

    # No flags supplied — fall through to printing the brick contract.
    raise typer.Exit(code=run_build(root))


@app.command()
def next() -> None:
    """Print the single next CLI command to run based on state.json."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    exit_code = run_next(yaml_path.parent)
    raise typer.Exit(code=exit_code)


@app.command()
def resume() -> None:
    """Print session context from HANDOFF.json for session restart."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_resume(yaml_path.parent))


@app.command()
def pause() -> None:
    """Write HANDOFF.json and .continue-here.md for session handoff."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_pause(yaml_path.parent))


@app.command()
def close_phase() -> None:
    """Merge current phase/* branch into its parent feature/* branch."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_close_phase(yaml_path.parent))


@app.command()
def close_feature() -> None:
    """Merge current feature/* branch into main."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_close_feature(yaml_path.parent))


@app.command()
def close_session() -> None:
    """Sprint review via Groq; write session-log.md and STATE.md."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_close_session(yaml_path.parent, yaml_path))


@app.command()
def new_project(
    name: str = typer.Argument(..., help="Project name slug (letters, digits, hyphens, underscores)."),
) -> None:
    """Scaffold a new project at context/projects/<name>/ with initial state files."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_new_project(yaml_path.parent, name))


@app.command()
def run() -> None:
    """Validate bricklayer.yaml and confirm all declared paths exist."""
    _validate()
    typer.echo("bricklayer.yaml loaded and all paths validated.")


if __name__ == "__main__":
    app()
