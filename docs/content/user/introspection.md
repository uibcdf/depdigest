# Introspection

A common support question is: “Which optional dependencies are installed in my
environment?” DepDigest gives you this with `get_info(...)`.

## Example

```python
from depdigest import get_info

rows = get_info("my_package")
for row in rows:
    print(
        row["Library"],
        row["Status"],
        row["Install (PyPI)"],
        row["Install (Conda)"],
    )
```

## Typical Use Cases

- CLI command like `mytool deps`.
- Notebook diagnostics for users.
- Support/debug reports in issue templates.

## What You Get

Each row includes:
- dependency key,
- installation status,
- dependency type,
- suggested install commands for PyPI and Conda.

## Next

Continue with [SMonitor Integration](smonitor.md) to understand diagnostics
behavior and controls.
