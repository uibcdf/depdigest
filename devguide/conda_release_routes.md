# Conda release routes for DepDigest

DepDigest publishes one `noarch: python` Conda artifact. Its local workflow is a
pilot of the two-route contract proposed in `uibcdf/molsyssuite#27`, not a literal
template for native packages. Python 3.14 preparation is tracked in
`uibcdf/depdigest#14`; the local route implementation is `uibcdf/depdigest#15`.

## Decide before tagging

The release owner completes `devtools/conda-build/release_plan.toml` **in the
candidate commit**. The `0.11.0` candidate selects the `staged` route; this
decision does not publish or promote a package. For a later version, reset and
review `version`, `route`, `reason`, `decision_by`, and `required_workflows`
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
Only then tag the **same SHA** and publish its stable GitHub Release. The direct
uploader rejects its staged plan; the release-triggered build workflow will show
an incomplete publication until promotion succeeds. Dispatch
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
`36230515248` as designed; the promotion run is the Conda publication path.
