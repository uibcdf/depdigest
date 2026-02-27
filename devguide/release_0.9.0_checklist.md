# Release 0.9.0 Checklist (RC)

This checklist is the execution guide for the first release-candidate cycle toward `1.0.0`.

## Scope guard (must hold)

- [x] Only bug fixes, hardening, and documentation consistency changes are included.
- [x] No new feature work is merged unless explicitly required to unblock release quality.
- [x] Public contracts stay stable (`depdigest.__all__`, `get_info` schema, CLI `audit` behavior).

## Contract and compatibility checks

- [x] Public API contract tests pass.
- [x] CLI contract tests pass.
- [x] `get_info(format="dict|json")` schema keys remain unchanged, or migration notes are added.
- [x] Any compatibility-sensitive adjustment is documented in `CHANGELOG.md` under Migration Notes.

## Integration and diagnostics checks

- [x] `_depdigest.py` integration guidance remains aligned with current behavior.
- [x] `DEPDIGEST_GUIDE.md` is updated when integration contract changes.
- [x] SMonitor diagnostics behavior remains consistent with `SMONITOR_GUIDE.md`.
- [x] No hardcoded warning/error strings bypass catalog-driven diagnostics.

## Quality gates

- [x] `pytest -q` passes.
- [x] Coverage run is green and remains in the established high-coverage band.
- [x] `depdigest audit` behavior remains CI-safe (`0/1` exits as documented).
- [x] `make -C docs html` succeeds.

## Documentation gates

- [x] User docs reflect current recommended integration flow.
- [x] Developer docs reflect current release and compatibility policy.
- [x] `CHANGELOG.md` includes a `0.9.0` section with Added/Changed/Migration Notes.
- [x] `devguide/roadmap.md` marks `0.9.0` status correctly before tagging.

## Release mechanics

- [x] Working tree is clean except intended release edits.
- [ ] Release commit is focused and pushed to `main`.
- [ ] Tag `0.9.0` is created and pushed (no `v` prefix).
- [ ] Post-tag sanity checks pass (docs/version references and no local drift).

## Exit criteria for closing 0.9.0

- [ ] External feedback loop has at least one real integrator validation cycle.
- [x] Any issues found are either fixed or triaged as non-blocking for `1.0.0`.
- [ ] Repository is ready to proceed with `0.9.1` (blocking fixes only) or directly to `1.0.0` prep.
