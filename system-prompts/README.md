# System Prompts

These files are AI-agnostic. Load them into any AI chat to activate
that pipeline phase. They work with Claude, GPT-4, Gemini, Codex,
or any capable AI — the rules stay the same regardless of tool.

## Files

| File | Phase | Load When |
|------|-------|-----------|
| `venture-os.md` | 2 — Strategy | You have a new idea to stress-test |
| `agent-os.md` | 3 — Agent Design | You have an Agent spec or Org Schema |
| `repo-auditor.md` | 1 — Repo Audit | You want to evaluate a GitHub repo |
| `plan-brain.md` | 4 — Build Planning | You have a PROJECT BRIEF to break into bricks |
| `sprint-brain.md` | 6 — Sprint Review | You finished a brick and need to review it |
| `stack-rules.md` | All | Load in every session — governs all builds |

## How to Use

### Option A — Claude Project (recommended)
1. Create a project in Claude
2. Upload all files from this folder + both files from `context/`
3. Set project instructions (see below)
4. Every new chat in the project has full context automatically

### Option B — Any AI chat
1. Open a new chat
2. Paste the relevant .md file as your first message
3. Also paste current `context/pipeline-status.md` and `context/decision-log.md`
4. State which phase you're entering

## Recommended Project Instructions

```
I am building the Idea-to-Product OS — a system for running 
AI-powered businesses. Read pipeline-status.md at the start of 
every session. Read decision-log.md for the last decision made. 
Apply stack-rules.md to every engineering plan. 
Never ask me to re-explain my stack.
```

## Skeptic Rule (important)

plan-brain.md and sprint-brain.md are used by the Builder AI.
The Skeptic review (bricklayer/skeptic-gate.md) must be run by
a DIFFERENT AI — never the same one that built the brick.

Builder: Claude Code or Codex
Skeptic: GPT-4 or Gemini

This prevents the AI from reviewing its own work.
