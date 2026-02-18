# Roadmap & Future Steps

DepDigest is currently at release **0.4.0**.

This roadmap captures likely next increments toward broader stable adoption.

## Recently delivered in 0.4.0

- CLI auditing workflow (`depdigest audit`) with CI-friendly exit behavior and JSON output.
- Structured introspection output in `get_info(..., format="table|dict|json")`.
- Expanded docs and tests around dependency introspection and architecture verification.

## Candidate priorities for next cycle

1. Docs automation helpers

Evaluate Sphinx helpers/extensions that can auto-extract dependency contracts from `_depdigest.py` examples.

2. Richer remediation hints

Improve dependency-missing guidance with clearer package-manager hints and project-specific URLs.

3. Plugin discovery evolution

Evaluate whether `LazyRegistry` should support non-filesystem discovery modes (for example entry points).

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

- Decide and implement (or explicitly reject) non-filesystem plugin discovery evolution for `LazyRegistry`.
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

### 0.9.x - Release candidates

- Run one or more RC iterations (`0.9.0`, `0.9.1`, ...) with external feedback.
- Accept only blocking fixes for `1.0.0` readiness.

### 1.0.0 - Stable release

- Public API and documented contracts are treated as stable.
- User and developer documentation are complete and consistent.
- CI/release workflows are considered production-stable.
