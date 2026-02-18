# Lazy Registry

When your library exposes many optional modules (formats, plugins, adapters),
`LazyRegistry` helps avoid eager imports at startup.

## Basic Pattern

```python
from depdigest import LazyRegistry

formats = LazyRegistry(
    package_prefix="my_package.formats",
    directory="my_package/formats",
    attr_name="format_name",
)
```

## What Happens Under the Hood

- Directory entries are scanned lazily.
- Each candidate module is imported only when registry is initialized.
- If `MAPPING` links a folder to a soft dependency and capability visibility is
  restricted, unavailable entries can be skipped.
- Plugin import failures are non-fatal and can be reported through diagnostics.

## Required Convention

Each module should expose the attribute used by `attr_name`.

Example:

```python
# my_package/formats/openmm_form/__init__.py
format_name = "openmm"
```

## Recommended Pairing

Use with `_depdigest.py` mapping:

```python
MAPPING = {
    "openmm_form": "openmm.unit",
}
```

## Next

Continue with [Introspection](introspection.md) to show dependency status to
your users.
