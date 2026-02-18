# Developers

Welcome. This section is for contributors who want to develop, maintain, or extend DepDigest.

The path below is intentionally ordered. If you follow it in sequence, you will go from a local setup to production-ready contributions with the same conventions used in this repository.

If your goal is integrating DepDigest into your own package (not contributing to this repository), start in the [User section](../user/index.md).

## Developer Path

1. [Contributing Workflow](contributing-workflow.md): branch, commit, and PR expectations.
2. [Development Environment](development-environment.md): local setup, test commands, and docs build.
3. [Architecture](architecture.md): how DepDigest is structured and why key design decisions were made.
4. [Implementation Patterns](implementation-patterns.md): how to implement features without breaking runtime behavior.
5. [SMonitor for Contributors](smonitor-for-contributors.md): diagnostics contract and emission rules.
6. [Testing and Coverage](testing-and-coverage.md): required test strategy and coverage workflow.
7. [Editorial Guide](editorial-guide.md): style and structure rules for docs and developer-facing text.
8. [Release and Versioning](release-and-versioning.md): practical release flow and tagging checks.
9. [Contributor Checklist](contributor-checklist.md): final pre-PR and pre-release checklist.

## Canonical References

- Project-level implementation contract: [DEPDIGEST_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/standards/DEPDIGEST_GUIDE.md)
- SMonitor integration authority for this repository: [SMONITOR_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/SMONITOR_GUIDE.md)
- Internal design notes used to build this section: `devguide/`

```{toctree}
:maxdepth: 1
:hidden:

contributing-workflow.md
development-environment.md
architecture.md
implementation-patterns.md
smonitor-for-contributors.md
testing-and-coverage.md
editorial-guide.md
release-and-versioning.md
contributor-checklist.md
```
