"""Tests for cli/config.py — YAML loader, path validation, and .env loading."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Ensure repo root is on sys.path so `cli` is importable
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.config import _load_dotenv, load_and_validate  # noqa: E402
from cli.commands.close_session import (  # noqa: E402
    DEFAULT_LLM_API_KEY_ENV,
    DEFAULT_LLM_HEAVY_MODEL,
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_PROVIDER,
    _read_llm_config,
)


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
# Happy path — all paths valid
# ---------------------------------------------------------------------------


def test_happy_path_all_paths_valid(tmp_path: Path) -> None:
    """All declared paths exist → load_and_validate returns config dict."""
    _make_file(tmp_path, "system-prompts/plan.md")
    _make_file(tmp_path, "tools/verify.py")

    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  plan: system-prompts/plan.md\n"
        "tools:\n  verify: tools/verify.py\n"
        "agents: {}\n",
    )

    result = load_and_validate(yaml_path)
    assert isinstance(result, dict)
    assert "phases" in result
    assert "tools" in result


def test_happy_path_empty_sections(tmp_path: Path) -> None:
    """Empty sections are valid — no files to check."""
    yaml_path = _write_yaml(tmp_path, "phases: {}\ntools: {}\nagents: {}\n")
    result = load_and_validate(yaml_path)
    assert result == {"phases": {}, "tools": {}, "agents": {}}


# ---------------------------------------------------------------------------
# Missing path → error message + exit 1
# ---------------------------------------------------------------------------


def test_missing_path_prints_error_and_exits(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """One path declared but absent → human-readable error, exit 1."""
    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  plan: system-prompts/nonexistent.md\n"
        "tools: {}\nagents: {}\n",
    )

    with pytest.raises(SystemExit) as exc_info:
        load_and_validate(yaml_path)

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "Missing: system-prompts/nonexistent.md" in err
    assert "check bricklayer.yaml" in err


def test_missing_path_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Error output must not contain 'Traceback'."""
    yaml_path = _write_yaml(
        tmp_path,
        "tools:\n  missing_tool: tools/ghost.py\n"
        "phases: {}\nagents: {}\n",
    )

    with pytest.raises(SystemExit):
        load_and_validate(yaml_path)

    err = capsys.readouterr().err
    assert "Traceback" not in err


def test_multiple_missing_paths_all_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """All missing paths are reported, not just the first one."""
    yaml_path = _write_yaml(
        tmp_path,
        "phases:\n  a: missing/a.md\n  b: missing/b.md\n"
        "tools: {}\nagents: {}\n",
    )

    with pytest.raises(SystemExit) as exc_info:
        load_and_validate(yaml_path)

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "missing/a.md" in err
    assert "missing/b.md" in err


# ---------------------------------------------------------------------------
# Missing YAML file entirely → exit 1
# ---------------------------------------------------------------------------


def test_missing_yaml_file_exits_with_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """No bricklayer.yaml → human-readable message, exit 1."""
    yaml_path = tmp_path / "bricklayer.yaml"  # does NOT exist

    with pytest.raises(SystemExit) as exc_info:
        load_and_validate(yaml_path)

    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "bricklayer.yaml not found at repo root" in err


def test_missing_yaml_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Missing yaml error must not include 'Traceback'."""
    yaml_path = tmp_path / "bricklayer.yaml"

    with pytest.raises(SystemExit):
        load_and_validate(yaml_path)

    err = capsys.readouterr().err
    assert "Traceback" not in err


# ---------------------------------------------------------------------------
# .env auto-loading (_load_dotenv)
# ---------------------------------------------------------------------------


def test_dotenv_loads_key_value(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """KEY=VALUE in .env is loaded into os.environ."""
    monkeypatch.delenv("_BL_TEST_KEY_BRICK25", raising=False)
    (tmp_path / ".env").write_text("_BL_TEST_KEY_BRICK25=hello\n", encoding="utf-8")
    _load_dotenv(tmp_path)
    assert os.environ.get("_BL_TEST_KEY_BRICK25") == "hello"


def test_dotenv_absent_silent_skip(tmp_path: Path) -> None:
    """.env absent → no error, no exception."""
    _load_dotenv(tmp_path)  # must not raise


def test_dotenv_does_not_overwrite_existing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Existing os.environ key is NOT overwritten by .env value."""
    monkeypatch.setenv("_BL_TEST_NOOVERWRITE_BRICK25", "original")
    (tmp_path / ".env").write_text(
        "_BL_TEST_NOOVERWRITE_BRICK25=new_value\n", encoding="utf-8"
    )
    _load_dotenv(tmp_path)
    assert os.environ["_BL_TEST_NOOVERWRITE_BRICK25"] == "original"


def test_dotenv_malformed_line_skips_with_warning_other_lines_load(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Malformed line (no '=') is skipped with warning; subsequent lines still load."""
    monkeypatch.delenv("_BL_TEST_GOOD_BRICK25", raising=False)
    (tmp_path / ".env").write_text(
        "MALFORMED_LINE_NO_EQUALS\n_BL_TEST_GOOD_BRICK25=loaded\n", encoding="utf-8"
    )
    _load_dotenv(tmp_path)
    err = capsys.readouterr().err
    assert "warning" in err.lower() or "malformed" in err.lower()
    assert os.environ.get("_BL_TEST_GOOD_BRICK25") == "loaded"


# ---------------------------------------------------------------------------
# LLM config (_read_llm_config)
# ---------------------------------------------------------------------------


def _write_llm_yaml(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "bricklayer.yaml"
    p.write_text(content, encoding="utf-8")
    return p


def test_llm_config_present_no_deprecation_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """llm: section present → correct values returned, no deprecation warning."""
    yaml_path = _write_llm_yaml(
        tmp_path,
        "llm:\n  provider: groq\n  model: my-model\n"
        "  heavy_model: my-heavy\n  api_key_env: MY_KEY\n",
    )
    result = _read_llm_config(yaml_path)
    err = capsys.readouterr().err
    assert "warning" not in err.lower()
    assert result["model"] == "my-model"
    assert result["heavy_model"] == "my-heavy"
    assert result["api_key_env"] == "MY_KEY"
    assert result["provider"] == "groq"


def test_llm_config_absent_uses_groq_defaults_with_warning(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """llm: section absent → Groq defaults returned, deprecation warning on stderr."""
    yaml_path = _write_llm_yaml(tmp_path, "phases: {}\ntools: {}\n")
    result = _read_llm_config(yaml_path)
    err = capsys.readouterr().err
    assert "warning" in err.lower()
    assert result["provider"] == DEFAULT_LLM_PROVIDER
    assert result["model"] == DEFAULT_LLM_MODEL
    assert result["heavy_model"] == DEFAULT_LLM_HEAVY_MODEL
    assert result["api_key_env"] == DEFAULT_LLM_API_KEY_ENV


def test_llm_config_unsupported_provider_exits_1_with_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """provider: openai → 'not yet supported' error, exit 1."""
    yaml_path = _write_llm_yaml(
        tmp_path, "llm:\n  provider: openai\n  api_key_env: OPENAI_KEY\n"
    )
    with pytest.raises(SystemExit) as exc_info:
        _read_llm_config(yaml_path)
    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "openai" in err.lower()
    assert "not yet supported" in err.lower()


def test_llm_config_unsupported_provider_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Unsupported provider error must not show a Python traceback."""
    yaml_path = _write_llm_yaml(
        tmp_path, "llm:\n  provider: anthropic\n  api_key_env: ANTHROPIC_KEY\n"
    )
    with pytest.raises(SystemExit):
        _read_llm_config(yaml_path)
    err = capsys.readouterr().err
    assert "Traceback" not in err
