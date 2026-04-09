# Agent CLI Module

> Community 14 · 44 nodes · cohesion 0.06

[← Back to index](index.md)

## Nodes

| Node | File | Type |
|------|------|------|
| agent.py | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| agent_deploy() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| agent_list() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| agent_live() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| agent_new() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| agent_status() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| _build_placeholder_map() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| _build_registry_entry() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| _format_detail() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| _format_row() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| _get_template_path() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| _print_deploy_ready() | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | code |
| cli/commands/agent.py — Agent subcommands: list, status, new, deploy, live.  WHY | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Mark a deployed agent as live after VPS confirmation. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Format one agent dict as a fixed-width table row.      Why it exists: Both the h | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Format one agent dict as a labelled detail block.      Why it exists: ``agent st | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Print all agents from registry.yaml as a formatted table.      Why it exists: Op | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Print the full detail block for a single agent by ID.      Why it exists: ``agen | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Return an error message if ``agent_id`` fails format validation, else None. | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Resolve the nanobot template directory path.      Why it exists: The template li | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Build the token→value map used to patch template files.      Why it exists: Temp | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Replace all placeholder tokens in a file in place.      Why it exists: copytree( | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Copy nanobot template and replace all placeholder tokens.      Why it exists: Th | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Create a minimal raw-python Discord bot scaffold.      Why it exists: Raw-python | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Build the registry dict for a newly scaffolded agent.      Why it exists: The re | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Scaffold a new agent directory and register it in registry.yaml.      Validates | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Run a git subcommand in ``cwd`` with a fixed timeout.      Why it exists: All gi | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Print the deploy-ready block with VPS docker commands.      Why it exists: Tony | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Copy a scaffolded agent to the deploy repo, push, and print VPS commands.      V | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| Mark a deployed agent as live in the registry.      Intended for manual invocati | `/Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/commands/agent.py` | rationale |
| *(+14 more)* | | |

## Key Relationships

- **agent.py** `contains` → _format_row() `[EXTRACTED]`
- **agent.py** `contains` → _format_detail() `[EXTRACTED]`
- **agent.py** `contains` → run_agent_list() `[EXTRACTED]`
- **agent_deploy()** `contains` → agent.py `[EXTRACTED]`
- **agent_deploy()** `calls` → run_agent_deploy() `[INFERRED]`
- **agent_deploy()** `rationale_for` → Copy agent to the ai-agents repo, push, and print VPS docker commands. `[EXTRACTED]`
- **agent_list()** `contains` → agent.py `[EXTRACTED]`
- **agent_list()** `calls` → run_agent_list() `[INFERRED]`
- **agent_list()** `rationale_for` → List all agents from registry.yaml in a formatted table. `[EXTRACTED]`
- **agent_live()** `contains` → agent.py `[EXTRACTED]`
- **agent_live()** `calls` → run_agent_live() `[INFERRED]`
- **agent_live()** `rationale_for` → Mark a deployed agent as live after VPS confirmation. `[EXTRACTED]`
- **agent_new()** `contains` → agent.py `[EXTRACTED]`
- **agent_new()** `calls` → run_agent_new() `[INFERRED]`
- **agent_new()** `rationale_for` → Scaffold a new agent directory and register it in registry.yaml. `[EXTRACTED]`
- **agent_status()** `contains` → agent.py `[EXTRACTED]`
- **agent_status()** `calls` → run_agent_status() `[INFERRED]`
- **agent_status()** `rationale_for` → Print the full detail block for a single agent by ID. `[EXTRACTED]`
- **_build_placeholder_map()** `contains` → agent.py `[EXTRACTED]`
- **_build_placeholder_map()** `calls` → _scaffold_nanobot() `[INFERRED]`
- **_build_placeholder_map()** `rationale_for` → Build the token→value map used to patch template files.      Why it exists: Temp `[EXTRACTED]`
- **_build_registry_entry()** `contains` → agent.py `[EXTRACTED]`
- **_build_registry_entry()** `calls` → run_agent_new() `[INFERRED]`
- **_build_registry_entry()** `rationale_for` → Build the registry dict for a newly scaffolded agent.      Why it exists: The re `[EXTRACTED]`
- **_format_detail()** `contains` → agent.py `[EXTRACTED]`
- **_format_detail()** `calls` → run_agent_status() `[INFERRED]`
- **_format_detail()** `rationale_for` → Format one agent dict as a labelled detail block.      Why it exists: ``agent st `[EXTRACTED]`
- **_format_row()** `contains` → agent.py `[EXTRACTED]`
- **_format_row()** `calls` → run_agent_list() `[INFERRED]`
- **_format_row()** `rationale_for` → Format one agent dict as a fixed-width table row.      Why it exists: Both the h `[EXTRACTED]`