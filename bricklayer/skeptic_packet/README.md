# Skeptic Packet

This folder provides deterministic inputs for Skeptic review.

Required files:
- `spec.md` (copy of repo-root `spec.md`)
- `diff.patch` or `diff.txt` (patch/diff of changes)
- `test_output.txt` (latest test output)
- `state_excerpt.json` (relevant excerpt from `state.json`)
- `scoped_files_bundle.md` (full text content of all files listed in `spec.md` FILES scope when present)
- `files_manifest.json` (explicit included/missing file list from scope)

Recommended diff command:
- `git diff > skeptic_packet/diff.patch`

Notes:
- `diff.patch` now includes tracked, staged, and untracked file patches when git is available.
- Use `scoped_files_bundle.md` if the reviewer tool truncates or omits newly created files from patch parsing.

The Skeptic verdict must be written to repo-root `skeptic_verdict.md`.
Approval is rejected unless `skeptic_verdict.md` contains `Verdict: PASS`.
