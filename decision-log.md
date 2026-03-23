# Decision Log

## v2 Debt — config.py hardcoded YAML keys

**Brick:** Brick 1 - CLI Scaffold + YAML Loader + Startup Validation
**Date:** 2026-03-23
**Status:** DEFERRED to v2

`cli/config.py` iterates a hardcoded list of top-level keys (`phases`, `tools`, `agents`) when validating paths. If bricklayer.yaml adds new top-level sections with path values, they will be silently ignored.

**Fix in v2:** Replace the hardcoded key list with a generic recursive path-value scan, or introduce a `paths:` top-level section as the canonical place for all path declarations.
