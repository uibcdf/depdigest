# Hard vs Soft Dependencies

This distinction is central to using DepDigest correctly.

If you get this right, your library will be both robust and fast to import.

## Quick Definition

- **Hard dependency**:
  required for your library's essential behavior.
- **Soft dependency**:
  optional; only required for specific integrations/features.

In `_depdigest.py`, this is declared with `type`.

## Example

```python
LIBRARIES = {
    "numpy": {"type": "hard", "pypi": "numpy"},
    "openmm.unit": {"type": "soft", "pypi": "openmm", "conda": "openmm"},
}
```

## What DepDigest Does (and Does Not Do)

DepDigest:
- reads your policy from `_depdigest.py`;
- enforces checks where you place `@dep_digest(...)`;
- provides actionable install hints.

DepDigest does **not**:
- install dependencies automatically;
- replace your package manager or environment solver;
- decide architecture for you.

## Should I Use `@dep_digest` for Hard Dependencies?

Short answer:
- for many projects, **no** for most hard dependencies;
- **yes** only when you need uniform runtime diagnostics or delayed imports in
  selected boundaries.

Practical guidance:
- If a dependency is truly hard and required at package startup anyway, regular
  import/packaging constraints are usually enough.
- If you still want standardized runtime error style across hard+soft paths,
  you may guard hard paths too.

In both cases, declare hard dependencies in `LIBRARIES` so policy remains
explicit and introspectable.

## How to Decide the Type

Mark as **hard** when:
- the package is required for core functionality;
- users cannot reasonably use your library without it.

Mark as **soft** when:
- only some workflows need it;
- you can keep default paths fully functional without it.

## Important Practical Rule

Even for soft dependencies, keep imports lazy in guarded paths:

```python
@dep_digest("openmm.unit")
def to_openmm(x):
    import openmm.unit
    ...
```

Avoid top-level imports for soft dependencies.

## Common Mistakes

1. Marking an optional backend as hard:
   users are forced to install unnecessary packages.
2. Marking a core dependency as soft:
   failures appear later and in confusing places.
3. Using install-name aliases as keys:
   keys should be importable module names.

## Recommended Pattern

Treat your dependency list as two layers:
- **hard layer**: minimal, stable, always needed;
- **soft layer**: extensions, adapters, optional formats/backends.

Then guard only the soft layer at runtime with DepDigest.
