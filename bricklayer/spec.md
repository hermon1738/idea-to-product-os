BRICK: Brick 14 - three-level branching upgrade

WHAT:
  Upgrade branching from two levels (brick/feature) to three
  levels (feature → phase → brick). Add --phase flag to
  bricklayer branch. Add bricklayer close-phase and
  bricklayer close-feature commands. Update --verdict PASS
  merge routing to detect current branch level and merge to
  the correct parent.

INPUT:
  cli/commands/branch.py, cli/commands/build.py, cli/main.py,
  state.json

OUTPUT:
  BRANCH CREATION:
    bricklayer branch --feature reddit-monitor
      → creates feature/reddit-monitor from main
    bricklayer branch --phase 1 scaffold
      → creates phase/1-scaffold from current feature/* branch
    bricklayer branch 14 three-level-branching
      → creates brick/14-three-level-branching from current
        phase/* branch

  VERDICT PASS ROUTING:
    brick/* → merges to current_phase from state.json
    phase/* → merges to current_feature from state.json
    feature/* → merges to main

  NEW COMMANDS:
    bricklayer close-phase
    bricklayer close-feature

  STATE TRACKING:
    state.json gains current_feature and current_phase fields

GATE:
  RUNS — full three-level flow test

BLOCKER:
  Phase 4 multi-project commands assume this branching model.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/branch.py
- cli/commands/build.py
- cli/commands/close_phase.py
- cli/commands/close_feature.py
- cli/main.py
- tests/test_three_level_branch.py
- tests/test_branch.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Feature branch
- Created from main; error if not on main; state updated.

2) Phase branch
- Created from feature/*; error if not on feature/*; state updated.

3) Brick branch
- Created from phase/*; error if not on phase/*; state updated.

4) Verdict PASS routing
- brick/* → merge to current_phase; phase/* → merge to
  current_feature; feature/* → merge to main.

5) close-phase
- Merges phase/* → current_feature, deletes branch, updates state.

6) close-feature
- Merges feature/* → main, deletes branch, updates state.

7) Error cases
- Wrong parent → clear error, exit 1, no state change.
- Git failures → clear error, exit 1, no traceback.

8) State fields
- current_feature and current_phase track correctly through
  full three-level flow.

TEST REQUIREMENTS:
- Feature/phase/brick creation happy paths
- Wrong parent errors for all three levels
- Verdict PASS routing for all three levels
- close-phase and close-feature happy paths
- close-phase/close-feature wrong branch errors
- State field updates through full flow
- Git failures → exit 1, no traceback
- CliRunner integration

OUT OF SCOPE:
- Modifying state.py schema validation
- Changes to bricklayer.yaml structure
- Any Phase 4 commands
