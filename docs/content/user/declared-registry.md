# Declaration-based plugin lookup (from 0.14.0)

`DeclaredRegistry` is the additive public capability implemented under
[DepDigest #34](https://github.com/uibcdf/depdigest/issues/34) and admitted in
**DepDigest 0.14.0**, with publication tracked in
[DepDigest #35](https://github.com/uibcdf/depdigest/issues/35). Public consumers
require a published DepDigest >=0.14.0; 0.13.0 does not provide this API.
Source experiments must identify the exact provider commit. MolSysMT adoption
and conversion parity remain in
[MolSysMT #382](https://github.com/uibcdf/molsysmt/issues/382).

The host supplies canonical identity-to-plugin declarations from its catalogue:

```python
from depdigest import DeclaredRegistry

formats = DeclaredRegistry(
    package_prefix="my_package.formats",
    directory="my_package/formats",
    declarations={"native": "native_form", "openmm": "openmm_form"},
    attr_name="format_name",
)

list(formats.keys())  # visible names; no implementation imports
formats.declared_keys()  # all declarations, including hidden optional formats
formats.loaded_keys()  # visible successful caches and manual overrides
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
soft dependency in the default strict policy emits existing availability diagnostics
and fails before plugin import.
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

## Explicit adapter inspection (from 0.15.0, #36)

DepDigest 0.15.0 adds a keyword-only constructor policy:

```python
adapters = DeclaredRegistry(
    "my_package.formats",
    "my_package/formats",
    {"optional": "optional_form"},
    attr_name="format_name",
    load_policy="adapter",
)
adapter = adapters["optional"]  # inspect Python adapter metadata
```

`load_policy="strict"` is the default and preserves the 0.14.0 pre-import soft
dependency check. Explicit `"adapter"` omits that check when materializing a value;
the requested adapter must still import successfully and match its declared identity.
Unknown policy values raise `ValueError`. This policy is selected per registry and
does not change `LazyRegistry`, dependency configuration, engine choice or inventory.

Current visibility remains authoritative: an absent soft engine is hidden with
`SHOW_ALL_CAPABILITIES=False`, including cached adapters. With all capabilities
shown, an importable adapter may expose metadata while its engine is absent.
Manual caller overrides retain their existing precedence. A plugin initializer
that eagerly imports its engine can still fail; real import and transitive errors
remain chained causes rather than being relabeled as engine absence.

The same identity, failure/success cache, retry/refresh, mutation, diagnostics and
explicit `discover()` rules apply to both policies and discovery modes. Discovery
in adapter policy may inspect eligible absent-engine adapters; it still imports
only when explicitly requested and may visit many implementations. Metadata-only
enumeration and selective indexed lookup retain their scope.

Importability and a successful load event certify adapter materialization only.
`get_info()` still reports actual engine availability. Hosts must keep
`dep_digest`/`check_dependency` at execution-dependent operations; an absent
requested engine still raises, and no alternative engine is selected. Adapter
inspection is not execution, version compatibility or scientific qualification.

This option is **not in published 0.14.0**. Public consumers require DepDigest
>=0.15.0 after its admission under DepDigest #37; preparing these docs is not
publication proof. Source experiments must pin the implementation commit. Source
checks, provider publication, MolSysMT #382 adoption/conversion parity and speed
measurements remain separate, coordinated in MolSysSuite #115.
