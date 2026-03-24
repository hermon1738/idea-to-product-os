BRICK: Brick 8.6 - branching workflow

WHAT:
  New `bricklayer branch` command creates and checks out a correctly
  named branch. bricklayer build guards against working on main and
  exits 1. bricklayer build --verdict PASS auto-merges single-brick
  branches to main with --no-ff and deletes the branch. Feature
  branches stay open after PASS.

INPUT:
  cli/main.py, cli/commands/build.py, state.json, current git branch.

OUTPUT:
  bricklayer branch N name
    → creates and checks out brick/N-name
    → updates state.json current_branch field
  bricklayer branch --feature name
    → creates and checks out feature/name
    → updates state.json current_branch field
  bricklayer build on main
    → prints "You are on main. Create a branch first:
      bricklayer branch [N] [name]" and exits 1
  bricklayer build --verdict PASS on brick/N-name
    → merges to main with --no-ff, deletes branch
    → prints "Merged brick/N-name → main. Branch deleted."
  bricklayer build --verdict PASS on feature/name
    → does NOT merge, keeps branch open
    → prints "Feature branch open. Merge to main when all
      bricks in this feature pass."

GATE:
  RUNS — bricklayer branch creates correct branch name and checks
  it out. bricklayer build blocked on main exits 1. --verdict PASS
  on brick branch merges --no-ff and deletes. --verdict PASS on
  feature branch stays open. Existing branch → error, exit 1.
  No raw traceback on any git failure path.

BLOCKER:
  Every Phase 3 brick needs proper branching.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/branch.py
- cli/commands/build.py
- cli/main.py
- tests/test_branch.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) bricklayer branch N name
- Creates and checks out brick/N-name.
- Updates state.json current_branch.
- Exit 0.

2) bricklayer branch --feature name
- Creates and checks out feature/name.
- Updates state.json current_branch.
- Exit 0.

3) bricklayer build main guard
- On main → prints message with bricklayer branch usage, exits 1.
- No raw traceback.

4) bricklayer build on non-main branch
- Proceeds normally (no guard trigger).

5) --verdict PASS on brick/N-name
- Merges to main with --no-ff, deletes branch, prints merge message.
- State advanced by update_state.py --complete.
- Exit 0.

6) --verdict PASS on feature/name
- No merge, prints feature-branch message.
- State advanced by update_state.py --complete.
- Exit 0.

7) Branch already exists
- Clear error, exit 1, no overwrite.

8) Git operation failure
- Clear human-readable error, exit 1, no raw traceback, state
  not advanced.

TEST REQUIREMENTS:
- branch N name → brick/N-name created, checked out, state updated
- branch --feature name → feature/name created, checked out, state updated
- build on main → exit 1, correct message, no traceback
- build on non-main → no guard trigger
- --verdict PASS on brick branch → merge --no-ff, delete, state advance
- --verdict PASS on feature branch → no merge, feature message, state advance
- branch already exists → error, exit 1
- git failure → error, exit 1, no traceback, state not advanced
- CliRunner: branch command and main guard, assert exit codes

OUT OF SCOPE:
- Push to remote
- PR creation
- Any multi-brick feature branch merge strategy beyond "stay open"
