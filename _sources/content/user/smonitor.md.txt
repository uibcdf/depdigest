# SMonitor Integration

DepDigest uses SMonitor as its diagnostics backend.

For most users, this is transparent: you can use DepDigest directly and still
get structured, readable dependency diagnostics.

## What SMonitor Provides in Practice

- Consistent messages for missing dependencies.
- Structured events for debugging and support workflows.
- Breadcrumb-style traceability in instrumented paths.

## Is SMonitor Optional?

In the current DepDigest release, SMonitor is a runtime dependency.

That means:
- you do not need to install/configure it separately in normal use;
- DepDigest will initialize its integration automatically.

## Default Behavior

If a dependency is missing in a guarded path:
- DepDigest raises a dependency error for your application flow;
- SMonitor emits a structured diagnostic event in parallel.

If diagnostics emission fails, core DepDigest behavior remains robust.

When `LazyRegistry` performs its first scan, successful plugin loads can emit
`DEP-DBG-LOAD-002` at `DEBUG` level. Its fields identify the loaded plugin,
module, the registry access that started the scan, and that access's file and
line. A `keys()` or `values()` access still scans all entries; the trigger
names the access, not an individual plugin request. Failed loads retain their
separate `DEP-DBG-LOAD-001` diagnostic.

## Do I Need to Configure SMonitor?

Usually no.

But if your project needs custom diagnostics behavior, you can configure
SMonitor explicitly:

```python
import smonitor

smonitor.configure(
    profile="user",  # or dev / qa / debug
    level="WARNING",
)
```

Example to reduce diagnostics side effects in specific contexts:

```python
import smonitor

smonitor.configure(enabled=False)
```

## Where DepDigest Stores Its Diagnostic Definitions

- Runtime config: `depdigest/_smonitor.py`
- Catalog/meta: `depdigest/_private/smonitor/catalog.py`

If you maintain your own library, keep your equivalent catalog and templates
coherent with your dependency behavior.

## Next

Continue with [Edge Cases](edge-cases.md) for integration pitfalls and
production caveats.
