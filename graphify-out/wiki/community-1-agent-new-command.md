# Agent New Command

> Community 1 · 88 nodes · cohesion 0.04

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_agent_new.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| _cli_agent_new() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| _make_nanobot_template() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| _make_registry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| Tests for Brick 23 — bricklayer agent new command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | rationale |
| Create registry.yaml in tmp_path with the given agents. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | rationale |
| Create a minimal nanobot-template directory under tmp_path. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | rationale |
| Helper: invoke bricklayer agent new with standard flags via CliRunner. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | rationale |
| test_build_placeholder_map_agent_id() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_placeholder_map_container_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_placeholder_map_discord_channel() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_placeholder_map_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_placeholder_map_role() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_placeholder_map_sequence() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_registry_entry_id() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_registry_entry_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_registry_entry_runtime() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_build_registry_entry_status_stopped() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_cli_agent_new_invalid_id_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_cli_agent_new_nanobot_directory_created() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_cli_agent_new_nanobot_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_cli_agent_new_nanobot_registered_in_registry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_cli_agent_new_no_yaml_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_cli_agent_new_raw_python_directory_created() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_cli_agent_new_raw_python_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_get_template_path_agents_none() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_get_template_path_default() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_get_template_path_empty_agents_dict() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_get_template_path_from_config() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| test_replace_placeholders_missing_file_no_crash() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_new.py` | code |
| *(+58 more)* | | |

## Key Relationships

- **test_agent_new.py** `contains` → _make_registry() `[EXTRACTED]`
- **test_agent_new.py** `contains` → _make_nanobot_template() `[EXTRACTED]`
- **test_agent_new.py** `contains` → test_validate_valid_id_returns_none() `[EXTRACTED]`
- **_cli_agent_new()** `contains` → test_agent_new.py `[EXTRACTED]`
- **_cli_agent_new()** `calls` → _make_registry() `[INFERRED]`
- **_cli_agent_new()** `calls` → _make_nanobot_template() `[INFERRED]`
- **_make_nanobot_template()** `contains` → test_agent_new.py `[EXTRACTED]`
- **_make_nanobot_template()** `calls` → test_scaffold_nanobot_creates_directory() `[INFERRED]`
- **_make_nanobot_template()** `calls` → test_scaffold_nanobot_agent_yaml_id_replaced() `[INFERRED]`
- **_make_registry()** `contains` → test_agent_new.py `[EXTRACTED]`
- **_make_registry()** `calls` → test_scaffold_nanobot_creates_directory() `[INFERRED]`
- **_make_registry()** `calls` → test_run_agent_new_nanobot_returns_zero() `[INFERRED]`
- **Tests for Brick 23 — bricklayer agent new command.** `rationale_for` → test_agent_new.py `[EXTRACTED]`
- **Create registry.yaml in tmp_path with the given agents.** `rationale_for` → _make_registry() `[EXTRACTED]`
- **Create a minimal nanobot-template directory under tmp_path.** `rationale_for` → _make_nanobot_template() `[EXTRACTED]`
- **Helper: invoke bricklayer agent new with standard flags via CliRunner.** `rationale_for` → _cli_agent_new() `[EXTRACTED]`
- **test_build_placeholder_map_agent_id()** `contains` → test_agent_new.py `[EXTRACTED]`
- **test_build_placeholder_map_container_name()** `contains` → test_agent_new.py `[EXTRACTED]`