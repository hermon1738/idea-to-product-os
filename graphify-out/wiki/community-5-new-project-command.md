# New Project Command

> Community 5 · 64 nodes · cohesion 0.04

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_new_project.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| _project_dir() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| Tests for Brick 19 — bricklayer new-project command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | rationale |
| Create a minimal bricklayer.yaml so CliRunner commands can find the repo. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | rationale |
| _setup_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_decision_log_contains_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_decision_log_has_separator_row() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_decision_log_has_table_header() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_decision_log_heading_format() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_json_has_all_required_keys() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_json_last_test_run_has_all_keys() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_json_last_test_run_nulls() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_json_loop_count_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_json_nulls_for_optional_fields() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_json_project_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_json_serializable() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_md_contains_created_date() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_md_contains_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_md_contains_required_fields() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_build_state_md_heading_format() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_cli_new_project_all_files_exist() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_cli_new_project_duplicate_exit_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_cli_new_project_exit_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_cli_new_project_invalid_name_exit_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_cli_new_project_output_contains_path() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_cli_new_project_prints_created() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_cli_new_project_state_json_content() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_run_new_project_creates_decision_log() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_run_new_project_creates_project_directory() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| test_run_new_project_creates_projects_dir_if_absent() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_new_project.py` | code |
| *(+34 more)* | | |

## Key Relationships

- **test_new_project.py** `contains` → _setup_repo() `[EXTRACTED]`
- **test_new_project.py** `contains` → _project_dir() `[EXTRACTED]`
- **test_new_project.py** `contains` → test_validate_name_simple_alpha() `[EXTRACTED]`
- **_project_dir()** `contains` → test_new_project.py `[EXTRACTED]`
- **_project_dir()** `calls` → test_run_new_project_creates_project_directory() `[INFERRED]`
- **_project_dir()** `calls` → test_run_new_project_creates_state_md() `[INFERRED]`
- **Tests for Brick 19 — bricklayer new-project command.** `rationale_for` → test_new_project.py `[EXTRACTED]`
- **Create a minimal bricklayer.yaml so CliRunner commands can find the repo.** `rationale_for` → _setup_repo() `[EXTRACTED]`
- **_setup_repo()** `contains` → test_new_project.py `[EXTRACTED]`
- **_setup_repo()** `calls` → test_cli_new_project_exit_zero() `[INFERRED]`
- **_setup_repo()** `calls` → test_cli_new_project_prints_created() `[INFERRED]`
- **test_build_decision_log_contains_name()** `contains` → test_new_project.py `[EXTRACTED]`
- **test_build_decision_log_has_separator_row()** `contains` → test_new_project.py `[EXTRACTED]`
- **test_build_decision_log_has_table_header()** `contains` → test_new_project.py `[EXTRACTED]`
- **test_build_decision_log_heading_format()** `contains` → test_new_project.py `[EXTRACTED]`
- **test_build_state_json_has_all_required_keys()** `contains` → test_new_project.py `[EXTRACTED]`