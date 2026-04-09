# Branch Command Tests

> Community 3 · 71 nodes · cohesion 0.04

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_branch.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | code |
| _make_project() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | code |
| _mock_get_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | code |
| _mock_git_fail() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | code |
| _mock_git_success() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | code |
| Tests for Brick 8.6 — bricklayer branch command and build main guard. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| brick/N-name is constructed from number + slugified name. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| current_branch is written to state.json. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| Output contains the created branch name. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| Missing number → error, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| Missing name → error, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| feature/name is constructed when --feature is set. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| current_branch is set to feature/name in state.json. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| --feature with no name → error, exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| Existing branch → clear error, exit 1, no overwrite. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| On branch-exists error, state.json is not modified. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| Return a side_effect that reports a specific branch for git rev-parse. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| PASS on brick/* merges to current_phase from state.json. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| PASS on brick/* prints merge confirmation with phase target. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| PASS on feature/* merges to main. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| PASS on feature/* still calls update_state --complete. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| PASS: merge failure → exit 1, state not advanced. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| PASS: merge failure → no raw traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| CliRunner: `bricklayer build` on main → exit 1. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| CliRunner: main guard prints helpful branch creation hint. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| CliRunner: main guard → no raw traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| CliRunner: `bricklayer build` on non-main branch → no guard trigger (exit 0). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| CliRunner: `bricklayer branch 9 bricklayer-pause` → exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| CliRunner: branch command prints created branch name. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_branch.py` | rationale |
| *(+41 more)* | | |

## Key Relationships

- **test_branch.py** `contains` → _make_project() `[EXTRACTED]`
- **test_branch.py** `contains` → _read_state() `[EXTRACTED]`
- **test_branch.py** `contains` → _mock_git_success() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_branch.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _make_project() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_build_on_main_exits_one() `[INFERRED]`
- **_make_project()** `contains` → test_branch.py `[EXTRACTED]`
- **_make_project()** `calls` → test_run_branch_brick_creates_correct_name() `[INFERRED]`
- **_make_project()** `calls` → test_run_branch_brick_updates_state() `[INFERRED]`
- **_mock_get_branch()** `contains` → test_branch.py `[EXTRACTED]`
- **_mock_get_branch()** `calls` → test_verdict_pass_brick_branch_prints_merge_message() `[INFERRED]`
- **_mock_get_branch()** `calls` → test_verdict_pass_feature_branch_state_advances() `[INFERRED]`
- **_mock_git_fail()** `contains` → test_branch.py `[EXTRACTED]`
- **_mock_git_success()** `contains` → test_branch.py `[EXTRACTED]`
- **Tests for Brick 8.6 — bricklayer branch command and build main guard.** `rationale_for` → test_branch.py `[EXTRACTED]`
- **brick/N-name is constructed from number + slugified name.** `rationale_for` → test_run_branch_brick_creates_correct_name() `[EXTRACTED]`
- **current_branch is written to state.json.** `rationale_for` → test_run_branch_brick_updates_state() `[EXTRACTED]`
- **Output contains the created branch name.** `rationale_for` → test_run_branch_brick_prints_branch_name() `[EXTRACTED]`