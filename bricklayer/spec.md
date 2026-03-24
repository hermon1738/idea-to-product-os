BRICK: Brick 10 - bricklayer resume

WHAT:
  `bricklayer resume` reads HANDOFF.json and prints a fully formatted
  context block that can be pasted directly into a new Claude Code
  session — no manual reconstruction required. After printing, checks
  if current git branch matches HANDOFF.json current_branch and warns
  if mismatched. Does not auto-switch branches.

INPUT:
  HANDOFF.json at repo root (written by bricklayer pause).

OUTPUT:
  Printed context block:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    RESUMING SESSION
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Project:      <project>
    Branch:       <current_branch>
    Brick:        <brick> — <brick_name>
    Last action:  <last_action>
    Loop count:   <loop_count>
    Paused at:    <timestamp>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Next command: <next_command>
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  If current branch != HANDOFF.json current_branch:
    Warning: you are on <current> but session was paused on
    <expected>. Switch with: git checkout <expected>
  Exit 0 in all success cases (including branch mismatch warning).

GATE:
  RUNS — run `bricklayer pause` then `bricklayer resume` in sequence.
  Confirm resume output matches all HANDOFF.json fields exactly.
  Switch branches, run resume again — confirm branch mismatch warning.
  Corrupt/missing HANDOFF.json → clear error, exit 1, no traceback.

BLOCKER:
  Without this, session restart is still manual.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/resume.py
- cli/main.py
- tests/test_resume.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Happy path
- Valid HANDOFF.json → formatted context block printed with all
  fields, exit 0.

2) Branch match
- Current branch == HANDOFF.json current_branch → no warning.

3) Branch mismatch
- Current branch differs → warning with both branch names, exit 0.

4) Missing HANDOFF.json
- Error: "No session to resume. Run bricklayer pause first."
  Exit 1. No files written. No raw traceback.

5) Malformed HANDOFF.json
- Clear error, exit 1, no raw traceback.

6) Missing required field
- Clear error naming the missing field, exit 1.

7) CliRunner integration
- `bricklayer resume` via CliRunner → exit 0, output contains all
  required fields in correct format.

TEST REQUIREMENTS:
- Happy path: all fields in output, exit 0
- Branch match: no warning
- Branch mismatch: warning with correct names, exit 0
- Missing HANDOFF.json: correct error message, exit 1, no traceback
- Malformed HANDOFF.json: error, exit 1, no traceback
- Missing required field: error names the field, exit 1
- CliRunner: exit 0, all fields in output

OUT OF SCOPE:
- Auto-switching branches
- Writing any files
- Any network operations
