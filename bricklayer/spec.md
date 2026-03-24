BRICK: Brick 12 - bricklayer close-session

WHAT:
  `bricklayer close-session` is the formal session ending command.
  It loads sprint-brain.md, formats a sprint review prompt from
  current state, calls Groq to generate the review, writes the
  output to session-log.md, updates STATE.md with current position,
  and prints the next session start command. Replaces the manual
  sprint review paste ritual.

INPUT:
  state.json, bricklayer/spec.md, system-prompts/sprint-brain.md
  (path from bricklayer.yaml), Groq API key from environment

OUTPUT:
  1. Groq call with sprint-brain.md as system prompt +
     current brick status as user message
  2. session-log.md written at repo root with:
     - timestamp
     - bricks attempted this session
     - sprint review output from Groq
  3. STATE.md written/updated at repo root with:
     - current project
     - current brick
     - last action
     - next command
  4. Printed to terminal:
     "Session closed. Next session:
      bricklayer resume"

GATE:
  OUTPUTS — run `bricklayer close-session`, confirm:
  session-log.md exists with Groq output, STATE.md exists with
  correct current position, terminal prints next session
  instruction. Run with missing Groq key → clear error, exit 1.

BLOCKER:
  This is the last Phase 3 brick. Completes the full session
  management loop: pause → resume → commit → close-session.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/close_session.py
- cli/main.py
- tests/test_close_session.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Happy path
- Valid state.json + Groq key → session-log.md written,
  STATE.md written, correct terminal output, exit 0.

2) session-log.md format
- Timestamp present, brick status present, Groq output present.

3) STATE.md format
- All 4 fields present (current project, current brick, last
  action, next command), values match state.json.

4) Missing GROQ_API_KEY
- Error "GROQ_API_KEY not set in environment", exit 1,
  no files written, no raw traceback.

5) Missing state.json
- Clear error, exit 1, no raw traceback.

6) Groq call fails (mock non-200 response)
- Clear error, exit 1, session-log.md not written in partial state.

7) Missing sprint-brain.md path in bricklayer.yaml
- Clear error naming the missing path, exit 1.

8) CliRunner integration
- Invoke `bricklayer close-session` via CliRunner with mocked
  Groq call, assert exit code, file existence, and STATE.md content.

TEST REQUIREMENTS:
- Happy path: valid state + Groq key → both files written, exit 0
- session-log.md format: timestamp, brick status, Groq output
- STATE.md format: 4 fields present, values match state.json
- Missing GROQ_API_KEY: error message, exit 1, no files written
- Missing state.json: error, exit 1, no traceback
- Groq call fails: error, exit 1, no partial files
- Missing sprint-brain.md: error naming path, exit 1
- CliRunner: exit 0, files exist, STATE.md content correct

OUT OF SCOPE:
- Pushing to remote
- Sending notifications or webhooks
- Any git operations
- Groq model selection (always llama-3.1-8b-instant)
