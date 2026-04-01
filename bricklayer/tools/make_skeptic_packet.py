#!/usr/bin/env python3
"""Generate skeptic packet artifacts deterministically from repo root."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path.cwd()
PACKET_DIR = ROOT / "skeptic_packet"
SPEC_SRC = ROOT / "spec.md"
STATE_SRC = ROOT / "state.json"
CONTEXT_PATH = ROOT / "context.txt"


def _parse_test_command() -> list[str]:
    """Read TEST_COMMAND from context.txt and return as argv list.

    Why it exists: make_skeptic_packet previously used a hardcoded
    pytest command with no path argument, causing it to run pytest
    against the bricklayer/ CWD and find no tests (exit 5). Reading
    from context.txt makes the skeptic packet use the same test command
    as run_tests_and_capture, ensuring consistent results.

    Returns:
        Parsed argv list from TEST_COMMAND line in context.txt.
        Falls back to ["python3", "-m", "pytest", "-q"] if not found.
    """
    import shlex
    if CONTEXT_PATH.exists():
        for line in CONTEXT_PATH.read_text(encoding="utf-8").splitlines():
            if line.startswith("TEST_COMMAND:"):
                cmd = line.split(":", 1)[1].strip()
                if cmd:
                    return shlex.split(cmd)
    return ["python3", "-m", "pytest", "-q"]


TEST_CMD = _parse_test_command()
STATE_KEYS = [
    "current_brick",
    "status",
    "loop_count",
    "last_gate_failed",
    "last_test_run",
]


def parse_scoped_files() -> list[str]:
    lines = SPEC_SRC.read_text(encoding="utf-8").splitlines()
    scoped: list[str] = []
    in_files = False

    for line in lines:
        stripped = line.strip()
        if stripped == "FILES:":
            in_files = True
            continue
        if in_files and stripped.endswith(":") and not line.startswith(" "):
            break
        if in_files and stripped.startswith("-"):
            scoped.append(stripped[1:].strip())
    return scoped


def write_spec_copy() -> Path:
    dst = PACKET_DIR / "spec.md"
    shutil.copyfile(SPEC_SRC, dst)
    return dst


def write_state_excerpt() -> Path:
    dst = PACKET_DIR / "state_excerpt.json"
    with STATE_SRC.open("r", encoding="utf-8") as f:
        state = json.load(f)

    excerpt = {k: state.get(k) for k in STATE_KEYS if k in state}
    with dst.open("w", encoding="utf-8") as f:
        json.dump(excerpt, f, indent=2)
        f.write("\n")
    return dst


def write_test_output() -> tuple[Path, int]:
    dst = PACKET_DIR / "test_output.txt"
    proc = subprocess.run(
        TEST_CMD,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    with dst.open("w", encoding="utf-8") as f:
        f.write(proc.stdout)
    return dst, proc.returncode


def _get_git_root() -> "Path | None":
    """Return the absolute repo root, or None if not in a git repo."""
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return Path(proc.stdout.strip())
    return None


def _git_add_spec_files(git_root: Path, files: list[str]) -> None:
    """Stage all spec FILES in the git index before building the packet."""
    if not files:
        return
    subprocess.run(
        ["git", "add", "--"] + files,
        cwd=str(git_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def is_git_repo() -> bool:
    if shutil.which("git") is None:
        return False

    probe = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    return probe.returncode == 0 and probe.stdout.strip() == "true"


def write_diff_artifact() -> Path:
    patch_path = PACKET_DIR / "diff.patch"
    text_path = PACKET_DIR / "diff.txt"

    if is_git_repo():
        proc = subprocess.run(
            ["git", "diff"],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        cached = subprocess.run(
            ["git", "diff", "--cached"],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

        patch_chunks = [proc.stdout, cached.stdout]
        for path in [p.strip() for p in untracked.stdout.splitlines() if p.strip()]:
            untracked_patch = subprocess.run(
                ["git", "diff", "--no-index", "--", "/dev/null", path],
                cwd=str(ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            patch_chunks.append(untracked_patch.stdout)

        with patch_path.open("w", encoding="utf-8") as f:
            f.write("".join(patch_chunks))
        if text_path.exists():
            text_path.unlink()
        return patch_path

    message = (
        "git diff unavailable: 'git' is not installed or current directory "
        "is not a git repository.\n"
    )
    with text_path.open("w", encoding="utf-8") as f:
        f.write(message)
    if patch_path.exists():
        patch_path.unlink()
    return text_path


def write_scoped_files_bundle() -> tuple[Path, Path]:
    bundle_path = PACKET_DIR / "scoped_files_bundle.md"

    scoped_files = parse_scoped_files()
    present: list[str] = []
    missing: list[str] = []
    sections: list[str] = []

    for rel in scoped_files:
        source = ROOT / rel
        if source.is_file():
            present.append(rel)
            try:
                contents = source.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                contents = "[binary file omitted]"
            sections.append(f"## FILE: {rel}\n\n```text\n{contents}\n```\n")
        else:
            missing.append(rel)

    bundle_path.write_text(
        "# Scoped Files Bundle\n\n" + "\n".join(sections), encoding="utf-8"
    )

    manifest_path = PACKET_DIR / "files_manifest.json"
    payload = {
        "scoped_files_from_spec": scoped_files,
        "included_files": present,
        "missing_files": missing,
    }
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return bundle_path, manifest_path


def main() -> int:
    PACKET_DIR.mkdir(parents=True, exist_ok=True)

    # Auto-stage all spec FILES before building packet so new files appear in diff
    if is_git_repo():
        git_root = _get_git_root()
        if git_root is not None:
            _git_add_spec_files(git_root, parse_scoped_files())

    written_spec = write_spec_copy()
    written_state = write_state_excerpt()
    written_test, test_exit = write_test_output()
    written_diff = write_diff_artifact()
    written_bundle, written_manifest = write_scoped_files_bundle()

    print("Skeptic packet updated:")
    print(f"- {written_spec.relative_to(ROOT)}")
    print(f"- {written_state.relative_to(ROOT)}")
    print(f"- {written_test.relative_to(ROOT)} (test exit {test_exit})")
    print(f"- {written_diff.relative_to(ROOT)}")
    print(f"- {written_bundle.relative_to(ROOT)}")
    print(f"- {written_manifest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
