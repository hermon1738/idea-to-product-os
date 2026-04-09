# Skeptic Packet Tests

> Community 10 · 51 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_build_skeptic.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | code |
| _cli_invoke() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | code |
| Tests for Brick 7 (revision) — bricklayer build --skeptic-packet flag handler. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Tool exits 0 but packet dir is missing → exit 1, state not updated. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| State is not updated when packet dir is missing after tool exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Tool exits 0 but packet dir is empty → exit 1, state not updated. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| State not updated when packet dir is empty. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Guard fires for any next_action other than tests_passed → exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Guard message tells user to run tests first. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Guard does not mutate state.json. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Guard output contains no raw Python traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| state.json present but next_action key absent → guard fires, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Missing next_action key prints the guard message (not a KeyError traceback). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| run_skeptic_packet returns 1 when tool exits non-zero. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Tool failure leaves state.json unchanged. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Returns 1 when skeptic key absent from config. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Error message mentions 'skeptic', no traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Set up project, mock run_tool, invoke `bricklayer build [flags]`. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| CliRunner: --skeptic-packet exits 0 when guard passes and packet dir exists. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| CliRunner: state.json next_action=skeptic_packet_ready after success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| CliRunner: --skeptic-packet exits 1 when next_action != tests_passed. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| CliRunner: passing --test and --skeptic-packet together exits 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| CliRunner: mutex error message printed when two flags passed. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| Write bricklayer/state.json (and optionally skeptic_packet/) under tmp_path. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| run_skeptic_packet returns 0 when guard passes, tool exits 0, packet dir exists. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| run_skeptic_packet sets next_action to 'skeptic_packet_ready' on success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| run_skeptic_packet prints the packet directory path on success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | rationale |
| _read_next_action() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | code |
| test_cli_guard_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_skeptic.py` | code |
| *(+21 more)* | | |

## Key Relationships

- **test_build_skeptic.py** `contains` → _make_project() `[EXTRACTED]`
- **test_build_skeptic.py** `contains` → _read_next_action() `[EXTRACTED]`
- **test_build_skeptic.py** `contains` → test_happy_path_returns_zero() `[EXTRACTED]`
- **_cli_invoke()** `contains` → test_build_skeptic.py `[EXTRACTED]`
- **_cli_invoke()** `calls` → _make_project() `[INFERRED]`
- **_cli_invoke()** `calls` → test_cli_happy_path_exits_zero() `[INFERRED]`
- **_make_project()** `contains` → test_build_skeptic.py `[EXTRACTED]`
- **_make_project()** `calls` → test_happy_path_returns_zero() `[INFERRED]`
- **_make_project()** `calls` → test_happy_path_updates_state() `[INFERRED]`
- **Tests for Brick 7 (revision) — bricklayer build --skeptic-packet flag handler.** `rationale_for` → test_build_skeptic.py `[EXTRACTED]`
- **Tool exits 0 but packet dir is missing → exit 1, state not updated.** `rationale_for` → test_fix2_missing_packet_dir_returns_one() `[EXTRACTED]`
- **State is not updated when packet dir is missing after tool exit 0.** `rationale_for` → test_fix2_missing_packet_dir_state_unchanged() `[EXTRACTED]`
- **Tool exits 0 but packet dir is empty → exit 1, state not updated.** `rationale_for` → test_fix2_empty_packet_dir_returns_one() `[EXTRACTED]`
- **State not updated when packet dir is empty.** `rationale_for` → test_fix2_empty_packet_dir_state_unchanged() `[EXTRACTED]`
- **Guard fires for any next_action other than tests_passed → exit 1.** `rationale_for` → test_guard_wrong_next_action_returns_one() `[EXTRACTED]`
- **Guard message tells user to run tests first.** `rationale_for` → test_guard_prints_run_tests_first() `[EXTRACTED]`