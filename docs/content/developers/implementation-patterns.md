# Implementation Patterns

Use this page as a practical blueprint when adding or changing features.

## 1. Keep dependency checks close to execution

Use `@dep_digest` on functions that require optional dependencies, and keep the corresponding imports inside function bodies.

Pattern:

```python
from depdigest import dep_digest

@dep_digest("openmm")
def run_simulation(system):
    import openmm
    ...
```

This preserves fast import time and clear runtime diagnostics.

## 2. Define dependency policy in `_depdigest.py`

`_depdigest.py` is the integration contract used by DepDigest.

Minimum fields:
- `LIBRARIES`;
- optional `MAPPING` for plugin directories;
- optional `SHOW_ALL_CAPABILITIES`;
- optional `EXCEPTION_CLASS`.

Contract reference:
- [DEPDIGEST_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/standards/DEPDIGEST_GUIDE.md)

## 3. Use runtime registration only where it is justified

`register_package_config` is useful for tests and dynamic package systems. Avoid overusing it for static packages where `_depdigest.py` is available.

## 4. Treat hard vs soft correctly

- Hard dependencies: required for base package behavior.
- Soft dependencies: optional capabilities that must fail gracefully when unavailable.

If this boundary is wrong, users either get unnecessary hard requirements or unclear runtime failures.

For detailed semantics, see [Hard vs Soft](../user/hard-vs-soft.md).

## 5. Enforce lazy-import architecture continuously

Use the CLI audit in local checks and CI:

```bash
depdigest audit --src-root my_pkg --soft-deps openmm,mdtraj
```

This catches top-level imports of soft dependencies before they become startup regressions.
