# Idea-to-Product OS

A tool-independent operating system for running AI-powered companies.
Take any business idea from concept to deployed agents doing real work.

---

## What This Is

Idea-to-Product OS is a system of prompts, workflows, and live agents
that turns a business idea into a running organization — with AI agents
handling recurring operational work and a human overseeing approvals.

It is not tied to any single AI tool. The system prompts are plain
markdown files. Use Claude, GPT-4, Gemini, Codex — the workflow
rules stay the same regardless of tool.

---

## The Three Layers

```
LAYER 1 — SYSTEM PROMPTS (AI-agnostic)
  Markdown files that define how each phase works.
  Load them into any AI chat to activate that phase.

LAYER 2 — BRICKLAYER BLUEPRINT (build engine)
  Tool-independent workflow for building software brick by brick.
  Includes an independent Skeptic review system — a different AI
  reviews every brick before it ships. No self-validation.

LAYER 3 — LIVE AGENTS (running infrastructure)
  Discord bots deployed on a VPS via Docker.
  Handle recurring tasks, logging, and pipeline automation.
```

---

## The Pipeline

```
Entry Point A: GitHub repo to evaluate  → Start at Phase 1
Entry Point B: Original idea            → Start at Phase 2
Entry Point C: Know what to build       → Start at Phase 3
Entry Point D: Have a spec ready        → Start at Phase 4
```

| Phase | Tool | What It Does |
|-------|------|-------------|
| 1 | Repo Auditor | Evaluates GitHub repos, outputs Agent spec or Project Brief |
| 2 | Venture OS | Co-CEO strategy session, stress-tests the idea, outputs Org Schema |
| 3 | Agent-OS | Designs agent hierarchy, outputs Bricklayer briefs |
| 4 | Bricklayer / plan-brain | Breaks work into bricks with gates |
| 5 | Implement | Builder AI codes the brick |
| 5b | Skeptic Review | Different AI reviews the brick via skeptic-gate.md |
| 6 | Sprint Review | sprint-brain reviews what shipped, outputs next brick |
| 7 | Session Scribe | Logs every session to decision-log.md automatically |

**Rule: start as early in the pipeline as you can afford to.
Venture OS takes 10 minutes. Building the wrong thing takes days.**

---

## Repository Structure

```
idea-to-product-os/
├── README.md                  ← this file
├── docs/
│   ├── vision.md              ← the full system vision
│   ├── pipeline.md            ← phase-by-phase breakdown
│   ├── architecture.md        ← how all layers connect
│   └── getting-started.md     ← set up on a new machine
├── system-prompts/            ← load into any AI chat
│   ├── venture-os.md
│   ├── agent-os.md
│   ├── repo-auditor.md
│   └── stack-rules.md
├── bricklayer/                ← full Bricklayer Blueprint
│   ├── README.md
│   ├── WORKFLOW.md
│   ├── skeptic-gate.md
│   ├── PROMPTS/
│   └── tools/
├── agents/                    ← see hermon1738/ai-agents
│   └── README.md
└── infrastructure/
    ├── docker-compose.yml
    └── env.example
```

---

## Related Repositories

| Repo | Purpose |
|------|---------|
| [hermon1738/ai-agents](https://github.com/hermon1738/ai-agents) | Live deployed agents (Session Scribe, org-schema-formatter, assignment-dispatcher) |
| [hermon1738/Bricklayer_blueprint](https://github.com/hermon1738/Bricklayer_blueprint) | Bricklayer Blueprint source |

---

## Core Principles

- **Small bricks pass. Large bricks fail.** When in doubt, reduce scope.
- **No self-validation.** The AI that builds a brick cannot review it.
- **Log everything.** Empty decision logs = context loss at scale.
- **Fill capacity before adding infra.** Don't add new services when existing ones can handle the load.
- **Human gates on irreversible actions.** Deployments and external communications require human approval.
- **Push to GitHub after every deploy.** The VPS is not a backup.
