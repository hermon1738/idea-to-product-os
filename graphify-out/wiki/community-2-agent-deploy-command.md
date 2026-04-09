# Agent Deploy Command

> Community 2 · 78 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_agent_deploy.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| _cli_deploy() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| _git_failure() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| _git_success() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| _make_agent_dir() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| _make_deploy_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| _make_registry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| Tests for Brick 24 — bricklayer agent deploy and agent live commands. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| TimeoutExpired from subprocess.run must surface as exit 1, not a traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Confirm no raw traceback appears in stderr when git push times out. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Re-deploying unchanged agent files must exit 0, not abort. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Write registry.yaml to tmp_path. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Operator must see a clear message when nothing was pushed. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| VPS docker commands must still be printed even when nothing was pushed. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Create a minimal agent scaffold dir under context/agents/<id>/. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Invoke bricklayer agent deploy via CliRunner with mocked git. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Create a bare directory to use as the deploy repo (not a real git repo). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Return a mock CompletedProcess indicating git success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| Return a mock CompletedProcess indicating git failure. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | rationale |
| test_cli_agent_deploy_agent_missing_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_deploy_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_deploy_no_env_var_error_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_deploy_no_env_var_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_deploy_no_yaml_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_deploy_output_contains_deploy_ready() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_live_already_live_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_live_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_live_no_yaml_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_live_output_contains_marked_live() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| test_cli_agent_live_unknown_id_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_agent_deploy.py` | code |
| *(+48 more)* | | |

## Key Relationships

- **test_agent_deploy.py** `contains` → _make_registry() `[EXTRACTED]`
- **test_agent_deploy.py** `contains` → _make_agent_dir() `[EXTRACTED]`
- **test_agent_deploy.py** `contains` → _make_deploy_repo() `[EXTRACTED]`
- **_cli_deploy()** `contains` → test_agent_deploy.py `[EXTRACTED]`
- **_cli_deploy()** `calls` → _make_deploy_repo() `[INFERRED]`
- **_cli_deploy()** `calls` → _git_success() `[INFERRED]`
- **_git_failure()** `contains` → test_agent_deploy.py `[EXTRACTED]`
- **_git_failure()** `calls` → test_run_agent_deploy_not_git_repo_returns_one() `[INFERRED]`
- **_git_failure()** `calls` → test_run_agent_deploy_not_git_repo_error_message() `[INFERRED]`
- **_git_success()** `contains` → test_agent_deploy.py `[EXTRACTED]`
- **_git_success()** `calls` → test_run_agent_deploy_returns_zero() `[INFERRED]`
- **_git_success()** `calls` → test_run_agent_deploy_copies_files() `[INFERRED]`
- **_make_agent_dir()** `contains` → test_agent_deploy.py `[EXTRACTED]`
- **_make_agent_dir()** `calls` → test_run_agent_deploy_returns_zero() `[INFERRED]`
- **_make_agent_dir()** `calls` → test_run_agent_deploy_copies_files() `[INFERRED]`
- **_make_deploy_repo()** `contains` → test_agent_deploy.py `[EXTRACTED]`
- **_make_deploy_repo()** `calls` → test_run_agent_deploy_returns_zero() `[INFERRED]`
- **_make_deploy_repo()** `calls` → test_run_agent_deploy_copies_files() `[INFERRED]`
- **_make_registry()** `contains` → test_agent_deploy.py `[EXTRACTED]`
- **_make_registry()** `calls` → test_run_agent_deploy_returns_zero() `[INFERRED]`
- **_make_registry()** `calls` → test_run_agent_deploy_copies_files() `[INFERRED]`
- **Tests for Brick 24 — bricklayer agent deploy and agent live commands.** `rationale_for` → test_agent_deploy.py `[EXTRACTED]`
- **TimeoutExpired from subprocess.run must surface as exit 1, not a traceback.** `rationale_for` → test_run_agent_deploy_git_timeout_returns_one() `[EXTRACTED]`
- **Confirm no raw traceback appears in stderr when git push times out.** `rationale_for` → test_run_agent_deploy_git_timeout_no_traceback() `[EXTRACTED]`