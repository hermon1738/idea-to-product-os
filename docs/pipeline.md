# Pipeline — Idea-to-Product OS

The pipeline has 7 phases and 4 entry points.
Not every idea starts at Phase 1.

---

## Entry Points

| Entry | When to Use | Start At |
|-------|-------------|----------|
| A | You have a GitHub repo to evaluate | Phase 1 |
| B | You have an original idea in your head | Phase 2 |
| C | You know what to build, no strategy needed | Phase 3 |
| D | You have a spec, just need a build plan | Phase 4 |

**Rule: start as early as you can afford to.**
Venture OS is 10 minutes. Building the wrong thing is days.

---

## Phase 1 — Repo Auditor

**Tool:** `system-prompts/repo-auditor.md`
**Load into:** Any AI chat
**Trigger:** Drop a GitHub URL

Evaluates a GitHub repo and outputs either an Agent-OS spec
or a Bricklayer project brief. Runs automatically — no setup.

Output: `Agent spec:` prompt or `PROJECT BRIEF` block

---

## Phase 2 — Venture OS

**Tool:** `system-prompts/venture-os.md`
**Load into:** Any AI chat
**Trigger:** Describe your idea in plain language

Co-CEO strategy session. Stress-tests the idea across departments
(Product, Engineering, Revenue, Marketing, Ops, AI Agents).
Makes the Build / Adapt / Ignore call.

Output: Org Schema with departments, agents needed, dependencies,
pipeline entry, and next action.

---

## Phase 3 — Agent-OS

**Tool:** `system-prompts/agent-os.md`
**Load into:** Any AI chat
**Trigger:** `Agent spec: [description]` or paste an Org Schema

Designs the full agent hierarchy. Director vs Worker agents,
triggers, inputs, outputs, tools, failure modes.

Output: Agent blueprint + Bricklayer PROJECT BRIEF per agent

---

## Phase 4 — Bricklayer / plan-brain

**Tool:** `bricklayer/` directory
**Builder:** Claude Code, Codex, GPT-4, or any AI
**Trigger:** Paste a PROJECT BRIEF

Breaks work into bricks — small, testable, sequenced units.
Each brick has a FILES scope, Acceptance Criteria, Test Requirements,
and Out of Scope. One active brick at a time.

Output: spec.md with first brick defined and ready to build

---

## Phase 5 — Implement + Skeptic Review

**Builder:** Any AI (Claude Code, Codex, GPT-4)
**Skeptic:** DIFFERENT AI — never the same one that built it
**Tools:** `bricklayer/tools/` + `bricklayer/skeptic-gate.md`

Builder implements the brick following `PROMPTS/BUILDER_PROMPT.md`.
Runs verify tools, test capture, and generates skeptic_packet.

Skeptic receives the packet and runs `skeptic-gate.md` protocol:
- Flaw Hunt
- Blind Spot Hunt
- Long-Term Scaling Check
- Failure-First Challenge

Skeptic writes `skeptic_verdict.md`. Must contain `Verdict: PASS`.
If FAIL: loop_count increments. At 3: rescope the brick.

**Critical rule: the AI that builds cannot review its own work.**

---

## Phase 6 — Sprint Review

**Tool:** `system-prompts/sprint-brain.md` (or `bricklayer/WORKFLOW.md`)
**Load into:** Any AI chat

Reviews what shipped. Closes the brick. Outputs next brick.
Produces a `!scribe` command for Session Scribe.

---

## Phase 7 — Session Scribe

**Tool:** Session Scribe Discord bot (`!scribe` command)
**Trigger:** End of every session

Paste a session summary. Groq extracts decisions and updates:
- `decision-log.md` — append-only session history
- `pipeline-status.md` — full pipeline state rewritten

After `!scribe` runs, copy both files back into your AI project
context so the next session starts with full context.

---

## The Full Loop

```
Session start  → read pipeline-status.md (30 seconds to orient)
               → read decision-log.md (last session's next action)
               → tell AI which phase you're entering

During session → work through the phase
               → produce the phase output

Session end    → !scribe in Discord
               → sync docs back to AI project context
               → next session starts oriented
```
