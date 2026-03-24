"""Shared tool invocation and output capture for bricklayer build flags."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any


def run_tool(
    tool_path: Path,
    args: list[str] | None = None,
    cwd: Path | None = None,
) -> tuple[int, str]:
    """Run ``python3 tool_path [args]``, capture combined stdout+stderr.

    Returns (exit_code, output_string).
    """
    cmd = ["python3", str(tool_path)] + (args or [])
    proc = subprocess.run(
        cmd,
        cwd=str(cwd or tool_path.parent),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return proc.returncode, proc.stdout


def get_tool_path(config: dict[str, Any], tool_name: str, root: Path) -> Path | None:
    """Resolve a named tool from bricklayer.yaml config.

    Returns the absolute Path or None if the key is absent.
    """
    tools = config.get("tools") or {}
    rel = tools.get(tool_name)
    if rel is None:
        return None
    p = Path(rel)
    if not p.is_absolute():
        p = root / p
    return p
