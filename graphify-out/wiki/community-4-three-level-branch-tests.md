# Three-Level Branch Tests

> Community 4 · 69 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| test_three_level_branch.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| _cli_setup() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| _fake_checkout_ok() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| _fake_git_current() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| _fake_run_tool() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| _mock_proc() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| Tests for Brick 14 — three-level branching (feature/phase/brick). | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| Return a side_effect list for sequential subprocess.run calls. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| Write state.json with next_action=skeptic_packet_ready. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| Patch run_tool and get_tool_path so verdict can complete without real tools. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| Simulate: feature branch → phase branch → brick branch → state fields. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| Side-effect that returns the given branch for rev-parse calls. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| After close-phase + close-feature, all branch fields are cleared. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| Side-effect: checkout succeeds, subsequent calls succeed. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | rationale |
| _read_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| _subprocess_side_effects() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_brick_branch_created_from_phase() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_brick_branch_from_feature_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_brick_branch_from_main_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_brick_branch_missing_name_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_brick_branch_missing_number_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_brick_branch_updates_state() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_branch_feature_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_branch_feature_wrong_parent_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_branch_phase_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_branch_phase_wrong_parent_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_close_feature_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_close_feature_wrong_branch_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_close_phase_exits_zero() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| test_cli_close_phase_wrong_branch_exits_one() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/tests/test_three_level_branch.py` | code |
| *(+39 more)* | | |

## Key Relationships

- **test_three_level_branch.py** `contains` → _write_state() `[EXTRACTED]`
- **test_three_level_branch.py** `contains` → _read_state() `[EXTRACTED]`
- **test_three_level_branch.py** `contains` → _fake_git_current() `[EXTRACTED]`
- **_cli_setup()** `contains` → test_three_level_branch.py `[EXTRACTED]`
- **_cli_setup()** `calls` → _write_state() `[INFERRED]`
- **_cli_setup()** `calls` → test_cli_branch_feature_exits_zero() `[INFERRED]`
- **_fake_checkout_ok()** `contains` → test_three_level_branch.py `[EXTRACTED]`
- **_fake_checkout_ok()** `rationale_for` → Side-effect: checkout succeeds, subsequent calls succeed. `[EXTRACTED]`
- **_fake_git_current()** `contains` → test_three_level_branch.py `[EXTRACTED]`
- **_fake_git_current()** `rationale_for` → Side-effect that returns the given branch for rev-parse calls. `[EXTRACTED]`
- **_fake_run_tool()** `contains` → test_three_level_branch.py `[EXTRACTED]`
- **_fake_run_tool()** `calls` → test_verdict_pass_on_brick_merges_to_phase() `[INFERRED]`
- **_fake_run_tool()** `calls` → test_verdict_pass_on_phase_merges_to_feature() `[INFERRED]`
- **_mock_proc()** `contains` → test_three_level_branch.py `[EXTRACTED]`
- **_mock_proc()** `calls` → test_close_phase_merges_to_feature() `[INFERRED]`
- **_mock_proc()** `calls` → test_close_phase_updates_state() `[INFERRED]`
- **Tests for Brick 14 — three-level branching (feature/phase/brick).** `rationale_for` → test_three_level_branch.py `[EXTRACTED]`
- **Return a side_effect list for sequential subprocess.run calls.** `rationale_for` → _subprocess_side_effects() `[EXTRACTED]`
- **Write state.json with next_action=skeptic_packet_ready.** `rationale_for` → _write_state_for_verdict() `[EXTRACTED]`
- **Patch run_tool and get_tool_path so verdict can complete without real tools.** `rationale_for` → _fake_run_tool() `[EXTRACTED]`