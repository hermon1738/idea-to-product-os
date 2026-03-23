"""YAML loader and path validation for bricklayer.yaml."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

YAML_FILENAME = "bricklayer.yaml"


def find_yaml(start: Path | None = None) -> Path | None:
    """Walk upward from start (default: cwd) looking for bricklayer.yaml."""
    current = (start or Path.cwd()).resolve()
    while True:
        candidate = current / YAML_FILENAME
        if candidate.exists():
            return candidate
        parent = current.parent
        if parent == current:
            return None
        current = parent


def load_and_validate(yaml_path: Path | None = None) -> dict:
    """Load bricklayer.yaml and validate all declared paths.

    Prints human-readable errors and exits 1 on any failure.
    """
    if yaml_path is None:
        yaml_path = find_yaml()

    if yaml_path is None or not yaml_path.exists():
        print("bricklayer.yaml not found at repo root")
        sys.exit(1)

    try:
        raw = yaml_path.read_text(encoding="utf-8")
        config = yaml.safe_load(raw) or {}
    except Exception as exc:  # noqa: BLE001
        print(f"bricklayer.yaml could not be parsed: {exc}")
        sys.exit(1)

    base = yaml_path.parent
    missing: list[str] = []

    for section_key in ("phases", "tools", "agents"):
        section = config.get(section_key) or {}
        if not isinstance(section, dict):
            continue
        for _name, rel_path in section.items():
            if rel_path is None:
                continue
            p = Path(rel_path)
            if not p.is_absolute():
                p = base / p
            if not p.exists():
                missing.append(str(rel_path))

    if missing:
        for m in missing:
            print(f"Missing: {m} — check bricklayer.yaml")
        sys.exit(1)

    return config
