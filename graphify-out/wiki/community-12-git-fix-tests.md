# Git Fix Tests

> Community 12 · 46 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_git_fixes.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| _load_make_skeptic_packet() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| _mock_git_success() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| Tests for Brick 8.5 — auto-stage (make_skeptic_packet.py) and auto-commit (run_v | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| git add is called before git commit. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| All files are passed to git add. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| Commit message uses feat(brick-N) format. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| Commit message includes Co-Authored-By trailer. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| If git add fails, git commit is never called. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| PASS path calls git commit. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| PASS: git commit fails → exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| PASS: git commit fails → state.json next_action unchanged. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| PASS: update_state is called after commit succeeds. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| FAIL path: git commit is never called. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| _git_add_spec_files calls git add with all listed files. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| Files not in FILES list are not passed to git add. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| _git_add_spec_files does nothing when files list is empty. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| CliRunner: --verdict PASS triggers git commit. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| CliRunner: --verdict PASS with failing commit exits 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| Import make_skeptic_packet from bricklayer/tools/ fresh each time. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| BRICK: line is parsed and returned. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| Missing BRICK: line returns fallback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | rationale |
| _read_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| test_auto_stage_calls_git_add_with_spec_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| test_auto_stage_non_spec_file_not_staged() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| test_auto_stage_skips_when_no_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| test_cli_pass_calls_git_commit() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| test_cli_pass_commit_failure_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_git_fixes.py` | code |
| *(+16 more)* | | |

## Key Relationships

- **test_git_fixes.py** `contains` → _make_project() `[EXTRACTED]`
- **test_git_fixes.py** `contains` → _read_state() `[EXTRACTED]`
- **test_git_fixes.py** `contains` → _load_make_skeptic_packet() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_git_fixes.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _make_project() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_pass_calls_git_commit() `[INFERRED]`
- **_load_make_skeptic_packet()** `contains` → test_git_fixes.py `[EXTRACTED]`
- **_load_make_skeptic_packet()** `calls` → test_auto_stage_calls_git_add_with_spec_files() `[INFERRED]`
- **_load_make_skeptic_packet()** `calls` → test_auto_stage_non_spec_file_not_staged() `[INFERRED]`
- **_make_project()** `contains` → test_git_fixes.py `[EXTRACTED]`
- **_make_project()** `calls` → test_run_verdict_pass_runs_git_commit() `[INFERRED]`
- **_make_project()** `calls` → test_run_verdict_pass_commit_failure_exits_one() `[INFERRED]`
- **_mock_git_success()** `contains` → test_git_fixes.py `[EXTRACTED]`
- **Tests for Brick 8.5 — auto-stage (make_skeptic_packet.py) and auto-commit (run_v** `rationale_for` → test_git_fixes.py `[EXTRACTED]`
- **git add is called before git commit.** `rationale_for` → test_git_commit_spec_calls_git_add_then_commit() `[EXTRACTED]`
- **All files are passed to git add.** `rationale_for` → test_git_commit_spec_passes_files_to_add() `[EXTRACTED]`
- **Commit message uses feat(brick-N) format.** `rationale_for` → test_git_commit_spec_message_contains_brick_number() `[EXTRACTED]`
- **Commit message includes Co-Authored-By trailer.** `rationale_for` → test_git_commit_spec_message_contains_co_authored_by() `[EXTRACTED]`