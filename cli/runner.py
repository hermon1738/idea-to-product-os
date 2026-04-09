"""Shared tool invocation and output capture for bricklayer build flags.

WHY THIS EXISTS:
    Every build flag (--snapshot, --verify, --test, --skeptic-packet) needs
    to invoke a Python tool script, capture combined stdout+stderr, and return
    the exit code to the caller. Without a shared runner, each flag handler
    would duplicate the subprocess setup — any difference in how they handle
    stderr vs stdout, text encoding, or cwd would produce subtle inconsistencies
    in the output captured into state.json and the skeptic packet.

DESIGN DECISIONS:
- Merge stderr into stdout via stderr=STDOUT. Alternative was to capture them
  separately and interleave. Rejected because the bricklayer tools print
  progress and errors to a mix of stdout/stderr; capturing separately would
  lose ordering and make the combined output in test_output.txt unreadable.
- Return (exit_code, output) tuple rather than raising on non-zero exit.
  Alternative was to raise a subprocess.CalledProcessError. Rejected because
  callers need to decide what a non-zero exit means in context (--test failing
  updates state differently from --verify failing); raising would hide that
  policy in the runner rather than keeping it in the caller.
- Resolve tool paths via bricklayer.yaml config, not hardcoded paths.
  Alternative was embedding paths in each build flag handler. Rejected because
  hardcoded paths break when users place tool scripts in custom locations.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

# Timeout in seconds for any single tool invocation. Long-running test suites
# should still complete well within this — it is a safety net against hung
# processes, not a performance constraint.
TOOL_TIMEOUT_SECONDS: int = 300


def run_tool(
    tool_path: Path,
    args: list[str] | None = None,
    cwd: Path | None = None,
) -> tuple[int, str]:
    """Run ``python3 tool_path [args]`` and return (exit_code, combined_output).

    Why it exists: Build flag handlers need a single, consistent way to invoke
    pipeline tool scripts and capture their output. Without this wrapper, each
    handler would set up subprocess arguments differently, producing
    inconsistent encoding, cwd, and error-capture behaviour.

    Args:
        tool_path: Absolute path to the Python tool script to run.
        args: Optional list of additional CLI arguments passed after the
              script path.
        cwd: Working directory for the subprocess. Defaults to the directory
             containing ``tool_path`` so relative paths inside the tool
             resolve against its own location.

    Returns:
        Tuple of (exit_code, output_string). output_string combines stdout
        and stderr in interleaved order as they were written.
    """
    cmd = ["python3", str(tool_path)] + (args or [])
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or tool_path.parent),
        stdout=subprocess.PIPE,
        # Merge stderr into stdout so the captured output is a single coherent
        # stream matching what the user would see if they ran the tool directly.
        stderr=subprocess.STDOUT,
        text=True,
        timeout=TOOL_TIMEOUT_SECONDS,
        check=False,  # Caller inspects returncode; we do not raise on failure.
    )
    return proc.returncode, proc.stdout


def get_tool_path(config: dict[str, Any], tool_name: str, root: Path) -> Path | None:
    """Resolve a named tool entry from bricklayer.yaml config to an absolute Path.

    Why it exists: Tool paths in bricklayer.yaml are relative to the YAML
    file's directory. Every caller needs the same resolution logic; duplicating
    it would cause subtle bugs if one caller resolves relative to cwd instead.

    Args:
        config: Parsed bricklayer.yaml dict (from load_and_validate).
        tool_name: Key under the ``tools:`` section (e.g. ``"verify"``,
                   ``"test"``).
        root: Absolute path to the repo root (directory containing
              bricklayer.yaml). Relative tool paths are resolved against this.

    Returns:
        Absolute Path to the tool script, or None if the key is absent from
        the ``tools:`` section.
    """
    tools = config.get("tools") or {}
    rel = tools.get(tool_name)
    if rel is None:
        # The key is absent or explicitly null — caller decides what to do.
        return None
    import os as _os
    rel = _os.path.expandvars(rel)
    p = Path(rel)
    if not p.is_absolute():
        # Relative paths in bricklayer.yaml are always relative to the YAML
        # file location (repo root), not to cwd.
        p = root / p
    return p
