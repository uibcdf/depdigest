---
summary: Review inherited Python ecosystem policy in DepDigest.
issue: uibcdf/depdigest#18
status: active
opened: 2026-09-24
closed:
verification: measured
area: [governance, dependencies, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review inherited Python ecosystem policy in DepDigest

## What

MOLI's pinned Python developer-tools and support-library policies now apply to
DepDigest through MolSysSuite. The earlier guide copy and compatible policy caller
do not establish adoption. Before this review, all three hosted pytest workflows
used pytest-receptor's local `llm` profile, and the generated test environment
allowed any version at or above 1.1.0. The published 1.1.0 release is already
used in the isolated Python 3.14 feasibility environment.

## How

Pin pytest-receptor 1.1.0 in the canonical test requirements and regenerate the
derived Conda environments. Select the `ci` profile in routine CI, the full
12-cell matrix, and the Python 3.14 feasibility workflow without changing test
selection, coverage, or exit status. Configure receptor rerun commands for the
repository's `python -m pytest` invocation. Keep the `llm` profile for agent-driven
local pytest. GH Run Receptor already has a repository profile file; use its
published release for first inspection of the exact-commit hosted runs and
fall back to native GitHub evidence when needed.

Review the inherited support-library boundaries independently:

- SMonitor is applicable and already provides missing-dependency and plugin-load
  diagnostics. `tests/test_core.py` exercises emitted signals and the error
  behavior when emission fails.
- ArgDigest depends on DepDigest. DepDigest has several public argument checks,
  but adding ArgDigest to this library would create a runtime dependency cycle.
  Resolve their contract through `uibcdf/depdigest#18` without introducing that
  cycle; the support-library review remains partial meanwhile.
- DepDigest itself implements the optional dependency loading and explanation
  boundary, so importing DepDigest into its own package is inapplicable.
- No physical quantity parsing, conversion, or dimensional validation boundary
  was found in DepDigest, so PyUnitWizard is inapplicable.

## Why

The CI profile and exact release pin make the inherited developer-tools rule
observable. Keeping the support-library review partial prevents a false claim
that a known applicability question has been resolved.

## Evidence and current state

Commit `19a478ba5e2b99a65de71616d6a920f02866253f` contains the developer-tool
changes. The isolated local checkout passed 104 tests with
`python -m pytest --receptor=llm -q tests`, full-tree Ruff check and format, the
developer-guide index check, and MolSysSuite's repository checker. The local
receptor build was `1.1.0+13.g43d37d6`; hosted CI independently resolved the
exact published `pytest-receptor 1.1.0 py_1` from `uibcdf`.

Exact-commit routine CI `36063274018` passed with `--receptor=ci` (103 passed,
one skip). The shared policy run `36063275021` passed. Full Python/OS matrix
`36063283769` passed 12/12 cells, and the separate Python 3.14 feasibility
run `36063283598` passed 3/3. GH Run Receptor inspected all four runs; native
CI logs confirmed the exact package pin and command. The inherited
developer-tools review is therefore adopted. The support-library review is
partial while the ArgDigest boundary and dependency cycle remain unresolved
under `uibcdf/depdigest#18`.

## Acceptance criteria

- Locally run the complete suite with `pytest --receptor=llm` and validate the
  generated dependency files.
- The exact source commit passes routine CI, full matrix, and the shared policy
  gate; inspect hosted evidence with GH Run Receptor.
- MolSysSuite records developer-tools adoption only after hosted validation and
  support-libraries as partial until the ArgDigest boundary is settled.
