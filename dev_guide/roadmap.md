# Roadmap & Future Steps

DepDigest is currently in **v0.1.1 (Alpha)**. The following steps are planned to move it toward a stable release.

## What remains to be done?

1.  **CLI Tooling**:
    *   Create a standalone CLI command (`depdigest audit`) that wraps the AST tools to scan projects for top-level imports.
2.  **Sphinx Integration**:
    *   Develop a Sphinx extension that reads `_dependencies` metadata from functions and automatically adds "Required: [Library]" notes to the HTML documentation.
3.  **Comprehensive Error Context**:
    *   Enhance the error messages to include not just the missing library, but also installation instructions tailored to the OS (detected via `sys.platform`).

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
