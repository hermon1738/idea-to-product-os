# Graph Report - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os  (2026-04-09)

## Corpus Check
- 99 files · ~94,090 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1597 nodes · 2350 edges · 93 communities detected
- Extraction: 64% EXTRACTED · 36% INFERRED · 0% AMBIGUOUS · INFERRED: 846 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `_make_registry()` - 47 edges
2. `_write_state()` - 40 edges
3. `_make_registry()` - 35 edges
4. `_make_project()` - 35 edges
5. `_make_deploy_repo()` - 28 edges
6. `_full_setup()` - 27 edges
7. `_make_agent_dir()` - 27 edges
8. `_mock_groq_success()` - 25 edges
9. `_make_project()` - 24 edges
10. `_make_registry()` - 22 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Session Close Pipeline"
Cohesion: 0.02
Nodes (84): _cli_setup(), _full_setup(), _mock_groq_success(), Tests for Brick 12 / Brick 18 — bricklayer close-session command., _is_git_repo returns True for a directory git-initialised as a repo., _is_git_repo returns False for a plain directory with no .git., DOCS_PATH not a git repo → warning to stderr, no subprocess calls., No git subprocess calls when _is_git_repo returns False. (+76 more)

### Community 1 - "Agent New Command"
Cohesion: 0.04
Nodes (46): _cli_agent_new(), _make_nanobot_template(), _make_registry(), Tests for Brick 23 — bricklayer agent new command., Create registry.yaml in tmp_path with the given agents., Create a minimal nanobot-template directory under tmp_path., Helper: invoke bricklayer agent new with standard flags via CliRunner., test_cli_agent_new_invalid_id_exits_one() (+38 more)

### Community 2 - "Agent Deploy Command"
Cohesion: 0.06
Nodes (63): _cli_deploy(), _git_failure(), _git_success(), _make_agent_dir(), _make_deploy_repo(), _make_registry(), Tests for Brick 24 — bricklayer agent deploy and agent live commands., TimeoutExpired from subprocess.run must surface as exit 1, not a traceback. (+55 more)

### Community 3 - "Branch Command Tests"
Cohesion: 0.04
Nodes (56): _cli_setup(), _make_project(), _mock_get_branch(), Tests for Brick 8.6 — bricklayer branch command and build main guard., brick/N-name is constructed from number + slugified name., current_branch is written to state.json., Output contains the created branch name., Missing number → error, exit 1. (+48 more)

### Community 4 - "Three-Level Branch Tests"
Cohesion: 0.06
Nodes (68): _cli_setup(), _fake_checkout_ok(), _fake_git_current(), _fake_run_tool(), _mock_proc(), Tests for Brick 14 — three-level branching (feature/phase/brick)., Return a side_effect list for sequential subprocess.run calls., Write state.json with next_action=skeptic_packet_ready. (+60 more)

### Community 5 - "New Project Command"
Cohesion: 0.04
Nodes (25): _project_dir(), Tests for Brick 19 — bricklayer new-project command., Create a minimal bricklayer.yaml so CliRunner commands can find the repo., _setup_repo(), test_cli_new_project_all_files_exist(), test_cli_new_project_duplicate_exit_one(), test_cli_new_project_exit_zero(), test_cli_new_project_invalid_name_exit_one() (+17 more)

### Community 6 - "Agent Registry Tests"
Cohesion: 0.05
Nodes (26): _make_malformed_registry(), _make_registry(), Tests for Brick 22 — agent list and status commands., Write a registry.yaml to tmp_path with the given agents., test_cli_agent_list_empty_exits_zero(), test_cli_agent_list_empty_shows_prompt(), test_cli_agent_list_exit_zero(), test_cli_agent_list_output_contains_id() (+18 more)

### Community 7 - "Build Verdict Tests"
Cohesion: 0.06
Nodes (57): _cli_setup(), _make_project(), Tests for Brick 8 — bricklayer build --verdict PASS|FAIL., PASS returns 1 when update_state tool exits non-zero., FAIL increments loop_count by 1., FAIL does not advance next_action., FAIL always returns 1., FAIL below threshold prints normal blocker message. (+49 more)

### Community 8 - "Context Command Tests"
Cohesion: 0.06
Nodes (43): _make_bricklayer_state(), _make_project(), Tests for Brick 20 — bricklayer context command., Write a minimal bricklayer.yaml for CliRunner tests., Create a full project directory at context/projects/<name>/., Write bricklayer/state.json with the given project field., _setup_repo(), test_cli_context_exit_zero() (+35 more)

### Community 9 - "Build Tools Tests"
Cohesion: 0.06
Nodes (52): _cli_invoke(), _make_project(), Tests for Brick 6 — bricklayer build --snapshot/--verify/--test flag handlers., run_snapshot sets next_action to 'snapshot_init' on success., run_snapshot returns 1 on non-zero tool exit., run_snapshot leaves state.json unchanged on tool failure., run_verify returns 0 on tool exit 0., run_verify sets next_action to 'verify' on success. (+44 more)

### Community 10 - "Skeptic Packet Tests"
Cohesion: 0.06
Nodes (50): _cli_invoke(), _make_project(), Tests for Brick 7 (revision) — bricklayer build --skeptic-packet flag handler., Tool exits 0 but packet dir is missing → exit 1, state not updated., State is not updated when packet dir is missing after tool exit 0., Tool exits 0 but packet dir is empty → exit 1, state not updated., State not updated when packet dir is empty., Guard fires for any next_action other than tests_passed → exit 1. (+42 more)

### Community 11 - "Pause & Resume Tests"
Cohesion: 0.08
Nodes (36): _cli_setup(), _fake_git_branch(), _make_project(), Tests for Brick 9 — bricklayer pause command., If .continue-here.md write fails, HANDOFF.json is cleaned up too., CliRunner: `bricklayer pause` exits 0., CliRunner: both HANDOFF.json and .continue-here.md are written., CliRunner: HANDOFF.json contains all 8 fields with correct values. (+28 more)

### Community 12 - "Git Fix Tests"
Cohesion: 0.06
Nodes (40): _cli_setup(), _load_make_skeptic_packet(), _make_project(), Tests for Brick 8.5 — auto-stage (make_skeptic_packet.py) and auto-commit (run_v, git add is called before git commit., All files are passed to git add., Commit message uses feat(brick-N) format., Commit message includes Co-Authored-By trailer. (+32 more)

### Community 13 - "Commit Command Tests"
Cohesion: 0.08
Nodes (31): _cli_setup(), _make_project(), _make_real_git_repo(), _mock_nothing_staged(), _mock_staged(), Tests for Brick 11 — bricklayer commit command., Create a minimal real git repo for integration testing., Integration: real git repo — bricklayer commit creates a correctly tagged commit (+23 more)

### Community 14 - "Agent CLI Module"
Cohesion: 0.06
Nodes (43): agent_deploy(), agent_list(), agent_live(), agent_new(), agent_status(), _build_placeholder_map(), _build_registry_entry(), _format_detail() (+35 more)

### Community 15 - "Registry Module Tests"
Cohesion: 0.07
Nodes (26): _make_malformed_registry(), _make_registry(), Tests for Brick 21 — agent registry module., Write a registry.yaml to tmp_path with the given agents., test_add_all_fields_persisted(), test_add_atomic_write_leaves_no_tmp_file(), test_add_duplicate_id_count_unchanged(), test_add_duplicate_id_file_not_modified() (+18 more)

### Community 16 - "State Module Tests"
Cohesion: 0.06
Nodes (36): Tests for cli/state.py — state.json reader/writer., write() with a partial last_test_run dict deep-merges; sibling keys survive., write() with a state missing a required field raises ValueError., write() with state missing last_test_run raises ValueError., write() where loop_count is a string raises ValueError., write() where completed_bricks is not a list raises ValueError., load() auto-creates state.json even when parent directory does not exist.      m, load() returns a valid dict when state.json is missing but parent exists.      T (+28 more)

### Community 17 - "Build Command Tests"
Cohesion: 0.07
Nodes (36): _cli_invoke(), Tests for cli/commands/build.py — bricklayer build (print contract)., parse_spec() extracts all 6 CONTRACT_FIELDS from a full spec., parse_spec() returns the correct content for each field., parse_spec() returns no GATE key (or empty string) when absent., parse_spec() returns empty string for a blank GATE section., run_build() returns 0 for a valid spec.md., run_build() prints all 6 field labels. (+28 more)

### Community 18 - "Config Loader Tests"
Cohesion: 0.07
Nodes (34): _make_file(), Tests for cli/config.py — YAML loader, path validation, and .env loading., Error output must not contain 'Traceback'., All missing paths are reported, not just the first one., No bricklayer.yaml → human-readable message, exit 1., Missing yaml error must not include 'Traceback'., KEY=VALUE in .env is loaded into os.environ., .env absent → no error, no exception. (+26 more)

### Community 19 - "Build & Merge Module"
Cohesion: 0.08
Nodes (33): _commit_and_merge(), _get_current_branch(), _git_commit_spec(), _handle_fail_verdict(), _merge_branch_to(), _merge_to_parent(), _parse_brick_name(), parse_spec() (+25 more)

### Community 20 - "Session Close Module"
Cohesion: 0.09
Nodes (33): _append_decision_log(), _build_decision_log_row(), _build_pipeline_status(), _build_user_message(), _call_groq(), _extract_structured_data(), _is_git_repo(), _load_sprint_brain() (+25 more)

### Community 21 - "Resume Command Tests"
Cohesion: 0.1
Nodes (16): _cli_setup(), _fake_git(), Tests for Brick 10 — bricklayer resume command., test_cli_resume_branch_mismatch_exits_zero(), test_cli_resume_exits_zero(), test_cli_resume_output_contains_all_fields(), test_run_resume_branch_match_no_warning(), test_run_resume_branch_mismatch_exits_zero() (+8 more)

### Community 22 - "CLI Entry Point"
Cohesion: 0.07
Nodes (29): branch(), build(), close_feature(), close_phase(), close_session(), commit(), context(), new_project() (+21 more)

### Community 23 - "Main CLI Tests"
Cohesion: 0.11
Nodes (23): _make_file(), CliRunner integration tests for cli/main.py., run command exits 1 when a yaml path is missing., Missing path error output must not show a Python traceback., run command exits 1 when bricklayer.yaml is not found anywhere., Create a minimal project for close-session tests. Returns yaml_path., CliRunner integration: .env loaded at startup; llm: section drives model choice., api_key_env pointing to an unset var → clear error message, exit 1, no traceback (+15 more)

### Community 24 - "Config Write Tests"
Cohesion: 0.11
Nodes (20): Tests for _write_context_txt — automatic context.txt generation from bricklayer., bricklayer/ directory is created if it doesn't exist., Write goes through a tempfile + os.replace, not a direct open() call., If language is not in the test: section, LANGUAGE defaults to Python., Running _write_context_txt twice overwrites with the latest values., Correct LANGUAGE and TEST_COMMAND lines are written when test: section exists., context.txt contains -v when test.command contains -v., When test: is absent, existing context.txt is left untouched and a warning is pr (+12 more)

### Community 25 - "Status Command Tests"
Cohesion: 0.13
Nodes (19): _make_project(), Tests for cli/commands/status.py — bricklayer status command., When state.json is absent, run_status() auto-creates it and exits 0.      Brick, Error message is human-readable and contains 'state.json'., CliRunner: status exits 0 and all 5 field labels appear in output., CliRunner: status exits 0 when state.json is absent (auto-create)., Create a minimal project tree under tmp_path. Returns the root., run_status() prints all 5 labeled fields and returns 0. (+11 more)

### Community 26 - "Next Command Tests"
Cohesion: 0.13
Nodes (19): _cli_invoke(), _make_state(), Tests for cli/commands/next.py — bricklayer next command., run_next() auto-creates state.json and exits 0 when file is absent.      Brick 2, Error output mentions state.json and contains no raw traceback., Write project files and invoke `bricklayer next` via CliRunner., CliRunner: `bricklayer next` exits 0 for a known next_action., CliRunner: output is the routed command for snapshot_init. (+11 more)

### Community 27 - "Close Phase Fix Tests"
Cohesion: 0.16
Nodes (17): _git(), _make_feature_repo(), _make_phase_repo(), Tests for Brick 26 fixes — null current_brick on close-phase/close-feature.  WHY, Initialise a temporary git repo checked out on a phase/* branch.      Sets up ma, Initialise a temporary git repo checked out on a feature/* branch.      Used for, close-phase with null current_brick exits 0 after a successful merge.      Befor, After close-phase, current_phase is None and current_brick is '' in state. (+9 more)

### Community 28 - "Skeptic Packet Tooling"
Cohesion: 0.24
Nodes (14): _get_git_root(), _git_add_spec_files(), is_git_repo(), main(), parse_scoped_files(), _parse_test_command(), Return the absolute repo root, or None if not in a git repo., Stage all spec FILES in the git index before building the packet. (+6 more)

### Community 29 - "Agent Registry Module"
Cohesion: 0.23
Nodes (14): add(), get(), load(), Agent registry: read and write context/agents/registry.yaml.  WHY THIS EXISTS:, Return a single agent dict by ID, or None if not found.      Args:         root:, Append a new agent to the registry.      Validates required fields and checks fo, Update the status field of an existing agent.      Args:         root: Repo root, Read and parse registry.yaml, returning the raw dict.      Why it exists: Both l (+6 more)

### Community 30 - "Pause Module"
Cohesion: 0.2
Nodes (13): _build_continue_md(), _build_handoff(), _get_current_branch(), _next_command(), _parse_brick(), Pause command: write HANDOFF.json and .continue-here.md for session handoff.  WH, Resolve a next_action value to the CLI command the next session should run., Assemble the HANDOFF.json payload from state and git.      Why it exists: Assemb (+5 more)

### Community 31 - "State Read/Write Module"
Cohesion: 0.23
Nodes (11): _deep_merge(), load(), _make_default_state(), state.json reader/writer with schema enforcement.  WHY THIS EXISTS:     state.js, Raise ValueError if data does not satisfy the state schema.      Why it exists:, Load and validate state.json, auto-creating it with defaults if missing.      Wh, Recursively merge updates into base; nested dicts are merged, not replaced., Deep-merge updates into state.json, validate, and persist atomically.      Why i (+3 more)

### Community 32 - "New Project Module"
Cohesion: 0.23
Nodes (11): _build_decision_log(), _build_state_json(), _build_state_md(), New-project command: scaffold context/projects/<name>/ with initial state files., Build initial state.json content for a new project.      Args:         name: Pro, Scaffold a new project directory with STATE.md, decision-log.md, state.json., Return an error message if name is invalid, else None.      Why it exists: Centr, Build initial STATE.md content for a new project.      Args:         name: Proje (+3 more)

### Community 33 - "Commit Module"
Cohesion: 0.23
Nodes (11): _build_message(), _check_staged(), _do_commit(), _parse_brick(), Commit command: git commit wrapper with auto-tagged brick ID message.  WHY THIS, Build the full conventional-commit message string.      Why it exists: The messa, Run ``git commit -m <message>`` and return (exit_code, output).      Why it exis, Commit staged files with an auto-tagged brick ID conventional-commit message. (+3 more)

### Community 34 - "Context Module"
Cohesion: 0.23
Nodes (11): _load_project_state(), Context command: print a compact project context block for AI session start.  WH, Extract "Next command:" value from STATE.md.      Why it exists: STATE.md is the, Return the project name to use, reading bricklayer/state.json if needed.      Wh, Print a compact context block for a project.      Why it exists: See module docs, Load and parse state.json from a project directory.      Why it exists: Centrali, Return the last n data rows from decision-log.md.      Why it exists: Only data, _read_last_decisions() (+3 more)

### Community 35 - "File Scope Verifier"
Cohesion: 0.36
Nodes (10): build_snapshot(), has_git_repo(), main(), modified_files_git(), modified_files_snapshot(), parse_allowed_files(), read_snapshot(), sha256_for() (+2 more)

### Community 36 - "Test Runner & Capture"
Cohesion: 0.38
Nodes (9): append_handover(), detect_missing_tool_from_output(), extract_failed_nodeids(), load_state(), main(), parse_test_command(), run_command(), save_state() (+1 more)

### Community 37 - "Config Loader Module"
Cohesion: 0.27
Nodes (9): find_yaml(), load_and_validate(), _load_dotenv(), YAML loader and path validation for bricklayer.yaml.  WHY THIS EXISTS:     Every, Write bricklayer/context.txt from the test: section of bricklayer.yaml.      WHY, Load bricklayer.yaml, resolve all declared paths, exit 1 on any failure.      Wh, Load a .env file from directory into os.environ (non-overwriting).      Why it e, Walk upward from start until bricklayer.yaml is found.      Why it exists: Comma (+1 more)

### Community 38 - "Branch Module"
Cohesion: 0.27
Nodes (9): _get_current_branch(), _git_create_checkout(), Branch command: create and checkout brick/phase/feature branches.  WHY THIS EXIS, Run ``git checkout -b <branch_name>`` and return (exit_code, output).      Why i, Create and checkout a branch at the correct hierarchy level.      Enforces the t, Convert a human-readable name to a lowercase-hyphenated git branch slug.      Wh, Return the current git branch name, or None if git fails or is absent.      Why, run_branch() (+1 more)

### Community 39 - "State Updater Tool"
Cohesion: 0.54
Nodes (7): append_handover(), complete_brick(), has_pass_verdict(), load_state(), main(), reject_completion(), save_state()

### Community 40 - "Component 40"
Cohesion: 0.32
Nodes (7): _format_block(), _get_current_branch(), Resume command: read HANDOFF.json and print a formatted session context block., Read HANDOFF.json and print a formatted session context block.      Validates al, Return the current git branch name, or None if git fails or is absent.      Why, Format the handoff dict into the resume context block string.      Why it exists, run_resume()

### Community 41 - "Component 41"
Cohesion: 0.32
Nodes (7): _get_current_branch(), _merge_no_ff(), Close-feature command: merge current feature/* branch into main.  WHY THIS EXIST, Merge current feature/* branch into main and clear feature context.      Enforce, Return the current git branch name, or None if git fails or is absent.      Why, Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T, run_close_feature()

### Community 42 - "Component 42"
Cohesion: 0.32
Nodes (7): _get_current_branch(), _merge_no_ff(), Close-phase command: merge current phase/* branch into parent feature/* branch., Merge current phase/* branch into its parent feature/* branch.      Reads the me, Return the current git branch name, or None if git fails or is absent.      Why, Checkout target, merge branch with --no-ff, delete branch.      Why it exists: T, run_close_phase()

### Community 43 - "Component 43"
Cohesion: 0.33
Nodes (5): get_tool_path(), Shared tool invocation and output capture for bricklayer build flags.  WHY THIS, Run ``python3 tool_path [args]`` and return (exit_code, combined_output).      W, Resolve a named tool entry from bricklayer.yaml config to an absolute Path., run_tool()

### Community 44 - "Component 44"
Cohesion: 0.4
Nodes (5): _parse_state_md(), Status command: print current brick, last test result, and next action.  WHY THI, Parse STATE.md into a key → value dict.      Why it exists: run_status needs pro, Print five pipeline status fields to stdout.      Combines data from state.json, run_status()

### Community 45 - "Component 45"
Cohesion: 0.5
Nodes (3): Next command: read next_action from state.json and print the next CLI command., Read next_action from state.json and print the corresponding CLI command.      W, run_next()

### Community 46 - "Component 46"
Cohesion: 1.0
Nodes (2): main(), section_lines()

### Community 47 - "Component 47"
Cohesion: 1.0
Nodes (1): Bricklayer CLI package.  WHY THIS EXISTS:     This file marks the cli/ directory

### Community 48 - "Component 48"
Cohesion: 1.0
Nodes (1): AGENT.md — AI Tool Entry Point

### Community 49 - "Component 49"
Cohesion: 1.0
Nodes (1): CLAUDE.md — Claude Code Session Entry Point

### Community 50 - "Component 50"
Cohesion: 1.0
Nodes (1): CODEX.md — Codex Entry Point

### Community 51 - "Component 51"
Cohesion: 1.0
Nodes (1): README.md — Idea-to-Product OS Overview

### Community 52 - "Component 52"
Cohesion: 1.0
Nodes (1): Idea-to-Product Pipeline — 7-Phase System

### Community 53 - "Component 53"
Cohesion: 1.0
Nodes (1): Bricklayer CLI

### Community 54 - "Component 54"
Cohesion: 1.0
Nodes (1): Skeptic Gate — Independent AI Review

### Community 55 - "Component 55"
Cohesion: 1.0
Nodes (1): skeptic_verdict.md — Verdict File (Tony Writes Only)

### Community 56 - "Component 56"
Cohesion: 1.0
Nodes (1): Brick — Scoped Unit of Work

### Community 57 - "Component 57"
Cohesion: 1.0
Nodes (1): spec.md — Active Brick Contract

### Community 58 - "Component 58"
Cohesion: 1.0
Nodes (1): state.json — Bricklayer Runtime State

### Community 59 - "Component 59"
Cohesion: 1.0
Nodes (1): Tony — Human Co-CEO & Decision Maker

### Community 60 - "Component 60"
Cohesion: 1.0
Nodes (1): Session Scribe Agent — AGT-SYS-001

### Community 61 - "Component 61"
Cohesion: 1.0
Nodes (1): NanoBot — Agent Template with Memory & Tool-Calling

### Community 62 - "Component 62"
Cohesion: 1.0
Nodes (1): Venture OS — Idea Stress-Test & Org Schema

### Community 63 - "Component 63"
Cohesion: 1.0
Nodes (1): arch-brain — Architecture Session

### Community 64 - "Component 64"
Cohesion: 1.0
Nodes (1): Agent-OS — AI Layer Design

### Community 65 - "Component 65"
Cohesion: 1.0
Nodes (1): plan-brain — Brick Planning from Architecture

### Community 66 - "Component 66"
Cohesion: 1.0
Nodes (1): sprint-brain — Post-Brick Sprint Review

### Community 67 - "Component 67"
Cohesion: 1.0
Nodes (1): Autonomous Build Mode — 7-Step Build Sequence

### Community 68 - "Component 68"
Cohesion: 1.0
Nodes (1): Hetzner VPS — Live Infrastructure

### Community 69 - "Component 69"
Cohesion: 1.0
Nodes (1): stack-rules.md — Engineering Standards

### Community 70 - "Component 70"
Cohesion: 1.0
Nodes (1): Loop Stop Rule — max 3 loops before rescope

### Community 71 - "Component 71"
Cohesion: 1.0
Nodes (1): /run-brick Skill — Autonomous Build Trigger

### Community 72 - "Component 72"
Cohesion: 1.0
Nodes (1): update_state.py — State Advancement Tool

### Community 73 - "Component 73"
Cohesion: 1.0
Nodes (1): Engineering Standards — Code Quality Rules

### Community 74 - "Component 74"
Cohesion: 1.0
Nodes (1): DEBT.md — Technical Debt Register

### Community 75 - "Component 75"
Cohesion: 1.0
Nodes (1): INTAKE — Project Brief SOP

### Community 76 - "Component 76"
Cohesion: 1.0
Nodes (1): Skeptic Gate Checklist

### Community 77 - "Component 77"
Cohesion: 1.0
Nodes (1): State JSON Schema

### Community 78 - "Component 78"
Cohesion: 1.0
Nodes (1): Stack Rules — Idea-to-Product OS

### Community 79 - "Component 79"
Cohesion: 1.0
Nodes (1): Venture OS — Strategy Layer

### Community 80 - "Component 80"
Cohesion: 1.0
Nodes (1): Arch-Brain — Architecture Session

### Community 81 - "Component 81"
Cohesion: 1.0
Nodes (1): Plan-Brain — Build Planning Mode

### Community 82 - "Component 82"
Cohesion: 1.0
Nodes (1): Agent-OS — AI Layer Design

### Community 83 - "Component 83"
Cohesion: 1.0
Nodes (1): Sprint-Brain — Sprint Review Mode

### Community 84 - "Component 84"
Cohesion: 1.0
Nodes (1): Pipeline Reference

### Community 85 - "Component 85"
Cohesion: 1.0
Nodes (1): Architecture Doc

### Community 86 - "Component 86"
Cohesion: 1.0
Nodes (1): Framework Decision Gate — RAW PYTHON vs NANOBOT

### Community 87 - "Component 87"
Cohesion: 1.0
Nodes (1): Raw Python Agent Runtime

### Community 88 - "Component 88"
Cohesion: 1.0
Nodes (1): Org Schema — Software Architecture Document

### Community 89 - "Component 89"
Cohesion: 1.0
Nodes (1): Docker CE — Agent Container Runtime

### Community 90 - "Component 90"
Cohesion: 1.0
Nodes (1): Groq LLM Stack

### Community 91 - "Component 91"
Cohesion: 1.0
Nodes (1): Builder AI — Claude Code / Codex

### Community 92 - "Component 92"
Cohesion: 1.0
Nodes (1): Skeptic AI — GPT-4 / Gemini

## Knowledge Gaps
- **481 isolated node(s):** `Read TEST_COMMAND from context.txt and return as argv list.      Why it exists:`, `Return the absolute repo root, or None if not in a git repo.`, `Stage all spec FILES in the git index before building the packet.`, `Tests for Brick 21 — agent registry module.`, `Write a registry.yaml to tmp_path with the given agents.` (+476 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Component 47`** (2 nodes): `__init__.py`, `Bricklayer CLI package.  WHY THIS EXISTS:     This file marks the cli/ directory`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 48`** (1 nodes): `AGENT.md — AI Tool Entry Point`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 49`** (1 nodes): `CLAUDE.md — Claude Code Session Entry Point`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 50`** (1 nodes): `CODEX.md — Codex Entry Point`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 51`** (1 nodes): `README.md — Idea-to-Product OS Overview`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 52`** (1 nodes): `Idea-to-Product Pipeline — 7-Phase System`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 53`** (1 nodes): `Bricklayer CLI`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 54`** (1 nodes): `Skeptic Gate — Independent AI Review`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 55`** (1 nodes): `skeptic_verdict.md — Verdict File (Tony Writes Only)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 56`** (1 nodes): `Brick — Scoped Unit of Work`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 57`** (1 nodes): `spec.md — Active Brick Contract`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 58`** (1 nodes): `state.json — Bricklayer Runtime State`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 59`** (1 nodes): `Tony — Human Co-CEO & Decision Maker`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 60`** (1 nodes): `Session Scribe Agent — AGT-SYS-001`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 61`** (1 nodes): `NanoBot — Agent Template with Memory & Tool-Calling`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 62`** (1 nodes): `Venture OS — Idea Stress-Test & Org Schema`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 63`** (1 nodes): `arch-brain — Architecture Session`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 64`** (1 nodes): `Agent-OS — AI Layer Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 65`** (1 nodes): `plan-brain — Brick Planning from Architecture`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 66`** (1 nodes): `sprint-brain — Post-Brick Sprint Review`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 67`** (1 nodes): `Autonomous Build Mode — 7-Step Build Sequence`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 68`** (1 nodes): `Hetzner VPS — Live Infrastructure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 69`** (1 nodes): `stack-rules.md — Engineering Standards`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 70`** (1 nodes): `Loop Stop Rule — max 3 loops before rescope`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 71`** (1 nodes): `/run-brick Skill — Autonomous Build Trigger`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 72`** (1 nodes): `update_state.py — State Advancement Tool`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 73`** (1 nodes): `Engineering Standards — Code Quality Rules`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 74`** (1 nodes): `DEBT.md — Technical Debt Register`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 75`** (1 nodes): `INTAKE — Project Brief SOP`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 76`** (1 nodes): `Skeptic Gate Checklist`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 77`** (1 nodes): `State JSON Schema`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 78`** (1 nodes): `Stack Rules — Idea-to-Product OS`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 79`** (1 nodes): `Venture OS — Strategy Layer`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 80`** (1 nodes): `Arch-Brain — Architecture Session`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 81`** (1 nodes): `Plan-Brain — Build Planning Mode`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 82`** (1 nodes): `Agent-OS — AI Layer Design`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 83`** (1 nodes): `Sprint-Brain — Sprint Review Mode`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 84`** (1 nodes): `Pipeline Reference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 85`** (1 nodes): `Architecture Doc`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 86`** (1 nodes): `Framework Decision Gate — RAW PYTHON vs NANOBOT`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 87`** (1 nodes): `Raw Python Agent Runtime`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 88`** (1 nodes): `Org Schema — Software Architecture Document`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 89`** (1 nodes): `Docker CE — Agent Container Runtime`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 90`** (1 nodes): `Groq LLM Stack`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 91`** (1 nodes): `Builder AI — Claude Code / Codex`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Component 92`** (1 nodes): `Skeptic AI — GPT-4 / Gemini`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Are the 45 inferred relationships involving `_make_registry()` (e.g. with `test_run_agent_deploy_returns_zero()` and `test_run_agent_deploy_copies_files()`) actually correct?**
  _`_make_registry()` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `_write_state()` (e.g. with `test_feature_branch_created_from_main()` and `test_feature_branch_slugifies_name()`) actually correct?**
  _`_write_state()` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `_make_registry()` (e.g. with `test_scaffold_nanobot_creates_directory()` and `test_run_agent_new_nanobot_returns_zero()`) actually correct?**
  _`_make_registry()` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `_make_project()` (e.g. with `test_load_project_state_returns_dict()` and `test_load_project_state_malformed_returns_none()`) actually correct?**
  _`_make_project()` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 26 inferred relationships involving `_make_deploy_repo()` (e.g. with `test_run_agent_deploy_returns_zero()` and `test_run_agent_deploy_copies_files()`) actually correct?**
  _`_make_deploy_repo()` has 26 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Read TEST_COMMAND from context.txt and return as argv list.      Why it exists:`, `Return the absolute repo root, or None if not in a git repo.`, `Stage all spec FILES in the git index before building the packet.` to the rest of the system?**
  _481 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Session Close Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.02 - nodes in this community are weakly interconnected._