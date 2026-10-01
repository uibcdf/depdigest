# Plugin Ecosystem with LazyRegistry

This showcase targets libraries with many optional plugins (formats, adapters, protocols).

## Problem

Eager importing of all plugins slows startup and fails unnecessarily when optional plugin dependencies are absent.

## Pattern

Create a lazy registry that discovers modules but imports them only on access:

```python
from depdigest import LazyRegistry

plugins = LazyRegistry(
    package_prefix="my_pkg.plugins",
    directory="my_pkg/plugins",
    attr_name="plugin_name",
)
```

With `MAPPING` configured in `_depdigest.py`, DepDigest can enforce plugin-specific dependencies without loading every plugin at startup.

## Why this works

- startup remains fast even with many plugins;
- failures are localized to the plugin requested;
- architecture scales as plugin count grows.

## Where to apply

- format converters;
- optional IO adapters;
- third-party integration layers.
