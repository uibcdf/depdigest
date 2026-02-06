# Introduction to DepDigest

**DepDigest** is a lightweight, zero-dependency infrastructure library designed to manage **optional dependencies** and **lazy loading** in complex Python ecosystems.

## What is it?
It is a "Dependency Orchestrator" that decouples the definition of a library's requirements from its execution logic. It provides decorators and registry proxies to ensure that external packages are only checked and loaded when strictly necessary.

## What does it do?
1.  **Enforces Availability**: Using the `@dep_digest` decorator, it ensures a library is installed before a function runs, throwing standardized, helpful errors if not.
2.  **Lazy Discovery**: It provides a `LazyRegistry` that scans directories for plugins or modules but avoids importing them until they are actually accessed.
3.  **Automatic Configuration**: It discovers project-specific settings (like `_depdigest.py`) automatically based on the caller's context.
4.  **Codebase Auditing**: It includes AST-based tools to detect "leaky" imports (top-level imports of optional dependencies) that slow down package initialization.
