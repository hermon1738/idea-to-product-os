BRICK: Brick 9 - bricklayer pause

WHAT:
  `bricklayer pause` writes two files that capture full session state
  so the next session can resume without any manual context
  reconstruction.

INPUT:
  state.json (current brick, loop_count, next_action, last_action,
  current_branch), bricklayer/spec.md (current brick contract),
  git current branch (via git rev-parse).

OUTPUT:
  HANDOFF.json (repo root):
    {
      "project": "bricklayer-cli",
      "brick": <current brick number>,
      "brick_name": "<current brick name>",
      "last_action": "<state.json next_action>",
      "loop_count": <state.json loop_count>,
      "current_branch": "<current git branch>",
      "timestamp": "<ISO 8601>",
      "next_command": "<output of bricklayer next>"
    }
  .continue-here.md (repo root):
    Last session ended: <timestamp>
    Project: <project>
    Branch: <current_branch>
    Current brick: Brick N — <name>
    Last action: <last_action>
    Next command: <next_command>
    Blockers: none
  Both files written atomically. If either write fails → clear
  error, exit 1, neither file left in partial state.

GATE:
  OUTPUTS — run `bricklayer pause`, confirm HANDOFF.json and
  .continue-here.md exist and contain correct values matching
  current state.json. Corrupt state.json → clear error, exit 1,
  no raw traceback.

BLOCKER:
  bricklayer resume (Brick 10) reads HANDOFF.json — nothing to
  resume without this.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/pause.py
- cli/main.py
- tests/test_pause.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Happy path
- Valid state.json → HANDOFF.json and .continue-here.md written
  with correct values. Exit 0.

2) HANDOFF.json fields
- All 8 fields present: project, brick, brick_name, last_action,
  loop_count, current_branch, timestamp, next_command.
- Timestamp is valid ISO 8601.

3) .continue-here.md content
- All 6 lines present: Last session ended, Project, Branch,
  Current brick, Last action, Next command.
- Values match HANDOFF.json.

4) Missing state.json
- Clear error, exit 1, no files written, no raw traceback.

5) Partial write safety
- If second file write fails, neither file is left in a partial
  or corrupted state (first file removed or both absent).

6) CliRunner integration
- `bricklayer pause` via CliRunner → exit 0, both files exist
  with correct content.

TEST REQUIREMENTS:
- Happy path: both files written, exit 0
- HANDOFF.json: all 8 fields, ISO 8601 timestamp
- .continue-here.md: all 6 lines, values match HANDOFF.json
- Missing state.json: error, exit 1, no files, no traceback
- Partial write safety: second write failure → neither file present
- CliRunner: exit 0, both files exist with correct content

OUT OF SCOPE:
- bricklayer resume (Brick 10)
- Any network or cloud sync of HANDOFF.json
- Pushing to remote
