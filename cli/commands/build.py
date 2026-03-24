"""Build command: parse bricklayer/spec.md and handle all build pipeline flags.

WHY THIS EXISTS:
    The bricklayer pipeline has eight ordered steps — snapshot, verify, test,
    skeptic-packet, verdict — each of which invokes a different tool script
    and updates state.json on success. Without a central build module, each
    step would be its own top-level command with duplicated tool-invocation
    boilerplate, duplicated state-update logic, and no shared enforcement of
    step ordering. Centralising them here means the ordering rules (e.g.
    skeptic-packet requires tests_passed) live in one place and cannot drift.

DESIGN DECISIONS:
- Expose each pipeline step as a flag on a single ``build`` command rather
  than as separate top-level commands. Alternative was ``bricklayer snapshot``,
  ``bricklayer verify``, etc. Rejected because the shared ``--`` prefix makes
  the step sequence visible in ``--help`` output and reinforces that these
  steps form an ordered pipeline, not independent operations.
- Guard ``--skeptic-packet`` on next_action == ``tests_passed``. Alternative
  was letting it run any time. Rejected because a skeptic packet generated
  before the test suite passes is evidence of an untested state — the skeptic
  would receive a packet with no valid test output.
- Auto-commit spec FILES on ``--verdict PASS`` before merging. Alternative
  was requiring the user to manually commit before running --verdict. Rejected
  because Brick 11 showed that a missing manual commit causes the auto-merge
  to include uncommitted edits in the target branch, polluting the parent
  branch's history with work that was not intended for it.
- Read current_phase / current_feature from state.json for merge routing
  rather than parsing the branch name. Alternative was parsing the branch
  name to derive the parent (e.g. stripping ``brick/14-`` to infer the
  phase). Rejected because branch names carry no semantic parent pointer —
  two bricks in the same phase would have different names but the same parent,
  and parsing the name would be fragile when non-standard names are used.
"""

from __future__ import annotations

import json as _json
import re
import subprocess as _subprocess
from pathlib import Path
from typing import Any

import typer

from cli.runner import get_tool_path, run_tool
from cli.state import write as state_write

# Relative paths from repo root — centralised so any rename only changes
# one place, not every function that needs to locate these files.
SPEC_RELPATH = "bricklayer/spec.md"
STATE_RELPATH = "bricklayer/state.json"
VERDICT_RELPATH = "bricklayer/skeptic_verdict.md"
TOOLS_CWD_RELPATH = "bricklayer"

# Number of FAIL verdicts before the pipeline demands a brick rescope.
# Named constant so the threshold is explicit and searchable; changing it
# here changes it everywhere without hunting for magic 3s.
_RESCOPE_THRESHOLD: int = 3

# The six spec contract sections, in the order they are displayed to the user.
CONTRACT_FIELDS = ["WHAT", "INPUT", "OUTPUT", "GATE", "BLOCKER", "WAVE"]

# Message printed when GATE section is empty — tells the user what to fix
# rather than just exiting silently.
_NO_GATE_MSG = "No gate defined for this brick. Add one to spec.md."


def parse_spec(text: str) -> dict[str, str]:
    """Parse spec.md text and return CONTRACT_FIELDS → value strings.

    A section header is a line matching ``^WORD:`` (all-caps identifier
    followed by a colon at column 0, nothing else on the line). Section
    content continues until the next header or end of file.

    Why it exists: Every build sub-command needs the spec contract for
    different purposes (contract display, file-list extraction, brick name
    extraction). A single parser avoids three slightly-different implementations
    that could disagree on edge cases like trailing whitespace.

    Args:
        text: Raw spec.md file content as a string.

    Returns:
        Dict mapping CONTRACT_FIELDS key → stripped value string. Keys absent
        from the spec are omitted from the result.
    """
    # Matches a line that is EXACTLY "WORD:" with optional trailing whitespace.
    # The multiline flag makes ^ match at every line start, not just the
    # beginning of the string.
    section_re = re.compile(r"^([A-Z][A-Z0-9_]*):\s*$", re.MULTILINE)
    result: dict[str, str] = {}
    lines = text.splitlines()

    # First pass: collect (line_number, section_name) for all headers.
    headers: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = section_re.match(line)
        if m:
            headers.append((i, m.group(1)))

    # Second pass: for each recognised header, slice lines up to the next
    # header (or EOF) to get the section body.
    for idx, (line_no, name) in enumerate(headers):
        if name not in CONTRACT_FIELDS:
            # Non-contract sections (e.g. ACCEPTANCE, FILES) are skipped here;
            # they are parsed by dedicated helpers (_parse_spec_files, etc.).
            continue
        start = line_no + 1
        end = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        block = "\n".join(lines[start:end])
        result[name] = block.strip()

    return result


def run_build(root: Path) -> int:
    """Print the brick contract from spec.md. Returns 0 on success, 1 on error.

    Why it exists: Developers need a quick way to review the active brick
    contract without opening spec.md manually. This command prints it in a
    structured, aligned format so the GATE and OUT_OF_SCOPE sections are
    immediately visible.

    Args:
        root: Repo root directory (contains bricklayer/spec.md).

    Returns:
        0 if the contract was printed successfully. 1 if spec.md is missing
        or the GATE section is empty.
    """
    spec_path = root / SPEC_RELPATH

    if not spec_path.exists():
        typer.echo(f"error: {SPEC_RELPATH} not found at {root}", err=True)
        return 1

    text = spec_path.read_text(encoding="utf-8")
    contract = parse_spec(text)

    gate = contract.get("GATE", "").strip()
    if not gate:
        # A missing GATE means the brick has no reviewable completion criteria.
        # Exit 1 rather than printing an incomplete contract — the user needs
        # to add a GATE before work begins.
        typer.echo(_NO_GATE_MSG)
        return 1

    for field in CONTRACT_FIELDS:
        label = field.lower() + ":"
        value = contract.get(field, "(not set)").strip()
        # Indent continuation lines to align under the first value line so the
        # output is readable when values span multiple lines.
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
    """Invoke a named pipeline tool and update state.json next_action on success.

    Why it exists: --snapshot, --verify, and --test all follow the same
    pattern: resolve the tool path, run it, stream output, update state on
    success. Without this helper, each handler duplicates that pattern and
    any fix (e.g. adding timeout handling) must be applied in three places.

    Args:
        root: Repo root directory.
        config: Parsed bricklayer.yaml dict.
        tool_key: Key under ``tools:`` in bricklayer.yaml
                  (e.g. ``"verify"``, ``"test"``).
        tool_args: Additional CLI arguments to pass to the tool script.
        next_action_value: The next_action string to write to state.json on
                           tool success (e.g. ``"snapshot_init"``).

    Returns:
        0 if the tool ran and exited 0. 1 if the tool is not configured, or
        if the tool exits non-zero.
    """
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

    # Advance the pipeline state only after a successful tool run.
    # Writing before exit_code check would move the state forward even when
    # the tool failed, making the next command think the step passed.
    state_write(root / STATE_RELPATH, {"next_action": next_action_value})
    return 0


def run_snapshot(root: Path, config: dict[str, Any]) -> int:
    """Run verify tool with --snapshot-init to capture the baseline file state.

    Why it exists: verify_files_touched.py needs to know which files existed
    before the brick started so it can detect out-of-scope edits. Without a
    baseline snapshot, it would treat every file as potentially in-scope.

    Args:
        root: Repo root directory.
        config: Parsed bricklayer.yaml dict.

    Returns:
        0 on success, 1 on failure.
    """
    return _run_flag_tool(root, config, "verify", ["--snapshot-init"], "snapshot_init")


def run_verify(root: Path, config: dict[str, Any]) -> int:
    """Run verify tool to check that only spec-listed files were modified.

    Why it exists: Without a scope check, an AI builder can silently edit
    files outside the brick's FILES list — polluting later bricks and
    invalidating the skeptic's review scope.

    Args:
        root: Repo root directory.
        config: Parsed bricklayer.yaml dict.

    Returns:
        0 on success, 1 on failure.
    """
    return _run_flag_tool(root, config, "verify", [], "verify")


def run_test(root: Path, config: dict[str, Any]) -> int:
    """Run the test suite via run_tests_and_capture.py.

    Why it exists: Tests must be run through the pipeline tool rather than
    directly so that the test output is captured into state.json and the
    skeptic packet in the format those consumers expect.

    Args:
        root: Repo root directory.
        config: Parsed bricklayer.yaml dict.

    Returns:
        0 on success, 1 on failure.
    """
    return _run_flag_tool(root, config, "test", [], "tests_passed")


def run_skeptic_packet(root: Path, config: dict[str, Any]) -> int:
    """Generate the skeptic_packet/ evidence bundle for independent review.

    Guards on next_action == ``tests_passed`` — the packet must not be
    generated before the test suite passes, as that would give the skeptic
    evidence of an untested state.

    Why it exists: The skeptic needs a self-contained bundle (spec, diff, test
    output) to review the brick without access to the live repo. Without a
    dedicated packet generator, each reviewer would need to manually assemble
    this evidence, which is error-prone and inconsistent.

    Args:
        root: Repo root directory.
        config: Parsed bricklayer.yaml dict.

    Returns:
        0 on success, 1 if the guard condition is not met, if the tool fails,
        or if the packet directory is missing/empty after the tool exits.
    """
    state_path = root / STATE_RELPATH

    # Guard: must have passed tests first.
    # Read raw JSON so a missing/malformed next_action key is handled via .get()
    # rather than raising a schema ValueError from state.load().
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1
    raw_state = _json.loads(state_path.read_text(encoding="utf-8"))

    if raw_state.get("next_action") != "tests_passed":
        # .get() rather than direct access — a missing key is treated as the
        # wrong value rather than a KeyError.
        typer.echo("Run tests first (bricklayer build --test)")
        return 1

    tool_path = get_tool_path(config, "skeptic", root)
    if tool_path is None:
        typer.echo("error: 'skeptic' tool not defined in bricklayer.yaml", err=True)
        return 1

    exit_code, output = run_tool(tool_path, [], cwd=root / TOOLS_CWD_RELPATH)
    typer.echo(output, nl=False)

    if exit_code != 0:
        typer.echo(f"error: skeptic-packet tool exited {exit_code}", err=True)
        return 1

    # Verify the packet directory exists and is non-empty after exit 0.
    # A tool that exits 0 but produces no files is a silent failure that would
    # pass the gate while giving the skeptic nothing to review.
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


def _get_current_branch(root: Path) -> str | None:
    """Return the current git branch name, or None on failure.

    Why it exists: build --verdict PASS needs to detect the branch level
    (brick/phase/feature) to route the auto-merge to the correct parent.
    Without this function, the main command in main.py would also need git
    access to enforce the main-branch guard.

    Args:
        root: Repo root directory used as the git working directory.

    Returns:
        Current branch name string, or None if git returns a non-zero exit
        code.

    Note:
        Unlike the version in branch.py, this function does not guard
        FileNotFoundError. If git is not installed, the subprocess call raises
        directly. This is a known gap (v2 debt); in practice the CLI requires
        git to be installed.
    """
    proc = _subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def _merge_branch_to(root: Path, branch_name: str, target: str) -> tuple[int, str]:
    """Checkout target, merge branch_name with --no-ff, delete branch_name.

    Why it exists: Merging a brick into its parent phase, a phase into its
    feature, or a feature into main all follow the same checkout-merge-delete
    pattern. A single helper means the merge options (--no-ff) are applied
    consistently — no merge in the three-level hierarchy can accidentally
    use fast-forward, which would lose the branch topology in git log.

    Args:
        root: Repo root directory used as the git working directory.
        branch_name: Fully-qualified name of the branch to merge
                     (e.g. ``"brick/14-three-level-branching"``).
        target: Name of the branch to merge into (e.g. ``"phase/1-scaffold"``).

    Returns:
        Tuple of (exit_code, message). exit_code is 0 on success. message is
        a human-readable summary for both success and failure cases.
    """
    checkout = _subprocess.run(
        ["git", "checkout", target],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        text=True,
        check=False,
    )
    if checkout.returncode != 0:
        return checkout.returncode, (
            f"error: git checkout {target} failed: {checkout.stdout.strip()}"
        )

    merge = _subprocess.run(
        ["git", "merge", "--no-ff", branch_name],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.STDOUT,
        text=True,
        check=False,
    )
    if merge.returncode != 0:
        return merge.returncode, (
            f"error: git merge --no-ff {branch_name} failed: {merge.stdout.strip()}"
        )

    # Best-effort branch deletion — if this fails (e.g. on Windows file lock),
    # the merge has already succeeded and the branch can be deleted manually.
    _subprocess.run(
        ["git", "branch", "-d", branch_name],
        cwd=str(root),
        stdout=_subprocess.PIPE,
        stderr=_subprocess.PIPE,
        check=False,
    )
    return 0, f"Merged {branch_name} → {target}. Branch deleted."


def _parse_brick_name(spec_text: str) -> str:
    """Extract the brick name from the ``BRICK: …`` line in spec.md.

    Why it exists: The auto-commit message in run_verdict must include the
    brick name for traceability. Without this parser, the commit message would
    fall back to a generic string, losing the brick context in git log.

    Args:
        spec_text: Raw spec.md file content.

    Returns:
        The brick name string (everything after ``BRICK:``), or ``"unknown brick"``
        if the line is not found.
    """
    for line in spec_text.splitlines():
        if line.startswith("BRICK:"):
            return line[len("BRICK:"):].strip()
    return "unknown brick"


def _parse_spec_files(spec_text: str) -> list[str]:
    """Return the FILES list from spec.md.

    Why it exists: run_verdict auto-commits all files declared in the spec
    before merging, so nothing on the branch is accidentally left uncommitted.
    Without parsing the FILES list from spec.md, the commit would need a
    hardcoded list, which would always be stale.

    Args:
        spec_text: Raw spec.md file content.

    Returns:
        List of file path strings from the FILES: section. Empty list if the
        section is absent.
    """
    files: list[str] = []
    in_files = False
    for line in spec_text.splitlines():
        stripped = line.strip()
        if stripped == "FILES:":
            in_files = True
            continue
        if in_files and stripped.endswith(":") and not line.startswith(" "):
            # A new section header at column 0 ends the FILES block.
            break
        if in_files and stripped.startswith("-"):
            files.append(stripped[1:].strip())
    return files


def _git_commit_spec(root: Path, brick_name: str, files: list[str]) -> tuple[int, str]:
    """Stage spec FILES and commit them with a standard brick message.

    Why it exists: Committing before merging ensures that the parent branch
    only receives committed work — Brick 11 showed that uncommitted edits on
    the brick branch would be silently carried into the parent branch during
    the auto-merge, polluting the parent's working tree.

    Args:
        root: Repo root directory.
        brick_name: Full brick name string (e.g. ``"Brick 14 - three-level branching"``).
        files: List of file paths to stage (relative to repo root).

    Returns:
        Tuple of (exit_code, combined_output). exit_code is 0 on success.
    """
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

    # Parse "Brick 14 - three-level branching" → num="14", desc="three-level branching"
    # for a conventional commit subject like "feat(brick-14): three-level branching".
    # The \u2013 matches an en-dash as well as a regular hyphen for robustness.
    m = re.match(r"Brick\s+([\d.]+)\s*[-\u2013]\s*(.*)", brick_name, re.IGNORECASE)
    if m:
        num, desc = m.group(1), m.group(2).strip()
        subject = f"feat(brick-{num}): {desc}"
    else:
        # Brick name doesn't match the expected pattern — use a generic prefix
        # rather than silently dropping the name.
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


def _handle_fail_verdict(state_path: Path, raw_state: dict[str, Any]) -> int:
    """Increment loop_count and emit FAIL or RESCOPE message.

    Why it exists: Isolating the FAIL path keeps run_verdict readable as a
    router. The threshold check and state update belong together — either both
    happen or neither does.

    Args:
        state_path: Absolute path to state.json (needed for state_write).
        raw_state: Already-parsed state.json dict (avoids a second read).

    Returns:
        Always 1 — FAIL is always an error exit.
    """
    # Read loop_count as int — json gives us an int already, but int() guards
    # against a malformed state where the value was written as a string.
    loop_count = int(raw_state.get("loop_count", 0))

    if loop_count >= _RESCOPE_THRESHOLD:
        # Already at or above the threshold — no point incrementing further.
        # Re-emit the rescope message so the user knows why the command is
        # blocked rather than seeing a silent exit 1.
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


def _merge_to_parent(
    root: Path,
    current_branch: str | None,
    raw_state: dict[str, Any],
) -> int:
    """Route auto-merge to the correct parent branch based on current branch level.

    Why it exists: Merge routing is the most nuanced part of the PASS path —
    a brick merges to its phase, a phase to its feature, a feature to main.
    Extracting it here keeps _commit_and_merge focused on the commit step and
    makes the routing logic independently testable.

    Args:
        root: Repo root directory.
        current_branch: Current git branch name (may be None if git fails).
        raw_state: Already-parsed state.json dict for reading current_phase and
                   current_feature merge targets.

    Returns:
        0 if the merge succeeded (or no merge was needed). 1 on error.
    """
    if current_branch is not None and current_branch.startswith("brick/"):
        # Brick merges to its phase — current_phase is set by bricklayer branch --phase.
        parent = raw_state.get("current_phase")
        if not parent:
            typer.echo(
                "error: current_phase not set in state.json — cannot determine merge target",
                err=True,
            )
            return 1
        merge_code, merge_msg = _merge_branch_to(root, current_branch, parent)
        typer.echo(merge_msg)
        if merge_code != 0:
            typer.echo("error: git merge failed — state not advanced", err=True)
            return 1

    elif current_branch is not None and current_branch.startswith("phase/"):
        # Phase merges to its feature — current_feature is set by bricklayer branch --feature.
        parent = raw_state.get("current_feature")
        if not parent:
            typer.echo(
                "error: current_feature not set in state.json — cannot determine merge target",
                err=True,
            )
            return 1
        merge_code, merge_msg = _merge_branch_to(root, current_branch, parent)
        typer.echo(merge_msg)
        if merge_code != 0:
            typer.echo("error: git merge failed — state not advanced", err=True)
            return 1

    elif current_branch is not None and current_branch.startswith("feature/"):
        # Feature always merges to main — there is no higher parent.
        merge_code, merge_msg = _merge_branch_to(root, current_branch, "main")
        typer.echo(merge_msg)
        if merge_code != 0:
            typer.echo("error: git merge failed — state not advanced", err=True)
            return 1

    return 0


def _commit_and_merge(root: Path, raw_state: dict[str, Any]) -> int:
    """Auto-commit spec FILES then merge the current branch to its parent.

    Why it exists: The PASS path has two sequential git operations — commit,
    then merge. Extracting them together keeps run_verdict as a router and
    makes it easy to test commit-without-merge and merge-without-commit
    scenarios in isolation.

    Args:
        root: Repo root directory.
        raw_state: Already-parsed state.json dict passed through to
                   _merge_to_parent for routing decisions.

    Returns:
        0 if both commit and merge succeeded. 1 on any failure.
    """
    spec_path = root / SPEC_RELPATH
    if spec_path.exists():
        spec_text = spec_path.read_text(encoding="utf-8")
        brick_name = _parse_brick_name(spec_text)
        spec_files = _parse_spec_files(spec_text)
        # Commit before merge — uncommitted edits on the branch would otherwise
        # be silently carried into the parent branch (Brick 11 FAILed for this
        # exact reason).
        commit_exit, commit_output = _git_commit_spec(root, brick_name, spec_files)
        if commit_output:
            typer.echo(commit_output, nl=False)
        if commit_exit != 0:
            typer.echo("error: git commit failed — state not advanced", err=True)
            return 1

    current_branch = _get_current_branch(root)
    return _merge_to_parent(root, current_branch, raw_state)


def run_verdict(root: Path, config: dict[str, Any], verdict_value: str) -> int:
    """Route PASS or FAIL verdict to the appropriate handler.

    Validates the verdict value, checks the skeptic-packet guard, then
    delegates to _commit_and_merge (PASS) or _handle_fail_verdict (FAIL).

    Why it exists: The verdict step closes the inner loop of the pipeline.
    Without it, there is no formal gate between the skeptic's decision and the
    branch merge — work could be merged without a recorded verdict, or the
    loop_count gate could be bypassed.

    Args:
        root: Repo root directory.
        config: Parsed bricklayer.yaml dict.
        verdict_value: ``"PASS"`` or ``"FAIL"``.

    Returns:
        0 on PASS with successful commit, merge, and state close. 1 on any
        error or on FAIL.
    """
    if verdict_value not in ("PASS", "FAIL"):
        typer.echo(
            f"error: invalid verdict '{verdict_value}'. Use PASS or FAIL.", err=True
        )
        return 1

    state_path = root / STATE_RELPATH

    # Guard: must have a skeptic packet before recording a verdict.
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1
    raw_state = _json.loads(state_path.read_text(encoding="utf-8"))
    if raw_state.get("next_action") != "skeptic_packet_ready":
        typer.echo(
            "Run skeptic packet first (bricklayer build --skeptic-packet)", err=True
        )
        return 1

    if verdict_value == "PASS":
        # Write the verdict file before committing — the file may itself be
        # part of the auto-commit if it is in the spec FILES list.
        verdict_path = root / VERDICT_RELPATH
        verdict_path.write_text("Verdict: PASS\n", encoding="utf-8")
        typer.echo(f"written: {verdict_path}")

        if _commit_and_merge(root, raw_state) != 0:
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

    return _handle_fail_verdict(state_path, raw_state)
