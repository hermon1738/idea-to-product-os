BRICK: Brick 28 (revision) - Auto-push docs after close-session

WHAT:
  After bricklayer close-session writes docs to DOCS_PATH,
  automatically run git add + git commit + git push in
  the DOCS_PATH directory. GitHub becomes the single
  source of truth immediately after every session.

  Revision fixes three issues from the original Brick 28 attempt:
  1. _push_docs does not handle subprocess.TimeoutExpired or
     FileNotFoundError — both crash the CLI instead of warning.
  2. cli/state.py was regressed — FileNotFoundError was introduced
     instead of the Brick 26 auto-create (p.parent.mkdir).
  3. No tests for timeout and FileNotFoundError error paths.

INPUT:
  DOCS_PATH env var (path to local ai-agents clone)

OUTPUT:
  After writing docs:
  → cd DOCS_PATH
  → git add docs/
  → git commit -m "sync: session docs YYYY-MM-DD HH:MM"
  → git push
  → prints "Docs pushed to GitHub"

  DOCS_PATH not set → skip silently (existing behavior)
  DOCS_PATH set but not a git repo → warning, skip push
  git push fails → warning printed, exit 0
  git times out → warning printed, exit 0
  git not in PATH → warning printed, exit 0
    (docs are written locally — push failure is never fatal)

GATE:
  RUNS -- run close-session with --summary and DOCS_PATH
  set. Confirm docs written AND pushed to GitHub in one
  command. Check git log in ai-agents clone shows new
  commit.

BLOCKER:
  Nothing. But sync stays broken without this.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/close_session.py
- cli/state.py
- tests/test_close_session.py
- tests/test_state.py
- tests/test_next.py
- tests/test_status.py
- bricklayer/spec.md
- bricklayer/state.json

ACCEPTANCE CRITERIA:
1) DOCS_PATH set, valid git repo → docs written + pushed, exit 0
2) DOCS_PATH set, not a git repo → warning, exit 0 (not fatal)
3) git push fails (non-zero exit) → warning printed, exit 0
4) DOCS_PATH not set → skip entirely, exit 0
5) Commit message format: "sync: session docs YYYY-MM-DD HH:MM"
6) subprocess.TimeoutExpired → warning to stderr, exit 0, no crash
7) FileNotFoundError (git not in PATH) → warning to stderr, exit 0, no crash
8) cli/state.py contains p.parent.mkdir(parents=True, exist_ok=True)

TEST REQUIREMENTS:
- DOCS_PATH set, valid git repo → docs written + pushed, exit 0
- DOCS_PATH set, not a git repo → warning, exit 0 (not fatal)
- git push fails → warning printed, exit 0
- DOCS_PATH not set → skip entirely, exit 0
- subprocess.TimeoutExpired in push → warning to stderr, exit 0
- FileNotFoundError in push → warning to stderr, exit 0

OUT OF SCOPE:
- Any file outside the FILES list
- Changing the Groq provider/model selection logic
- Changing the output format of decision-log or pipeline-status
- Any other git operations beyond add/commit/push in DOCS_PATH
