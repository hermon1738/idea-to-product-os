# Idea-to-Product OS

A general-purpose software planning and build pipeline that takes any software idea
from concept to deployed code — brick by brick.

---

## What This Is

A structured pipeline for turning software ideas into shipped products.
The system works for any product type: AI agents, web apps, backend systems, CLI tools.
Every stage is gated. Nothing moves forward without approval. Nothing ships without being challenged.

The human (Co-CEO) handles judgment, approvals, and architecture decisions.
AI tools handle implementation, review, and documentation — one verified brick at a time.

**Current state:** Bricklayer CLI operational with 811 tests. Pipeline v2 running.

---

## How the Pipeline Works

Not every idea starts at the same point. Entry depends on what you have.

```
  [A] GitHub repo    [B] Raw idea    [C] Clear concept    [D] Written spec
       │                  │                │                     │
       ▼                  ▼                │                     │
  Repo Auditor  ──▶  Venture OS ◀──────────┘                     │
  evaluate repo      stress-test idea                             │
                     Org Schema + Phase Confirmation              │
                          │                                       │
                          ▼                                       │
                      arch-brain                                  │
                      architecture session                        │
                      ARCHITECTURE.md (approved)                  │
                          │                                       │
                          ▼                                       │
                      Agent-OS ← only if AI Layer exists          │
                      design agents                               │
                          │                                       │
                          └───────────────────┬───────────────────┘
                                              ▼
                                         plan-brain
                                         phases + bricks
                                              │
                              ┌───────────────▼───────────────┐
                              │         BUILD LOOP            │
                              │   Builder AI implements       │
                              │   Skeptic AI reviews    ──── FAIL ──▶ fix & retry
                              │   Verdict: PASS               │       (max 3 loops)
                              └───────────────┬───────────────┘
                                              │ PASS
                                              ▼
                                        sprint-brain
                                        close brick, plan next
                                              │
                                              ▼
                                     SHIPPED PRODUCT
                                  Hetzner VPS · Docker · Discord
```

**Venture OS** — stress-tests the idea, maps it to architecture layers, confirms phases
with the Co-CEO before proceeding. No build starts without this gate.

**arch-brain** — takes the confirmed schema, runs an architecture options session,
and produces `docs/ARCHITECTURE.md` — the single source of truth for the entire build.
Two approval gates before the document is locked. All downstream planning loads this file.

**Agent-OS** — designs AI components: agent hierarchy, triggers, inputs, outputs, tools,
failure modes. Only runs when the architecture includes an AI layer. Skipped for
products without AI.

**plan-brain** — receives the approved architecture, breaks the build into phases and bricks.
Every brick has a FILES list, gate conditions, and tests. Every handoff loads `ARCHITECTURE.md`.

**Bricklayer CLI** — manages state, branches, gates, and sessions. Claude Code (or any
builder AI) works one brick at a time through a gated build loop.

**sprint-brain** — runs after every brick closes. Sprint review, debt log, next brick.

See [`docs/pipeline.md`](docs/pipeline.md) for a deep reference on each stage.

---

## System Files

| File | Role | When to load |
|------|------|--------------|
| `system-prompts/venture-os.md` | Idea stress-test + Org Schema | Start of any new idea |
| `system-prompts/arch-brain.md` | Architecture session → ARCHITECTURE.md | After Venture OS phase confirmation |
| `system-prompts/agent-os.md` | AI layer design | Only when Org Schema has an AI Layer |
| `system-prompts/plan-brain.md` | Brick planning | After ARCHITECTURE.md is approved |
| `system-prompts/sprint-brain.md` | Sprint review after each brick | End of every build session |
| `system-prompts/repo-auditor.md` | GitHub repo audit → project briefs | When evaluating external repos |
| `system-prompts/stack-rules.md` | Stack defaults + code architecture standards | Referenced by all other files |
| `context/decision-log.md` | Append-only session history | Updated after every session |
| `context/pipeline-status.md` | Current state snapshot | Updated each session |

---

## Product Types

The pipeline supports four product types. The architecture stage determines which apply.

- **AGENT** — Background automation. Discord or cron triggered. No UI.
- **WEB_APP** — Browser UI + backend + database. docker-compose on VPS.
- **SYSTEM** — Multi-layer software. Stack decided per project during Venture OS.
- **CLI_TOOL** — Python package. Local install. No server.

Stack defaults and code standards for each type are in `system-prompts/stack-rules.md`.

---

## Install

```bash
git clone https://github.com/hermon1738/idea-to-product-os.git
cd idea-to-product-os
pip install -e .
bricklayer --help
```

`bricklayer` is now a global command on your machine — use it from any project.

---

## Starting a New Project

The CLI is a global tool. New projects do not contain bricklayer source code,
tests, or infrastructure. They only need `bricklayer.yaml` and a small set of
bootstrap files.

### Step 1 — Create the repo and copy the template

```bash
mkdir my-project && cd my-project
git init
cp /path/to/idea-to-product-os/templates/bricklayer.yaml ./bricklayer.yaml
```

Open `bricklayer.yaml` and replace every `/path/to/idea-to-product-os`
with the absolute path to your actual installation.

### Step 2 — Run the bootstrap script

This is mandatory before the first brick runs. It creates all the files
bricklayer needs and verifies the tooling works end-to-end.

```bash
# Set git editor — avoids vim blocking the terminal during merges
git config core.editor "nano"

# Create bricklayer runtime directories
mkdir -p bricklayer/skeptic_packet

# Write initial state.json
# Update current_brick, current_phase, current_feature to match your first brick
cat > bricklayer/state.json << 'EOF'
{
  "current_brick": "BRICK_ID",
  "current_phase": "PHASE_NAME",
  "current_feature": "FEATURE_NAME",
  "status": "in_progress",
  "loop_count": 0,
  "last_gate_failed": null,
  "completed_bricks": [],
  "next_action": "snapshot_init",
  "last_test_run": {
    "command": "",
    "status": "",
    "exit_code": 0,
    "artifact": "",
    "failed_nodeids": []
  }
}
EOF

# Write context.txt
# TEST_COMMAND path must be relative to bricklayer/ directory
# Use ../ to go up to the project root, e.g. ../proxy/tests/
cat > bricklayer/context.txt << 'EOF'
LANGUAGE: Python
TEST_COMMAND: python3 -m pytest -q ../YOUR_TEST_PATH/
EOF

# Write .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
.pytest_cache/

# Environment
.env

# Bricklayer runtime — never committed
bricklayer/skeptic_packet/
bricklayer/skeptic_verdict.md
bricklayer/state.json
bricklayer/context.txt
bricklayer/handover.md
.workflow/

# Workspace — runtime bind mount root
workspace/

# macOS
.DS_Store
EOF
```

### Step 3 — Verify the full tooling sequence before Brick 1

Run these four commands in order and confirm each exits cleanly.
Do not start Brick 1 until all four pass.

```bash
bricklayer build --snapshot    # must exit 0
bricklayer build --verify      # must exit 0 — "OK: all touched files in spec FILES list"
bricklayer build --test        # must exit 0 — "PASS" with correct test count
bricklayer build --skeptic-packet  # must exit 0 — test_output.txt must show passing tests
```

If `--test` passes but `--skeptic-packet` shows wrong test count, check that
`context.txt` TEST_COMMAND path resolves correctly from `bricklayer/` as CWD.

### Step 4 — Start building

```bash
bricklayer branch --feature my-feature
bricklayer branch --phase 0 bootstrap
bricklayer branch 0 first-brick
bricklayer status
```

---

## Known Bootstrap Issues

These were discovered during the first project build and are fixed — documenting
them here so they are never hit again.

**make_skeptic_packet.py hardcoded pytest path (fixed)**
The tool originally ran `pytest -q` with no path argument, causing exit 5
(no tests found) because it ran from `bricklayer/` CWD. It now reads
`TEST_COMMAND` from `context.txt`. This fix is in the current repo.

**state.json location**
Lives at `bricklayer/state.json`. Not at root `state.json`. Not at `.workflow/state.json`.

**context.txt TEST_COMMAND path**
Relative to `bricklayer/` as CWD, not the project root. Use `../` to reach
the project root. Example: `../proxy/tests/` not `proxy/tests/`.

**state.json required fields**
All six fields are required or bricklayer will reject the file on write:
`current_brick`, `current_phase`, `current_feature`, `status`, `loop_count`,
`last_gate_failed`, `completed_bricks`, `next_action`, `last_test_run`.
`last_test_run` itself requires: `command`, `status`, `exit_code`, `artifact`,
`failed_nodeids`.

**git editor**
Set `git config core.editor "nano"` before the first merge. The default vim
editor blocks the terminal on merge commits and requires knowing vim commands
to exit.

---

## Quick Command Reference

```bash
bricklayer status                    # where are we right now
bricklayer next                      # exact next command to run
bricklayer resume                    # restore last session context
bricklayer branch --feature <n>      # new feature (from main)
bricklayer branch --phase N <n>      # new phase (from feature/*)
bricklayer branch N <n>              # new brick (from phase/*)
bricklayer build                     # print brick contract
bricklayer build --snapshot          # baseline snapshot
bricklayer build --verify            # scope check
bricklayer build --test              # run test suite
bricklayer build --skeptic-packet    # package for review
bricklayer build --verdict PASS      # close brick
bricklayer close-phase               # merge phase → feature
bricklayer close-feature             # merge feature → main
bricklayer pause                     # save session state
bricklayer commit -m "msg"           # mid-brick checkpoint commit
bricklayer close-session             # sprint review + log
bricklayer new-project <name>        # scaffold a new project
bricklayer context [--project <n>]   # print project context for AI session
bricklayer agent list                # list all agents in registry
bricklayer agent status --id <id>    # full detail for one agent
bricklayer agent new --id <id> \
  --runtime nanobot|raw-python \
  --project <project> --role <role>  # scaffold + register a new agent
bricklayer agent deploy --id <id>    # push agent to deploy repo, print VPS cmds
bricklayer agent live --id <id>      # mark agent live after VPS confirmation
```

---

## Repository Structure

```
idea-to-product-os/
├── README.md                   ← you are here
├── AGENT.md                    ← AI-tool entry point (read first in any session)
├── CLAUDE.md                   ← Claude Code specific (auto-loaded by Claude Code)
├── DEBT.md                     ← tracked technical debt
├── bricklayer.yaml             ← CLI config for this repo
├── pyproject.toml              ← bricklayer CLI install config
│
├── templates/
│   └── bricklayer.yaml         ← copy this into any new project
│
├── system-prompts/             ← AI-agnostic phase prompts
│   ├── venture-os.md           ← idea stress-test + Org Schema
│   ├── arch-brain.md           ← architecture session → ARCHITECTURE.md
│   ├── agent-os.md             ← AI layer design (conditional)
│   ├── plan-brain.md           ← brick planning
│   ├── sprint-brain.md         ← sprint review after each brick
│   ├── repo-auditor.md         ← GitHub repo evaluation
│   └── stack-rules.md          ← engineering standards (apply everywhere)
│
├── docs/                       ← human documentation
│   ├── pipeline.md             ← deep reference: each stage explained
│   ├── workflow.md             ← visual ASCII workflow diagram
│   ├── getting-started.md      ← setup guide for new machines
│   ├── architecture.md         ← system map and live infrastructure
│   └── vision.md               ← where this is going
│
├── cli/                        ← bricklayer CLI source (Python)
├── bricklayer/                 ← build tooling: tools/, spec.md, state.json
├── tests/                      ← CLI test suite (811 tests)
├── context/                    ← living session context files
│   ├── pipeline-status.md      ← current state of every component
│   └── decision-log.md         ← append-only session history
│
├── agents/                     ← agent registry and docs
│   └── README.md               ← live agents list (source: hermon1738/ai-agents)
└── infrastructure/             ← VPS and Docker config
```

---

## Live Agents

Three agents running on Hetzner VPS.
Source: [hermon1738/ai-agents](https://github.com/hermon1738/ai-agents).

| Agent | Trigger | Job |
|-------|---------|-----|
| Session Scribe | `!scribe` in Discord | Logs sessions, updates decision-log.md and pipeline-status.md |
| Org Schema Formatter | `!schema` in Discord | Converts Co-CEO session dump to structured Org Schema |
| Assignment Dispatcher | `!dispatch` in Discord | Converts Org Schema → one Bricklayer brief per agent |

---

## The Skeptic Rule

The AI that builds a brick cannot review it.
Builder: Claude Code. Skeptic: Gemini. Always different tools.
`loop_count` reaches 3 → stop, rescope the brick. No exceptions.

---

## The Three Repos

```
hermon1738/idea-to-product-os   ← this repo
  Pipeline system, CLI, docs, build tooling

hermon1738/ai-agents            ← live agent source
  One folder per deployed agent. Runs on Hetzner VPS.

Your project repos               ← your actual products
  Clean product code. bricklayer.yaml points back to OS tooling.
```

---

## Key Documents

| Document | What it answers |
|----------|----------------|
| [`docs/pipeline.md`](docs/pipeline.md) | How does the full pipeline work? Why is it structured this way? |
| [`docs/workflow.md`](docs/workflow.md) | Visual ASCII diagram of the full flow |
| [`docs/getting-started.md`](docs/getting-started.md) | How do I set this up on a new machine? |
| [`docs/architecture.md`](docs/architecture.md) | How do all the pieces connect? |
| [`docs/vision.md`](docs/vision.md) | Where is this going? |
| [`system-prompts/stack-rules.md`](system-prompts/stack-rules.md) | Engineering standards |
| [`DEBT.md`](DEBT.md) | Known limitations and tracked debt |
| [`templates/bricklayer.yaml`](templates/bricklayer.yaml) | Starting point for new projects |