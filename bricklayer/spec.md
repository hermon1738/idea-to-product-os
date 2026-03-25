BRICK: Brick 20 - bricklayer context

WHAT:
  `bricklayer context` prints a compact context block for a project
  that can be pasted directly into any AI session to orient it
  instantly. Replaces manual context assembly at session start.

INPUT:
  Optional --project flag. Defaults to current project from
  bricklayer/state.json if not specified.

OUTPUT:
  Formatted context block with dividers, state fields, last 3
  decision-log rows, and next command.

  Project not found -> clear error, exit 1
  context/projects/ empty or missing -> "No projects found", exit 1
  Malformed state.json -> clear error, exit 1

GATE:
  OUTPUTS

BLOCKER:
  bricklayer resume will call this in Phase 5 to restore full
  session context.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/context.py
- cli/main.py
- tests/test_context.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Valid project -> all 6 sections print correctly, exit 0
2) No --project flag -> reads project from bricklayer/state.json
3) Empty decision-log.md -> "No decisions logged yet"
4) More than 3 decisions -> only last 3 printed
5) Project not found -> clear error, exit 1, no traceback
6) context/projects/ missing -> "No projects found", exit 1
7) Malformed state.json in project -> clear error, exit 1

TEST REQUIREMENTS:
- Happy path: all fields correct, exit 0
- No --project: reads from bricklayer/state.json
- Empty decision-log.md: "No decisions logged yet"
- More than 3 decisions: only last 3
- Project not found: error, exit 1
- context/projects/ missing: error, exit 1
- Malformed state.json: error, exit 1
- CliRunner integration: all 6 sections in output

OUT OF SCOPE:
- Writing to any file
- Any command other than context
- Any file outside the FILES list
