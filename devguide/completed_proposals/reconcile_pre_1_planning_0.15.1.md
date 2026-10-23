---
summary: Reconcile pre-1.0 planning with public 0.15.1 and resolved consumer decisions.
issue: uibcdf/depdigest#41
status: resolved
opened: 2026-10-22
closed: 2026-10-22
verification: inspected
area: [documentation, release]
guard:
normative: devguide/release_1.0.0_checklist.md#candidate-specific-gates
blocked_by: []
supersedes: []
---

# Reconcile pre-1.0 planning with public 0.15.1

## What

The maintained roadmap and 1.0 preparation checklist still identify 0.13.0 as
current and leave closed audit-boundary decisions pending. Public 0.14.0,
0.15.0 and 0.15.1 have since delivered declaration-based loading, explicit
adapter inspection and bounded concurrent declared requests.

## How

Reconcile planning against committed release receipts and the owning issues.
Record ArgDigest #22, PyUnitWizard #93 and MolSysSuite #95 as resolved within
their measured audit-boundary scope. Keep the 2026-10-04 integration evidence
dated, the future 1.0 candidate gates unchecked and MolSysMT #382 receiving work
open. Preserve the explicit deferrals in #6, #8 and #40.

## Why

Contributors need accurate delivered capabilities and remaining decisions before
choosing another implementation or release. Historical source integration and
provider publication do not establish future-candidate or consumer acceptance.

## Acceptance criteria

- Current release and capability floors agree with retained release receipts.
- Resolved consumer decisions include their scope and evidence links.
- Remaining 1.0 decisions and exact-candidate gates stay explicitly pending.
- Deferred issues acquire no implementation commitment.
- Archive this record, regenerate indexes and pass reporting checks.

## Resolution — 2026-10-22

The [roadmap](../roadmap.md) and [1.0 checklist](../release_1.0.0_checklist.md)
now identify 0.15.1 as public and link the separate 0.14.0, 0.15.0 and 0.15.1
receipts and capability floors. The roadmap distinguishes unchanged legacy
loading from the delivered selective declared registry. Obsolete future-version
steps were replaced with the remaining decision and exact-candidate sequence.

ArgDigest #22, PyUnitWizard #93 and MolSysSuite #95 were inspected as closed.
The checklist records guarded execution-time imports versus six exact-file
exceptions, with immutable coordination/measurement links and their original
source identities. These are historical owner decisions, not a new runtime or
scientific qualification. MolSysMT #382 was inspected as open; its integration
and acceptance remain consumer-owned. #6/#8/#40 stay deferred.

The original #26 source checkpoint, archived reports and release receipts were
preserved. The checklist labels the 2026-10-04 source evidence explicitly and
keeps every future-candidate gate unchecked. Its durable candidate-specific
rule, cited in `normative`, requires exact source/artifact/integration evidence
before a future release decision. This prevents treating the reconciled
historical results as 1.0 qualification; automated reporting tests validate
lifecycle/index integrity, not network freshness or consumer acceptance.

Validation: the six existing `tests/test_reporting_protocol.py` cases passed
with `--receptor=llm`; regenerated indexes and `git diff --check` passed.
No new tests, integration run, public release or dependency change was needed
for this documentation reconciliation.
