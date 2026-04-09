# Build Tools Tests

> Community 9 · 53 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_build_tools.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | code |
| _cli_invoke() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | code |
| Tests for Brick 6 — bricklayer build --snapshot/--verify/--test flag handlers. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_snapshot sets next_action to 'snapshot_init' on success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_snapshot returns 1 on non-zero tool exit. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_snapshot leaves state.json unchanged on tool failure. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_verify returns 0 on tool exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_verify sets next_action to 'verify' on success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_verify returns 1 on non-zero tool exit. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_verify leaves state.json unchanged on tool failure. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_test returns 0 on tool exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_test sets next_action to 'tests_passed' on success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_test returns 1 on non-zero tool exit (test suite failure). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_test leaves state.json unchanged on test failure. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| Flag handler returns 1 when tool key absent from config. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| Error message mentions the missing tool key, no traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| Set up project, mock run_tool, invoke bricklayer build <flag>. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| CliRunner: `bricklayer build --snapshot` exits 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| CliRunner: next_action='snapshot_init' after --snapshot. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| CliRunner: `bricklayer build --verify` exits 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| CliRunner: next_action='verify' after --verify. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| CliRunner: `bricklayer build --test` exits 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| CliRunner: next_action='tests_passed' after --test. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| Write bricklayer/ dir + state.json. Returns repo root. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| get_tool_path returns resolved Path when key is present. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| get_tool_path returns None when the key is not in tools:. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| get_tool_path returns None when tools: section is absent entirely. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| run_snapshot returns 0 on tool exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | rationale |
| _read_next_action() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_build_tools.py` | code |
| *(+23 more)* | | |

## Key Relationships

- **test_build_tools.py** `contains` → _make_project() `[EXTRACTED]`
- **test_build_tools.py** `contains` → _read_next_action() `[EXTRACTED]`
- **test_build_tools.py** `contains` → test_get_tool_path_found() `[EXTRACTED]`
- **_cli_invoke()** `contains` → test_build_tools.py `[EXTRACTED]`
- **_cli_invoke()** `calls` → _make_project() `[INFERRED]`
- **_cli_invoke()** `calls` → test_cli_snapshot_exits_zero() `[INFERRED]`
- **_make_project()** `contains` → test_build_tools.py `[EXTRACTED]`
- **_make_project()** `calls` → test_snapshot_success_returns_zero() `[INFERRED]`
- **_make_project()** `calls` → test_snapshot_success_updates_state() `[INFERRED]`
- **Tests for Brick 6 — bricklayer build --snapshot/--verify/--test flag handlers.** `rationale_for` → test_build_tools.py `[EXTRACTED]`
- **run_snapshot sets next_action to 'snapshot_init' on success.** `rationale_for` → test_snapshot_success_updates_state() `[EXTRACTED]`
- **run_snapshot returns 1 on non-zero tool exit.** `rationale_for` → test_snapshot_failure_returns_one() `[EXTRACTED]`
- **run_snapshot leaves state.json unchanged on tool failure.** `rationale_for` → test_snapshot_failure_does_not_update_state() `[EXTRACTED]`
- **run_verify returns 0 on tool exit 0.** `rationale_for` → test_verify_success_returns_zero() `[EXTRACTED]`
- **run_verify sets next_action to 'verify' on success.** `rationale_for` → test_verify_success_updates_state() `[EXTRACTED]`
- **run_verify returns 1 on non-zero tool exit.** `rationale_for` → test_verify_failure_returns_one() `[EXTRACTED]`