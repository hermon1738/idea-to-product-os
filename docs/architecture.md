# Architecture — Idea-to-Product OS

## System Map

```
IDEA
  │
  ▼
VENTURE OS ──────────────────────────────────── Phase 2
Any AI + system-prompts/venture-os.md
Outputs: Org Schema
  │
  ▼
ORG SCHEMA FORMATTER ────────────────────────── Live Agent
Discord !schema command
Converts raw Co-CEO session to clean structured Org Schema
  │
  ▼
AGENT-OS ────────────────────────────────────── Phase 3
Any AI + system-prompts/agent-os.md
Designs agent hierarchy
Outputs: PROJECT BRIEF per agent
  │
  ▼
ASSIGNMENT DISPATCHER ───────────────────────── Live Agent
Discord !dispatch command
Converts Org Schema → one Bricklayer brief per agent
  │
  ▼
BRICKLAYER CLI + AI TOOL ────────────────────── Phases 4+5
bricklayer branch → bricklayer build sequence
Builder AI implements. Skeptic AI reviews. Verdict: PASS required.
One brick at a time. Three-level branch hierarchy.
  │
  ▼
DEPLOYED ORGANIZATION
  ├── Content Agent    → recurring content tasks
  ├── Research Agent   → scheduled monitoring
  ├── Ops Agent        → metrics and reporting
  └── [any software via Bricklayer]
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
  System prompts, docs, Bricklayer CLI source, build tooling

hermon1738/ai-agents            ← live agents
  ~/ai-agents/agents/[agent-name]/agent.py + Dockerfile

Your project repos               ← your products
  Clean product code + bricklayer.yaml pointing to OS tooling
```

---

## Bricklayer CLI

The CLI automates Phases 4–6. It is installed from this repo and used globally.

```
bricklayer branch      ← create feature/phase/brick branches
bricklayer build       ← run the build sequence (snapshot/verify/test/skeptic/verdict)
bricklayer status      ← current position
bricklayer next        ← next command to run
bricklayer pause       ← save session state
bricklayer resume      ← restore session state
bricklayer close-phase ← merge phase → feature
bricklayer close-feature ← merge feature → main
```

408 tests. Three-level branching model. Gate-enforced build loop.

---

## Three-Level Branching

```
main
 └── feature/<n>              (isolated per product or workstream)
      └── phase/<N>-<n>       (isolated per phase within a feature)
           └── brick/<N>-<n>  (isolated per brick within a phase)
```

Merge direction is always upward:
- brick/* → phase/* via `bricklayer build --verdict PASS`
- phase/* → feature/* via `bricklayer close-phase`
- feature/* → main via `bricklayer close-feature`

Multiple features can run in parallel as independent branches from main.

---

## Live Agents (current)

| Agent | ID | Command | Runtime | Status |
|-------|----|---------|---------|--------|
| Session Scribe | AGT-SYS-001 | `!scribe`, `!log`, `!status` | Raw Python | Live |
| Org Schema Formatter | AGT-SYS-002 | `!schema` | Raw Python | Live |
| Assignment Dispatcher | AGT-SYS-003 | `!dispatch` | Raw Python | Live |

All agents run on Hetzner CPX21, Ubuntu 24.04, Docker CE.
Source: hermon1738/ai-agents.

---

## Infrastructure Defaults

All agents follow `system-prompts/stack-rules.md`.

| Component | Choice | Reason |
|-----------|--------|--------|
| Host | Hetzner VPS CPX21 | Low cost, persistent, full control |
| Runtime | Docker CE | Isolated, reproducible, auto-restart |
| Base image | python:3.11-slim | Minimal, consistent |
| LLM | Groq llama-3.1-8b-instant | Fast, free tier sufficient |
| Control | Discord | Free, channel-per-agent structure |
| Secrets | --env-file ~/ai-agents/.env | Never hardcoded |

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
        │◀────────────────────────────│
        │ skeptic_verdict.md          │
        │ Verdict: PASS or FAIL       │
```

The AI that builds cannot review its own work.
loop_count reaches 3 → stop, rescope the brick.
