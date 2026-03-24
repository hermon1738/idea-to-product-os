"""Bricklayer CLI entry point."""

from __future__ import annotations

from typing import Optional

import typer

from cli.config import find_yaml, load_and_validate
from cli.commands.build import run_build, run_skeptic_packet, run_snapshot, run_verify, run_test, run_verdict
from cli.commands.next import run_next
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
def run() -> None:
    """Validate config and confirm the pipeline is ready."""
    _validate()
    typer.echo("bricklayer.yaml loaded and all paths validated.")


if __name__ == "__main__":
    app()
