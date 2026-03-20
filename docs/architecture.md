# Architecture — Idea-to-Product OS

## System Map

```
IDEA
  │
  ▼
VENTURE OS ──────────────────────────────────── Phase 2
Any AI + venture-os.md
Outputs: Org Schema
  │
  ▼
ORG SCHEMA FORMATTER ────────────────────────── Live Agent
Discord !schema command
Converts raw Co-CEO output to clean structured Org Schema
  │
  ▼
AGENT-OS ────────────────────────────────────── Phase 3
Any AI + agent-os.md
Designs agent hierarchy
Outputs: PROJECT BRIEF per agent
  │
  ▼
ASSIGNMENT DISPATCHER ───────────────────────── Live Agent
Discord !dispatch command
Converts Org Schema → one Bricklayer brief per agent automatically
  │
  ▼
BRICKLAYER BLUEPRINT ────────────────────────── Phase 4+5
roadmap.md → spec.md → Builder AI → skeptic_packet → Skeptic AI
One brick at a time. Independent review. Verdict: PASS required.
  │
  ▼
DEPLOYED COMPANY
  ├── Content Agent    → recurring content tasks
  ├── Research Agent   → scheduled monitoring
  ├── Ops Agent        → metrics and reporting
  ├── Code Agent       → feature implementation
  └── [any software the business needs via Bricklayer]
  │
  ▼
HUMAN OVERSIGHT
Approves external actions. Reviews Skeptic verdicts.
Handles judgment that agents cannot reliably make.
  │
  ▼
SESSION SCRIBE ──────────────────────────────── Live Agent
Discord !scribe command
Logs every session. Rewrites pipeline-status.md.
Closes the loop between sessions.
```

---

## The Three Repos

```
hermon1738/idea-to-product-os   ← this repo
  System prompts, docs, Bricklayer Blueprint, infrastructure

hermon1738/ai-agents            ← live agents
  ~/ai-agents/agents/[agent-name]/agent.py + Dockerfile
  One folder per deployed agent

hermon1738/Bricklayer_blueprint ← build engine source
  The canonical Bricklayer Blueprint
  Referenced as submodule or copied into idea-to-product-os/bricklayer/
```

---

## Live Agents (current)

| Agent | Command | What It Does |
|-------|---------|-------------|
| Session Scribe | `!scribe`, `!log`, `!status`, `!debug` | Logs sessions to decision-log.md and pipeline-status.md |
| Org Schema Formatter | `!schema` | Converts Co-CEO session dump to clean Org Schema |
| Assignment Dispatcher | `!dispatch` | Converts Org Schema to Bricklayer briefs, one per agent |

---

## Infrastructure Defaults

All agents follow these rules. Defined in `system-prompts/stack-rules.md`.

| Component | Choice | Reason |
|-----------|--------|--------|
| Host | Hetzner VPS CPX21 | Low cost, persistent, full control |
| Runtime | Docker CE | Isolated, reproducible, auto-restart |
| Base image | python:3.11-slim | Minimal, consistent |
| LLM | Groq (llama-3.1-8b-instant) | Fast, free tier sufficient |
| Control | Discord | Free, channel-per-agent org structure |
| Secrets | --env-file ~/ai-agents/.env | Single source, never hardcoded |

---

## The Skeptic System

The most important architectural decision in the build layer.

```
Builder AI                    Skeptic AI
(Claude Code / Codex)         (GPT-4 / Gemini — DIFFERENT tool)
        │                             │
        │ implements brick            │
        │ runs verify tools           │
        │ generates skeptic_packet/   │
        │─────────────────────────────▶
        │                             │ runs skeptic-gate.md
        │                             │ Flaw Hunt
        │                             │ Blind Spot Hunt
        │                             │ Scaling Check
        │                             │ Failure-First Challenge
        │                             │
        │◀────────────────────────────│
        │ skeptic_verdict.md          │
        │ Verdict: PASS or FAIL       │
```

**Why this matters:** An AI reviewing its own work has a systematic
bias toward approving it. The Skeptic system breaks this by requiring
a different AI — with no context of how the brick was built — to
challenge the output before it ships.

loop_count reaches 3 → stop, rescope the brick, reduce scope.
