# Graph Report - .  (2026-04-14)

## Corpus Check
- 170 files · ~93,683 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 989 nodes · 968 edges · 220 communities detected
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 305 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `agent.py` - 14 edges
2. `Graph Report — 1597 Nodes / 2350 Edges / 93 Communities` - 12 edges
3. `main.py (CLI Entry Point)` - 12 edges
4. `main()` - 11 edges
5. `run_close_session()` - 10 edges
6. `idea-to-product-os Knowledge Graph Wiki Index` - 10 edges
7. `main()` - 9 edges
8. `_commit_and_merge()` - 8 edges
9. `_sync_docs()` - 8 edges
10. `run_agent_new()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Session Scribe Agent` --semantically_similar_to--> `Session Scribe Agent (agents/)`  [INFERRED] [semantically similar]
  context/decision-log.md → agents/README.md
- `Org Schema Formatter Agent` --semantically_similar_to--> `Org Schema Formatter Agent (agents/)`  [INFERRED] [semantically similar]
  context/decision-log.md → agents/README.md
- `Assignment Dispatcher Agent` --semantically_similar_to--> `Assignment Dispatcher Agent (agents/)`  [INFERRED] [semantically similar]
  context/decision-log.md → agents/README.md
- `Honest Agent Capabilities — What Agents Can and Cannot Do` --semantically_similar_to--> `Hard Stops — Agent Safety Rules`  [INFERRED] [semantically similar]
  docs/vision.md → agents/nanobot-template/workspace/AGENTS.md
- `Wiki: Plan-Brain Build Planning (Community 81)` --semantically_similar_to--> `Plan-Brain — Phase 4 Build Planning`  [INFERRED] [semantically similar]
  graphify-out/wiki/community-81-component-81.md → system-prompts/README.md

## Hyperedges (group relationships)
- **Bricklayer Build Sequence** — builder_command_sequence, make_skeptic_packet_script, skeptic_gate_checklist, skeptic_verdict_file, handover_md, context_txt_file [EXTRACTED 1.00]
- **Skeptic Gate Review Sections** — skeptic_gate_flaw_hunt, skeptic_gate_blind_spot, skeptic_gate_scaling_check, skeptic_gate_failure_first [EXTRACTED 1.00]
- **Live Agent Trio** — agents_session_scribe, agents_org_schema, agents_assignment_dispatcher [EXTRACTED 1.00]
- **Pipeline Entry Points Feed into Bricklayer Build Loop** — docs_workflow_entry_points, docs_workflow_build_loop, docs_workflow_full_pipeline_diagram [EXTRACTED 0.95]
- **Skeptic Gate — Checklist / AI Tool / Rule Form Independent Review** — wiki_community76_skeptic_gate, wiki_community92_skeptic_ai, system_prompts_readme_skeptic_rule [INFERRED 0.88]
- **NanoBot Template — Instructions, Tools, and Runtime Config** — agents_md_nanobot_agent_instructions, tools_md_nanobot_tool_usage, tools_md_groq_model_config [EXTRACTED 0.92]
- **Pause Session Handoff Flow: pause.py builds HANDOFF.json and .continue-here.md** — community30_pause_py, community30_build_handoff, community30_build_continue_md, community30_run_pause [EXTRACTED 0.95]
- **Bricklayer CLI Test Suite: test files covering all major bricklayer commands** — community11_test_pause_py, community26_test_next_py, community8_test_context_py, community25_test_status_py, community13_test_commit_py, community9_test_build_tools_py, community23_test_main_py [INFERRED 0.88]
- **Agent Scaffold Pipeline: agent_new triggers template resolution, placeholder mapping, and registry entry creation** — community14_agent_new, community14_build_placeholder_map, community14_build_registry_entry, community14_get_template_path [INFERRED 0.85]
- **CLI Branch Merge Pipeline (close_phase, close_feature, build merge)** — community42_run_close_phase, community41_run_close_feature, community19_merge_to_parent, community19_merge_branch_to [INFERRED 0.85]
- **Session Close Groq Sprint Review Pipeline** — community20_load_sprint_brain, community20_build_user_message, community20_call_groq, community20_extract_structured_data, community20_append_decision_log [INFERRED 0.85]
- **Bricklayer CLI Command Routing in main.py** — community22_main_py, community22_build, community22_close_feature, community22_close_phase, community22_close_session [EXTRACTED 0.90]
- **Verdict PASS Flow: has_pass_verdict → complete_brick → save_state** — community39_has_pass_verdict, community39_complete_brick, community39_save_state [INFERRED 0.85]
- **State Initialization: load → _validate + _make_default_state** — community31_load, community31_validate, community31_make_default_state [INFERRED 0.85]
- **File Scope Snapshot Verification: build_snapshot → sha256_for + snapshot_target_files** — community35_build_snapshot, community35_sha256_for, community35_snapshot_target_files [INFERRED 0.80]
- **Skeptic Packet Generation Pipeline** — community28_make_skeptic_packet, community28_parse_scoped_files, community28_write_diff_artifact, community28_write_scoped_files_bundle, community28_write_spec_copy, community28_write_state_excerpt, community28_write_test_output [EXTRACTED 0.95]
- **Resume Command Test Suite** — community21_test_resume, community21_cli_setup, community21_fake_git, community40_run_resume, community40_format_block, community40_get_current_branch [INFERRED 0.80]
- **Config Loader Resolution Chain** — community37_find_yaml, community37_load_and_validate, community37_load_dotenv, community37_write_context_txt [EXTRACTED 0.90]

## Communities

### Community 0 - "Skeptic Packet Tests"
Cohesion: 0.04
Nodes (46): _make_project() — test_build_skeptic, Rationale: Tests for Brick 7 revision bricklayer build skeptic-packet flag handler, test_build_skeptic.py, _cli_setup() — test_git_fixes, _load_make_skeptic_packet(), _make_project() — test_git_fixes, Rationale: Tests for Brick 8.5 auto-stage make_skeptic_packet.py and auto-commit run_verdict, test_git_fixes.py (+38 more)

### Community 1 - "Agent CLI Commands"
Cohesion: 0.06
Nodes (43): agent_deploy(), agent_list(), agent_live(), agent_new(), agent_status(), _build_placeholder_map(), _build_registry_entry(), _format_detail() (+35 more)

### Community 2 - "Build Command Tests"
Cohesion: 0.06
Nodes (40): _cli_invoke() (test_build), Rationale: Tests for build.py — bricklayer build (print contract), test_build.py (Build Command Tests), build.py (Build & Merge Module), _get_current_branch() (build), parse_spec(), Rationale: Build Command Pipeline Flag Routing, run_build() (+32 more)

### Community 3 - "Docs and Onboarding"
Cohesion: 0.06
Nodes (41): 7-Step Autonomous Build Sequence, Factory Mental Model (OS / Product / Warehouse), Full New Project Workflow (5 Stages), reddit-monitor — Example Project, Skeptic Review via Gemini, Three-Repo Structure (OS / Project / ai-agents), Install Bricklayer CLI (pip install -e .), Prerequisites — Getting Started (+33 more)

### Community 4 - "Build and Merge Module"
Cohesion: 0.08
Nodes (33): _commit_and_merge(), _get_current_branch(), _git_commit_spec(), _handle_fail_verdict(), _merge_branch_to(), _merge_to_parent(), _parse_brick_name(), parse_spec() (+25 more)

### Community 5 - "Session Close Module"
Cohesion: 0.09
Nodes (33): _append_decision_log(), _build_decision_log_row(), _build_pipeline_status(), _build_user_message(), _call_groq(), _extract_structured_data(), _is_git_repo(), _load_sprint_brain() (+25 more)

### Community 6 - "Main CLI Entry"
Cohesion: 0.07
Nodes (29): branch(), build(), close_feature(), close_phase(), close_session(), commit(), context(), new_project() (+21 more)

### Community 7 - "Pause and Resume Tests"
Cohesion: 0.09
Nodes (27): _cli_setup() [test_pause], _fake_git_branch(), _make_project() [test_pause], If .continue-here.md write fails, HANDOFF.json is cleaned up too, CliRunner: bricklayer pause exits 0, Tests for Brick 9 — bricklayer pause command, test_build_handoff_all_fields_present(), test_build_handoff_brick_number() (+19 more)

### Community 8 - "Skeptic Packet Tooling"
Cohesion: 0.14
Nodes (21): bricklayer/context.txt, TEST_COMMAND Config, graphify-out/ Directory, _get_git_root(), _git_add_spec_files(), is_git_repo(), main(), parse_scoped_files() (+13 more)

### Community 9 - "NanoBot Agent Config"
Cohesion: 0.1
Nodes (22): Hard Stops — Agent Safety Rules, Heartbeat Tasks Pattern, NanoBot Agent Instructions Template, bricklayer.yaml — Project Config File, context.txt — Auto-Generated from bricklayer.yaml, Known Issues and Fixes, state.json Bootstrap — Required Fields and Branch Prefix Format, Honest Agent Capabilities — What Agents Can and Cannot Do (+14 more)

### Community 10 - "Agent CLI Tests"
Cohesion: 0.13
Nodes (19): agent_deploy(), agent_list(), agent_live(), agent_new(), agent.py, agent_status(), _build_placeholder_map(), _build_registry_entry() (+11 more)

### Community 11 - "State Updater Tool"
Cohesion: 0.11
Nodes (19): append_handover(), complete_brick(), has_pass_verdict(), load_state(), main() (update_state), reject_completion(), save_state(), update_state.py (+11 more)

### Community 12 - "State Read Write Module"
Cohesion: 0.12
Nodes (20): load(), _make_default_state(), Load and validate state.json auto-creating with defaults if missing rationale, Build a valid default state dict for a fresh project rationale, state.json reader/writer with schema enforcement rationale, Raise ValueError if data does not satisfy the state schema rationale, state.py, _validate() (+12 more)

### Community 13 - "Session Close Tests"
Cohesion: 0.13
Nodes (15): _cli_setup() (test_close_session), _full_setup() (test_close_session), _mock_groq_success() (test_close_session), Rationale: Tests for Bricklayer close-session Command, test_close_session.py (Session Close Pipeline Tests), _call_groq(), close_session.py (Session Close Module), _load_sprint_brain() (+7 more)

### Community 14 - "Registry Module Tests"
Cohesion: 0.12
Nodes (9): _make_malformed_registry(), _make_registry(), Tests for Brick 21 — agent registry module rationale, Write a registry.yaml to tmp_path with the given agents rationale, test_registry.py, _make_malformed_registry() (agent_commands), _make_registry() (agent_commands), Tests for Brick 22 — agent list and status commands rationale (+1 more)

### Community 15 - "Agent Registry Module"
Cohesion: 0.23
Nodes (14): add(), get(), load(), Agent registry: read and write context/agents/registry.yaml.  WHY THIS EXISTS:, Return a single agent dict by ID, or None if not found.      Args:         root:, Append a new agent to the registry.      Validates required fields and checks fo, Update the status field of an existing agent.      Args:         root: Repo root, Read and parse registry.yaml, returning the raw dict.      Why it exists: Both l (+6 more)

### Community 16 - "Builder Rules and Prompts"
Cohesion: 0.13
Nodes (13): Required Command Sequence, Builder Rules (BUILDER.md), Brick Spec Template, Definition of Done, Bricklayer Roadmap (Planning Contract), PRD Template, Blind Spot Hunt Section, Skeptic Gate Checklist (+5 more)

### Community 17 - "Pause Module"
Cohesion: 0.2
Nodes (13): _build_continue_md(), _build_handoff(), _get_current_branch(), _next_command(), _parse_brick(), Pause command: write HANDOFF.json and .continue-here.md for session handoff.  WH, Resolve a next_action value to the CLI command the next session should run., Assemble the HANDOFF.json payload from state and git.      Why it exists: Assemb (+5 more)

### Community 18 - "Commit Command Tests"
Cohesion: 0.14
Nodes (12): _cli_setup() [test_commit], _make_project() [test_commit], _make_real_git_repo(), _mock_nothing_staged(), _mock_staged(), Integration: nothing staged — exit 1, Integration: real git repo — bricklayer commit creates a correctly tagged commit, Create a minimal real git repo for integration testing (+4 more)

### Community 19 - "State Module"
Cohesion: 0.23
Nodes (11): _deep_merge(), load(), _make_default_state(), state.json reader/writer with schema enforcement.  WHY THIS EXISTS:     state.js, Raise ValueError if data does not satisfy the state schema.      Why it exists:, Load and validate state.json, auto-creating it with defaults if missing.      Wh, Recursively merge updates into base; nested dicts are merged, not replaced., Deep-merge updates into state.json, validate, and persist atomically.      Why i (+3 more)

### Community 20 - "New Project Module"
Cohesion: 0.23
Nodes (11): _build_decision_log(), _build_state_json(), _build_state_md(), New-project command: scaffold context/projects/<name>/ with initial state files., Build initial state.json content for a new project.      Args:         name: Pro, Scaffold a new project directory with STATE.md, decision-log.md, state.json., Return an error message if name is invalid, else None.      Why it exists: Centr, Build initial STATE.md content for a new project.      Args:         name: Proje (+3 more)

### Community 21 - "Commit Module"
Cohesion: 0.23
Nodes (11): _build_message(), _check_staged(), _do_commit(), _parse_brick(), Commit command: git commit wrapper with auto-tagged brick ID message.  WHY THIS, Build the full conventional-commit message string.      Why it exists: The messa, Run ``git commit -m <message>`` and return (exit_code, output).      Why it exis, Commit staged files with an auto-tagged brick ID conventional-commit message. (+3 more)

### Community 22 - "Context Module"
Cohesion: 0.23
Nodes (11): _load_project_state(), Context command: print a compact project context block for AI session start.  WH, Extract "Next command:" value from STATE.md.      Why it exists: STATE.md is the, Return the project name to use, reading bricklayer/state.json if needed.      Wh, Print a compact context block for a project.      Why it exists: See module docs, Load and parse state.json from a project directory.      Why it exists: Centrali, Return the last n data rows from decision-log.md.      Why it exists: Only data, _read_last_decisions() (+3 more)

### Community 23 - "Context Command Tests"
Cohesion: 0.17
Nodes (8): _make_bricklayer_state(), _make_project() [test_context], Create a full project directory at context/projects/<name>/, Tests for Brick 20 — bricklayer context command, Write bricklayer/state.json with the given project field, Write a minimal bricklayer.yaml for CliRunner tests, _setup_repo() [test_context], test_context.py

### Community 24 - "Commit Module Tests"
Cohesion: 0.2
Nodes (12): _build_message(), _check_staged(), commit.py, _do_commit(), _parse_brick(), Rationale: Build the full conventional-commit message string, Rationale: Return a list of staged file paths empty list if nothing is staged or git fails, Rationale: Commit command git commit wrapper with auto-tagged brick ID message (+4 more)

### Community 25 - "Context Module Tests"
Cohesion: 0.2
Nodes (12): context.py, _load_project_state(), Rationale: Context command print compact project context block for AI session start, Rationale: Load and parse state.json from a project directory centralised, Rationale: Return the last n data rows from decision-log.md, Rationale: Extract Next command value from STATE.md, Rationale: Return the project name reading bricklayer/state.json if needed, Rationale: Print a compact context block for a project (+4 more)

### Community 26 - "File Scope Verifier"
Cohesion: 0.36
Nodes (10): build_snapshot(), has_git_repo(), main(), modified_files_git(), modified_files_snapshot(), parse_allowed_files(), read_snapshot(), sha256_for() (+2 more)

### Community 27 - "Status Command Tests"
Cohesion: 0.25
Nodes (11): _make_project() [test_status], Tests for cli/commands/status.py — bricklayer status command, test_happy_path_all_five_fields_printed(), test_happy_path_values_correct(), test_status.py, _parse_state_md(), Parse STATE.md into a key-value dict for run_status, Print five pipeline status fields to stdout from state.json (+3 more)

### Community 28 - "File Scope Verifier Tests"
Cohesion: 0.18
Nodes (6): build_snapshot(), main() (verify_files_touched), modified_files_git(), modified_files_snapshot(), parse_allowed_files(), verify_files_touched.py

### Community 29 - "Test Runner and Capture"
Cohesion: 0.38
Nodes (9): append_handover(), detect_missing_tool_from_output(), extract_failed_nodeids(), load_state(), main(), parse_test_command(), run_command(), save_state() (+1 more)

### Community 30 - "Component 30"
Cohesion: 0.27
Nodes (9): find_yaml(), load_and_validate(), _load_dotenv(), YAML loader and path validation for bricklayer.yaml.  WHY THIS EXISTS:     Every, Write bricklayer/context.txt from the test: section of bricklayer.yaml.      WHY, Load bricklayer.yaml, resolve all declared paths, exit 1 on any failure.      Wh, Load a .env file from directory into os.environ (non-overwriting).      Why it e, Walk upward from start until bricklayer.yaml is found.      Why it exists: Comma (+1 more)

### Community 31 - "Component 31"
Cohesion: 0.27
Nodes (9): _get_current_branch(), _git_create_checkout(), Branch command: create and checkout brick/phase/feature branches.  WHY THIS EXIS, Run ``git checkout -b <branch_name>`` and return (exit_code, output).      Why i, Create and checkout a branch at the correct hierarchy level.      Enforces the t, Convert a human-readable name to a lowercase-hyphenated git branch slug.      Wh, Return the current git branch name, or None if git fails or is absent.      Why, run_branch() (+1 more)

### Community 32 - "Component 32"
Cohesion: 0.24
Nodes (10): config.py, find_yaml(), load_and_validate(), _load_dotenv(), Rationale: YAML loader and path validation for bricklayer.yaml, Rationale: Walk upward from start until bricklayer.yaml is found, Rationale: Load bricklayer.yaml resolve all declared paths exit 1 on any failure, Rationale: Load a .env file from directory into os.environ non-overwriting (+2 more)

### Community 33 - "Component 33"
Cohesion: 0.22
Nodes (9): Assignment Dispatcher Agent (agents/), Org Schema Formatter Agent (agents/), Agents README, Session Scribe Agent (agents/), hermon1738/ai-agents GitHub Repo, Assignment Dispatcher Agent, Org Schema Formatter Agent, Session Scribe Agent (+1 more)

### Community 34 - "Component 34"
Cohesion: 0.22
Nodes (8): _cli_invoke() [test_build_tools], _make_project() [test_build_tools], run_snapshot returns 1 on non-zero tool exit, run_snapshot sets next_action to 'snapshot_init' on success, run_test returns 0 on tool exit 0, Tests for Brick 6 — bricklayer build --snapshot/--verify/--test flag handlers, run_verify returns 0 on tool exit 0, test_build_tools.py

### Community 35 - "Component 35"
Cohesion: 0.22
Nodes (8): _cli_setup() (three_level_branch), _fake_git_current(), _fake_run_tool(), Tests for Brick 14 — three-level branching (feature/phase/brick) rationale, Side-effect that returns the given branch for rev-parse calls rationale, Patch run_tool and get_tool_path so verdict can complete without real tools rationale, _read_state() (three_level_branch), test_three_level_branch.py

### Community 36 - "Component 36"
Cohesion: 0.54
Nodes (7): append_handover(), complete_brick(), has_pass_verdict(), load_state(), main(), reject_completion(), save_state()

### Community 37 - "Component 37"
Cohesion: 0.32
Nodes (7): _format_block(), _get_current_branch(), Resume command: read HANDOFF.json and print a formatted session context block., Read HANDOFF.json and print a formatted session context block.      Validates al, Return the current git branch name, or None if git fails or is absent.      Why, Format the handoff dict into the resume context block string.      Why it exists, run_resume()

### Community 38 - "Component 38"
Cohesion: 0.32
Nodes (7): _get_current_branch(), _merge_no_ff(), Close-feature command: merge current feature/* branch into main.  WHY THIS EXIST, Merge current feature/* branch into main and clear feature context.      Enforce, Return the current git branch name, or None if git fails or is absent.      Why, Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T, run_close_feature()

### Community 39 - "Component 39"
Cohesion: 0.32
Nodes (7): _get_current_branch(), _merge_no_ff(), Close-phase command: merge current phase/* branch into parent feature/* branch., Merge current phase/* branch into its parent feature/* branch.      Reads the me, Return the current git branch name, or None if git fails or is absent.      Why, Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T, run_close_phase()

### Community 40 - "Component 40"
Cohesion: 0.29
Nodes (7): _cli_deploy() (test_agent_deploy), _git_success() (test_agent_deploy), _make_agent_dir() (test_agent_deploy), _make_deploy_repo() (test_agent_deploy), _make_registry() (test_agent_deploy), Rationale: Tests for Agent Deploy and Agent Live Commands, test_agent_deploy.py (Agent Deploy Command Tests)

### Community 41 - "Component 41"
Cohesion: 0.38
Nodes (5): _git(), _make_feature_repo(), _make_phase_repo(), Tests for Brick 26 fixes — null current_brick on close-phase/close-feature rationale, test_close_phase_fix.py

### Community 42 - "Component 42"
Cohesion: 0.33
Nodes (5): get_tool_path(), Shared tool invocation and output capture for bricklayer build flags.  WHY THIS, Run ``python3 tool_path [args]`` and return (exit_code, combined_output).      W, Resolve a named tool entry from bricklayer.yaml config to an absolute Path., run_tool()

### Community 43 - "Component 43"
Cohesion: 0.4
Nodes (5): _parse_state_md(), Status command: print current brick, last test result, and next action.  WHY THI, Parse STATE.md into a key → value dict.      Why it exists: run_status needs pro, Print five pipeline status fields to stdout.      Combines data from state.json, run_status()

### Community 44 - "Component 44"
Cohesion: 0.33
Nodes (4): _make_file() [test_main], CliRunner integration tests for cli/main.py, test_main.py, _write_yaml() [test_main]

### Community 45 - "Component 45"
Cohesion: 0.33
Nodes (2): _commit_and_merge(), _merge_to_parent()

### Community 46 - "Component 46"
Cohesion: 0.4
Nodes (3): Rationale: Automatic context.txt Generation from bricklayer.yaml, _read_context() (test_config_write), test_config_write.py

### Community 47 - "Component 47"
Cohesion: 0.4
Nodes (2): Rationale: Tests for state.json Reader/Writer, test_state.py (State Module Tests)

### Community 48 - "Component 48"
Cohesion: 0.5
Nodes (3): Next command: read next_action from state.json and print the next CLI command., Read next_action from state.json and print the corresponding CLI command.      W, run_next()

### Community 49 - "Component 49"
Cohesion: 0.67
Nodes (4): main() [print_brick_contract], print_brick_contract.py, section_lines(), spec.md — Active Brick Contract

### Community 50 - "Component 50"
Cohesion: 0.5
Nodes (4): _build_continue_md(), Build the .continue-here.md content from the handoff dict, Write HANDOFF.json and .continue-here.md; rolls back HANDOFF on second write failure, run_pause()

### Community 51 - "Component 51"
Cohesion: 0.5
Nodes (4): next.py, Next command: read next_action from state.json and print the next CLI command rationale, Read next_action from state.json and print the corresponding CLI command rationale, run_next()

### Community 52 - "Component 52"
Cohesion: 0.5
Nodes (4): _deep_merge(), Recursively merge updates into base rationale, Deep-merge updates into state.json validate and persist atomically rationale, write()

### Community 53 - "Component 53"
Cohesion: 1.0
Nodes (2): main(), section_lines()

### Community 54 - "Component 54"
Cohesion: 0.67
Nodes (3): Context Decision Log (Pipeline History), Context README (Living Memory), Hetzner VPS Deployment

### Community 55 - "Component 55"
Cohesion: 0.67
Nodes (3): skeptic_verdict.md — Verdict File (Tony Writes Only), Tony — Human Co-CEO & Decision Maker, Session Scribe Agent — AGT-SYS-001

### Community 56 - "Component 56"
Cohesion: 0.67
Nodes (2): _push_docs(), Hetzner VPS — Live Infrastructure

### Community 57 - "Component 57"
Cohesion: 1.0
Nodes (1): Bricklayer CLI package.  WHY THIS EXISTS:     This file marks the cli/ directory

### Community 58 - "Component 58"
Cohesion: 1.0
Nodes (2): bricklayer/handover.md, skeptic_packet/test_output.txt

### Community 59 - "Component 59"
Cohesion: 1.0
Nodes (2): Nanobot USER.md (Tony Profile), Tony (Human Co-CEO Operator)

### Community 60 - "Component 60"
Cohesion: 1.0
Nodes (2): Nanobot Template Requirements, Nanobot Template

### Community 61 - "Component 61"
Cohesion: 1.0
Nodes (1): CliRunner: both HANDOFF.json and .continue-here.md are written

### Community 62 - "Component 62"
Cohesion: 1.0
Nodes (1): CliRunner: .continue-here.md contains all required lines

### Community 63 - "Component 63"
Cohesion: 1.0
Nodes (1): CliRunner: HANDOFF.json contains all 8 fields with correct values

### Community 64 - "Component 64"
Cohesion: 1.0
Nodes (2): Error output mentions state.json and contains no raw traceback, test_missing_state_json_clear_error() [next]

### Community 65 - "Component 65"
Cohesion: 1.0
Nodes (2): run_next() auto-creates state.json and exits 0 when file is absent, test_missing_state_json_autocreates() [next]

### Community 66 - "Component 66"
Cohesion: 1.0
Nodes (1): run command exits 1 when a yaml path is missing

### Community 67 - "Component 67"
Cohesion: 1.0
Nodes (1): Missing path error output must not show a Python traceback

### Community 68 - "Component 68"
Cohesion: 1.0
Nodes (2): When state.json is absent, run_status() auto-creates it and exits 0, test_missing_state_json_autocreates() [status]

### Community 69 - "Component 69"
Cohesion: 1.0
Nodes (2): /run-brick Skill — Autonomous Build Trigger, Pipeline Reference

### Community 70 - "Component 70"
Cohesion: 1.0
Nodes (2): plan-brain — Brick Planning from Architecture, Autonomous Build Mode — 7-Step Build Sequence

### Community 71 - "Component 71"
Cohesion: 1.0
Nodes (0): 

### Community 72 - "Component 72"
Cohesion: 1.0
Nodes (2): CODEX.md — Codex Entry Point, Builder AI — Claude Code / Codex

### Community 73 - "Component 73"
Cohesion: 1.0
Nodes (2): arch-brain — Architecture Session, Architecture Doc

### Community 74 - "Component 74"
Cohesion: 1.0
Nodes (2): cli/__init__.py, Bricklayer CLI package rationale

### Community 75 - "Component 75"
Cohesion: 1.0
Nodes (1): Return a side_effect list for sequential subprocess.run calls rationale

### Community 76 - "Component 76"
Cohesion: 1.0
Nodes (1): Side-effect: checkout succeeds subsequent calls succeed rationale

### Community 77 - "Component 77"
Cohesion: 1.0
Nodes (2): Agent-OS — AI Layer Design (README), Agent-OS — AI Layer Design

### Community 78 - "Component 78"
Cohesion: 1.0
Nodes (2): README.md — Idea-to-Product OS Overview, Bricklayer CLI

### Community 79 - "Component 79"
Cohesion: 1.0
Nodes (2): state.json — Bricklayer Runtime State, State JSON Schema

### Community 80 - "Component 80"
Cohesion: 1.0
Nodes (2): CLAUDE.md — Claude Code Session Entry Point, INTAKE — Project Brief SOP

### Community 81 - "Component 81"
Cohesion: 1.0
Nodes (1): AGENT.md — AI Tool Entry Point

### Community 82 - "Component 82"
Cohesion: 1.0
Nodes (1): skeptic_verdict.md — Verdict File (Tony Writes Only)

### Community 83 - "Component 83"
Cohesion: 1.0
Nodes (1): Tony — Human Co-CEO & Decision Maker

### Community 84 - "Component 84"
Cohesion: 1.0
Nodes (1): Autonomous Build Mode — 7-Step Build Sequence

### Community 85 - "Component 85"
Cohesion: 1.0
Nodes (1): stack-rules.md — Engineering Standards

### Community 86 - "Component 86"
Cohesion: 1.0
Nodes (1): Engineering Standards — Code Quality Rules

### Community 87 - "Component 87"
Cohesion: 1.0
Nodes (1): Project STATE.md

### Community 88 - "Component 88"
Cohesion: 1.0
Nodes (0): 

### Community 89 - "Component 89"
Cohesion: 1.0
Nodes (1): README.md — Idea-to-Product OS Overview

### Community 90 - "Component 90"
Cohesion: 1.0
Nodes (1): Idea-to-Product Pipeline — 7-Phase System

### Community 91 - "Component 91"
Cohesion: 1.0
Nodes (1): Bricklayer CLI

### Community 92 - "Component 92"
Cohesion: 1.0
Nodes (1): Session Scribe Agent — AGT-SYS-001

### Community 93 - "Component 93"
Cohesion: 1.0
Nodes (1): Venture OS — Idea Stress-Test & Org Schema

### Community 94 - "Component 94"
Cohesion: 1.0
Nodes (1): arch-brain — Architecture Session

### Community 95 - "Component 95"
Cohesion: 1.0
Nodes (1): Agent-OS — AI Layer Design

### Community 96 - "Component 96"
Cohesion: 1.0
Nodes (1): plan-brain — Brick Planning from Architecture

### Community 97 - "Component 97"
Cohesion: 1.0
Nodes (1): sprint-brain — Post-Brick Sprint Review

### Community 98 - "Component 98"
Cohesion: 1.0
Nodes (1): CODEX.md — Codex Entry Point

### Community 99 - "Component 99"
Cohesion: 1.0
Nodes (1): CLAUDE.md — Claude Code Session Entry Point

### Community 100 - "Component 100"
Cohesion: 1.0
Nodes (1): /run-brick Skill — Autonomous Build Trigger

### Community 101 - "Component 101"
Cohesion: 1.0
Nodes (1): NanoBot — Agent Template with Memory & Tool-Calling

### Community 102 - "Component 102"
Cohesion: 1.0
Nodes (1): Hetzner VPS — Live Infrastructure

### Community 103 - "Component 103"
Cohesion: 1.0
Nodes (1): Loop Stop Rule — max 3 loops before rescope

### Community 104 - "Component 104"
Cohesion: 1.0
Nodes (1): Brick — Scoped Unit of Work

### Community 105 - "Component 105"
Cohesion: 1.0
Nodes (1): spec.md — Active Brick Contract

### Community 106 - "Component 106"
Cohesion: 1.0
Nodes (1): state.json — Bricklayer Runtime State

### Community 107 - "Component 107"
Cohesion: 1.0
Nodes (1): update_state.py — State Advancement Tool

### Community 108 - "Component 108"
Cohesion: 1.0
Nodes (1): Skeptic Gate — Independent AI Review

### Community 109 - "Component 109"
Cohesion: 1.0
Nodes (1): INTAKE — Project Brief SOP

### Community 110 - "Component 110"
Cohesion: 1.0
Nodes (1): BRICK 2.3: Discord UX

### Community 111 - "Component 111"
Cohesion: 1.0
Nodes (1): State JSON Schema

### Community 112 - "Component 112"
Cohesion: 1.0
Nodes (1): Stack Rules — Idea-to-Product OS

### Community 113 - "Component 113"
Cohesion: 1.0
Nodes (1): Docker CE — Agent Container Runtime

### Community 114 - "Component 114"
Cohesion: 1.0
Nodes (1): Groq LLM Stack

### Community 115 - "Component 115"
Cohesion: 1.0
Nodes (1): Sprint-Brain — Sprint Review Mode

### Community 116 - "Component 116"
Cohesion: 1.0
Nodes (1): Venture OS — Strategy Layer

### Community 117 - "Component 117"
Cohesion: 1.0
Nodes (1): Org Schema — Software Architecture Document

### Community 118 - "Component 118"
Cohesion: 1.0
Nodes (1): Arch-Brain — Architecture Session

### Community 119 - "Component 119"
Cohesion: 1.0
Nodes (1): Plan-Brain — Build Planning Mode

### Community 120 - "Component 120"
Cohesion: 1.0
Nodes (1): Agent-OS — AI Layer Design

### Community 121 - "Component 121"
Cohesion: 1.0
Nodes (1): Framework Decision Gate — RAW PYTHON vs NANOBOT

### Community 122 - "Component 122"
Cohesion: 1.0
Nodes (1): Raw Python Agent Runtime

### Community 123 - "Component 123"
Cohesion: 1.0
Nodes (1): Pipeline Reference

### Community 124 - "Component 124"
Cohesion: 1.0
Nodes (1): Architecture Doc

### Community 125 - "Component 125"
Cohesion: 1.0
Nodes (1): Builder AI — Claude Code / Codex

### Community 126 - "Component 126"
Cohesion: 1.0
Nodes (1): Skeptic AI — GPT-4 / Gemini

### Community 127 - "Component 127"
Cohesion: 1.0
Nodes (1): LANGUAGE Config (Python)

### Community 128 - "Component 128"
Cohesion: 1.0
Nodes (1): Test Gate Records

### Community 129 - "Component 129"
Cohesion: 1.0
Nodes (1): Completion Gate Records

### Community 130 - "Component 130"
Cohesion: 1.0
Nodes (1): Builder Hard Rules

### Community 131 - "Component 131"
Cohesion: 1.0
Nodes (1): Loop Stop Condition (loop_count >= 3)

### Community 132 - "Component 132"
Cohesion: 1.0
Nodes (1): Co-Dev Roles (Builder / Skeptic)

### Community 133 - "Component 133"
Cohesion: 1.0
Nodes (1): Decision Log (root)

### Community 134 - "Component 134"
Cohesion: 1.0
Nodes (1): v2 Debt — config.py Hardcoded YAML Keys

### Community 135 - "Component 135"
Cohesion: 1.0
Nodes (1): Session Log

### Community 136 - "Component 136"
Cohesion: 1.0
Nodes (1): Brick 1 — CLI Scaffold + YAML Loader + Startup Validation

### Community 137 - "Component 137"
Cohesion: 1.0
Nodes (1): Brick 25 — auto-.env loading + LLM config

### Community 138 - "Component 138"
Cohesion: 1.0
Nodes (1): Brick 26 — null state fields + missing state.json

### Community 139 - "Component 139"
Cohesion: 1.0
Nodes (1): Brick 27 — Fix close-session prompt quality

### Community 140 - "Component 140"
Cohesion: 1.0
Nodes (1): Brick 28 — Auto-push docs after close-session

### Community 141 - "Component 141"
Cohesion: 1.0
Nodes (1): pipeline-status.md (VPS Source of Truth)

### Community 142 - "Component 142"
Cohesion: 1.0
Nodes (1): Memory: --dangerously-skip-permissions Meaning

### Community 143 - "Component 143"
Cohesion: 1.0
Nodes (1): Known Version Pins (groq/httpx/discord.py)

### Community 144 - "Component 144"
Cohesion: 1.0
Nodes (1): Nanobot HEARTBEAT.md

### Community 145 - "Component 145"
Cohesion: 1.0
Nodes (1): Nanobot SOUL.md (Agent Identity)

### Community 146 - "Component 146"
Cohesion: 1.0
Nodes (1): groq/httpx Version Conflict Fix

### Community 147 - "Component 147"
Cohesion: 1.0
Nodes (0): 

### Community 148 - "Component 148"
Cohesion: 1.0
Nodes (0): 

### Community 149 - "Component 149"
Cohesion: 1.0
Nodes (0): 

### Community 150 - "Component 150"
Cohesion: 1.0
Nodes (1): test_cli_runner_missing_state_json_autocreates() [next]

### Community 151 - "Component 151"
Cohesion: 1.0
Nodes (0): 

### Community 152 - "Component 152"
Cohesion: 1.0
Nodes (0): 

### Community 153 - "Component 153"
Cohesion: 1.0
Nodes (0): 

### Community 154 - "Component 154"
Cohesion: 1.0
Nodes (0): 

### Community 155 - "Component 155"
Cohesion: 1.0
Nodes (0): 

### Community 156 - "Component 156"
Cohesion: 1.0
Nodes (0): 

### Community 157 - "Component 157"
Cohesion: 1.0
Nodes (0): 

### Community 158 - "Component 158"
Cohesion: 1.0
Nodes (0): 

### Community 159 - "Component 159"
Cohesion: 1.0
Nodes (0): 

### Community 160 - "Component 160"
Cohesion: 1.0
Nodes (0): 

### Community 161 - "Component 161"
Cohesion: 1.0
Nodes (1): test_cli_runner_missing_state_json_autocreates() [status]

### Community 162 - "Component 162"
Cohesion: 1.0
Nodes (1): test_missing_state_json_clear_error() [status]

### Community 163 - "Component 163"
Cohesion: 1.0
Nodes (0): 

### Community 164 - "Component 164"
Cohesion: 1.0
Nodes (0): 

### Community 165 - "Component 165"
Cohesion: 1.0
Nodes (1): Engineering Standards — Code Quality Rules

### Community 166 - "Component 166"
Cohesion: 1.0
Nodes (0): 

### Community 167 - "Component 167"
Cohesion: 1.0
Nodes (0): 

### Community 168 - "Component 168"
Cohesion: 1.0
Nodes (0): 

### Community 169 - "Component 169"
Cohesion: 1.0
Nodes (1): pause() CLI command

### Community 170 - "Component 170"
Cohesion: 1.0
Nodes (1): resume() CLI command

### Community 171 - "Component 171"
Cohesion: 1.0
Nodes (1): run() CLI command

### Community 172 - "Component 172"
Cohesion: 1.0
Nodes (1): DEBT.md — Technical Debt Register

### Community 173 - "Component 173"
Cohesion: 1.0
Nodes (0): 

### Community 174 - "Component 174"
Cohesion: 1.0
Nodes (0): 

### Community 175 - "Component 175"
Cohesion: 1.0
Nodes (0): 

### Community 176 - "Component 176"
Cohesion: 1.0
Nodes (0): 

### Community 177 - "Component 177"
Cohesion: 1.0
Nodes (0): 

### Community 178 - "Component 178"
Cohesion: 1.0
Nodes (0): 

### Community 179 - "Component 179"
Cohesion: 1.0
Nodes (0): 

### Community 180 - "Component 180"
Cohesion: 1.0
Nodes (0): 

### Community 181 - "Component 181"
Cohesion: 1.0
Nodes (0): 

### Community 182 - "Component 182"
Cohesion: 1.0
Nodes (0): 

### Community 183 - "Component 183"
Cohesion: 1.0
Nodes (0): 

### Community 184 - "Component 184"
Cohesion: 1.0
Nodes (0): 

### Community 185 - "Component 185"
Cohesion: 1.0
Nodes (0): 

### Community 186 - "Component 186"
Cohesion: 1.0
Nodes (0): 

### Community 187 - "Component 187"
Cohesion: 1.0
Nodes (0): 

### Community 188 - "Component 188"
Cohesion: 1.0
Nodes (0): 

### Community 189 - "Component 189"
Cohesion: 1.0
Nodes (0): 

### Community 190 - "Component 190"
Cohesion: 1.0
Nodes (0): 

### Community 191 - "Component 191"
Cohesion: 1.0
Nodes (1): Venture OS — Strategy Layer

### Community 192 - "Component 192"
Cohesion: 1.0
Nodes (1): _git_failure() (test_agent_deploy)

### Community 193 - "Component 193"
Cohesion: 1.0
Nodes (0): 

### Community 194 - "Component 194"
Cohesion: 1.0
Nodes (0): 

### Community 195 - "Component 195"
Cohesion: 1.0
Nodes (0): 

### Community 196 - "Component 196"
Cohesion: 1.0
Nodes (0): 

### Community 197 - "Component 197"
Cohesion: 1.0
Nodes (0): 

### Community 198 - "Component 198"
Cohesion: 1.0
Nodes (0): 

### Community 199 - "Component 199"
Cohesion: 1.0
Nodes (0): 

### Community 200 - "Component 200"
Cohesion: 1.0
Nodes (1): PASS returns 1 when update_state tool exits non-zero rationale

### Community 201 - "Component 201"
Cohesion: 1.0
Nodes (1): Brick — Scoped Unit of Work

### Community 202 - "Component 202"
Cohesion: 1.0
Nodes (0): 

### Community 203 - "Component 203"
Cohesion: 1.0
Nodes (0): 

### Community 204 - "Component 204"
Cohesion: 1.0
Nodes (0): 

### Community 205 - "Component 205"
Cohesion: 1.0
Nodes (1): NanoBot — Agent Template with Memory & Tool-Calling

### Community 206 - "Component 206"
Cohesion: 1.0
Nodes (1): Raw Python Agent Runtime

### Community 207 - "Component 207"
Cohesion: 1.0
Nodes (1): Org Schema — Software Architecture Document

### Community 208 - "Component 208"
Cohesion: 1.0
Nodes (1): AGENT.md — AI Tool Entry Point

### Community 209 - "Component 209"
Cohesion: 1.0
Nodes (0): 

### Community 210 - "Component 210"
Cohesion: 1.0
Nodes (0): 

### Community 211 - "Component 211"
Cohesion: 1.0
Nodes (0): 

### Community 212 - "Component 212"
Cohesion: 1.0
Nodes (0): 

### Community 213 - "Component 213"
Cohesion: 1.0
Nodes (0): 

### Community 214 - "Component 214"
Cohesion: 1.0
Nodes (0): 

### Community 215 - "Component 215"
Cohesion: 1.0
Nodes (0): 

### Community 216 - "Component 216"
Cohesion: 1.0
Nodes (1): Arch-Brain — Architecture Session

### Community 217 - "Component 217"
Cohesion: 1.0
Nodes (0): 

### Community 218 - "Component 218"
Cohesion: 1.0
Nodes (0): 

### Community 219 - "Component 219"
Cohesion: 1.0
Nodes (1): Docker CE — Agent Container Runtime

## Knowledge Gaps
- **437 isolated node(s):** `Read TEST_COMMAND from context.txt and return as argv list.      Why it exists:`, `Return the absolute repo root, or None if not in a git repo.`, `Stage all spec FILES in the git index before building the packet.`, `Copy graph audit artifacts into skeptic_packet and emit a presence manifest.`, `Shared tool invocation and output capture for bricklayer build flags.  WHY THIS` (+432 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Component 57`** (2 nodes): `__init__.py`, `Bricklayer CLI package.  WHY THIS EXISTS:     This file marks the cli/ directory`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 58`** (2 nodes): `bricklayer/handover.md`, `skeptic_packet/test_output.txt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 59`** (2 nodes): `Nanobot USER.md (Tony Profile)`, `Tony (Human Co-CEO Operator)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 60`** (2 nodes): `Nanobot Template Requirements`, `Nanobot Template`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 61`** (2 nodes): `CliRunner: both HANDOFF.json and .continue-here.md are written`, `test_cli_pause_writes_both_files()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 62`** (2 nodes): `CliRunner: .continue-here.md contains all required lines`, `test_cli_pause_continue_md_correct_content()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 63`** (2 nodes): `CliRunner: HANDOFF.json contains all 8 fields with correct values`, `test_cli_pause_handoff_json_correct_content()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 64`** (2 nodes): `Error output mentions state.json and contains no raw traceback`, `test_missing_state_json_clear_error() [next]`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 65`** (2 nodes): `run_next() auto-creates state.json and exits 0 when file is absent`, `test_missing_state_json_autocreates() [next]`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 66`** (2 nodes): `run command exits 1 when a yaml path is missing`, `test_run_command_missing_path_exits_1()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 67`** (2 nodes): `Missing path error output must not show a Python traceback`, `test_run_command_missing_path_no_traceback()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 68`** (2 nodes): `When state.json is absent, run_status() auto-creates it and exits 0`, `test_missing_state_json_autocreates() [status]`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 69`** (2 nodes): `/run-brick Skill — Autonomous Build Trigger`, `Pipeline Reference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 70`** (2 nodes): `plan-brain — Brick Planning from Architecture`, `Autonomous Build Mode — 7-Step Build Sequence`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 71`** (2 nodes): `_build_decision_log_row()`, `_build_pipeline_status()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 72`** (2 nodes): `CODEX.md — Codex Entry Point`, `Builder AI — Claude Code / Codex`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 73`** (2 nodes): `arch-brain — Architecture Session`, `Architecture Doc`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 74`** (2 nodes): `cli/__init__.py`, `Bricklayer CLI package rationale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 75`** (2 nodes): `Return a side_effect list for sequential subprocess.run calls rationale`, `_subprocess_side_effects()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 76`** (2 nodes): `_fake_checkout_ok()`, `Side-effect: checkout succeeds subsequent calls succeed rationale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 77`** (2 nodes): `Agent-OS — AI Layer Design (README)`, `Agent-OS — AI Layer Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 78`** (2 nodes): `README.md — Idea-to-Product OS Overview`, `Bricklayer CLI`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 79`** (2 nodes): `state.json — Bricklayer Runtime State`, `State JSON Schema`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 80`** (2 nodes): `CLAUDE.md — Claude Code Session Entry Point`, `INTAKE — Project Brief SOP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 81`** (1 nodes): `AGENT.md — AI Tool Entry Point`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 82`** (1 nodes): `skeptic_verdict.md — Verdict File (Tony Writes Only)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 83`** (1 nodes): `Tony — Human Co-CEO & Decision Maker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 84`** (1 nodes): `Autonomous Build Mode — 7-Step Build Sequence`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 85`** (1 nodes): `stack-rules.md — Engineering Standards`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 86`** (1 nodes): `Engineering Standards — Code Quality Rules`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 87`** (1 nodes): `Project STATE.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 88`** (1 nodes): `DEBT.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 89`** (1 nodes): `README.md — Idea-to-Product OS Overview`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 90`** (1 nodes): `Idea-to-Product Pipeline — 7-Phase System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 91`** (1 nodes): `Bricklayer CLI`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 92`** (1 nodes): `Session Scribe Agent — AGT-SYS-001`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 93`** (1 nodes): `Venture OS — Idea Stress-Test & Org Schema`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 94`** (1 nodes): `arch-brain — Architecture Session`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 95`** (1 nodes): `Agent-OS — AI Layer Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 96`** (1 nodes): `plan-brain — Brick Planning from Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 97`** (1 nodes): `sprint-brain — Post-Brick Sprint Review`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 98`** (1 nodes): `CODEX.md — Codex Entry Point`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 99`** (1 nodes): `CLAUDE.md — Claude Code Session Entry Point`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 100`** (1 nodes): `/run-brick Skill — Autonomous Build Trigger`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 101`** (1 nodes): `NanoBot — Agent Template with Memory & Tool-Calling`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 102`** (1 nodes): `Hetzner VPS — Live Infrastructure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 103`** (1 nodes): `Loop Stop Rule — max 3 loops before rescope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 104`** (1 nodes): `Brick — Scoped Unit of Work`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 105`** (1 nodes): `spec.md — Active Brick Contract`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 106`** (1 nodes): `state.json — Bricklayer Runtime State`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 107`** (1 nodes): `update_state.py — State Advancement Tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 108`** (1 nodes): `Skeptic Gate — Independent AI Review`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 109`** (1 nodes): `INTAKE — Project Brief SOP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 110`** (1 nodes): `BRICK 2.3: Discord UX`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 111`** (1 nodes): `State JSON Schema`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 112`** (1 nodes): `Stack Rules — Idea-to-Product OS`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 113`** (1 nodes): `Docker CE — Agent Container Runtime`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 114`** (1 nodes): `Groq LLM Stack`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 115`** (1 nodes): `Sprint-Brain — Sprint Review Mode`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 116`** (1 nodes): `Venture OS — Strategy Layer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 117`** (1 nodes): `Org Schema — Software Architecture Document`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 118`** (1 nodes): `Arch-Brain — Architecture Session`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 119`** (1 nodes): `Plan-Brain — Build Planning Mode`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 120`** (1 nodes): `Agent-OS — AI Layer Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 121`** (1 nodes): `Framework Decision Gate — RAW PYTHON vs NANOBOT`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 122`** (1 nodes): `Raw Python Agent Runtime`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 123`** (1 nodes): `Pipeline Reference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 124`** (1 nodes): `Architecture Doc`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 125`** (1 nodes): `Builder AI — Claude Code / Codex`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 126`** (1 nodes): `Skeptic AI — GPT-4 / Gemini`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 127`** (1 nodes): `LANGUAGE Config (Python)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 128`** (1 nodes): `Test Gate Records`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 129`** (1 nodes): `Completion Gate Records`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 130`** (1 nodes): `Builder Hard Rules`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 131`** (1 nodes): `Loop Stop Condition (loop_count >= 3)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 132`** (1 nodes): `Co-Dev Roles (Builder / Skeptic)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 133`** (1 nodes): `Decision Log (root)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 134`** (1 nodes): `v2 Debt — config.py Hardcoded YAML Keys`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 135`** (1 nodes): `Session Log`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 136`** (1 nodes): `Brick 1 — CLI Scaffold + YAML Loader + Startup Validation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 137`** (1 nodes): `Brick 25 — auto-.env loading + LLM config`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 138`** (1 nodes): `Brick 26 — null state fields + missing state.json`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 139`** (1 nodes): `Brick 27 — Fix close-session prompt quality`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 140`** (1 nodes): `Brick 28 — Auto-push docs after close-session`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 141`** (1 nodes): `pipeline-status.md (VPS Source of Truth)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 142`** (1 nodes): `Memory: --dangerously-skip-permissions Meaning`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 143`** (1 nodes): `Known Version Pins (groq/httpx/discord.py)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 144`** (1 nodes): `Nanobot HEARTBEAT.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 145`** (1 nodes): `Nanobot SOUL.md (Agent Identity)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 146`** (1 nodes): `groq/httpx Version Conflict Fix`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 147`** (1 nodes): `_sample_handoff()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 148`** (1 nodes): `test_build_continue_md_contains_all_required_lines()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 149`** (1 nodes): `test_cli_runner_known_state_correct_output()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 150`** (1 nodes): `test_cli_runner_missing_state_json_autocreates() [next]`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 151`** (1 nodes): `test_cli_context_output_has_all_six_sections()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 152`** (1 nodes): `test_cli_context_project_not_found_exits_one()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 153`** (1 nodes): `test_read_last_decisions_returns_last_3()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 154`** (1 nodes): `_setup_close_session_project()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 155`** (1 nodes): `test_help_no_traceback()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 156`** (1 nodes): `test_help_shows_commands()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 157`** (1 nodes): `test_run_command_no_yaml_exits_1()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 158`** (1 nodes): `test_close_session_loads_env_file_and_uses_llm_config()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 159`** (1 nodes): `test_close_session_api_key_env_unset_exits_1_with_clear_message()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 160`** (1 nodes): `test_cli_runner_happy_path()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 161`** (1 nodes): `test_cli_runner_missing_state_json_autocreates() [status]`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 162`** (1 nodes): `test_missing_state_json_clear_error() [status]`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 163`** (1 nodes): `test_missing_state_md_exits_zero()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 164`** (1 nodes): `test_missing_state_md_fallback_message()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 165`** (1 nodes): `Engineering Standards — Code Quality Rules`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 166`** (1 nodes): `test_build_message_subject_format()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 167`** (1 nodes): `test_build_message_body_contains_brick_line()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 168`** (1 nodes): `test_check_staged_returns_files()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 169`** (1 nodes): `pause() CLI command`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 170`** (1 nodes): `resume() CLI command`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 171`** (1 nodes): `run() CLI command`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 172`** (1 nodes): `DEBT.md — Technical Debt Register`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 173`** (1 nodes): `test_creates_bricklayer_directory_if_missing()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 174`** (1 nodes): `test_language_defaults_to_python_if_omitted()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 175`** (1 nodes): `test_missing_command_field_exits_with_error()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 176`** (1 nodes): `test_missing_test_section_leaves_existing_context_unchanged()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 177`** (1 nodes): `test_missing_test_section_no_existing_context_does_not_create_file()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 178`** (1 nodes): `test_overwrites_existing_context_txt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 179`** (1 nodes): `test_write_is_atomic()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 180`** (1 nodes): `_handle_fail_verdict()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 181`** (1 nodes): `run_skeptic_packet()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 182`** (1 nodes): `_append_decision_log()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 183`** (1 nodes): `test_load_autocreate_creates_file_on_disk()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 184`** (1 nodes): `test_load_autocreate_default_current_brick_is_empty_string()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 185`** (1 nodes): `test_load_autocreate_is_idempotent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 186`** (1 nodes): `test_load_autocreate_passes_schema_validation()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 187`** (1 nodes): `test_load_autocreate_prints_warning_to_stderr()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 188`** (1 nodes): `test_load_autocreate_project_name_from_repo_root()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 189`** (1 nodes): `test_load_autocreate_returns_valid_dict()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 190`** (1 nodes): `test_load_autocreate_with_missing_parent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 191`** (1 nodes): `Venture OS — Strategy Layer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 192`** (1 nodes): `_git_failure() (test_agent_deploy)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 193`** (1 nodes): `test_cli_runner_missing_gate_exits_one()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 194`** (1 nodes): `test_cli_runner_valid_spec_all_labels()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 195`** (1 nodes): `test_cli_runner_valid_spec_exits_zero()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 196`** (1 nodes): `test_parse_spec_empty_gate_returns_empty_string()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 197`** (1 nodes): `test_parse_spec_missing_gate_returns_empty()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 198`** (1 nodes): `test_add_creates_registry_dir_if_absent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 199`** (1 nodes): `test_add_duplicate_id_raises()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 200`** (1 nodes): `PASS returns 1 when update_state tool exits non-zero rationale`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 201`** (1 nodes): `Brick — Scoped Unit of Work`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 202`** (1 nodes): `test_close_feature_null_current_brick_state_cleared()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 203`** (1 nodes): `test_close_phase_null_current_brick_state_updated()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 204`** (1 nodes): `test_close_phase_valid_current_brick_unchanged_behavior()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 205`** (1 nodes): `NanoBot — Agent Template with Memory & Tool-Calling`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 206`** (1 nodes): `Raw Python Agent Runtime`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 207`** (1 nodes): `Org Schema — Software Architecture Document`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 208`** (1 nodes): `AGENT.md — AI Tool Entry Point`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 209`** (1 nodes): `test_brick_branch_created_from_phase()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 210`** (1 nodes): `test_brick_branch_updates_state()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 211`** (1 nodes): `test_cli_close_feature_exits_zero()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 212`** (1 nodes): `test_cli_close_phase_exits_zero()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 213`** (1 nodes): `write_state_excerpt()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 214`** (1 nodes): `write_test_output()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 215`** (1 nodes): `test_cli_resume_missing_handoff_exits_one()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 216`** (1 nodes): `Arch-Brain — Architecture Session`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 217`** (1 nodes): `test_cli_guard_exits_one()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 218`** (1 nodes): `_mock_git_success()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 219`** (1 nodes): `Docker CE — Agent Container Runtime`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `idea-to-product-os Knowledge Graph Wiki Index` connect `Skeptic Packet Tests` to `Commit Module Tests`, `Context Module Tests`, `Component 32`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `main.py (CLI Entry Point)` connect `Build Command Tests` to `Session Close Tests`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Why does `context.py` connect `Context Module Tests` to `Skeptic Packet Tests`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `agent.py` (e.g. with `Framework Decision Gate — RAW PYTHON vs NANOBOT` and `Venture OS — Idea Stress-Test & Org Schema`) actually correct?**
  _`agent.py` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `run_close_session()` (e.g. with `_read_llm_config()` and `_load_state()`) actually correct?**
  _`run_close_session()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Read TEST_COMMAND from context.txt and return as argv list.      Why it exists:`, `Return the absolute repo root, or None if not in a git repo.`, `Stage all spec FILES in the git index before building the packet.` to the rest of the system?**
  _437 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Skeptic Packet Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._