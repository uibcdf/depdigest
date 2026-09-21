---
summary: Guard direct Conda releases and promote exact staged files.
issue: uibcdf/depdigest#15
status: active
opened: 2026-09-21
closed:
severity: high
verification: inspected
area: [packaging, release, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Guard direct Conda releases and promote exact staged files

## What

The current DepDigest workflow uploads a manually dispatched candidate to staging,
but a later stable GitHub Release rebuilds build `py_0` and uploads it to `main`.
Labels do not give identical owner/package/version/subdir/filename coordinates
independent file identities. A staged `py_0` may therefore collide with the release
upload rather than publishing the tested candidate. This is an inspected risk in
DepDigest, not a claimed hosted failure here. The same mechanism was measured in
Pytest Receptor and SMonitor under `uibcdf/molsyssuite#27`.

## How

Follow the proposed shared two-route contract while keeping one-job noarch build
mechanics local. A reviewed release plan in the candidate commit names the exact
version, `direct` or `staged` route, rationale, decision owner, and required gates.
Both routes check exact-commit CI and retain a bounded receipt.

For `direct`, the stable Release event checks that no distribution for the version
exists in any Anaconda label, builds/tests build `py_0` from public dependencies,
uploads once to `main`, and independently matches the public file digest. Ambiguous
registry state fails closed. For `staged`, manual dispatch builds/tests only to
staging. The Release event rejects direct upload, and a separate explicit promotion
dispatch names the exact staged coordinate, tag SHA and SHA-256. The shared Action
adds the `main` label to the same file without rebuilding or replacing it.

The SMonitor implementation in `uibcdf/smonitor#20` is a noarch reference; central
decision criteria remain proposed in `uibcdf/molsyssuite#27`. The Python 3.14
candidate under `uibcdf/depdigest#14` requires staging and installed-package gates.

## Why

Staging would otherwise introduce a release-time collision or silently alter the
validated bytes. Removing all release-triggered publication would regress ordinary
unstaged releases. The two routes preserve automatic routine publication while
making staged releases exact-file promotions.

## Acceptance criteria

- The route is decided in the candidate commit before any staging or release tag.
- A staged plan cannot enter the release-triggered direct uploader.
- A direct plan requires exact-commit gates, an unoccupied version, package tests,
  producer evidence, and an independent public digest postcheck.
- Promotion checks the stable release identity and exact staged coordinate/digest,
  retains its receipt, and does not rebuild, re-upload or overwrite the file.
- Negative tests cover route mismatch, occupied version, registry error and digest
  mismatch; hosted execution later verifies each route without claiming synthetic
  local tests are a public release.

## Current status

The two-route code, explicit promotion workflow, local procedure, and negative
tests are committed. The candidate release plan selects `0.11.0` and `staged`
because the first Python 3.14 artifact needs installed-package and consumer
checks before public visibility. The exact candidate
`9913c1e2041494dc01cd85d3173d9e8675ad5df8` passed its required 12-cell
source matrix in run `35646637134`. Hosted staging run `35646813805`
exercised the guarded staged route successfully and retained route/producer
receipts; the independently queried `noarch` file has SHA-256
`ac41c5bd79eea47c3206efb58aede50da0e2f1f10b5791f000bd2f3df1d19082`.
The clean installed-package gate then passed producer verification and all
12 Linux/macOS/Windows × Python 3.11--3.14 jobs in run `35660591628`.
The workflow and negative provenance tests passed locally (104/104 tests on
Python 3.13 and 3.14 with 12 workers; Ruff clean). The staged route is now
hosted-proven up to installed-package testing. The direct route and promotion
remain unexercised; consumer gates, stable release, public promotion, public
install and Zenodo verification remain open.
