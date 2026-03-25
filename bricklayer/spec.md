BRICK: Brick 22 - agent list + status commands

WHAT:
  Two read-only agent commands: `bricklayer agent list` prints all
  agents from registry.yaml in a formatted table. `bricklayer agent
  status <id>` prints the full detail block for one agent.

INPUT:
  context/agents/registry.yaml (built in Brick 21)

OUTPUT:
  bricklayer agent list → formatted table of all agents (or empty
  message if none registered)
  bricklayer agent status <id> → full detail block for one agent
  (or error + exit 1 if ID not found)

GATE:
  RUNS — bricklayer agent list prints table with 3 agents.
  bricklayer agent status idea-os-scribe-01 prints full detail.
  Unknown ID exits 1 with clear message. Empty registry prints
  the new-agent prompt.

BLOCKER:
  bricklayer agent new (Brick 23) adds to this list.

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/agent.py
- cli/main.py
- tests/test_agent_commands.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) bricklayer agent list prints table with ID/NAME/RUNTIME/STATUS columns
2) bricklayer agent list with empty registry prints "No agents registered. Run: bricklayer agent new", exits 0
3) bricklayer agent list with missing registry.yaml prints empty message, exits 0
4) bricklayer agent status <known-id> prints full detail block with all fields, exits 0
5) bricklayer agent status <unknown-id> prints "Agent not found: <id>", exits 1
6) bricklayer agent status with missing registry.yaml prints clear error, exits 1
7) No raw tracebacks on any error path

TEST REQUIREMENTS:
- list: 3 agents in registry → table printed with all 3, exit 0
- list: empty registry → new-agent prompt printed, exit 0
- list: missing registry.yaml → empty list message, exit 0
- status: known ID → full detail block printed, exit 0
- status: unknown ID → error message, exit 1, no raw traceback
- status: missing registry.yaml → clear error, exit 1
- CliRunner integration: both commands via CliRunner, assert exit codes
  and output contains expected fields

OUT OF SCOPE:
- Any write operations to registry.yaml
- bricklayer agent new (Brick 23)
- bricklayer agent deploy (Brick 24)
- Any file outside the FILES list
