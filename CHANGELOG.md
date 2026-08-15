# Changelog

All notable changes to this project are documented in this file.

The format is intentionally simple and release-oriented.
Each release should include a **Migration Notes** section when compatibility-sensitive behavior changes.

## [Unreleased]

### Added

- Decorator overhead benchmark in `benchmarks/decorator_overhead.py`.

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
