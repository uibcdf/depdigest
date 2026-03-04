# CI Profile

This page provides a recommended CI baseline for libraries integrating DepDigest.

Goal: catch optional-dependency regressions early while keeping pipelines simple.

## Recommended checks

1. Run tests

```bash
pytest -q
```

2. Run coverage

```bash
pytest --cov=your_package --cov-report=term-missing
```

3. Run architecture audit for soft dependencies

```bash
depdigest audit --src-root your_package --soft-deps openmm,mdtraj
```

4. (Optional) Emit machine-readable dependency status

```python
from depdigest import get_info
payload = get_info("your_package", format="json")
```

## Minimal GitHub Actions job example

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.13"
      - run: python -m pip install . --no-deps
      - run: pytest -q
      - run: depdigest audit --src-root your_package --soft-deps openmm,mdtraj
```

## Why this profile works

- tests validate behavior;
- coverage highlights untested branches;
- audit guards lazy-import architecture;
- optional JSON introspection helps agents/automation.

## Next

Use the [Production Checklist](production-checklist.md) before release.
