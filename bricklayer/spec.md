BRICK: Brick 17 - Documentation full update

WHAT:
  Update every documentation file to reflect the current state of the system.
  Create AGENT.md, CLAUDE.md, templates/bricklayer.yaml. Rewrite README.md,
  docs/getting-started.md, docs/architecture.md, bricklayer/Readme.md,
  context/pipeline-status.md to match current system state.

INPUT:
  All existing documentation files; current CLI state (Bricks 1–16 done)

OUTPUT:
  Root README covers full OS. AGENT.md and CLAUDE.md exist as session entry
  points. templates/bricklayer.yaml exists as new-project starting point.
  All rewritten docs reflect Phase 3 complete, 408 tests, three-level branching.

GATE:
  OUTPUTS — manual gate:
  - bricklayer --help still works
  - No broken markdown links
  - Root README covers full OS, not just CLI
  - AGENT.md and CLAUDE.md exist and are usable as session entry points
  - templates/bricklayer.yaml exists
  - context/pipeline-status.md shows 2026-03-24 current state
  - bricklayer/Readme.md has no pre-CLI content

BLOCKER:
  Nothing.

WAVE:
  SEQUENTIAL

FILES:
- README.md
- AGENT.md
- CLAUDE.md
- templates/bricklayer.yaml
- docs/getting-started.md
- docs/architecture.md
- bricklayer/Readme.md
- context/pipeline-status.md
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) README.md covers full OS (not just CLI)
2) AGENT.md exists and is tool-agnostic
3) CLAUDE.md exists with Claude Code specific rules
4) templates/bricklayer.yaml exists with correct placeholder paths
5) docs/getting-started.md has CLI install + new project setup
6) docs/architecture.md has three-level branching + live agents
7) bricklayer/Readme.md has no pre-CLI content
8) context/pipeline-status.md shows current state dated 2026-03-24
9) No broken links in any file

TEST REQUIREMENTS:
- No automated tests.
- Gate: 408 tests still passing (docs changes touch no Python).

OUT OF SCOPE:
- Any Python code changes
- New CLI features
- Test file modifications
