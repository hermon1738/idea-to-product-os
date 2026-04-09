# Agent Registry Tests

> Community 6 · 60 nodes · cohesion 0.05

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_agent_commands.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| _make_malformed_registry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| _make_registry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| Tests for Brick 22 — agent list and status commands. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | rationale |
| Write a registry.yaml to tmp_path with the given agents. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | rationale |
| test_cli_agent_list_empty_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_list_empty_shows_prompt() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_list_exit_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_list_no_yaml_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_list_output_contains_id() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_status_known_id_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_status_no_yaml_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_status_output_contains_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_status_unknown_id_error_in_output() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_cli_agent_status_unknown_id_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_agent_label() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_channel() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_id() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_location() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_role() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_runtime() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_detail_contains_trigger() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_row_contains_id() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_row_contains_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_row_contains_runtime() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_row_contains_status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| test_format_row_missing_key_renders_empty() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_commands.py` | code |
| *(+30 more)* | | |

## Key Relationships

- **test_agent_commands.py** `contains` → _make_registry() `[EXTRACTED]`
- **test_agent_commands.py** `contains` → _make_malformed_registry() `[EXTRACTED]`
- **test_agent_commands.py** `contains` → test_format_row_contains_id() `[EXTRACTED]`
- **_make_malformed_registry()** `contains` → test_agent_commands.py `[EXTRACTED]`
- **_make_malformed_registry()** `calls` → test_run_agent_list_malformed_registry_returns_one() `[INFERRED]`
- **_make_malformed_registry()** `calls` → test_run_agent_list_malformed_registry_no_traceback() `[INFERRED]`
- **_make_registry()** `contains` → test_agent_commands.py `[EXTRACTED]`
- **_make_registry()** `calls` → test_run_agent_list_empty_registry_returns_zero() `[INFERRED]`
- **_make_registry()** `calls` → test_run_agent_list_empty_registry_prints_prompt() `[INFERRED]`
- **Tests for Brick 22 — agent list and status commands.** `rationale_for` → test_agent_commands.py `[EXTRACTED]`
- **Write a registry.yaml to tmp_path with the given agents.** `rationale_for` → _make_registry() `[EXTRACTED]`
- **test_cli_agent_list_empty_exits_zero()** `contains` → test_agent_commands.py `[EXTRACTED]`
- **test_cli_agent_list_empty_exits_zero()** `calls` → _make_registry() `[INFERRED]`
- **test_cli_agent_list_empty_shows_prompt()** `contains` → test_agent_commands.py `[EXTRACTED]`
- **test_cli_agent_list_empty_shows_prompt()** `calls` → _make_registry() `[INFERRED]`
- **test_cli_agent_list_exit_zero()** `contains` → test_agent_commands.py `[EXTRACTED]`
- **test_cli_agent_list_exit_zero()** `calls` → _make_registry() `[INFERRED]`
- **test_cli_agent_list_no_yaml_exits_one()** `contains` → test_agent_commands.py `[EXTRACTED]`
- **test_cli_agent_list_output_contains_id()** `contains` → test_agent_commands.py `[EXTRACTED]`
- **test_cli_agent_list_output_contains_id()** `calls` → _make_registry() `[INFERRED]`