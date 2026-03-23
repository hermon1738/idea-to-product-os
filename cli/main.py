"""Bricklayer CLI entry point."""

from __future__ import annotations

import typer

from cli.config import load_and_validate

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
    _validate()
    typer.echo("Validation passed. Use bricklayer/tools/ to inspect state.")


@app.command()
def run() -> None:
    """Validate config and confirm the pipeline is ready."""
    _validate()
    typer.echo("bricklayer.yaml loaded and all paths validated.")


if __name__ == "__main__":
    app()
