---
summary: The noarch Conda package omits the depdigest launcher on Windows.
issue: uibcdf/depdigest#19
status: active
opened: 2026-09-24
closed:
severity: medium
verification: inspected
area: [conda, cli]
guard: tests/test_conda_recipe.py::test_noarch_recipe_declares_the_installed_console_launcher
normative:
blocked_by: []
supersedes: []
---

# Noarch Conda package omits its Windows launcher

## What

`pyproject.toml` declares `depdigest = depdigest.cli:main`, but the noarch Conda recipe
omitted `build.entry_points`. Its Linux recipe test ran `depdigest --help`, yet the
published noarch package did not create the Windows command launcher.

## How

Declare the exact console entry point in the recipe. The staged installed-package
matrix must find the `depdigest` executable inside its Conda prefix and run that
executable with `--help` instead of running `python -m depdigest`.

## Why

The module invocation can work while the user-facing command is missing. The existing
staged matrix already includes Windows, so the launcher check can make that gap visible
before promotion.

## Acceptance criteria

- The noarch recipe declares the same command and target as `[project.scripts]`.
- The installed-package gate rejects a missing or foreign launcher on Windows.
- A new staged package build passes the Windows matrix from a clean installation.
- Public availability is claimed only after a new immutable build coordinate is
  independently verified.

## Current state

The recipe and staged-install gate are corrected on `main`, with focused local tests.
Version `0.11.1` build `py_0` passed hosted installed-artifact verification on
Linux, macOS, and Windows with Python 3.11–3.14. The existing public package is
not considered repaired: this exact file is labeled `staging` only.

## Staged evidence — 2026-09-26

- Candidate commit: `456ae6b7bcce1402c6504e2cf74d3721f2dcd39e`.
- Exact source matrix: [run `36229520653`](https://github.com/uibcdf/depdigest/actions/runs/36229520653),
  12/12 passed on attempt 2. Windows/Python 3.12 first hit a temporary
  `__pycache__` copy race in `test_broadcast_requirements`; the failed cell
  passed unchanged on rerun.
- Staging producer: [run `36229720222`](https://github.com/uibcdf/depdigest/actions/runs/36229720222),
  `depdigest-0.11.1-py_0.tar.bz2`, SHA-256
  `bc54290422dc8af90d7d9f75f64fc12ece6b5da78e04dc66a3b7ddf2882799fa`.
- Installed-package gate: [run `36229868929`](https://github.com/uibcdf/depdigest/actions/runs/36229868929),
  producer receipt verified and 12/12 clean installations passed, including all
  four Windows cells. Each cell located `depdigest` inside its Conda prefix and
  ran `depdigest --help` outside the source checkout.
- Independent Anaconda release query listed this one noarch file with only the
  `staging` label and the same SHA-256. No public promotion or post-public
  verification has been performed.
