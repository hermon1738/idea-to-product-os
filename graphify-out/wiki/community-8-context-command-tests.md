# Context Command Tests

> Community 8 · 56 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_context.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| _make_bricklayer_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| Tests for Brick 20 — bricklayer context command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | rationale |
| Write a minimal bricklayer.yaml for CliRunner tests. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | rationale |
| Create a full project directory at context/projects/<name>/. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | rationale |
| Write bricklayer/state.json with the given project field. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | rationale |
| _setup_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_cli_context_exit_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_cli_context_no_decisions() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_cli_context_no_flag_uses_bricklayer_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_cli_context_output_has_all_six_sections() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_cli_context_output_has_project_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_cli_context_project_not_found_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_load_project_state_malformed_returns_none() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_load_project_state_missing_returns_none() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_load_project_state_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_load_project_state_returns_dict() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_last_decisions_empty_log() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_last_decisions_limit_to_3() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_last_decisions_missing_file() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_last_decisions_returns_last_3() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_last_decisions_returns_rows() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_last_decisions_skips_header() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_last_decisions_skips_separator() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_next_command_default_on_missing_field() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_next_command_default_on_missing_file() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_read_next_command_returns_value() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_resolve_project_name_from_bricklayer_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| test_resolve_project_name_missing_state_returns_none() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_context.py` | code |
| *(+26 more)* | | |

## Key Relationships

- **test_context.py** `contains` → _make_project() `[EXTRACTED]`
- **test_context.py** `contains` → _make_bricklayer_state() `[EXTRACTED]`
- **test_context.py** `contains` → _setup_repo() `[EXTRACTED]`
- **_make_bricklayer_state()** `contains` → test_context.py `[EXTRACTED]`
- **_make_bricklayer_state()** `calls` → test_resolve_project_name_from_bricklayer_state() `[INFERRED]`
- **_make_bricklayer_state()** `calls` → test_resolve_project_name_strips_brick_prefix() `[INFERRED]`
- **_make_project()** `contains` → test_context.py `[EXTRACTED]`
- **_make_project()** `calls` → test_load_project_state_returns_dict() `[INFERRED]`
- **_make_project()** `calls` → test_load_project_state_malformed_returns_none() `[INFERRED]`
- **Tests for Brick 20 — bricklayer context command.** `rationale_for` → test_context.py `[EXTRACTED]`
- **Write a minimal bricklayer.yaml for CliRunner tests.** `rationale_for` → _setup_repo() `[EXTRACTED]`
- **Create a full project directory at context/projects/<name>/.** `rationale_for` → _make_project() `[EXTRACTED]`
- **Write bricklayer/state.json with the given project field.** `rationale_for` → _make_bricklayer_state() `[EXTRACTED]`
- **_setup_repo()** `contains` → test_context.py `[EXTRACTED]`
- **_setup_repo()** `calls` → test_cli_context_exit_zero() `[INFERRED]`
- **_setup_repo()** `calls` → test_cli_context_output_has_project_name() `[INFERRED]`
- **test_cli_context_exit_zero()** `contains` → test_context.py `[EXTRACTED]`
- **test_cli_context_exit_zero()** `calls` → _setup_repo() `[INFERRED]`
- **test_cli_context_exit_zero()** `calls` → _make_project() `[INFERRED]`
- **test_cli_context_no_decisions()** `contains` → test_context.py `[EXTRACTED]`
- **test_cli_context_no_decisions()** `calls` → _setup_repo() `[INFERRED]`
- **test_cli_context_no_decisions()** `calls` → _make_project() `[INFERRED]`