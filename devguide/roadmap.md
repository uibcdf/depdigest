# Roadmap & Future Steps

Updated: **2026-10-22**, under [#41](https://github.com/uibcdf/depdigest/issues/41).

DepDigest's current public release is **0.15.1**, with Python 3.11--3.14 support.
Its exact noarch Conda file, source and installed twelve-cell matrices,
independent public installation, documentation and Zenodo source snapshot are
recorded in the [release receipt](evidence/release_0.15.1_2026-10-13.json).
The installed matrix covers Linux, Windows and macOS ARM64; the independent
public installation covers Linux/Python 3.14. These scopes do not establish
consumer scientific or conversion parity.

The audit-boundary decisions in ArgDigest #22, PyUnitWizard #93 and MolSysSuite
#95 are resolved; see the [1.0 preparation checklist](release_1.0.0_checklist.md)
for outcomes and evidence. Receiving integration of `DeclaredRegistry` remains
open in [MolSysMT #382](https://github.com/uibcdf/molsysmt/issues/382).
Provider publication and consumer acceptance are separate milestones.

## Recently delivered

### 0.5.0

- CLI auditing workflow (`depdigest audit`) with CI-friendly exit behavior and JSON output.
- Structured introspection output in `get_info(..., format="table|dict|json")`.
- Expanded docs and tests around dependency introspection and architecture verification.

### 0.6.0

- `LazyRegistry` now supports optional `entry_points` discovery mode.
- `entrypoint_group` support added for plugin ecosystems using Python entry points.
- Dynamic runtime registration now includes scoped overrides (`temporary_package_config`) and explicit unregister support.
- User/contract docs updated for entry-point-based discovery.

### 0.7.0

- Public API contract tests added for exported symbols and `get_info` schema.
- CLI contract tests added for baseline command behavior.
- Developer docs now include explicit API stability guarantees.

### 0.8.0

- Freeze feature intake and prioritize release-quality hardening.
- Focus on API/docs consistency and bug fixing only.
- Finalize deprecation and support policy notes for the stable line.
- Add changelog-based migration notes as a release gate.

### 0.9.0

- Execute RC checklist from `devguide/release_0.9.0_checklist.md`.
- Close RC quality gates with internal hardening validation.

### 0.10.0

- Execute stabilization checklist from `devguide/release_0.10.0_stabilization_checklist.md`.
- Run external integrator validation cycle as stabilization milestone.
- Accept stabilization fixes from real-world feedback and CI usage.
- Shared collective E2E module added: `tests/e2e/test_collective_error_path.py` (cross-repo error-path baseline).

### 0.11.0

- Decorator hot-path performance work delivered: internal `@signal` self-instrumentation
  removed from `dep_digest` / `check_dependency`, and `when={...}` condition parameters
  precomputed at decoration time.
- Conditional dependency checks made array-safe for arguments with vectorized `==`.
- Reproducible benchmark added: `python benchmarks/decorator_overhead.py`.
- Completed proposals are now archived under `devguide/completed_proposals/`, matching the
  PyUnitWizard convention; `devguide/pending_proposals/` holds only open work and carries a
  `README.md` index of what each open document is waiting on.
- The first Python 3.14 package followed the staged Conda route. The source and
  exact installed-package matrices passed on Python 3.11--3.14 across Ubuntu,
  macOS, and Windows; the same file was promoted to public `uibcdf`, and a clean
  Python 3.14 public installation passed. Published ArgDigest 0.12.1 also passed
  a Python 3.13 consumer smoke; its Python 3.14 qualification was a separate
  consumer decision.

### 0.11.1

- Repaired the Windows `depdigest` launcher in the noarch Conda recipe.
- Passed twelve clean installed-package cells across Linux, macOS, and Windows
  before promoting the same SHA-256-verified file to the public channel.
- Independently installed the public file on Linux/Python 3.13 and ran the
  installed command outside the source checkout.

### 0.12.0 and 0.13.0

- 0.12.0 published optional executable discovery and explicit disabled installer
  routes under #22. TopoMT adopted the custom-command/error contract.
- 0.13.0 published expanded module/class control-flow auditing under #27/#29.
  Static findings remain distinct from runtime import reachability and syntax
  validation. See the [release receipt](evidence/release_0.13.0_2026-10-04.json).
- Both releases passed their exact-source and installed twelve-cell matrices
  and promoted the same verified files to the public Conda channel.

### 0.14.0

- #34 introduced opt-in `DeclaredRegistry`: metadata-only identity enumeration,
  selective filesystem/entry-point loading and explicit discovery, overrides,
  caching and retry/refresh contracts. `LazyRegistry` retains its full scan.
- #35 qualified and published that API, including the portable Windows
  distribution preflight. See the [release receipt](evidence/release_0.14.0_2026-10-10.json).

### 0.15.0

- #36 added explicit `load_policy="adapter"` for selective adapter inspection
  with an absent optional engine. The strict default remains unchanged;
  inspection does not establish engine availability or authorize execution.
- #37 qualified and published the capability. Public use of this option requires
  DepDigest >=0.15.0; see the [release receipt](evidence/release_0.15.0_2026-10-13.json).
- #33 repaired development bootstrap preview and failure propagation.

### 0.15.1

- #39 serialized overlapping declared value requests on one registry, sharing
  initialization and the cached value or failure cause. Genuine same-thread
  recursion still fails. Public use of this guarantee requires >=0.15.1.
- Mutation, discovery, retry/refresh and configuration changes require external
  coordination. Arbitrary cross-registry cycles are outside the bounded contract.
  See the [API stability guidance](../docs/content/developers/api-stability.md)
  and [release receipt](evidence/release_0.15.1_2026-10-13.json).
- #38 corrected copied Conda descriptive metadata without changing dependencies.

### Preparation for 1.0.0

- Prepare final release narrative and final go/no-go checklist.
- Keep contract stability and release-gate reproducibility as hard blockers.
- The 2026-10-04 [integration checkpoint](collective_evidence_pack.md) remains
  dated source evidence under #26. The maintained
  [1.0 checklist](release_1.0.0_checklist.md) tracks resolved decisions and
  remaining candidate-specific gates, including review of the newer public APIs.
- #6 remains deferred after complete-call consumer measurements; #8 remains
  deferred without a current consumer import boundary. Neither blocks 1.0.
- [#40](https://github.com/uibcdf/depdigest/issues/40) records a future Python
  3.15 lazy-import evaluation and explicitly defers implementation. It creates
  no Python support change, 1.0 commitment or release deadline. Early 2027 is
  a possible review checkpoint, conditional on ecosystem maturity.

### Delivered diagnostics before 1.0

- #7 completed bounded LazyRegistry success diagnostics on 2026-09-26.
  `DEP-DBG-LOAD-002` records plugin, module, triggering access and caller.
  See [the completed proposal](completed_proposals/lazy_registry_smonitor.md).
- `LazyRegistry` still performs a whole permitted-plugin scan at first access.
  Selective declared loading is available separately through `DeclaredRegistry`
  from 0.14.0; changing legacy loading semantics has no accepted plan.

## Candidate priorities for next cycle

1. 1.0.0 release narrative closure

Review the public contracts through 0.15.1, consolidate migration/support notes
and name the release decision owner. No 1.0 candidate or publication date is set.

2. Final contract verification

Re-validate API/CLI/schema contracts and release-gate consistency before tagging.

3. Ecosystem sign-off traceability

Record relevant receiving-consumer acceptance and compatibility limitations,
including the status of MolSysMT #382. Existing audit decisions and provider release
receipts do not substitute for candidate-specific integration evidence.

## Open design questions

These are unaccepted ideas, not scheduled features or 1.0 blockers. A concrete
consumer requirement and an owning proposal must precede implementation.

1. Version constraints policy

Should DepDigest support optional minimum-version checks as part of dependency declarations?

2. CI profile standardization

Should we provide a built-in strict profile for `depdigest audit` + introspection checks to simplify downstream CI adoption?

3. Introspection schema contract

The `dict/json` output already carries documented `depdigest.get_info` schema
version `1.0`, protected by contract tests. Schema evolution needs a consumer
requirement and an explicit compatibility decision.

## Route to 1.0.0

The versioned entries above describe delivered history. Remaining work follows
the [1.0 checklist](release_1.0.0_checklist.md):

1. Close contract, support, migration and consumer-acceptance decisions.
2. Select an exact candidate and reviewed release route.
3. Execute the required source, installed-artifact and receiving-integration
   gates for that candidate; retain their distinct scopes and evidence.
4. Record an explicit go/no-go decision before any 1.0 tag or publication.

### After 1.0.0

- Reconsider #6/#8 when a representative consumer provides a justified need.
- Successful LazyRegistry diagnostics are already delivered under #7. Per-entry
  loading is available through the separate declared registry API; changing
  legacy semantics remains an unaccepted design change.
