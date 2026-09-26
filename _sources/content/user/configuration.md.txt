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
    "openmm.unit": {
        "type": "soft",
        "pypi": "openmm",
        "conda": "openmm",
        "channel": "conda-forge",
    },
}

DOC_URL = "https://your-project.example/docs/dependencies"

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
- `conda`: Conda package name shown in missing-dependency hints; defaults to
  the import root when omitted.
- `channel`: Conda channel for that package; defaults to `conda-forge`.
- `pypi`: optional PyPI package name. The pip command appears only when set.
- `DOC_URL`: your library's dependency documentation URL, used by both the
  SMonitor event and exception. Without it, the link falls back to DepDigest.
- `MAPPING`: connects plugin folders to dependency keys (used by `LazyRegistry`).
- `SHOW_ALL_CAPABILITIES`: if `False`, unavailable soft capabilities can be hidden.

## Optional: Custom Exception Class

You can define in `_depdigest.py`:

```python
EXCEPTION_CLASS = MyDependencyError
```

DepDigest supports multiple constructor contracts and falls back to a plain
message when needed.

For packages registered in code instead of `_depdigest.py`, pass the same
documentation value as `DepConfig(doc_url="https://your-project.example/docs")`.

## Next

Continue with [Conditional Dependencies](conditional-deps.md) to enforce
dependencies only for specific argument combinations.
