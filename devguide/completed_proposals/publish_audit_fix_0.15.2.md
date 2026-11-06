---
summary: Publish the qualified relative-import audit fix as DepDigest 0.15.2.
issue: uibcdf/depdigest#49
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
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

## Public package delivery — 2026-11-05

Candidate `028f8dd8fdcdbaae4d52897deabb690383379195` passes all twelve source
cells in 42079204173 and all twelve exact-file installed cells in 42111520771.
Producer 42110739688 built the original 32908-byte noarch build once. Annotated
tag and stable Release 0.15.2 identify that same source. Promotion 42133713911
adds main to the original archive, retaining staging and SHA-256
`1da96487be3c1eb870701ee53b97a6341e30a6700a75c6eef5468e9f14dc579c`.
Independent public registry/index/download and a fresh public-only Linux/Python
3.14.10 installation verify file provenance, version, resources, CLI, maintained
contracts, relative-import correction and original MIT notice. Pip check is clean.

The guard named above rejects an actual reversal of the relative-import filter,
protecting the reported false-positive mechanism. Adverse license cases and a
real Windows autocrlf checkout protect the original notice. Source, installed
smoke and consumer/scientific scopes remain distinct in the
[normalized receipt](../evidence/release_0.15.2_2026-11-05.json).

Source-only Zenodo DOI `10.5281/zenodo.23991553` and its downloaded ZIP are
verified. At this delivery checkpoint, docs workflow 42133650004 had generated
0.15.2 successfully, but GitHub Pages was still building commit
`70397d2b936a5fa6b2d8a8d962d70cf2c8e41c24` and the actual audit page served
0.15.1. The report stayed active for that public-page check and closeout. Central
release notice MolSysSuite #170 records actual public package delivery;
MolSysSuite #166 / DockingMT #19 retain independent receiving ownership.

## Final deployed documentation and closeout — 2026-11-05

Pages run 42136997013 passes build, status reporting and deployment at the exact
generated commit above. The actual public audit page returns HTTP 200, renders
0.15.2 and documents the relative-import correction. The receipt preserves the
earlier pending observation without treating the generation workflow as proof
of deployed content. No duplicate Pages build was requested.

The three hosted checks for the public documentary commit
`2f6faa8fa8f36ee07e5df8018463ad8321089141` pass: CI 42139870550, publication
governance 42139871343 and policy 42139871483. Public package and source archive
receiving was handed to MolSysSuite #166 and DockingMT #19 with immutable source
guide/evidence links. Consumer adoption and scientific acceptance remain separate.

This record is archived with the normalized release receipt. Task-owned resource
retirement is recorded separately; shared environments, primary editable version
metadata and historical public tags/artifacts are preserved.
