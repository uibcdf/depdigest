# Pending proposals

Documents in this directory still require implementation, validation, or an
explicit promotion decision.

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
