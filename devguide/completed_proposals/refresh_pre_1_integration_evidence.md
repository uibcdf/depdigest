---
summary: Refresh pre-1.0 integration evidence and verify consumer dependency diagnostics.
issue: uibcdf/depdigest#26
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [integration, release]
guard: tests/e2e/test_collective_error_path.py
normative:
blocked_by: []
supersedes: []
---

# Refresh pre-1.0 integration evidence

## What

The collective evidence pack still uses the March 0.10.0 baseline. Its E2E
asserts a dimensionality failure and the presence of an installation key but
never exercises a missing dependency or its diagnostic payload.

## How

Run real SMonitor, ArgDigest and PyUnitWizard sources with the current DepDigest
checkout in isolated Python 3.14 processes. Reuse public dependency guards,
introspection and audit operations. Preserve sibling checkouts and record clean
current snapshots for dated evidence. Extend the regression and maintain a
standalone probe with explicit import origins and revisions.

## Why

Stable release preparation needs current evidence and explicit remaining gates.
Local source integration does not grant public artifact qualification or final
collective sign-off.

## Acceptance criteria

- Successful quantity flow and dimensionality failure are checked with real engines.
- A clearly identified integrator fixture tests dependency absence, actionable
  remediation, consumer fields, repeated events and pre-body rejection.
- Optional startup imports are checked independently of static audit results.
- Evidence, roadmap and pre-1.0 checklist reflect observed results and limitations.
- Provider findings receive owner issues; runtime APIs and dependencies stay unchanged.

## Resolution (2026-10-04)

The maintained standalone probe and isolated regression now exercise the real
Pint/ArgDigest/PyUnitWizard quantity flow and a clearly identified integrator
composition with the DepDigest guard. Two simulated missing-unyt calls must
raise before the body and emit rendered, coded diagnostics with installation
routes, consumer fields and a breadcrumb; dict/JSON introspection must agree.
This is the failure mechanism missing from the prior E2E assertions, protected
by the addressable `tests/e2e/test_collective_error_path.py` guard.

The same module runs four fresh import processes. The separate probe tests
reject an invalid workspace and an eager optional import under a module-level
conditional. Five integration cases and two probe tests passed; the complete
qualified Python 3.14 suite passed 148 tests using clean pinned consumer sources.
Repository-wide Ruff check/format, generated indexes and diff checks passed.
The HTML documentation built with the declared profile in a temporary environment.

The [evidence pack](../collective_evidence_pack.md) retains exact source commits,
all twelve import samples, static audit results, simulated-absence limitations
and the historical March checkpoint. The roadmap now identifies #7 as delivered
and the existing versioned introspection schema. The new
[1.0 checklist](../release_1.0.0_checklist.md) separates completed preparation
from candidate-specific artifact gates and owner decisions.

Static module-level audit traversal remains open in DepDigest #27, with its
own queued report. PyUnitWizard #93 owns the template audit exemption/layout
decision. Those handoffs do not imply their implementation or collective
release sign-off. This refresh changes no runtime API, dependency, consumer
checkout or public release. #6/#8 remain deferred.
