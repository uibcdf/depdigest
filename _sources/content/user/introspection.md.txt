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

## Output Formats

`get_info(...)` supports multiple formats:
- `format="table"` (default): list of readable rows.
- `format="dict"`: structured dictionary for programmatic use.
- `format="json"`: JSON string for CI logs, agents, or tooling.

Example:

```python
from depdigest import get_info

payload = get_info("my_package", format="dict")
payload_json = get_info("my_package", format="json")
```

## Stable Schema Contract

For `dict/json` outputs, DepDigest uses schema:
- name: `depdigest.get_info`
- version: `1.0`

Top-level keys:
- `schema`
- `module_path`
- `dependency_count`
- `installed_count`
- `missing_count`
- `dependencies`

Each dependency entry includes:
- `library`
- `installed`
- `status` (`installed` or `missing`)
- `type` (`hard` or `soft`)
- `package_name` (`pypi`, `conda`)
- `install` (`pypi`, `conda`)

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
