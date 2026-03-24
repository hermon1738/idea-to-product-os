# bricklayer-cli

A Python CLI that enforces the Bricklayer build pipeline — a gated, brick-by-brick
software delivery workflow. Each brick has a written contract, a scoped file list,
a test gate, an independent skeptic review, and a hard close step before the next
brick begins. The CLI automates the bookkeeping so the workflow rules are checked
by the tool, not by memory.

---

## Install

```bash
git clone <repo-url>
cd idea-to-product-os
pip install -e .
bricklayer --help
```

Requires Python 3.9+. Dependencies (`typer`, `pyyaml`) are installed automatically.

For `bricklayer close-session`, also install the Groq client:

```bash
pip install groq==0.11.0
```

---

## bricklayer.yaml

`bricklayer.yaml` lives at the repo root and declares where your system prompt files
and pipeline tools are. The CLI walks up from the current directory to find it.

Minimal working example:

```yaml
phases:
  review: system-prompts/sprint-brain.md

tools:
  verify: bricklayer/tools/verify_files_touched.py
  test:   bricklayer/tools/run_tests_and_capture.py
  skeptic: bricklayer/tools/make_skeptic_packet.py
  state:  bricklayer/tools/update_state.py

agents: {}
```

All paths are relative to `bricklayer.yaml`. The CLI exits 1 with a clear error if
any declared path does not exist.

---

## Branching Model

Work is organized in three nested levels. Each level must be created from its
correct parent branch — the CLI enforces this and exits 1 if the parent is wrong.

```
main
 └── feature/reddit-monitor          (created from main)
      ├── phase/1-scaffold            (created from feature/*)
      │    ├── brick/1-cli-entry-point (created from phase/*)
      │    └── brick/2-state-reader
      └── phase/2-build-loop
           └── brick/5-build-contract
```

Merge direction is always upward:

```
brick/* → phase/*   (via bricklayer build --verdict PASS)
phase/* → feature/* (via bricklayer close-phase)
feature/* → main    (via bricklayer close-feature)
```

The merge target at each level is read from `bricklayer/state.json` fields
`current_phase` and `current_feature`, which are set automatically when you
create branches with the `bricklayer branch` command.

### Parallel features

Two features can run simultaneously as independent branches from `main`:

```
main
 ├── feature/reddit-monitor
 │    └── phase/1-scaffold
 │         └── brick/1-api-client
 └── feature/auth-system
      └── phase/1-login-flow
           └── brick/1-jwt-handler
```

Each feature branch is isolated. Merging one feature to `main` does not affect
the other. Coordinate merge order manually to resolve any conflicts.

---

## Commands

### `bricklayer status`

Prints the current brick, last action, and next command from `bricklayer/state.json`.

```
$ bricklayer status
project:     idea-to-product-os
phase:       (STATE.md not found)
brick:       Brick 14 - three-level branching upgrade
last action: Tests PASS (exit 0)
next:        skeptic_packet_ready
```

---

### `bricklayer next`

Prints the single next CLI command to run based on `state.json`. Use this when
resuming mid-brick and you need to know where you left off.

```
$ bricklayer next
bricklayer build --verdict PASS|FAIL
```

---

### `bricklayer branch`

Creates and checks out a branch at the correct level. Enforces the parent branch
rule — exits 1 if you are on the wrong parent.

```bash
# Create a feature branch (must be on main)
bricklayer branch --feature reddit-monitor
# → branch: feature/reddit-monitor

# Create a phase branch (must be on a feature/* branch)
bricklayer branch --phase 1 scaffold
# → branch: phase/1-scaffold

# Create a brick branch (must be on a phase/* branch)
bricklayer branch 14 three-level-branching
# → branch: brick/14-three-level-branching
```

Branch names are slugified automatically. State fields `current_feature`,
`current_phase`, and `current_branch` are updated on creation.

---

### `bricklayer build`

Runs pipeline tools or prints the brick contract. Refuses to run on `main`.

```bash
bricklayer build                  # Print brick contract from spec.md
bricklayer build --snapshot       # Run snapshot-init (capture baseline file state)
bricklayer build --verify         # Run verify_files_touched.py (scope check)
bricklayer build --test           # Run test suite via run_tests_and_capture.py
bricklayer build --skeptic-packet # Generate skeptic_packet/ evidence bundle
bricklayer build --verdict PASS   # Record verdict, auto-commit, merge to parent
bricklayer build --verdict FAIL   # Record FAIL verdict, exit 1
```

`--verdict PASS` detects the current branch level and merges to the correct parent:

| Branch level | Merges to |
|---|---|
| `brick/*` | `current_phase` from state.json |
| `phase/*` | `current_feature` from state.json |
| `feature/*` | `main` |

After merging, the branch is deleted and `update_state.py --complete` runs.

---

### `bricklayer close-phase`

Merges the current `phase/*` branch into its parent `feature/*` branch, then
deletes the phase branch. Exits 1 if you are not on a `phase/*` branch.

```
$ bricklayer close-phase
Merged phase/1-scaffold → feature/reddit-monitor. Branch deleted.
Phase merged to feature/reddit-monitor. Start next phase with: bricklayer branch --phase N name
```

---

### `bricklayer close-feature`

Merges the current `feature/*` branch into `main`, then deletes the feature branch.
Exits 1 if you are not on a `feature/*` branch.

```
$ bricklayer close-feature
Merged feature/reddit-monitor → main. Branch deleted.
Feature merged to main. Branch deleted.
```

---

### `bricklayer commit`

Commits staged files with an auto-formatted brick ID message. Use this for
mid-brick checkpoints between the snapshot and verify steps.

```bash
git add path/to/file.py
bricklayer commit -m "add input validation"
```

Output commit message format:

```
feat(brick-15): add input validation

Brick: 15 — documentation update (three-level branching)
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

Exits 1 if nothing is staged, if `-m` is omitted, or if the message is empty.

---

### `bricklayer pause`

Writes `HANDOFF.json` and `.continue-here.md` at the repo root. Run this before
ending a session so the next session can pick up exactly where you left off.

```bash
bricklayer pause
# written: HANDOFF.json
# written: .continue-here.md
```

`HANDOFF.json` captures: project, brick number, brick name, last action, loop
count, current branch, timestamp, and next command.

---

### `bricklayer resume`

Reads `HANDOFF.json` and prints a formatted context block for session restart.
If the current branch does not match the branch recorded in `HANDOFF.json`, a
warning is printed but the command still exits 0.

```
$ bricklayer resume
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESUMING SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project:       idea-to-product-os
Branch:        brick/15-docs-branching-update
Brick:         15 — documentation update (three-level branching)
Last action:   snapshot_init
Loop count:    0
Timestamp:     2026-03-24T10:00:00+00:00
Next command:  bricklayer build --snapshot
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### `bricklayer close-session`

Calls the Groq API to run a sprint review using `system-prompts/sprint-brain.md`
as the system prompt and the current `state.json` as the user message. Writes the
output to `session-log.md` and updates `STATE.md`.

Requires `GROQ_API_KEY` in the environment:

```bash
export GROQ_API_KEY=gsk_...
bricklayer close-session
# Session closed. Next session:
#   bricklayer resume
```

Exits 1 with a clear error if `GROQ_API_KEY` is missing, `state.json` is not
found, `sprint-brain.md` is not at the path declared in `bricklayer.yaml`, or
the Groq API call fails. No files are written on failure.

---

## The Build Loop

A complete brick follows this sequence. Steps must be run in order — each step
gates the next.

```
1. bricklayer branch --feature <name>        (from main)
   bricklayer branch --phase N <name>        (from feature/*)
   bricklayer branch N <name>                (from phase/*)

2. Update bricklayer/spec.md with the brick contract
   (FILES list, ACCEPTANCE CRITERIA, TEST REQUIREMENTS)

3. bricklayer build --snapshot
   → captures baseline file state before any edits

4. Implement — touch only files listed in spec.md FILES

5. bricklayer build --verify
   → exits 1 if any edited file is not in spec.md FILES

6. bricklayer build --test
   → runs test suite, updates state.json

7. bricklayer build --skeptic-packet
   → generates skeptic_packet/ evidence bundle for independent review

8. bricklayer build --verdict PASS
   → writes verdict, auto-commits, merges brick → phase, closes brick

9. bricklayer close-phase                    (when all bricks in phase done)
   → merges phase → feature

10. bricklayer close-feature                 (when all phases in feature done)
    → merges feature → main
```

The skeptic review (between steps 7 and 8) must be done by a different AI than
the one that built the brick. The builder cannot approve its own output.

---

## Known Limitations (v2 debt)

These are real gaps in the current implementation.

**Manual `git checkout` desyncs state.json.**
If you use `git checkout` directly to switch branches instead of `bricklayer branch`,
the `current_feature` and `current_phase` fields in `state.json` will not update.
The automated merge routing in `--verdict PASS` and `close-phase` will then fail or
merge into a stale target. Always use `bricklayer branch` to create and switch
branches.

**Merge conflicts leave the working tree in MERGING state.**
If a merge fails (e.g., during `close-phase` or `--verdict PASS`), the command
exits 1 but does not run `git merge --abort`. Resolve the conflict manually with
`git merge --abort` or by resolving and committing the conflict, then re-run
the command.

**`null` in `state.json` current_brick causes a crash in `bricklayer commit`.**
`state.get("current_brick", "")` does not guard against a JSON `null` value. If
`current_brick` is explicitly set to `null`, the regex call will raise a
`TypeError`. Workaround: keep `current_brick` as a string.

**`bricklayer commit` gives a misleading error when run outside a git repository.**
If the working directory is not a git repo, `_check_staged` returns an empty list
and the user sees "Nothing staged. Use git add first." instead of a not-a-git-repo
error.

**`session-log.md` is overwritten on every `close-session` run.**
There is no append mode or timestamped archive. Commit `session-log.md` to source
control before closing a second session if you need the history.

**`close-session` blocks on network failure.**
If the Groq API is unreachable, the command fails and no files are written. There
is no offline fallback. HTTP 429 (rate limit) and prompt-too-large errors do not
produce targeted guidance.

**`bricklayer build --verdict PASS` auto-merge can fail on conflict.**
Resolve manually with `git merge --abort` (or fix the conflict), then re-run
`--verdict PASS`.

**`state.json` is a single-developer file.**
The branch hierarchy tracking (`current_feature`, `current_phase`) lives in a
local JSON file that is not designed for multi-developer synchronization. This
tool is intended for solo or single-AI-builder workflows.
