---
summary: Discover declared plugin identities without importing unrelated implementations.
issue: uibcdf/depdigest#34
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: reproduced
area: [loader, public-api]
guard: tests/test_declared_registry.py::test_metadata_and_requested_load_leave_unrelated_sentinel_unimported
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

## Resolution — 2026-10-10

Implemented in `0887c41793582603eb3b1dc3ea70c995c4e71b13`. The guard creates an
unrelated plugin that raises on import, verifies metadata without imports, requests
only the target and asserts that the sentinel never enters `sys.modules`. This
protects the consumer's unnecessary whole-registry initialization mechanism.
The remaining contracts are covered by `tests/test_declared_registry.py` and the
unchanged legacy registry tests in `tests/test_core.py`.

Qualification:

- Linux Python 3.14.7: `python -m pytest --receptor=llm tests`, 235 passed,
  no skips, against clean SDK `1f753e318d8dfa43c5bae1fa127e30ea86fa93b6`.
- Linux Python 3.11.16, 3.12.12 and 3.13.14: 74 directed registry/core/public
  API/import contracts passed per interpreter. Python 3.12 used native pytest
  because the existing environment lacks pytest-receptor; its warning about
  `receptor_rerun_command` is retained, not represented as a receptor pass.
- Source CI `38052403367` passed on the exact implementation SHA. Conda publication
  governance `38052403675` passed. Initial policy `38052403686` failed only on Python
  code-block formatting in the new documentation; the closeout formats both blocks
  and requires a subsequent policy pass before closing the GitHub issue.
- Sphinx HTML built successfully with two existing `myst.header` warnings in
  `docs/index.md:33,39`; strict `-W` therefore fails. Validation labels the build
  `unreleased-issue34`, independently of the stale ignored local version file.
- Ruff lint, full-tree formatting and report-index checks are required at closeout.

Handoffs: MolSysMT #382 comment `6097540923`, ElastNetMT #26 comment `6097545003`
and MolSysSuite #115 comment `6097541204`. They retain public-admission and consumer
validation ownership. No consumer implementation, dependency floor, tag, release
or candidate artifact was changed. The existing Windows preflight rejection remains
separate in DepDigest #30 / MolSysSuite #112; these results do not certify a green
OS matrix or installed/public artifacts.
