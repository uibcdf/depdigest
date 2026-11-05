---
summary: Confirm inclusive runtime minima without speculative upper bounds.
issue: uibcdf/depdigest#44
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: inspected
area: [distribution, compatibility]
guard:
normative: MOLSYSSUITE_GUIDE.md#dependencies-and-ci-acquisition
blocked_by: []
supersedes: []
---

# Confirm inclusive runtime minima without speculative upper bounds

## What

Review required and optional runtime providers, generated Conda routes and maintained acquisition pins. Keep the justified SMonitor 0.13.0 API floor, Python support bounds and release qualification pins distinct. Exercise public floor and newer provider packages with actual prefix origins; retain untested scope.

## How

Review source `02339c2917588a91ba938575be44816d706b5e27` and the immutable references
in the owning issue. Use task-owned copies/environments for executed checks.
Record exact dispositions, evidence and remaining release/consumer limitations.

## Why

Owner confirmation needs measured scope rather than guide receipt, broad CI or
an assumption that a source update qualifies existing public bytes.

## Acceptance criteria

- Complete the owning issue's metadata/runtime/operation-specific review.
- Retain exact executed versions, checks and limitations.
- Archive this report and regenerate indexes on completion.
- Return an explicit Review completed confirmation to the owner and central tracker.

## Resolution — 2026-11-05

No runtime declaration change was needed. `smonitor>=0.13.0` is aligned in
`pyproject.toml`, `devtools/requirements.yaml`, the generated recipe and all
runtime-bearing environments. Its consumed API is `signal`, `ensure_configured`,
`DiagnosticBundle`, `emit_from_catalog` and `merge_extra`. Public SMonitor 0.13.0
supplies these operations. There is no owned optional runtime extra; optional
engine/package declarations are consumer inputs, not undeclared mandatory
providers. Python bounds, exact feasibility/installed-gate provider pins and
test/docs/build-tool pins retain their distinct purposes. No runtime cap or
exception was introduced or removed.

A private installed DepDigest wheel passed the same 147 existing core, declared
registry, concurrency, decorator, optional-engine and audit checks with public
SMonitor 0.13.0 `py313_1` on Python 3.13.18 and public SMonitor 0.22.1 `py_0` on
Python 3.14.10. Origins were checked in the private prefixes; both `pip check`
results are clean and both preflights verify twenty declared/installed routes.
The API's minimum remains 0.13.0; public 0.13.0 has no Python 3.14 Conda build,
so its actual compatible interpreter was selected rather than fabricating a
3.14 floor qualification. Other minors/platforms and unknown future providers
are not certified. No central dependency graph edge changed.

The normative dependency rule preserves the justified inclusive floor and
forbids a speculative cap. Exact versions, public URLs/digests, selected test
scope and qualification limits are in the retained maintenance receipt.

[Normalized maintenance evidence](../evidence/maintenance_reviews_2026-11-05.json)
retains checked inputs and distinct executed scopes. Owner and central confirmations
link the final adopted commit and hosted controls separately.

Final local checks: 75 selected cases pass without skips with the pinned SDK;
Ruff check/format, generated indexes, relative links and diff checks pass.
