# Audit CLI

DepDigest includes a lightweight CLI command to detect imports of soft dependencies
in source scopes that can execute while a module is imported.

This helps you enforce lazy-import architecture in CI before regressions reach users.

## Basic command

```bash
depdigest audit --src-root my_pkg --soft-deps openmm,mdtraj
```

Behavior:
- exit code `0`: no violations found;
- exit code `1`: one or more top-level soft-dependency imports found.

## What the audit scans

The audit includes imports inside module-level `if`, `try` (including handlers,
`else` and `finally`), loops, `with`, `match` and class bodies. It skips function
and async-function bodies, including classes defined inside those functions.
Original source line numbers are retained in text and JSON output.

Simple type-check-only branches are excluded when their guard uses an explicit
import from `typing`, including aliases:

```python
from typing import TYPE_CHECKING as TC

if TC:
    import openmm  # excluded: this branch is only for type checking
else:
    import mdtraj  # reported: this is a runtime branch
```

`import typing as t` followed by `if t.TYPE_CHECKING:` and negated guards are
also recognized.
If the name is rebound anywhere in eager source, a wildcard import can shadow
it, or the condition has another shape, both branches are scanned conservatively.
Assignments to a recognized module's `TYPE_CHECKING` attribute also disable its
exemption. Rebindings inside delayed function bodies do not change this scan.

Other conditions are not evaluated: even `if False:` is scanned. The audit does
not follow calls, dynamic imports or module reachability. An optional adapter
loaded only on request can still contain an import that is reported when its
source is audited; inspect that boundary before choosing an explicit exemption.
Syntax-error files retain the historical behavior of producing no findings.
A zero exit code is therefore not a syntax check or proof of absent runtime
import leaks; pair the audit with compilation and relevant import regressions.

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
