# Session Close Pipeline

> Community 0 · 151 nodes · cohesion 0.02

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_close_session.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| _full_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| _mock_groq_success() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| Tests for Brick 12 / Brick 18 — bricklayer close-session command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| _is_git_repo returns True for a directory git-initialised as a repo. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| _is_git_repo returns False for a plain directory with no .git. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| DOCS_PATH not a git repo → warning to stderr, no subprocess calls. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| No git subprocess calls when _is_git_repo returns False. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| _push_docs returns None (no exception) when not a git repo. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| git push returncode != 0 → warning to stderr. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| Push failure does not raise — returns None. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| Successful push prints 'Docs pushed to GitHub'. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| Commit message starts with 'sync: session docs'. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| git add call targets docs/ only, not the entire repo. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| subprocess.TimeoutExpired → warning to stderr, no crash. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| subprocess.TimeoutExpired does not propagate — returns None. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| FileNotFoundError (git not in PATH) → warning to stderr, no crash. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| FileNotFoundError does not propagate — returns None. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| DOCS_PATH not set → _push_docs never invoked. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| DOCS_PATH set and exists → _push_docs called once with docs_path. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| Push failure (non-fatal) does not change run_close_session return code. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| DOCS_PATH set but not a git repo → warning printed, exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| _sync_docs returns None (no exception) when DOCS_PATH is not set. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | rationale |
| test_append_decision_log_appends_row() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| test_append_decision_log_appends_to_existing_file() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| test_append_decision_log_creates_file_if_missing() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| test_append_decision_log_creates_header_if_missing() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| test_append_decision_log_multiple_rows() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| test_build_decision_log_row_contains_component() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_close_session.py` | code |
| *(+121 more)* | | |

## Key Relationships

- **test_close_session.py** `contains` → _write_state() `[EXTRACTED]`
- **test_close_session.py** `contains` → _write_yaml() `[EXTRACTED]`
- **test_close_session.py** `contains` → _write_sprint_brain() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_close_session.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _full_setup() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_close_session_exits_zero() `[INFERRED]`
- **_full_setup()** `contains` → test_close_session.py `[EXTRACTED]`
- **_full_setup()** `calls` → _write_state() `[INFERRED]`
- **_full_setup()** `calls` → _write_yaml() `[INFERRED]`
- **_mock_groq_success()** `contains` → test_close_session.py `[EXTRACTED]`
- **_mock_groq_success()** `calls` → test_call_groq_returns_text() `[INFERRED]`
- **_mock_groq_success()** `calls` → test_call_groq_passes_model() `[INFERRED]`
- **Tests for Brick 12 / Brick 18 — bricklayer close-session command.** `rationale_for` → test_close_session.py `[EXTRACTED]`
- **_is_git_repo returns True for a directory git-initialised as a repo.** `rationale_for` → test_is_git_repo_returns_true_for_real_repo() `[EXTRACTED]`
- **_is_git_repo returns False for a plain directory with no .git.** `rationale_for` → test_is_git_repo_returns_false_for_plain_dir() `[EXTRACTED]`
- **DOCS_PATH not a git repo → warning to stderr, no subprocess calls.** `rationale_for` → test_push_docs_not_git_repo_prints_warning() `[EXTRACTED]`
- **No git subprocess calls when _is_git_repo returns False.** `rationale_for` → test_push_docs_not_git_repo_no_subprocess_calls() `[EXTRACTED]`
- **_push_docs returns None (no exception) when not a git repo.** `rationale_for` → test_push_docs_not_git_repo_returns_none() `[EXTRACTED]`