# Adopt the shared MolSysSuite policy and Ruff gate

**Status:** Active since 2026-09-06.
**Issue:** `uibcdf/depdigest#3`.
**Suite rollout:** `uibcdf/molsyssuite#6`.

## Proposal

Route suite-wide concerns to the MolSysSuite repository and adopt its immutable
`policy-v1.1.0` caller. Keep DepDigest's product tests, dependency-resolution contracts,
release process, and any stricter local checks under this repository's ownership.

Define the local Ruff baseline explicitly for Python 3.11 with `E4`, `E7`, `E9`, `F`, and
`I`; use Ruff 0.16.5 in the Python 3.13 development environment; and establish the lint
and format baseline in an isolated mechanical commit.

## Evidence before implementation

- `requires-python` is the equivalent canonical range `>=3.11.0,<3.14.0`.
- CI covers Python 3.11, 3.12, and 3.13.
- Ruff 0.16.5 with the common isolated rules reports 39 findings: 21 import-order
  findings, 15 unused imports, and three late-import findings.
- `ruff format --isolated --check .` reports 36 files requiring formatting.
- `python -m pytest -q -p no:cacheprovider` passes 49 tests.

## Acceptance criteria

- Contributor guidance distinguishes suite-wide and repository-local ownership.
- The development environment selects Python 3.13 and Ruff 0.16.5.
- Local Ruff configuration includes the common baseline and does not inherit unrelated
  settings from a parent directory.
- Ruff lint and format checks pass without changing DepDigest behavior.
- The 49-test suite and the shared MolSysSuite workflow pass.
