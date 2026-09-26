---
summary: Missing-dependency hints ignore consumer documentation and disagree on installation order.
issue: uibcdf/depdigest#17
status: resolved
opened: 2026-09-24
closed: 2026-09-26
severity: medium
verification: inspected
area: [diagnostics, dependencies]
guard: tests/test_core.py::test_consumer_dependency_hint_is_shared_by_event_and_exception
normative:
blocked_by: []
supersedes: []
---

# Missing-dependency hints ignore consumer documentation

## What

For a missing optional dependency, the SMonitor event points at DepDigest's
documentation and lists pip before Conda. The exception also points at
DepDigest, but lists Conda first. The consumer cannot supply its own
documentation URL through `_depdigest.py` or `DepConfig`. The original consumer
evidence is in `uibcdf/depdigest#17` and `uibcdf/sabueso#46`.

## How

Add a consumer documentation URL to the package configuration. Construct the
installation and documentation hint once, then send it to both the diagnostic
and exception. Use the configured Conda package and optional channel first;
include a pip command only when a PyPI package name is declared. Keep the
existing DepDigest URL as the fallback for consumers without one.

## Why

The person missing a dependency needs the consumer's instructions. Conflicting
commands and a library-internal documentation link make the two messages harder
to act on, especially when Conda is the consumer's supported installation path.

## Acceptance criteria

- File-based and registered configurations can supply a documentation URL.
- The SMonitor event and exception carry the same ordered installation hint.
- Conda package and channel values are honored; pip appears only when declared.
- Tests cover consumer values and the fallback when they are absent.

## Resolution and verification

The package config now accepts `DOC_URL`, or `DepConfig(doc_url=...)` for a
registered package. The decorator forwards each dependency's Conda name and
optional channel, its declared PyPI name, and the consumer documentation URL.
The checker constructs one Conda-first hint and supplies the same text to the
SMonitor catalog event and raised exception. When no PyPI name is declared,
the hint omits pip; when no consumer URL is supplied, it links to DepDigest.

`tests/test_core.py::test_consumer_dependency_hint_is_shared_by_event_and_exception`
is the durable guard: it compares the event payload with the exception text
and checks channel, ordering, and the consumer URL. Adjacent tests cover the
fallback and both configuration sources. The full local suite passed 111 tests
with one environment-dependent skip after refreshing generated indexes.
