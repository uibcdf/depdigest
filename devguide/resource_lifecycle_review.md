# Resource lifecycle review

Owner: uibcdf/depdigest. Coordination: uibcdf/molsyssuite#104.
Reviewed source baseline: d5a7ac0ae66beaff1ba080e7114bcdd55398c21c.
Date: 2026-10-08. This is a bounded source/tool review, not a historical
filesystem cleanup or full installed-platform qualification.

| Operation | Ownership and lifetime | Evidence / remaining scope |
| --- | --- | --- |
| `create_conda_env.py` | Private YAML exists through the completed manager; context restores cwd/removes its directory on return/error. Requested environment remains caller-owned, including a partial failed create. | Real child success/failure, exact arguments/spaced paths, private cleanup and caller preservation: eight create/update guards. Failure suppression repaired in uibcdf/depdigest#32. |
| `update_conda_env.py` | Supplied YAML and active environment are caller-owned; no private directory is created. Existing prune is an explicit local operation, not closeout cleanup. | Same guard proves child status, original files and sentinel custody. No actual environment update/solver run. |
| Installed audit and optional-engine checks | Managed private source fixture/missing-command path; synchronous audit children finish or timeout before context exit. Temporary provider configuration restores through its owner context. | Source inspection plus ordinary staged-verifier tests; these source tests do not certify public artifact bytes or installed matrix. |
| `integration_probe.py` | Fresh process checks explicit source roots; output stdout/explicit receipt belongs to invoking task. It neither installs nor edits siblings. | Source inspection and ordinary probe controls; five collective sibling cases not executed in isolated workspace. No cleanup of explicit caller receipts. |
| Release route, distribution receipts and workflows | Explicit candidate/promotion JSON and immutable artifact receipts belong to release task; workflow uploads retained evidence before publication/promotion. Hosted caches/environments belong to runner/tool managers. | Source custody inspection and twenty default qualified distribution routes. No release, workflow mutation, solver/cache deletion or installed-matrix dispatch. |
| Broadcast, freeze, index and starter scripts | Generated recipe/environment files, frozen build-source metadata and indexes are explicit maintained/build outputs. Starter environment is caller-owned; print/help does not authorize deleting it. | Source inspection and existing source guards; generated outputs must be reviewed by their owner. Do not treat them as disposable private staging. |

## Local environment tooling and shared operation

The central `conda_environment_tools.apply_environment` operation is opt-in under
uibcdf/molsyssuite#108 and requires a reviewed dependency-routes@3 profile.
This repository retains its @2 qualified routes. #32 repairs existing calls via
standard-library subprocess argument lists/result propagation; it introduces no
new generator, duplicate SDK or implicit shared-tool migration. Runtime provider
consumers require no API, dependency, guide or pin adoption for this local repair.

## Closeout boundary

Retain task-owned source/SDK clones, test fixtures and receipts only while the
review needs them. After native proof and handoff, verify exact checkout HEAD,
clean status and ownership before removing those clones/fixtures. Preserve
primary editable clones, the qualified/shared Conda environment, human/active
work, release receipts and unrelated tasks. Report cleanup failures explicitly.

Historical retained resources require owner attribution and a separate owner
review; no blanket /tmp search/removal or full compliance claim follows from this
inspection. Original dated #104 screen/probes remain separate from this later
local repair, source tests and hosted gate evidence.
