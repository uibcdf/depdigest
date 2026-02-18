# DepDigest

**DepDigest** is a lightweight Python library for managing **optional dependencies** and **lazy loading** in large analytical or scientific projects.

It helps maintain a "Zero-Cost Startup" by ensuring that heavy external libraries are only checked and imported when actually needed.

## Key Features

- **`@dep_digest` Decorator**: Enforce dependency availability at runtime with clear error messages.
- **Lazy Loading**: Discover and load modules (plugins, forms) from directories only when accessed.
- **Architecture Validation**: Tools to scan your codebase and ensure no top-level imports of soft dependencies leak into your core.
- **Symmetry with ArgDigest**: Designed to work in tandem with argument validation frameworks.
- **smonitor integration**: Structured diagnostics for missing dependencies.
- **Runtime config discovery**: Automatically resolves package `_depdigest.py`.
- **Manual config registration**: Supports dynamic/testing contexts via `register_package_config`.

## Quick Example

```python
from depdigest import dep_digest, get_info

@dep_digest('openmm')
def simulate(system):
    import openmm
    # ...

def dependency_info():
    return get_info("my_package")
```

## smonitor

DepDigest emits structured events when a dependency is missing. Configuration is
loaded from `_smonitor.py` in the package root (`depdigest/_smonitor.py`), and
the catalog lives in `depdigest/_private/smonitor/catalog.py` with metadata in
`depdigest/_private/smonitor/meta.py`.

## Installation

```bash
pip install depdigest
```

## Requirements

- Python `>=3.10,<3.14`
- Runtime dependency: `smonitor`

## Development

Run tests:

```bash
pytest -q
```

Run tests with coverage:

```bash
pytest --cov=depdigest --cov-report=term-missing
```

## License

MIT License.
