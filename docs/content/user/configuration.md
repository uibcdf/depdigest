# Configuration

After your first guarded function, the next step is to centralize dependency
metadata in `_depdigest.py`.

## Why Configure Explicitly

A package configuration gives you:
- one source of truth for dependency names;
- explicit distinction between hard and soft dependencies;
- better installation hints for users.

## Create `_depdigest.py`

Place this file in your package root:

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

## Meaning of Each Field

- `LIBRARIES`: dependency catalog.
- `type`:
  - `hard`: expected as mandatory.
  - `soft`: optional integration.
- `pypi` / `conda`: install names shown in hints.
- `MAPPING`: connects plugin folders to dependency keys (used by `LazyRegistry`).
- `SHOW_ALL_CAPABILITIES`: if `False`, unavailable soft capabilities can be hidden.

## Optional: Custom Exception Class

You can define in `_depdigest.py`:

```python
EXCEPTION_CLASS = MyDependencyError
```

DepDigest supports multiple constructor contracts and falls back to a plain
message when needed.

## Next

Continue with `Conditional Dependencies` to enforce dependencies only for
specific argument combinations.
