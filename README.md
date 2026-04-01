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

**Current state:** Bricklayer CLI operational with 408 tests. Pipeline phases 1–7 running.

---

## How the Pipeline Works

```
Idea
 ↓
Venture OS ─→ Org Schema + Phase Confirmation
 ↓
arch-brain ─→ ARCHITECTURE.md (approved)
 ↓
Agent-OS    ← only if AI Layer exists
 ↓
plan-brain ─→ phases + bricks
 ↓
Claude Code ─→ one brick at a time
 ↓
Bricklayer CLI ─→ gates, state, branches
```

**Venture OS** — stress-tests the idea, maps it to architecture layers, confirms phases
with the Co-CEO before proceeding. No build starts without this gate.

**arch-brain** — takes the confirmed schema, runs an architecture options session,
and produces `docs/ARCHITECTURE.md` — the single source of truth for the entire build.
Two approval gates before the document is locked. All downstream planning loads this file.

**Agent-OS** — designs AI components: agent hierarchy, triggers, inputs, outputs, tools,
failure modes. Only runs when the architecture includes an AI layer. Skipped for
products without AI (web apps, CLI tools, pure backend systems).

**plan-brain** — receives the approved architecture, breaks the build into phases and bricks.
Every brick has a FILES list, Acceptance Criteria, Test Requirements, and Out of Scope.
Every handoff loads `ARCHITECTURE.md` to stay aligned.

**Bricklayer CLI** — manages state, branches, gates, and sessions. Claude Code (or any
builder AI) works one brick at a time through a gated build loop: implement → verify →
test → skeptic review → PASS → close.

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

- **AGENT** — An AI agent or multi-agent system with memory, cron, or tool-calling.
- **WEB_APP** — A user-facing web application with frontend, backend, and database layers.
- **SYSTEM** — A backend service, API, or infrastructure component without a UI.
- **CLI_TOOL** — A command-line tool for developer or operator use.

Stack defaults and code standards for each type are in `system-prompts/stack-rules.md`.

---

## Quick Start

**Step 1** — Load `system-prompts/venture-os.md` into any AI chat. Describe your idea.

**Step 2** — Confirm phases from the Org Schema output. Do not proceed until the Co-CEO approves.

**Step 3** — Load `system-prompts/arch-brain.md`. Run the architecture session. Approve two gates.

**Step 4** — Approve `docs/ARCHITECTURE.md`. This document is now locked as the source of truth.

**Step 5** — Load `system-prompts/plan-brain.md`. Hand it the approved architecture. Generate build plan.

**Step 6** — Hand Brick 1 to Claude Code (or any builder AI). Follow the bricklayer build loop.

**Step 7** — After each brick closes, run `system-prompts/sprint-brain.md` for sprint review.

---

## Infrastructure

Hetzner VPS CPX21, Docker CE, Groq free tier, Discord for agent control.
Target cost: ~$30/mo. Three live agents currently running on the VPS.
Agent source lives at [hermon1738/ai-agents](https://github.com/hermon1738/ai-agents).

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
cp /path/to/idea-to-product-os/templates/env.example .env
# Edit bricklayer.yaml — replace all /path/to/idea-to-product-os
# Edit .env — set GROQ_API_KEY and DOCS_PATH for THIS project
```

**Step 2 — Update the paths in `bricklayer.yaml`:**

Open `bricklayer.yaml` and replace every `/path/to/idea-to-product-os`
with the absolute path to your actual installation.

**Step 3 — Verify:**

```bash
bricklayer --help
```

The CLI validates every path on startup and tells you exactly which ones are missing.

**Step 4 — Start building:**

```bash
bricklayer branch --feature my-feature
bricklayer branch --phase 1 scaffold
bricklayer branch 1 first-brick
bricklayer status
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
