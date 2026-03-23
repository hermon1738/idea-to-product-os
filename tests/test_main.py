"""CliRunner integration tests for cli/main.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.main import app  # noqa: E402

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_yaml(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "bricklayer.yaml"
    p.write_text(content, encoding="utf-8")
    return p


def _make_file(tmp_path: Path, rel: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("", encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# --help
# ---------------------------------------------------------------------------


def test_help_exits_zero() -> None:
    """bricklayer --help → exit 0."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_help_no_traceback() -> None:
    """bricklayer --help output must not contain 'Traceback'."""
    result = runner.invoke(app, ["--help"])
    assert "Traceback" not in (result.output or "")


def test_help_shows_commands() -> None:
    """--help output mentions at least one subcommand."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # typer prints the app help with usage info
    assert len(result.output) > 0


# ---------------------------------------------------------------------------
# run command — happy path (uses real bricklayer.yaml in repo root)
# ---------------------------------------------------------------------------


def test_run_command_passes_with_valid_yaml(tmp_path: Path) -> None:
    """run command exits 0 when all yaml paths exist."""
    _make_file(tmp_path, "system-prompts/plan.md")

    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  plan: system-prompts/plan.md\ntools: {}\nagents: {}\n",
    )

    # Patch find_yaml to return our temp yaml
    import cli.config as config_mod
    original_find = config_mod.find_yaml

    def patched_find(start=None):
        return yaml_path

    config_mod.find_yaml = patched_find
    try:
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
        assert "Traceback" not in (result.output or "")
    finally:
        config_mod.find_yaml = original_find


# ---------------------------------------------------------------------------
# run command — missing path → exit 1, correct message, no traceback
# ---------------------------------------------------------------------------


def test_run_command_missing_path_exits_1(tmp_path: Path) -> None:
    """run command exits 1 when a yaml path is missing."""
    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  missing: system-prompts/ghost.md\ntools: {}\nagents: {}\n",
    )

    import cli.config as config_mod
    original_find = config_mod.find_yaml

    def patched_find(start=None):
        return yaml_path

    config_mod.find_yaml = patched_find
    try:
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 1
        assert "Missing: system-prompts/ghost.md" in result.output
        assert "check bricklayer.yaml" in result.output
        assert "Traceback" not in result.output
    finally:
        config_mod.find_yaml = original_find


def test_run_command_missing_path_no_traceback(tmp_path: Path) -> None:
    """Missing path error output must not show a Python traceback."""
    yaml_path = _write_yaml(
        tmp_path,
        "tools:\n  ghost: tools/ghost.py\nphases: {}\nagents: {}\n",
    )

    import cli.config as config_mod
    original_find = config_mod.find_yaml

    def patched_find(start=None):
        return yaml_path

    config_mod.find_yaml = patched_find
    try:
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 1
        assert "Traceback" not in result.output
    finally:
        config_mod.find_yaml = original_find


# ---------------------------------------------------------------------------
# run command — missing yaml → exit 1, correct message
# ---------------------------------------------------------------------------


def test_run_command_no_yaml_exits_1() -> None:
    """run command exits 1 when bricklayer.yaml is not found anywhere."""
    import cli.config as config_mod
    original_find = config_mod.find_yaml

    def patched_find(start=None):
        return None

    config_mod.find_yaml = patched_find
    try:
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 1
        assert "bricklayer.yaml not found at repo root" in result.output
        assert "Traceback" not in result.output
    finally:
        config_mod.find_yaml = original_find
