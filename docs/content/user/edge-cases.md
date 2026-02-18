# Edge Cases

This page documents the recovecos that usually appear during real integration.

## 1. Optional Imports at Top Level

Avoid this:

```python
import mdtraj  # top-level optional import
```

Do this:

```python
@dep_digest("mdtraj")
def to_mdtraj(obj):
    import mdtraj
    ...
```

Reason:
- top-level imports break lazy startup.

## 2. Missing vs Broken `_depdigest.py`

- Missing file:
  DepDigest falls back to a safe default config.
- Broken file (syntax/import error):
  internal error is raised intentionally, so integration bugs are visible.

## 3. Custom Exceptions

If you define `EXCEPTION_CLASS`, DepDigest tries multiple constructor styles and
falls back to a plain message if necessary.

## 4. Runtime Registration in Tests

For tests/dynamic packages:
- `register_package_config(...)`
- `clear_package_configs()`

Clear state between tests to avoid leakage.

## 5. Caching

DepDigest caches:
- installation checks (`is_installed`);
- resolved configuration (`resolve_config`).

In tests, clear caches when changing environment assumptions.

## 6. Diagnostics Availability

DepDigest emits SMonitor catalog events for missing dependencies and loader
issues. If diagnostics emission fails, core behavior still remains robust.
