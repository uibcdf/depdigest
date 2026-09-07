---
summary: Adopt the shared issue-backed developer-guide lifecycle.
issue: uibcdf/depdigest#5
status: resolved
opened: 2026-09-07
closed: 2026-09-07
verification: inspected
area: [governance, reporting]
guard: tests/test_reporting_protocol.py
normative: devguide/reporting_protocol.md
blocked_by: []
supersedes: []
---

# Adopt the shared issue-backed developer-guide lifecycle

## What

Bring DepDigest's reports under the common MolSysSuite lifecycle while preserving its
existing open-work curation and completed-proposal archive.

## How

Document path mappings, add the shared metadata template, generate queue and archive
indexes, validate offline, and give all current queued proposals stable issues.

## Why

The proposal queue distinguishes open and completed work but did not connect the open
records to GitHub issues or provide a synchronized bug-report surface.

## Acceptance criteria

- Current queued proposals have open issues and common metadata.
- Generated indexes cover queues and the documented archive mappings.
- Offline validation guards metadata and lifecycle consistency.
- Contributor guidance routes local and suite-wide work correctly.

## Resolution

DepDigest now validates issue identity and lifecycle metadata offline, generates its
queue and archive indexes, and maps its established completed-proposal directory into
the common archive. The three product proposals remain open as issues #6, #7, and #8;
the pre-adoption fast-cache record remains immutable through a named exemption.
