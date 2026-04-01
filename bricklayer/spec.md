BRICK: Docs — Repo Documentation Update

WHAT:
  Update the idea-to-product-os repo documentation to accurately
  reflect the current pipeline — a general-purpose software planning
  and build system, not an AI agent company tool.

INPUT:
  Current README.md and docs/pipeline.md

OUTPUT:
  Updated README.md and docs/pipeline.md

GATE:
  - README accurately describes all pipeline stages in correct order
  - Every system file listed with its role
  - No references to "AI agent company" or old Org Schema format
  - Pipeline diagram matches what the system actually does
  - docs/pipeline.md exists and has all 9 sections

BLOCKER:
  New contributors will run the wrong workflow if docs describe the old system.

WAVE:
  SEQUENTIAL

FILES:
- README.md
- docs/pipeline.md
- bricklayer/spec.md
- bricklayer/state.json

ACCEPTANCE CRITERIA:
1) README section 1 (WHAT THIS IS) describes a general-purpose build pipeline
2) README pipeline diagram includes Venture OS, arch-brain, Agent-OS, plan-brain, Claude Code, Bricklayer CLI
3) README system files table includes arch-brain.md
4) Agent-OS listed as conditional (only if AI Layer exists)
5) No reference to "AI agent company" or old Org Schema format anywhere
6) README includes Product Types section (AGENT, WEB_APP, SYSTEM, CLI_TOOL)
7) README Quick Start matches the actual current workflow
8) docs/pipeline.md exists and contains all 9 sections
9) Both files are non-empty and readable

TEST REQUIREMENTS:
- N/A (docs brick) — confirm both files exist and are non-empty

OUT OF SCOPE:
- Any file outside the FILES list
- Changes to system-prompts/ files
- Changes to CLI source code
- Changes to tests
