# SMonitor for Contributors

DepDigest uses SMonitor as its diagnostics layer. This is not optional for internal diagnostics behavior.

## What is mandatory

1. Emit diagnostics through catalog entries, not hardcoded strings.
2. Keep template wiring aligned with the catalog single source of truth.
3. Do not silence emission failures with empty `except` blocks.
4. Use `@signal` on orchestration paths where traceability matters.

Canonical local guide:
- [SMONITOR_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/SMONITOR_GUIDE.md)

## Files you should know

- `depdigest/_smonitor.py`
- `depdigest/_private/smonitor/catalog.py`
- `depdigest/_private/smonitor/meta.py`

## Exception level policy

Some dependency checks intentionally explore unavailable states. In those paths, `exception_level="DEBUG"` is expected to avoid noisy error telemetry for normal branching.

## When changing diagnostics

Before merging, verify:
- new catalog entries have coherent templates and metadata;
- links in diagnostics point to valid docs/issues locations;
- fallback behavior preserves context if emission fails.
