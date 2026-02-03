# DepDigest

**DepDigest** is a lightweight Python library for managing **optional dependencies** and **lazy loading** in large analytical or scientific projects.

It helps maintain a "Zero-Cost Startup" by ensuring that heavy external libraries are only checked and imported when actually needed.

## Key Features

- **`@dep_digest` Decorator**: Enforce dependency availability at runtime with clear error messages.
- **Lazy Loading**: Discover and load modules (plugins, forms) from directories only when accessed.
- **Architecture Validation**: Tools to scan your codebase and ensure no top-level imports of soft dependencies leak into your core.
- **Symmetry with ArgDigest**: Designed to work in tandem with argument validation frameworks.

## Quick Example

```python
from depdigest import dep_digest

@dep_digest('openmm')
def simulate(system):
    import openmm
    # ...
```

## Installation

```bash
pip install depdigest
```

## License

MIT License.
