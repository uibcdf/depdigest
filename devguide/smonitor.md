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
