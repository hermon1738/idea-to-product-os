---
type: community
cohesion: 0.23
members: 15
---

# Agent Registry Module

**Cohesion:** 0.23 - loosely connected
**Members:** 15 nodes

## Members
- [[Agent registry read and write contextagentsregistry.yaml.  WHY THIS EXISTS]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[Append a new agent to the registry.      Validates required fields and checks fo]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[Read and parse registry.yaml, returning the raw dict.      Why it exists Both l]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[Return a single agent dict by ID, or None if not found.      Args         root]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[Return all agents from registry.yaml as a list of dicts.      Args         root]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[Update the status field of an existing agent.      Args         root Repo root]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[Write registry data atomically using a temp file and rename.      Why it exists]] - rationale - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[_read_raw()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[_registry_path()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[_write_atomic()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[add()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[get()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[load()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[registry.py]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py
- [[update_status()]] - code - /Users/hermonmetaferia/Downloads/projects using ai workflow/idea-to-product-os/cli/registry.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Agent_Registry_Module
SORT file.name ASC
```
