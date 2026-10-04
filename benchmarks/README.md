# Decorator performance probes

Run these with the qualified Python 3.14 development environment. They measure
warm calls on one host; their timings do not qualify public artifacts, other
platforms or consumer scientific correctness.

- `decorator_overhead.py`: current overhead above a bare scalar function.
- `decorator_fast_path_probe.py`: historical epoch prototypes and wrapper floor.
  Its correctness checks do not cover the current full dependency contract.
- `decorator_consumer_probe.py`: complete MolSysMT extraction and PyUnitWizard
  value-conversion calls, with SMonitor enabled and disabled separately.

## Consumer comparison

The consumer probe requires MolSysMT, PyUnitWizard, OpenMM and Pint, plus their
ordinary dependencies. It does not install anything or skip missing engines.
Optional consumers are not imported by `--help` or when importing the probe.

Use a fresh process for every mode:

```bash
python benchmarks/decorator_consumer_probe.py --mode current
python benchmarks/decorator_consumer_probe.py --mode epoch
python benchmarks/decorator_consumer_probe.py --mode floor
```

`current` runs the shipped guard. `epoch` models cached successful Python checks
without conditions under **fixed configuration**; it deliberately does not
implement invalidation and cannot be deployed. Executable and conditional
guards retain their current checks in that model. `floor` removes dependency
guard frames and is an optimistic timing bound, with no availability enforcement.
Neither model changes the installed package or is imported by product code.

Each run checks input identity or copied atom/bond counts and converted scalar
value, warms its cases, and records medians, ranges, all samples, one-call
dependency-check counts and actual source origins/commits. These bounded output
checks do not substitute for scientific tests. Import/discovery, cold starts,
dependency absence, configuration changes and installation are outside the
timed region. Production error and invalidation behavior is guarded separately
by `tests/test_decorator_cache_contract.py` and `tests/test_optional_engines.py`.

Compare more than one process order and keep the zero-check PyUnitWizard case
as a drift control. An apparent improvement in that case is not a DepDigest
saving. Overlapping ranges and different model orders need cautious
interpretation; `floor` is a theoretical bound, not a statistical assertion
that its observed median must always be lowest.

For a 300-atom topology:

```bash
python benchmarks/decorator_consumer_probe.py --mode current --waters 100 --iterations 200
```

`--iterations`, `--repeats` and `--waters` must be positive. `--snapshot-root`
accepts a directory containing clean `molsysmt`, `pyunitwizard`, `argdigest` and
`smonitor` clones. It puts those source roots ahead of installed copies without
installing or editing them, and always uses this DepDigest checkout. Pin each
clone to a reviewed commit and inspect every recorded origin and worktree state
before comparing results.

The intentionally retained measurement receipt is
[`results/decorator_consumer_2026-10-03.json`](results/decorator_consumer_2026-10-03.json).
It contains local timings and source revisions, not raw workflow logs. The
decision and compatibility constraints belong to
[`devguide/pending_proposals/decorator_fast_path_and_observability_boundary.md`](../devguide/pending_proposals/decorator_fast_path_and_observability_boundary.md)
and `uibcdf/depdigest#6`.
