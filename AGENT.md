# AGENT.md — Idea-to-Product OS

Read this file at the start of every session before doing anything else.
This file works for Claude Code, Codex, Cursor, Gemini CLI, or any AI coding tool.

---

## What This Repo Is

A pipeline for turning ideas into deployed AI agent organizations.
You are the AI engineer. Tony is the human Co-CEO who approves, reviews, and decides.

The pipeline has 7 phases. The CLI (`bricklayer`) handles state, branching, and gates.
The system prompts in `system-prompts/` handle strategy, design, and planning.
You handle implementation.

---

## Your First Move — Every Session

```bash
bricklayer resume          # prints full context from last session
bricklayer status          # current project, brick, last action
bricklayer next            # exact next command to run
```

Read the output. That tells you where you are and what to do next.
Do not proceed until you have run these three commands.

---

## Brick Handoff Format

Brick handoffs work with any AI tool. When you receive a brick handoff:

- **Claude Code**: start the session message with `/run-brick`
- **Copilot CLI / Codex / Cursor / any AI**: read this file and
  follow Autonomous Build Mode below — same sequence, same rules

The sequence is identical regardless of which tool runs it.
The tool is the brain. The CLI enforces the gates.

---

## The Branching Model

All work happens on branches. Never commit directly to main.

```
main
 └── feature/<n>              (from main)
      └── phase/<N>-<n>       (from feature/*)
           └── brick/<N>-<n>  (from phase/*)
```

```bash
bricklayer branch --feature <n>    # creates feature/* from main
bricklayer branch --phase N <n>    # creates phase/* from feature/*
bricklayer branch N <n>            # creates brick/* from phase/*
```

Rules:
- Never branch a brick from main or a feature branch directly
- Never branch a phase from main or a brick branch directly
- The CLI enforces parent validation and exits 1 if wrong
- Each new phase branches from the updated feature branch
  so it includes all prior phase changes automatically

---

## Autonomous Build Mode

When you receive a brick handoff, execute the full build sequence
without pausing for approval at each step.

Run these steps in order. Stop at the first failure and report.
Do not skip ahead.

```
REPO_ROOT      = directory containing bricklayer.yaml
BRICKLAYER_DIR = REPO_ROOT/bricklayer/

Step 1 — FROM BRICKLAYER_DIR:
  python3 tools/print_brick_contract.py

Step 2 — FROM BRICKLAYER_DIR:
  python3 tools/verify_files_touched.py --snapshot-init

Step 3 — FROM REPO_ROOT:
  Implement — touch ONLY files in bricklayer/spec.md FILES section.
  Documentation and production-ready style are part of implementation.
  Write them as you go, not as an afterthought.

Step 4 — FROM REPO_ROOT:
  git add <every new untracked file listed in spec FILES>
  This must happen before make_skeptic_packet.py runs.
  New files not staged are invisible to the skeptic diff.
  Never skip this step.

Step 5 — FROM BRICKLAYER_DIR:
  python3 tools/verify_files_touched.py
  If FAIL — stop here. Report failure. Do not continue.

Step 6 — FROM BRICKLAYER_DIR:
  python3 tools/run_tests_and_capture.py
  If FAIL — stop here. Report failure. Do not continue.

Step 7 — FROM BRICKLAYER_DIR:
  python3 tools/make_skeptic_packet.py
```

After Step 7 — STOP. Post this exact report and wait for Tony's verdict:

```
SUMMARY:
- <3–6 bullets of what was implemented>

FILES_CHANGED:
- <one file per line, with status: new / modified>

TEST_RESULT:
- command: <exact command run>
- result: PASS | FAIL
- exit_code: <int>

SKEPTIC_READY: YES
```

⛔ NEVER write skeptic_verdict.md. Tony writes it. Always. No exception.
⛔ NEVER run bricklayer build --verdict PASS until Tony provides the verdict.

After Tony provides Verdict: PASS in skeptic_verdict.md:
```bash
bricklayer build --verdict PASS
# → commits all spec FILES, merges brick → phase,
#   deletes brick branch, runs update_state.py --complete
```

---

## Switching Tools Mid-Session

If you hit a context limit and need to switch tools:

```bash
bricklayer pause
# → writes HANDOFF.json with full session state
```

In the new tool, first message:
```bash
bricklayer resume
# → prints exactly where you are and what to do next
```

The state lives in files. Any tool picks up exactly where the last one stopped.

---

## The Build Sequence — Quick Reference

```bash
# Setup:
bricklayer branch N brick-name     # from correct phase branch

# Autonomous Build Mode (Steps 1–7):
bricklayer build --snapshot        # baseline snapshot
# implement + document             # write code + docs
# git add new files                # stage untracked
bricklayer build --verify          # scope check
bricklayer build --test            # run tests
bricklayer build --skeptic-packet  # package for review
# STOP — post report, wait for Tony's verdict

# After Tony's Verdict: PASS:
bricklayer build --verdict PASS    # close brick
```

---

## Docs Isolation — Important for New Projects

Each project controls where `bricklayer close-session` writes docs
via the `DOCS_PATH` env var in its own `.env` file.

```
idea-to-product-os project:
  DOCS_PATH=/path/to/ai-agents/docs    ← infrastructure log

reddit-monitor project:
  DOCS_PATH=/path/to/reddit-monitor/docs  ← project log

client-project:
  DOCS_PATH=/path/to/client-project/docs  ← client log
```

Each project's `.env` lives at its own root. When you `cd` into a
project and run `bricklayer close-session`, it reads that project's
`.env` and writes to that project's docs only.
No cross-contamination between projects.

---

## Phase System Prompts

Planning phases run in the Claude.ai browser project where Tony has
full context. For build sessions you only need stack-rules.md.

| Phase | File | Where to use |
|-------|------|-------------|
| 1 — Repo Audit | `system-prompts/repo-auditor.md` | Claude.ai project |
| 2 — Strategy | `system-prompts/venture-os.md` | Claude.ai project |
| 3 — Agent Design | `system-prompts/agent-os.md` | Claude.ai project |
| 4 — Build Plan | `system-prompts/plan-brain.md` | Claude.ai project |
| 6 — Sprint Review | `system-prompts/sprint-brain.md` | Claude.ai project |
| All phases | `system-prompts/stack-rules.md` | Every session |

---

## Engineering Standards

Read `system-prompts/stack-rules.md` before writing any code.
The skeptic checks every one of these. Violations = critical flaw.

- Type hints on every function signature — no exceptions
- No bare except — catch specific exceptions only
  except json.JSONDecodeError as exc:  ← correct
  except Exception:                    ← FAIL
- Atomic writes for critical files (write to .tmp then rename)
- Named UPPER_CASE constants for magic numbers/strings
- subprocess: capture_output=True, text=True, timeout=N, check=False
- Max 40 lines per function, max 3 nesting levels
- Errors to stderr — typer.echo(msg, err=True), never print()
- No mutable default arguments

---

## Documentation Standard

Every new or modified module must have:

Module header:
  WHY THIS EXISTS: one paragraph — what problem, what breaks without it
  DESIGN DECISIONS: bullet list — what was chosen, alternatives rejected

Every function/method:
  - What it does in plain English (not a restatement of the name)
  - Why it exists — what breaks without it
  - Args, returns, raises with exact conditions

Inline comments on every non-obvious line — explain WHY not WHAT:
  Bad:  # Loop through parents
  Good: # Walk up from cwd() so developers in subdirectories
        # still find bricklayer.yaml (caught in Brick 1 gate)

Undocumented code fails the gate. Documentation is not optional.

---

## Docs Gate

If a brick adds, removes, or changes a command, agent, or workflow:
- README.md must be in FILES and updated
- docs/pipeline.md must be updated if pipeline phases change
- DEBT.md must be updated if new debt is logged

The skeptic checks: do the docs reflect what was built?
Undocumented behavior = incomplete brick.

---

## Critical Rules

- ⛔ NEVER write skeptic_verdict.md — Tony writes it, always
- ⛔ NEVER run --verdict PASS before Tony provides the verdict file
- Never work on main, feature/*, or phase/* branches directly
- Never touch files not in bricklayer/spec.md FILES section
- Never proceed past a failing step — stop and report
- Step 4 (git add) is mandatory every brick — never skip it
- Skeptic must be a different AI than the builder
- Documentation is mandatory — undocumented code = FAIL
- Production-ready style is mandatory — violations = critical flaw

---

## Tool-Specific Notes

**Claude Code** — reads CLAUDE.md automatically. The `/run-brick`
skill activates Autonomous Build Mode. If unavailable, follow
Autonomous Build Mode above — identical sequence, same rules.

**Copilot CLI** — reads `AGENTS.md` (same as this file via
`.github/copilot-instructions.md`). Follow Autonomous Build Mode.
Use Autopilot mode (Shift+Tab) for autonomous execution.

**Codex** — reads `CODEX.md` which points here.
Follow Autonomous Build Mode. Runs autonomously by default.

**Cursor** — reads `.cursorrules` which points here.
Follow Autonomous Build Mode.

**Any other AI** — follow Autonomous Build Mode above.
The sequence is identical regardless of tool.

---

## Context Files

| File | What it contains |
|------|-----------------| 
| `context/pipeline-status.md` | Current state of every component |
| `context/decision-log.md` | Every decision made, append-only |
| `bricklayer/state.json` | Current brick, last action, loop count |
| `HANDOFF.json` | Last session pause state |
| `DEBT.md` | Known technical debt |