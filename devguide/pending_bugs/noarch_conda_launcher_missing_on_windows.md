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

The recipe and staged-install gate are corrected in source, with focused local tests.
Hosted installed-artifact evidence is pending; the existing public package is not
considered repaired by this source change alone.
