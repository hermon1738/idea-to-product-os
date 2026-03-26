# Idea-to-Product OS

A pipeline for turning ideas into running AI organizations.
You are the Co-CEO. AI agents are your employees.
Every build is gated, reviewed, and logged.

---

## What This Is

A system for running AI-powered software businesses with minimal manual overhead.
The pipeline takes you from a raw idea all the way to deployed, running agents —
with structured review at every step so nothing ships without being challenged.

The human handles judgment, approvals, and external relationships.
Agents handle the repeatable operational work.

**Current state:** Pipeline Phases 1–7 operational. Bricklayer CLI (Phases 4–6)
ships with 408 tests. Three live agents on Hetzner VPS.

---

## How It Works

```
IDEA
  │
  ▼
Phase 1 — Repo Auditor       Evaluate a GitHub repo. Should you build on it?
Phase 2 — Venture OS         Stress-test your idea. Build / Adapt / Ignore.
Phase 3 — Agent-OS           Design the agent hierarchy. What agents? What jobs?
Phase 4 — Bricklayer Plan    Break the build into gated bricks. One at a time.
Phase 5 — Build + Review     AI builds. Different AI reviews. Verdict: PASS required.
Phase 6 — Sprint Review      Close the brick. Log what shipped.
Phase 7 — Session Scribe     Log the session. Keep context alive between sessions.
  │
  ▼
DEPLOYED AGENT ORGANIZATION
  Running on Hetzner VPS. Managed via Docker. Triggered via Discord.
```

Not every idea starts at Phase 1. See [`docs/pipeline.md`](docs/pipeline.md) for entry points.

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
tests, or infrastructure. They only need one file: `bricklayer.yaml`.

**Step 1 — Copy the template into your new project:**

```bash
mkdir my-project && cd my-project
git init
cp /path/to/idea-to-product-os/templates/bricklayer.yaml ./bricklayer.yaml
```

**Step 2 — Update the paths in `bricklayer.yaml`:**

Open `bricklayer.yaml` and replace every `/path/to/idea-to-product-os`
with the absolute path to your actual installation.

Example — if your OS lives at `/Users/tony/projects/idea-to-product-os`:

```yaml
phases:
  plan:   /Users/tony/projects/idea-to-product-os/system-prompts/plan-brain.md
  review: /Users/tony/projects/idea-to-product-os/system-prompts/sprint-brain.md

tools:
  verify:  /Users/tony/projects/idea-to-product-os/bricklayer/tools/verify_files_touched.py
  # ... etc
```

**Step 3 — Verify:**

```bash
bricklayer --help
```

The CLI validates every path on startup and tells you exactly which ones
are missing before anything runs.

**Step 4 — Start building:**

```bash
bricklayer branch --feature my-feature
bricklayer branch --phase 1 scaffold
bricklayer branch 1 first-brick
bricklayer status
```

Your project repo stays clean — no bricklayer source, no tools, no tests.
Just your product code and `bricklayer.yaml`.

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
│   ├── venture-os.md           ← Phase 2: idea strategy
│   ├── agent-os.md             ← Phase 3: agent design
│   ├── plan-brain.md           ← Phase 4: build planning
│   ├── sprint-brain.md         ← Phase 6: sprint review
│   ├── repo-auditor.md         ← Phase 1: repo evaluation
│   └── stack-rules.md          ← engineering standards (apply everywhere)
│
├── docs/                       ← human documentation
│   ├── pipeline.md             ← full pipeline explained, entry points
│   ├── getting-started.md      ← setup guide for new machines
│   ├── architecture.md         ← system map, live agents, three repos
│   └── vision.md               ← where this is going
│
├── cli/                        ← bricklayer CLI source (Python)
├── bricklayer/                 ← build tooling: tools/, spec.md, state.json
├── tests/                      ← CLI test suite (408 tests)
├── context/                    ← living session context files
│   ├── pipeline-status.md      ← current state of every component
│   └── decision-log.md         ← append-only session history
│
├── agents/                     ← agent registry and docs
│   └── README.md               ← live agents list (source: hermon1738/ai-agents)
└── infrastructure/             ← VPS and Docker config
```

---

## Using Any AI Tool

The system prompts are AI-agnostic. They work with Claude, GPT-4, Gemini, Codex,
Cursor, or any capable AI. The rules stay the same regardless of tool.

See [`AGENT.md`](AGENT.md) — the AI-tool entry point read by any AI at session start.

**Skeptic rule:** the AI that builds a brick cannot review it.
Builder: Claude Code / Codex. Skeptic: GPT-4 / Gemini. Always different tools.

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

## Live Agents

Three agents running on Hetzner VPS.
Source: [hermon1738/ai-agents](https://github.com/hermon1738/ai-agents).

| Agent | Trigger | Job |
|-------|---------|-----|
| Session Scribe | `!scribe` in Discord | Logs sessions, updates decision-log.md and pipeline-status.md |
| Org Schema Formatter | `!schema` in Discord | Converts Co-CEO session dump to structured Org Schema |
| Assignment Dispatcher | `!dispatch` in Discord | Converts Org Schema → one Bricklayer brief per agent |

---

## Key Documents

| Document | What it answers |
|----------|----------------|
| [`docs/pipeline.md`](docs/pipeline.md) | How does the full pipeline work? |
| [`docs/getting-started.md`](docs/getting-started.md) | How do I set this up on a new machine? |
| [`docs/architecture.md`](docs/architecture.md) | How do all the pieces connect? |
| [`docs/vision.md`](docs/vision.md) | Where is this going? |
| [`system-prompts/stack-rules.md`](system-prompts/stack-rules.md) | Engineering standards |
| [`DEBT.md`](DEBT.md) | Known limitations |
| [`templates/bricklayer.yaml`](templates/bricklayer.yaml) | Starting point for new projects |

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
