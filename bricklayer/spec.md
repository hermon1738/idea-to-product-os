BRICK: Brick 8.5 - git fixes (auto-stage + auto-commit on verdict)

WHAT:
  Two permanent fixes to the git workflow:
  1. make_skeptic_packet.py reads spec.md FILES section and runs
     git add on every listed file before building the packet.
     New files are never invisible to the skeptic diff.
  2. bricklayer build --verdict PASS runs git commit on all files
     in spec.md FILES after update_state.py --complete succeeds.
     Prior brick files never pollute the next brick's verify step.

INPUT:
  bricklayer/tools/make_skeptic_packet.py (modified — auto git add),
  cli/commands/build.py (modified — auto git commit on PASS),
  bricklayer/spec.md FILES section (source of truth for current brick).

OUTPUT:
  make_skeptic_packet.py auto-stages all spec FILES before building
  the packet. bricklayer build --verdict PASS auto-commits all spec
  FILES using commit format: "feat(brick-N): [brick name]" with
  Co-Authored-By trailer. Exit 0 on success; exit 1 if commit fails
  with clear error, state not advanced.

GATE:
  RUNS — make_skeptic_packet.py stages all spec FILES before diff.
  --verdict PASS creates a git commit containing all spec FILES.
  Commit message matches stack-rules format. State advances only
  after commit succeeds. No raw traceback on any error path.

BLOCKER:
  Every Phase 3 brick will hit both issues without this fix.

WAVE:
  SEQUENTIAL

FILES:
- bricklayer/tools/make_skeptic_packet.py
- cli/commands/build.py
- tests/test_git_fixes.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Auto-stage (make_skeptic_packet.py)
- Runs git add on every file listed in spec.md FILES before building
  the packet. New/untracked files listed in FILES are staged.
- Files NOT in spec.md FILES are NOT staged by the tool.

2) Auto-commit on PASS verdict
- --verdict PASS: after update_state.py --complete succeeds, reads
  spec.md FILES, runs git commit with message
  "feat(brick-N): [brick name]" and Co-Authored-By trailer.
- git log shows a new commit containing all spec FILES.
- state.json advances (next_action updated by update_state.py).

3) Auto-commit failure handling
- If git commit exits non-zero (e.g. nothing to commit), --verdict
  PASS prints clear error and exits 1. State is not advanced.

4) CliRunner integration
- --verdict PASS via CliRunner: commit created, state advanced.

TEST REQUIREMENTS:
- auto-stage: new file in spec FILES is staged by make_skeptic_packet.py
- auto-stage: file not in spec FILES is not staged
- auto-commit PASS: git log shows new commit with spec FILES
- auto-commit PASS: state.json next_action advances
- auto-commit failure: git commit failure → exit 1, state not advanced
- CliRunner: --verdict PASS → commit created, state advanced

OUT OF SCOPE:
- Changing FAIL path behavior
- Changing loop_count / RESCOPE logic
- Any behavior not listed above
