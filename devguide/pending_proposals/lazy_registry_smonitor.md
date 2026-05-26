# Proposal: LazyRegistry SMonitor Instrumentation

## Abstract

We propose instrumenting `depdigest`'s `LazyRegistry` with `smonitor` diagnostic signals. This enables real-time auditing of when and why optional dependencies (like PyTorch, OpenMM, or MDTraj) are lazily loaded into the session, preventing silent "leaky" imports that degrade package startup times.

---

## The Problem

`depdigest` is critical for ensuring a "Zero-Cost Startup" by lazily importing heavy optional dependencies using `LazyRegistry`.
However, developers currently lack visibility into the loading lifecycle. If a soft dependency gets accidentally imported during normal operations due to a leaky query or eager initialization call:
1. It silently slows down execution.
2. It increases memory footprints.
3. Finding which function or registry entry triggered the import is extremely tedious because the import happens implicitly behind the scenes.

---

## Proposed Solution

Integrate `smonitor` signals directly into `depdigest`'s core lazy-loading mechanisms.

### 1. Instrumentation of `LazyRegistry.import_module`
Whenever `LazyRegistry` resolves and imports a module (or encounters a dynamic entry point), it will emit an SMonitor signal:
```python
# Inside depdigest/registry.py (Concept)
from smonitor import signal

@signal(tags=["dependency", "lazy_load"])
def _load_module(self, module_name):
    # Core lazy import logic
    pass
```

### 2. Traceability Extra Metadata
The emitted signal will record:
* **`module_name`**: E.g., `openmm.unit`.
* **`trigger`**: The attribute or plugin name accessed by the user.
* **`caller`**: The file and line number that requested the registry entry.

---

## Benefits

* **Auditability**: Developers can trace the exact chain of execution that caused a heavy dependency to load.
* **Leaky Import Prevention**: Facilitates writing automated test assertions to ensure that specific actions do *not* trigger optional imports.
* **Zero Overhead**: Inactive unless `smonitor` is enabled, preserving sub-microsecond lazy-registry query performance.
