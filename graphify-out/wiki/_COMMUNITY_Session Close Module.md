---
type: community
cohesion: 0.09
members: 34
---

# Session Close Module

**Cohesion:** 0.09 - loosely connected
**Members:** 34 nodes

## Members
- [[Append one row to decision-log.md, creating the file with header if absent.]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Build one sanitized pipe-delimited decision-log row from extracted data.      Wh]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Build pipeline-status.md content from current state and sprint review.      Why]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Build the Groq user message from current state.json data.      Why it exists Th]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Call GROQ_HEAVY_MODEL to extract structured JSON from sprint review prose.]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Call the Groq API and return the response text, or None on any failure.      Why]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Close-session command sprint review via Groq, writes session-log.md and STATE.m]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Load state.json and return the parsed dict, or None on any failure.      Why it]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Load the sprint-brain.md system prompt from the path declared in bricklayer.yaml]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Read LLM configuration from the llm section of bricklayer.yaml.      Why it exi]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Replace pipe characters with dashes so they cannot corrupt markdown tables.]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Return True if path is inside a git repository.      Why it exists Before runni]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Run git add  commit  push in DOCS_PATH to sync session docs to GitHub.      Wh]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Sprint review via Groq; write session-log.md, STATE.md, and sync VPS docs.]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Sync decision-log.md and pipeline-status.md to DOCS_PATH if set, then push.]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Write STATE.md with project name, current brick, and next command.      Why it e]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[Write session-log.md with brick status and Groq sprint review.      Why it exist]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_append_decision_log()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_build_decision_log_row()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_build_pipeline_status()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_build_user_message()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_call_groq()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_extract_structured_data()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_is_git_repo()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_load_sprint_brain()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_load_state()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_push_docs()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_read_llm_config()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_sanitize_pipe()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_sync_docs()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_write_session_log()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[_write_state_md()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[close_session.py]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py
- [[run_close_session()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/close_session.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Session_Close_Module
SORT file.name ASC
```
