# Skeptic Packet Tooling

> Community 28 · 15 nodes · cohesion 0.24

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| make_skeptic_packet.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| _get_git_root() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| _git_add_spec_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| is_git_repo() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| main() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| parse_scoped_files() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| _parse_test_command() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| Return the absolute repo root, or None if not in a git repo. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | rationale |
| Stage all spec FILES in the git index before building the packet. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | rationale |
| Read TEST_COMMAND from context.txt and return as argv list.      Why it exists: | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | rationale |
| write_diff_artifact() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| write_scoped_files_bundle() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| write_spec_copy() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| write_state_excerpt() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |
| write_test_output() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/bricklayer/tools/make_skeptic_packet.py` | code |

## Key Relationships

- **make_skeptic_packet.py** `contains` → _parse_test_command() `[EXTRACTED]`
- **make_skeptic_packet.py** `contains` → parse_scoped_files() `[EXTRACTED]`
- **make_skeptic_packet.py** `contains` → write_spec_copy() `[EXTRACTED]`
- **_get_git_root()** `contains` → make_skeptic_packet.py `[EXTRACTED]`
- **_get_git_root()** `calls` → main() `[INFERRED]`
- **_get_git_root()** `rationale_for` → Return the absolute repo root, or None if not in a git repo. `[EXTRACTED]`
- **_git_add_spec_files()** `contains` → make_skeptic_packet.py `[EXTRACTED]`
- **_git_add_spec_files()** `calls` → main() `[INFERRED]`
- **_git_add_spec_files()** `rationale_for` → Stage all spec FILES in the git index before building the packet. `[EXTRACTED]`
- **is_git_repo()** `contains` → make_skeptic_packet.py `[EXTRACTED]`
- **is_git_repo()** `calls` → write_diff_artifact() `[INFERRED]`
- **is_git_repo()** `calls` → main() `[INFERRED]`
- **main()** `contains` → make_skeptic_packet.py `[EXTRACTED]`
- **main()** `calls` → is_git_repo() `[INFERRED]`
- **main()** `calls` → _get_git_root() `[INFERRED]`
- **parse_scoped_files()** `contains` → make_skeptic_packet.py `[EXTRACTED]`
- **parse_scoped_files()** `calls` → write_scoped_files_bundle() `[INFERRED]`
- **parse_scoped_files()** `calls` → main() `[INFERRED]`
- **_parse_test_command()** `contains` → make_skeptic_packet.py `[EXTRACTED]`
- **_parse_test_command()** `rationale_for` → Read TEST_COMMAND from context.txt and return as argv list.      Why it exists: `[EXTRACTED]`
- **Return the absolute repo root, or None if not in a git repo.** `rationale_for` → _get_git_root() `[EXTRACTED]`
- **Stage all spec FILES in the git index before building the packet.** `rationale_for` → _git_add_spec_files() `[EXTRACTED]`
- **Read TEST_COMMAND from context.txt and return as argv list.      Why it exists:** `rationale_for` → _parse_test_command() `[EXTRACTED]`