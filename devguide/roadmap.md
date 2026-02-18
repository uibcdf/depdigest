# Roadmap & Future Steps

DepDigest is currently at release **0.3.0**.

This roadmap captures potential next increments toward a broader, stable adoption path.

## Candidate priorities

1. CLI auditing workflow

Create a `depdigest audit` command that wraps AST validation utilities and reports import-leak violations in a CI-friendly format.

2. Docs automation helpers

Evaluate Sphinx helpers/extensions that can auto-extract dependency contracts from `_depdigest.py` examples.

3. Richer remediation hints

Improve dependency-missing guidance with clearer package-manager hints and project-specific URLs.

## Already in place

- Runtime dependency enforcement through `@dep_digest`.
- Conditional enforcement support via `when={...}`.
- Lazy plugin/module loading through `LazyRegistry`.
- Runtime configuration resolution and registration (`register_package_config`).
- Structured diagnostics integrated through SMonitor.
- User and Developer docs expanded into guided learning paths.

## Open design questions

1. Version constraints policy

Should DepDigest support optional minimum-version checks as part of dependency declarations?

2. Plugin discovery scope

Should `LazyRegistry` support additional discovery mechanisms (for example entry points) beyond filesystem scanning?

3. Output ergonomics

Should introspection output include an optional machine-readable profile optimized for CI checks and agents?
