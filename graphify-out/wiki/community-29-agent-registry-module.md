# Agent Registry Module

> Community 29 · 15 nodes · cohesion 0.23

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| registry.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |
| add() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |
| get() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |
| load() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |
| Agent registry: read and write context/agents/registry.yaml.  WHY THIS EXISTS: | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | rationale |
| Return a single agent dict by ID, or None if not found.      Args:         root: | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | rationale |
| Append a new agent to the registry.      Validates required fields and checks fo | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | rationale |
| Update the status field of an existing agent.      Args:         root: Repo root | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | rationale |
| Read and parse registry.yaml, returning the raw dict.      Why it exists: Both l | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | rationale |
| Write registry data atomically using a temp file and rename.      Why it exists: | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | rationale |
| Return all agents from registry.yaml as a list of dicts.      Args:         root | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | rationale |
| _read_raw() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |
| _registry_path() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |
| update_status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |
| _write_atomic() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py` | code |

## Key Relationships

- **registry.py** `contains` → _registry_path() `[EXTRACTED]`
- **registry.py** `contains` → _read_raw() `[EXTRACTED]`
- **registry.py** `contains` → _write_atomic() `[EXTRACTED]`
- **add()** `contains` → registry.py `[EXTRACTED]`
- **add()** `calls` → _read_raw() `[INFERRED]`
- **add()** `calls` → get() `[INFERRED]`
- **get()** `contains` → registry.py `[EXTRACTED]`
- **get()** `calls` → load() `[INFERRED]`
- **get()** `calls` → add() `[INFERRED]`
- **load()** `contains` → registry.py `[EXTRACTED]`
- **load()** `calls` → _read_raw() `[INFERRED]`
- **load()** `calls` → get() `[INFERRED]`
- **Agent registry: read and write context/agents/registry.yaml.  WHY THIS EXISTS:** `rationale_for` → registry.py `[EXTRACTED]`
- **Return a single agent dict by ID, or None if not found.      Args:         root:** `rationale_for` → get() `[EXTRACTED]`
- **Append a new agent to the registry.      Validates required fields and checks fo** `rationale_for` → add() `[EXTRACTED]`
- **Update the status field of an existing agent.      Args:         root: Repo root** `rationale_for` → update_status() `[EXTRACTED]`
- **Read and parse registry.yaml, returning the raw dict.      Why it exists: Both l** `rationale_for` → _read_raw() `[EXTRACTED]`
- **Write registry data atomically using a temp file and rename.      Why it exists:** `rationale_for` → _write_atomic() `[EXTRACTED]`