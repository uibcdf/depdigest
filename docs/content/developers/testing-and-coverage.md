# Testing and Coverage

DepDigest is infrastructure. Regressions are expensive downstream, so tests must cover behavior, not only lines.

## 1. Minimum local test command

```bash
pytest -q
```

## 2. Coverage command

```bash
pytest --cov=depdigest --cov-report=term-missing
```

## 3. Architecture audit command

```bash
depdigest audit --src-root depdigest --soft-deps openmm,mdtraj
```

## 4. Areas that should always be covered

1. Missing dependency behavior in `check_dependency`.
2. Conditional decorator paths (`when={...}`) in `@dep_digest`.
3. `LazyRegistry` behavior when plugin imports fail.
4. Config resolution behavior:
- package with valid `_depdigest.py`;
- package without `_depdigest.py`;
- broken `_depdigest.py`.
5. Diagnostics emission and fallback paths for SMonitor integration.

## 5. Test design guidance

Prefer tests that assert user-visible behavior:
- exception class and message quality;
- actionable install hints;
- deterministic output for introspection APIs.

Avoid brittle tests tightly coupled to internal implementation details unless those details are part of the contract.
