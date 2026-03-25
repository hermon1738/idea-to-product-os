BRICK: Brick 18 - close-session docs sync

WHAT:
  Upgrade `bricklayer close-session` to write directly to
  decision-log.md and pipeline-status.md on the VPS after the Groq
  sprint review call. Replaces the manual !scribe Discord ritual for
  CLI sessions. Discord !scribe stays as fallback only.

INPUT:
  state.json, bricklayer/spec.md, system-prompts/sprint-brain.md,
  DOCS_PATH env var (path to ~/ai-agents/docs/ — defaults to None
  if not set, in which case skip docs write silently)

OUTPUT:
  Existing behavior (unchanged):
    → calls Groq with sprint-brain.md + current state
    → writes session-log.md locally
    → updates STATE.md
    → prints next session instruction

  New behavior (added):
    → after Groq call, also extracts structured data from sprint
      review output
    → appends one row to decision-log.md at DOCS_PATH
      Format: | date | component | decision | status | next_action |
    → rewrites pipeline-status.md at DOCS_PATH with updated state
    → prints "Docs synced to [DOCS_PATH]" on success
    → if DOCS_PATH not set → prints "DOCS_PATH not set,
      skipping docs sync" and continues (not a failure)
    → if DOCS_PATH set but path doesn't exist → prints warning
      and continues (not a failure — VPS may not be mounted)

GATE:
  RUNS — run bricklayer close-session with DOCS_PATH set to a temp
  directory. Confirm decision-log.md gets a new row and
  pipeline-status.md is rewritten. Run without DOCS_PATH — confirm
  it exits 0 with skip message.

BLOCKER:
  Nothing downstream.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/close_session.py
- tests/test_close_session.py
- bricklayer/spec.md
- DEBT.md

ACCEPTANCE CRITERIA:
1) DOCS_PATH set + valid dir → decision-log.md gets new row,
   pipeline-status.md rewritten, exit 0
2) DOCS_PATH not set → "DOCS_PATH not set, skipping docs sync"
   printed, exit 0
3) DOCS_PATH set but missing dir → warning printed, exit 0
4) decision-log.md missing → created with header + row appended
5) Groq call fails → docs sync does not run
6) GROQ_HEAVY_MODEL constant = "llama-3.3-70b-versatile" added

TEST REQUIREMENTS:
- Happy path: DOCS_PATH set, valid state → decision-log.md row +
  pipeline-status.md rewritten, exit 0
- DOCS_PATH not set → skip message, exit 0
- DOCS_PATH set but dir missing → warning, exit 0
- decision-log.md missing → created with header + row
- Groq call fails → docs sync does not run
- CliRunner integration: mock Groq + mock filesystem

OUT OF SCOPE:
- Changes to any other CLI command
- Changes to session-log.md or STATE.md behavior
- Discord integration
- Any Python file outside the FILES list
