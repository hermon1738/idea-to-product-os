---
name: dangerously-skip-permissions meaning
description: What --dangerously-skip-permissions means in Tony's bricklayer workflow
type: feedback
---

When Tony passes `--dangerously-skip-permissions` at the start of a brick, it means: proceed autonomously through the full dev sequence (steps 1–6: print contract, snapshot, implement, verify, run tests, make skeptic packet) without pausing to ask permission at each tool call.

**Why:** Tony doesn't want Claude to stop and ask for approval at every Bash/Write/Edit tool call during routine brick execution.

**How to apply:** It does NOT bypass the skeptic gate. Tony still provides the verdict file himself. Stop at step 7 (SKEPTIC_READY) and wait for Tony to write `bricklayer/skeptic_verdict.md`. Only after `Verdict: PASS` is present should `update_state.py --complete` be run.
