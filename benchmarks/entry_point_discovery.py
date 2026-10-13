"""Measure fresh standard-library entry-point queries without loading plugins.

One invocation is one cold sample. Build/install and Python startup are outside
the measured interval. Allocation tracing is a separate, explicitly selected run.
Group batching applies only when both groups are requested at the same boundary;
this probe is not an application speedup or a persistent-cache implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as metadata
import json
import platform
import sys
import time
import tracemalloc
from pathlib import Path

GROUPS = ("ackredit.citations", "ackredit.formats")
MODES = ("single", "separate", "grouped")


def discover(mode):
    """Use the existing metadata provider at this call's freshness boundary."""
    if mode not in MODES:
        raise ValueError(f"Unsupported discovery mode: {mode}")
    if mode == "single":
        return {GROUPS[1]: tuple(metadata.entry_points(group=GROUPS[1]))}
    if mode == "separate":
        return {group: tuple(metadata.entry_points(group=group)) for group in GROUPS}
    snapshot = metadata.entry_points()
    return {group: tuple(snapshot.select(group=group)) for group in GROUPS}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=MODES, default="single")
    parser.add_argument("--site", type=Path, help="normally installed fixture target")
    parser.add_argument("--allocations", action="store_true")
    args = parser.parse_args(argv)
    if args.site is not None:
        if not args.site.is_dir():
            parser.error("--site must name an existing installed target")
        sys.path.insert(0, str(args.site.resolve()))
    if args.allocations:
        tracemalloc.start()
    start = time.perf_counter_ns()
    groups = discover(args.mode)
    elapsed = time.perf_counter_ns() - start
    peak = tracemalloc.get_traced_memory()[1] if args.allocations else None
    if args.allocations:
        tracemalloc.stop()
    identity = {
        group: [
            [ep.name, ep.value, ep.dist.metadata["Name"], ep.dist.version]
            for ep in entries
        ]
        for group, entries in groups.items()
    }
    # Metadata discovery must not materialize the implementation module.
    loaded = sorted(
        name for name in sys.modules if name.startswith("ackredit_bench_pack")
    )
    if loaded:
        raise AssertionError(f"Discovery imported fixture implementations: {loaded}")
    print(
        json.dumps(
            {
                "schema": "depdigest.entry-point-discovery-probe@1",
                "mode": args.mode,
                "python": platform.python_version(),
                "platform": platform.platform(),
                "measurement": "allocations" if args.allocations else "timing",
                "discovery_ns": elapsed,
                "peak_python_bytes": peak,
                "identities": identity,
                "identity_sha256": hashlib.sha256(
                    json.dumps(identity, sort_keys=True).encode()
                ).hexdigest(),
                "distribution_count": sum(1 for _ in metadata.distributions()),
                "loaded_fixture_modules": loaded,
                "scope": "fresh metadata query; no callbacks or consumer report timing",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
