---
summary: Share optional-engine availability and truthful installation routes across scientific consumers.
issue: uibcdf/depdigest#22
status: open
opened: 2026-09-30
closed:
severity: medium
verification: reproduced
area: [dependency, integration]
guard: tests/test_optional_engines.py
normative: docs/content/user/optional-engines.md
blocked_by: []
supersedes: []
---

# Optional scientific engines

## What

Complete the existing DepDigest/SMonitor optional-dependency recipe for original
Python engines and local executable engines. Ownership remains in DepDigest;
scientific execution and result conversion remain in the consumer.

## How

TopoMT needs pip-only Pocketeer, AlphaSpace2 and pyCASTA plus the Conda-installed
fpocket command. Main at `edce73e10ffb8b94a336f1862e7b5700f989d1cf` already supplies
conditional guards and consumer documentation/channel metadata. However, explicit
`conda=None` is treated as an absent value, disabled routes produce commands naming
`None` in the inventory, the inventory ignores the channel, and executable plugins
use Python discovery.

The prepared implementation shares kind-aware availability between the checker,
decorator, inventory and LazyRegistry. Executables use current PATH/permissions
without executing a command. Explicit disabled routes return `None` in the
inventory and are absent from hints. Existing Python defaults and public inventory
keys remain compatible. The adoption page describes both provider and consumer
responsibilities; the canonical provider-owned integration guide is updated.
Suite adoption is tracked in `uibcdf/molsyssuite#62`.

Evidence: provider suite 129 passed and one collective sibling test skipped in an
isolated checkout; Ruff passed; HTML documentation built with two existing index
heading warnings. TopoMT's latest consumer regression selection passed 61 tests;
29 dependency/catalog tests passed against this prepared provider, and three
installed-distribution comparisons passed on Linux/Python 3.13.14. AlphaSpace2's
published unbound contact initialization requires a consumer compatibility step;
pyCASTA's absolute internal imports require process isolation. Those are not
availability mechanisms to move into DepDigest.

## Why

MolSysMT already adopts the core guard mechanism, while MolSysViewer uses a
different consumer exception contract. Future DockingMT and ElastNetMT should find
one owned recipe and shared tests rather than duplicate executable discovery,
invent install commands, or silently substitute a scientific method.

## Acceptance criteria

- Review, integrate and release the provider changes; do not mark this proposal
  complete merely because its isolated implementation passes tests.
- Preserve Python guard behavior and SMonitor event contracts.
- Keep disabled installers and declared channels consistent across entry points.
- Synchronize the accepted canonical guide through MolSysSuite.
- Track consumer adoption and retirement of local executable compatibility checks.
- Keep transitive imports, service state, execution failures and scientific parity
  distinct from availability.
