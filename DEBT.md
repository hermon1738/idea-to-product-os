# bricklayer-cli — v2 Debt Register
> Tracked technical debt. Review before closing any phase.
> Items here are known limitations, not blocking bugs.

---

## Open Items

| ID | Component | Description | Logged | Priority |
|---|---|---|---|---|
| D-001 | runner.py | subprocess.TimeoutExpired unhandled — tool hang blocks CLI forever | Brick 16 | MEDIUM |
| D-002 | state.py | tmp.rename() PermissionError on Windows when another process holds state.json | Brick 16 | LOW |
| D-003 | branch.py / close_feature.py | Detached HEAD returns "HEAD" which bypasses startswith("feature/") prefix checks | Brick 16 | MEDIUM |
| D-004 | state.py | json.JSONDecodeError not caught on malformed state.json — raw traceback possible | Bricks 2/3/4 | MEDIUM |
| D-005 | build.py | "nothing to commit" blocks --verdict PASS on exploratory bricks with no file changes | Brick 8.5 | LOW |
| D-006 | config.py | Top-level YAML keys hardcoded — new sections added to bricklayer.yaml bypass validation silently | Brick 1 | LOW |
| D-007 | state.py | Schema validation won't scale — pydantic/dataclasses migration flagged | Brick 2 | LOW |
| D-008 | next.py | _ROUTING table hardcoded — should eventually be driven by bricklayer.yaml | Brick 4 | LOW |
| D-009 | make_skeptic_packet.py | git add errors swallowed silently — missing file in spec FILES list gives no warning | Brick 8.5 | LOW |
| D-010 | AGT-SYS-001 | Session Scribe is raw Python — no tool-calling, no memory, no scheduling. NanoBot upgrade planned. | Brick 16 | MEDIUM |
| D-011 | close_session.py | _extract_structured_data fallback is naive — if heavy model returns invalid JSON, defaults to generic values. Smarter retry or schema-enforced prompt needed. | Brick 18 | LOW |
| D-012 | close_session.py | response_format={"type":"json_object"} not used — JSON fence-stripping is brittle if model outputs prose before the code block | Brick 18 | LOW |
| D-013 | close_session.py | .exists() used instead of .is_dir() for DOCS_PATH check — silently fails if DOCS_PATH is a file, not a directory | Brick 18 | LOW |
| D-014 | new_project.py | Windows reserved names (CON, PRN, COM1, etc.) pass the name regex and will crash on mkdir — no platform check | Brick 19 | LOW |
| D-015 | new_project.py | No max name length validation — names over 255 chars will fail at OS level with no user-friendly error | Brick 19 | LOW |
| D-016 | new_project.py | Path separators in success output use os.sep — on Windows produces mixed slashes (context\projects\name/) | Brick 19 | LOW |
| D-017 | new_project.py | state.json schema lock-in — adding fields later requires migration command for all existing project state.json files | Brick 19 | LOW |
| D-018 | context.py | decision-log.md row parsing breaks if any data row contains "Date" in second column or uses non-standard table spacing | Brick 20 | LOW |
| D-019 | context.py | projects_dir not-empty check missing — empty context/projects/ dir falls through to "project not found" instead of "No projects found" | Brick 20 | LOW |
| D-020 | context.py | _resolve_project_name falls back to current_brick when project field absent — raw brick name without " - " separator used as project path, could produce unexpected resolution | Brick 20 | LOW |
| D-021 | registry.py | _write_atomic uses static .tmp suffix — concurrent add()/update_status() calls clobber the same temp file, corrupting the registry; fix: tempfile.NamedTemporaryFile | Brick 21 | HIGH |
| D-022 | registry.py | add() checks key presence only — empty string or None values pass REQUIRED_FIELDS validation; fix: check truthiness or type of each field value | Brick 21 | LOW |
| D-023 | registry.py | O(N) read-modify-write entire YAML file on every add()/update_status() — will cause contention at scale with many agents or frequent status updates | Brick 21 | LOW |
| D-024 | agent.py | Hardcoded column widths (_COL_ID=24, _COL_NAME=22) break table alignment for any agent with an ID or name longer than the column — no truncation or dynamic width fallback | Brick 22 | LOW |
| D-025 | agent.py | run_agent_status prints "Agent not found: <id>" when registry.yaml is missing — does not distinguish between "file absent" and "ID absent in existing registry" | Brick 22 | LOW |
| D-026 | agent.py | _TEMPLATE_FILES_TO_PATCH hardcodes 4 files — any new workspace/*.md files added to nanobot-template that contain __PLACEHOLDER__ tokens will not be patched | Brick 23 | LOW |
| D-027 | agent.py | shutil.copytree called without ignore= — .git/, .pyc, .DS_Store and other artifacts in nanobot-template are copied into every scaffolded agent directory | Brick 23 | LOW |
| D-028 | agent.py | _RAW_PYTHON_REQUIREMENTS hardcoded as string constant — updating pinned versions requires a code change rather than editing a standalone requirements template file | Brick 23 | LOW |
| D-029 | agent.py | git push failure leaves a dangling local commit in deploy repo — next successful deploy will push it bundled with the new commit | Brick 24 | MEDIUM |
| D-030 | agent.py | deploy prints --env-file ~/ai-agents/.env without verifying the file exists on VPS — missing .env causes container to start without secrets and fail silently | Brick 24 | LOW |
| D-031 | agent.py | deploy does not validate DEPLOY_REPO_PATH branch state — detached HEAD or feature branch causes git push to fail or push to wrong upstream | Brick 24 | MEDIUM |
| D-032 | agent.py | manual SSH "last mile" will bottleneck at scale — future bricklayer agent run-on-vps command should handle docker pull+run remotely | Brick 24 | LOW |
| D-033 | agent.py | subprocess.run(["git", ...]) raises FileNotFoundError if git is not in PATH — no catch for this; raw traceback reaches user in violation of "no raw traceback" rule | Brick 24 | MEDIUM |
| D-034 | agent.py | shutil.rmtree(target_dir) runs before shutil.copytree — if copytree fails (e.g. disk full), target_dir is permanently deleted with no rollback | Brick 24 | LOW |
| D-035 | agent.py | git add stages all files in agents/<id>/ but deploy repo may have other files already staged — unrelated staged changes bundled into the deployment commit | Brick 24 | LOW |
| D-036 | config.py | _load_dotenv inline parser has no support for multi-line values, variable expansion, or export prefix — edge cases like KEY="val with spaces" work only when the entire value is quoted | Brick 25 | LOW |
| D-037 | close_session.py | openai and anthropic provider support not yet implemented — provider: openai exits 1 with "not yet supported"; tracked for D-037 | Brick 25 | LOW |

## Closed Items
| ID | Description | Resolved In |
|---|---|---|
| — | — | — |
| D-038 | close_phase.py / close_feature.py | state_write crashes with ValueError if current_brick is null — merge succeeds but state update fails silently | Brick 25 area | MEDIUM |
