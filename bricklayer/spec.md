BRICK: Brick 26 - null state fields + missing state.json

WHAT:
  Two related state.json hardening fixes:
  1. close-phase and close-feature crash with ValueError if current_brick
     is null in state.json. The merge succeeds but the state update fails.
     Fix: treat null as empty string when writing state after a merge.
  2. Every bricklayer command fails with "state.json not found" on a
     fresh repo or new project. Fix: when state.json is missing,
     auto-create it with safe defaults instead of exiting 1.

INPUT:
  cli/commands/close_phase.py, cli/commands/close_feature.py,
  cli/state.py, cli/commands/ (all commands that read state)

OUTPUT:
  Fix 1: close-phase and close-feature coerce null current_brick to ""
  before state_write — no ValueError, merge stays consistent.
  Fix 2: state.load() auto-creates state.json with defaults when missing,
  prints warning to stderr, returns valid dict.

GATE:
  RUNS — in /tmp/test-fresh-repo:
  1. git init + copy bricklayer.yaml
  2. bricklayer status -> works, prints defaults, no error
  3. bricklayer branch --feature test -> works
  4. Full branch -> close-phase -> close-feature flow with null
     current_brick in state -> no crash, merges succeed, state
     updates correctly

BLOCKER:
  Real sessions on fresh project repos fail without this.

WAVE:
  SEQUENTIAL

FILES:
- cli/state.py
- cli/commands/close_phase.py
- cli/commands/close_feature.py
- tests/test_state.py
- tests/test_close_phase_fix.py
- DEBT.md
- bricklayer/spec.md
- bricklayer/state.json

ACCEPTANCE CRITERIA:
1) state.load() missing file -> auto-creates state.json with safe defaults
2) auto-created state has project = directory name of repo root
3) auto-created state passes schema validation
4) auto-create prints warning to stderr: "state.json not found — created with defaults at <path>"
5) close-phase with null current_brick -> merge succeeds, state updated, no ValueError, exit 0
6) close-feature with null current_brick -> merge succeeds, state updated, no ValueError, exit 0
7) close-phase with valid current_brick -> unchanged behavior
8) Full fresh-repo flow: status -> branch -> close-phase -> close-feature all work without pre-existing state.json

TEST REQUIREMENTS:
- state.load() missing file -> auto-creates with correct defaults, prints warning to stderr
- auto-created state has project = directory name of repo root
- auto-created state passes schema validation
- close-phase with null current_brick -> merge succeeds, state updated, no ValueError, exit 0
- close-feature with null current_brick -> merge succeeds, state updated, no ValueError, exit 0
- close-phase with valid current_brick -> unchanged behavior
- full fresh-repo flow: status -> branch -> close-phase -> close-feature all succeed

OUT OF SCOPE:
- Any file outside the FILES list
- Changes to other commands beyond state.load() call chain
- Schema migration or backfill of existing state.json files
