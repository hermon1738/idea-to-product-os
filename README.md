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
       │                  │                │                      │
       ▼                  ▼                │                      │
  Repo Auditor  ──▶  Venture OS ◀──────────┘                      │
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

### Step 2 — Run the bootstrap setup

This is mandatory before the first brick runs. Do not skip it.

First, update the `test:` section in `bricklayer.yaml` with your project's
test path before running anything else:

```yaml
test:
  language: Python
  command: python3 -m pytest -v ../proxy/
```

**IMPORTANT — target the package root, not a `tests/` subdirectory.**
If tests are co-located with modules (e.g. `proxy/providers/groq/tests/`),
a path like `../proxy/tests/` silently skips them. Always use the highest
common ancestor that contains all your tests. Wrong path = silent PASS
with missing test coverage.

`context.txt` is auto-generated from this — never edit it directly.

Then run the bootstrap:

```bash
# Set git editor — prevents vim blocking the terminal during merges
git config core.editor "nano"

# Create bricklayer runtime directories
mkdir -p bricklayer/skeptic_packet

# Write initial state.json
# CRITICAL: current_phase and current_feature MUST include the full branch
# prefix — use "phase/0-name" not "0-name", "feature/my-project" not "my-project".
# Wrong prefixes cause --verdict PASS to fail on merge.
cat > bricklayer/state.json << 'EOF'
{
  "current_brick": "0.1-first-brick",
  "current_phase": "phase/0-phase-name",
  "current_feature": "feature/project-name",
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

### Step 3 — Validate and write context.txt

`bricklayer run` validates all paths in `bricklayer.yaml` and writes
`bricklayer/context.txt` automatically from the `test:` section. Run this
once after bootstrap and any time you change `bricklayer.yaml`.

```bash
bricklayer run                  # validates all paths + writes context.txt
cat bricklayer/context.txt      # confirm it wrote correctly
```

Expected output:
```
# AUTO-GENERATED by bricklayer — do not edit manually
LANGUAGE: Python
TEST_COMMAND: python3 -m pytest -v ../YOUR_TEST_PATH/
```

If `bricklayer run` reports missing paths, fix every `/path/to/idea-to-product-os`
placeholder in `bricklayer.yaml` and run `bricklayer run` again until it shows:
`bricklayer.yaml loaded and all paths validated.`

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

**test command targeting wrong path causes silent test skips**
Setting `test.command` to a specific `tests/` subdirectory (e.g.
`../proxy/tests/`) silently skips all tests co-located with modules
in subdirectories. The test run reports PASS with a low count — the
skeptic has no signal that entire test suites were never executed.
Always target the package root: `../proxy/` not `../proxy/tests/`.
See stack-rules.md Test Discovery Rule for the full rule.

**make_skeptic_packet.py hardcoded pytest path (fixed)**
The tool originally ran `pytest -q` with no path argument, causing exit 5
(no tests found) because it ran from `bricklayer/` CWD. It now reads
`TEST_COMMAND` from `context.txt`. This fix is in the current repo.

**context.txt is auto-generated — never edit it manually**
`context.txt` is written by `bricklayer run` from the `test:` section of
`bricklayer.yaml`. Editing it directly will cause it to be overwritten on
the next `bricklayer run`. Always change `bricklayer.yaml` instead, then
run `bricklayer run` to apply.

**bricklayer run is the validation command**
`bricklayer run` is the command that validates all paths in `bricklayer.yaml`
and writes `context.txt`. Run it after bootstrap and after any change to
`bricklayer.yaml`. Other commands like `bricklayer build` or `bricklayer status`
do not trigger path validation or context.txt write.

**state.json location**
Lives at `bricklayer/state.json`. Not at root `state.json`. Not at `.workflow/state.json`.

**state.json required fields and branch prefix format**
All of the following fields are required or bricklayer rejects the file:
`current_brick`, `current_phase`, `current_feature`, `status`, `loop_count`,
`last_gate_failed`, `completed_bricks`, `next_action`, `last_test_run`.
`last_test_run` itself requires: `command`, `status`, `exit_code`, `artifact`,
`failed_nodeids`.

**CRITICAL — branch prefix format:** `current_phase` and `current_feature` must
include the full branch prefix. Write `"phase/0-llm-proxy"` not `"0-llm-proxy"`.
Write `"feature/remote-build-executor"` not `"remote-build-executor"`. Wrong
values cause `--verdict PASS` to fail with a git checkout error. The CLI writes
these correctly when `bricklayer branch` runs — only manual state.json edits
can introduce this error.

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
bricklayer run                       # validate yaml + write context.txt
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