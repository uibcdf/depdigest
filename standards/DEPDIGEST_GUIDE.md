# DepDigest Guide (Canonical)

Source of truth for integrating and using **DepDigest** in this library.

Metadata
- Source repository: `depdigest`
- Source document: `standards/DEPDIGEST_GUIDE.md`
- Source version: `depdigest@0.1.1`
- Last synced: 2026-02-06

## What is DepDigest

DepDigest is a lightweight infrastructure library designed to manage **optional dependencies** and **lazy loading**. It ensures that heavy external packages are only checked and imported when strictly necessary, maintaining a "Zero-Cost Startup" for the host library.

## Why this matters in this library

- **Startup Performance**: Prevents accidental top-level imports of optional libraries.
- **Robustness**: Enforces availability at runtime with professional error messages.
- **Dynamic Discovery**: Supports lazy plugin/form registries that respond to user-defined visibility settings.
- **Auditability**: Provides tools to scan the codebase for "leaky" imports.

## Required files in this library

- `_depdigest.py`: Package-level configuration (libraries, mappings, visibility).

## Core API for Developers

### 1. The `@dep_digest` Decorator
Enforce a dependency just-in-time.

```python
from depdigest import dep_digest

@dep_digest('openmm')
def simulate(system):
    import openmm # Safe lazy import
    ...
```

**Conditional Check**:
```python
@dep_digest('mdtraj', when={'to_form': 'mdtraj.Trajectory'})
def convert(item, to_form):
    ...
```

### 2. The `LazyRegistry`
Create a directory-based plugin system that doesn't load everything at once.

```python
from depdigest import LazyRegistry

registry = LazyRegistry(
    package_prefix='A.plugins',
    directory='/path/to/plugins',
    attr_name='plugin_id'
)
```

## Required behavior (non-negotiable)

1.  **Lazy Imports**: Never import an optional dependency at the module top-level. Always import inside the function/method guarded by `@dep_digest`.
2.  **Mapping Integrity**: Every form or plugin that requires an external library **MUST** be mapped in `_depdigest.py`.
3.  **Use get_info**: Expose a user-facing function to report dependency status using `depdigest.get_info('A')`.

## SMonitor Integration

DepDigest is instrumented with `@smonitor.signal(tags=["dependency"])`. Every dependency check and automated loading process is traceable.

## Naming conventions

- **Config symbols**: Use uppercase (`LIBRARIES`, `MAPPING`, `SHOW_ALL_CAPABILITIES`).
- **Keys**: Use importable module names (e.g., `'openmm.unit'`, `'mdtraj'`).

---
*Document created on February 6, 2026, as the authority for DepDigest integration.*
