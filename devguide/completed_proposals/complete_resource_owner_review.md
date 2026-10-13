---
summary: Complete the owner review of applicable DepDigest resource lifecycles.
issue: uibcdf/depdigest#33
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: measured
area: [development, resources]
guard: tests/test_dev_env_lifecycle.py
normative:
blocked_by: []
supersedes: []
---

# Complete DepDigest resource ownership review

## What

Complete the component review requested by MolSysSuite #104 and DepDigest #33.
The dated expansion in `devguide/resource_lifecycle_review.md` records the actual
applicable development, testing, documentation, build and qualification routes,
retained resources and ownership boundaries. The synchronized common guide and
SDK pin remain unchanged. This is local owner disposition, not a whole-suite or
all-platform compliance declaration.

## How

Source review found four bootstrap failure mechanisms: print/default mode changed
environments, unsourced persist performed setup, editable installation targeted the
caller directory, and a micromamba override could suppress manager errors. Nine
controlled Bash guards failed before the repair and pass afterward, preserving
caller files and manager exit status. The owning bootstrap now previews before
manager calls, requires explicit sourced setup, installs this repository root and
propagates failed creation/update. Requested environments, including partial failed
ones, remain caller-owned; no solver/environment mutation is performed by these
controlled guards.

Six additional staged-verifier lifecycle cases execute real private fixtures on
success and injected failure, prove directory cleanup, restore module/path/config
state and preserve a caller sentinel. Existing create/update guards continue to
protect helper resource custody and failures (#32). Metadata benchmark child
processes complete with timeouts inside owned workspaces; measurement receipts
remain maintained evidence.

Eight exact historical DepDigest paths from central #104 were absent at inspection.
No deletion was performed or attributed. Primary caches/build/documentation/editable
outputs and shared environments are retained with explicit owner disposition.
Task-owned clones, environments and fixtures have an ownership manifest and a
useful lifetime through evidence and issue handoffs; the follow-on authorized #36
extends that lifetime. Final retirement is reported independently of inspection.

## Why

Temporary resource policy requires operation ownership and useful lifetime, not
blanket age-based disposal. Local fixtures and development behavior belong here;
shared runner/cache managers and shared policy belong to their existing owners.
A source review and controlled Linux guards do not certify new public artifact
bytes, native/scientific engines or Windows Bash execution. Published 0.14.0
qualification remains in its existing release receipt.

## Acceptance criteria

- Every applicable local route has an explicit disposition and caller protection.
- Reproduced bootstrap gaps are repaired with meaningful failure guards.
- Executed cleanup, retained resources and unknown historical attribution are distinct.
- Owning results are reported to central #104 without closing its other work.

## Published source closeout — 2026-10-13

Implementation `5744450a0778eb2d801cabd95d61ccda092a823b` was pushed directly
without skipping CI. Exact-head native CI 38375008495, MolSysSuite policy
38375009891 and publication governance 38375009553 pass; GH Run Receptor independently
reports an executed successful CI test job. Owning issues #33 and #31 are closed;
local resource disposition was delivered to MolSysSuite #104 and discovery ownership
to Ackredit #117. Useful manifest-owned resources remain through the separately
authorized #36 follow-on; final disposal is reported separately.

## Owned task retirement — 2026-10-13

After all source/native checks and consumer/owning issue handoffs, the useful
lifetime of the manifest-owned #31/#33/#36 resources ended. Conda removed the exact
private test prefix with exit 0. Reviewed clean pinned SDK/Ackredit clones,
private source/consumer snapshots, wheel fixtures, benchmark environments and
owned test workspaces were retired with the exact task root; the separately
tracked first pytest fixture root was also removed. No active process reference
to either exact root remained. Both paths are confirmed absent and no cleanup
error occurred. Normalized proof is retained in
`devguide/evidence/task_resource_retirement_2026-10-13.json`.

Primary repos/editable metadata, shared environments, caller/tool caches and
generated outputs, unrelated temporary resources and historical release receipts
remain preserved. This is actual disposal of identified current-task resources;
it does not attribute the historical #104 path absences or establish machine-wide
cleanup. The shared Python 3.14 dependency observation was delivered to its
existing maintenance owner MolSysSuite #82; no shared environment was repaired.
