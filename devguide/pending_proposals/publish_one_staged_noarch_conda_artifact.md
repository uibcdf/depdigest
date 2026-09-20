---
summary: Publish one staged noarch Conda artifact instead of interpreter-platform duplicates
issue: uibcdf/depdigest#13
status: active
opened: 2026-09-20
closed:
verification: measured
area: [packaging, release, tooling]
guard:
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
