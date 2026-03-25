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

The CLI enforces parent validation and exits 1 if you are on the wrong branch.

---

## The Build Sequence — Every Brick

```bash
# 1. Create the brick branch (from the correct phase branch)
bricklayer branch N brick-name

# 2. Update bricklayer/spec.md with the brick contract

# 3. Snapshot baseline
bricklayer build --snapshot

# 4. Implement — touch ONLY files listed in spec.md FILES section

# 5. Scope check
bricklayer build --verify

# 6. Run tests
bricklayer build --test

# 7. Package for review
bricklayer build --skeptic-packet

# 8. STOP — post the skeptic packet. Wait for Tony's verdict.
#    ⛔ DO NOT write skeptic_verdict.md yourself. Tony writes it.

# 9. After Tony confirms PASS:
bricklayer build --verdict PASS
# → auto-commits, merges brick → phase, deletes brick branch
```

---

## Phase System Prompts

| Phase | File | Load when |
|-------|------|-----------|
| 1 — Repo Audit | `system-prompts/repo-auditor.md` | Evaluating a GitHub repo |
| 2 — Strategy | `system-prompts/venture-os.md` | Stress-testing a new idea |
| 3 — Agent Design | `system-prompts/agent-os.md` | Designing agents from an Org Schema |
| 4 — Build Plan | `system-prompts/plan-brain.md` | Breaking a PROJECT BRIEF into bricks |
| 6 — Sprint Review | `system-prompts/sprint-brain.md` | Reviewing a completed brick |
| All phases | `system-prompts/stack-rules.md` | Engineering standards — always applies |

---

## Engineering Standards (short version)

Read `system-prompts/stack-rules.md` before writing any code.

- Type hints on every function signature
- No bare except — catch specific exceptions only
- Atomic writes for critical files (write to .tmp then rename)
- Named constants for magic numbers
- subprocess: always specify capture_output, text, timeout, check=False
- Max 40 lines per function, max 3 nesting levels
- Errors to stderr via typer.echo(msg, err=True)

---

## Documentation Standard

Every new or modified module must have:
- Module header: WHY THIS EXISTS + DESIGN DECISIONS
- Function docstrings: what, why, args, returns, raises
- Inline comments: explain WHY not WHAT on non-obvious lines

Undocumented code fails the gate.

---

## Critical Rules

- ⛔ Never write `skeptic_verdict.md`. Tony writes it. Always.
- Never work directly on `main`, `feature/*`, or `phase/*` branches
- Never touch files not listed in `bricklayer/spec.md` FILES section
- Never proceed past a failing step
- `git add` new untracked files before `bricklayer build --skeptic-packet`
- Skeptic must be a different AI than the builder

---

## Context Files

| File | What it contains |
|------|-----------------|
| `context/pipeline-status.md` | Current state of every component |
| `context/decision-log.md` | Every decision made, append-only |
| `bricklayer/state.json` | Current brick, last action, loop count |
| `HANDOFF.json` | Last session pause state |
| `DEBT.md` | Known technical debt |
