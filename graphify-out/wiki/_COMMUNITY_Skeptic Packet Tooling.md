---
type: community
cohesion: 0.14
members: 22
---

# Skeptic Packet Tooling

**Cohesion:** 0.14 - loosely connected
**Members:** 22 nodes

## Members
- [[Brick bricklayer-cli Test Command Config (spec.md)]] - document - bricklayer/skeptic_packet/spec.md
- [[Copy graph audit artifacts into skeptic_packet and emit a presence manifest.]] - rationale - bricklayer/tools/make_skeptic_packet.py
- [[Read TEST_COMMAND from context.txt and return as argv list.      Why it exists]] - rationale - bricklayer/tools/make_skeptic_packet.py
- [[Return the absolute repo root, or None if not in a git repo.]] - rationale - bricklayer/tools/make_skeptic_packet.py
- [[Stage all spec FILES in the git index before building the packet.]] - rationale - bricklayer/tools/make_skeptic_packet.py
- [[TEST_COMMAND Config]] - document - bricklayer/context.txt
- [[_get_git_root()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[_git_add_spec_files()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[_parse_test_command()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[bricklayercontext.txt]] - document - bricklayer/context.txt
- [[graphify-out Directory]] - document - bricklayer/tools/make_skeptic_packet.py
- [[is_git_repo()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[main()_2]] - code - bricklayer/tools/make_skeptic_packet.py
- [[make_skeptic_packet.py]] - code - bricklayer/tools/make_skeptic_packet.py
- [[parse_scoped_files()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[skeptic_packetspec.md]] - document - bricklayer/skeptic_packet/spec.md
- [[write_diff_artifact()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[write_graph_audit_artifacts()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[write_scoped_files_bundle()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[write_spec_copy()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[write_state_excerpt()]] - code - bricklayer/tools/make_skeptic_packet.py
- [[write_test_output()]] - code - bricklayer/tools/make_skeptic_packet.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Skeptic_Packet_Tooling
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Builder Rules and Prompts]]

## Top bridge nodes
- [[graphify-out Directory]] - degree 2, connects to 1 community