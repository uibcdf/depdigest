---
summary: Adopt immutable Conda v2.3.0 operations in the owned publisher.
issue: uibcdf/depdigest#46
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: inspected
area: [distribution, compatibility]
guard: tests/test_noarch_conda_publication.py
normative:
blocked_by: []
supersedes: []
---

# Adopt immutable Conda v2.3.0 operations in the owned publisher

## What

Review the local build/upload and same-file promotion operations independently. Pin the external v2.3.0 commit without replacing the local workflow, enabling conversion or changing candidate/source/file/digest gates. Preserve output and receipt retention; run local and provider offline contract guards. No upload, promotion or release is commissioned.

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

The two owned root build/upload calls and the separate `/promote` call now pin
immutable v2.3.0 source `87c70b1443d5f22d738ee3ddf812bdbe0152f6c2`, reviewed against
central delivery `95f693be10c9205ab9b912cb53453710a207bf45`. Unneeded deprecated
`mambabuild: false` inputs were omitted. Existing noarch host build, tar.bz2
format and false conversion flags are preserved. The exact-upload and withdrawal
sub-actions are not adopted; no local native/environment profile was replaced.

Required source gates, exact candidate/version/build identity, staging label,
producer paths/evidence outputs, original digest custody, installed qualification
before promotion, label mapping, receipts and independent public verification
remain in place. The two reviewed workflow hashes in the route inventory were
regenerated. Existing positive/negative local guards retain these assertions and
now require the reviewed provider SHA rather than obsolete moving tags.

Twenty-six selected provider tests passed in a task-owned tool venv using
simulated transports, covering active build environment selection, upload helper
refusals, label/digest promotion and producer events. The exact frozen local
publication-governance contract and twenty-route dependency preflight passed.
These are source/administrative checks, not an execution of the real local
publisher, a registry transaction, credential access or installed/public/scientific
qualification. A future authorized candidate must execute the actual route and
retain its own original receipts; old producer identities are not retrofitted.
The existing guard module protects candidate/gate order and same-file promotion,
not merely the provider pin string.

[Normalized maintenance evidence](../evidence/maintenance_reviews_2026-11-05.json)
retains checked inputs and distinct executed scopes. Owner and central confirmations
link the final adopted commit and hosted controls separately.

Final local checks: 75 selected cases pass without skips with the pinned SDK;
Ruff check/format, generated indexes, relative links and diff checks pass.
