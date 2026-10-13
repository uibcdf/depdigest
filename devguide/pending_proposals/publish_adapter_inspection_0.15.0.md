---
summary: Publish the qualified adapter-inspection capability as DepDigest 0.15.0.
issue: uibcdf/depdigest#37
status: active
opened: 2026-10-13
closed:
severity: medium
verification: measured
area: [release, distribution]
guard:
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
