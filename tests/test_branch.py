"""Tests for Brick 8.6 — bricklayer branch command and build main guard."""

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

from cli.commands.branch import _git_create_checkout, _slugify, run_branch  # noqa: E402
from cli.commands.build import (  # noqa: E402
    _get_current_branch,
    _merge_brick_branch,
    run_verdict,
)
from cli.main import app  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_STATE: dict = {
    "current_brick": "Brick 8.6 - branching workflow",
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

_SPEC_TEXT = """\
BRICK: Brick 8.6 - branching workflow

WHAT:
  Branching workflow.

GATE:
  RUNS

FILES:
- cli/commands/branch.py
- cli/commands/build.py
- cli/main.py
- tests/test_branch.py
- bricklayer/spec.md
"""


def _make_project(
    tmp_path: Path,
    next_action: str = "skeptic_packet_ready",
    current_branch: str = "brick/8.6-branching-workflow",
) -> Path:
    brick_dir = tmp_path / "bricklayer"
    brick_dir.mkdir(exist_ok=True)
    state = {**_BASE_STATE, "next_action": next_action, "current_branch": current_branch}
    (brick_dir / "state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    (brick_dir / "spec.md").write_text(_SPEC_TEXT, encoding="utf-8")
    return tmp_path


def _read_state(root: Path) -> dict:
    return json.loads((root / "bricklayer/state.json").read_text(encoding="utf-8"))


def _mock_git_success(*_args, **_kwargs) -> MagicMock:
    m = MagicMock()
    m.returncode = 0
    m.stdout = ""
    return m


def _mock_git_fail(*_args, **_kwargs) -> MagicMock:
    m = MagicMock()
    m.returncode = 1
    m.stdout = "fatal: git error"
    return m


# ---------------------------------------------------------------------------
# _slugify
# ---------------------------------------------------------------------------


def test_slugify_basic() -> None:
    assert _slugify("bricklayer-pause") == "bricklayer-pause"


def test_slugify_spaces() -> None:
    assert _slugify("session management") == "session-management"


def test_slugify_uppercase() -> None:
    assert _slugify("MyFeature") == "myfeature"


def test_slugify_special_chars() -> None:
    assert _slugify("v2.0 (new)") == "v2-0-new"


# ---------------------------------------------------------------------------
# _git_create_checkout
# ---------------------------------------------------------------------------


def test_git_create_checkout_calls_checkout_b(tmp_path: Path) -> None:
    with patch("cli.commands.branch._subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="")
        _git_create_checkout(tmp_path, "brick/9-test")
    cmd = mock_run.call_args[0][0]
    assert cmd == ["git", "checkout", "-b", "brick/9-test"]


def test_git_create_checkout_returns_nonzero_on_failure(tmp_path: Path) -> None:
    with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_fail):
        code, output = _git_create_checkout(tmp_path, "brick/9-test")
    assert code == 1
    assert "fatal" in output


# ---------------------------------------------------------------------------
# run_branch — brick branch
# ---------------------------------------------------------------------------


def test_run_branch_brick_creates_correct_name(tmp_path: Path) -> None:
    """brick/N-name is constructed from number + slugified name."""
    _make_project(tmp_path)

    with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
        result = run_branch(tmp_path, "9", "bricklayer-pause", feature=False)

    assert result == 0


def test_run_branch_brick_updates_state(tmp_path: Path) -> None:
    """current_branch is written to state.json."""
    _make_project(tmp_path)

    with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
        run_branch(tmp_path, "9", "bricklayer pause", feature=False)

    assert _read_state(tmp_path)["current_branch"] == "brick/9-bricklayer-pause"


def test_run_branch_brick_prints_branch_name(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Output contains the created branch name."""
    _make_project(tmp_path)

    with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
        run_branch(tmp_path, "9", "bricklayer-pause", feature=False)

    assert "brick/9-bricklayer-pause" in capsys.readouterr().out


def test_run_branch_brick_missing_number_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Missing number → error, exit 1."""
    _make_project(tmp_path)
    result = run_branch(tmp_path, None, "some-name", feature=False)
    assert result == 1
    assert "Traceback" not in capsys.readouterr().err


def test_run_branch_brick_missing_name_exits_one(tmp_path: Path) -> None:
    """Missing name → error, exit 1."""
    _make_project(tmp_path)
    result = run_branch(tmp_path, "9", None, feature=False)
    assert result == 1


# ---------------------------------------------------------------------------
# run_branch — feature branch
# ---------------------------------------------------------------------------


def test_run_branch_feature_creates_correct_name(tmp_path: Path) -> None:
    """feature/name is constructed when --feature is set."""
    _make_project(tmp_path)

    with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
        result = run_branch(tmp_path, "session-management", None, feature=True)

    assert result == 0


def test_run_branch_feature_updates_state(tmp_path: Path) -> None:
    """current_branch is set to feature/name in state.json."""
    _make_project(tmp_path)

    with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
        run_branch(tmp_path, "session-management", None, feature=True)

    assert _read_state(tmp_path)["current_branch"] == "feature/session-management"


def test_run_branch_feature_missing_name_exits_one(tmp_path: Path) -> None:
    """--feature with no name → error, exit 1."""
    _make_project(tmp_path)
    result = run_branch(tmp_path, None, None, feature=True)
    assert result == 1


# ---------------------------------------------------------------------------
# run_branch — branch already exists
# ---------------------------------------------------------------------------


def test_run_branch_already_exists_exits_one(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Existing branch → clear error, exit 1, no overwrite."""
    _make_project(tmp_path)

    def already_exists(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 128
        m.stdout = "fatal: A branch named 'brick/9-test' already exists."
        return m

    with patch("cli.commands.branch._subprocess.run", side_effect=already_exists):
        result = run_branch(tmp_path, "9", "test", feature=False)

    assert result == 1
    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


def test_run_branch_already_exists_state_unchanged(tmp_path: Path) -> None:
    """On branch-exists error, state.json is not modified."""
    _make_project(tmp_path)
    before = _read_state(tmp_path)["current_branch"]

    with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_fail):
        run_branch(tmp_path, "9", "test", feature=False)

    assert _read_state(tmp_path)["current_branch"] == before


# ---------------------------------------------------------------------------
# _get_current_branch
# ---------------------------------------------------------------------------


def test_get_current_branch_returns_branch_name(tmp_path: Path) -> None:
    def fake_git(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = "brick/8.6-branching-workflow\n"
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=fake_git):
        result = _get_current_branch(tmp_path)

    assert result == "brick/8.6-branching-workflow"


def test_get_current_branch_returns_none_on_failure(tmp_path: Path) -> None:
    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_fail):
        result = _get_current_branch(tmp_path)

    assert result is None


# ---------------------------------------------------------------------------
# _merge_brick_branch
# ---------------------------------------------------------------------------


def test_merge_brick_branch_returns_zero_on_success(tmp_path: Path) -> None:
    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_success):
        code, msg = _merge_brick_branch(tmp_path, "brick/9-test")
    assert code == 0
    assert "brick/9-test" in msg
    assert "main" in msg


def test_merge_brick_branch_returns_one_on_checkout_failure(tmp_path: Path) -> None:
    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_fail):
        code, msg = _merge_brick_branch(tmp_path, "brick/9-test")
    assert code == 1
    assert "Traceback" not in msg


def test_merge_brick_branch_returns_one_on_merge_failure(tmp_path: Path) -> None:
    call_count = [0]

    def side_effect(cmd, **kwargs):
        call_count[0] += 1
        m = MagicMock()
        if call_count[0] == 1:  # git checkout main — success
            m.returncode = 0
            m.stdout = ""
        else:  # git merge — fail
            m.returncode = 1
            m.stdout = "CONFLICT: merge conflict"
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
        code, msg = _merge_brick_branch(tmp_path, "brick/9-test")

    assert code == 1
    assert "Traceback" not in msg


def test_merge_brick_branch_message_format(tmp_path: Path) -> None:
    with patch("cli.commands.build._subprocess.run", side_effect=_mock_git_success):
        _, msg = _merge_brick_branch(tmp_path, "brick/9-test")
    assert "Merged brick/9-test → main" in msg
    assert "Branch deleted" in msg


# ---------------------------------------------------------------------------
# run_verdict PASS — branch merge logic
# ---------------------------------------------------------------------------


def _mock_get_branch(name: str):
    """Return a side_effect that reports a specific branch for git rev-parse."""
    def side_effect(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        if cmd[:3] == ["git", "rev-parse", "--abbrev-ref"]:
            m.stdout = name + "\n"
        else:
            m.stdout = ""
        return m
    return side_effect


def test_verdict_pass_brick_branch_merges_to_main(tmp_path: Path) -> None:
    """PASS on brick/* calls _merge_brick_branch."""
    root = _make_project(tmp_path, current_branch="brick/8.6-branching-workflow")
    merged = []

    def fake_git(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = ""
        if cmd[:2] == ["git", "merge"]:
            merged.append(cmd)
        if cmd[:3] == ["git", "rev-parse", "--abbrev-ref"]:
            m.stdout = "brick/8.6-branching-workflow\n"
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=fake_git):
        with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
            result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert result == 0
    assert any("--no-ff" in str(c) for c in merged)


def test_verdict_pass_brick_branch_prints_merge_message(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """PASS on brick/* prints merge confirmation."""
    root = _make_project(tmp_path)

    with patch("cli.commands.build._subprocess.run", side_effect=_mock_get_branch("brick/8.6-test")):
        with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
            run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    out = capsys.readouterr().out
    assert "Merged" in out
    assert "main" in out


def test_verdict_pass_feature_branch_no_merge(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """PASS on feature/* does NOT merge; prints feature message."""
    root = _make_project(tmp_path)
    merge_calls = []

    def fake_git(cmd, **kwargs):
        m = MagicMock()
        m.returncode = 0
        m.stdout = "feature/session-management\n" if cmd[:3] == ["git", "rev-parse", "--abbrev-ref"] else ""
        if cmd[:2] == ["git", "merge"]:
            merge_calls.append(cmd)
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=fake_git):
        with patch("cli.commands.build.run_tool", return_value=(0, "COMPLETED\n")):
            result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert result == 0
    assert not merge_calls
    out = capsys.readouterr().out
    assert "Feature branch open" in out


def test_verdict_pass_feature_branch_state_advances(tmp_path: Path) -> None:
    """PASS on feature/* still calls update_state --complete."""
    root = _make_project(tmp_path)
    update_called = []

    def fake_run_tool(tool_path, args, cwd=None):
        update_called.append(args)
        s = json.loads((root / "bricklayer/state.json").read_text())
        s["next_action"] = "brick_complete"
        (root / "bricklayer/state.json").write_text(json.dumps(s, indent=2))
        return 0, "COMPLETED\n"

    with patch("cli.commands.build._subprocess.run", side_effect=_mock_get_branch("feature/session-management")):
        with patch("cli.commands.build.run_tool", side_effect=fake_run_tool):
            result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert result == 0
    assert update_called


def test_verdict_pass_merge_failure_exits_one(tmp_path: Path) -> None:
    """PASS: merge failure → exit 1, state not advanced."""
    root = _make_project(tmp_path)
    update_called = []

    call_count = [0]

    def side_effect(cmd, **kwargs):
        call_count[0] += 1
        m = MagicMock()
        if cmd[:3] == ["git", "rev-parse", "--abbrev-ref"]:
            m.returncode = 0
            m.stdout = "brick/8.6-test\n"
        elif cmd[:2] == ["git", "add"]:
            m.returncode = 0
            m.stdout = ""
        elif cmd[:2] == ["git", "commit"]:
            m.returncode = 0
            m.stdout = ""
        elif cmd[:2] == ["git", "checkout"]:
            m.returncode = 0
            m.stdout = ""
        elif cmd[:2] == ["git", "merge"]:
            m.returncode = 1
            m.stdout = "CONFLICT: merge conflict"
        else:
            m.returncode = 0
            m.stdout = ""
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
        with patch("cli.commands.build.run_tool") as mock_tool:
            result = run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    assert result == 1
    mock_tool.assert_not_called()


def test_verdict_pass_merge_failure_no_traceback(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """PASS: merge failure → no raw traceback."""
    root = _make_project(tmp_path)

    def side_effect(cmd, **kwargs):
        m = MagicMock()
        if cmd[:3] == ["git", "rev-parse", "--abbrev-ref"]:
            m.returncode = 0
            m.stdout = "brick/8.6-test\n"
        elif cmd[:2] == ["git", "merge"]:
            m.returncode = 1
            m.stdout = "CONFLICT"
        else:
            m.returncode = 0
            m.stdout = ""
        return m

    with patch("cli.commands.build._subprocess.run", side_effect=side_effect):
        with patch("cli.commands.build.run_tool", return_value=(0, "")):
            run_verdict(root, _CONFIG_WITH_STATE, "PASS")

    combined = capsys.readouterr()
    assert "Traceback" not in combined.out
    assert "Traceback" not in combined.err


# ---------------------------------------------------------------------------
# Build main guard
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


def test_cli_build_on_main_exits_one(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build` on main → exit 1."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build._subprocess.run", side_effect=_mock_get_branch("main")):
            result = cli_runner.invoke(app, ["build"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1


def test_cli_build_on_main_prints_branch_hint(tmp_path: Path) -> None:
    """CliRunner: main guard prints helpful branch creation hint."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build._subprocess.run", side_effect=_mock_get_branch("main")):
            result = cli_runner.invoke(app, ["build"])
    finally:
        os.chdir(old_cwd)
    assert "main" in result.output
    assert "bricklayer branch" in result.output


def test_cli_build_on_main_no_traceback(tmp_path: Path) -> None:
    """CliRunner: main guard → no raw traceback."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build._subprocess.run", side_effect=_mock_get_branch("main")):
            result = cli_runner.invoke(app, ["build"])
    finally:
        os.chdir(old_cwd)
    assert "Traceback" not in result.output


def test_cli_build_on_non_main_proceeds(tmp_path: Path) -> None:
    """CliRunner: `bricklayer build` on non-main branch → no guard trigger (exit 0)."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.build._subprocess.run", side_effect=_mock_get_branch("brick/8.6-test")):
            result = cli_runner.invoke(app, ["build"])
    finally:
        os.chdir(old_cwd)
    # Should not exit 1 due to main guard (may exit 0 or 1 for other reasons)
    assert result.output != ""
    assert "You are on main" not in result.output


# ---------------------------------------------------------------------------
# CliRunner: branch command
# ---------------------------------------------------------------------------


def test_cli_branch_brick_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer branch 9 bricklayer-pause` → exit 0."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
            result = cli_runner.invoke(app, ["branch", "9", "bricklayer-pause"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_branch_brick_output_contains_branch_name(tmp_path: Path) -> None:
    """CliRunner: branch command prints created branch name."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
            result = cli_runner.invoke(app, ["branch", "9", "bricklayer-pause"])
    finally:
        os.chdir(old_cwd)
    assert "brick/9-bricklayer-pause" in result.output


def test_cli_branch_feature_exits_zero(tmp_path: Path) -> None:
    """CliRunner: `bricklayer branch --feature session-management` → exit 0."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
            result = cli_runner.invoke(app, ["branch", "--feature", "session-management"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 0


def test_cli_branch_feature_output_contains_branch_name(tmp_path: Path) -> None:
    """CliRunner: feature branch command prints created branch name."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_success):
            result = cli_runner.invoke(app, ["branch", "--feature", "session-management"])
    finally:
        os.chdir(old_cwd)
    assert "feature/session-management" in result.output


def test_cli_branch_already_exists_exits_one(tmp_path: Path) -> None:
    """CliRunner: branch already exists → exit 1."""
    _cli_setup(tmp_path)
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with patch("cli.commands.branch._subprocess.run", side_effect=_mock_git_fail):
            result = cli_runner.invoke(app, ["branch", "9", "test"])
    finally:
        os.chdir(old_cwd)
    assert result.exit_code == 1
    assert "Traceback" not in result.output
