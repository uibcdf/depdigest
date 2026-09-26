---
summary: Importing DepDigest eagerly imports importlib.metadata in every consumer.
issue: uibcdf/depdigest#16
status: resolved
opened: 2026-09-21
closed: 2026-09-26
severity: medium
verification: measured
area: [performance, imports]
guard: tests/test_import_cost.py::test_generated_version_path_does_not_import_metadata
normative:
blocked_by: []
supersedes: []
---

# Eager metadata import in DepDigest consumers

## What

`depdigest.__init__` imports `importlib.metadata` before checking its generated
`_version.py`. It also imports `LazyRegistry`, whose module imports the metadata
entry-point finder even when no registry is used. `uibcdf/depdigest#16` records
55–65 ms attributable to the metadata dependency tree in an Ackredit import.

## How

Read the generated version file first in an installed distribution, using
package metadata only when that file is absent. Delay entry-point discovery
imports until a registry actually chooses `entry_points` mode. Check an
installed wheel in a fresh interpreter, preserving the version and registry
contracts.

## Why

Importing DepDigest for its optional-dependency API should not pay for plugin
discovery or package metadata that the caller did not request.

## Acceptance criteria

- An installed import reports its packaged version without loading
  `importlib.metadata`.
- Entry-point discovery still works on first use.
- Source-tree fallback and existing public APIs still work.

## Resolution and verification

DepDigest now reads the generated `_version.py` first and consults package
metadata only for a source checkout without that file. `LazyRegistry` imports
the entry-point finder only when entry-point discovery is requested. Existing
entry-point tests still exercise successful loading, filtering and failure.

The durable guard starts a fresh isolated interpreter with a generated version
module and proves that importing DepDigest leaves `importlib.metadata` unloaded.
A locally built, installed wheel also reported its generated version from an
off-checkout path with `metadata_loaded False`. This wheel was a local test
artifact, not a public release. The full local suite passed 112 tests with
one environment-dependent skip.
