# Roadmap & Future Steps

DepDigest is currently at public release **0.11.1**, including Python 3.14
support. Its noarch Conda artifact is verified; the Zenodo source snapshot
recorded below belongs to release 0.11.0.

This roadmap captures likely next increments toward broader stable adoption.

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
  a Python 3.13 consumer smoke; its own Python 3.14 transition is next.

### 0.11.1

- Repaired the Windows `depdigest` launcher in the noarch Conda recipe.
- Passed twelve clean installed-package cells across Linux, macOS, and Windows
  before promoting the same SHA-256-verified file to the public channel.
- Independently installed the public file on Linux/Python 3.13 and ran the
  installed command outside the source checkout.

### 1.0.0 (in progress)

- Prepare final release narrative and final go/no-go checklist.
- Keep contract stability and release-gate reproducibility as hard blockers.

## Candidate priorities for next cycle

1. 1.0.0 release narrative closure

Consolidate final migration notes and ecosystem compatibility statements.

2. Final contract verification

Re-validate API/CLI/schema contracts and release-gate consistency before tagging.

3. Ecosystem sign-off traceability

Link collective evidence artifacts for final pre-1.0 confidence.

## Open design questions

1. Version constraints policy

Should DepDigest support optional minimum-version checks as part of dependency declarations?

2. CI profile standardization

Should we provide a built-in strict profile for `depdigest audit` + introspection checks to simplify downstream CI adoption?

3. Introspection schema contract

Should the `dict/json` output from `get_info` be versioned as a formal public schema contract?

## Route to 1.0.0

This is the working milestone path toward a stable `1.0.0` release.

### 0.5.0 - Contract stabilization

- Finalize and document the `get_info(format="dict|json")` schema contract.
- Improve dependency-missing remediation hints (clearer install guidance/context).
- Publish a recommended CI profile for integrators (`depdigest audit` + key checks).

### 0.6.0 - Controlled extension

- Deliver non-filesystem plugin discovery evolution for `LazyRegistry` (entry points).
- Harden dynamic config and runtime registration edge cases.
- Expand advanced integration docs around these behaviors.

### 0.7.0 - Hardening

- Increase regression coverage in critical orchestration paths.
- Lock down behavior expectations for public API surfaces.
- Reduce technical debt that could affect stability.

### 0.8.0 - Release candidate preparation

- Freeze new feature intake.
- Focus on bug fixing, API/docs consistency, and release quality.
- Finalize deprecation/support policy notes for the stable line.

### 0.10.0 - Stabilization

- Run external validation and address stabilization fixes only.
- Keep contracts stable while gathering final confidence before `1.0.0`.

### 1.0.0 - Stable release

- Public API and documented contracts are treated as stable.
- User and developer documentation are complete and consistent.
- CI/release workflows are considered production-stable.

### 1.1.0 - Post-stable diagnostics

- Instrument successful `LazyRegistry` loads with a catalog-driven `lazy_load` signal
  (`devguide/pending_proposals/lazy_registry_smonitor.md`, reduced scope A).
- Deferred out of the 1.0.0 line on purpose: useful but not blocking, and the full-fidelity
  variant would change observable `LazyRegistry` semantics during the contract freeze.
