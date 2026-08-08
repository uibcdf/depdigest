# Optional Backend Routing

This showcase models a common scenario: your library supports multiple engines, but only some users activate optional ones.

## Problem

You want a fast default path while still supporting an optional backend like OpenMM.

## Pattern

Use a conditional dependency check and keep backend import lazy:

```python
from depdigest import dep_digest

@dep_digest("openmm", when={"backend": "openmm"})
def run(job, backend="native"):
    if backend == "openmm":
        import openmm
        return run_openmm(job)
    return run_native(job)
```

## Why this works

- Users on default backend pay zero optional-import cost.
- Optional dependency is enforced only on the path that needs it.
- Missing dependency errors remain explicit and actionable.

## Where to apply

- computational engines;
- export backends;
- optional acceleration providers.
