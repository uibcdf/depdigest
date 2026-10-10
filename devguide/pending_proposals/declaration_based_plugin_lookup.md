---
summary: Discover declared plugin identities without importing unrelated implementations.
issue: uibcdf/depdigest#34
status: open
opened: 2026-10-10
closed:
severity: medium
verification: reproduced
area: [loader, public-api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Declaration-based plugin lookup

## What

Provide an additive, opt-in registry that enumerates declared canonical identities
without loading implementations and loads only a requested plugin. Preserve the
documented first-access full scan of `LazyRegistry`.

## How

`DeclaredRegistry` owns filtering, selective filesystem/entry-point loading,
implementation/failure caches, explicit retry/refresh, dynamic overrides and
diagnostics. The host supplies canonical declarations and retains aliases,
catalogue parsing and argument/converter validation. Undeclared discovery is an
explicit operation, never a side effect of metadata or missing-key lookup.

The consumer evidence in `uibcdf/molsysmt#382` and `uibcdf/elastnetmt#26` identifies
MolSysMT source `3347a108a19177482dcab4bd73a02374c960cd5e` and editable DepDigest
`ba670098a5b773e7f1570adc47b890d063bd5627`. Three instrumented Linux/Python 3.14.7
workers validating a target name took 3.258–3.408 seconds and added 1,156
`molsysmt.form` module entries. These diagnostic samples are not workflow benchmarks.
The implementation baseline here is `264e16057cbb395a673f5004a4adab798c7ff079`.

## Why

DepDigest owns the reusable operation; MolSysMT should not fork a generic registry
or bypass public argument validation. Consumer scientific/conversion parity is
owned by MolSysMT #382. Ackredit grouped discovery freshness (#31) remains separate.

## Acceptance criteria

- An import-failing unrelated sentinel is untouched by metadata and selective lookup.
- Both discovery modes, visibility policies, current configuration overrides,
  dynamic registrations and deterministic ordering have contract tests.
- Missing/mismatched declarations, duplicates, failed loads, explicit retries,
  discovery fallback and materialization differ clearly from metadata enumeration.
- Diagnostics identify the actual plugin, trigger and caller, preserving load errors.
- Supported interpreter contracts are qualified and legacy tests remain green.
- Public admission is explicit: this is unreleased source, absent from 0.13.0;
  public adoption requires the first published version admitting the API. No new
  release, candidate artifact or publication is authorized by this issue.

## Coordination

The shared impact record is `uibcdf/molsyssuite#115`; it will link the exact
provider source and consumer handoff.
The canonical guide and `docs/content/user/declared-registry.md` define the admission
boundary. Runtime adoption and guide delivery are independent follow-up states.
