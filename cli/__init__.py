"""Bricklayer CLI package.

WHY THIS EXISTS:
    This file marks the cli/ directory as a Python package, enabling imports
    like ``from cli.config import load_and_validate``. Without it, Python
    would not recognise ``cli`` as a namespace and every import from any
    submodule would fail with a ModuleNotFoundError at startup.

DESIGN DECISIONS:
- Empty module body: no shared state or re-exports in __init__.py.
  Alternative was to re-export commonly-used symbols here for shorter import
  paths (e.g. ``from cli import load_and_validate``). Rejected because it
  creates circular-import risk and hides the true source of each symbol —
  callers should import from the explicit submodule so grep and static
  analysis can trace dependencies.
"""
