"""Commit command: git commit wrapper with auto-tagged brick ID message.

WHY THIS EXISTS:
    Mid-brick checkpoints need commits that carry the brick number and a
    co-author attribution without requiring the developer to type the full
    conventional-commit format by hand. Without this command, manual commits
    would be inconsistently formatted, making it impossible to grep git log
    for all commits belonging to a specific brick.

DESIGN DECISIONS:
- Auto-tag the commit subject with the brick number from state.json rather
  than requiring the user to supply it. Alternative was a plain ``git commit``
  passthrough. Rejected because inconsistent commit messages make audit trails
  useless — you cannot answer "what changed in Brick 14?" from git log if
  brick numbers are not in the subjects.
- Require staged files before committing (check via ``git diff --cached``).
  Alternative was passing ``-a`` to ``git commit`` to auto-stage all tracked
  changes. Rejected because auto-staging is dangerous in a pipeline where
  only spec-listed files should be committed — it would silently include any
  modified file that was not in the spec.
- Parse brick number and name from state.json ``current_brick`` field.
  Alternative was parsing from spec.md. Rejected because state.json is
  already loaded for the staged-file check; reading spec.md would add a
  second file I/O call for no extra accuracy.
"""

from __future__ import annotations

import json
import re
import subprocess as _subprocess
from pathlib import Path

import typer

# Relative path to state.json from the repo root.
STATE_RELPATH = "bricklayer/state.json"

# Co-author line appended to every commit message so AI-assisted commits are
# traceable in git log. Using a constant avoids typo drift across files.
_COAUTHOR = "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"


def _parse_brick(current_brick: str) -> tuple[str, str]:
    """Parse ``current_brick`` string into (brick_number, brick_name).

    Why it exists: The commit message format requires the brick number and
    a short description separately. Without this parser, the commit message
    function would need to embed the regex, making it harder to test the
    parsing logic in isolation.

    Args:
        current_brick: Value of ``current_brick`` from state.json
                       (e.g. ``"Brick 14 - three-level branching"``).

    Returns:
        Tuple (brick_number, brick_name). If the string does not match the
        expected pattern, returns (``"?"``, original string) so the commit
        message degrades gracefully rather than raising.

    Example:
        ``_parse_brick("Brick 14 - three-level branching")``
        → ``("14", "three-level branching")``
    """
    # Matches "Brick N - description" or "Brick N — description" (en-dash).
    m = re.match(r"Brick\s+([\d.]+)\s*[-\u2013]\s*(.*)", current_brick, re.IGNORECASE)
    if m:
        return m.group(1), m.group(2).strip()
    return "?", current_brick


def _check_staged(root: Path) -> list[str]:
    """Return a list of staged file paths; empty list if nothing is staged or git fails.

    Why it exists: Committing with nothing staged produces a confusing
    ``git commit`` error about an empty commit. This check surfaces a clearer
    message before git is invoked.

    Args:
        root: Repo root directory used as the git working directory.

    Returns:
        List of relative file paths that are staged for commit. Empty list if
        nothing is staged, git is not installed (FileNotFoundError), or the
        git command fails.
    """
    try:
        proc = _subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=str(root),
            stdout=_subprocess.PIPE,
            stderr=_subprocess.PIPE,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # git is not on PATH — return empty list so the caller surfaces the
        # "Nothing staged" message rather than a raw traceback.
        return []
    return [f for f in proc.stdout.splitlines() if f.strip()]


def _build_message(brick_num: str, brick_name: str, user_msg: str) -> str:
    """Build the full conventional-commit message string.

    Why it exists: The message format (subject + body with brick reference and
    co-author) must be identical for every commit. Centralising it here means
    the format is defined once and tests can assert against a known structure.

    Args:
        brick_num: Brick number string (e.g. ``"14"``).
        brick_name: Brick description (e.g. ``"three-level branching"``).
        user_msg: The user-supplied commit description (e.g.
                  ``"add phase branch validation"``).

    Returns:
        Full commit message string with subject, blank line, brick reference,
        and co-author footer.
    """
    return (
        f"feat(brick-{brick_num}): {user_msg}\n\n"
        f"Brick: {brick_num} \u2014 {brick_name}\n"
        f"{_COAUTHOR}"
    )


def _do_commit(root: Path, message: str) -> tuple[int, str]:
    """Run ``git commit -m <message>`` and return (exit_code, output).

    Why it exists: Isolating the subprocess call makes tests able to mock just
    the commit step without mocking all of subprocess.run globally.

    Args:
        root: Repo root directory used as the git working directory.
        message: Full commit message string.

    Returns:
        Tuple of (exit_code, combined_output). exit_code is 0 on success.
        On FileNotFoundError (git not installed), returns (1, error message).
    """
    try:
        proc = _subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(root),
            stdout=_subprocess.PIPE,
            stderr=_subprocess.STDOUT,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return 1, "error: git executable not found"
    return proc.returncode, proc.stdout.strip()


def run_commit(root: Path, message: str) -> int:
    """Commit staged files with an auto-tagged brick ID conventional-commit message.

    Reads the active brick from state.json, verifies files are staged, builds
    the commit message, and calls git commit.

    Why it exists: See module docstring.

    Args:
        root: Repo root directory (contains bricklayer.yaml).
        message: Short commit description supplied by the user via ``-m``.

    Returns:
        0 on success. 1 if message is empty, state.json is missing or corrupt,
        nothing is staged, or git commit fails.
    """
    if not message.strip():
        typer.echo("Commit message cannot be empty", err=True)
        return 1

    state_path = root / STATE_RELPATH
    if not state_path.exists():
        typer.echo(f"error: state.json not found at {state_path}", err=True)
        return 1

    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        typer.echo(f"error: state.json is corrupt — {exc}", err=True)
        return 1

    # current_brick may be None in state.json (known v2 gap) — .get() with a
    # default empty string avoids a TypeError from _parse_brick when the value
    # is JSON null.
    brick_num, brick_name = _parse_brick(state.get("current_brick", "") or "")

    staged = _check_staged(root)
    if not staged:
        typer.echo("Nothing staged. Use git add first.", err=True)
        return 1

    full_msg = _build_message(brick_num, brick_name, message.strip())
    code, output = _do_commit(root, full_msg)
    if code != 0:
        typer.echo(f"error: git commit failed: {output}", err=True)
        return 1

    typer.echo(output)
    return 0
