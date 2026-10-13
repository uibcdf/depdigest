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

## Complete owner disposition — 2026-10-13

Receiving review for DepDigest #33, source baseline
`1b746ece24587e920e49ea20f2bfebde7c3efc24` plus the owning bootstrap repair.
Canonical temporary-resource policy inspected at MolSysSuite
`125905227e56fb680694140b31284f9df196a395`; executable dependency SDK remains pinned
at `6d6172d6cd00c5ac2d4ebadb71df554ec5b7fa26`. Earlier dated evidence stays historical.

| Applicable route/resource | Owner and useful lifetime; disposition | Proof and limits |
| --- | --- | --- |
| Development bootstrap | Explicit sourced `persist` owns setup operations; the named environment remains the caller's through later use, including partial failures. Kernel registration is an explicit caller-retained user resource. Preview owns no environment operation. | Nine POSIX Bash controlled guards reproduced and repair preview mutations, unsourced setup, wrong editable root and suppressed micromamba failure. No real solver/update or Windows Bash qualification. |
| Conda create/update helpers | Create owns its private YAML workspace until the synchronous child returns; update uses caller YAML/environment. Both preserve caller inputs and expose nonzero child status. | Existing eight real controlled child guards (#32); requested environments are retained rather than removed by helpers. |
| Installed audit/optional-engine/declared-registry verifier | Each operation owns a `TemporaryDirectory` through its check. Audit children have a 30-second timeout. Context cleanup raises visibly; config/path/modules restore through `finally` and provider contexts. | Six success/injected-failure cleanup cases execute all three operations, remove their exact private paths and preserve caller sentinel/state. Source fixture checks do not qualify public archive bytes. |
| Pytest and developer tests | Pytest owns temporary fixtures/test caches; receipt output belongs to the task. Tests use unique roots and context/fixture teardown. Maintain caches during active debugging; retire only explicitly owned basetemp after proof. | Full source tests plus directed lifecycle controls. The first failing bootstrap run's exact pytest root is tracked in the task manifest; shared pytest parent and unrelated runs are preserved. |
| Benchmarks | Decorator probes use in-process data; consumer probe reads explicit source roots and joins bounded child commands. Entry-point measurements reuse Ackredit-owned wheel/install/verifier operations in private task environments. Caller stdout/JSON are retained evidence. | 150 metadata workers completed with 30-second timeouts inside managed workspaces; all original wheel/file checks passed. No copied build/install engine, sibling source edits or actual scientific consumer qualification. |
| Integration probe | Explicit sibling sources are read-only, output is caller-owned. Python's process lifetime bounds import/global state; the caller owns requested output paths. | Existing bad-source controls and inspection; five sibling-workspace end-to-end cases remain unavailable in isolated source tests. |
| Dependency generation, freeze and report indexes | Requirements/environment/recipe generation and indexes are reviewed maintained files, version freeze is an explicit build-source output. No implicit temporary resource is introduced. | Generated-index checks and default twenty-route qualified dependency preflight; generated recipe files and shared guidance are unchanged. |
| Build, staging, promotion and public qualification | Conda owns build workspaces/prefixes/caches, GitHub runners own hosted environments and checkout roots. Release tasks own immutable archives/provenance/receipts and retain them through publication and audit. | Inspection plus existing source custody/native-evidence guards; original 0.14.0 source/staged/public qualification stays in its dated receipt. No new artifact, promotion or hosted installed matrix is claimed here. |
| Documentation | Sphinx/Jupyter tools own generated `_build`, autosummary, execution/cache outputs; the invoking caller controls rebuild and later disposal. Docs source/notebooks and checked-in generated outputs remain maintained inputs. | Workflow/config inspection; retained local paths below are preserved. Documentation execution/Qt/browser/native engines are not newly qualified by this owner review. |
| Task checkouts and private environments | This authorized task owns the manifest-identified clones, environment prefixes, metadata wheels and test roots. Lifetime extends through the follow-on #36 evidence and all issue handoffs. | Exact baseline/pins, clean SDK/Ackredit snapshots and child exit statuses are checked. Final disposal and any cleanup failure must be separately reported after lifetime ends. |

### Retained resources and historical attribution

At inspection the primary checkout contained `.pytest_cache`, `docs/_build`,
`build`, `depdigest.egg-info` and `docs/api/autosummary`. They serve caller/tool
workflows and cannot be uniquely attributed to this task. Disposition: retain;
responsible owner is the repository caller with the generating tool. Review date
2026-10-13. Removal condition is explicit owner intent after checking active use,
useful evidence and generated/tracked status. This is retained caller custody,
not an approved blanket deletion or a reproduced resource leak. Root `dist` and
root/docs `.jupyter_cache` were absent; absence does not establish past disposal.
Shared Conda environments, primary editable version metadata and dirty sibling
checkouts were preserved. Unrelated environment dependency conflicts are shared
workspace maintenance under MolSysSuite #82, outside these local repairs.

Eight exact DepDigest historical paths named in central #104's inventory were
checked, and all were absent. No deletion was performed, no historical disposal
was attributed, and this is not a complete machine inventory. The normalized
receipt `devguide/evidence/resource_owner_review_2026-10-13.json` records the
bounded inspection and controlled proof. There are no remaining reproduced local
implementation gaps in the reviewed routes. Hosted/native/scientific qualification
and caller-retained resources keep the explicit component/tool boundaries above;
no universal tool/platform matrix or shared cache cleanup is inferred.
