---
summary: Publish the qualified declaration-based registry as DepDigest 0.14.0.
issue: uibcdf/depdigest#35
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: reproduced
area: [release, distribution]
guard: tests/test_staged_conda_install.py::test_declared_registry_gate_rejects_a_suppressed_unrelated_import
normative:
blocked_by: []
supersedes: []
---

# Publish DepDigest 0.14.0

## What

Publish the new public `DeclaredRegistry` API implemented in #34. Diego authorized
the tag and package publication on 2026-10-10. MolSysMT owns its later adoption
and scientific/conversion parity under `uibcdf/molsysmt#382`; impact coordination
remains `uibcdf/molsyssuite#115`.

## How

Adopt immutable SDK `6d6172d6cd00c5ac2d4ebadb71df554ec5b7fa26`, delivered by
`uibcdf/molsyssuite#112`, pairing the route inventory and six SDK checkouts.
Preserve actual workflow LF bytes via Git attributes and review changed workflow
hashes. This retains substantive missing-route/hash/dependency refusals.
The original matrix `38054361890` at `9912b013f8a521fb5e9a20c43d3e32836ad65790`
passes eight Linux/macOS test cells but fails four Windows cells before tests
because native backslashes differ from portable inventory identities.

The committed plan selects 0.14.0 build 0 and staging. The installed verifier
additionally exercises metadata, selective loading, caching and an unrelated
sentinel whose marker exposes even a suppressed failed import. Required archive
resources now include `depdigest/core/registry.py`.

## Why

Implementation closure is not published API admission. A new minor version makes
the capability floor explicit; source, installed and public evidence must agree
before consumers may require it. Historical 0.13.0 source/file/digest remains
unchanged.

## Acceptance criteria

- All twelve source cells and suite policy execute successfully at one final SHA.
- One staging file is built and verified with original producer receipts/digest.
- All twelve clean installed cells exercise the version-applicable new contract.
- Tag 0.14.0 and its stable GitHub Release identify that same candidate SHA.
- Promotion adds main to the same SHA-256-verified file without rebuilding it.
- Independent registry/main solver index and downloaded-file identity pass.
- Public installation verifies version, API, source provenance and CLI.
- Owning issue and normalized release receipt record completed evidence and limits.

## Resolution — 2026-10-10

Published stable tag and Release `0.14.0` on candidate
`affd73ef04070a9bf492173c0db615292a73e5d1`, annotated tag object
`b3ae6cd28743bf84f9547812d9a33e6ee3c82417`. The source matrix `38059326760`
passed all twelve cells; source policy `38059299168` and tag policy
`38063810826` passed. Local Python 3.14.7 qualification passed 239 tests with
no skips. Hosted source CI passed 234 tests and skipped five optional
sibling-workspace cases; these do not establish MolSysMT scientific parity.

Producer `38059892340` built the single staging archive
`depdigest-0.14.0-py_0.tar.bz2`, SHA-256
`3622a95cfb45871c3eed2709b38fc3f5b683b8b73555c1d91253b4b7080737d5`.
Installed run `38060431615` passed producer verification and all twelve
off-checkout installation cells, including the new selective-loading sentinel.
The pinned SDK independently verified every required native job and step.
Promotion `38063846322` added main to that same file without rebuilding it;
the independent public registry/main solver-index verifier and a downloaded-file
hash check passed. A clean public-only-channel Linux/Python 3.14.8 installation
with public SMonitor 0.16.0 `py_1` passed provenance, version, CLI, engine,
audit and declaration-registry checks.

The guard deliberately attempts an unrelated import and suppresses its raised
exception; the sentinel marker still makes qualification fail. It protects the
new installed API against a silent whole-registry load. Original producer,
native-gate, promotion and public verification receipts establish the external
publication claims separately from this local regression assertion.

Documentation deployment `38063824454` passed, and the public registry guide
renders 0.14.0. Zenodo run `38063826679` verified source-snapshot DOI
`10.5281/zenodo.23284363`; its ZIP download matched recorded size and checksum.
The [normalized receipt](../evidence/release_0.14.0_2026-10-10.json) retains exact
source/file/gate identities and scope. MolSysMT #382 and MolSysSuite #115 retain
consumer adoption and scientific/performance validation ownership.
