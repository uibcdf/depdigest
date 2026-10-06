# Conda release routes for DepDigest

DepDigest publishes one `noarch: python` Conda artifact. Its local workflow is a
pilot of the two-route contract proposed in `uibcdf/molsyssuite#27`, not a literal
template for native packages. Python 3.14 preparation is tracked in
`uibcdf/depdigest#14`; the local route implementation is `uibcdf/depdigest#15`.

## Decide before tagging

The release owner completes `devtools/conda-build/release_plan.toml` **in the
candidate commit**. The retained `0.13.0` plan selects the `staged` route; this
decision does not publish or promote a package. For a later version, reset and
review `version`, `build_number`, `route`, `reason`, `decision_by`,
`required_workflows` and their explicit `gate_jobs`
before any tag or dispatch. Keep
`.github/workflows/CI_full_matrix.yaml` among the gates. Run that full matrix on
the final candidate commit; any later commit needs a new exact-commit run. The
workflow records the final tag SHA and gate run IDs in its retained receipt, so
the plan must not contain a circular pre-commit SHA or run ID.

Choose `staged` whenever an installed candidate must pass a gate before public
visibility, claimed Python/platform support or packaging changes materially,
dependencies have to be tested together, or any file for that version already
exists under staging or another label. This includes the first Python 3.14
release. Choose `direct` only when none of those conditions applies, public
dependencies resolve, ordinary release gates passed, the action tests its
package before upload, and the target version is wholly unoccupied. Being a
patch or noarch release alone does not permit direct publication. If evidence
is ambiguous, pause or stage; the central decision criteria remain under review.

## Direct: ordinary unstaged release

Tag the exact candidate SHA with canonical `X.Y.Z` and publish a stable GitHub
Release. The release event checks the committed `direct` decision, tag identity,
successful full-matrix run at that SHA, and an explicit absent-version response
from Anaconda across labels. Any existing distribution or registry error fails
closed. The action builds and tests `py_0` with public dependencies, uploads once
to `main`, retains producer evidence, and independently compares the public
record with the built file SHA-256. Never use `--force`.

The GitHub Release is public before its Conda job completes. Until the public
postcheck passes, publication is incomplete; a failed or ambiguous job needs
investigation, not a blind retry. The central proposal still has to settle
whether this bounded non-atomic interval is acceptable for routine releases.

## Staged: installed-candidate evidence first

Commit `route = "staged"` before candidate work. Dispatch
`.github/workflows/build_and_upload_conda_packages.yaml` with a full candidate
SHA, exact version, and non-negative build number. It verifies the candidate
and exact-commit gates, then builds/tests only into `uibcdf/label/staging`.
If the version is untagged, only a runner-local tag is made for version derivation.
A repair increments the build number and never overwrites an existing coordinate.

Verify the exact staged file and SHA-256, clean off-checkout installation on the
supported interpreters and platforms, dependencies, and any consumer gates.
For DepDigest, dispatch `.github/workflows/test_staged_conda_package.yaml` with
the candidate SHA, version, build number, and successful staging run ID. Its
producer gate cross-checks the GitHub run and both retained receipts; the
12-cell matrix then installs the exact package from staging with SMonitor
channel-qualified from public `uibcdf`. The solver uses flexible priority
because strict priority masks that public SMonitor build when staging also has
the same package name; explicit coordinates and installed-record checks keep
both package origins exact. Each cell verifies Conda's installed
record (including SHA-256 and exact download URLs, rather than solver-specific
`channel` field formatting), Python and package versions, off-checkout
import, and CLI. A failed or missing cell is not evidence of support. The
validation workflow may be added after a staged artifact was built, provided it
checks the immutable candidate SHA and artifact digest; do not mistake the
validation workflow's newer HEAD for a change to the staged candidate.
Only then tag the **same SHA** and publish its stable GitHub Release. The release
workflow validates the committed route and skips its direct build and upload
steps for a staged plan; that successful route selection is not evidence of
public Conda publication. Dispatch
`.github/workflows/promote_conda_package.yaml` with the tagged SHA, exact
version, build number and independently verified digest. The shared
`promote@v2.2.2` Action adds `main` to that same file, keeps `staging`, emits a
receipt, and is followed by an independent public-channel query. Do not rebuild,
re-upload, choose a staging build implicitly, or move the tag.

## Evidence and scope

Retain the route receipt, producer or promotion evidence, full GitHub workflow
conclusions, and exact registry coordinate/digest. GH Run Receptor provides the
compact first inspection; it cannot replace GitHub or Anaconda source facts.
The 0.10.2 `py_0` candidate predates this release-plan gate and is not a Python
3.14 artifact. During 0.11.0 preparation, staging builds `py_0` and `py_1`
provided earlier evidence but were superseded after release metadata and
formatting changes; neither was promoted. The final tagged commit
`d5b259a0f4ab00756858869061604fd64d561850` passed the 12-cell source
matrix in run `35664438560` and suite policy in run `35664438912`.
Staging run `35664759083` uploaded `depdigest-0.11.0-py_2.tar.bz2` with SHA-256
`b6ba665d9125f49506b7e4231e6065f164d3b643117a22288b44baafceff270f`.
Run `35665346654` passed producer verification and all twelve clean installed
Linux/macOS/Windows × Python 3.11--3.14 cells. Published ArgDigest 0.12.1 passed
a Linux/Python 3.13 consumer smoke with the same staged DepDigest file.

GitHub Release 0.11.0 is public. Promotion run `35665723593` added `main` to
the same `py_2` file; its receipt and independent public/staging queries agree
on the digest. A new Linux/Python 3.14 environment installed DepDigest and
SMonitor exclusively from public channels, imported from `site-packages`,
and ran the CLI. Zenodo record `22884369` archived the source snapshot and its
downloaded bytes matched the public file size and checksum; it does not claim
that Zenodo archived the Conda artifact. The release-triggered *direct* uploader
failed its route guard as designed; the separate promotion is the authoritative
Conda publication path for this staged release. The direct route remains
unexercised and should not be called hosted-proven.

## 0.11.1 launcher repair

The `0.11.1` staged candidate is commit
`456ae6b7bcce1402c6504e2cf74d3721f2dcd39e`. Exact-commit full-matrix
run `36229520653` passed all twelve cells on attempt 2 after one Windows
`__pycache__` copy race in the first attempt. Staging run `36229720222`
uploaded `depdigest-0.11.1-py_0.tar.bz2` with SHA-256
`bc54290422dc8af90d7d9f75f64fc12ece6b5da78e04dc66a3b7ddf2882799fa`.
Installed-package run `36229868929` verified its producer receipts and all
twelve clean Linux/macOS/Windows × Python 3.11–3.14 cells, including the
actual `depdigest --help` launcher in the Conda prefix.

Annotated tag `0.11.1` and its stable GitHub Release identify that same
candidate SHA. Promotion run `36230598357` verified the digest and added
`main` to the staged file without rebuilding it. The retained promotion
receipt and an independent Anaconda release query agree on the one noarch
file and its `staging` and `main` labels. A fresh Linux/Python 3.13
installation from public channels verified the exact URL and digest, imported
the installed package, and ran its launcher outside the checkout. The
release-triggered direct uploader rejected the staged route in run
`36230515248` as designed under the workflow version present in that tagged
commit; the promotion run is the Conda publication path. Later release tags use
the route selector to leave this workflow green for a valid staged decision
without uploading. An invalid or mismatched decision still fails closed. The
direct route still needs a real release to prove its hosted publication path.

## 0.11.2 direct candidate

The candidate selects `direct` in `devtools/conda-build/release_plan.toml`.
This patch does not change the package layout or claimed Python/platform
support, and its dependencies are already public. The exact candidate commit
must pass the full source matrix; release automation must also confirm that
Anaconda has no file for 0.11.2 in any label before building, testing, and
uploading its single noarch file. A public digest comparison is required before
calling this route proven. Committing this plan does not publish the release.

The stable `0.11.2` tag and GitHub Release now identify candidate
`87f0bb1a2bd0d24532588d900c7af736b5cd1a05`. The exact-commit source
matrix passed all twelve cells in run `36233298114`. Direct release run
`36233613024` checked the empty version, built and tested one noarch package,
uploaded it to `main`, and verified the public digest. The retained route
receipt and producer event record SHA-256
`9b7ec4d493930219a0982421072e432994257378d779a3e6306f37b35d850c58`;
an independent Anaconda query and fresh public-file download matched it.
This is the first hosted proof of the direct route in DepDigest.

## 0.12.0 optional-engine candidate

The committed plan selects `staged` for the optional-engine capability in #22.
Run the full source matrix and suite policy on the exact candidate, then dispatch
the existing staging producer and twelve-cell installed gate for build `py_0`.
Verify the installed optional-executable/disabled-installer behavior separately
before tagging that same commit. A stable release and digest-verified promotion
publish the same file; public poststate and clean installation must agree.
TopoMT adoption and the common contract are tracked in uibcdf/molsyssuite#62.
This candidate plan is not a publication claim.


### 0.12.0 public poststate: 2026-10-01

Stable tag and GitHub Release `0.12.0` identify
`0da46d9ff31fbe2f92e4e667a32868aebe840b39`.
Exact-source matrix `36788849230` passed all twelve test cells and policy
`36788753565` passed. Producer `36789413638` built the immutable staged artifact;
installed matrix `36823713839` passed all twelve verification steps, including
the new optional-engine contract, public SMonitor and off-checkout import/CLI.
The release-event route selection `36824505071` passed and performed no direct
upload; documentation publication `36824505069` passed.

Promotion `36824539168` verified
`noarch/depdigest-0.12.0-py_0.tar.bz2` with SHA-256
`03d5aa569bfeb95bdd253a52e68e59094d9af5a6c4c7bc4ba228d3e36cfb30a3`,
added `main` to the same file and retained `staging`. Its receipt reports
`status=verified`; its independent public-channel query passed. An independent
public download has that same digest. A fresh public-channel Conda environment
on Linux/Python 3.13.15 verified version/import origin/URL/digest, installed
optional-engine behavior and launcher. TopoMT's six availability tests and seven
administrative tests pass against this public installation. This certifies the
provider availability contract, not installed scientific engine parity.

## 0.13.0 expanded-audit public poststate: 2026-10-04

Stable tag and GitHub Release 0.13.0 identify
`df771e00e886fd9b12915adf54c1bd75c4b5476c`. Exact-source matrix
`37192645716` and policy `37192635455` passed. Staging producer `37194076957`
built `noarch/depdigest-0.13.0-py_0.tar.bz2`, SHA-256
`e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`.
Archive inspection and installed matrix `37194436139` passed all twelve cells,
including the expanded audit scope/typing/source-line/JSON/exit contract.

Promotion `37194867340` verified and added main to that same file; its pinned
independent verifier passed both registry and main solver-index checks. A separate
public download and clean Linux/Python 3.14.7 install matched its digest, public
dependency URLs and installed runtime/launcher/contracts. Documentation
`37194867145` deployed 0.13.0. Zenodo `23135234` was independently verified
with its single source ZIP's downloaded size/checksum; no Conda archival is claimed.
The [normalized release receipt](evidence/release_0.13.0_2026-10-04.json) records
source, artifact, closure and evidence scopes. Consumer adoption remains independent
under MolSysSuite #95, ArgDigest #22 and PyUnitWizard #93.


## Maintained prospective controls — 2026-10-06

Under uibcdf/depdigest#30, twenty route declarations and source resources delegate
to the fixed shared provider. Default source checks verify actual installed public
bounds. Candidate build/promote calls require all twelve executed source jobs and
policy steps, with version/build matching the committed recipe context. Bootstrap
inspection alone cannot clear that debt.

Future installed workflow calls also supply the independently verified `sha256`
and run at a ref identifying the original candidate. Preparation compares it
against original producer receipts and checks the native/checkout source. The run
title binds exact filename/digest. Future promotion calls supply `installed_run_id`
in addition to original source/version/build/digest; the thin provider invocation
verifies and retains the thirteen-job evidence before the existing promoter runs.
Historical newer-workflow qualification remains a separate explicit source/file
binding review; it cannot silently satisfy this prospective candidate profile.

Original public 0.13.0 remains candidate
`df771e00e886fd9b12915adf54c1bd75c4b5476c`, producer `37194076957`, source
matrix `37192645716`, policy `37192635455`, installed matrix `37194436139`
and promotion `37194867340`. Its file `depdigest-0.13.0-py_0.tar.bz2` retains
SHA-256 `e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b`.
Do not reconstruct, overwrite or republish it to exercise new source guards.
