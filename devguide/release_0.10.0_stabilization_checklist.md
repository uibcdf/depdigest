# Release 0.10.0 Stabilization Checklist

This checklist captures the external-validation stabilization cycle after `0.9.0`.

## External integrator validation

- [ ] Validate DepDigest in at least one real downstream library.
- [ ] Run downstream CI flows that include dependency-gated paths.
- [ ] Confirm `depdigest audit` integration works in downstream CI.
- [ ] Record feedback issues with severity (`blocking` vs `non-blocking`).
- [x] Shared collective E2E module exists and runs locally (`tests/e2e/test_collective_error_path.py`).

## Contract stability checks

- [ ] Public API contract tests remain green in this repo.
- [ ] CLI contract tests remain green in this repo.
- [ ] `get_info` schema remains stable (`depdigest.get_info@1.0`) or has migration notes.
- [ ] Any compatibility-sensitive change is documented in `CHANGELOG.md`.

## Stabilization fixes

- [ ] Fix all blocking issues reported by downstream validation.
- [ ] Keep changes limited to stabilization (no unrelated feature intake).
- [ ] Ensure SMonitor diagnostics remain catalog-driven and traceable.

## Quality gates

- [ ] `pytest -q` passes.
- [ ] Coverage remains in the established high-coverage band.
- [ ] `depdigest audit` returns expected status in repository self-check.
- [ ] `make -C docs html` succeeds.

## Release preparation

- [ ] Add `0.10.0` section in `CHANGELOG.md` (Added/Changed/Migration Notes).
- [ ] Update `devguide/roadmap.md` to mark `0.10.0` delivered.
- [ ] Commit and push release-ready state.
- [ ] Create and push tag `0.10.0` (no `v` prefix).
