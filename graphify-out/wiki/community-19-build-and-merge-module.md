# Build & Merge Module

> Community 19 · 34 nodes · cohesion 0.08

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| build.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _commit_and_merge() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _get_current_branch() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _git_commit_spec() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _handle_fail_verdict() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _merge_branch_to() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _merge_to_parent() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _parse_brick_name() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| parse_spec() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _parse_spec_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| Build command: parse bricklayer/spec.md and handle all build pipeline flags.  WH | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Print the brick contract from spec.md. Returns 0 on success, 1 on error.      Wh | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Invoke a named pipeline tool and update state.json next_action on success. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Run verify tool with --snapshot-init to capture the baseline file state.      Wh | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Run verify tool to check that only spec-listed files were modified.      Why it | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Run the test suite via run_tests_and_capture.py.      Why it exists: Tests must | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Generate the skeptic_packet/ evidence bundle for independent review.      Guards | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Return the current git branch name, or None on failure.      Why it exists: buil | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Checkout target, merge branch_name with --no-ff, delete branch_name.      Why it | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Extract the brick name from the ``BRICK: …`` line in spec.md.      Why it exists | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Return the FILES list from spec.md.      Why it exists: run_verdict auto-commits | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Stage spec FILES and commit them with a standard brick message.      Why it exis | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Increment loop_count and emit FAIL or RESCOPE message.      Why it exists: Isola | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Route auto-merge to the correct parent branch based on current branch level. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Auto-commit spec FILES then merge the current branch to its parent.      Why it | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Route PASS or FAIL verdict to the appropriate handler.      Validates the verdic | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| Parse spec.md text and return CONTRACT_FIELDS → value strings.      A section he | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | rationale |
| run_build() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| _run_flag_tool() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| run_skeptic_packet() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/build.py` | code |
| *(+4 more)* | | |

## Key Relationships

- **build.py** `contains` → parse_spec() `[EXTRACTED]`
- **build.py** `contains` → run_build() `[EXTRACTED]`
- **build.py** `contains` → _run_flag_tool() `[EXTRACTED]`
- **_commit_and_merge()** `contains` → build.py `[EXTRACTED]`
- **_commit_and_merge()** `calls` → _parse_brick_name() `[INFERRED]`
- **_commit_and_merge()** `calls` → _parse_spec_files() `[INFERRED]`
- **_get_current_branch()** `contains` → build.py `[EXTRACTED]`
- **_get_current_branch()** `calls` → _commit_and_merge() `[INFERRED]`
- **_get_current_branch()** `rationale_for` → Return the current git branch name, or None on failure.      Why it exists: buil `[EXTRACTED]`
- **_git_commit_spec()** `contains` → build.py `[EXTRACTED]`
- **_git_commit_spec()** `calls` → _commit_and_merge() `[INFERRED]`
- **_git_commit_spec()** `rationale_for` → Stage spec FILES and commit them with a standard brick message.      Why it exis `[EXTRACTED]`
- **_handle_fail_verdict()** `contains` → build.py `[EXTRACTED]`
- **_handle_fail_verdict()** `calls` → run_verdict() `[INFERRED]`
- **_handle_fail_verdict()** `rationale_for` → Increment loop_count and emit FAIL or RESCOPE message.      Why it exists: Isola `[EXTRACTED]`
- **_merge_branch_to()** `contains` → build.py `[EXTRACTED]`
- **_merge_branch_to()** `calls` → _merge_to_parent() `[INFERRED]`
- **_merge_branch_to()** `rationale_for` → Checkout target, merge branch_name with --no-ff, delete branch_name.      Why it `[EXTRACTED]`
- **_merge_to_parent()** `contains` → build.py `[EXTRACTED]`
- **_merge_to_parent()** `calls` → _merge_branch_to() `[INFERRED]`
- **_merge_to_parent()** `calls` → _commit_and_merge() `[INFERRED]`
- **_parse_brick_name()** `contains` → build.py `[EXTRACTED]`
- **_parse_brick_name()** `calls` → _commit_and_merge() `[INFERRED]`
- **_parse_brick_name()** `rationale_for` → Extract the brick name from the ``BRICK: …`` line in spec.md.      Why it exists `[EXTRACTED]`
- **parse_spec()** `contains` → build.py `[EXTRACTED]`
- **parse_spec()** `calls` → run_build() `[INFERRED]`
- **parse_spec()** `rationale_for` → Parse spec.md text and return CONTRACT_FIELDS → value strings.      A section he `[EXTRACTED]`
- **_parse_spec_files()** `contains` → build.py `[EXTRACTED]`
- **_parse_spec_files()** `calls` → _commit_and_merge() `[INFERRED]`
- **_parse_spec_files()** `rationale_for` → Return the FILES list from spec.md.      Why it exists: run_verdict auto-commits `[EXTRACTED]`