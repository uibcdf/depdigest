# Pending proposals

Documents in this directory still require implementation, validation, or an
explicit promotion decision.

See [`../reporting_protocol.md`](../reporting_protocol.md). The entries below are
generated from report metadata.

<!-- generated: devguide_index -->

### Active (1)

- [`guard_conda_release_routes.md`](guard_conda_release_routes.md) — [#15](https://github.com/uibcdf/depdigest/issues/15) — Guard direct Conda releases and promote exact staged files. *(active, inspected)*

### Open (2)

- [`decorator_fast_path_and_observability_boundary.md`](decorator_fast_path_and_observability_boundary.md) — [#6](https://github.com/uibcdf/depdigest/issues/6) — Evaluate an epoch-cached decorator fast path and its observability cost. *(open, measured)*
- [`mapped_dependency_declaration.md`](mapped_dependency_declaration.md) — [#8](https://github.com/uibcdf/depdigest/issues/8) — Declare mapped optional dependencies through one conditional wrapper. *(open, measured)*

<!-- /generated -->

## Context

- The no-contract-change variant of LazyRegistry instrumentation was completed
  under `uibcdf/depdigest#7`; its record is in `../completed_proposals/`.
- `decorator_fast_path_and_observability_boundary.md`: remeasured in 0.11.2
  preparation and deferred until its cache and observability contract is safe.
- `mapped_dependency_declaration.md`: one wrapper instead of one per possible
  backend, for functions that dispatch on a parameter. The mapping's public
  meaning and a real consumer boundary remain undecided, so it stays deferred.

Completed proposals are archived in `../completed_proposals/` with a closing
status header recording where they were implemented.
