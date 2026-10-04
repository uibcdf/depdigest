---
summary: Publish expanded optional-import audit coverage as DepDigest 0.13.0.
issue: uibcdf/depdigest#29
status: open
opened: 2026-10-04
closed:
verification: asserted
area: [release, audit, distribution]
guard:
normative:
blocked_by: []
supersedes: []
---

# DepDigest 0.13.0 release

## What

Publish #27 as a minor release because unchanged source audits can gain findings
and return 1. Consumer adoption is independently owned by MolSysSuite #95,
ArgDigest #22 and PyUnitWizard #93; it is not a prerequisite for this isolated
provider release. #6 and #8 remain deferred.

## How

The authorized release owner is Diego, from the 2026-10-04 instruction to proceed
with 0.13.0. The committed plan selects staging with build `py_0`. Pin the final
candidate only after release content is committed. Require its twelve-cell source
matrix and suite policy, then build one noarch artifact and qualify that file on
Linux/macOS/Windows with Python 3.11–3.14 and public SMonitor 0.16.0 `py_1`.
The installed gate additionally exercises expanded audit scope, type-only and
delayed exclusions, exact source lines, JSON and visible allow-violations behavior.
Record immutable receipts and digest before tagging or promoting the same bytes.

The generated version file is the runtime version-bearing resource. Conda is
the claimed distribution route; no PyPI publication or wheel claim is added.
The existing dependency/recipe contract remains unchanged. Test environment and
recipe constraints, source imports, archive resources and exact installed
dependency origins must be verified independently of solver success.

Zenodo archival applies to this stabilizing member. Only CITATION.cff is present;
its version/date/repository/authors/license are updated for this release. A bounded
query observed one active release hook, which is not archival proof. Adopt the
shared recovery workflow pinned to MolSysSuite
`ed0d5a9f1a9d5334bb354ca1acc33ae0ec465e77`, with fixed cutoff
`2026-10-04T00:00:00Z`, six-hour scheduled discovery and exact-tag manual recovery.
Its public probe records pending/unavailable/verified separately and retains the
original 72-hour deadline. Source snapshots do not certify Conda archival.

## Why

Publishing the provider allows consumers to adopt independently without delaying
the useful scanner correction. A minor version and explicit migration notes
make its additional audit findings visible to gate owners.

## Acceptance criteria

- Release notes, API/migration guidance, canonical guide and metadata agree.
- Exact candidate source, policy, distribution and installed-audit gates pass.
- Public tag and GitHub Release identify that same candidate.
- Exact staged file is promoted once and public registry/digest/install agree.
- Documentation deployment and bounded archival state are verified separately.
- Consumer owner issues receive exact public provider evidence.
