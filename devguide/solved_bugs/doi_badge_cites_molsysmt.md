---
summary: The README DOI badge cites the MolSysMT archive.
issue: uibcdf/depdigest#10
status: resolved
opened: 2026-09-19
closed: 2026-09-19
severity: high
verification: reproduced
area: [documentation, citation, releases]
guard: tests/test_readme_metadata.py
normative:
blocked_by: []
supersedes: []
---

# The README DOI badge cites the MolSysMT archive

## What

DepDigest's README used Zenodo badge repository ID `137937243`. GitHub's public API
identifies that repository ID as `uibcdf/molsysmt`, and Zenodo redirects the badge to
`10.5281/zenodo.17850104`, the MolSysMT 0.12.0 record.

## How

Remove the false badge rather than replacing it with an unverified DOI. A bounded
anonymous audit on 2026-09-19 found no `depdigest` record in the Zenodo Records API, and
the correct GitHub repository-ID badge endpoint returned 404. The separate archival
follow-up is `uibcdf/depdigest#11` under `uibcdf/molsyssuite#24`.

## Why

A citation badge is a public identity claim. Pointing at another component can produce
incorrect citations and cannot be retained while DepDigest's own archival state is
`absent`.

## Acceptance criteria

- The MolSysMT badge ID is absent from the DepDigest README.
- A regression test protects the repository identity boundary.
- The central badge proposal and Zenodo inventory record the measured finding.
- Restoring a DOI badge requires independently verified DepDigest evidence.

## Resolution

The foreign DOI badge was removed. `tests/test_readme_metadata.py` prevents the known
MolSysMT repository ID and redirect from returning to DepDigest. The public audit found
no DepDigest record, so no replacement DOI was asserted; `uibcdf/depdigest#11` owns the
required archival work before the next release.
