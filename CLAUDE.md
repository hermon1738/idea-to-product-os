# CLAUDE.md — Claude Code Session Entry Point

Claude Code reads this file automatically at session start.

---

## Step 1 — Read AGENT.md first

```bash
cat AGENT.md
```

AGENT.md is the AI-tool agnostic entry point for this repo.
It contains your build sequence, branching rules, engineering standards,
and documentation requirements. Read it before doing anything else.

---

## Step 2 — Orient

```bash
bricklayer resume
bricklayer status
bricklayer next
```

---

## Step 3 — Use /run-brick for builds

The `/run-brick` skill is installed at `~/.claude/skills/run-brick.md`.
Start any brick message with `/run-brick` to run the full 7-step
build sequence autonomously.

---

## Claude Code Specific Rules

**⛔ NEVER write `bricklayer/skeptic_verdict.md`.**
This has been violated in past sessions. It applies unconditionally.
No flag, no message, no permission overrides it. Tony writes the verdict. Always.

**`bricklayer build --verdict PASS` closes a brick.**
Not `update_state.py --complete` directly. Run it only after Tony has
written `Verdict: PASS` in skeptic_verdict.md.

**Launch with dangerously-skip-permissions for builds:**
```bash
claude --dangerously-skip-permissions
```
Allows the build sequence to run without per-tool approval prompts.
Does not change the skeptic_verdict.md rule.

---

## Quick Reference

```bash
bricklayer status                    # current position
bricklayer next                      # next command to run
bricklayer branch --feature <n>      # new feature (from main)
bricklayer branch --phase N <n>      # new phase (from feature/*)
bricklayer branch N <n>              # new brick (from phase/*)
bricklayer build --snapshot          # baseline snapshot
bricklayer build --verify            # scope check
bricklayer build --test              # run tests
bricklayer build --skeptic-packet    # package for review
bricklayer build --verdict PASS      # close brick (after human verdict)
bricklayer close-phase               # merge phase → feature
bricklayer close-feature             # merge feature → main
bricklayer pause / resume            # session save / restore
bricklayer commit -m "msg"           # mid-brick checkpoint
bricklayer close-session             # sprint review + log
```
