# Proposal: High-Frequency In-Memory Dependency Caching

> **Estado: ENTREGADA.** Cerrada el 2026-08-15 y archivada desde
> `devguide/pending_proposals/`. Implementada en `4f2fbec` (condiciones array-safe) y
> `4fccafd` (retirada del auto-instrumentado con `@signal`, precálculo de la firma de
> `when=`, benchmark). Ver la sección «Auditoría e implementación» al final para el
> alcance real y las mediciones. Benchmark: `python benchmarks/decorator_overhead.py`.

## Abstract

We propose introducing a thread-safe, sub-microsecond in-memory caching mechanism for `@dep_digest` checks. This guarantees that repeated dependency checks inside hot scientific loops (e.g., rendering loops or coordinate-update steps) have absolutely zero latency overhead.

---

## The Problem

`@dep_digest` validates the presence of optional dependencies (e.g., `numpy`, `pyunitwizard`) dynamically when functions are called.
Although checking if a module exists in `sys.modules` is generally fast in Python, calling package utilities, checking conda/pypi registry maps, or running validation wrappers repeatedly in high-frequency scientific loops (like processing thousands of atom selections or rendering visual frames at 60 FPS) introduces minor CPU overhead that accumulates over time.

---

## Proposed Solution

Introduce a fast caching registry layer inside `depdigest` to store resolved package availability states.

### 1. The Cache Architecture
* Maintain a simple, thread-safe in-memory cache dictionary (`dict[str, bool]`) recording package installation status:
  ```python
  # depdigest/core.py (Concept)
  _INSTALLATION_CACHE: dict[str, bool] = {}
  ```

### 2. Fast-Path Resolution
When `@dep_digest` or `is_installed` is called:
1. It first checks if the library key exists in `_INSTALLATION_CACHE`.
2. If yes, it returns the boolean status instantly (sub-microsecond execution time).
3. If no (cache miss), it runs the standard validation checks (inspecting `sys.modules`, resolving paths), registers the result in the cache, and returns.

### 3. Cache Invalidation
Since Python packages are rarely installed or uninstalled *mid-session*, the cache can remain persistent throughout the library's import lifespan. If needed, a helper `depdigest.clear_cache()` can be exposed.

---

## Benefits

* **High-Frequency Performance**: Bypasses all validation overhead in recursive, inner scientific loop calls.
* **Safer Integrations**: Encourages developers to keep `@dep_digest` on public wrappers and hot interior functions without fearing a performance regression.

---

## Evidencia medida (2026-07-12), y un defecto que esta propuesta no cubre

Añadido tras perfilar el ecosistema desde MolSysViewer. Ver
`pyunitwizard/devguide/pending_proposals/python_overhead_before_rusterization.md`.

**Esta propuesta estaba escrita sin números. Aquí están.**

Perfilando **300 llamadas** a `puw.get_value` (una conversión de unidades trivial):

- **3.000 invocaciones del wrapper de DepDigest** — **10 por llamada**.
- El trabajo real (pint) es **17 µs de 262 µs** — el **7 %**. El resto es la capa de decoradores.

El cache que propone este documento ataca una parte. **Pero hay dos costes más que se pagan en
cada llamada y que el cache no elimina.**

### Defecto 1: DepDigest se decora a sí mismo con SMonitor

`depdigest/core/decorator.py:58`:

```python
@wraps(func)
@signal(
    tags=["dependency"], exception_level="DEBUG"
)  # ← @signal DE SMONITOR, sobre el wrapper
def wrapper(*args, **kwargs): ...
```

**Cada función con `@digest` paga, además de su propio wrapper, el decorador de SMonitor
completo.** Y el `wrapper` de SMonitor construye el manager y accede a su config **antes** de
comprobar si la telemetría está activada (ver
`smonitor/devguide/pending_proposals/overhead_optimization_and_profiles.md`).

Así que el coste se **multiplica**: DepDigest paga SMonitor, y SMonitor no tiene fast path.

### Defecto 2: `resolve_config()` se ejecuta en cada llamada

```python
def wrapper(*args, **kwargs):
    # 2. RESOLVE CONFIG AT RUNTIME
    # This allows tests to register config AFTER function definition
    cfg = resolve_config(module_path)  # ← en CADA invocación
```

El comentario explica **por qué** (permitir que los tests registren config a posteriori), y es una
razón legítima. Pero el precio se paga en **producción, millones de veces**, por una comodidad que
sólo necesitan los tests.

**Arreglo:** cachear el `cfg` por `module_path` e **invalidar el cache** cuando un test registre
configuración nueva (`depdigest.clear_cache()`, que esta misma propuesta ya contempla para las
dependencias). La comodidad de los tests se conserva; el coste desaparece del camino caliente.

Y si hay un `when=`, se ejecuta además `inspect.signature(...).bind(...)` **por llamada** —
`inspect` es de lo más caro de Python. Ese `sig` puede resolverse **una vez, al decorar**, no en
cada invocación.

### Cómo verificar

```bash
python -c "
import timeit
from pyunitwizard import ...
q = puw.quantity(1.5,'angstroms')
t = timeit.timeit(lambda: puw.get_value(q, to_unit='nanometers'), number=3000)/3000
print(f'{t*1e6:.1f} µs   (hoy: 262 µs | pint desnudo: 17 µs)')"
```

## Auditoría e implementación (2026-07-12)

La caché principal descrita por esta propuesta ya existía antes de esta ronda:

- `is_installed()` usa `lru_cache(maxsize=None)`;
- `resolve_config()` usa `lru_cache(maxsize=128)`;
- registrar, retirar o limpiar configuración invalida la caché;
- la firma de una condición `when=` ya se calcula una vez al decorar.

Por tanto, no se añadió una segunda caché ni una API redundante de invalidación. El defecto real
corregido fue el auto-instrumentado: se retiró `@signal` tanto del wrapper de `dep_digest` como de
`check_dependency`. Una dependencia ausente conserva su diagnóstico explícito mediante el catálogo
de SMonitor; las llamadas exitosas dejan de producir telemetría interna duplicada.

Benchmark reproducible: `python benchmarks/decorator_overhead.py`.

| `@dep_digest("json")`, dependencia presente | antes | después |
|---|---:|---:|
| llamada total | 1.198 ns | 631 ns |
| overhead sobre función desnuda | 1.127 ns | 547 ns |

En la medición integrada de PyUnitWizard, con SMonitor desactivado, `puw.get_value(...)` pasó de
**137,9 µs** tras el fast path de SMonitor a **125,8 µs** tras retirar la instrumentación interna
de DepDigest.

El perfil posterior encontró el coste dominante real: las cinco condiciones `when={"to_form":
...}` de `convert` ejecutaban `Signature.bind()` y `apply_defaults()` en cada llamada, aunque
`to_form` fuera el valor por defecto `None`. DepDigest ahora precalcula la posición y el default de
los parámetros condicionantes; el camino común los resuelve directamente y conserva `bind()` sólo
como fallback para firmas no ordinarias. Con este cambio, la misma operación integrada baja a
**54,1 µs**. La semántica positional/keyword/default está cubierta explícitamente.
