# Quick Start

This is the fastest way to integrate DepDigest in your library.

Goal:
- keep import-time startup fast,
- guard optional dependencies at runtime,
- provide clear, actionable errors when something is missing.

## Step 1: Install

```bash
conda install -c uibcdf depdigest
```

If you are developing from source:

```bash
python -m pip install --no-deps --editable .
```

## Step 2: Guard a Function

Copy this:

```python
from depdigest import dep_digest

@dep_digest("openmm")
def run_simulation(system):
    import openmm
    return openmm.Platform.getNumPlatforms()
```

Adapt this:
- replace `"openmm"` with your optional dependency key;
- replace function body with your real logic.

What this means:
- the dependency is checked when `run_simulation(...)` is called;
- the import stays lazy (inside the function);
- if `openmm` is missing, users get a readable error with install hints.

## Step 3: Validate Behavior

Try two scenarios:
- with `openmm` installed: function runs;
- without `openmm`: function raises a dependency error and suggests install commands.

## Why This Pattern Matters

Without DepDigest, optional dependencies often leak as top-level imports and
slow down startup for everyone. With DepDigest, only users who need a feature
pay the dependency cost.

## Next

Continue with `Configuration` to centralize dependency policy in `_depdigest.py`.
