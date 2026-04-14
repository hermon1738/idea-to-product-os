"""Tests for Brick 8.5 — auto-stage (make_skeptic_packet.py) and auto-commit (run_verdict PASS)."""

from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest
from typer.testing import CliRunner

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cli.commands.build import (  # noqa: E402
    _git_commit_spec,
    _parse_brick_name,
    _parse_spec_files,
    run_verdict,
)
from cli.main import app  # noqa: E402

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

_SPEC_TEXT = """\
BRICK: Brick 8.5 - git fixes (auto-stage + auto-commit on verdict)

WHAT:
  Git fixes.

GATE:
  RUNS

FILES:
- bricklayer/tools/make_skeptic_packet.py
- cli/commands/build.py
- tests/test_git_fixes.py
- bricklayer/spec.md
"""

_BASE_STATE: dict = {
    "current_brick": "Brick 8.5 - git fixes",
    "status": "IN_PROGRESS",
    "loop_count": 0,
    "last_gate_failed": None,
    "completed_bricks": [],
    "next_action": "skeptic_packet_ready",
    "last_test_run": {
        "command": "python3 -m pytest -q",
        "status": "PASS",
        "exit_code": 0,
        "artifact": "skeptic_packet/test_output.txt",
    },
}

_CONFIG_WITH_STATE: dict = {"tools": {"state": "bricklayer/tools/update_state.py"}}


def _make_project(tmp_path: Path, next_action: str = "skeptic_packet_ready") -> Path:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    state = {**_BASE_STATE, "next_action": next_action}
    (brick_dir / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    (brick_dir / "spec.md").write_text(_SPEC_TEXT, encoding="utf-8")
    return tmp_path


def _read_state(root: Path) -> dict:
    return json.loads((root / "bricklayer/state.json").read_text(encoding="utf-8"))


def _load_make_skeptic_packet():
    """Import make_skeptic_packet from bricklayer/tools/ fresh each time."""
    tools_dir = str(ROOT / "bricklayer" / "tools")
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    sys.modules.pop("make_skeptic_packet", None)
    return importlib.import_module("make_skeptic_packet")


# ---------------------------------------------------------------------------
# _parse_brick_name
# ---------------------------------------------------------------------------


def test_parse_brick_name_extracts_name() -> None:
    """BRICK: line is parsed and returned."""
    text = "BRICK: Brick 8.5 - git fixes\n\nWHAT:\n  stuff\n"
    assert _parse_brick_name(text) == "Brick 8.5 - git fixes"


def test_parse_brick_name_missing_returns_unknown() -> None:
    """Missing BRICK: line returns fallback."""
    assert _parse_brick_name("no brick line here\n") == "unknown brick"


# ---------------------------------------------------------------------------
# _parse_spec_files
# ---------------------------------------------------------------------------


def test_parse_spec_files_returns_all_files() -> None:
    files = _parse_spec_files(_SPEC_TEXT)
    assert "bricklayer/tools/make_skeptic_packet.py" in files
    assert "cli/commands/build.py" in files
    assert "tests/test_git_fixes.py" in files
    assert "bricklayer/spec.md" in files


def test_parse_spec_files_empty_when_no_section() -> None:
    assert _parse_spec_files("BRICK: X\n\nWHAT:\n  y\n") == []


# ---------------------------------------------------------------------------
# _git_commit_spec — unit tests (subprocess mocked)
# ---------------------------------------------------------------------------


def _mock_git_success(*_args, **_kwargs):
    m = MagicMock()
    m.returncode = 0
    m.stdout = "[main abc123] feat(brick-8.5): git fixes\n"
    return m


def test_git_commit_spec_calls_git_add_then_commit(tmp_path: Path) -> None:
    """git add is called before git commit."""
    call_cmds: list[list[str]] = []

    def recorder(cmd, **kwargs):
        call_cmds.append(cmd[:2])
        m = MagicMock()
        m.returncode = 0
        m.stdout = ""
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=recorder):
        _git_commit_spec(tmp_path, "Brick 8.5 - git fixes", ["file.py"])

    assert call_cmds[0] == ["git", "add"]
    assert call_cmds[1] == ["git", "commit"]


def test_git_commit_spec_passes_files_to_add(tmp_path: Path) -> None:
    """All files are passed to git add."""
    files = ["cli/commands/build.py", "bricklayer/spec.md"]

    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_success) as mock_run:
        _git_commit_spec(tmp_path, "Brick 8.5 - git fixes", files)

    add_cmd = mock_run.call_args_list[0][0][0]
    assert "cli/commands/build.py" in add_cmd
    assert "bricklayer/spec.md" in add_cmd


def test_git_commit_spec_message_contains_brick_number(tmp_path: Path) -> None:
    """Commit message uses feat(brick-N) format."""
    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_success) as mock_run:
        _git_commit_spec(tmp_path, "Brick 8.5 - git fixes", ["f.py"])

    commit_cmd = mock_run.call_args_list[1][0][0]
    msg_idx = commit_cmd.index("-m") + 1
    msg = commit_cmd[msg_idx]
    assert "feat(brick-8.5):" in msg


def test_git_commit_spec_message_contains_co_authored_by(tmp_path: Path) -> None:
    """Commit message includes Co-Authored-By trailer."""
    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_success) as mock_run:
        _git_commit_spec(tmp_path, "Brick 8.5 - git fixes", ["f.py"])

    commit_cmd = mock_run.call_args_list[1][0][0]
    msg_idx = commit_cmd.index("-m") + 1
    assert "Co-Authored-By" in commit_cmd[msg_idx]


def test_git_commit_spec_returns_zero_on_success(tmp_path: Path) -> None:
    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_success):
        code, _ = _git_commit_spec(tmp_path, "Brick 8.5 - git fixes", ["f.py"])
    assert code == 0


def test_git_commit_spec_returns_nonzero_on_commit_failure(tmp_path: Path) -> None:
    def side_effect(cmd, **kwargs):
        m = MagicMock()
        if cmd[:2] == ["git", "add"]:
            m.returncode = 0
            m.stdout = ""
        else:
            m.returncode = 1
            m.stdout = "nothing to commit, working tree clean\n"
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
        code, output = _git_commit_spec(tmp_path, "Brick 8.5 - git fixes", ["f.py"])
    assert code == 1
    assert "nothing to commit" in output


def test_git_commit_spec_aborts_if_add_fails(tmp_path: Path) -> None:
    """If git add fails, git commit is never called."""
    call_cmds: list[list[str]] = []

    def side_effect(cmd, **kwargs):
        call_cmds.append(cmd[:2])
        m = MagicMock()
        m.returncode = 1
        m.stdout = "add error"
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
        code, _ = _git_commit_spec(tmp_path, "Brick 8.5 - git fixes", ["f.py"])

    assert code == 1
    assert ["git", "commit"] not in call_cmds


# ---------------------------------------------------------------------------
# run_verdict PASS — auto-commit integration
# ---------------------------------------------------------------------------


def test_run_verdict_pass_runs_git_commit(tmp_path: Path) -> None:
    """PASS path calls git commit."""
    root = _make_project(tmp_path)
    call_cmds: list[list[str]] = []

    def recorder(cmd, **kwargs):
        call_cmds.append(cmd[:2])
        m = MagicMock()
        m.returncode = 0
        m.stdout = ""
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=recorder):
        with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
            run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert ["git", "commit"] in call_cmds


def test_run_verdict_pass_commit_failure_exits_one(tmp_path: Path) -> None:
    """PASS: git commit fails → exit 1."""
    root = _make_project(tmp_path)

    def side_effect(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0 if cmd[:2] == ["git", "add"] else 1
        m.stdout = "nothing to commit, working tree clean\n"
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
        with patch("cli.commands.build.run_tool") as mock_tool:
            result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert result == 1
    mock_tool.assert_not_called()


def test_run_verdict_pass_commit_failure_state_not_advanced(tmp_path: Path) -> None:
    """PASS: git commit fails → state.json next_action unchanged."""
    root = _make_project(tmp_path)
    before = _read_state(root)["next_action"]

    def side_effect(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0 if cmd[:2] == ["git", "add"] else 1
        m.stdout = ""
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
        run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert _read_state(root)["next_action"] == before


def test_run_verdict_pass_state_advances_after_commit(tmp_path: Path) -> None:
    """PASS: update_state is called after commit succeeds."""
    root = _make_project(tmp_path)
    update_state_called = []

    def fake_run_tool(tool_path, args, cwd=None):
        update_state_called.append(args)
        state_path = root / "bricklayer" / "state.json"
        s = json.loads(state_path.read_text())
        s["next_action"] = "brick_complete"
        state_path.write_text(json.dumps(s, indent=2))
        return 0, "COMPLETED\n"

    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_success):
        with patch("cli.commands.build.run_tool", side_effect=fake_run_tool):
            result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert result == 0
    assert update_state_called
    assert "--complete" in update_state_called[0]
    assert _read_state(root)["next_action"] == "brick_complete"


def test_run_verdict_fail_not_affected(tmp_path: Path) -> None:
    """FAIL path: git commit is never called."""
    root = _make_project(tmp_path)

    with patch("cli.commands.build._subprocess.run") as mock_run:
        result = run_verdict(root, _CONFIG_WITH_STATE, "FAIL")

    assert result == 1
    mock_run.assert_not_called()


# ---------------------------------------------------------------------------
# make_skeptic_packet._git_add_spec_files — unit tests
# ---------------------------------------------------------------------------


def test_auto_stage_calls_git_add_with_spec_files(tmp_path: Path) -> None:
    """_git_add_spec_files calls git add with all listed files."""
    mod = _load_make_skeptic_packet()
    files = ["cli/commands/build.py", "bricklayer/spec.md"]

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        mod._git_add_spec_files(tmp_path, files)

    mock_run.assert_called_once()
    cmd = mock_run.call_args[0][0]
    assert cmd[:3] == ["git", "add", "--"]
    assert "cli/commands/build.py" in cmd
    assert "bricklayer/spec.md" in cmd


def test_auto_stage_non_spec_file_not_staged(tmp_path: Path) -> None:
    """Files not in FILES list are not passed to git add."""
    mod = _load_make_skeptic_packet()
    spec_files = ["cli/commands/build.py"]  # only these should be staged

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        mod._git_add_spec_files(tmp_path, spec_files)

    cmd = mock_run.call_args[0][0]
    assert "tests/some_other_file.py" not in cmd
    assert "bricklayer/state.json" not in cmd


def test_auto_stage_skips_when_no_files(tmp_path: Path) -> None:
    """_git_add_spec_files does nothing when files list is empty."""
    mod = _load_make_skeptic_packet()

    with patch("subprocess.run") as mock_run:
        mod._git_add_spec_files(tmp_path, [])

    mock_run.assert_not_called()


def test_graph_audit_artifacts_copied_when_graphify_present(tmp_path: Path) -> None:
    """Graphify outputs are copied into skeptic_packet and reflected in manifest."""
    mod = _load_make_skeptic_packet()
    graphify_out = tmp_path / "graphify-out"
    packet_dir = tmp_path / "skeptic_packet"
    graphify_out.mkdir(parents=True)
    packet_dir.mkdir(parents=True)
    (graphify_out / "GRAPH_REPORT.md").write_text("report", encoding="utf-8")
    (graphify_out / "manifest.json").write_text('{"ok": true}', encoding="utf-8")
    (graphify_out / "graph.json").write_text('{"nodes": []}', encoding="utf-8")

    with patch.object(mod, "ROOT", tmp_path), patch.object(mod, "PACKET_DIR", packet_dir), patch.object(
        mod, "GRAPHIFY_OUT_DIR", graphify_out
    ), patch.object(mod, "GRAPH_AUDIT_MANIFEST", packet_dir / "graph_audit_manifest.json"):
        copied, manifest = mod.write_graph_audit_artifacts()

    copied_names = {path.name for path in copied}
    assert copied_names == {"graph_audit_report.md", "graph_manifest.json", "graph.json"}
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["graphify_detected"] is True
    assert payload["missing_required_artifacts"] == []


def test_graph_audit_manifest_written_when_graphify_missing(tmp_path: Path) -> None:
    """Manifest is always emitted so skeptic can verify Graphify presence state."""
    mod = _load_make_skeptic_packet()
    packet_dir = tmp_path / "skeptic_packet"
    packet_dir.mkdir(parents=True)

    with patch.object(mod, "ROOT", tmp_path), patch.object(mod, "PACKET_DIR", packet_dir), patch.object(
        mod, "GRAPHIFY_OUT_DIR", tmp_path / "graphify-out"
    ), patch.object(mod, "GRAPH_AUDIT_MANIFEST", packet_dir / "graph_audit_manifest.json"):
        copied, manifest = mod.write_graph_audit_artifacts()

    assert copied == []
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["graphify_detected"] is False
    assert payload["copied_artifacts"] == []


# ---------------------------------------------------------------------------
# CliRunner integration
# ---------------------------------------------------------------------------

cli_runner = CliRunner()


def _cli_setup(tmp_path: Path, next_action: str = "skeptic_packet_ready") -> None:
    _make_project(tmp_path, next_action=next_action)
    (tmp_path / "bricklayer.yaml").write_text(
        "phases: {}\ntools:\n  state: bricklayer/tools/update_state.py\nagents: {}\n",
        encoding="utf-8",
    )
    tools_dir = tmp_path / "bricklayer" / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    (tools_dir / "update_state.py").write_text("", encoding="utf-8")


def test_cli_pass_calls_git_commit(tmp_path: Path) -> None:
    """CliRunner: --verdict PASS triggers git commit."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    git_calls: list[list[str]] = []

    def recorder(cmd, **kwargs):
        git_calls.append(cmd[:2])
        m = MagicMock()
        m.returncode = 0
        m.stdout = "[main abc] feat(brick-8.5): git fixes\n"
        return m

    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build._subprocess.run", side_effect=recorder):
            with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
                result = cli_runner.invoke(app, ["build", "--verdict", "PASS"])
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 0
    assert ["git", "commit"] in git_calls


def test_cli_pass_commit_failure_exits_one(tmp_path: Path) -> None:
    """CliRunner: --verdict PASS with failing commit exits 1."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()

    def side_effect(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0 if cmd[:2] == ["git", "add"] else 1
        m.stdout = "nothing to commit, working tree clean\n"
        return m

    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
            result = cli_runner.invoke(app, ["build", "--verdict", "PASS"])
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 1
