# Implementation Guide

This guide summarizes a practical DepDigest integration flow for a host library.

## 1. Define `_depdigest.py`

Place `_depdigest.py` in your package root and define dependency policy:

```python
LIBRARIES = {
    "numpy": {"type": "hard", "pypi": "numpy"},
    "mdtraj": {"type": "soft", "pypi": "mdtraj"},
    "openmm": {"type": "soft", "pypi": "openmm", "conda": "openmm"},
}

MAPPING = {
    "form_mdtraj": "mdtraj",
    "form_openmm": "openmm",
}

SHOW_ALL_CAPABILITIES = True
```

For the full contract, use:
- `standards/DEPDIGEST_GUIDE.md`

## 2. Guard optional paths with `@dep_digest`

```python
from depdigest import dep_digest

@dep_digest("openmm")
def run_simulation(system):
    import openmm
    ...
```

Use conditional checks when dependency use depends on runtime arguments:

```python
@dep_digest("openmm", when={"engine": "OpenMM"})
def compute_energy(item, engine="Native"):
    if engine == "OpenMM":
        import openmm
        ...
```

## 3. Use `LazyRegistry` for plugin ecosystems

```python
from depdigest import LazyRegistry

plugins = LazyRegistry(
    package_prefix="my_pkg.plugins",
    directory="my_pkg/plugins",
    attr_name="plugin_name",
)
```

## 4. Expose introspection for users and tools

```python
from depdigest import get_info

human_rows = get_info("my_pkg")
machine_payload = get_info("my_pkg", format="dict")
```

## 5. Validate architecture in CI

Use the CLI audit to detect top-level imports of soft dependencies:

```bash
depdigest audit --src-root my_pkg --soft-deps openmm,mdtraj
```

## 6. Follow the guided docs

- Integration tutorial path: `docs/content/user/index.md`
- Contributor/maintenance path: `docs/content/developers/index.md`
