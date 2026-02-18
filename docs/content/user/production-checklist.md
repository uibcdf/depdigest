# Production Checklist

Use this checklist before releasing a library integrated with DepDigest.

## Dependency Policy

- [ ] `DEPDIGEST_GUIDE.md` is present in project root and reviewed by the team.
- [ ] The project root keeps `DEPDIGEST_GUIDE.md` near package `_depdigest.py`.
- [ ] `_depdigest.py` exists in package root.
- [ ] `LIBRARIES` keys are importable module names.
- [ ] `type` values (`hard`/`soft`) reflect real policy.
- [ ] `pypi`/`conda` names are correct.
- [ ] `MAPPING` covers plugin directories that need optional dependencies.

## Runtime Integration

- [ ] Optional paths are guarded with `@dep_digest(...)`.
- [ ] Optional imports are inside guarded functions (no top-level leaks).
- [ ] Conditional paths use `when={...}` where appropriate.
- [ ] `LazyRegistry` is used for plugin-heavy areas when needed.

## User Experience

- [ ] Missing dependency errors are clear and actionable.
- [ ] Dependency status is exposed (for example via `get_info(...)`).
- [ ] Install hints shown to users match real package channels.

## Testing

- [ ] Tests cover missing dependency behavior.
- [ ] Tests cover conditional dependency paths.
- [ ] Tests cover lazy registry non-fatal plugin import failures.
- [ ] Tests cover `_depdigest.py` missing vs broken behavior.
- [ ] Coverage is tracked in CI.

## Diagnostics

- [ ] SMonitor integration is active and catalog wiring is correct.
- [ ] No silent diagnostic failure hides critical behavior.

If all boxes are checked, your integration is typically ready for release.

Canonical source for the latest contract:
- [DEPDIGEST_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/standards/DEPDIGEST_GUIDE.md)
