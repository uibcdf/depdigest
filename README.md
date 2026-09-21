# DepDigest

[![MolSysSuite: Support Library](https://img.shields.io/badge/MolSysSuite-support%20library-2563eb?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#support-library)
[![MolSysSuite policy](https://github.com/uibcdf/depdigest/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/depdigest/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13 | 3.14](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/depdigest)](https://github.com/uibcdf/depdigest/blob/main/LICENSE)
[![Tests](https://github.com/uibcdf/depdigest/actions/workflows/CI.yaml/badge.svg?branch=main)](https://github.com/uibcdf/depdigest/actions/workflows/CI.yaml)
[![Codecov](https://codecov.io/github/uibcdf/depdigest/graph/badge.svg)](https://codecov.io/github/uibcdf/depdigest)
[![Documentation](https://github.com/uibcdf/depdigest/actions/workflows/sphinx_docs_to_gh_pages.yaml/badge.svg)](https://www.uibcdf.org/depdigest/)
[![GitHub release](https://img.shields.io/github/v/release/uibcdf/depdigest)](https://github.com/uibcdf/depdigest/releases/latest)
[![Conda](https://img.shields.io/conda/vn/uibcdf/depdigest)](https://anaconda.org/uibcdf/depdigest)
[![Zenodo DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22884368.svg)](https://doi.org/10.5281/zenodo.22884368)

*Digesting dependencies into clear, actionable insight.*

## Overview

**DepDigest** is a lightweight Python library for managing **optional dependencies** and **lazy loading** in large analytical or scientific projects.

It helps maintain a "Zero-Cost Startup" by ensuring that heavy external libraries are only checked and imported when actually needed.

Understand your dependencies. Trust your code.

Current release line:
- `0.11.0` delivered with Python 3.14 support on the published noarch Conda package
- `1.0.0` preparation in progress

## Documentation

- User guide: `docs/content/user/index.md`
- Developer guide: `docs/content/developers/index.md`
- Contribution guide: `CONTRIBUTING.md`
- Implementation contract: `standards/DEPDIGEST_GUIDE.md`
- Conda release routes: `devguide/conda_release_routes.md`

## Key Features

- **`@dep_digest` Decorator**: Enforce dependency availability at runtime with clear error messages.
- **Lazy Loading**: Discover and load modules (plugins, forms) from directories only when accessed.
- **Architecture Validation**: Tools to scan your codebase and ensure no top-level imports of soft dependencies leak into your core.
- **Audit CLI**: `depdigest audit` command for CI-friendly lazy-import checks.
- **Symmetry with ArgDigest**: Designed to work in tandem with argument validation frameworks.
- **smonitor integration**: Structured diagnostics for missing dependencies.
- **Runtime config discovery**: Automatically resolves package `_depdigest.py`.
- **Manual config registration**: Supports dynamic/testing contexts via `register_package_config`.

## Quick Example

```python
from depdigest import dep_digest, get_info


@dep_digest("openmm")
def simulate(system):
    import openmm
    # ...


def dependency_info():
    return get_info("my_package")
```

## smonitor

DepDigest emits structured events when a dependency is missing. Configuration is
loaded from `_smonitor.py` in the package root (`depdigest/_smonitor.py`), and
the catalog lives in `depdigest/_private/smonitor/catalog.py` with metadata in
`depdigest/_private/smonitor/meta.py`.

## Installation

```bash
conda install -c uibcdf depdigest
```

## Requirements

- Published `0.11.0`: Python `>=3.11,<3.15`. Its public Conda build was
  independently installed on Python 3.14 after twelve-cell staged-package
  testing on Linux, macOS, and Windows.
- Runtime dependency: `smonitor`

## Development

Run tests:

```bash
pytest --receptor=llm -n 12
```

Run tests with coverage:

```bash
pytest --receptor=llm -n 12 --cov=depdigest --cov-report=term-missing
```

Run architecture audit:

```bash
depdigest audit --src-root depdigest --soft-deps openmm,mdtraj
```

Build docs locally:

```bash
make -C docs html
```

## License

MIT License.
