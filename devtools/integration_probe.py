"""Validate source integrations in a fresh process; this does not qualify releases."""

from __future__ import annotations

import argparse
import importlib
import importlib.abc
import json
import platform
import runpy
import subprocess
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ("depdigest", "smonitor", "argdigest", "pyunitwizard")


def _sources(workspace):
    roots = {name: workspace / name for name in PACKAGES}
    roots["depdigest"] = ROOT
    for name, root in roots.items():
        if not (root / name / "__init__.py").is_file():
            raise ValueError(f"Missing source package: {root / name}")
        sys.path.insert(0, str(root.resolve()))
    return roots


def _provenance(roots):
    result = {}
    for name, root in roots.items():
        facts = {"root": str(root.resolve())}
        for key, arguments in (
            ("commit", ["rev-parse", "HEAD"]),
            ("worktree", ["status", "--porcelain"]),
        ):
            completed = subprocess.run(
                ["git", "-C", str(root), *arguments],
                text=True,
                capture_output=True,
                timeout=10,
                check=True,
            )
            facts[key] = completed.stdout.strip()
        module = sys.modules.get(name)
        if module is not None:
            origin = Path(module.__file__).resolve()
            if origin.parent != (root / name).resolve():
                raise AssertionError(f"Unexpected {name} import: {origin}")
            facts["origin"] = str(origin)
        result[name] = facts
    return result


def _optional_roots(root, package):
    config = root / package / "_depdigest.py"
    if not config.is_file():
        return []
    libraries = runpy.run_path(str(config)).get("LIBRARIES", {})
    return sorted(
        {
            name.split(".")[0]
            for name, entry in libraries.items()
            if entry.get("type", "soft") == "soft"
            and entry.get("kind", "python") == "python"
        }
    )


def _imports(roots, package):
    optional = _optional_roots(roots[package], package)
    already_loaded = set(sys.modules)
    start = time.perf_counter()
    importlib.import_module(package)
    elapsed = time.perf_counter() - start
    loaded = sorted(set(sys.modules) - already_loaded)
    eager = [name for name in optional if name in sys.modules]
    if eager:
        raise AssertionError(f"{package} eagerly imported optional roots: {eager}")
    return {
        "package": package,
        "optional_roots_checked": optional,
        "eager_optional_roots": eager,
        "loaded_module_count": len(loaded),
        "import_seconds": elapsed,
        "qualification": "structural_optional_import_check; timing_has_no_budget",
    }


class _UnavailableBackend(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "unyt" or fullname.startswith("unyt."):
            raise ModuleNotFoundError(
                "Backend blocked by integration probe", name=fullname
            )
        return None


def _contracts():
    import argdigest
    import pyunitwizard as puw
    import smonitor
    from argdigest.contrib import pyunitwizard_support

    import depdigest

    smonitor.configure(enabled=True, handlers=[], level="DEBUG", event_buffer_size=400)
    manager = smonitor.get_manager()
    puw.configure.reset()
    puw.configure.load_library(["pint"])
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    bodies = []

    def accept_distance(distance, backend="pint"):
        bodies.append(backend)
        return puw.get_value(distance, to_unit="angstrom")

    # An integrator fixture uses the real consumer declaration, not a replacement
    # config. This composition is not claimed as a current PyUnitWizard call site.
    accept_distance.__module__ = "pyunitwizard"
    operation = depdigest.dep_digest("unyt", when={"backend": "unyt"})(accept_distance)
    operation = argdigest.arg_digest.map(
        distance={
            "kind": "quantity",
            "rules": [pyunitwizard_support.check(dimensionality={"[L]": 1})],
        }
    )(operation)
    quantity = puw.quantity(1.0, "nanometer", form="pint")
    value = operation(quantity)
    if abs(value - 10.0) > 1e-10 or bodies != ["pint"]:
        raise AssertionError("Quantity flow or nonmatching optional route changed")

    start = len(manager.recent_events())
    try:
        operation(puw.quantity(1.0, "picosecond", form="pint"))
    except argdigest.DigestValueError:
        pass
    else:
        raise AssertionError("Wrong dimensionality was accepted")
    dimensionality_codes = sorted(
        {
            event.get("code", "")
            for event in manager.recent_events()[start:]
            if (event.get("code") or "").startswith(("ARG-", "PUW-"))
        }
    )
    if not dimensionality_codes or bodies != ["pint"]:
        raise AssertionError("Contract failure lost its signal or reached the body")

    if any(name == "unyt" or name.startswith("unyt.") for name in sys.modules):
        raise AssertionError("Absent-backend scenario needs a fresh process")
    blocker = _UnavailableBackend()
    sys.meta_path.insert(0, blocker)
    depdigest.is_installed.cache_clear()
    start = len(manager.recent_events())
    messages = []
    try:
        for _ in range(2):
            try:
                operation(quantity, backend="unyt")
            except ImportError as error:
                message = str(error)
                if not all(
                    text in message
                    for text in (
                        "unyt",
                        "accept_distance",
                        "pip install unyt",
                        "conda install -c conda-forge unyt",
                    )
                ):
                    raise AssertionError(f"Missing actionable remediation: {message}")
                messages.append(message)
            else:
                raise AssertionError("Missing dependency was accepted")
        info = depdigest.get_info("pyunitwizard", format="dict")
        row = next(item for item in info["dependencies"] if item["library"] == "unyt")
        if row["installed"] or row["status"] != "missing":
            raise AssertionError("Introspection disagrees with the dependency guard")
        if info != json.loads(depdigest.get_info("pyunitwizard", format="json")):
            raise AssertionError("JSON and dict introspection disagree")
        missing = [
            event
            for event in manager.recent_events()[start:]
            if (event.get("code") or "").startswith("DEP-")
        ]
        if (
            len(missing) != 2
            or any(event["code"] != "DEP-ERR-MISS-001" for event in missing)
            or bodies != ["pint"]
        ):
            raise AssertionError("Missing calls lost diagnostics or reached the body")
        for event in missing:
            extra = event.get("extra", {})
            if (
                extra.get("library") != "unyt"
                or extra.get("caller") != "accept_distance"
                or "pip install unyt" not in extra.get("install_hint", "")
                or "conda install -c conda-forge unyt"
                not in extra.get("install_hint", "")
                or not event.get("context", {}).get("chain")
                or not event.get("message")
            ):
                raise AssertionError(f"Missing structured consumer diagnostic: {event}")
    finally:
        sys.meta_path.remove(blocker)
        depdigest.is_installed.cache_clear()
    return {
        "quantity_angstrom": value,
        "dimensionality_codes": dimensionality_codes,
        "missing_codes": [event["code"] for event in missing],
        "missing_contexts": [event.get("context", {}) for event in missing],
        "missing_messages": messages,
        "dependency_row": row,
        "body_calls": bodies,
        "qualification": "integrator_composition_and_real_quantity_flow; simulated_absence",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT.parent)
    parser.add_argument("--case", choices=("contracts", "imports"), default="contracts")
    parser.add_argument("--package", choices=PACKAGES)
    parser.add_argument(
        "--output", type=Path, help="write the JSON receipt to this file"
    )
    args = parser.parse_args(argv)
    if args.case == "imports" and args.package is None:
        parser.error("--case imports requires --package")
    try:
        # Keep the receipt machine-readable even when consumer diagnostics print.
        with redirect_stdout(sys.stderr):
            roots = _sources(args.workspace.resolve())
            result = (
                _imports(roots, args.package)
                if args.case == "imports"
                else _contracts()
            )
            receipt = {
                "schema": "depdigest.integration_probe@1",
                "case": args.case,
                "python": sys.version,
                "platform": platform.platform(),
                "sources": _provenance(roots),
                "result": result,
            }
    except (AssertionError, ValueError) as error:
        parser.exit(1, f"Integration probe failed: {error}\n")
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
