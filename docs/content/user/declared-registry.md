# Declaration-based plugin lookup (unreleased)

`DeclaredRegistry` is an additive source capability under
[DepDigest #34](https://github.com/uibcdf/depdigest/issues/34). Public release 0.13.0
does not provide it. Source experiments must identify the exact provider commit;
public adoption must wait for a published version explicitly admitting this API.
No release is authorized by this request. MolSysMT adoption and conversion parity
remain in [MolSysMT #382](https://github.com/uibcdf/molsysmt/issues/382).

The host supplies canonical identity-to-plugin declarations from its catalogue:

```python
from depdigest import DeclaredRegistry

formats = DeclaredRegistry(
    package_prefix="my_package.formats",
    directory="my_package/formats",
    declarations={"native": "native_form", "openmm": "openmm_form"},
    attr_name="format_name",
)

list(formats.keys())      # visible names; no implementation imports
formats.declared_keys()  # all declarations, including hidden optional formats
formats.loaded_keys()    # visible successful caches and manual overrides
native = formats["native"]  # imports only native_form
```

The host owns catalogue parsing, aliases, argument validation and converter
capabilities. DepDigest owns filtering, loading, caching and diagnostics. A plugin,
package initializer or dependency probe can itself import other modules; the registry
cannot suppress those consumer import effects.

## Enumeration and mutation

- `keys()`, iteration, length and membership inspect visible declarations. Membership
  does not certify loadability: failed/stale declarations remain listed.
  `declared_keys()` returns all declarations, including hidden ones.
- `values()` and `items()` are mapping views. Iterating their values, `dict(formats)`,
  `get()`, `pop()` and other operations that request a value can import plugins.
  Failed materialization raises `KeyError`; `get()` returns its default.
- `DeclaredRegistry` implements `MutableMapping`, rather than subclassing `dict`.
  Legacy `LazyRegistry` retains its existing first-access full scan, including keys.
- Declarations preserve input order. New manual identities follow in assignment
  order. An override of a declared identity keeps its position and takes precedence
  over imports and filtering. The host owns that supplied implementation.
- Deletion removes the declaration, override and cached value. `clear()` removes all
  entries without importing anything. Neither operation unloads modules.

## Declaration and discovery policy

Declarations accept a mapping or iterable of `(identity, plugin_key)` pairs. Both
must be nonempty strings, with one canonical identity per plugin. Duplicate identities
or plugin keys raise `ValueError` at construction. A mapping cannot retain duplicates
already discarded by the host's parser.

In filesystem mode plugin keys name immediate package directories using Python
identifiers. The implementation's `attr_name` must match the declaration exactly.
Missing directories, missing attributes and mismatches fail lookup without removing
the declaration or admitting a cached implementation.

Entry-point mode accepts `discovery_mode="entry_points"` and `entrypoint_group` as
with `LazyRegistry`. Declarations refer to entry-point names, also used as configuration
mapping keys. Only the requested entry point's `load()` runs. A missing identity
attribute falls back to its entry-point name. Zero or multiple matches fail before
loading. Modern `select(group=...)` and legacy group dictionaries are supported.

Undeclared plugins are excluded from indexed lookup. Explicit `discover()` imports
eligible undeclared candidates in sorted plugin-key order and adds their identities.
Existing declarations and overrides win; the first newly discovered identity wins.
Failures, missing identities and collisions are diagnosed and skipped. This fallback
may import many implementations and is never triggered by metadata or missing-key
lookup. Successful declarations are not reloaded by discovery.

## Caching, freshness and diagnostics

Successful and failed requests are cached. Failures raise `KeyError` chained from
the cause. Repeated lookups do not retry or repeat load diagnostics. `retry(identity)`
clears one failure and requests it again. `refresh()` clears failures and the registry's
entry-point snapshot, retaining declarations, overrides and successful implementations.
Repeat `discover()` skips failures until refresh. A removed entry point with an already
cached implementation remains usable. Refresh does not unload/reimport modules.
Same-plugin recursive loads raise `KeyError`; independent nested loads work. Loading
is synchronous without concurrent-access synchronization.

Each access or enumeration resolves current package configuration. Registered and
temporary overrides affect an existing registry. Restricted soft capabilities are
hidden, even if cached; restoring visibility exposes the same cached implementation.
With `SHOW_ALL_CAPABILITIES=True`, names stay visible, but requesting an unavailable
soft dependency emits existing availability diagnostics and fails before plugin import.
Hard dependencies remain visible. Manual overrides take precedence over filtering.
Availability does not certify versions or successful scientific execution.

Executable availability follows current PATH. Python availability retains
`is_installed`'s cache: clear it after installation and refresh the registry before
retrying. File-based configuration changes require the existing configuration-cache
discipline; registered overrides invalidate their own cache. Recorded load failures
still need retry/refresh after configuration changes.

Load diagnostics identify the plugin, requested identity trigger and actual call site.
Fallback uses the `discover()` trigger. Emission failures do not discard successful
implementations or replace original load errors.
