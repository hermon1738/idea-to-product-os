# Pause & Resume Tests

> Community 11 · 48 nodes · cohesion 0.08

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_pause.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| _fake_git_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| Tests for Brick 9 — bricklayer pause command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | rationale |
| If .continue-here.md write fails, HANDOFF.json is cleaned up too. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | rationale |
| CliRunner: `bricklayer pause` exits 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | rationale |
| CliRunner: both HANDOFF.json and .continue-here.md are written. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | rationale |
| CliRunner: HANDOFF.json contains all 8 fields with correct values. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | rationale |
| CliRunner: .continue-here.md contains all required lines. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | rationale |
| Return a subprocess.run side_effect that reports a given branch name. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | rationale |
| _sample_handoff() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_continue_md_branch_matches_handoff() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_continue_md_contains_all_required_lines() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_continue_md_contains_blockers_none() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_continue_md_next_command_matches_handoff() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_continue_md_timestamp_matches_handoff() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_all_fields_present() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_brick_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_brick_number() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_current_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_last_action_matches_next_action() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_loop_count() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_project_is_root_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_build_handoff_timestamp_is_iso8601() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_cli_pause_continue_md_correct_content() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_cli_pause_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_cli_pause_handoff_json_correct_content() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_cli_pause_writes_both_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| test_next_command_known_action() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_pause.py` | code |
| *(+18 more)* | | |

## Key Relationships

- **test_pause.py** `contains` → _make_project() `[EXTRACTED]`
- **test_pause.py** `contains` → _fake_git_branch() `[EXTRACTED]`
- **test_pause.py** `contains` → test_parse_brick_extracts_number_and_name() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_pause.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _make_project() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_pause_exits_zero() `[INFERRED]`
- **_fake_git_branch()** `contains` → test_pause.py `[EXTRACTED]`
- **_fake_git_branch()** `calls` → test_build_handoff_all_fields_present() `[INFERRED]`
- **_fake_git_branch()** `calls` → test_build_handoff_brick_number() `[INFERRED]`
- **_make_project()** `contains` → test_pause.py `[EXTRACTED]`
- **_make_project()** `calls` → test_build_handoff_all_fields_present() `[INFERRED]`
- **_make_project()** `calls` → test_build_handoff_brick_number() `[INFERRED]`
- **Tests for Brick 9 — bricklayer pause command.** `rationale_for` → test_pause.py `[EXTRACTED]`
- **If .continue-here.md write fails, HANDOFF.json is cleaned up too.** `rationale_for` → test_run_pause_second_write_failure_removes_handoff() `[EXTRACTED]`
- **CliRunner: `bricklayer pause` exits 0.** `rationale_for` → test_cli_pause_exits_zero() `[EXTRACTED]`
- **CliRunner: both HANDOFF.json and .continue-here.md are written.** `rationale_for` → test_cli_pause_writes_both_files() `[EXTRACTED]`
- **CliRunner: HANDOFF.json contains all 8 fields with correct values.** `rationale_for` → test_cli_pause_handoff_json_correct_content() `[EXTRACTED]`
- **CliRunner: .continue-here.md contains all required lines.** `rationale_for` → test_cli_pause_continue_md_correct_content() `[EXTRACTED]`