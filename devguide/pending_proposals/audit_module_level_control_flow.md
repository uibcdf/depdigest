---
summary: Define static audit coverage for imports inside module-level control flow.
issue: uibcdf/depdigest#27
status: open
opened: 2026-10-04
closed:
verification: measured
area: [audit, imports]
guard:
normative:
blocked_by: []
supersedes: []
---

# Audit coverage for module-level control flow

## What

`check_top_level_imports` examines direct import nodes in `tree.body`. An import
under `if True`, `try` or a class body can execute during package import but is
outside that scan. The current syntax-error behavior also intentionally returns
no findings, as protected by an existing test; changing that needs its own
compatibility decision.

## How

At runtime baseline `a056c2fa9962e21c93b7c149118b41f9bf646947`, create a package
with this initializer:

```python
if True:
    import unyt
```

`python -m depdigest audit --src-root pkg --soft-deps unyt --json` returns zero
with no violations. During #26, the independent runtime import probe detected
the equivalent conditional eager-import fixture in
`tests/test_integration_probe.py::test_import_probe_detects_a_conditional_eager_optional_import`.
No current consumer startup leak is inferred from this synthetic reproduction.

## Why

A clean static audit cannot certify absent optional startup imports. Before
strengthening its pre-1.0 guarantee, define module-level control-flow traversal,
delayed function-body exclusions and type-check-only semantics explicitly.

## Acceptance criteria

- Document static coverage and limits.
- Decide and test conditional, try and class-body handling.
- Preserve allowed delayed imports and verify CLI JSON/exit behavior.
- Decide syntax-error handling separately rather than silently altering it.
