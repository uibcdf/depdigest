# Deprecation and Support Policy

This page defines how DepDigest maintains compatibility while moving toward `1.0.0`.

## Python support window

- DepDigest supports active Python versions listed in `pyproject.toml` classifiers and CI jobs.
- Support for an older Python minor can be dropped in a minor release when maintenance cost or ecosystem constraints justify it.
- When support is dropped, docs, CI, classifiers, and user-facing compatibility notes must be updated in the same release cycle.

## Public API deprecation policy

For symbols in `depdigest.__all__` and documented CLI behavior:

- Prefer additive changes over breaking replacements.
- If a behavior must change, document the deprecation first and keep compatibility for at least one minor release when feasible.
- Emit clear migration guidance in docs and release notes.
- Remove deprecated behavior only after contract tests and docs are updated to the new baseline.

## Schema and contract changes

For `get_info(format="dict|json")` and CLI machine-readable outputs:

- Treat schema/key changes as contract changes.
- Bump the documented schema version when contract changes are intentional.
- Add migration notes for integrators that parse output in CI.

## Contributor checklist for compatibility-sensitive changes

Before merging deprecations or support-window updates:

- update `docs/content/developers/api-stability.md`;
- update `standards/DEPDIGEST_GUIDE.md` when integration contract changes;
- add/adjust contract tests;
- ensure release notes call out migration impact explicitly.
