# Roadmap & Future Steps

DepDigest is currently in **v0.1.1 (Alpha)**. The following steps are planned to move it toward a stable release.

## What remains to be done?

1.  **CLI Tooling**:
    *   Create a standalone CLI command (`depdigest audit`) that wraps the AST tools.
2.  **Sphinx Integration**:
    *   Develop a Sphinx extension to auto-document required dependencies.
3.  **Comprehensive Error Context**:
    *   Enhance the error messages to include installation instructions tailored to the OS.

## Current Progress

- **v0.1.1**: 
    - Full telemetry integration with `@smonitor.signal`.
    - Unit test suite established with 100% core coverage.
    - Dynamic configuration resolution finalized.
    - Support for manual package configuration registration.

## Future Potential Steps

1.  **Dynamic Installation Hints**:
    *   Allow the configuration to define alternative PyPI/Conda names or specific channels.
2.  **Performance Profiling Mode**:
    *   A mode that reports how much time is being "saved" by not importing optional dependencies.
3.  **Integration with standard packaging**:
    *   Potentially reading optional dependencies directly from `pyproject.toml` (extra requirements).

## Critical Next Decisions

*   **Standardization of `LazyRegistry`**: Should it support non-directory based plugins (e.g. entry points)?
*   **Dependency on Pandas**: Should we offer a built-in `info()` function that doesn't require Pandas for environments that don't have it?