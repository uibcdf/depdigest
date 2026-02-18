# Introduction to DepDigest

DepDigest is an orchestration layer for optional dependencies in Python libraries.

It keeps import-time startup light while enforcing dependency requirements where execution actually happens.

## Core capabilities

1. Runtime dependency enforcement

`@dep_digest(...)` validates dependency availability when a guarded function is called.

2. Conditional dependency checks

`when={...}` enforces dependencies only on selected execution paths.

3. Lazy plugin loading

`LazyRegistry` discovers modules lazily to avoid eager startup imports.

4. Integration contracts

`_depdigest.py` defines hard/soft dependency policy and optional plugin mapping.

5. Structured diagnostics

SMonitor integration emits actionable dependency diagnostics with traceability.

6. Architecture audit CLI

`depdigest audit` detects top-level imports of soft dependencies and supports CI-friendly exit codes/JSON output.

7. Structured introspection output

`get_info(..., format="table|dict|json")` supports both human-readable and automation-ready dependency reporting.

## Canonical docs

- User integration path: `docs/content/user/index.md`
- Contributor path: `docs/content/developers/index.md`
- Integration contract: `standards/DEPDIGEST_GUIDE.md`
