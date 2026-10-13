---
summary: Publish the qualified adapter-inspection capability as DepDigest 0.15.0.
issue: uibcdf/depdigest#37
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: measured
area: [release, distribution]
guard: tests/test_staged_conda_install.py::test_adapter_inspection_gate_rejects_execution_without_engine_check
normative:
blocked_by: []
supersedes: []
---

# Publish DepDigest 0.15.0

## What

Diego authorized publication on 2026-10-13. Admit explicit selective adapter
inspection from #36, preserving strict default/visibility/execution guards.

## How

Use the existing immutable SDK and staged noarch route, build 0. The installed
verifier adds a version-applicable adapter operation with positive and meaningful
negative guards, and private fixture cleanup on success/failure. Pass source and
installed twelve-cell matrices on one exact candidate; promote the same verified
file after stable tagging/Release. Retain independent registry/index/download and
fresh public install proof. No dependency or consumer floor changes are made here.

## Why

Source implementation closure is not public admission. MolSysMT #382 and central
MolSysSuite #115 require a published capability before public runtime adoption.

## Acceptance criteria

- Final candidate passes source matrix and policy without missing required steps.
- Original producer receipts, resource/version/digest and installed matrix agree.
- Stable 0.15.0 tag and Release identify that same candidate.
- Same verified archive is promoted, independently public/index/download verified.
- Clean public installation exercises the installed new contract and launcher.
- Publication/docs/archival evidence and consumer handoff retain distinct scopes.

## Local preparation — 2026-10-13

Private Python 3.14.8/public SMonitor 0.16.0 py_1 passes 286 source cases with
five unavailable sibling-workspace skips. The new installed gate's positive
check and three mutation controls execute: bypassed execution checks, weakened
strict default and a suppressed unrelated import are all rejected. Its actual
private fixture also cleans on success/injected failure. The default SDK
preflight verifies twenty routes; Ruff and reporting/index checks pass. These
are private source checks, not artifact/public qualification. Required providers,
SDK pin, Python range and historical 0.14.0 artifacts remain unchanged.

## Resolution — 2026-10-13

Stable annotated tag and Release 0.15.0 identify final candidate
`01d83c7b176a2b6cdcbdb42d33f3060f2eda5af7`, tag object
`cfe4bb54b554c5f16383f54a6d4e5da734c59e8c`. Source matrix 38415352585
passes twelve cells on attempt 2; the first attempt's macOS/Python 3.12 cell
failed fetching micromamba before tests, while eleven cells passed. The full
same-source rerun succeeds. Source policy 38415275687, routine CI 38415357505,
publication governance 38415275444 and tag policy 38417378234 pass. The earlier
preparation index mismatch was corrected before fixing this final candidate.

Producer 38416272276 builds exactly one staging archive
`depdigest-0.15.0-py_0.tar.bz2`, SHA-256
`5b888794367e7cd2fd24eac23471b1d26bcbbdfe4d2a14cf77a53f104a110d98`.
Original receipts, independent registry/download and pinned SDK archive checks
agree on version, dependencies and fourteen resources. All non-generated resource
bytes match candidate source. Installed run 38416982119 passes producer checking
and all twelve off-checkout cells, including the 0.15.0 adapter contract. The
pinned native verifier independently checks every required job/step and attempt.

The Release-event selector 38417507371 passes without rebuilding or uploading.
Promotion 38417506809 adds main to the same verified file and retains staging;
its receipt, independent registry/main solver index and public download agree.
A fresh public-only-channel Linux/Python 3.14.8 environment with public SMonitor
0.16.0 py_1 verifies exact distribution/module version, prefix origin, URLs/digest,
fourteen resource hashes, launcher and all engine/audit/registry/adapter contracts.
The guard rejects a mutated unguarded adapter execution and protects the installed
inspection/execution distinction; strict-default and suppressed-sentinel mutations
are independently rejected. Installed smoke is not a complete installed pytest suite.

Documentation 38417507451 passes and its canonical public www guide renders 0.15.0
and the policy. Zenodo 38417508548 independently verifies source-snapshot record
23345127 / DOI `10.5281/zenodo.23345127`; the downloaded source ZIP matches size
465471 and MD5 `ba4ec509e2ebb8f31e1f55584043e148`. No Conda archival is claimed.
[Normalized release proof](../evidence/release_0.15.0_2026-10-13.json) retains
source/file/native/public/installed/archival scopes. Public capability admission is
now DepDigest >=0.15.0; MolSysMT #382 and central #115 own later receiving work.

## Task resource retirement — 2026-10-13

After verified publication and owning/consumer handoffs, Conda removed both exact
private test/public prefixes with exit 0. The reviewed clean pinned SDK clone,
source snapshot, archive/raw read-only receipts and fixtures were retired with
the manifest-owned task root after confirming no active reference. That exact
root is absent; no cleanup error occurred. Required normalized evidence remains
in this repository. Shared environments, primary source/editable metadata, caller
caches and historical releases are preserved. Executed proof:
`devguide/evidence/release_resource_retirement_0.15.0_2026-10-13.json`.
