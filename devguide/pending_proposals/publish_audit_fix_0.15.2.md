---
summary: Publish the qualified relative-import audit fix as DepDigest 0.15.2.
issue: uibcdf/depdigest#49
status: active
opened: 2026-11-05
closed:
verification: inspected
area: [release, distribution]
guard: tests/test_staged_conda_install.py::test_audit_gate_rejects_relative_false_positives
normative:
blocked_by: []
supersedes: []
---

# Publish DepDigest 0.15.2

## What

Diego authorized tag and package publication on 2026-11-05. Publish the #47/#48
relative-import correction and #45/#46 metadata/publisher maintenance through
the reviewed staged route. Runtime APIs and dependency bounds are unchanged.

## How

Commit the exact candidate plan before any dispatch/tag. Pass twelve source
cells and policy, build one staging archive, inspect original receipts and
license/resources, then pass all twelve installed cells, including the new
relative-import and original-license checks. Tag the same source, publish the
Release titled exactly 0.15.2 and promote the same SHA-256-verified bytes.
Independently verify public registry/index/download/clean installation, deployed
docs and source-only Zenodo archive. Keep all scopes and limitations distinct.

## Why

Accepted source and private builds do not admit a public provider. Consumers
need an actually published correction instead of a development source pin.

## Acceptance criteria

- Final source and exact installed matrices pass without missing required cells.
- New adverse controls reject false-relative findings and changed license payloads.
- Producer/tag/file/digest/public identities agree; no rebuild or overwrite occurs.
- Docs/archive evidence and consumer handoffs retain their actual scopes.
- Archive this report, retain normalized receipts and retire owned task resources.

## Local preparation — 2026-11-05

A private Python 3.14/public SMonitor 0.16.0 py_1 environment passed 334 source
cases and skipped five unavailable sibling-workspace integration cases; those
skips establish no consumer/scientific qualification. Pip check is clean and
the pinned SDK verifies twenty distribution routes. The new installed-audit
operation rejects an actual isolated reversal of the relative-import fix;
license guards reject wrong expressions/declarations, missing notices and
changed original bytes. Ruff/format/index/diff checks pass. Local source is an
editable 1+unknown snapshot, separate from the future exact Conda artifact.

## Superseded source preparation — 2026-11-05

Candidate 9905afa8ab13aa821a9b426d57daf16098f213e2 passed routine source CI,
policy and publication governance. Full matrix 42077818845 exposed a new
Windows source-fixture failure: Git autocrlf transformed the original LICENSE
notice to CRLF, while the release guard requires canonical LF bytes. The
license's actual text and committed blob were unchanged. Completed Windows
jobs 127422625686/127422625137 failed before package construction. The run
was canceled once the mechanism was known; successful/failed/canceled cells
retain their original outcomes and cannot qualify a later candidate.

The correction pins LICENSE to LF in .gitattributes. The existing real
autocrlf-checkout regression now also compares LICENSE bytes; it fails against
the old rule and passes with the correction. The new candidate must rerun the
complete exact-source matrix. No staged or public file was created at the old SHA.
