BRICK: Brick 11 - bricklayer commit

WHAT:
  `bricklayer commit` is a git commit wrapper that auto-tags commits
  with the current brick ID and phase from state.json. Enforces the
  stack-rules.md commit message format. Replaces manual git commit
  during mid-brick checkpoints.

INPUT:
  state.json (brick number, brick name), -m message from user,
  staged files in git index at time of call.

OUTPUT:
  bricklayer commit -m "add deep merge fix"
    → commits staged files with message:
      "feat(brick-11): add deep merge fix

       Brick: 11 — bricklayer commit
       Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    → prints commit hash and message, exit 0
  bricklayer commit with nothing staged
    → "Nothing staged. Use git add first.", exit 1
  bricklayer commit with no -m flag
    → "Commit message required: bricklayer commit -m 'your message'",
      exit 1
  bricklayer commit -m ""
    → "Commit message cannot be empty", exit 1

GATE:
  RUNS — stage a file, run bricklayer commit -m "test", confirm git
  log shows correctly formatted commit with brick ID. Run with
  nothing staged — error, exit 1. Run with no -m — error, exit 1.

BLOCKER:
  bricklayer close-session (Brick 12) uses this to commit session
  summary.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/commit.py
- cli/main.py
- tests/test_commit.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Happy path
- Files staged, -m provided → commit created with correct format,
  prints commit hash and message, exit 0.

2) Commit message format
- Subject: "feat(brick-N): <message>"
- Body: "Brick: N — <brick_name>"
- Trailer: "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

3) Nothing staged
- "Nothing staged. Use git add first.", exit 1, no traceback.

4) No -m flag
- Usage error printed, exit 1, no traceback.

5) Empty -m string
- "Commit message cannot be empty", exit 1.

6) Missing state.json
- Clear error, exit 1, no traceback.

7) git commit fails
- Clear error, exit 1, no traceback.

8) CliRunner integration
- `bricklayer commit -m "msg"` via CliRunner → exit 0,
  commit message matches format.

TEST REQUIREMENTS:
- Happy path: commit created, message format correct, exit 0
- Format: feat(brick-N) prefix, brick name in body, Co-Authored-By
- Nothing staged: "Nothing staged" error, exit 1, no traceback
- No -m: usage error, exit 1, no traceback
- Empty -m: "Commit message cannot be empty", exit 1
- Missing state.json: error, exit 1, no traceback
- git commit fails: error, exit 1, no traceback
- CliRunner: exit 0, log entry format correct

OUT OF SCOPE:
- Amending commits
- Interactive rebase
- Any push operations
