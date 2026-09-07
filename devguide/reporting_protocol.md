# Reporting protocol

This repository implements the common lifecycle accepted in `uibcdf/molsyssuite#11`.
The central policy owns the shared meanings; this document maps them to DepDigest.

## Ownership and identity

DepDigest-specific bugs and proposals use `uibcdf/depdigest#<number>`. Suite-wide work
uses `uibcdf/molsyssuite`. Every queued document must have an owning issue, while an
incoming issue may close after triage without acquiring a document.

## Local paths

- `pending_bugs/`: open defects;
- `pending_proposals/`: open proposals;
- `solved_bugs/`: resolved defects;
- `completed_proposals/`: implemented proposals;
- `archive/withdrawn_proposals/`: withdrawn or superseded proposals.

These resolved locations form the permanent archive. The historical fast-cache report
listed in `devtools/devguide_reports.py::LEGACY_ARCHIVE` predates adoption and remains
immutable without retrofitted issue metadata. No queued report is exempt.

## Filing and closing

Open the issue first, copy `templates/report.md`, fill the common metadata, expand What /
How / Why, and regenerate indexes. On closure, set the closed status and date, cite a
test in `guard` or a durable rule in `normative` for resolved work, move the record to
its mapped archive, regenerate, and close the issue with the outcome and record path.

**Archive, never delete.** Correct open reports in place. Append a dated correction to
an archived report instead of rewriting its historical claim. GitHub and report state
must agree after filing and closing; board operations remain manual and authenticated,
while the repository guard stays offline.

## Checks

```bash
python devtools/devguide_index.py
python devtools/devguide_index.py --check
python -m pytest -q tests/test_reporting_protocol.py
```
