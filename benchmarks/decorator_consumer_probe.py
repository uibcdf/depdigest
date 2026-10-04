"""Time complete warm consumer calls against two explicitly unqualified models.

Run each mode in a fresh process. ``epoch`` assumes fixed configuration;
``floor`` removes guards and is only an optimistic bound. Neither is a product
implementation. Optional consumers are imported only when the probe runs.
"""

from __future__ import annotations

import argparse
import importlib
import json
import platform
import statistics
import subprocess
import sys
import timeit
from functools import wraps
from pathlib import Path

MODES = ("current", "epoch", "floor")
SNAPSHOT_PACKAGES = ("smonitor", "argdigest", "pyunitwizard", "molsysmt")


def _install_model(mode):
    import depdigest
    from depdigest.core import decorator
    from depdigest.core.config import resolve_config

    original = decorator.dep_digest
    if mode == "current":
        return

    def factory(library, when=None):
        def decorate(function):
            guarded = original(library, when)(function)
            if mode == "floor":
                # Keep the original dependency metadata, remove only its frame.
                return guarded.__wrapped__
            if when is not None:
                return guarded
            verified_epoch = -1
            epoch = 0  # Fixed process-local experiment; no invalidation contract.

            @wraps(guarded)
            def wrapper(*args, **kwargs):
                nonlocal verified_epoch
                if verified_epoch == epoch:
                    return function(*args, **kwargs)
                result = guarded(*args, **kwargs)
                config = resolve_config(function.__module__)
                if config.libraries.get(library, {}).get("kind", "python") == "python":
                    verified_epoch = epoch
                return result

            return wrapper

        return decorate

    depdigest.dep_digest = decorator.dep_digest = factory


def _cases(waters):
    import molsysmt as msm
    import pyunitwizard as puw
    from molsysmt.form.openmm_Topology.extract import extract
    from openmm.app import Topology, element

    topology = Topology()
    chain = topology.addChain()
    for _ in range(waters):
        residue = topology.addResidue("HOH", chain)
        oxygen = topology.addAtom("O", element.oxygen, residue)
        for name in ("H1", "H2"):
            topology.addBond(oxygen, topology.addAtom(name, element.hydrogen, residue))
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    quantity = puw.quantity(1.0, "nanometer")

    cases = {
        "molsysmt_adapter_reuse": lambda: extract(topology, copy_if_all=False),
        "molsysmt_adapter_copy": lambda: extract(topology),
        "molsysmt_public_reuse": lambda: msm.extract(topology, copy_if_all=False),
        "molsysmt_public_copy": lambda: msm.extract(topology),
        "pyunitwizard_get_value": lambda: puw.get_value(quantity, to_unit="angstrom"),
    }
    for name, call in cases.items():
        result = call()
        if name.endswith("reuse"):
            if result is not topology:
                raise AssertionError(f"{name}: input identity changed")
        elif name.endswith("copy"):
            if (
                result is topology
                or result.getNumAtoms() != 3 * waters
                or result.getNumBonds() != 2 * waters
            ):
                raise AssertionError(f"{name}: topology copy changed")
        elif abs(result - 10.0) > 1e-10:
            raise AssertionError(f"{name}: unit conversion changed")
    return cases


def _checks(call):
    from depdigest.core import decorator

    checked = []
    original = decorator.check_dependency

    def counted(*args, **kwargs):
        checked.append(args[0])
        return original(*args, **kwargs)

    decorator.check_dependency = counted
    try:
        call()
    finally:
        decorator.check_dependency = original
    return checked


def _source(name):
    module = importlib.import_module(name)
    origin = Path(module.__file__).resolve()
    root = origin.parent.parent
    result = {"origin": str(origin)}
    for key, arguments in (
        ("commit", ("rev-parse", "HEAD")),
        ("worktree", ("status", "--porcelain")),
    ):
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        result[key] = completed.stdout.strip() if completed.returncode == 0 else None
    return result


def _positive_integer(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=MODES, default="current")
    parser.add_argument("--iterations", type=_positive_integer, default=2000)
    parser.add_argument("--repeats", type=_positive_integer, default=7)
    parser.add_argument("--waters", type=_positive_integer, default=1)
    parser.add_argument(
        "--snapshot-root",
        type=Path,
        help="directory containing clean smonitor/argdigest/pyunitwizard/molsysmt clones",
    )
    args = parser.parse_args(argv)
    if args.snapshot_root is not None:
        for package in SNAPSHOT_PACKAGES:
            root = args.snapshot_root / package
            if not (root / package / "__init__.py").is_file():
                parser.error(f"missing snapshot package: {root}")
            sys.path.insert(0, str(root.resolve()))
    # A directly invoked benchmark must use this DepDigest checkout.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import smonitor

    _install_model(args.mode)
    smonitor.configure(enabled=False, handlers=[])
    cases = _cases(args.waters)
    output = {
        "schema": "depdigest.decorator_consumer_probe@1",
        "mode": args.mode,
        "qualification": "timing_only; fixed_configuration; models_not_shipped",
        "python": sys.version,
        "platform": platform.platform(),
        "iterations": args.iterations,
        "repeats": args.repeats,
        "water_residues": args.waters,
        "sources": {name: _source(name) for name in ("depdigest", *SNAPSHOT_PACKAGES)},
        "results": {},
    }
    for telemetry in (False, True):
        smonitor.configure(enabled=telemetry, handlers=[])
        measured = {}
        for name, call in cases.items():
            for _ in range(25):
                call()
            checks = _checks(call)
            samples = [
                elapsed / args.iterations * 1e6
                for elapsed in timeit.repeat(
                    call, number=args.iterations, repeat=args.repeats
                )
            ]
            measured[name] = {
                "median_us": statistics.median(samples),
                "min_us": min(samples),
                "max_us": max(samples),
                "samples_us": samples,
                "checked_libraries": checks,
            }
        output["results"]["telemetry_on" if telemetry else "telemetry_off"] = measured
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
