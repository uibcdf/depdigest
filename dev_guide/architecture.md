# Architecture & Critical Decisions

DepDigest is built around the "Zero-Config" philosophy: a library should only need a configuration file (`_depdigest.py`), and the orchestrator should handle the rest.

## Critical Decisions Taken

1.  **Dynamic Runtime Resolution**:
    *   *Decision*: The `@dep_digest` decorator resolves the project configuration at runtime (call time) instead of definition time (import time).
    *   *Rationale*: This is crucial for **testing and mocking**. It allows tests to inject alternative configurations after the modules have already been imported.

2.  **Inheritance from `dict` for `LazyRegistry`**:
    *   *Decision*: The lazy loader acts exactly like a dictionary.
    *   *Rationale*: It allows seamless integration with existing code that expects conversion maps or plugin registries without changing the call sites.

3.  **Automatic Root Discovery**:
    *   *Decision*: Using `func.__module__` to find the package root.
    *   *Rationale*: It eliminates the need for developers to manually pass configuration objects to decorators, mirroring the successful pattern of `ArgDigest`.

4.  **Symmetry with ArgDigest**:
    *   *Decision*: Adopting the `_dep_digestion` and `_depdigest.py` naming convention.
    *   *Rationale*: It reduces the cognitive load for developers working within the UIBCDF ecosystem.

## Pending Decisions

1.  **Inter-dependency Resolution**:
    *   How should we handle a situation where `SoftDep_A` requires `SoftDep_B`? Currently, we assume the developer handles this inside the lazy import block.
2.  **Version Enforcement**:
    *   Should `@dep_digest` also check for minimum versions? This would add complexity but increase robustness.
