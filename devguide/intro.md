# Introduction to DepDigest

DepDigest is an orchestration layer for optional dependencies in Python libraries.

It helps maintain fast import-time behavior while enforcing dependency requirements where execution actually occurs.

## Core capabilities

1. Runtime dependency enforcement

`@dep_digest(...)` validates dependency availability when the guarded function is called.

2. Conditional dependency checks

`when={...}` lets you enforce dependencies only on specific execution paths.

3. Lazy plugin loading

`LazyRegistry` scans and exposes modules lazily to avoid eager startup imports.

4. Integration contracts

`_depdigest.py` acts as the package contract for hard/soft dependencies and optional mapping behavior.

5. Structured diagnostics

SMonitor integration provides consistent, actionable diagnostic signals.

## Canonical docs

- User integration path: `docs/content/user/index.md`
- Contributor path: `docs/content/developers/index.md`
- Integration contract: `standards/DEPDIGEST_GUIDE.md`
