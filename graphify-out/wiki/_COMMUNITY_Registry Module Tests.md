---
type: community
cohesion: 0.12
members: 18
---

# Registry Module Tests

**Cohesion:** 0.12 - loosely connected
**Members:** 18 nodes

## Members
- [[Tests for Brick 21 — agent registry module rationale]] - document - graphify-out/wiki/community-15-registry-module-tests.md
- [[Tests for Brick 22 — agent list and status commands rationale]] - document - graphify-out/wiki/community-6-agent-registry-tests.md
- [[Write a registry.yaml to tmp_path with the given agents rationale]] - document - graphify-out/wiki/community-15-registry-module-tests.md
- [[_make_malformed_registry()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[_make_malformed_registry() (agent_commands)]] - code - graphify-out/wiki/community-6-agent-registry-tests.md
- [[_make_registry()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[_make_registry() (agent_commands)]] - code - graphify-out/wiki/community-6-agent-registry-tests.md
- [[test_add_all_fields_persisted()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[test_add_atomic_write_leaves_no_tmp_file()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[test_add_duplicate_id_count_unchanged()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[test_add_duplicate_id_file_not_modified()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[test_agent_commands.py]] - code - graphify-out/wiki/community-6-agent-registry-tests.md
- [[test_cli_agent_list_empty_exits_zero()]] - code - graphify-out/wiki/community-6-agent-registry-tests.md
- [[test_cli_agent_list_exit_zero()]] - code - graphify-out/wiki/community-6-agent-registry-tests.md
- [[test_cli_agent_status_known_id_exits_zero()]] - code - graphify-out/wiki/community-6-agent-registry-tests.md
- [[test_load_malformed_yaml_error_message()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[test_load_malformed_yaml_raises_value_error()]] - code - graphify-out/wiki/community-15-registry-module-tests.md
- [[test_registry.py]] - code - graphify-out/wiki/community-15-registry-module-tests.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Registry_Module_Tests
SORT file.name ASC
```
