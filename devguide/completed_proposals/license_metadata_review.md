---
summary: Modernize MIT license metadata and qualify compatible build minima.
issue: uibcdf/depdigest#45
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: inspected
area: [distribution, compatibility]
guard:
normative: https://github.com/uibcdf/molsyssuite/blob/41698b982ff56983a49c0089b135ed769a38b9da/devguide/python_license_metadata.md
blocked_by: []
supersedes: []
---

# Modernize MIT license metadata and qualify compatible build minima

## What

Preserve the exact existing MIT notice. Declare SPDX and explicit license files, raise and align the Setuptools capability floor, and inspect real wheel/sdist metadata and notice bytes including a wheel rebuilt from the sdist. Keep source/build qualification separate from a future public candidate.

## How

Review source `02339c2917588a91ba938575be44816d706b5e27` and the immutable references
in the owning issue. Use task-owned copies/environments for executed checks.
Record exact dispositions, evidence and remaining release/consumer limitations.

## Why

Owner confirmation needs measured scope rather than guide receipt, broad CI or
an assumption that a source update qualifies existing public bytes.

## Acceptance criteria

- Complete the owning issue's metadata/runtime/operation-specific review.
- Retain exact executed versions, checks and limitations.
- Archive this report and regenerate indexes on completion.
- Return an explicit Review completed confirmation to the owner and central tracker.

## Resolution — 2026-11-05

The original MIT copyright and notice are unchanged. Project metadata now uses
`license = "MIT"` and `license-files = ["LICENSE"]`. The Setuptools capability
floor is >=77.0.3 in project build requirements, the owning requirements source,
regenerated recipe and setup/build environments. Versioningit remains >=3.0;
Python and runtime dependency requirements are unchanged. Conda descriptive
metadata uses MIT and explicitly includes `LICENSE` from the source root.
No deprecated license classifier was present.

Real private wheel and sdist builds passed on Python 3.14.7 with the exact
minimum Setuptools 77.0.3 and versioningit 3.0.0, without build isolation hiding
a different backend. A wheel rebuilt from the sdist also passed. A modern-tool
wheel passed with Setuptools 84.0.0/versioningit 3.3.0. All four artifacts have
metadata 2.4, `License-Expression: MIT`, `License-File: LICENSE` and the exact
original notice bytes. The receipt retains artifact and notice SHA-256 values.
The private snapshot version is `1+unknown`; these are neither replacements for
0.15.1 nor a new release candidate.

The normative packaging reference requires a compatible declared backend and
actual notice inclusion. Generated-profile checks pass; the future exact-source
and installed Conda matrices, resources/launchers, archive and publication gates
remain required at the next authorized candidate. No historical file is changed.

[Normalized maintenance evidence](../evidence/maintenance_reviews_2026-11-05.json)
retains checked inputs and distinct executed scopes. Owner and central confirmations
link the final adopted commit and hosted controls separately.

Final local checks: 75 selected cases pass without skips with the pinned SDK;
Ruff check/format, generated indexes, relative links and diff checks pass.
