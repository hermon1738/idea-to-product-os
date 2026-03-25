# bricklayer-cli — v2 Debt Register
> Tracked technical debt. Review before closing any phase.
> Items here are known limitations, not blocking bugs.

---

## Open Items

| ID | Component | Description | Logged | Priority |
|---|---|---|---|---|
| D-001 | runner.py | subprocess.TimeoutExpired unhandled — tool hang blocks CLI forever | Brick 16 | MEDIUM |
| D-002 | state.py | tmp.rename() PermissionError on Windows when another process holds state.json | Brick 16 | LOW |
| D-003 | branch.py / close_feature.py | Detached HEAD returns "HEAD" which bypasses startswith("feature/") prefix checks | Brick 16 | MEDIUM |
| D-004 | state.py | json.JSONDecodeError not caught on malformed state.json — raw traceback possible | Bricks 2/3/4 | MEDIUM |
| D-005 | build.py | "nothing to commit" blocks --verdict PASS on exploratory bricks with no file changes | Brick 8.5 | LOW |
| D-006 | config.py | Top-level YAML keys hardcoded — new sections added to bricklayer.yaml bypass validation silently | Brick 1 | LOW |
| D-007 | state.py | Schema validation won't scale — pydantic/dataclasses migration flagged | Brick 2 | LOW |
| D-008 | next.py | _ROUTING table hardcoded — should eventually be driven by bricklayer.yaml | Brick 4 | LOW |
| D-009 | make_skeptic_packet.py | git add errors swallowed silently — missing file in spec FILES list gives no warning | Brick 8.5 | LOW |
| D-010 | AGT-SYS-001 | Session Scribe is raw Python — no tool-calling, no memory, no scheduling. NanoBot upgrade planned. | Brick 16 | MEDIUM |

## Closed Items
| ID | Description | Resolved In |
|---|---|---|
| — | — | — |
