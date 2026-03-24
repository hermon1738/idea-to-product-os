"""Build command: parses bricklayer/spec.md and handles all build flags."""

from __future__ import annotations

import json as _json
import re
import subprocess as _subprocess
from pathlib import Path
from typing import Any

import typer

from cli.runner import get_tool_path, run_tool
from cli.state import write as state_write

SPEC_RELPATH = "bricklayer/spec.md"
STATE_RELPATH = "bricklayer/state.json"
VERDICT_RELPATH = "bricklayer/skeptic_verdict.md"
TOOLS_CWD_RELPATH = "bricklayer"

_RESCOPE_THRESHOLD = 3

# The 6 contract fields, in display order.
CONTRACT_FIELDS = ["WHAT", "INPUT", "OUTPUT", "GATE", "BLOCKER", "WAVE"]

_NO_GATE_MSG = "No gate defined for this brick. Add one to spec.md."


def parse_spec(text: str) -> dict[str, str]:
    """Parse spec.md text and return a dict of CONTRACT_FIELDS → value strings.

    A section starts with a line matching ``^WORD:`` (all-caps identifier
    followed by colon at column 0). Content continues until the next such
    header or end of file. Leading/trailing whitespace is stripped from the
    collected value.
    """
    section_re = re.compile(r"^([A-Z][A-Z0-9_]*):\s*$", re.MULTILINE)
    result: dict[str, str] = {}
    lines = text.splitlines()
    # Find all section-header positions
    headers: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = section_re.match(line)
        if m:
            headers.append((i, m.group(1)))

    for idx, (line_no, name) in enumerate(headers):
        if name not in CONTRACT_FIELDS:
            continue
        start = line_no + 1
        end = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        block = "\n".join(lines[start:end])
        result[name] = block.strip()

    return result


def run_build(root: Path) -> int:
    """Print brick contract from spec.md. Returns 0 on success, 1 on error."""
    spec_path = root / SPEC_RELPATH

    if not spec_path.exists():
        typer.echo(f"error: {SPEC_RELPATH} not found at {root}", err=True)
        return 1

    text = spec_path.read_text(encoding="utf-8")
    contract = parse_spec(text)

    gate = contract.get("GATE", "").strip()
    if not gate:
        typer.echo(_NO_GATE_MSG)
        return 1

    for field in CONTRACT_FIELDS:
        label = field.lower() + ":"
        value = contract.get(field, "(not set)").strip()
        # Indent continuation lines to align under the first line
        indent = " " * (len(label) + 1)
        value_lines = value.splitlines()
        if value_lines:
            first = value_lines[0]
            rest = ("\n" + indent).join(value_lines[1:])
            formatted = first + (("\n" + indent + rest) if rest else "")
        else:
            formatted = "(not set)"
        typer.echo(f"{label} {formatted}")

    return 0


# ---------------------------------------------------------------------------
# Flag handlers — --snapshot, --verify, --test
# ---------------------------------------------------------------------------


def _run_flag_tool(
    root: Path,
    config: dict[str, Any],
    tool_key: str,
    tool_args: list[str],
    next_action_value: str,
) -> int:
    """Generic flag handler: resolve tool, run it, update state on success."""
    tool_path = get_tool_path(config, tool_key, root)
    if tool_path is None:
        typer.echo(
            f"error: '{tool_key}' tool not defined in bricklayer.yaml",
            err=True,
        )
        return 1

    exit_code, output = run_tool(tool_path, tool_args, cwd=root / TOOLS_CWD_RELPATH)
    typer.echo(output, nl=False)

    if exit_code != 0:
        typer.echo(f"error: tool exited {exit_code}", err=True)
        return 1

    state_write(root / STATE_RELPATH, {"next_action": next_action_value})
    return 0


def run_snapshot(root: Path, config: dict[str, Any]) -> int:
    """Run verify tool with --snapshot-init. Sets next_action to 'snapshot_init'."""
    return _run_flag_tool(root, config, "verify", ["--snapshot-init"], "snapshot_init")


def run_verify(root: Path, config: dict[str, Any]) -> int:
    """Run verify tool. Sets next_action to 'verify' on success."""
    return _run_flag_tool(root, config, "verify", [], "verify")


def run_test(root: Path, config: dict[str, Any]) -> int:
    """Run test tool. Sets next_action to 'tests_passed' on success."""
    return _run_flag_tool(root, config, "test", [], "tests_passed")


def run_skeptic_packet(root: Path, config: dict[str, Any]) -> int:
    """Run --skeptic-packet. Guards on next_action == 'tests_passed'."""
    state_path = root / STATE_RELPATH

    # Guard: must have passed tests first.
    # Read raw JSON so a missing/malformed next_action key is handled via .get()
    # rather than a schema ValueError from state_load.
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1
    raw_state = _json.loads(state_path.read_text(encoding="utf-8"))
    # FIX 1: .get() so a missing key is treated as wrong value, not KeyError
    if raw_state.get("next_action") != "tests_passed":
        typer.echo("Run tests first (bricklayer build --test)")
        return 1

    # Resolve tool path
    tool_path = get_tool_path(config, "skeptic", root)
    if tool_path is None:
        typer.echo("error: 'skeptic' tool not defined in bricklayer.yaml", err=True)
        return 1

    exit_code, output = run_tool(tool_path, [], cwd=root / TOOLS_CWD_RELPATH)
    typer.echo(output, nl=False)

    if exit_code != 0:
        typer.echo(f"error: skeptic-packet tool exited {exit_code}", err=True)
        return 1

    # FIX 2: confirm packet directory actually exists and is non-empty
    packet_path = root / "bricklayer" / "skeptic_packet"
    if not packet_path.exists() or not packet_path.is_dir():
        typer.echo(
            f"error: packet directory not found at {packet_path} after tool exit 0",
            err=True,
        )
        return 1
    if not any(packet_path.iterdir()):
        typer.echo(
            f"error: packet directory is empty at {packet_path}",
            err=True,
        )
        return 1

    typer.echo(f"packet: {packet_path}")
    state_write(state_path, {"next_action": "skeptic_packet_ready"})
    return 0


def _parse_brick_name(spec_text: str) -> str:
    """Extract brick name from 'BRICK: ...' line in spec.md."""
    for line in spec_text.splitlines():
        if line.startswith("BRICK:"):
            return line[len("BRICK:"):].strip()
    return "unknown brick"


def _parse_spec_files(spec_text: str) -> list[str]:
    """Return the FILES list from spec.md."""
    files: list[str] = []
    in_files = False
    for line in spec_text.splitlines():
        stripped = line.strip()
        if stripped == "FILES:":
            in_files = True
            continue
        if in_files and stripped.endswith(":") and not line.startswith(" "):
            break
        if in_files and stripped.startswith("-"):
            files.append(stripped[1:].strip())
    return files


def _git_commit_spec(root: Path, brick_name: str, files: list[str]) -> tuple[int, str]:
    """Stage spec FILES and commit with standard message. Returns (exit_code, output)."""
    add = _subprocess.run(
        ["git", "add", "--"] + files,
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        text=True,
        check=False,
    )
    if add.returncode != 0:
        return add.returncode, add.stdout or ""

    m = re.match(r"Brick\s+([\d.]+)\s*[-\u2013]\s*(.*)", brick_name, re.IGNORECASE)
    if m:
        num, desc = m.group(1), m.group(2).strip()
        subject = f"feat(brick-{num}): {desc}"
    else:
        subject = f"feat(brick): {brick_name}"

    msg = f"{subject}\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    commit = _subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        text=True,
        check=False,
    )
    return commit.returncode, commit.stdout or ""


def run_verdict(root: Path, config: dict[str, Any], verdict_value: str) -> int:
    """Run --verdict PASS|FAIL. Closes or fails the current brick."""
    if verdict_value not in ("PASS", "FAIL"):
        typer.echo(
            f"error: invalid verdict '{verdict_value}'. Use PASS or FAIL.", err=True
        )
        return 1

    state_path = root / STATE_RELPATH

    # Guard: must have a skeptic packet first
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1
    raw_state = _json.loads(state_path.read_text(encoding="utf-8"))
    if raw_state.get("next_action") != "skeptic_packet_ready":
        typer.echo(
            "Run skeptic packet first (bricklayer build --skeptic-packet)", err=True
        )
        return 1

    # --- PASS ---
    if verdict_value == "PASS":
        verdict_path = root / VERDICT_RELPATH
        verdict_path.write_text("Verdict: PASS\n", encoding="utf-8")
        typer.echo(f"written: {verdict_path}")

        # Auto-commit spec FILES before advancing state so prior-brick files
        # never pollute the next brick's verify step.
        spec_path = root / SPEC_RELPATH
        if spec_path.exists():
            spec_text = spec_path.read_text(encoding="utf-8")
            brick_name = _parse_brick_name(spec_text)
            spec_files = _parse_spec_files(spec_text)
            commit_exit, commit_output = _git_commit_spec(root, brick_name, spec_files)
            if commit_output:
                typer.echo(commit_output, nl=False)
            if commit_exit != 0:
                typer.echo("error: git commit failed — state not advanced", err=True)
                return 1

        tool_path = get_tool_path(config, "state", root)
        if tool_path is None:
            typer.echo("error: 'state' tool not defined in bricklayer.yaml", err=True)
            return 1

        exit_code, output = run_tool(tool_path, ["--complete"], cwd=root / TOOLS_CWD_RELPATH)
        typer.echo(output, nl=False)
        if exit_code != 0:
            typer.echo(f"error: update_state tool exited {exit_code}", err=True)
            return 1
        return 0

    # --- FAIL ---
    loop_count = int(raw_state.get("loop_count", 0))

    if loop_count >= _RESCOPE_THRESHOLD:
        typer.echo(
            f"RESCOPE: loop_count={loop_count} — split the brick or tighten criteria."
        )
        typer.echo("Update bricklayer/spec.md before continuing.")
        return 1

    new_count = loop_count + 1
    state_write(state_path, {"loop_count": new_count})

    if new_count >= _RESCOPE_THRESHOLD:
        typer.echo(
            f"RESCOPE: loop_count={new_count} — split the brick or tighten criteria."
        )
        typer.echo("Update bricklayer/spec.md before continuing.")
    else:
        typer.echo(
            f"FAIL: loop_count now {new_count}. Fix issues and run the build loop again."
        )
    return 1
