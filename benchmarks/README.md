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

## Entry-point discovery assessment (#31)

`entry_point_discovery.py` measures the existing standard-library metadata provider
without loading plugin implementations. It is a measurement tool, not a runtime
registration API or persistent cache. Run one fresh process per sample:

```bash
python benchmarks/entry_point_discovery.py --mode single
python benchmarks/entry_point_discovery.py --mode separate
python benchmarks/entry_point_discovery.py --mode grouped
python benchmarks/entry_point_discovery.py --mode grouped --allocations
```

`single` requests formats only; `separate` queries citations and formats afresh;
`grouped` selects both from one native snapshot. `--site` adds a normally installed
fixture target. Allocation tracing is a separate run; startup/import/build/install
are excluded from the measured interval. Filesystem cache state is uncontrolled.

The retained [receipt](results/entry_point_discovery_2026-10-13.json) uses Ackredit's
existing `benchmark_plugins.write_pack/build_packs`,
`benchmark_lifecycle.environment` and `qualification_bundle.verify_installed`
operations at `4d1a1094f165a574efcb516b83cbf89351683347`. Build 21 controlled pure
wheels across the profiles below and install each profile normally in a disposable
venv inheriting a clean developer environment. Run the original-wheel/file verifier
under each venv's own interpreter. Each mode/profile has seven fresh-process timing
and three separate allocation samples; alternate profile/mode order between samples.
Keep the original wheel/file maps and probe hash, then retain normalized receipts
before retiring the owned environments. This is metadata-only fixture evidence,
not Ackredit report timings, clean published-runtime closure or public qualification.

Linux/Python 3.14.8 medians, in microseconds:

| Packs × references per pack | Single | Separate | Grouped |
| --- | ---: | ---: | ---: |
| 0 × 1 | 5,553.40 | 7,972.93 | 5,671.53 |
| 1 × 1 | 5,696.97 | 8,111.90 | 5,811.20 |
| 10 × 1 | 6,782.86 | 10,272.89 | 7,110.99 |
| 1 × 1,000 | 5,692.86 | 8,190.62 | 5,796.22 |
| 10 × 100 | 6,887.09 | 10,034.02 | 6,927.34 |

Peak traced Python bytes span 210,119–245,251; they are not process RSS.
Ordered metadata identities match between separate/grouped modes. Guards cover
Python 3.11–3.14, custom finders, ZIP/distribution duplicates and late providers.

Decision: retain `importlib.metadata.entry_points(group=...)` for independent first
demand/reload. Native `entry_points().select(group=...)` can batch truly simultaneous
metadata demands, with no intervening registration. An old snapshot misses later
providers, including those installed by callbacks. These results do not justify a
faster single-demand cache or new DepDigest discovery engine. Consumer callbacks,
warning/conflict policy and refresh boundaries remain Ackredit-owned.
