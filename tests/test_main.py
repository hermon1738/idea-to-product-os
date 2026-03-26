"""CliRunner integration tests for cli/main.py."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

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


# ---------------------------------------------------------------------------
# close-session CliRunner integration — .env + llm config
# ---------------------------------------------------------------------------


def _setup_close_session_project(tmp_path: Path) -> Path:
    """Create a minimal project for close-session tests. Returns yaml_path."""
    # .env with a custom api key env var name to avoid colliding with real GROQ_API_KEY
    (tmp_path / ".env").write_text(
        "_BL_TEST_CS_KEY=key-from-dotenv\n", encoding="utf-8"
    )
    # sprint-brain.md
    (tmp_path / "sprint-brain.md").write_text(
        "You are a sprint reviewer.\n", encoding="utf-8"
    )
    # bricklayer.yaml with llm: section using custom api_key_env
    yaml_path = tmp_path / "bricklayer.yaml"
    yaml_path.write_text(
        "phases:\n  review: sprint-brain.md\n"
        "tools: {}\nagents: {}\n"
        "llm:\n  provider: groq\n  model: test-model\n"
        "  heavy_model: test-heavy\n  api_key_env: _BL_TEST_CS_KEY\n",
        encoding="utf-8",
    )
    # state.json
    bricklayer_dir = tmp_path / "bricklayer"
    bricklayer_dir.mkdir()
    (bricklayer_dir / "state.json").write_text(
        json.dumps({
            "current_brick": "Brick 25 - test",
            "status": "IN_PROGRESS",
            "loop_count": 0,
            "last_gate_failed": None,
            "completed_bricks": [],
            "next_action": "unknown",
            "last_test_run": {},
        }),
        encoding="utf-8",
    )
    return yaml_path


def test_close_session_loads_env_file_and_uses_llm_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CliRunner integration: .env loaded at startup; llm: section drives model choice."""
    yaml_path = _setup_close_session_project(tmp_path)

    # Remove _BL_TEST_CS_KEY from real env — it must come from .env only.
    monkeypatch.delenv("_BL_TEST_CS_KEY", raising=False)

    # Patch cli.main.find_yaml (the binding used by the close_session command).
    with patch("cli.main.find_yaml", return_value=yaml_path):
        with patch("cli.commands.close_session.Groq") as MockGroq:
            client = MockGroq.return_value
            mock_resp = MagicMock()
            mock_resp.choices[0].message.content = "Sprint review complete."
            client.chat.completions.create.return_value = mock_resp

            result = runner.invoke(app, ["close-session"])

    assert result.exit_code == 0, result.output
    # Verify Groq was initialised with the key from .env (not from real env)
    MockGroq.assert_called_once_with(api_key="key-from-dotenv", timeout=30.0)
    # Verify the model from llm: section was used
    first_call = client.chat.completions.create.call_args_list[0]
    assert first_call.kwargs.get("model") == "test-model"

    # Cleanup env var set by _load_dotenv during this test
    os.environ.pop("_BL_TEST_CS_KEY", None)


def test_close_session_api_key_env_unset_exits_1_with_clear_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """api_key_env pointing to an unset var → clear error message, exit 1, no traceback."""
    yaml_path = _setup_close_session_project(tmp_path)

    # Remove the key and clear .env so it is definitely unset
    monkeypatch.delenv("_BL_TEST_CS_KEY", raising=False)
    (tmp_path / ".env").write_text("", encoding="utf-8")

    with patch("cli.main.find_yaml", return_value=yaml_path):
        result = runner.invoke(app, ["close-session"])

    assert result.exit_code == 1
    assert "_BL_TEST_CS_KEY" in result.output
    assert "Traceback" not in result.output
