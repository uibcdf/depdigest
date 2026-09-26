# DepDigest Python support-library applicability

This is DepDigest's local applicability decision under the effective MOLI
support-library policy, tracked by `uibcdf/depdigest#18` and the MolSysSuite
inventory. The policy requires a library when its boundary exists; it does not
require all four libraries as dependencies.

## Current boundaries

| Library | Decision | Evidence |
| --- | --- | --- |
| SMonitor | Applicable and used | Missing-dependency and plugin-load diagnostics in `depdigest/_private/smonitor/catalog.py`, `depdigest/core/checker.py`, and `depdigest/core/loader.py`; `tests/test_core.py` checks emitted events and fallback behavior. |
| DepDigest | Implemented here | This package provides optional-dependency discovery and explanation; adding itself as a dependency has no meaning. |
| PyUnitWizard | Not applicable | The public API does not parse, convert, or validate physical quantities. |
| ArgDigest | Not applicable to the present API | The public entry points below perform ordinary shape checks, not nontrivial scientific constraints, argument normalization, or cross-field validation. |

The ArgDigest review considered each public check:

- `register_package_config` requires a nonempty package name and a `DepConfig`
  instance. These are routine type and presence errors.
- `LazyRegistry` accepts one of two discovery modes and requires a group name
  for entry-point mode. This is ordinary constructor shape validation.
- `get_info` accepts one of three output formats. Its format check is an
  ordinary enum error.
- `dep_digest` compares `when` values to select whether a dependency check
  applies. It does not certify or normalize the caller's scientific arguments.
- `check_dependency` tests package availability, which is DepDigest's own
  optional-dependency boundary rather than argument validation.

ArgDigest's published manifest depends on DepDigest. Adding ArgDigest here for
the routine checks above would introduce a dependency cycle and an unused
support-library dependency. If DepDigest later adds a nontrivial public
argument rule, review that rule before implementation and record a cycle-free
design or a bounded policy exception in `uibcdf/depdigest#18` or a successor
issue. A simple new enum or type check does not by itself change this decision.

The separate developer-tools review is adopted: hosted pytest uses the `ci`
profile with an exact published Pytest Receptor pin, and GH Run Receptor was
used to inspect exact-commit CI, full-matrix, feasibility, and policy runs.
Its measured evidence is retained in
`devguide/completed_proposals/review_inherited_python_ecosystem_policy.md`.
