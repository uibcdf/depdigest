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

Published DepDigest 0.10.1 declares `>=3.11,<3.14`. The authorized development
candidate now declares `>=3.11,<3.15` in metadata and its Conda dependency source,
but this is not yet a public 3.14 package. ArgDigest, PyUnitWizard, and incubating
Ackredit consume DepDigest; the older public boundary prevents clean 3.14
environments for that chain.

## Acceptance criteria

- A hosted non-claiming 3.14 source matrix succeeds on Linux, macOS, and Windows.
- Central transition authorization precedes any target-range metadata claim.
- Metadata, full CI, generated environments, recipe, docs, and release notes agree.
- A staged exact-commit noarch artifact passes clean installed-package tests, with
  published SMonitor and independently checked package provenance.
- The GitHub Release, exact-file Conda promotion, public clean-install checks,
  and required Zenodo verification pass before central admission.

## Current status

Local Linux and three-platform hosted source feasibility passed. MolSysSuite commit
`10c0948` records DepDigest as `authorized`, not `admitted`. The target-range
metadata, derived noarch recipe/environments, twelve-cell required CI matrix, and
candidate documentation are prepared locally. The complete source suite passed
88 tests on both Python 3.13 and 3.14 with 12 workers. The central repository
checker accepts the candidate; a local Conda render for Python 3.14 succeeded,
but derived the latest existing tag `0.10.1` because no new candidate tag exists.
Packaged, public, and archival gates remain open. No release, tag, or public
Python 3.14 support claim has been made.

The first required twelve-cell matrix run, `35601640919`, at candidate commit
`ea57f821a3eb174360657ea1c7bde48bb7d7d42c` failed in all twelve jobs during
the test step. The shared failure was the requirements broadcaster test: the
test environment omitted PyYAML, which that script imports. Windows additionally
exposed a Unix-only `PYTHONPATH` separator in the workflow and POSIX `shlex`
parsing of Windows temporary paths in the new Conda release-route tests. GH Run
Receptor identified the test failures; the native failed-step log was consulted
for the platform-specific details. These are CI/test-environment defects, not
evidence that the DepDigest runtime fails on Python 3.14. The corrections now
pass all 89 source tests locally on both Python 3.13 and 3.14 with 12 workers;
the required hosted matrix must be repeated at the new exact commit before any
compatibility claim advances.

The corrected matrix run `35603608717` at
`2e7abd4cceae8df925eb6a4607416118ba07ab47` passed all twelve jobs across
Ubuntu, macOS, Windows, and Python 3.11--3.14. Review then found that both
off-checkout import smoke steps still ended with an `echo` and did not enforce
failure of the preceding Python command, the suite-wide defect tracked by
`uibcdf/molsyssuite#33`. DepDigest is piloting `set -euo pipefail` in both steps
and an executable regression test that substitutes a failing import and requires
the job script to exit nonzero before the trailing echo. This makes the installed
import check meaningful; a new exact-commit hosted matrix is required before
counting the twelve jobs as release-gate evidence. The pilot and its hosted
result should be reported to the central issue for reuse by other members.

The first pilot run, `35604512974`, passed all eight Ubuntu/macOS cells and failed
the four Windows cells only in the new regression test. On the hosted Windows
Python process, bare `bash` resolved to the WSL launcher, which had no Linux
distribution, rather than to the Git Bash executable used by the workflow's
`shell: bash -l {0}` steps. The test now locates Git Bash relative to Git on
Windows and invokes that executable explicitly. The hosted result remains red;
the corrected pilot needs another exact-commit matrix run.

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
