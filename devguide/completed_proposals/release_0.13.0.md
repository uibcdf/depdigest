---
summary: Publish expanded optional-import audit coverage as DepDigest 0.13.0.
issue: uibcdf/depdigest#29
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [release, audit, distribution]
guard: tests/test_staged_conda_install.py::test_audit_gate_rejects_old_scanner_clean_result
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

## Resolution (2026-10-04)

Stable tag and GitHub Release 0.13.0 identify candidate
`df771e00e886fd9b12915adf54c1bd75c4b5476c`. Source matrix `37192645716`
passed all twelve cells and suite policy `37192635455` passed. The candidate's
182-test local check includes the five isolated sibling-workspace cases omitted
from hosted source cells; that integration scope is Linux/Python 3.14 only.
Ruff/format, preflight and documentation content checks passed. No required
failed gate is waived.

Producer `37194076957` built one `noarch/depdigest-0.13.0-py_0.tar.bz2`,
SHA-256 `e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`.
Its native identity and two receipts agree. Independent staged download and
archive checks verified metadata, required resources and generated version.
Installed gate `37194436139` passed all twelve cells with public SMonitor
0.16.0 `py_1`, including the new audit contract. The selected guard rejects
the historical scanner's incorrect clean result, preventing qualification of
an installed package that omits conditional imports.

Promotion `37194867340` added main to the same file and passed the pinned
independent registry/solver-index verifier. A separate public download matched
the digest, and a clean Linux/Python 3.14.7 public-channel install verified URL,
digest, dependency, installed origin/version, launcher, engine and audit contracts.
An installed-provider integration with pinned ArgDigest/PyUnitWizard source also
passed, reproducing their one/eleven optional-source findings without claiming
adoption. An initial temporary input included mandatory pint; corrected inputs
now come from each consumer's own optional declaration.

Documentation deployment `37194867145` passed and the public audit page renders
0.13.0 and its typing scope. Hosted archival `37194867696` and an independent
probe verified Zenodo record `23135234`, version DOI
`10.5281/zenodo.23135234`, concept DOI `10.5281/zenodo.22884368` and the sole
source ZIP. Downloaded bytes match size 363891 and
`md5:e10bf97f34997c2fee9c82aa04488508`. This is source-snapshot archival,
not Conda archival. The pinned six-hour/exact-tag recovery route remains active.

The normalized [release receipt](../evidence/release_0.13.0_2026-10-04.json)
retains exact source/artifact identities, input hashes, resolved public closure,
gate scopes, adoption limits and public evidence. Changelog/migration/API/guide
and citation metadata agree. MolSysSuite #95 and consumer owner issues receive
the public provider handoff; their guide/source adoption decisions remain open.
