# Status Command Tests

> Community 25 · 20 nodes · cohesion 0.13

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_status.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| Tests for cli/commands/status.py — bricklayer status command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| When state.json is absent, run_status() auto-creates it and exits 0.      Brick | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| Error message is human-readable and contains 'state.json'. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| CliRunner: status exits 0 and all 5 field labels appear in output. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| CliRunner: status exits 0 when state.json is absent (auto-create). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| Create a minimal project tree under tmp_path. Returns the root. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| run_status() prints all 5 labeled fields and returns 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| run_status() prints values sourced from the correct files. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| When STATE.md is absent, exit code is still 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| When STATE.md is absent, project and phase show fallback text, not blank. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | rationale |
| test_cli_runner_happy_path() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| test_cli_runner_missing_state_json_autocreates() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| test_happy_path_all_five_fields_printed() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| test_happy_path_values_correct() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| test_missing_state_json_autocreates() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| test_missing_state_json_clear_error() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| test_missing_state_md_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |
| test_missing_state_md_fallback_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_status.py` | code |

## Key Relationships

- **test_status.py** `contains` → _make_project() `[EXTRACTED]`
- **test_status.py** `contains` → test_happy_path_all_five_fields_printed() `[EXTRACTED]`
- **test_status.py** `contains` → test_happy_path_values_correct() `[EXTRACTED]`
- **_make_project()** `contains` → test_status.py `[EXTRACTED]`
- **_make_project()** `calls` → test_happy_path_all_five_fields_printed() `[INFERRED]`
- **_make_project()** `calls` → test_happy_path_values_correct() `[INFERRED]`
- **Tests for cli/commands/status.py — bricklayer status command.** `rationale_for` → test_status.py `[EXTRACTED]`
- **When state.json is absent, run_status() auto-creates it and exits 0.      Brick** `rationale_for` → test_missing_state_json_autocreates() `[EXTRACTED]`
- **Error message is human-readable and contains 'state.json'.** `rationale_for` → test_missing_state_json_clear_error() `[EXTRACTED]`
- **CliRunner: status exits 0 and all 5 field labels appear in output.** `rationale_for` → test_cli_runner_happy_path() `[EXTRACTED]`
- **CliRunner: status exits 0 when state.json is absent (auto-create).** `rationale_for` → test_cli_runner_missing_state_json_autocreates() `[EXTRACTED]`
- **Create a minimal project tree under tmp_path. Returns the root.** `rationale_for` → _make_project() `[EXTRACTED]`
- **run_status() prints all 5 labeled fields and returns 0.** `rationale_for` → test_happy_path_all_five_fields_printed() `[EXTRACTED]`
- **run_status() prints values sourced from the correct files.** `rationale_for` → test_happy_path_values_correct() `[EXTRACTED]`