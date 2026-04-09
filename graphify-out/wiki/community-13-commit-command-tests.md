# Commit Command Tests

> Community 13 · 44 nodes · cohesion 0.08

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_commit.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| _make_real_git_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| _mock_nothing_staged() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| _mock_staged() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| Tests for Brick 11 — bricklayer commit command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | rationale |
| Create a minimal real git repo for integration testing. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | rationale |
| Integration: real git repo — bricklayer commit creates a correctly tagged commit | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | rationale |
| Integration: nothing staged → exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | rationale |
| Return a side_effect for subprocess.run that reports staged files. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | rationale |
| test_build_message_blank_line_after_subject() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_build_message_body_contains_brick_line() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_build_message_subject_format() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_build_message_trailer_present() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_check_staged_returns_empty_on_file_not_found() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_check_staged_returns_empty_when_nothing() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_check_staged_returns_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_cli_commit_no_m_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_cli_commit_no_m_no_traceback() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_cli_commit_no_m_prints_usage() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_cli_commit_output_contains_commit_info() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_cli_commit_real_git_creates_commit() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_cli_commit_real_git_nothing_staged_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_cli_commit_with_message_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_parse_brick_decimal() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_parse_brick_extracts_number_and_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_parse_brick_unknown_format() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_run_commit_calls_git_commit() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| test_run_commit_empty_message_error_text() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_commit.py` | code |
| *(+14 more)* | | |

## Key Relationships

- **test_commit.py** `contains` → _make_project() `[EXTRACTED]`
- **test_commit.py** `contains` → _mock_staged() `[EXTRACTED]`
- **test_commit.py** `contains` → _mock_nothing_staged() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_commit.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _make_project() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_commit_no_m_exits_one() `[INFERRED]`
- **_make_project()** `contains` → test_commit.py `[EXTRACTED]`
- **_make_project()** `calls` → test_run_commit_returns_zero() `[INFERRED]`
- **_make_project()** `calls` → test_run_commit_calls_git_commit() `[INFERRED]`
- **_make_real_git_repo()** `contains` → test_commit.py `[EXTRACTED]`
- **_make_real_git_repo()** `calls` → test_cli_commit_real_git_creates_commit() `[INFERRED]`
- **_make_real_git_repo()** `calls` → test_cli_commit_real_git_nothing_staged_exits_one() `[INFERRED]`
- **_mock_nothing_staged()** `contains` → test_commit.py `[EXTRACTED]`
- **_mock_nothing_staged()** `calls` → test_run_commit_nothing_staged_exits_one() `[INFERRED]`
- **_mock_nothing_staged()** `calls` → test_run_commit_nothing_staged_message() `[INFERRED]`
- **_mock_staged()** `contains` → test_commit.py `[EXTRACTED]`
- **_mock_staged()** `calls` → test_run_commit_returns_zero() `[INFERRED]`
- **_mock_staged()** `calls` → test_run_commit_prints_output() `[INFERRED]`
- **Tests for Brick 11 — bricklayer commit command.** `rationale_for` → test_commit.py `[EXTRACTED]`
- **Create a minimal real git repo for integration testing.** `rationale_for` → _make_real_git_repo() `[EXTRACTED]`
- **Integration: real git repo — bricklayer commit creates a correctly tagged commit** `rationale_for` → test_cli_commit_real_git_creates_commit() `[EXTRACTED]`
- **Integration: nothing staged → exit 1.** `rationale_for` → test_cli_commit_real_git_nothing_staged_exits_one() `[EXTRACTED]`