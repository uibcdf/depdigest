---
summary: Expand DepDigest support to Python 3.14 after hosted and package evidence.
issue: uibcdf/depdigest#14
status: active
opened: 2026-09-21
closed:
severity: medium
verification: measured
area: [python, compatibility, packaging, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Expand DepDigest support to Python 3.14

## What

Evaluate and then deliver Python 3.14 support under `uibcdf/molsyssuite#29`. DepDigest
is next after SMonitor in the pure-Python dependency chain. Neither source-tree
compatibility nor a noarch recipe alone authorizes a public support claim.

## How

The first local feasibility run used a disposable Linux CPython 3.14.7 Conda
environment with public `uibcdf/noarch::smonitor-0.16.0-py_1` and
`uibcdf/noarch::pytest-receptor-1.1.0-py_1`. With NumPy and Pint for the sibling
cross-library E2E test and PyYAML for the requirements broadcaster test, commit
`24d24983b19b9f07b2708942c37f0b34f3fcd110` passed all 67 tests using
`--receptor=llm -n 12`. Before those three test-only dependencies were installed,
the suite failed on imports; those failures did not demonstrate a DepDigest defect.
The source was selected through `PYTHONPATH=.` and was **not** an installed 3.14
DepDigest distribution.

Add a manually dispatched, explicitly non-claiming 3.14 source matrix for Linux,
macOS, and Windows. It must resolve its test environment from public channels and
retain the exact hosted conclusions. If it passes, coordinate the `authorized`
transition state centrally, update metadata, derived Conda environments and recipe,
the required CI matrix and documentation together, then stage an exact-SHA noarch
candidate. Verify the installed candidate off-checkout on Python 3.11--3.14 and the
claimed platforms before promoting exactly those bytes. The Conda publication route
must satisfy `uibcdf/molsyssuite#27`; Zenodo readiness is separately tracked in
`uibcdf/depdigest#11` and must be resolved before the public release.

## Why

DepDigest currently declares `>=3.11,<3.14` in project metadata and its Conda
dependency source. ArgDigest, PyUnitWizard, and incubating Ackredit consume it;
leaving this boundary unchanged prevents clean 3.14 environments for that chain.

## Acceptance criteria

- A hosted non-claiming 3.14 source matrix succeeds on Linux, macOS, and Windows.
- Central transition authorization precedes any target-range metadata claim.
- Metadata, full CI, generated environments, recipe, docs, and release notes agree.
- A staged exact-commit noarch artifact passes clean installed-package tests, with
  published SMonitor and independently checked package provenance.
- The GitHub Release, exact-file Conda promotion, public clean-install checks,
  and required Zenodo verification pass before central admission.

## Current status

Local Linux and three-platform hosted source feasibility passed. Packaged, public,
and archival gates remain open. No release, tag, or Python 3.14 support claim has
been made.

## Hosted feasibility evidence

Commit `cd4680a653942c4cace7e8ae89b9cc623242f12c` added the non-claiming source
matrix and its GH Run Receptor rule. Workflow run `35595697428` completed successfully
on Ubuntu, macOS, and Windows with Python 3.14, public SMonitor 0.16.0 build `py_1`,
and public Pytest Receptor 1.1.0 build `py_1`. GH Run Receptor reported `PASS`,
`conclusion=success`, and 3/3 jobs. A separate GitHub run query confirmed the exact
commit SHA and success for each named platform job. The workflow tests checkout
source through `PYTHONPATH` without installing a DepDigest distribution, so package
metadata, off-checkout installation, Conda publication, and Zenodo remain unproven.

This is sufficient feasibility evidence to request central `authorized` status, not
`admitted` status. The next local step is a consistent target-range candidate and
its required hosted CI matrix.
