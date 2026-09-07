---
summary: Evaluate an epoch-cached decorator fast path and its observability cost.
issue: uibcdf/depdigest#6
status: open
opened: 2026-09-07
closed:
verification: measured
area: [performance, observability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Proposal: an epoch-cached fast path for `@dep_digest`, and the observability it would cost

**Status:** proposal (2026-08-15). Measured on this host, with the command next to each figure.
**Recommendation:** do not implement before 1.0.0, and decide it **jointly** with
[`lazy_registry_smonitor.md`](lazy_registry_smonitor.md) — see section 5, they are the same
decision seen from two sides.
**Origin:** follow-up to `../completed_proposals/fast_dependency_cache.md`, which took the per-call
overhead from 1198 ns to 631 ns. This document asks how much of the remainder is reachable.

---

## 1. Where the remaining overhead goes

With the dependency present and no `when={...}`, `decorator.py:87-120` runs three nested Python
calls per invocation to reconfirm something that does not change:

1. `resolve_config(module_path)` — an `lru_cache` hit,
2. `cfg.libraries.get(library, {})` and `lib_info.get('pypi')`,
3. `check_dependency(...)` with four keyword arguments, which itself calls `is_installed(...)` —
   another `lru_cache` hit.

## 2. What a fast path would buy

Modelled on the trick SMonitor already uses (`smonitor/core/decorator.py`, the
`if config is not plan[0]` identity check): a module-level epoch counter, bumped by
`register_package_config`, `unregister_package_config`, `clear_package_configs` and
`temporary_package_config`. The wrapper records the epoch at which its check passed; if the epoch
still matches, it goes straight to `func(*args, **kwargs)`.

| | ns/call | overhead |
|---|---:|---:|
| bare function | 66 | — |
| **`@wraps` passthrough — the floor** | 188 | **122** |
| epoch cache, closure cell | 223 | **157** |
| epoch cache, list | 241 | 176 |
| **`@dep_digest` today** | 575 | **507** |

**The overhead drops from ~507 to ~157 ns (3.2x), but only 35 of those 157 ns are DepDigest's own
work.** The other 122 ns are the irreducible cost of wrapping a Python function at all. Of today's
507 ns, roughly **385 are reachable**; the rest cannot go without ceasing to be a Python wrapper.

Verified while measuring: a **missing** dependency still raises on every call — a negative verdict
is never cached — and a bumped epoch forces re-verification.

### The larger, less obvious win

When the dependency is present, `check_dependency` has **no observable effect**: everything in it
hangs off `if not is_installed(...)` (`checker.py:26`). So once verified, the entire `when={...}`
machinery can be skipped, because the only thing a condition decides is whether to call a function
that will do nothing. That collapses the conditional case — today the most expensive at 720 ns —
into the same fast path. In production, where dependencies are installed, this is the dominant case.

**This is also the single riskiest part of the proposal.** See 4.3.

## 3. Ecosystem impact

Five `@dep_digest` wrappers run per `puw.get_value` call (measured in
`pyunitwizard/devguide/pending_proposals/telemetry_cost_remeasured_and_signal_boundary.md`,
section 2.1). At ~350 ns saved each, that is **~1.8 us of a 31.3 us call, about 6 %**.

Real, but an order of magnitude below the 13.4 us of PyUnitWizard's own overhead that the same
document identifies as the next cost block. **This proposal does not change where the next
bottleneck is.**

## 4. What it would cost

Stated before deciding, not after.

### 4.1 It removes the hook that made the ecosystem measurable

The wrapper-counting method just documented in PyUnitWizard's proposal works by reading
`resolve_config.cache_info()` deltas — the wrapper consults the cache once per invocation. A fast
path that returns early **never calls `resolve_config`**, and that counter stops moving. The
observability disappears together with the cost.

Today that hook exists *by accident*, as a side effect of redundant work. If the fast path lands,
an explicit counter has to replace it, or the ecosystem loses its cheapest way to answer "how many
wrappers does this call traverse?".

### 4.2 It pulls against the other pending proposal

`lazy_registry_smonitor.md` wants **more** visibility into which optional dependencies actually get
exercised. Skipping the `when={...}` evaluation makes it impossible to know afterwards which
conditions were evaluated or which dependencies were touched. One document wants to erase exactly
what the other wants to record.

### 4.3 It couples the fast path to an internal detail of `check_dependency`

The argument in section 2 — that skipping `when={...}` is unobservable — holds only because
`check_dependency` does nothing when the dependency is present. That is true today. The day someone
adds success-path telemetry there, which is precisely what 4.2 asks for, the skip turns it into dead
code and **no existing test would fail**. A comment is not enough; the invariant needs a test that
pins it.

### 4.4 Contract freeze

DepDigest is in a feature freeze heading to 1.0.0 with contract stability as a hard blocker. This
changes observable behaviour in a narrow case: today `resolve_config` is consulted per call, so a
configuration change is seen immediately; with epochs it is seen only if the change goes through the
four public registration functions. Mutating `_PACKAGE_CONFIGS` by hand would stop working —
although that is already broken today, since `resolve_config` is `lru_cache`d.

`lazy_registry_smonitor.md` was deferred to 1.1.0 on this same argument. Applying it to one
proposal and not the other would be incoherent.

### 4.5 One more invariant that degrades quietly

Every new path that mutates `_PACKAGE_CONFIGS` must remember to bump the epoch. Today it must
already remember `resolve_config.cache_clear()`, so this is not new — but it doubles what there is
to remember. Mitigate with a single private helper that does both, rather than two parallel
disciplines.

### 4.6 What is *not* a problem

By elimination, and checked while measuring: negative verdicts are never cached; error attribution
is unchanged, since a missing dependency never reaches the fast path; under the GIL the integer read
is benign, and a torn read under free-threading costs at most a redundant re-check; and the
staleness of installing a package mid-session already exists today through `is_installed`'s
`lru_cache`.

## 5. Recommendation

**Defer to 1.1.0 and decide together with `lazy_registry_smonitor.md`.**

Sections 4.1-4.3 are all the same question: *how much observability is how many nanoseconds worth?*
One proposal buys speed by erasing information; the other buys information at the cost of speed.
Deciding them separately guarantees the second partially undoes the first.

Against 6 % of a call whose dominant cost lies elsewhere, spending pre-1.0 contract risk is a poor
trade **today**. It may be a good one once 1.0.0 has shipped and the observability boundary has been
settled deliberately.

## 6. How to verify

```bash
# per-wrapper overhead as it stands
python benchmarks/decorator_overhead.py

# every figure in section 2, plus the two correctness checks
python benchmarks/decorator_fast_path_probe.py
```

`benchmarks/decorator_fast_path_probe.py` carries the prototype decorators behind section 2. They
are **prototypes, not shipped code**: nothing in the package imports them, and they exist so these
figures can be re-measured on any host before the deferred decision is taken. The script also
asserts the two properties the proposal relies on — a missing dependency raising on *every* call,
and re-verification after an epoch bump — so a change that quietly broke either would fail loudly
rather than produce an optimistic number.

Confirmation run of that script on the provenance host, reported as
`overhead_*` keys: floor 124 ns, current 500 ns, epoch-cached 155 ns, DepDigest's own work above the
floor 31 ns, reachable saving 345 ns. Those differ from section 2 by a few nanoseconds in each row,
which is the run-to-run spread on a shared host — the ratios hold, the absolutes should not be
quoted to the nanosecond.

## 7. Provenance

Single host: Python 3.13.14, x86_64, Linux 7.0.0, `depdigest` 0.10.0+2, `smonitor` 0.12.0,
`pyunitwizard` 0.22.0. Each figure is the mean of 300,000 iterations via `timeit`. The bare-function
control stayed at 66-71 ns across every run.

Per-call figures at this scale are sensitive to the host and to what else it is doing: treat them as
ratios between rows measured in the same session, not as absolutes.
