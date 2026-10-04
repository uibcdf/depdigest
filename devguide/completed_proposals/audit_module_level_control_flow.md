---
summary: Define static audit coverage for imports inside module-level control flow.
issue: uibcdf/depdigest#27
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [audit, imports]
guard: tests/test_ast_tools.py::test_module_level_blocks_are_audited
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

## Resolution (2026-10-04)

The owning reusable operation in `depdigest/utils/ast_tools.py` now traverses
module/class control flow, including if/try handlers/else/finally, loops, with
and match bodies. Function/async-function bodies and their nested classes remain
delayed. The original reproduction now reports the import at its original line
and exits 1. The guard selector above exercises twelve previously missed block
shapes, preventing the original direct-`tree.body` failure mechanism.

Simple explicit imports of `typing.TYPE_CHECKING`, aliases and negation exclude
only the typing branch. Rebound names, attribute writes, wildcard imports and
unresolved/compound conditions are conservatively scanned. Tests protect class,
exception, loop and pattern-capture shadowing and delayed rebindings. CLI
regressions protect source lines, JSON keys, exit 1 and visible allow-violations
behavior. Existing syntax-error behavior is deliberately retained and documented;
the audit is not a syntax validator or runtime reachability proof.

The qualified Linux/Python 3.14 suite passed 180 tests, including all five
integration cases on the preserved clean consumer snapshots. Coverage was 94%
overall and 99% for the AST utility. Repository-wide Ruff check/format and diff
checks passed; HTML documentation built with the declared temporary docs profile.

The intentionally retained
[`evidence/audit_control_flow_2026-10-04.json`](../evidence/audit_control_flow_2026-10-04.json)
records the scanner digest and before/after audits. ArgDigest now has one source
finding and PyUnitWizard eleven on their pinned #26 snapshots; runtime root-import
checks still pass. The template-only exemption no longer clears the expanded
PyUnitWizard audit. These findings are handed off to ArgDigest #22 and PyUnitWizard
#93 without changing consumer code or adopting blanket exemptions.

MolSysSuite #95 received notice before the provider push and tracks all ten
registered guide consumers, guide synchronization and adoption separately.
The canonical provider guide documents the unreleased change; public DepDigest
0.12.0 is unchanged. The maintained evidence pack retains its historical results
and adds this correction; the 1.0 checklist marks scanner coverage complete but
keeps consumer and candidate gates pending.

Authorized internal development follows direct commits/pushes on main and
applicable CI checkpoints, now stated consistently in CONTRIBUTING.md. PRs are
retained for external contributions and requested owner review.
