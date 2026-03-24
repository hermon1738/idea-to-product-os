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

## Commands

### `bricklayer status`

Prints the current brick, last action, and next command from `bricklayer/state.json`.

```
$ bricklayer status
project:     idea-to-product-os
phase:       (STATE.md not found)
brick:       Brick 12 - bricklayer close-session
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

Creates and checks out a `brick/N-name` or `feature/name` branch, and records it
in `state.json`.

```bash
# Start a brick branch
bricklayer branch 13 readme-update
# → branch: brick/13-readme-update

# Start a feature branch
bricklayer branch --feature my-feature
# → branch: feature/my-feature
```

---

### `bricklayer build`

Runs pipeline tools or prints the brick contract. Refuses to run on `main` — create
a branch first.

```bash
bricklayer build                  # Print brick contract from spec.md
bricklayer build --snapshot       # Run snapshot-init (capture baseline file state)
bricklayer build --verify         # Run verify_files_touched.py (scope check)
bricklayer build --test           # Run test suite via run_tests_and_capture.py
bricklayer build --skeptic-packet # Generate skeptic_packet/ evidence bundle
bricklayer build --verdict PASS   # Record verdict, auto-commit, auto-merge to main
bricklayer build --verdict FAIL   # Record FAIL verdict, exit 1
```

`--verdict PASS` on a `brick/` branch:
1. Writes `bricklayer/skeptic_verdict.md`
2. Auto-commits all files declared in `spec.md FILES`
3. Merges the branch to `main` with `--no-ff` and deletes it
4. Runs `update_state.py --complete`

`--verdict PASS` on a `feature/` branch commits and records the verdict but does
not merge — feature branches are merged manually.

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
feat(brick-13): add input validation

Brick: 13 — readme update
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
Branch:        brick/13-readme-update
Brick:         13 — readme update
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

A complete brick follows this 8-step sequence:

```
1. bricklayer branch N name
   → creates brick/N-name, records branch in state.json

2. Update bricklayer/spec.md with the brick contract
   (FILES list, ACCEPTANCE CRITERIA, TEST REQUIREMENTS)

3. bricklayer build --snapshot
   → captures baseline file state before any edits

4. Implement — touch only files listed in spec.md FILES

5. bricklayer build --verify
   → exits 1 if any edited file is not in spec.md FILES

6. bricklayer build --test
   → runs test suite, updates state.json, appends to handover.md

7. bricklayer build --skeptic-packet
   → generates skeptic_packet/ evidence bundle for review

8. bricklayer build --verdict PASS
   → writes verdict, auto-commits, merges to main, closes brick
```

If any step exits 1, stop. Do not advance to the next step until the gate passes.

The skeptic review (between steps 7 and 8) must be done by a different AI than
the one that built the brick. The builder cannot approve its own output.

---

## Known Limitations (v2 debt)

These are real gaps in the current implementation. They do not block normal use
but are worth knowing before hitting them.

**`null` in `state.json` current_brick causes a crash in `bricklayer commit`.**
`state.get("current_brick", "")` does not guard against a JSON `null` value. If
`current_brick` is explicitly set to `null`, the regex call will raise a
`TypeError`. Workaround: keep `current_brick` as a string.

**`bricklayer commit` gives a misleading error when run outside a git repository.**
If the working directory is not a git repo, `_check_staged` returns an empty list
and the user sees "Nothing staged. Use git add first." instead of a not-a-git-repo
error.

**`session-log.md` is overwritten on every `close-session` run.**
There is no append mode or timestamped archive. Each run replaces the previous log.
Commit `session-log.md` to source control before closing a second session if you
need the history.

**`close-session` blocks on network failure.**
If the Groq API is unreachable (DNS failure, rate limit, network partition), the
command fails and no files are written. There is no offline fallback or retry.
The Groq error string is surfaced as-is; HTTP 429 (rate limit) and
prompt-too-large errors do not produce targeted guidance.

**`bricklayer build --verdict PASS` auto-merge can fail on conflict.**
If `main` has diverged from the brick branch since branching, the `--no-ff` merge
will fail. The state is not advanced, but the working tree may be left on `main`.
Resolve the conflict manually and re-run `--verdict PASS`.

**`bricklayer.yaml` validation runs on every command.**
The config loader validates all declared paths on startup. If a path is missing
(e.g. a system prompt file was deleted), every command exits 1 until fixed — even
commands that do not use that path.
