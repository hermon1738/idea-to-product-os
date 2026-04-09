# Session Close Module

> Community 20 · 34 nodes · cohesion 0.09

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| close_session.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _append_decision_log() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _build_decision_log_row() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _build_pipeline_status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _build_user_message() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _call_groq() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _extract_structured_data() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _is_git_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _load_sprint_brain() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _load_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| _push_docs() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| Close-session command: sprint review via Groq, writes session-log.md and STATE.m | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Read LLM configuration from the llm: section of bricklayer.yaml.      Why it exi | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Load state.json and return the parsed dict, or None on any failure.      Why it | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Load the sprint-brain.md system prompt from the path declared in bricklayer.yaml | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Build the Groq user message from current state.json data.      Why it exists: Th | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Call the Groq API and return the response text, or None on any failure.      Why | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Write session-log.md with brick status and Groq sprint review.      Why it exist | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Write STATE.md with project name, current brick, and next command.      Why it e | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Replace pipe characters with dashes so they cannot corrupt markdown tables. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Call GROQ_HEAVY_MODEL to extract structured JSON from sprint review prose. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Build one sanitized pipe-delimited decision-log row from extracted data.      Wh | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Append one row to decision-log.md, creating the file with header if absent. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Build pipeline-status.md content from current state and sprint review.      Why | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Return True if path is inside a git repository.      Why it exists: Before runni | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Run git add / commit / push in DOCS_PATH to sync session docs to GitHub.      Wh | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Sync decision-log.md and pipeline-status.md to DOCS_PATH if set, then push. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| Sprint review via Groq; write session-log.md, STATE.md, and sync VPS docs. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | rationale |
| _read_llm_config() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| run_close_session() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py` | code |
| *(+4 more)* | | |

## Key Relationships

- **close_session.py** `contains` → _read_llm_config() `[EXTRACTED]`
- **close_session.py** `contains` → _load_state() `[EXTRACTED]`
- **close_session.py** `contains` → _load_sprint_brain() `[EXTRACTED]`
- **_append_decision_log()** `contains` → close_session.py `[EXTRACTED]`
- **_append_decision_log()** `calls` → _sync_docs() `[INFERRED]`
- **_append_decision_log()** `rationale_for` → Append one row to decision-log.md, creating the file with header if absent. `[EXTRACTED]`
- **_build_decision_log_row()** `contains` → close_session.py `[EXTRACTED]`
- **_build_decision_log_row()** `calls` → _sanitize_pipe() `[INFERRED]`
- **_build_decision_log_row()** `calls` → _sync_docs() `[INFERRED]`
- **_build_pipeline_status()** `contains` → close_session.py `[EXTRACTED]`
- **_build_pipeline_status()** `calls` → _sanitize_pipe() `[INFERRED]`
- **_build_pipeline_status()** `calls` → _sync_docs() `[INFERRED]`
- **_build_user_message()** `contains` → close_session.py `[EXTRACTED]`
- **_build_user_message()** `calls` → run_close_session() `[INFERRED]`
- **_build_user_message()** `rationale_for` → Build the Groq user message from current state.json data.      Why it exists: Th `[EXTRACTED]`
- **_call_groq()** `contains` → close_session.py `[EXTRACTED]`
- **_call_groq()** `calls` → run_close_session() `[INFERRED]`
- **_call_groq()** `rationale_for` → Call the Groq API and return the response text, or None on any failure.      Why `[EXTRACTED]`
- **_extract_structured_data()** `contains` → close_session.py `[EXTRACTED]`
- **_extract_structured_data()** `calls` → _sync_docs() `[INFERRED]`
- **_extract_structured_data()** `rationale_for` → Call GROQ_HEAVY_MODEL to extract structured JSON from sprint review prose. `[EXTRACTED]`
- **_is_git_repo()** `contains` → close_session.py `[EXTRACTED]`
- **_is_git_repo()** `calls` → _push_docs() `[INFERRED]`
- **_is_git_repo()** `rationale_for` → Return True if path is inside a git repository.      Why it exists: Before runni `[EXTRACTED]`
- **_load_sprint_brain()** `contains` → close_session.py `[EXTRACTED]`
- **_load_sprint_brain()** `calls` → run_close_session() `[INFERRED]`
- **_load_sprint_brain()** `rationale_for` → Load the sprint-brain.md system prompt from the path declared in bricklayer.yaml `[EXTRACTED]`
- **_load_state()** `contains` → close_session.py `[EXTRACTED]`
- **_load_state()** `calls` → run_close_session() `[INFERRED]`
- **_load_state()** `rationale_for` → Load state.json and return the parsed dict, or None on any failure.      Why it `[EXTRACTED]`