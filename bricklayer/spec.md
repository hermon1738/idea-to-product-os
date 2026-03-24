BRICK: Brick 8 - bricklayer build --verdict PASS|FAIL

WHAT:
  --verdict PASS|FAIL closes or fails the current brick.
  PASS: writes bricklayer/skeptic_verdict.md with "Verdict: PASS",
  then runs update_state.py --complete.
  FAIL: increments loop_count in state.json; if loop_count reaches
  or already equals 3, prints RESCOPE and exits 1 without advancing.
  Guard: refuses to run if next_action != skeptic_packet_ready.

INPUT:
  state.json (loop_count, next_action), update_state.py (state key
  in bricklayer.yaml). Verdict value is PASS or FAIL.

OUTPUT:
  PASS: skeptic_verdict.md written, update_state.py --complete runs,
  state advances. Exit 0.
  FAIL (loop_count < 3): loop_count incremented, blocker printed, exit 1.
  FAIL (loop_count reaches/is >= 3): RESCOPE printed, exit 1.
  Invalid value: error printed, exit 1.
  Wrong next_action: guard error printed, exit 1.

GATE:
  RUNS — PASS writes skeptic_verdict.md and runs update_state tool.
  FAIL increments loop_count correctly. loop_count=3 triggers RESCOPE
  with no state advance. No raw traceback on any error path.

BLOCKER:
  Nothing downstream in MVP. Completes the build loop.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/build.py
- cli/main.py
- tests/test_build_verdict.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) PASS path
- next_action=skeptic_packet_ready → skeptic_verdict.md written with
  "Verdict: PASS", update_state.py --complete invoked, exit 0.

2) FAIL path — normal
- next_action=skeptic_packet_ready, loop_count < 2 → loop_count
  incremented by 1, blocker message printed, exit 1.

3) FAIL path — RESCOPE triggered (reaches 3)
- loop_count=2 → increments to 3, RESCOPE printed, exit 1.

4) FAIL path — already at loop_count=3
- loop_count=3 → hard stop: RESCOPE printed, exit 1, state unchanged.

5) Guard
- next_action != skeptic_packet_ready → guard error, exit 1,
  nothing written, state not modified.

6) Missing loop_count key
- loop_count absent from state.json → treated as 0, no traceback.

7) Invalid verdict value
- --verdict with value other than PASS or FAIL → error, exit 1.

8) CliRunner integration
- --verdict PASS: exit 0, skeptic_verdict.md written.
- --verdict FAIL: exit 1, loop_count incremented.

TEST REQUIREMENTS:
- PASS: verdict.md written with "Verdict: PASS", run_tool called, exit 0
- FAIL loop_count=1 → increments to 2, exit 1, next_action unchanged
- FAIL loop_count=2 → increments to 3, RESCOPE in output, exit 1
- FAIL loop_count=3 → RESCOPE, exit 1, state unchanged
- Guard: wrong next_action → error, exit 1, no writes
- Missing loop_count key → fallback to 0, exit 1, no traceback
- Invalid verdict value → error, exit 1
- CliRunner: PASS → exit 0, verdict.md exists
- CliRunner: FAIL → exit 1, loop_count incremented

OUT OF SCOPE:
- Writing handover.md (that is update_state.py's responsibility)
- Any other --complete behavior beyond invoking the tool
- All prior v2 debt items
