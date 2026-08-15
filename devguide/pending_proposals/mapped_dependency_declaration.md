# Proposal: declaring N backends with one wrapper instead of N

**Status:** proposal (2026-08-15). Measured on this host, with the command next to each figure.
**Origin:** PyUnitWizard, where `convert()` carried five stacked `@dep_digest` decorators — one
per optional backend — costing 23% of the call. Recorded in
`pyunitwizard/devguide/dependency_declaration_placement.md`.
**Relation to [`decorator_fast_path_and_observability_boundary.md`](decorator_fast_path_and_observability_boundary.md):**
complementary, not competing. That document makes **each** wrapper cheaper. This one asks why a
dispatcher needs **five** of them. Neither subsumes the other, and this one does not trade away
observability.

---

## 1. The shape of the problem

A function that dispatches on a parameter needs one declaration per possible value:

```python
@dep_digest("unyt", when={"to_form": "unyt"})
@dep_digest("openmm.unit", when={"to_form": "openmm.unit"})
@dep_digest("astropy.units", when={"to_form": "astropy.units"})
@dep_digest("physipy", when={"to_form": "physipy"})
@dep_digest("quantities", when={"to_form": "quantities"})
def convert(quantity_or_unit, to_unit=None, to_form=None, parser=None, to_type="quantity"):
```

Every call pays for all five, and at most one can match. Measured by unwrapping the stack layer by
layer in PyUnitWizard:

| | us |
|---|---:|
| `convert()` decorated | 27.32 |
| `convert()` undecorated | 20.38 |
| **the five layers** | **6.24** |

About half of each wrapper's ~1.25 us is the wrapper frame and `*args, **kwargs` repacking, not the
logic — `resolve_config` is 0.091 us and the library lookup 0.077 us on this host. So this is not
mainly a cost the fast-path proposal can remove: **it is a cost of there being five frames.**

## 2. Why this matters beyond one call site

The cost scales with the number of backends a consumer supports. Adding a seventh backend to
PyUnitWizard would make every conversion slower, whether or not that backend is ever used. That is
a bad incentive to put in front of a library whose purpose is interoperability: it charges a toll
for breadth.

Any consumer with the same shape — a `backend=` / `engine=` / `format=` parameter selecting an
optional dependency — has the same problem.

## 3. The declaration already exists in `_depdigest.py`

`MAPPING` is exactly this table:

```python
MAPPING = {
    'unyt': 'unyt',
    'openmm.unit': 'openmm.unit',
    'astropy.units': 'astropy.units',
    ...
}
```

Today it is consumed only by `LazyRegistry` (`depdigest/core/loader.py:78`) for plugin discovery.
A consumer that uses `@dep_digest` but not `LazyRegistry` — PyUnitWizard is one — declares the same
table twice, in two formats, with no mechanism keeping them in step.

## 4. Sketch

One decorator, resolving the required library from a parameter:

```python
@dep_digest_for(parameter="to_form")          # resolves through MAPPING
def convert(quantity_or_unit, to_unit=None, to_form=None, ...):
```

At call time: read the parameter (the position is already precomputed by
`_condition_parameter_sources`), look it up in `cfg.mapping`, and check that library if there is a
hit. One frame, one dict lookup, same enforcement.

Open design questions, none of them cosmetic:

- **Which mapping?** Reusing `MAPPING` couples this to `LazyRegistry`'s meaning, which is plugin
  discovery, not dependency declaration. They agree in PyUnitWizard, and there is no guarantee they
  agree elsewhere. A separate key is honest but adds a second table to keep in step — the very
  problem this is meant to remove.
- **What does `_dependencies` record?** Today one entry per decorator. A mapped decorator knows the
  whole set at decoration time, so it can record all of them — but only if the mapping is resolved
  eagerly, which contradicts `resolve_config`'s deliberately late resolution.
- **Unmapped values.** A parameter value absent from the mapping should almost certainly be a
  no-op rather than an error, since not every value selects an optional dependency. That needs
  stating, because the silent-no-op reading is also how a typo goes unnoticed.

## 5. How to verify

```bash
# per-wrapper cost, five stacked conditional declarations
python - <<'PY'
import timeit
from depdigest import dep_digest

def base(a, to_form=None): return a
f = base
for lib in ("unyt", "openmm.unit", "astropy.units", "physipy", "quantities"):
    f = dep_digest(lib, when={"to_form": lib})(f)

us = lambda fn: timeit.timeit(lambda: fn(1, to_form="pint"), number=50000) / 50000 * 1e6
print(f"undecorated {us(base):.2f} us   five layers {us(f):.2f} us")
PY
```

On this host: `undecorated 0.09 us   five layers 3.85 us`. Lower than the 6.24 us measured
in PyUnitWizard, as expected -- this toy takes two arguments, and roughly half the per-wrapper
cost is repacking `*args, **kwargs`, which grows with the real signature.

## 6. Recommendation

Worth doing, **after** 1.0.0 and after the two documents it sits beside are decided, because all
three touch the same wrapper. Its case is the strongest of the three in one specific respect: it
buys speed without giving up any information, whereas the fast-path proposal explicitly trades
observability for it.

It is not urgent for PyUnitWizard. That repository removed the declarations from `convert()`
entirely, on the ground that they were misplaced rather than merely expensive: `convert()` imports
no backend, so the enforcement already belonged to its `load_library()`. This proposal matters for
the case that motivates it honestly — a function that *does* import the optional dependency it
dispatches on, and so genuinely needs the declaration at that boundary.
