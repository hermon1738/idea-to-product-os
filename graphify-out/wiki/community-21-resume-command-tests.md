# Resume Command Tests

> Community 21 · 33 nodes · cohesion 0.10

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_resume.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| _fake_git() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| Tests for Brick 10 — bricklayer resume command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | rationale |
| test_cli_resume_branch_mismatch_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_cli_resume_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_cli_resume_missing_handoff_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_cli_resume_output_contains_all_fields() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_brick_number_and_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_last_action() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_loop_count() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_next_command() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_resuming_session() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_rule_lines() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_format_block_contains_timestamp() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_branch_match_no_warning() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_branch_mismatch_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_branch_mismatch_prints_warning() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_branch_mismatch_warning_includes_checkout_hint() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_malformed_json_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_malformed_json_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_malformed_json_prints_error() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_missing_field_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_missing_field_names_field_in_error() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_missing_handoff_correct_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_missing_handoff_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_missing_handoff_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| test_run_resume_output_contains_divider_lines() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_resume.py` | code |
| *(+3 more)* | | |

## Key Relationships

- **test_resume.py** `contains` → _write_handoff() `[EXTRACTED]`
- **test_resume.py** `contains` → _fake_git() `[EXTRACTED]`
- **test_resume.py** `contains` → test_format_block_contains_rule_lines() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_resume.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _write_handoff() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_resume_exits_zero() `[INFERRED]`
- **_fake_git()** `contains` → test_resume.py `[EXTRACTED]`
- **_fake_git()** `calls` → test_run_resume_returns_zero() `[INFERRED]`
- **_fake_git()** `calls` → test_run_resume_prints_all_fields() `[INFERRED]`
- **Tests for Brick 10 — bricklayer resume command.** `rationale_for` → test_resume.py `[EXTRACTED]`
- **test_cli_resume_branch_mismatch_exits_zero()** `contains` → test_resume.py `[EXTRACTED]`
- **test_cli_resume_branch_mismatch_exits_zero()** `calls` → _cli_setup() `[INFERRED]`
- **test_cli_resume_branch_mismatch_exits_zero()** `calls` → _fake_git() `[INFERRED]`
- **test_cli_resume_exits_zero()** `contains` → test_resume.py `[EXTRACTED]`
- **test_cli_resume_exits_zero()** `calls` → _cli_setup() `[INFERRED]`
- **test_cli_resume_exits_zero()** `calls` → _fake_git() `[INFERRED]`
- **test_cli_resume_missing_handoff_exits_one()** `contains` → test_resume.py `[EXTRACTED]`
- **test_cli_resume_output_contains_all_fields()** `contains` → test_resume.py `[EXTRACTED]`
- **test_cli_resume_output_contains_all_fields()** `calls` → _cli_setup() `[INFERRED]`
- **test_cli_resume_output_contains_all_fields()** `calls` → _fake_git() `[INFERRED]`
- **test_format_block_contains_branch()** `contains` → test_resume.py `[EXTRACTED]`
- **test_format_block_contains_brick_number_and_name()** `contains` → test_resume.py `[EXTRACTED]`