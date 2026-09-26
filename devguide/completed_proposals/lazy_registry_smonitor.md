---
summary: Instrument LazyRegistry with SMonitor without changing observable semantics.
issue: uibcdf/depdigest#7
status: resolved
opened: 2026-09-07
closed: 2026-09-26
verification: inspected
area: [observability, registry]
guard: tests/test_core.py::test_lazy_registry_success_signal_identifies_trigger_and_caller
normative:
blocked_by: []
supersedes: []
---

# Proposal: LazyRegistry SMonitor Instrumentation

> **Estado: RESUELTA** (2026-09-26). La revisión 2026-08-15 que sigue conserva el
> razonamiento previo; la resolución y su alcance se describen al final.

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

---

## Revisión 2026-08-15

### Qué ya existe

`depdigest/core/loader.py` tiene hoy `@signal(tags=["loader"])` sobre `_scan_and_load`
(`:45`) y la señal de catálogo `plugin_load_failed` / `DEP-DBG-LOAD-001` en el camino de
error (`:90-113`). **Solo se observa el fallo, nunca la carga exitosa**, que es
justamente el caso que la propuesta quiere auditar.

### La premisa de «Zero Overhead» para la señal existente

Cuando se escribió esta propuesta, el `@signal` de SMonitor construía el manager y leía su
config **antes** de comprobar si la telemetría estaba activa. Ya no: en SMonitor 0.12.0,
`smonitor/core/decorator.py:72` abre el wrapper con
`if not runtime.signals_enabled: return fn(*args, **kwargs)`, y el plan por-llamada se
cachea por identidad del `ManagerConfig`. El coste con SMonitor desactivado es una lectura
de bandera. Este análisis previo no incluye la captura de `caller` ni la señal de éxito
que se implementaron después.

### Decisión de diseño pendiente en 2026-08-15

La propuesta asume un `_load_module(module_name)` por módulo, **pero no existe**:
`_scan_and_load` importa todos los plugins de golpe en el primer acceso, y
`__getitem__` / `get` / `__contains__` (`:115-137`) llaman a `_ensure_initialized()` sin
propagar la clave accedida. Por tanto no hay de dónde sacar `trigger`. Dos caminos:

- **(A) Barato.** Propagar la clave: `_ensure_initialized(key)`. El `trigger` pasa a ser
  «qué acceso disparó el escaneo completo», no «qué módulo concreto se pidió». Sin cambio
  de contrato.
- **(B) Fiel a la propuesta.** Carga por-entrada: escanear nombres sin importar, importar
  solo al acceder. **Cambia semántica pública observable** — hoy `keys()` / `values()`
  fuerzan la importación de todo.

### Alcance previsto en 2026-08-15

- **1.1.0 (post-estable):** camino (A). Entrada `lazy_load` en `CATALOG` + `CODES` +
  `SIGNALS` (`extra_required: ["module", "trigger", "caller"]`, nivel `DEBUG`), `caller`
  real en vez del string fijo de `:102`, y tests de «esta acción NO importa X».
- **Sin fecha:** camino (B), solo si aparece un caso real que lo justifique. Hoy es
  especulativo y concentra todo el riesgo.

Separar (A) de (B) es lo que convierte esta propuesta de bloqueada en entregable.
Complementa a `depdigest audit`, que detecta imports top-level de forma estática pero no
puede ver una importación disparada en runtime.

## Resolución 2026-09-26

Se implementó el camino (A), acotado y sin cambiar el contrato de carga:
`LazyRegistry` sigue importando todos los plugins permitidos en el primer
acceso. El catálogo emite `DEP-DBG-LOAD-002` en `DEBUG` por cada carga exitosa,
con `plugin`, `module`, `trigger` y la ubicación real del acceso que inició el
escaneo. `trigger` identifica ese acceso, no afirma que cada plugin fuera
solicitado individualmente. La emisión fallida no impide cargar el plugin.

`tests/test_core.py::test_lazy_registry_success_signal_identifies_trigger_and_caller`
protege la carga diferida, el evento renderizado y la atribución del acceso.
Una prueba adyacente protege el comportamiento cuando SMonitor falla. La
suite local pasó 114 pruebas con una omisión dependiente del entorno. La carga
por entrada del camino (B) queda fuera de este resultado y requeriría un caso
real y una propuesta distinta por su cambio observable de semántica.
