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

The `0.11.0` staged route has now passed the entire hosted path. Candidate
`d5b259a0f4ab00756858869061604fd64d561850` passed the 12-cell source
matrix (`35664438560`) and suite policy (`35664438912`). Staging run
`35664759083` produced `noarch/depdigest-0.11.0-py_2.tar.bz2` with SHA-256
`b6ba665d9125f49506b7e4231e6065f164d3b643117a22288b44baafceff270f`.
Installed-package run `35665346654` passed its producer check and all 12
Linux/macOS/Windows × Python 3.11--3.14 cells. A public ArgDigest 0.12.1
consumer smoke passed against the exact staged file. The `0.11.0` tag and
GitHub Release identify that candidate; promotion run `35665723593` copied
the exact file and digest to the public channel without rebuilding. A clean
public-channel Python 3.14 installation and CLI smoke passed. Zenodo archived
the release source snapshot as record `22884369`.

The direct route remains unexercised on a release candidate and is not
claimed proven. The release-triggered direct-build workflow correctly failed
its route guard for staged releases 0.11.0 and 0.11.1; this produced visible
red runs even though explicit promotion succeeded. A later workflow change
selects the committed route before entering the direct branch. For future
staged tags, it skips the direct build and upload while keeping malformed or
mismatched plans as failures. Keep this proposal open until a real direct
release proves the hosted publication path.
