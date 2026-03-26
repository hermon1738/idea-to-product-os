BRICK: Brick 23 - bricklayer agent new

WHAT:
  `bricklayer agent new` scaffolds a new agent directory by cloning
  nanobot-template or creating a raw-python scaffold, filling in
  agent ID and metadata, and registering the agent in registry.yaml.

INPUT:
  Agent ID (--id), runtime flag (--runtime), project name
  (--project), role (--role)

OUTPUT:
  For --runtime nanobot: copies agents/nanobot-template/ to
    context/agents/<id>/, replaces all __PLACEHOLDER__ values in
    agent.yaml, workspace/SOUL.md, workspace/AGENTS.md,
    workspace/USER.md; registers agent in registry.yaml with
    status: stopped.
  For --runtime raw-python: creates context/agents/<id>/ with
    agent.py, Dockerfile, requirements.txt, agent.yaml; registers
    agent in registry.yaml with status: stopped.
  Prints: "Agent scaffolded: context/agents/<id>/"
          "Next: edit workspace/ files, then bricklayer agent deploy"

GATE:
  OUTPUTS — nanobot scaffold created with all placeholders replaced,
  agent registered with status stopped. raw-python scaffold created.
  Duplicate ID exits 1, no files created.

BLOCKER:
  bricklayer agent deploy (Brick 24)

WAVE:
  SEQUENTIAL

FILES:
- cli/commands/agent.py
- tests/test_agent_new.py
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) --runtime nanobot: context/agents/<id>/ created from template, all __PLACEHOLDER__ replaced
2) --runtime raw-python: context/agents/<id>/ created with agent.py, Dockerfile, requirements.txt, agent.yaml
3) agent registered in registry.yaml with status: stopped after scaffold
4) duplicate ID: error, exit 1, no directory created, registry unchanged
5) invalid ID format (spaces, uppercase): error with format hint, exit 1
6) unknown runtime: error listing nanobot/raw-python, exit 1
7) nanobot-template missing: clear error with expected path, exit 1
8) No raw tracebacks on any error path

TEST REQUIREMENTS:
- nanobot: valid args -> directory created, placeholders replaced, registered, exit 0
- nanobot: agent.yaml contains correct id, project, role, sequence, status=stopped
- raw-python: valid args -> directory created with agent.py, Dockerfile, requirements.txt, agent.yaml, exit 0
- raw-python: agent.py contains correct AGENT_ID constant
- duplicate ID -> error, exit 1, no directory created, registry unchanged
- invalid ID (spaces) -> error with format hint, exit 1
- invalid ID (uppercase) -> error with format hint, exit 1
- unknown runtime -> error listing nanobot/raw-python, exit 1
- nanobot-template missing -> clear error with expected path, exit 1
- CliRunner integration: both runtimes, assert exit code, directory existence, registry entry

OUT OF SCOPE:
- bricklayer agent deploy (Brick 24)
- Any file outside the FILES list
