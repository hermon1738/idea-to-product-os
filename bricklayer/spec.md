BRICK: Brick 16 - docs and production-ready pass

WHAT:
  Retroactively apply comprehensive documentation and
  production-ready standards to all existing cli/ modules.
  Style and documentation changes only — zero logic changes.

INPUT:
  All existing cli/ modules (15 files)

OUTPUT:
  Every cli/ module has:
  1. Module header docstring (WHY THIS EXISTS + DESIGN DECISIONS)
  2. Every function/method has a full docstring
  3. Inline comments on every non-obvious line (WHY not WHAT)
  4. All production-ready violations fixed:
     - Type hints on every function signature
     - No bare excepts — specific exceptions only
     - No silent failures
     - Named constants for magic numbers/strings
     - Atomic writes on critical file operations
     - subprocess calls fully specified
     - Max 40 lines per function
     - Max 3 nesting levels
     - Errors to stderr via typer.echo(err=True)

GATE:
  OUTPUTS + RUNS:
  - Full test suite passes: python3 -m pytest -q ../tests/
  - 408+ tests passing
  - No bare excepts anywhere in cli/
  - No untyped function signatures anywhere in cli/

BLOCKER:
  Nothing.

WAVE:
  SEQUENTIAL

FILES:
- cli/__init__.py
- cli/config.py
- cli/state.py
- cli/runner.py
- cli/main.py
- cli/commands/branch.py
- cli/commands/build.py
- cli/commands/close_feature.py
- cli/commands/close_phase.py
- cli/commands/commit.py
- cli/commands/next.py
- cli/commands/pause.py
- cli/commands/resume.py
- cli/commands/status.py
- cli/commands/close_session.py
- tests/test_config.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Module header docstrings
- Every cli/ module has WHY THIS EXISTS and DESIGN DECISIONS sections.

2) Function docstrings
- Every function has description, why it exists, Args, Returns, Raises.

3) Inline comments
- Every non-obvious line explains WHY not WHAT.

4) Type hints
- Every function signature has full type hints.

5) No bare excepts
- Zero bare except clauses in cli/.

6) Named constants
- No magic numbers or strings inline.

7) Tests pass
- 408+ tests passing after all changes.

TEST REQUIREMENTS:
- No new tests.
- Gate: python3 -m pytest -q ../tests/ → 408+ passing.

OUT OF SCOPE:
- Logic changes
- New features
- Test file modifications
