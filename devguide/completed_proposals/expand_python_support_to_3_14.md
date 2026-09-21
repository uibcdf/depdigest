---
summary: Expand DepDigest support to Python 3.14 after hosted and package evidence.
issue: uibcdf/depdigest#14
status: resolved
opened: 2026-09-21
closed: 2026-09-21
severity: medium
verification: measured
area: [python, compatibility, packaging, ci]
guard: tests/test_staged_conda_install.py
normative: devguide/conda_release_routes.md
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

At filing, published DepDigest 0.10.1 declared `>=3.11,<3.14`. Release 0.11.0
now publicly delivers `>=3.11,<3.15`. ArgDigest, PyUnitWizard, and incubating
Ackredit consume DepDigest; their own 3.14 support still requires separate
evidence and releases.

## Acceptance criteria

- A hosted non-claiming 3.14 source matrix succeeds on Linux, macOS, and Windows.
- Central transition authorization precedes any target-range metadata claim.
- Metadata, full CI, generated environments, recipe, docs, and release notes agree.
- A staged exact-commit noarch artifact passes clean installed-package tests, with
  published SMonitor and independently checked package provenance.
- The GitHub Release, exact-file Conda promotion, public clean-install checks,
  and required Zenodo verification pass before central admission.

## Pre-release chronology

At the first checkpoint, local Linux and three-platform hosted source feasibility
passed. MolSysSuite commit
`10c0948` records DepDigest as `authorized`, not `admitted`. The target-range
metadata, derived noarch recipe/environments, twelve-cell required CI matrix, and
candidate documentation are committed. The complete source suite passed
91 tests on both Python 3.13 and 3.14 with 12 workers. The central repository
checker accepts the candidate; a local Conda render for Python 3.14 succeeded,
but derived the latest existing tag `0.10.1` because no new candidate tag exists.
Packaged, public, and archival gates were still open at that checkpoint.

The first required twelve-cell matrix run, `35601640919`, at candidate commit
`ea57f821a3eb174360657ea1c7bde48bb7d7d42c` failed in all twelve jobs during
the test step. The shared failure was the requirements broadcaster test: the
test environment omitted PyYAML, which that script imports. Windows additionally
exposed a Unix-only `PYTHONPATH` separator in the workflow and POSIX `shlex`
parsing of Windows temporary paths in the new Conda release-route tests. GH Run
Receptor identified the test failures; the native failed-step log was consulted
for the platform-specific details. These are CI/test-environment defects, not
evidence that the DepDigest runtime fails on Python 3.14. The corrections now
passed all 89 source tests locally on both Python 3.13 and 3.14 with 12 workers
at that revision. A later exact-commit hosted matrix is recorded below.

The corrected matrix run `35603608717` at
`2e7abd4cceae8df925eb6a4607416118ba07ab47` passed all twelve jobs across
Ubuntu, macOS, Windows, and Python 3.11--3.14. Review then found that both
off-checkout import smoke steps still ended with an `echo` and did not enforce
failure of the preceding Python command, the suite-wide defect tracked by
`uibcdf/molsyssuite#33`. DepDigest piloted `set -euo pipefail` in both steps
and an executable regression test that substitutes a failing import and requires
the job script to exit nonzero before the trailing echo. This makes the installed
import check meaningful; a new exact-commit hosted matrix was required before
counting the twelve jobs as release-gate evidence. The pilot and its hosted
result are recorded below for reuse by other members.

The first pilot run, `35604512974`, passed all eight Ubuntu/macOS cells and failed
the four Windows cells only in the new regression test. On the hosted Windows
Python process, bare `bash` resolved to the WSL launcher, which had no Linux
distribution, rather than to the Git Bash executable used by the workflow's
`shell: bash -l {0}` steps. The test now locates Git Bash relative to Git on
Windows and invokes that executable explicitly. That hosted attempt remains red;
the corrected pilot was checked in the later matrix below.

## Required hosted matrix evidence

The final pilot commit `05af5f879ea0c4d098b8dcfaf35841a13d584b1b` passed
the full 12-cell matrix in run `35642619746`, attempt 2. Attempt 1 passed ten
jobs, including all Windows and macOS cells; Ubuntu 3.11 and 3.13 stopped before
environment creation because the micromamba download endpoint returned HTTP 500
twice. Their post-step `Unexpected end of JSON input` was a consequence of that
failed download, not a DepDigest test failure. Only the two failed jobs were
rerun. GH Run Receptor reported `PASS` and 12/12 jobs at the final attempt;
a separate GitHub query confirmed the exact SHA, overall `success`, and twelve
named successful jobs.

The full matrix installs DepDigest with pip from this checkout, performs the
off-checkout import smoke under fail-fast Bash, and runs the source test suite
on Python 3.11--3.14 on Ubuntu, macOS, and Windows. It does **not** build or
validate a Conda artifact. The later staging and installed-package evidence is
recorded below. At that point DepDigest remained centrally `authorized`, not
`admitted`, pending the consumer, release, public-install and archival gates.

## Staged Conda artifact and installed-package evidence

Candidate `0.11.0` was frozen at `9913c1e2041494dc01cd85d3173d9e8675ad5df8`.
Its source matrix passed 12/12 in run `35646637134`. Staging run `35646813805`
built and uploaded one `noarch` file, `depdigest-0.11.0-py_0.tar.bz2`, with
SHA-256 `ac41c5bd79eea47c3206efb58aede50da0e2f1f10b5791f000bd2f3df1d19082`.
The producer and route receipts agree on the candidate commit, version, route,
file, and successful upload; an independent registry query found the same digest
under `uibcdf/label/staging`. A disposable Linux/Python 3.14 installation
confirmed the staged package and public SMonitor 0.16.0 off-checkout.

The separate installed-package gate at run `35660591628` passed its producer
verification and all twelve clean Linux/macOS/Windows × Python 3.11--3.14 jobs.
Each cell installed the exact staged DepDigest coordinate and public SMonitor
build, then checked SHA-256, exact source URLs, interpreter and distribution
versions, off-checkout import, and CLI. The gate was added after the candidate
commit and validates its immutable artifact rather than treating the gate's own
HEAD as the package under test. Local regression tests for provenance and the
workflow passed 104/104 on Python 3.13 and 3.14 with 12 workers; Ruff passed.

Two initial gate attempts remain red in the history. Run `35659370222` failed
at environment creation because libmamba's strict channel priority masked the
public SMonitor build when staging also contained SMonitor. Run `35660085653`
installed packages but rejected every cell because micromamba formatted the
Conda `channel` metadata differently from Conda. Flexible priority with
channel-qualified coordinates and exact installed URL/digest checks resolved
both issues without relaxing package identity. These are gate-implementation
failures, not package defects. The pattern and caveats were shared in
`uibcdf/molsyssuite#27`; 3.14 status was updated in `uibcdf/molsyssuite#29`.

The remaining gates at that checkpoint were consumer compatibility, stable
release, exact-file promotion, public clean installation, and Zenodo verification.

## Public 0.11.0 release and resolution

The final tag `0.11.0` resolves to
`d5b259a0f4ab00756858869061604fd64d561850`. Exact-commit source CI
passed 12/12 in run `35664438560`, and suite policy passed in run
`35664438912`. Staging run `35664759083` built the final noarch `py_2` file
with SHA-256 `b6ba665d9125f49506b7e4231e6065f164d3b643117a22288b44baafceff270f`.
The producer receipt, staging registry record, and clean installed-package
matrix agree on that identity. Run `35665346654` passed all twelve
Linux/macOS/Windows × Python 3.11--3.14 cells. Published ArgDigest 0.12.1
passed a Linux/Python 3.13 consumer smoke with the final staged file; ArgDigest
still declares Python `<3.14`, so this does not claim 3.14 support for it.

The stable GitHub Release was published on 2026-09-21. Promotion run
`35665723593` added the public Conda label to the exact `py_2` file; independent
public and staging queries returned the same SHA-256. A fresh Linux/Python
3.14.7 environment resolved DepDigest 0.11.0 and SMonitor 0.16.0 from public
`uibcdf` and conda-forge, imported the installed distribution off-checkout,
and ran the CLI. The public Zenodo record `22884369` reports version DOI
`10.5281/zenodo.22884369` and concept DOI `10.5281/zenodo.22884368`; the
downloaded source snapshot matched its reported size and checksum. No Conda
file was claimed as archived in Zenodo. The public docs deployment passed in
run `35665694974`. MolSysSuite records DepDigest as `admitted` under
`uibcdf/molsyssuite#29`; the suite-wide default remains narrower.

The executable guard `tests/test_staged_conda_install.py` rejects mismatched
producer identities, wrong artifact digests and URLs, and a staged dependency
substituted for the public one. The hosted matrix and public registry audit
provide the release-specific evidence that a local test cannot synthesize.

## Hosted feasibility evidence

Commit `cd4680a653942c4cace7e8ae89b9cc623242f12c` added the non-claiming source
matrix and its GH Run Receptor rule. Workflow run `35595697428` completed successfully
on Ubuntu, macOS, and Windows with Python 3.14, public SMonitor 0.16.0 build `py_1`,
and public Pytest Receptor 1.1.0 build `py_1`. GH Run Receptor reported `PASS`,
`conclusion=success`, and 3/3 jobs. A separate GitHub run query confirmed the exact
commit SHA and success for each named platform job. The workflow tests checkout
source through `PYTHONPATH` without installing a DepDigest distribution, so package
metadata, off-checkout installation, Conda publication, and Zenodo remain unproven.

That feasibility run justified central `authorized` status, not `admitted`
status. The later required CI, packaged and public evidence is recorded above.
