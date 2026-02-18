# About

DepDigest is a dependency orchestration layer for Python libraries that need
optional integrations without sacrificing startup performance.

The common problem in scientific and analytical packages is this:
- users want many optional backends and formats;
- developers add imports eagerly;
- import time grows, and missing dependency errors appear in confusing places.

DepDigest addresses that with explicit runtime dependency guards and lazy loading.

## The Problem It Solves

- Avoids accidental heavy imports at module import time.
- Enforces dependency checks only when code paths need them.
- Supports lazy plugin/registry loading by dependency availability.
- Emits structured diagnostics through SMonitor.

## How It Works

1. You declare dependency policy in `_depdigest.py`.
2. You guard runtime entry points with `@dep_digest(...)`.
3. You keep optional imports inside guarded functions.
4. You use `LazyRegistry` to avoid eager plugin/module imports.
5. You expose status via `get_info(...)` if desired.

## Design Tradeoffs

- Zero-cost startup for optional integrations.
- Runtime clarity over silent fallback.
- Structured diagnostics instead of ad-hoc messages.

Tradeoff to accept:
- You must be disciplined with lazy imports and dependency declarations.
- In return, users get deterministic behavior and cleaner failure modes.

## Who Should Use DepDigest

Use it when:
- your package has optional backends/tools;
- import-time performance matters;
- you want consistent dependency diagnostics.

You may not need it when:
- your dependency graph is small and always mandatory;
- import cost is negligible for your use case.
