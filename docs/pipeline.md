# Pipeline Reference — Idea-to-Product OS

This document explains each stage of the pipeline in depth: what it is, what triggers it,
what it produces, what it feeds next, and the rules that govern it.

Read this when you want to understand **why** the pipeline is structured the way it is,
not just how to run it. For the quick how-to, see `README.md`.

---

## 1. Philosophy

### Plan before you build

The most expensive mistake in software is building the wrong thing correctly.
Every hour spent planning at the start saves 10 hours of rework mid-build.
This pipeline front-loads all architectural and strategic decisions before a single
line of code is written. By the time a builder AI touches the codebase, the architecture
is already approved, the phases are defined, and every brick knows exactly which files
it is allowed to touch.

### Why gates matter

Without gates, work drifts. A builder AI that can redefine scope mid-brick will
scope-creep every session. A builder AI that reviews its own output will rationalize
its own mistakes. Gates enforce discipline that no single participant — human or AI —
will enforce on their own.

This pipeline has two types of gates:

**Approval gates** — a human (the Co-CEO) explicitly approves a document or decision
before the pipeline advances. These exist at the end of Venture OS (phase confirmation)
and twice during arch-brain (options approval, final architecture approval).

**Skeptic gates** — an AI different from the builder reviews the completed brick using
a structured checklist. The builder cannot write the verdict. The verdict must say
`Verdict: PASS` before the brick closes. At 3 failed loops, the brick is rescoped.

### Why one brick at a time

Context fragmentation is the primary failure mode for AI-assisted builds. When a builder
AI holds too many open threads, it loses track of scope, skips edge cases, and introduces
regressions. One brick at a time with a FILES scope list enforces focus. The skeptic gate
catches what slips through.

---

## 2. Stage: Venture OS

**File:** `system-prompts/venture-os.md`
**Trigger:** You have a software idea — raw, half-formed, or already shaped.
**Runs in:** Any AI chat (Claude, GPT-4, Gemini, etc.)

### What it does

Venture OS is a structured Co-CEO strategy session. It stress-tests the idea across
multiple dimensions: product fit, engineering feasibility, revenue model, marketing angle,
operational requirements, and AI layer necessity. It makes an explicit **Build / Adapt / Ignore**
call before any architecture work begins.

It then produces an **Org Schema** — a structured description of the product's layers,
the phases required to build it, and confirmation of which pipeline stages apply.

### What triggers the next stage

The Co-CEO reviews the Org Schema and explicitly confirms the phases. This is not automatic.
The human reads it, challenges it if needed, and gives a go-ahead. Only then does the
pipeline advance to arch-brain.

### What it produces

- Org Schema with: product type, architecture layers, phases, and pipeline entry point
- Phase confirmation (Co-CEO approved)

### What it feeds

arch-brain receives the confirmed Org Schema and uses it as input for the architecture session.

### Rules

- Never skip Venture OS for a new idea. 10 minutes of strategy prevents days of rework.
- If the idea is already fully formed and the Co-CEO knows exactly what to build,
  entry can start at arch-brain directly — but the Org Schema still needs to exist.

---

## 3. Stage: arch-brain

**File:** `system-prompts/arch-brain.md`
**Trigger:** Venture OS phase confirmation is complete.
**Runs in:** Any AI chat

### What it does

arch-brain runs a structured architecture session. It takes the confirmed Org Schema
and produces `docs/ARCHITECTURE.md` — the single source of truth for the entire build.

The session has two approval gates:

1. **Options gate** — arch-brain presents multiple architecture options with trade-offs.
   The Co-CEO selects one. No document is produced until this gate passes.

2. **Final approval gate** — arch-brain drafts `ARCHITECTURE.md`. The Co-CEO reviews
   and approves it. Once approved, this document is locked.

### What it produces

`docs/ARCHITECTURE.md` — a structured document containing:
- Product type and tech stack
- Layer diagram (what each layer is and how they connect)
- Data flow
- Key decisions and the reasoning behind them
- What is explicitly out of scope

### What it feeds

- plan-brain loads `ARCHITECTURE.md` when generating the build plan
- Every brick handoff loads `ARCHITECTURE.md` to stay aligned
- Agent-OS (if triggered) receives `ARCHITECTURE.md` as its input

### Rules

- `ARCHITECTURE.md` is the source of truth. If a brick conflicts with it, the brick
  is wrong — not the architecture.
- Changes to `ARCHITECTURE.md` mid-build require the Revision Protocol (see section 9).
- arch-brain must appear in every pipeline run, even if the architecture seems obvious.
  The approval gates exist to catch assumptions before they become regressions.

---

## 4. Stage: Agent-OS

**File:** `system-prompts/agent-os.md`
**Trigger:** `ARCHITECTURE.md` is approved AND the architecture has an AI layer.
**Runs in:** Any AI chat

### What it does

Agent-OS designs the AI components of the product. It takes the approved architecture
and produces a full agent blueprint: agent hierarchy, triggers, inputs, outputs, tools,
memory requirements, and failure modes.

It also outputs a Bricklayer PROJECT BRIEF for each agent component — structured build
instructions ready to hand to plan-brain.

### What it produces

- Agent blueprint (hierarchy, triggers, tools, failure modes)
- PROJECT BRIEF per agent component

### What it feeds

plan-brain receives the PROJECT BRIEFs and uses them to generate brick sequences.

### Rules

**Agent-OS is conditional.** It only runs when the architecture has an AI layer.
For web apps, CLI tools, or backend systems without AI components, this stage is skipped entirely.

The Framework Decision Gate (in `agent-os.md` §4.5) determines whether each agent
should be a RAW PYTHON script or a NANOBOT:
- **RAW PYTHON:** single-purpose, no memory, no cron, no OpenClaw, Discord/webhook trigger (ALL must be true)
- **NANOBOT:** memory, cron, 2+ agent org, OpenClaw delegation, or tool-calling (ANY triggers it)
- **DEFER:** surface ambiguity to the Co-CEO — never default to a path

---

## 5. Stage: plan-brain

**File:** `system-prompts/plan-brain.md`
**Trigger:** `ARCHITECTURE.md` is approved. PROJECT BRIEFs exist (from Agent-OS if applicable).
**Runs in:** Any AI chat

### What it does

plan-brain receives the approved architecture and any PROJECT BRIEFs, then breaks the
entire build into phases and bricks. Every brick is a small, testable, sequenced unit
of work.

Each brick defines:
- **FILES** — the exact list of files the builder is allowed to touch
- **Acceptance Criteria** — what done looks like
- **Test Requirements** — what tests must pass
- **Out of Scope** — explicit list of what this brick does NOT do

One brick is active at a time. plan-brain hands off Brick 1 to the builder.

### What it produces

- `bricklayer/spec.md` with Brick 1 defined
- Phase and brick sequence for the full build

### What it feeds

The Bricklayer CLI + Claude Code take `spec.md` and execute the build loop.

### Rules

- Every brick must have a FILES list. A brick without a FILES list is not a valid brick.
- Every handoff loads `ARCHITECTURE.md`. Bricks that contradict the architecture are invalid.
- plan-brain does not write code. It only plans.

---

## 6. Stage: Bricklayer CLI / Claude Code

**Tools:** `bricklayer/` directory, `bricklayer` CLI, `bricklayer/tools/`
**Trigger:** `spec.md` exists with Brick 1 defined.
**Builder:** Claude Code (or any builder AI)
**Skeptic:** A different AI — never the same one that built it

### What it does

The builder AI implements the brick exactly as defined in `spec.md`. It is allowed to
touch only the FILES listed in the spec. The build loop runs as follows:

1. `bricklayer build --snapshot` — baseline snapshot of current state
2. Implement — touch only FILES listed in spec.md
3. `bricklayer build --verify` — scope check (confirms no files outside the list were touched)
4. `bricklayer build --test` — run the test suite, capture results
5. `bricklayer build --skeptic-packet` — package all evidence for skeptic review
6. **STOP** — post packet to skeptic. Wait for verdict.
7. After `Verdict: PASS` in `skeptic_verdict.md`:
   `bricklayer build --verdict PASS` — close the brick, advance state

### Branch model

```
main
 └── feature/<name>
      └── phase/<name>
           └── brick/<name>
```

Each brick lives on its own branch. Merging flows upward: brick → phase → feature → main.

### Loop stop rule

If a brick fails skeptic review 3 times (`loop_count >= 3`), stop building.
Rewrite `spec.md` — split the brick into smaller units, tighten criteria.
Append a RESCOPE NOTE to handover.md. Do not attempt a fourth loop on the same scope.

### Rules

- The builder cannot write `skeptic_verdict.md`. Ever. This rule has no exceptions.
- `bricklayer build --verdict PASS` is the only valid way to close a brick.
  Do not run `update_state.py --complete` directly.
- `bricklayer --dangerously-skip-permissions` is available for autonomous build sessions.
  It does not change the skeptic_verdict.md rule.

---

## 7. Stage: sprint-brain

**File:** `system-prompts/sprint-brain.md`
**Trigger:** End of every build session (after one or more bricks close).
**Runs in:** Any AI chat

### What it does

sprint-brain reviews what shipped in the session, closes out the brick, and produces
the next action. It generates a `!scribe` command for the Session Scribe agent, which
updates `decision-log.md` and `pipeline-status.md`.

After `!scribe` runs, copy both context files back into the AI project context so the
next session starts oriented.

### What it produces

- Session summary
- Next brick brief
- `!scribe` command for Session Scribe
- Updated `decision-log.md` and `pipeline-status.md` (via Session Scribe)

### Rules

- sprint-brain runs after every session, not just at major milestones.
- The updated context files must be synced back before the next session starts.
  A session that starts without reading `pipeline-status.md` is starting blind.

---

## 8. The Architecture Document

`docs/ARCHITECTURE.md` is the most important artifact in the pipeline.

### What it contains

- Product type (AGENT, WEB_APP, SYSTEM, CLI_TOOL)
- Tech stack (language, framework, database, infrastructure)
- Layer diagram — every layer of the system, how they connect, and what each does
- Data flow — how data moves through the system from input to output
- Key decisions — the choices made and the reasoning behind them
- Out of scope — what this build explicitly does not include

### Why it matters

Every downstream stage depends on it. plan-brain reads it to generate valid bricks.
Every brick handoff loads it to stay in scope. The skeptic checks bricks against it.
When there is a conflict between a brick and the architecture, the brick is wrong.

### When it is written

arch-brain produces it after the Co-CEO approves the architecture options. It is
locked after the final approval gate. No code is written until this document exists
and is approved.

---

## 9. Revision Protocol

Architecture changes mid-build are expensive. They invalidate bricks, break scope
assumptions, and require rework. This protocol governs how changes happen without
causing chaos.

### When revision is warranted

- A new external constraint appears that the architecture did not account for
- A completed brick reveals a fundamental flaw in the layer design
- The Co-CEO makes a strategic decision that changes the product shape

### How to revise

1. **Stop the current brick.** Do not continue building under an architecture that
   no longer applies.

2. **Document the change request.** Write a clear description of what changed and why.
   Append to `context/decision-log.md`.

3. **Re-run arch-brain** with the change request. Treat it as a new architecture session,
   but scoped to the changed layer. Both approval gates apply.

4. **Update `ARCHITECTURE.md`.** The revised document becomes the new source of truth.

5. **Audit affected bricks.** Review any in-progress bricks against the new architecture.
   Rewrite specs that are now invalid.

6. **Resume building.** The pipeline continues from the updated spec.

### What not to do

Do not patch the architecture informally. Do not tell a builder AI "just ignore the
architecture for this brick." Do not let a brick contradict `ARCHITECTURE.md` and call
it a "temporary exception." These shortcuts always compound into regressions.
