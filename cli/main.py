"""Bricklayer CLI entry point."""

from __future__ import annotations

from typing import Optional

import typer

from cli.config import find_yaml, load_and_validate
from cli.commands.branch import run_branch
from cli.commands.build import (
    _get_current_branch,
    run_build,
    run_skeptic_packet,
    run_snapshot,
    run_verify,
    run_test,
    run_verdict,
)
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
    """Run YAML validation; exits 1 on any failure."""
    load_and_validate()


@app.command()
def status() -> None:
    """Show current brick status from state.json."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    exit_code = run_status(yaml_path.parent)
    raise typer.Exit(code=exit_code)


@app.command()
def branch(
    number: Optional[str] = typer.Argument(None, help="Brick number (e.g. 9)."),
    name: Optional[str] = typer.Argument(None, help="Branch name slug."),
    feature: bool = typer.Option(False, "--feature", help="Create a feature/ branch."),
) -> None:
    """Create and checkout a brick/N-name or feature/name branch."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    raise typer.Exit(code=run_branch(yaml_path.parent, number, name, feature))


@app.command()
def build(
    snapshot: bool = typer.Option(False, "--snapshot", help="Run snapshot-init tool."),
    verify: bool = typer.Option(False, "--verify", help="Run verify-files tool."),
    test: bool = typer.Option(False, "--test", help="Run test suite tool."),
    skeptic_packet: bool = typer.Option(False, "--skeptic-packet", help="Run skeptic packet tool."),
    verdict: Optional[str] = typer.Option(None, "--verdict", help="Record verdict: PASS or FAIL."),
) -> None:
    """Print brick contract, or run a build tool with a flag."""
    yaml_path = find_yaml()
    if yaml_path is None:
        typer.echo("error: bricklayer.yaml not found", err=True)
        raise typer.Exit(code=1)
    root = yaml_path.parent

    # Guard: refuse to operate on main
    current_branch = _get_current_branch(root)
    if current_branch == "main":
        typer.echo("You are on main. Create a branch first:")
        typer.echo("  bricklayer branch [N] [name]")
        raise typer.Exit(code=1)

    has_verdict = verdict is not None
    active = sum([snapshot, verify, test, skeptic_packet]) + (1 if has_verdict else 0)

    if active > 0:
        # Enforce mutual exclusivity — only one flag at a time
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

    raise typer.Exit(code=run_build(root))


@app.command()
def next() -> None:
    """Print the next CLI command to run based on state.json."""
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
def run() -> None:
    """Validate config and confirm the pipeline is ready."""
    _validate()
    typer.echo("bricklayer.yaml loaded and all paths validated.")


if __name__ == "__main__":
    app()
