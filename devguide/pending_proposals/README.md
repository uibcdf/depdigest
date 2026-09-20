# Pending proposals

Documents in this directory still require implementation, validation, or an
explicit promotion decision.

See [`../reporting_protocol.md`](../reporting_protocol.md). The entries below are
generated from report metadata.

<!-- generated: devguide_index -->

### Open (3)

- [`decorator_fast_path_and_observability_boundary.md`](decorator_fast_path_and_observability_boundary.md) — [#6](https://github.com/uibcdf/depdigest/issues/6) — Evaluate an epoch-cached decorator fast path and its observability cost. *(open, measured)*
- [`lazy_registry_smonitor.md`](lazy_registry_smonitor.md) — [#7](https://github.com/uibcdf/depdigest/issues/7) — Instrument LazyRegistry with SMonitor without changing observable semantics. *(open, inspected)*
- [`mapped_dependency_declaration.md`](mapped_dependency_declaration.md) — [#8](https://github.com/uibcdf/depdigest/issues/8) — Declare mapped optional dependencies through one conditional wrapper. *(open, measured)*

<!-- /generated -->

## Context

- `lazy_registry_smonitor.md`: scope reduced to the no-contract-change variant
  and deferred to 1.1.0; the per-entry loading variant remains undecided because
  it would change observable `LazyRegistry` semantics.
- `decorator_fast_path_and_observability_boundary.md`: measured and deferred to
  1.1.0. Must be decided **together** with the document above — one buys speed by
  erasing information, the other buys information at the cost of speed.
- `mapped_dependency_declaration.md`: one wrapper instead of one per possible
  backend, for functions that dispatch on a parameter. Touches the same wrapper
  as the two above, so decide it alongside them; unlike the fast path, it buys
  speed without trading away observability.

Completed proposals are archived in `../completed_proposals/` with a closing
status header recording where they were implemented.
