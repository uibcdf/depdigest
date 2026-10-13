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


## Hosted runner recovery — 2026-10-13

Candidate e275703 passes routine CI, policy/governance and nine source cells,
including macOS/Python 3.12. Three macos-latest jobs remain queued without assigned
runners after more than thirty minutes. Preserve this as partial, superseded
source evidence; it cannot authorize publication.

Use the supported explicit macos-15 ARM64 runner for all four source and all four
installed macOS cells. GitHub documents it as a standard M1 runner, like
macos-latest; MolSysSuite's current Python CI policy requires macOS ARM64 and
permits this platform choice. This is a runner choice, not a platform exception
or unexecuted-gate waiver. Source/installed job names, exact native profiles and
reviewed workflow byte hashes agree on the new label. All three operating systems,
four Python minors, full source tests and clean installed gates remain required.
No package runtime/dependency/constructor changes accompany this recovery.

All gates reset on the resulting exact candidate. Public tagging/admission still
awaits executed source and installed matrices. Responsible maintainer: Diego;
operational runner selection can be reviewed at the next release using actual
queue/runtime evidence. Shared coordination is recorded in MolSysSuite #115.


The initial runner-selection commit 1f8911d fails one existing matrix guard that
still expects the old label (`test_python314_candidate_contract.py`); routine CI
38458737813 records 299 passes, five omissions and that one failure. Correct the
expected label consistently and run the whole private suite before fixing the
next candidate. This test failure is retained and cannot qualify publication.


The replaced matrix 38452565534 did not respond to normal cancellation. Its
`always()` full-test condition lets queued work continue even after cancellation;
GitHub documents force-cancel for exactly this condition. The force-cancel endpoint
retired that superseded run. The source lane now uses `!cancelled()` so dependency
skip/failure still permits the full matrix, while requested cancellation stops it.
The existing required-cell guard also protects this control. This changes no
passing-gate criteria; obsolete or cancelled jobs still cannot qualify a release.
Official recovery reference: https://docs.github.com/en/actions/how-tos/troubleshoot-workflows.
