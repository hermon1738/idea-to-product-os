BRICK: Brick 15 - documentation update (three-level branching)

WHAT:
  Update README.md to replace the two-level branching section
  with the full three-level model, add the two new commands,
  add a branching hierarchy diagram, update the build loop
  section, and add a parallel features section.

INPUT:
  README.md (current), all Brick 14 shipped commands

OUTPUT:
  README.md updated with:
  1. Branching model section with ASCII diagram
  2. Updated command reference for --phase, close-phase,
     close-feature
  3. Updated build loop section using three-level model
  4. Parallel features section
  5. No references to old two-level model

GATE:
  OUTPUTS — manual read-through confirming all criteria.

BLOCKER:
  Nothing.

WAVE:
  SEQUENTIAL

FILES:
- README.md
- bricklayer/Readme.md
- bricklayer/state.json
- bricklayer/spec.md

ACCEPTANCE CRITERIA:
1) Branching model section
- ASCII diagram shows main → feature → phase → brick hierarchy.

2) Command reference
- bricklayer branch --feature <name>
- bricklayer branch --phase N <name>
- bricklayer branch N <name> (from phase/*)
- bricklayer close-phase
- bricklayer close-feature
All present with descriptions and examples.

3) Build loop
- Shows full session using three-level model.

4) Parallel features
- Explains how two features run as independent branches.

5) No old two-level references
- Zero mentions of old two-level model.

6) No placeholder text
- Zero TODO, TBD, or template boilerplate.

7) No phantom features
- Only commands that currently exist.

TEST REQUIREMENTS:
- No automated tests.
- Gate: manual read-through + pytest -q must show 408 passing.

OUT OF SCOPE:
- Any code changes
- API reference
- Changelog
