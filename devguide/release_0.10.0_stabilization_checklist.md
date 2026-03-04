# Release 0.10.0 Stabilization Checklist

This checklist captures the external-validation stabilization cycle after `0.9.0`.

## External integrator validation

- [x] Validate DepDigest in at least one real downstream library.
- [x] Run downstream CI flows that include dependency-gated paths.
- [x] Confirm `depdigest audit` integration works in downstream CI.
- [x] Record feedback issues with severity (`blocking` vs `non-blocking`).
- [x] Shared collective E2E module exists and runs locally (`tests/e2e/test_collective_error_path.py`).

## Contract stability checks

- [x] Public API contract tests remain green in this repo.
- [x] CLI contract tests remain green in this repo.
- [x] `get_info` schema remains stable (`depdigest.get_info@1.0`) or has migration notes.
- [x] Any compatibility-sensitive change is documented in `CHANGELOG.md`.

## Stabilization fixes

- [x] Fix all blocking issues reported by downstream validation.
- [x] Keep changes limited to stabilization (no unrelated feature intake).
- [x] Ensure SMonitor diagnostics remain catalog-driven and traceable.

## Quality gates

- [x] `pytest -q` passes.
- [x] Coverage remains in the established high-coverage band.
- [x] `depdigest audit` returns expected status in repository self-check.
- [x] `make -C docs html` succeeds.

## Release preparation

- [x] Add `0.10.0` section in `CHANGELOG.md` (Added/Changed/Migration Notes).
- [x] Update `devguide/roadmap.md` to mark `0.10.0` delivered.
- [x] Commit and push release-ready state.
- [x] Create and push tag `0.10.0` (no `v` prefix).
