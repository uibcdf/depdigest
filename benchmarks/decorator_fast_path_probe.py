"""Probe for `devguide/pending_proposals/decorator_fast_path_and_observability_boundary.md`.

The decorators below are **prototypes, not shipped code**. They exist so the
figures in that proposal can be reproduced and re-measured on any host before
the deferred 1.1.0 decision is taken. Nothing here is imported by the package.

Two questions are answered:

1. How far can the per-call `@dep_digest` overhead go? The epoch-cached
   variants are compared against the current decorator and against a bare
   `@wraps` passthrough, which is the floor for any Python wrapper.
2. Does the fast path stay correct? A missing dependency must raise on *every*
   call — a negative verdict is never cached — and bumping the epoch must force
   re-verification.

Run: ``python benchmarks/decorator_fast_path_probe.py``
"""

from __future__ import annotations

import json
from functools import wraps
from timeit import timeit

import smonitor

from depdigest import dep_digest
from depdigest.core.checker import check_dependency
from depdigest.core.config import resolve_config

PRESENT = "json"
MISSING = "depdigest_probe_no_such_module"

# Stand-in for the module-level counter that `register_package_config`,
# `unregister_package_config`, `clear_package_configs` and
# `temporary_package_config` would bump alongside `resolve_config.cache_clear()`.
_EPOCH = [0]


def bump_epoch() -> None:
    _EPOCH[0] += 1


def passthrough(func):
    """The irreducible cost of wrapping a Python function at all."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def dep_digest_list(library: str):
    """Prototype: epoch cache in a list — two subscripts per call."""

    def decorator(func):
        module_path = func.__module__
        plan = [-1, False]  # [verified_epoch, verified]
        epoch = _EPOCH

        @wraps(func)
        def wrapper(*args, **kwargs):
            if plan[0] == epoch[0] and plan[1]:
                return func(*args, **kwargs)
            cfg = resolve_config(module_path)
            lib_info = cfg.libraries.get(library, {})
            check_dependency(
                library,
                pypi_name=lib_info.get("pypi"),
                caller=func.__name__,
                exception_class=cfg.exception_class,
            )
            plan[0] = epoch[0]
            plan[1] = True
            return func(*args, **kwargs)

        return wrapper

    return decorator


def dep_digest_cell(library: str):
    """Prototype: epoch cache in a closure cell.

    ``verified_epoch`` is only ever assigned the epoch at which the check
    passed, so one equality test replaces the ``(epoch, verified)`` pair.
    """

    def decorator(func):
        module_path = func.__module__
        verified_epoch = -1
        epoch = _EPOCH

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal verified_epoch
            if verified_epoch == epoch[0]:
                return func(*args, **kwargs)
            cfg = resolve_config(module_path)
            lib_info = cfg.libraries.get(library, {})
            check_dependency(
                library,
                pypi_name=lib_info.get("pypi"),
                caller=func.__name__,
                exception_class=cfg.exception_class,
            )
            verified_epoch = epoch[0]
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _check_correctness() -> None:
    """The two properties the proposal claims. Loud failure if either breaks."""

    def plain(value: int) -> int:
        return value + 1

    for name, factory in (("list", dep_digest_list), ("cell", dep_digest_cell)):
        guarded = factory(MISSING)(plain)
        for attempt in range(3):
            try:
                guarded(1)
            except ImportError:
                continue
            raise AssertionError(
                f"{name}: a missing dependency stopped raising on call {attempt}; "
                "a negative verdict must never be cached"
            )

        cached = factory(PRESENT)(plain)
        assert cached(1) == 2
        bump_epoch()
        assert cached(1) == 2, f"{name}: re-verification after an epoch bump failed"


def main(number: int = 300_000) -> None:
    def plain(value: int) -> int:
        return value + 1

    current = dep_digest(PRESENT)(plain)
    floor = passthrough(plain)
    fast_list = dep_digest_list(PRESENT)(plain)
    fast_cell = dep_digest_cell(PRESENT)(plain)

    # Match `decorator_overhead.py`: telemetry off, so the figures are about the
    # decorator itself and stay comparable between the two benchmarks.
    smonitor.configure(enabled=False, handlers=[])

    _check_correctness()

    def ns(fn) -> float:
        return timeit(fn, number=number) / number * 1e9

    bare_ns = ns(lambda: plain(1))
    floor_ns = ns(lambda: floor(1))
    current_ns = ns(lambda: current(1))
    list_ns = ns(lambda: fast_list(1))
    cell_ns = ns(lambda: fast_cell(1))

    print(
        json.dumps(
            {
                "calls": number,
                "bare_ns": bare_ns,
                "passthrough_ns": floor_ns,
                "current_ns": current_ns,
                "fast_list_ns": list_ns,
                "fast_cell_ns": cell_ns,
                "overhead_floor_ns": floor_ns - bare_ns,
                "overhead_current_ns": current_ns - bare_ns,
                "overhead_fast_cell_ns": cell_ns - bare_ns,
                "reachable_saving_ns": current_ns - cell_ns,
                "depdigest_work_above_floor_ns": cell_ns - floor_ns,
            }
        )
    )


if __name__ == "__main__":
    main()
