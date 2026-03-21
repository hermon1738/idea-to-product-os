# INTAKE — Project Brief Standard Operating Procedure

## Rule

A PROJECT BRIEF is not an execution order.
It is an input to the planning process.

No brief gets executed directly. No exceptions.

---

## Mandatory Sequence

When a PROJECT BRIEF is received:

1. **Load `PROMPTS/BUILDER_PROMPT.md` first.**
   Do not read the brief. Do not touch any files. Load the builder prompt first.

2. **Run the brief through plan-brain decomposition.**
   Feed the brief into `plan-brain.md` (Bricklayer Blueprint).
   Output: a sequenced set of bricks with gates, risks, and a FIRST BRICK.

3. **Write the first brick to `spec.md`.**
   One brick at a time. `spec.md` holds only the active brick.

4. **Execute per `WORKFLOW.md`.**
   Follow the exact command sequence. No shortcuts. No combined bricks.
   Every brick passes its gate before the next begins.

---

## What Skipping This Looks Like

- Brief → direct implementation → no spec → no gate → no skeptic review
- This is a pipeline violation. Stop and restart from step 1.

---

## Input Sources

A PROJECT BRIEF may arrive from:
- `system-prompts/agent-os.md` (Agent-OS Bricklayer Handoff)
- `system-prompts/plan-brain.md` (plan-brain FIRST BRICK output)
- Direct user input in session

Source does not change the procedure. All briefs enter at step 1.
