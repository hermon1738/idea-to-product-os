# Workflow — Idea-to-Product OS

Visual diagram of the full pipeline from raw idea to deployed agent organization.

---

## Full Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       IDEA-TO-PRODUCT OS — FULL FLOW                       │
└─────────────────────────────────────────────────────────────────────────────┘

  CHOOSE YOUR ENTRY POINT
  ────────────────────────────────────────────────────────────────────────────
   [A] GitHub repo         [B] Raw idea           [C] Concept clear      [D] Spec written
   to evaluate?            need strategy?          skip strategy          skip to plan
        │                       │                       │                      │
        ▼                       ▼                       │                      │
  ┌───────────┐         ┌───────────┐                   │                      │
  │ Phase 1   │         │ Phase 2   │                   │                      │
  │   Repo    │         │ Venture   │                   │                      │
  │  Auditor  │         │    OS     │                   │                      │
  │           │         │           │                   │                      │
  │ Drop URL  │         │ Describe  │                   │                      │
  │ → outputs │         │ idea →    │                   │                      │
  │ spec or   │         │ Org Schema│                   │                      │
  │   brief   │         │ + verdict │                   │                      │
  └─────┬─────┘         └─────┬─────┘                   │                      │
        │                     │                         │                      │
        └──────────┬──────────┘                         │                      │
                   │                                    │                      │
                   ▼                                    │                      │
             ┌───────────┐                              │                      │
             │ Phase 3   │◀─────────────────────────────┘                      │
             │ Agent-OS  │                                                      │
             │           │                                                      │
             │ Design    │                                                      │
             │ agent     │                                                      │
             │ hierarchy │                                                      │
             │ → PROJECT │                                                      │
             │   BRIEF   │                                                      │
             └─────┬─────┘                                                      │
                   │                                                            │
                   └────────────────────────────────────┬───────────────────────┘
                                                        │
                                                        ▼
                                                  ┌───────────┐
                                                  │ Phase 4   │
                                                  │Bricklayer │
                                                  │   Plan    │
                                                  │           │
                                                  │ Break work│
                                                  │ into gated│
                                                  │  bricks   │
                                                  │ → spec.md │
                                                  └─────┬─────┘
                                                        │
                                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                          BRICKLAYER BUILD LOOP  (Phase 5)                     │
│                                                                               │
│   bricklayer branch N brick-name        ← create brick branch                │
│            │                                                                  │
│            ▼                                                                  │
│   ┌─────────────────────┐                                                     │
│   │    Builder AI       │  Claude Code / Codex / GPT-4                        │
│   │                     │                                                     │
│   │  implement brick    │  (touch ONLY files in spec.md FILES section)        │
│   │  bricklayer build --snapshot                                              │
│   │  bricklayer build --verify                                                │
│   │  bricklayer build --test                                                  │
│   │  bricklayer build --skeptic-packet  ← packages for review                │
│   └──────────┬──────────┘                                                     │
│              │                                                                │
│              ▼                                                                │
│   ┌─────────────────────┐                                                     │
│   │    Skeptic AI       │  DIFFERENT tool from builder                        │
│   │  (GPT-4 / Gemini)   │                                                     │
│   │                     │                                                     │
│   │  Flaw Hunt          │                                                     │
│   │  Blind Spot Hunt    │                                                     │
│   │  Scaling Check      │                                                     │
│   │  Failure-First      │                                                     │
│   │                     │                                                     │
│   │  writes skeptic_    │                                                     │
│   │  verdict.md         │                                                     │
│   └──────────┬──────────┘                                                     │
│              │                                                                │
│         ┌────▼─────┐                                                          │
│         │ Verdict? │                                                          │
│         └────┬─────┘                                                          │
│       ┌──────┴───────┐                                                        │
│    PASS│           FAIL│                                                      │
│       ▼               ▼                                                       │
│  bricklayer       loop_count++                                                │
│  build            (max 3 loops)                                               │
│  --verdict PASS       │                                                       │
│       │            ┌──▼────────────────────────────┐                         │
│       │            │ loop < 3: fix and resubmit    │─────────────────────────┐│
│       │            │ loop = 3: rescope the brick   │                         ││
│       │            └───────────────────────────────┘                         ││
│       │                                                                       ││
└───────┼───────────────────────────────────────────────────────────────────────┘│
        │                                              rebuild loop ─────────────┘
        ▼
  ┌───────────┐
  │ Phase 6   │
  │  Sprint   │
  │  Review   │
  │           │
  │ Close     │
  │ brick.    │
  │ Log what  │
  │ shipped.  │
  │ Plan next.│
  └─────┬─────┘
        │
        ▼
  ┌───────────┐
  │ Phase 7   │
  │  Session  │
  │   Scribe  │
  │           │
  │  !scribe  │
  │ in Discord│
  │           │
  │ updates   │
  │ decision- │
  │ log.md +  │
  │ pipeline- │
  │ status.md │
  └─────┬─────┘
        │
        ▼
  ┌─────────────────────────────────────────────────────────┐
  │                 DEPLOYED AGENT ORGANIZATION             │
  │                                                         │
  │   Agents running on Hetzner VPS · Docker CE             │
  │   Triggered via Discord · Managed via bricklayer        │
  └─────────────────────────────────────────────────────────┘
        │
        │   (next session)
        ▼
  read pipeline-status.md → orient → continue building
```

---

## Git Branching Flow

```
  main
   │
   └── feature/<name>                 ← bricklayer branch --feature <name>
        │
        └── phase/<N>-<name>          ← bricklayer branch --phase N <name>
             │
             └── brick/<N>-<name>     ← bricklayer branch N <name>
                  │
                  │  (build loop runs here)
                  │
                  └──▶ merged back into phase/* on Verdict: PASS
                            │
                            └──▶ merged into feature/* via bricklayer close-phase
                                      │
                                      └──▶ merged into main via bricklayer close-feature

  Merge direction is always UPWARD. Never work directly on main.
```

---

## Session Lifecycle

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                        SESSION LIFECYCLE                            │
  └─────────────────────────────────────────────────────────────────────┘

  SESSION START                              SESSION END
  ────────────                               ───────────
  bricklayer resume       ───▶  work  ───▶  !scribe in Discord
  bricklayer status                          │
  bricklayer next                            ▼
                                        decision-log.md updated
                                        pipeline-status.md rewritten
                                             │
                                             ▼
                                        copy both files back into
                                        AI project context
                                             │
                                             ▼
                                        NEXT SESSION starts oriented
```

---

## The Three Repos

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │  hermon1738/idea-to-product-os    ← THIS REPO                         │
  │  Pipeline system, Bricklayer CLI, docs, system prompts, build tooling  │
  └────────────────────────────────────────────────────────────────────────┘
                │
                │  CLI installed globally (pip install -e .)
                │
                ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │  Your project repos               ← CLEAN product code                │
  │  Contains only: product code + bricklayer.yaml                        │
  │  bricklayer.yaml points back to OS tooling paths                      │
  └────────────────────────────────────────────────────────────────────────┘
                │
                │  Agents scaffolded via bricklayer agent new
                │  Deployed via bricklayer agent deploy
                │
                ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │  hermon1738/ai-agents             ← LIVE agents                       │
  │  One folder per deployed agent. Runs on Hetzner VPS via Docker.       │
  └────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference: Which Entry Point?

```
  Have a GitHub repo to evaluate?        → Entry A → Phase 1 (Repo Auditor)
  Have a raw idea, need to stress-test?  → Entry B → Phase 2 (Venture OS)
  Know what to build, skip strategy?     → Entry C → Phase 3 (Agent-OS)
  Have a spec, just need a build plan?   → Entry D → Phase 4 (Bricklayer Plan)

  Rule: start as early as you can afford to.
  Venture OS takes 10 minutes. Building the wrong thing takes days.
```
