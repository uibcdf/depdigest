# Architecture

DepDigest follows a zero-friction integration model: the host library declares dependency policy in `_depdigest.py`, and DepDigest resolves and enforces that policy at runtime.

## Core design decisions

1. Runtime config resolution (call time)

`@dep_digest` resolves configuration when the decorated function is called, not when it is imported.

Why this matters:
- tests can override config after imports;
- dynamic plugin environments can register config at runtime;
- import-time side effects are minimized.

2. LazyRegistry behaves like a dictionary

`LazyRegistry` was designed for drop-in compatibility with mapping-based registries and conversion tables.

Why this matters:
- easier adoption in existing codebases;
- fewer API migrations in host libraries.

3. Automatic package root discovery

DepDigest infers package context from call-site/module information to find `_depdigest.py` automatically.

Why this matters:
- less boilerplate for integrators;
- consistent behavior across modules of the same package.

## Architectural invariants

Contributors should preserve these invariants:
- soft dependencies must never be required at import time;
- missing soft dependencies must produce actionable diagnostics;
- hard dependency checks must remain explicit and deterministic;
- runtime registration (`register_package_config`) must remain predictable for tests.
