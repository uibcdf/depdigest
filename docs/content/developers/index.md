# Developer

This section documents integration details, contracts, and operational practices
for maintainers embedding DepDigest in their own library.

## 1. Configuration Contract (`_depdigest.py`)

Create `_depdigest.py` in your package root:

```python
LIBRARIES = {
    "numpy": {"type": "hard", "pypi": "numpy"},
    "mdtraj": {"type": "soft", "pypi": "mdtraj"},
    "openmm.unit": {"type": "soft", "pypi": "openmm", "conda": "openmm"},
}

MAPPING = {
    "mdtraj_form": "mdtraj",
    "openmm_form": "openmm.unit",
}

SHOW_ALL_CAPABILITIES = True
```

Recommended additions:
- `EXCEPTION_CLASS = YourDependencyError`
- clear `MAPPING` entries for plugin directories

## 2. Runtime Resolution Model

DepDigest resolves config at runtime (call time), not at decoration time.
This is important for:
- test overrides after import;
- dynamic package registration in plugin environments.

## 3. Runtime Registration (Testing / Dynamic Packages)

```python
from depdigest import DepConfig, register_package_config

register_package_config(
    "my_dynamic_pkg",
    DepConfig(
        libraries={"toolkit": {"type": "soft", "pypi": "toolkit"}},
        show_all_capabilities=False,
    ),
)
```

Use `clear_package_configs()` in tests to avoid cross-test leakage.

## 4. SMonitor Integration Contract

DepDigest uses SMonitor as diagnostics backend. Catalog and templates live in:

- `depdigest/_private/smonitor/catalog.py`
- `depdigest/_smonitor.py`

Practical rules:
- emit diagnostics through catalog entries;
- keep `CODES`/`SIGNALS` wired from catalog as single source of truth;
- preserve fallback behavior if emission fails in non-critical paths.

## 5. Testing Checklist

```bash
pytest -q
```

```bash
pytest --cov=depdigest --cov-report=term-missing
```

Minimum coverage targets for integrations:
- dependency missing path (`check_dependency`);
- conditional decorator behavior (`when=...`);
- lazy registry non-fatal behavior on plugin errors;
- config resolution behavior when `_depdigest.py` is missing vs broken.

## 6. Frequent Integration Mistakes

- Top-level import of soft dependencies.
- Using non-importable keys in `LIBRARIES` (must be importable module names).
- Forgetting to map plugin directories in `MAPPING`.
- Assuming default exception constructor signature only.
