---
summary: Publish one staged noarch Conda artifact instead of interpreter-platform duplicates
issue: uibcdf/depdigest#13
status: resolved
opened: 2026-09-20
closed: 2026-09-20
verification: measured
area: [packaging, release, tooling]
guard: tests/test_noarch_conda_publication.py
normative:
blocked_by: []
supersedes: []
---

# Publish one staged noarch Conda artifact instead of interpreter-platform duplicates

## What

DepDigest is pure Python, but its Conda workflow builds three interpreter jobs and asks
each action invocation to create platform-specific copies. The UIBCDF channel has no
Linux ARM64 DepDigest package.

Publish one `noarch: python` artifact. Manual runs must name an exact commit, version, and
build number and may upload only to `staging`; only a GitHub Release may target `main`.

## How

Adopt the contract proven in `uibcdf/smonitor#16`: a bounded Python recipe, one build
job, exact candidate validation, staging-only dispatch, release-only main publication,
static package-version freezing, recipe-level installed identity checks, and version 2.1
producer evidence. Declare the noarch package kind in the GH Run Receptor rule.

The central dependency source gains the Python and SMonitor bounds already present in
project metadata and the recipe, then regenerates its derived environments so a future
broadcast cannot undo the package contract.

## Why

MolSysMT run `35499866604` measured three Linux ARM64 solve failures because DepDigest
and three sibling support packages have no records for that subdirectory. A pure-Python
package does not need interpreter or native-platform duplication. This is the DepDigest
implementation under `uibcdf/molsyssuite#27`.

## Acceptance criteria

- Tests guard noarch metadata, exact candidate staging, one-job topology, structured
  evidence, and exact installed version identity.
- A hosted run publishes one staged noarch coordinate from the named SHA.
- Clean off-checkout Python 3.11 and 3.13 environments install the coordinate with staged
  SMonitor and import exact DepDigest metadata and module versions.
- The main UIBCDF channel receives no candidate package.

## First hosted attempt

Run `35505813369` failed during recipe rendering, before compilation or upload. The
dependency broadcaster had serialized the parametrized build number as a single-quoted
YAML scalar with doubled inner quotes. YAML could load it, but Jinja rejected it with
`expected token ',', got 'DEPDIGEST_CONDA_BUILD_NUMBER'`.

The broadcaster now restores both version and build-number Jinja expressions after YAML
serialization and resolves all paths from its own location, so the root-level invocation
documented in `devtools/AGENTS.md` works. A test executes it from a temporary repository
root and checks the resulting recipe. Because no coordinate was uploaded, the next
candidate remains build 0.

## Hosted verification

Run `35506310258` built, tested, and uploaded one noarch artifact from exact commit
`5695ca43ddae31b6f7be70a287b940ee0b99a5d2`. GH Run Receptor reported one successful
noarch job and one structured producer-evidence artifact.

Clean off-checkout environments invoked with isolated Python installed
`depdigest-0.10.2-py_0` on Python 3.11 and 3.13. In both environments, distribution
metadata and `depdigest.__version__` were exactly `0.10.2`, and dependency resolution
selected staged `smonitor 0.15.1`. The staging channel lists that single coordinate; the
main UIBCDF channel returns no match for DepDigest 0.10.2.

## Resolution

Implemented in `7a0b45a` and corrected in `5695ca4`. DepDigest now publishes one bounded
noarch package, uses exact-SHA staging dispatch and release-only main publication, freezes
and tests its installed version identity, retains action v2.1 evidence, and advertises the
noarch package kind to GH Run Receptor. Its dependency broadcaster is root-invocable and
preserves both recipe Jinja expressions.

Local validation passed 67 tests with 12 workers plus Ruff, formatting, devguide, and
receptor configuration gates. The guard is `tests/test_noarch_conda_publication.py`.
