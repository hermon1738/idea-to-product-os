# Bricklayer — Build System

The `bricklayer/` directory contains the build tooling that the CLI wraps.
You do not invoke these tools directly — use the `bricklayer` CLI commands.

---

## How It Works

Work is broken into bricks — small, scoped, testable units.
Each brick has a contract in `spec.md`. The CLI enforces that contract at every step.

One active brick at a time. One gate between each step.
Nothing moves forward without passing the gate.

---

## Directory Structure

```
bricklayer/
├── spec.md              ← active brick contract (FILES, ACCEPTANCE CRITERIA, GATE)
├── state.json           ← current position (brick, last_action, loop_count)
├── state-schema.md      ← state.json field definitions
├── BUILDER.md           ← builder rules (read by AI at brick start)
├── WORKFLOW.md          ← full workflow SOP (reference)
├── INTAKE.md            ← how new bricks enter the system
├── roadmap.md           ← all planned bricks and phases
├── manifest.md          ← project manifest
├── skeptic-gate.md      ← skeptic review protocol
├── skeptic_packet/      ← evidence bundle generated per brick
├── PROMPTS/
│   └── BUILDER_PROMPT.md ← what the builder AI reads to start a brick
└── tools/
    ├── print_brick_contract.py      ← prints spec.md in structured format
    ├── verify_files_touched.py      ← checks edited files match spec FILES list
    ├── run_tests_and_capture.py     ← runs test suite, captures output
    ├── make_skeptic_packet.py       ← assembles skeptic_packet/ evidence bundle
    └── update_state.py              ← advances state.json on verdict PASS
```

---

## The Build Sequence

Run via `bricklayer build` commands — not directly.

```
bricklayer build --snapshot       → verify_files_touched.py --snapshot-init
bricklayer build --verify         → verify_files_touched.py
bricklayer build --test           → run_tests_and_capture.py
bricklayer build --skeptic-packet → make_skeptic_packet.py
bricklayer build --verdict PASS   → update_state.py --complete + git commit + merge
```

---

## spec.md Contract Format

```
BRICK: Brick N - Name

FILES:
- path/to/file.py
- path/to/test_file.py

ACCEPTANCE CRITERIA:
1) Description of what must be true

TEST REQUIREMENTS:
- Happy path: ...
- Edge case: ...

OUT OF SCOPE:
- What is explicitly NOT included
```

The `verify_files_touched.py` tool exits 1 if any edited file is not in the FILES list.
The `update_state.py` tool rejects completion if `Verdict: PASS` is not in `skeptic_verdict.md`.

---

## Gate Rules

- loop_count >= 3 → hard stop, rescope the brick, reduce scope
- Skeptic must be a different AI than the builder
- `skeptic_verdict.md` is written by the human, never by the builder AI
- Files not in spec.md FILES list must not be touched

---

## For New Projects

If you are using this build system in a new project (not this repo),
you do not copy the `bricklayer/` directory. You copy `templates/bricklayer.yaml`
to your project root and point it at the tools in this repo.

See the root README for setup instructions.
