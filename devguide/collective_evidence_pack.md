# Collective Evidence Pack

This document is the cross-repo handoff artifact for collective validation with:
- `../smonitor`
- `../argdigest`
- `../pyunitwizard`

## What this is

`collective_evidence_pack.md` is the canonical checkpoint record for DepDigest:
- local evidence already validated in this repository,
- required cross-library E2E evidence,
- pending items that cannot be closed locally.

## How to use this file

1. Before each RC/stabilization checkpoint:
- refresh local evidence and references.

2. During cross-repo synchronization:
- compare status notes across all four repositories.

3. At go/no-go decisions:
- use decision placeholders to record owner, date, blockers, and evidence links.

## How to update this file

1. Update metadata (`Date`, `baseline`, `head reference`).
2. Refresh local quality and dependency-policy evidence.
3. Keep only reproducible, in-repo references.
4. Do not mark collective closure from local-only evidence.

Date: `2026-03-04`
DepDigest baseline: `0.10.0` delivered, `1.0.0` preparation window
DepDigest head reference for this pack: `09b2302` (`0.10.0`)

## 1. Local quality baseline (DepDigest)

- Source status references:
  - `devguide/roadmap.md`
  - `devguide/release_0.10.0_stabilization_checklist.md`

## 2. Contract evidence index (DepDigest)

Use this section to keep concrete, local references for:
- shared collective error-path E2E module: `tests/e2e/test_collective_error_path.py`,
- `_depdigest.py` hard/soft policy contract,
- `depdigest audit` behavior and coverage,
- `get_info` schema contract and compatibility,
- remediation hint quality and diagnostics integration.

## 3. Collective E2E target scenario (must be validated across repos)

Goal:
- dependency-related failures provide actionable remediation hints that appear in
  the same E2E path where PyUnitWizard/ArgDigest/SMonitor propagate diagnostics.

Minimum acceptance evidence:
- reproducible command/workflow,
- captured output/events or artifact,
- per-library references to tests/commits proving the path.

## 4. Shared status template

```md
Status note (YYYY-MM-DD):
- smonitor: <done locally|in progress|blocked|pending> (<reference>)
- depdigest: <done locally|in progress|blocked|pending> (<reference>)
- argdigest: <done locally|in progress|blocked|pending> (<reference>)
- pyunitwizard: <done locally|in progress|blocked|pending> (<reference>)
- collective validation: <pending|in progress|done> (<evidence>)
```

## 5. Status note (2026-03-04)

- smonitor: in progress (`0.11.4-16-ge0e1a8c`, collective closure still pending)
- depdigest: done locally (`0.10.0`, stabilization checklist closed and tagged)
- argdigest: in progress (`0.9.0-9-gc543c1a`, remediation-hint path pending collective closure)
- pyunitwizard: done locally (`0.21.1-1-g9fd9b46`, post-RC stabilization active)
- collective validation: in progress (shared E2E green; collective finality criteria still pending in molsyssuite)

## 6. Pending collective closures (from DepDigest perspective)

- collective `depdigest audit` leak checks across sibling libraries,
- collective proof of remediation hints in E2E contract failure path,
- startup/import-cost budget validation in ecosystem-level runs.

## 7. Decision log placeholders

- `go/no-go owner`:
- `date`:
- `collective evidence links`:
- `open blockers`:
- `resolution plan`:
