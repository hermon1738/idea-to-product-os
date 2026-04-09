# Main CLI Tests

> Community 23 · 24 nodes · cohesion 0.11

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_main.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| _make_file() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| CliRunner integration tests for cli/main.py. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| run command exits 1 when a yaml path is missing. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| Missing path error output must not show a Python traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| run command exits 1 when bricklayer.yaml is not found anywhere. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| Create a minimal project for close-session tests. Returns yaml_path. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| CliRunner integration: .env loaded at startup; llm: section drives model choice. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| api_key_env pointing to an unset var → clear error message, exit 1, no traceback | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| bricklayer --help → exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| bricklayer --help output must not contain 'Traceback'. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| --help output mentions at least one subcommand. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| run command exits 0 when all yaml paths exist. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | rationale |
| _setup_close_session_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_close_session_api_key_env_unset_exits_1_with_clear_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_close_session_loads_env_file_and_uses_llm_config() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_help_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_help_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_help_shows_commands() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_run_command_missing_path_exits_1() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_run_command_missing_path_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_run_command_no_yaml_exits_1() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| test_run_command_passes_with_valid_yaml() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |
| _write_yaml() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_main.py` | code |

## Key Relationships

- **test_main.py** `contains` → _write_yaml() `[EXTRACTED]`
- **test_main.py** `contains` → _make_file() `[EXTRACTED]`
- **test_main.py** `contains` → test_help_exits_zero() `[EXTRACTED]`
- **_make_file()** `contains` → test_main.py `[EXTRACTED]`
- **_make_file()** `calls` → test_run_command_passes_with_valid_yaml() `[INFERRED]`
- **CliRunner integration tests for cli/main.py.** `rationale_for` → test_main.py `[EXTRACTED]`
- **run command exits 1 when a yaml path is missing.** `rationale_for` → test_run_command_missing_path_exits_1() `[EXTRACTED]`
- **Missing path error output must not show a Python traceback.** `rationale_for` → test_run_command_missing_path_no_traceback() `[EXTRACTED]`
- **run command exits 1 when bricklayer.yaml is not found anywhere.** `rationale_for` → test_run_command_no_yaml_exits_1() `[EXTRACTED]`
- **Create a minimal project for close-session tests. Returns yaml_path.** `rationale_for` → _setup_close_session_project() `[EXTRACTED]`
- **CliRunner integration: .env loaded at startup; llm: section drives model choice.** `rationale_for` → test_close_session_loads_env_file_and_uses_llm_config() `[EXTRACTED]`
- **api_key_env pointing to an unset var → clear error message, exit 1, no traceback** `rationale_for` → test_close_session_api_key_env_unset_exits_1_with_clear_message() `[EXTRACTED]`
- **bricklayer --help → exit 0.** `rationale_for` → test_help_exits_zero() `[EXTRACTED]`