# Conda release routes for DepDigest

DepDigest publishes one `noarch: python` Conda artifact. Its local workflow is a
pilot of the two-route contract proposed in `uibcdf/molsyssuite#27`, not a literal
template for native packages. Python 3.14 preparation is tracked in
`uibcdf/depdigest#14`; the local route implementation is `uibcdf/depdigest#15`.

## Decide before tagging

The release owner completes `devtools/conda-build/release_plan.toml` **in the
candidate commit**. The repository carries an intentionally incomplete template:
it cannot publish a package until `version`, `route`, `reason`, `decision_by`, and
`required_workflows` are reviewed. Keep
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
3.14 artifact. The new routes have local tests but no hosted release proof yet;
do not call them publicly validated until a future release exercises them.
