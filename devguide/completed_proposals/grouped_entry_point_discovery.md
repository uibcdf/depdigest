---
summary: Decide grouped entry-point discovery ownership and freshness from measured evidence.
issue: uibcdf/depdigest#31
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: medium
verification: measured
area: [discovery, performance]
guard: tests/test_entry_point_discovery.py
normative:
blocked_by: []
supersedes: []
---

# Assess grouped entry-point discovery

## What

Ackredit #117 requested a standalone provider assessment, distinct from module
registry loading. The accepted decision is to retain the standard-library
`importlib.metadata.entry_points` operation, with a fresh query at the consumer's
actual first demand or explicit reload. There is no new DepDigest runtime API,
persistent cache, dependency floor, consumer adoption or release in this change.

## How

The reproducible provider probe is `benchmarks/entry_point_discovery.py`; its
contract and measurement table are in `benchmarks/README.md`. The retained receipt
`benchmarks/results/entry_point_discovery_2026-10-13.json` contains 150 fresh-process
samples, wheel/file verification and tool/source hashes. Five normally installed
controlled profiles reuse Ackredit's existing fixture builder and verifier at
`4d1a1094f165a574efcb516b83cbf89351683347`. Seven timing and three separate Python
allocation samples cover each of three modes. Build/install, Python startup and
module import are outside timing; filesystem cache state is uncontrolled.

Single-demand discovery costs 5.55–6.89 ms; a simultaneous two-group snapshot costs
5.67–7.11 ms, versus 7.97–10.27 ms for two separate queries. This is metadata-only
Linux/Python 3.14.8 evidence, not Ackredit report timing, a clean published-runtime
closure, statistical significance, scientific correctness or a portable guarantee.

Eight guards preserve entry-point order/identity, same-name points from distinct
distributions, duplicate-distribution selection, ZIP layouts, custom in-memory
finders, late installation in the same/new site and single-group demand. Directed
guards execute on Linux/Python 3.11–3.14. In particular, fresh queries see newly
installed providers while an old snapshot does not. No plugin implementation is
loaded by metadata discovery.

## Why

The standard library already owns supported finder/layout behavior and offers
`entry_points().select(group=...)` for truly simultaneous demands. A native snapshot
may be selected for both groups only when no intervening registration can change
discovery. Independent first format demand and citation reload must query afresh;
a callback can alter provider availability even between groups in one public call.
A blanket cache narrows that existing contract. These measurements do not justify
a faster single-demand implementation or a second discovery engine in DepDigest.
Registration callbacks, conflict handling and warning catalogs remain Ackredit's.

Reopen provider design only with a measured workload and explicit freshness contract
that require capabilities beyond native selection. Consumer adoption and public
release qualification remain separate future work.

## Acceptance criteria

- Provider ownership and supported approach are explicit: standard-library metadata.
- Existing discovery semantics and late-provider freshness have addressable guards.
- Reproduction, raw bounded measurements and limitations are maintained here.
- The decision is handed back to Ackredit #117 after published source gates pass.

## Published source closeout — 2026-10-13

Implementation `5744450a0778eb2d801cabd95d61ccda092a823b` was pushed directly
without skipping CI. Exact-head native CI 38375008495, MolSysSuite policy
38375009891 and publication governance 38375009553 pass; GH Run Receptor independently
reports an executed successful CI test job. Owning issues #33 and #31 are closed;
local resource disposition was delivered to MolSysSuite #104 and discovery ownership
to Ackredit #117. Useful manifest-owned resources remain through the separately
authorized #36 follow-on; final disposal is reported separately.
