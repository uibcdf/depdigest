# About

DepDigest is a dependency orchestration layer for Python libraries that rely on optional integrations and plugin ecosystems.

Its goal is simple: keep import-time startup light, while making runtime dependency behavior explicit, actionable, and diagnosable.

## Why DepDigest exists

In many scientific and analytical Python libraries, optional capabilities are added over time (backends, formats, connectors, acceleration engines). Without explicit dependency discipline, this usually leads to:

- top-level imports of optional packages;
- slow and fragile package initialization;
- dependency failures surfacing far from the real call site;
- inconsistent, low-context user messages.

DepDigest addresses this by centralizing dependency policy and enforcing it where execution actually happens.

## What DepDigest provides

1. Runtime dependency guards with `@dep_digest(...)`.
2. A contract file (`_depdigest.py`) to declare hard and soft dependencies.
3. Lazy loading patterns through `LazyRegistry`.
4. Introspection utilities (for example `get_info(...)`) to expose current environment capability status.
5. Structured diagnostics via SMonitor for traceable, actionable error/warning paths.

## Design principles

1. Runtime clarity over implicit behavior.

Dependency decisions should happen where execution happens, not at import time.

2. Fast default startup.

Optional integrations should not penalize users who do not use them.

3. Contract-driven integration.

Dependency behavior should be declared once and reused consistently (`_depdigest.py` and `DEPDIGEST_GUIDE.md`).

4. Diagnostics as product behavior.

Missing dependencies are expected states in optional ecosystems. They should be explained clearly, with remediation hints.

## What DepDigest is not

DepDigest does not replace package managers, environment solvers, or full observability stacks.

It is focused on one problem: robust optional-dependency orchestration inside Python libraries.

## Who should use DepDigest

DepDigest is a good fit when your library:

- has optional engines, formats, or plugin integrations;
- needs to keep import-time overhead low;
- wants predictable dependency checks and high-quality diagnostics;
- is maintained by multiple developers and benefits from a shared dependency contract.

It may be unnecessary for very small packages with only mandatory dependencies and negligible startup/import cost.

## Contracts and references

- Integration contract: [DEPDIGEST_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/standards/DEPDIGEST_GUIDE.md)
- SMonitor integration authority in this repository: [SMONITOR_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/SMONITOR_GUIDE.md)
- User onboarding path: [User section](../user/index.md)
- Contributor onboarding path: [Developers section](../developers/index.md)
