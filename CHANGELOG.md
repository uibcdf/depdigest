# Changelog

All notable changes to this project are documented in this file.

The format is intentionally simple and release-oriented.
Each release should include a **Migration Notes** section when compatibility-sensitive behavior changes.

## [Unreleased]

### Added

- `DeclaredRegistry`: opt-in identity declarations, metadata-only enumeration,
  selective filesystem/entry-point loading, explicit undeclared discovery, dynamic
  overrides and bounded retry/refresh policy (#34).

### Migration Notes

- `LazyRegistry` retains its first-access full scan. `DeclaredRegistry` implements
  `MutableMapping`; visible names can include implementations that fail to load.
  Value access raises `KeyError` with the cause; successful and failed loads are
  cached. Public adoption requires the first published admitting version; 0.13.0
  does not provide this API. No release is authorized by #34.

## [0.13.0] - 2026-10-04

### Fixed

- Static optional-import audits now inspect module and class control flow,
  including if, try/except/else/finally, loops, with and match bodies.
- Simple explicit, unrebound `typing.TYPE_CHECKING` guards, including aliases
  and negation, exclude only their typing branch. Delayed function bodies
  remain excluded.

### Migration Notes

- Audits that previously passed can now report additional imports and exit 1.
  Review the reported import boundary; use a documented, narrow file exemption
  only for an intentional eager adapter. `--allow-violations` still displays
  findings while returning 0. JSON keys and source line reporting are unchanged.
- Unresolved, rebound or compound typing conditions are scanned conservatively.
  The audit does not execute code or prove root-import reachability. Dynamic
  imports remain outside its scope, and syntax-error files retain the historical
  empty result; validate syntax separately.
- Consumer adoption is independent of this provider release and is tracked in
  MolSysSuite #95, ArgDigest #22 and PyUnitWizard #93. Runtime dependency guards,
  configuration and inventory APIs retain their previous contracts.

## [0.12.0] - 2026-09-30

### Added

- Optional executable dependencies with `kind="executable"` and an explicit
  command/path, shared by guards, inventory and plugin discovery. Availability
  follows the current PATH and permissions without executing or installing tools.
- A provider-owned optional-engine recipe and integration guidance, coordinated
  with MolSysSuite and the initial TopoMT consumer.

### Fixed

- Explicit `pypi=None` and `conda=None` installation routes no longer invent hints
  or inventory commands. Declared Conda channels remain consistent across APIs.
- Dotted Python discovery preserves missing transitive dependencies in an
  imported parent instead of reporting the requested engine as absent.

### Migration Notes

- Declare both installer routes explicitly in new optional-engine integrations;
  omitted routes retain legacy defaults. Existing Python keys remain import names.
- Executable entries use capability keys and their actual command/path. A custom
  command must be checked using the same value passed to execution.
- Availability does not certify versions, ABI, service health or scientific
  execution. Preserve those errors at the consumer boundary. No engine is installed
  automatically and no alternative method is silently selected.
- The 0.12.0 candidate follows the staged Conda route with source and installed
  artifact gates before stable tagging and exact-file promotion.

## [0.11.2] - 2026-09-26

### Fixed

- Missing-dependency diagnostics now use the consumer's documentation URL and
  one Conda-first installation hint in both SMonitor and the exception.
- Installed imports read the generated version file without eagerly loading
  `importlib.metadata`; entry-point discovery is loaded only when requested.
- A staged GitHub Release now skips the direct Conda uploader while preserving
  fail-closed route validation.

### Added

- `LazyRegistry` emits a DEBUG diagnostic for each successful plugin load on
  its first scan, including the initiating access and call site.

### Migration Notes

- A plain `check_dependency(...)` call without a declared PyPI package no longer
  suggests pip. Supply `pypi_name` when a pip installation route is supported.
- Consumers can set `DOC_URL` in `_depdigest.py` or pass `doc_url` to `DepConfig`.

## [0.11.1] - 2026-09-26

### Fixed

- The noarch Conda package now installs the `depdigest` command launcher on
  Windows. The staged installed-package gate checks the actual executable
  across Linux, macOS, and Windows with Python 3.11–3.14.

### Migration Notes

- No Python API changes or migration steps.

## [0.11.0] - 2026-09-21

### Added

- Decorator overhead benchmark in `benchmarks/decorator_overhead.py`.
- Python 3.14 metadata and a twelve-cell Linux/macOS/Windows compatibility
  matrix, with a separate twelve-cell clean installation gate for the staged
  Conda artifact. Public 3.14 support depends on the release and public-channel
  postchecks.
- A guarded direct Conda route and exact-file staging promotion procedure,
  together with producer-receipt and installed-artifact verification.

### Changed

- `@dep_digest` and `check_dependency` no longer instrument themselves with SMonitor's
  `@signal`. Missing dependencies keep their catalog-driven diagnostic; successful calls
  no longer emit duplicated internal telemetry.
- Conditional dependency checks (`when={...}`) now precompute the position and default of
  each condition parameter at decoration time, so the common path avoids
  `Signature.bind()`/`apply_defaults()` per call (`bind()` remains as fallback for
  non-ordinary signatures).

### Fixed

- Conditional dependency checks are array-safe: arguments whose `==` returns a vectorized
  result no longer raise an ambiguous-truth-value error; they match only when every
  comparison element is true.
- CI/Conda workflows updated to maintained action versions.

### Migration Notes

- No breaking API changes. Behavior change to be aware of: successful `@dep_digest` calls
  no longer emit internal SMonitor events. Integrators asserting on `dependency`-tagged
  signals for successful calls must update those assertions; missing-dependency
  diagnostics (`DEP-ERR-MISS-001`) are unchanged.

## [0.10.0] - 2026-03-04

### Added

- Collective stabilization evidence synced through shared E2E module usage across sibling repositories.

### Changed

- Stabilization checklist for `0.10.0` completed and recorded.
- Roadmap advanced from `0.9.x` closure to `0.10.0` delivered state and `1.0.0` active preparation.
- CI split model retained (`CI.yaml` fast path + `CI_full_matrix.yaml` scheduled matrix) as stabilized release behavior.

### Migration Notes

- No breaking API changes introduced in `0.10.0`.

## [0.9.1] - 2026-02-27

### Added

- `0.10.0` stabilization checklist in `devguide/release_0.10.0_stabilization_checklist.md`.

### Changed

- Split CI into fast `CI.yaml` (push/PR) and scheduled/manual `CI_full_matrix.yaml`.
- Removed coverage and JUnit report generation from `CI_full_matrix.yaml`.
- Documentation build version now resolves from repository-local `depdigest/_version.py`.
- Developer release gates section expanded to include stabilization phase naming.

### Migration Notes

- No breaking API changes introduced in `0.9.1`.

## [0.9.0] - 2026-02-27

### Added

- RC execution checklist for release `0.9.0` in `devguide/release_0.9.0_checklist.md`.

### Changed

- Roadmap now tracks `0.9.0` as delivered and moves external integrator validation to `0.10.0` stabilization.

### Migration Notes

- No breaking API changes introduced in `0.9.0`.

## [0.8.0] - 2026-02-27

### Added

- Developer-facing support and deprecation policy documentation.
- Explicit pre-RC quality gates in the release workflow docs.
- Changelog workflow with centralized migration notes for release-impacting changes.

### Changed

- Roadmap status updated to close `0.8.0` release-preparation tasks.

### Migration Notes

- No breaking API changes introduced in `0.8.0`.

## [0.7.0] - 2026-02-27

### Added

- Public API contract tests for exported symbols and `get_info` schema expectations.
- CLI contract tests for baseline `depdigest audit` behavior.
- API stability documentation for contributors.

### Migration Notes

- No breaking API changes introduced in `0.7.0`.
