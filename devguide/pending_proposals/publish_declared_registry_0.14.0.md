---
summary: Publish the qualified declaration-based registry as DepDigest 0.14.0.
issue: uibcdf/depdigest#35
status: open
opened: 2026-10-10
closed:
severity: medium
verification: reproduced
area: [release, distribution]
guard:
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
