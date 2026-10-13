---
summary: Serialize concurrent declared adapter requests without false recursion errors.
issue: uibcdf/depdigest#39
status: active
opened: 2026-10-13
closed:
severity: medium
verification: reproduced
area: [registry, concurrency]
guard: tests/test_concurrent_first_load.py
normative:
blocked_by: []
supersedes: []
---

# Concurrent declared registry requests

## What

MolSysMT #382 requests safe overlapping first adapter loads on a shared
DeclaredRegistry. Published 0.15.0 explicitly lacks synchronization; the second
thread currently receives a false recursive-load KeyError. This is a new bounded
consumer requirement, not evidence of scientific corruption.

## How

Review the proposed per-registry RLock, retain same-thread recursive refusal and
coherent success/failure cache/provenance, and use event-controlled provider guards
before integration. Existing registry contracts and both policies must pass.
Document the exact scope and public admission independently from consumer adoption.

## Why

Consumers should use the owning provider rather than subclassing it, duplicating
caches or requiring all adapters to be prewarmed. Mutation/discovery and arbitrary
cross-registry cycles do not receive an untested concurrency promise.

## Acceptance criteria

- Overlapping declared value requests share one initialization and identical value.
- Real recursion fails within a bounded process timeout; failures/cause caching/retry remain.
- Current visibility, selective loading and diagnostics remain coherent.
- Source and installed/public qualification admit the supported scope before a consumer floor.
- Archive the owning record, hand off to MolSysMT #382 and MolSysSuite #115.


## Reproduction and implementation — 2026-10-13

Eight event-controlled overlapping cases fail before the fix with a false
recursive-load KeyError; both bounded real-recursion controls already pass.
The proposed per-registry RLock, owned by `core/registry.py`, makes all 62 registry
cases pass without changing caller capture or loader machinery. The lock remains
held through initialization/cache/diagnostics; coarse serialization avoids
races in shared load provenance and supports independent same-thread nested loads.
Different cold adapters on one registry no longer initialize in parallel; this is
a correctness tradeoff, not a throughput improvement claim.

Prepare compatible patch 0.15.1 with unchanged dependencies and constructor.
Installed qualification adds a reusable, isolated, bounded reader probe. Source
and installed gates and immutable public promotion are still pending; no consumer
floor or adoption is changed by source implementation alone.


## Local candidate qualification — 2026-10-13

Private source snapshot (editable `1+unknown`, not a release artifact), clean
Python 3.14.8/public SMonitor 0.16.0 py_1/public pytest-receptor 1.1.0 py_1:
298 passed, five sibling-workspace omissions; pip check is clean. All ten new
reader guards pass separately under existing read-only Python 3.11, 3.12 and 3.13
environments. Python 3.12 lacks the receptor and reports its unknown-config
warning; native pytest still succeeds. The public twelve-cell matrix remains the
platform qualification gate. All twenty pinned SDK distribution routes, Ruff,
formatting and report indexes pass.

The installed probe's positive contract succeeds. A non-reentrant Lock mutation
is killed by its bounded process control, rather than hanging the test worker.
No shared environment or primary editable version metadata was changed.


## Qualification correction — 2026-10-13

The first source candidate c90edca passes routine CI, policy and governance,
and eight Linux/Windows full-matrix cells; four macOS cells are queued. Review
found the bounded negative probe could leave child fixtures after killing a
non-reentrant-lock regression. The parent now owns the child's temporary root
and removes it after success, failure and timeout. Cleanup guards exercise
success/injected failure and actual killed-child retirement. This is a verifier
lifecycle correction, not a runtime change; the candidate and full matrix are
reset before public admission. Earlier partial source evidence is superseded.


After that correction, the complete private suite passes 300 cases with the same
five sibling omissions. Positive/injected-failure/actual killed-child controls
verify parent-owned retirement. The two identified local pre-correction fixture
roots were retired after matching their unique probe signature and checking no
active reference; caller/shared resources were preserved.

A bounded local warm-getter measurement (Linux/Python 3.14.8, empty explicit
configuration, seven repeats of 100000 calls) gives baseline median 0.417 us and
RLock median 0.587 us, a 0.170 us increase. This small synthetic cost and coarse
serialization are accepted for coherent initialization. It is not a consumer
throughput/speed result; consumers own later measurements.
