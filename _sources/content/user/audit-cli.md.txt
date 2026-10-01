# Audit CLI

DepDigest includes a lightweight CLI command to detect top-level imports of soft dependencies.

This helps you enforce lazy-import architecture in CI before regressions reach users.

## Basic command

```bash
depdigest audit --src-root my_pkg --soft-deps openmm,mdtraj
```

Behavior:
- exit code `0`: no violations found;
- exit code `1`: one or more top-level soft-dependency imports found.

## CI-friendly JSON output

```bash
depdigest audit --src-root my_pkg --soft-deps openmm --json
```

## Exemptions

Use exemptions for generated files or intentionally eager modules:

```bash
depdigest audit \
  --src-root my_pkg \
  --soft-deps openmm \
  --exempt-file my_pkg/legacy_bridge.py \
  --exempt-dir my_pkg/tests
```

## Allow violations temporarily

If you need a non-blocking transition period:

```bash
depdigest audit --src-root my_pkg --soft-deps openmm --allow-violations
```

This still reports violations but returns exit code `0`.

## Next

Use the [Production Checklist](production-checklist.md) to finalize release readiness.
