# Next Command Tests

> Community 26 · 20 nodes · cohesion 0.13

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_next.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| _cli_invoke() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| _make_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| Tests for cli/commands/next.py — bricklayer next command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| run_next() auto-creates state.json and exits 0 when file is absent.      Brick 2 | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| Error output mentions state.json and contains no raw traceback. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| Write project files and invoke `bricklayer next` via CliRunner. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| CliRunner: `bricklayer next` exits 0 for a known next_action. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| CliRunner: output is the routed command for snapshot_init. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| CliRunner: `bricklayer next` exits 0 when state.json is absent (auto-create). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| Write state.json with the given next_action. Returns repo root. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| run_next() maps each known next_action to the correct CLI command. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| Unknown next_action is printed as-is, exit 0. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | rationale |
| test_cli_runner_known_state_correct_output() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| test_cli_runner_known_state_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| test_cli_runner_missing_state_json_autocreates() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| test_missing_state_json_autocreates() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| test_missing_state_json_clear_error() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| test_routing_known_actions() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |
| test_unknown_next_action_passthrough() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_next.py` | code |

## Key Relationships

- **test_next.py** `contains` → _make_state() `[EXTRACTED]`
- **test_next.py** `contains` → test_routing_known_actions() `[EXTRACTED]`
- **test_next.py** `contains` → test_unknown_next_action_passthrough() `[EXTRACTED]`
- **_cli_invoke()** `contains` → test_next.py `[EXTRACTED]`
- **_cli_invoke()** `calls` → _make_state() `[INFERRED]`
- **_cli_invoke()** `calls` → test_cli_runner_known_state_exits_zero() `[INFERRED]`
- **_make_state()** `contains` → test_next.py `[EXTRACTED]`
- **_make_state()** `calls` → test_routing_known_actions() `[INFERRED]`
- **_make_state()** `calls` → test_unknown_next_action_passthrough() `[INFERRED]`
- **Tests for cli/commands/next.py — bricklayer next command.** `rationale_for` → test_next.py `[EXTRACTED]`
- **run_next() auto-creates state.json and exits 0 when file is absent.      Brick 2** `rationale_for` → test_missing_state_json_autocreates() `[EXTRACTED]`
- **Error output mentions state.json and contains no raw traceback.** `rationale_for` → test_missing_state_json_clear_error() `[EXTRACTED]`
- **Write project files and invoke `bricklayer next` via CliRunner.** `rationale_for` → _cli_invoke() `[EXTRACTED]`
- **CliRunner: `bricklayer next` exits 0 for a known next_action.** `rationale_for` → test_cli_runner_known_state_exits_zero() `[EXTRACTED]`
- **CliRunner: output is the routed command for snapshot_init.** `rationale_for` → test_cli_runner_known_state_correct_output() `[EXTRACTED]`
- **CliRunner: `bricklayer next` exits 0 when state.json is absent (auto-create).** `rationale_for` → test_cli_runner_missing_state_json_autocreates() `[EXTRACTED]`