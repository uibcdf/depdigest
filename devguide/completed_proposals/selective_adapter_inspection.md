---
summary: Add explicit adapter inspection while retaining strict loading and execution checks.
issue: uibcdf/depdigest#36
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: measured
area: [registry, optional-engines]
guard: tests/test_declared_registry.py::test_adapter_inspection_keeps_visibility_and_guarded_execution
normative:
blocked_by: []
supersedes: []
---

# Explicit selective adapter inspection

## What

DepDigest #36 extends the owning DeclaredRegistry implementation with explicit,
keyword-only `load_policy="adapter"`. Omission or `"strict"` retains the published
0.14.0 dependency precheck. Invalid policies raise ValueError. There is no copied
registry, consumer private override, new dependency/provider floor or legacy change.

## How

The adapter policy skips only the pre-import mapped soft dependency check. Current
visibility still applies before materialization, including cached entries. Identity,
success/failure caching, retry/refresh, explicit discovery, mutation, recursion and
existing SMonitor provenance retain their owner implementation. The same option
covers filesystem and entry-point routes. Import/transitive failures remain real
chained causes, and inventory reports actual engine availability.

Fifteen proposed-policy cases failed before implementation. All 52 registry cases
now pass on local Linux/Python 3.11–3.14. Tests cover absent Python/executable engines,
both visibility modes, unrelated failing sentinel custody, current config over cached
adapters, real import failures with one diagnostic and explicit retry, identity
rejection, refresh/discovery/mutation, explicit/default strict parity and unchanged
legacy all-capability materialization. The named guard actually loads metadata while
the engine is absent, then calls a decorated operation and requires ImportError
before its body. It also proves inventory absence and untouched unrelated plugins.

A bounded consumer control uses an unmodified git-archive snapshot of MolSysMT
`c38a2e146936fad4d199a26e9f5a5c5033377a9a`, exactly the original request commit.
On Linux/Python 3.14.7, with CuPy absent, the new policy exposes `cupy_ndarray`
`form_type='class'` and XYZ converter metadata; the adapter was not already imported
after host initialization. Strict lookup still fails and a restricted config hides
the cached adapter; restoring config exposes the same object. This uses shared
developer dependencies read-only, and does not prove full consumer adoption,
conversion parity, clean runtime closure or scientific execution. Normalized source
and consumer proof: `devguide/evidence/selective_adapter_inspection_2026-10-13.json`.

## Why

MolSysMT #382 needs adapter metadata without every optional scientific engine.
Importability is distinct from execution. Hosts still own `dep_digest` or
`check_dependency` at execution-dependent operations, and no engine is implicitly
installed, chosen or substituted. Strict and adapter policies are explicit; neither
configuration nor metadata access silently enables the new behavior.

This resolves provider source implementation only. Published 0.14.0 does not accept
this option. A later admitted minor release, prospectively 0.15.0, needs its own exact
source matrix, staged installed validation, immutable tag/Release and same-file
promotion before a public capability floor. Existing 0.14.0 release receipts/plan
remain historical; no new tag, artifact or publication is made here. MolSysMT #382
adoption/conversion parity and any speed claims remain consumer-owned, coordinated
in MolSysSuite #115 with motivating ElastNetMT #26.

## Acceptance criteria

- Explicit adapter loading preserves strict default, legacy behavior and visibility.
- Metadata inspection does not certify availability or scientific execution.
- Identity/failure/provenance/retry/mutation/discovery guards pass on 3.11–3.14.
- Canonical guide, public contract and unreleased notes specify the admission boundary.
- Exact provider source and scoped compatibility evidence are handed to the consumer
  and central coordination; public release and consumer adoption remain separate.

## Published source closeout — 2026-10-13

Implementation `4e962e8664e942a89e43da3e6819ac9cb5b5d98a` is pushed unskipped.
Exact-head CI 38376365712, policy 38376366821 and publication governance
38376366804 pass. Explicit source matrix 38376389645 passes all twelve Linux,
macOS and Windows / Python 3.11–3.14 cells. Native job facts prove both distribution
checks and test steps succeeded in each cell; its unrelated optional backlog-decision
helper is intentionally skipped. GH Run Receptor confirms twelve executed successful
test jobs. Clean local full source proof is 280 passed / five unavailable sibling
integration skips. These are source gates, not new installed/public artifact gates.

Issue #36 closes provider implementation, with the exact source contract and
unreleased/public admission boundary delivered to MolSysMT #382 and MolSysSuite
#115. Public 0.14.0 and consumer adoption remain unchanged. Final owned resource
retirement is recorded separately in the component's lifecycle receipt.

## Public capability admission — 2026-10-13

Release #37 publishes DepDigest 0.15.0 at candidate
`01d83c7b176a2b6cdcbdb42d33f3060f2eda5af7`. Twelve source cells and twelve
clean installed cells pass; the same staging archive is promoted and independently
verified in public main/index/download/installation. The registry resource retains
this implementation's exact bytes. Public use of `load_policy="adapter"` can now
require DepDigest >=0.15.0. Source-only statements above remain dated historical
checkpoints. Release proof: `devguide/evidence/release_0.15.0_2026-10-13.json`.
MolSysMT #382 adoption/parity/performance remains separately owned.
