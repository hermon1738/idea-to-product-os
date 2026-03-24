BRICK: Brick 13 - README + documentation update

WHAT:
  Update README.md to accurately reflect what exists after
  Phases 1-3. A developer who has never seen this repo should
  be able to clone, install, and run bricklayer status in
  under 5 minutes by following the README alone.

INPUT:
  All shipped code (Bricks 1-12), bricklayer.yaml, existing
  README.md

OUTPUT:
  README.md covering:
  1. What bricklayer-cli is — one paragraph, no hype
  2. Install steps: git clone → pip install -e . → bricklayer --help
  3. bricklayer.yaml setup — what it is, minimal working example
  4. Every working command with one-line description and example output
  5. The build loop — how a full brick sequence works end to end
  6. Known limitations (v2 debt) — honest list of what doesn't work yet

GATE:
  OUTPUTS — read the README cold as if you have never seen this
  repo. Confirm: install steps work from scratch, every command
  listed exists and runs, no references to features that don't
  exist yet, no placeholder text remaining.

BLOCKER:
  Nothing. Ships before Phase 4 adds more commands to document.

WAVE:
  PARALLEL

FILES:
- README.md
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Install section
- git clone + pip install -e . + bricklayer --help steps shown.
2) Commands section
- All 8 working commands documented with description + example.
3) Build loop section
- 8-step sequence shown end to end.
4) v2 debt section
- Honest limitations listed; no hype language.
5) No placeholder text
- Zero instances of TODO, TBD, or template boilerplate.
6) No phantom features
- No references to commands or flags that don't yet exist.

TEST REQUIREMENTS:
- No automated tests for this brick.
- Gate: manual read-through confirming all criteria above.

OUT OF SCOPE:
- API reference generation
- Changelog / release notes
- Any code changes
