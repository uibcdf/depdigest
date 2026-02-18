# Showcase

This page highlights common usage patterns.

## Pattern 1: Optional Backend Conversion

Use `@dep_digest` so optional backends are only required when selected:

```python
@dep_digest("openmm", when={"backend": "openmm"})
def run(job, backend="native"):
    if backend == "openmm":
        import openmm
    return job
```

What this gives you:
- fast default path;
- explicit optional-path enforcement;
- clearer user feedback when backend is unavailable.

## Pattern 2: Lazy Plugin Registry

Use `LazyRegistry` to avoid importing all plugins at startup:

```python
from depdigest import LazyRegistry

plugins = LazyRegistry(
    package_prefix="my_pkg.plugins",
    directory="my_pkg/plugins",
    attr_name="plugin_name",
)
```

When this helps most:
- many plugin folders;
- only a small subset used per session;
- optional plugin dependencies.

## Pattern 3: Environment Status Reporting

Surface user-facing dependency status:

```python
from depdigest import get_info

def dependency_status():
    return get_info("my_pkg")
```

Typical place to use it:
- CLI command (`my_pkg deps`);
- diagnostics section in notebooks;
- support/debug output for users.
