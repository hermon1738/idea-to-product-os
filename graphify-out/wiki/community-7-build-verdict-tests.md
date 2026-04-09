# Build Verdict Tests

> Community 7 · 58 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_build_verdict.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | code |
| Tests for Brick 8 — bricklayer build --verdict PASS|FAIL. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| PASS returns 1 when update_state tool exits non-zero. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| FAIL increments loop_count by 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| FAIL does not advance next_action. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| FAIL always returns 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| FAIL below threshold prints normal blocker message. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| loop_count=2 increments to 3 on FAIL. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| loop_count reaches 3 → RESCOPE message printed. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| loop_count reaches 3 → still exits 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| loop_count=3 already → hard stop, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| loop_count=3 hard stop → state.json not modified. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| loop_count=3 hard stop → RESCOPE printed. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| loop_count=3 hard stop → no raw traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| Guard fires for any next_action other than skeptic_packet_ready. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| Guard fires → skeptic_verdict.md is NOT written. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| Guard fires → no raw traceback in any output. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| Missing loop_count key treated as 0; FAIL increments to 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| Missing loop_count key → no raw traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| Invalid verdict string (not PASS or FAIL) → exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| Invalid verdict string → no raw traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| CliRunner: `bricklayer build --verdict PASS` exits 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| CliRunner: `bricklayer build --verdict PASS` writes skeptic_verdict.md. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| CliRunner: `bricklayer build --verdict FAIL` exits 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| CliRunner: `bricklayer build --verdict FAIL` increments loop_count. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| PASS writes skeptic_verdict.md with 'Verdict: PASS'. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| PASS calls run_tool with --complete. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| PASS returns 0 when update_state tool exits 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_verdict.py` | rationale |
| *(+28 more)* | | |

## Key Relationships

- **test_build_verdict.py** `contains` → _make_project() `[EXTRACTED]`
- **test_build_verdict.py** `contains` → _read_state() `[EXTRACTED]`
- **test_build_verdict.py** `contains` → _verdict_path() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_build_verdict.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _make_project() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_pass_exits_zero() `[INFERRED]`
- **_make_project()** `contains` → test_build_verdict.py `[EXTRACTED]`
- **_make_project()** `calls` → test_pass_writes_verdict_file() `[INFERRED]`
- **_make_project()** `calls` → test_pass_calls_update_state() `[INFERRED]`
- **Tests for Brick 8 — bricklayer build --verdict PASS|FAIL.** `rationale_for` → test_build_verdict.py `[EXTRACTED]`
- **PASS returns 1 when update_state tool exits non-zero.** `rationale_for` → test_pass_tool_failure_returns_one() `[EXTRACTED]`
- **FAIL increments loop_count by 1.** `rationale_for` → test_fail_increments_loop_count() `[EXTRACTED]`
- **FAIL does not advance next_action.** `rationale_for` → test_fail_next_action_unchanged() `[EXTRACTED]`
- **FAIL always returns 1.** `rationale_for` → test_fail_exits_one() `[EXTRACTED]`
- **FAIL below threshold prints normal blocker message.** `rationale_for` → test_fail_prints_blocker_message() `[EXTRACTED]`
- **loop_count=2 increments to 3 on FAIL.** `rationale_for` → test_fail_loop_count_2_increments_to_3() `[EXTRACTED]`