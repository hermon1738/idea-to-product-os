BRICK: Brick 21 - agent registry

WHAT:
  A YAML-based agent registry at context/agents/registry.yaml that
  tracks every agent with its ID, project, runtime, status, trigger,
  and location. A registry module in cli/ reads and writes it.
  Pre-populated with the 3 live agents.

INPUT:
  context/agents/ directory

OUTPUT:
  context/agents/registry.yaml — master index with 3 live agents
  cli/registry.py — load(), get(), add(), update_status()

GATE:
  OUTPUTS

BLOCKER:
  bricklayer agent list/new/deploy read from this registry.

WAVE:
  SEQUENTIAL

FILES:
- context/agents/registry.yaml
- cli/registry.py
- tests/test_registry.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) registry.yaml exists with 3 live agents, all required fields
2) load() returns list of 3 dicts
3) get("idea-os-scribe-01") returns correct agent dict
4) add() valid agent -> appended, written atomically
5) add() missing required field -> ValueError, file not modified
6) add() duplicate ID -> ValueError, file not modified
7) update_status() valid ID -> persisted correctly
8) update_status() unknown ID -> ValueError
9) registry.yaml missing -> load() returns empty list, no crash
10) malformed registry.yaml -> clear error, no raw traceback

TEST REQUIREMENTS:
- load(): 3 agents, all required fields
- get(): known ID -> correct dict; unknown ID -> None
- add(): valid -> appended atomically
- add(): missing field -> ValueError, file unchanged
- add(): duplicate ID -> ValueError, file unchanged
- update_status(): valid -> persisted
- update_status(): unknown ID -> ValueError
- missing registry.yaml -> load() returns []
- malformed yaml -> ValueError with clear message

OUT OF SCOPE:
- Any CLI command registration
- Any file outside the FILES list
