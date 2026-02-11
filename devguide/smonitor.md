# SMonitor integration

DepDigest uses SMonitor as the single diagnostics layer.

## Files

- `depdigest/_smonitor.py`
- `depdigest/_private/smonitor/catalog.py`
- `depdigest/_private/smonitor/meta.py`

## Rules

- Emit through catalog entries only.
- Keep user messages explicit and helpful.
- Keep URLs in `meta.py` so hints remain consistent.

## Telemetry & Traceability

DepDigest is instrumented with `@smonitor.signal` to ensure that every dependency check and automated loading process is visible in the diagnostic trace.

**Instrumented areas:**
- **Dependency Wrapper**: The `@dep_digest` decorator logic.
- **Dependency Checker**: The `check_dependency` function.
- **Lazy Loader**: The `_scan_and_load` method in `LazyRegistry`.

## Exception signal level

The `@signal` wrapper in `depdigest.core.decorator.dep_digest` uses
`exception_level="DEBUG"`.

Rationale:
- dependency checks can intentionally branch through missing/unavailable states;
- these transitions are part of normal decision flow and often recoverable;
- reporting them as `ERROR` would reduce signal quality in telemetry.
