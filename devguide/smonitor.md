# SMonitor Integration

DepDigest uses SMonitor as the diagnostics backend for dependency orchestration.

## Canonical reference

- `SMONITOR_GUIDE.md` (repository root)

## Relevant files

- `depdigest/_smonitor.py`
- `depdigest/_private/smonitor/catalog.py`
- `depdigest/_private/smonitor/meta.py`

## Integration rules

1. Emit diagnostics through catalog entries (no ad-hoc hardcoded diagnostic strings).
2. Keep catalog/template wiring coherent.
3. Do not silence emission failures with empty exception blocks.
4. Keep traceability for key orchestration paths using `@signal`.

## Exception-level policy

Some dependency checks intentionally explore unavailable states; these paths can use `exception_level="DEBUG"` to avoid noisy false-positive error telemetry.
