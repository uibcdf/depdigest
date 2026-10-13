"""Bounded subprocess probe of the installed declared-registry reader contract."""

from __future__ import annotations

import importlib
import sys
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event
from types import SimpleNamespace
from unittest.mock import patch

from depdigest import DeclaredRegistry


class _ContentionProbe:
    """Observe an actual competing acquisition without scheduling sleeps."""

    def __init__(self, lock, observed):
        self.lock, self.observed = lock, observed

    def __enter__(self):
        if not self.lock.acquire(blocking=False):
            self.observed.set()
            self.lock.acquire()
        return self

    def __exit__(self, *_args):
        self.lock.release()


def _verify_case(root: Path, policy: str, mode: str, fail: bool) -> None:
    host = "depdigest_installed_concurrent_" + uuid.uuid4().hex
    directory = root / host
    directory.mkdir()
    (directory / "__init__.py").write_text("", encoding="utf-8")
    (directory / "control.py").write_text(
        "from threading import Event\nentered = Event()\nrelease = Event()\n"
        f"initializations = 0\nfail = {fail!r}\nregistry = None\n",
        encoding="utf-8",
    )
    for name, content in {
        "target": (
            f"from {host} import control\ncontrol.initializations += 1\n"
            "control.entered.set()\n"
            "if not control.release.wait(10):\n    raise TimeoutError('probe release')\n"
            "if control.fail:\n    raise RuntimeError('probe failure')\n"
            "form_name = 'Target'\n"
        ),
        "recursive": (
            f"from {host} import control\ncontrol.registry['Recursive']\n"
            "form_name = 'Recursive'\n"
        ),
        "sentinel": (
            "from pathlib import Path\n"
            f"Path({str(root / 'sentinel-imported')!r}).touch()\n"
            "raise AssertionError('unrelated plugin imported')\n"
        ),
    }.items():
        plugin = directory / name
        plugin.mkdir()
        (plugin / "__init__.py").write_text(content, encoding="utf-8")
    control = importlib.import_module(host + ".control")
    declarations = {
        "Target": "target",
        "Recursive": "recursive",
        "Sentinel": "sentinel",
    }
    points = [
        SimpleNamespace(
            name=name,
            value=f"{host}.{name}",
            load=lambda name=name: importlib.import_module(f"{host}.{name}"),
        )
        for name in declarations.values()
    ]
    options = {"load_policy": policy}
    if mode == "entry_points":
        options.update(discovery_mode=mode, entrypoint_group=host)
    with patch("depdigest.core.loader.entry_points", return_value={host: points}):
        registry = DeclaredRegistry(host, directory, declarations, **options)
        observed, finished = Event(), Event()
        registry._access_lock = _ContentionProbe(registry._access_lock, observed)

        def second():
            try:
                return registry["Target"]
            finally:
                finished.set()
                observed.set()

        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(lambda: registry["Target"])
            try:
                if not control.entered.wait(5):
                    raise ValueError("installed first initialization did not start")
                other = pool.submit(second)
                if not observed.wait(5) or finished.is_set():
                    raise ValueError("installed overlapping request did not wait")
            finally:
                control.release.set()
        if fail:
            causes = []
            for future in (first, other):
                try:
                    future.result(timeout=5)
                except KeyError as error:
                    causes.append(error.__cause__)
                else:
                    raise ValueError("installed initialization failure was suppressed")
            if not isinstance(causes[0], RuntimeError) or causes[0] is not causes[1]:
                raise ValueError("installed waiters did not share the failure cause")
            control.fail = False
            try:
                registry["Target"]
            except KeyError as error:
                if error.__cause__ is not causes[0]:
                    raise ValueError("installed cached cause changed") from error
            else:
                raise ValueError("installed failure retried implicitly")
            module = registry.retry("Target")
            expected_initializations = 2
        else:
            module = first.result(timeout=5)
            if other.result(timeout=5) is not module:
                raise ValueError("installed waiters received different values")
            expected_initializations = 1
        if (
            control.initializations != expected_initializations
            or registry["Target"] is not module
        ):
            raise ValueError("installed initialization/cache mismatch")
        control.registry = registry
        try:
            registry["Recursive"]
        except KeyError as error:
            if not isinstance(error.__cause__, KeyError) or "Recursive load" not in str(
                error.__cause__
            ):
                raise ValueError("installed recursive cause mismatch") from error
        else:
            raise ValueError("installed recursive load succeeded")
        if (root / "sentinel-imported").exists():
            raise ValueError("installed reader touched an unrelated plugin")


def verify_concurrent_registry() -> None:
    """Exercise both policies/routes, shared values/causes, retry and recursion.

    The calling verifier must bound the whole process so a regressed plain Lock
    cannot leave its installed qualification worker blocked indefinitely.
    """
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        sys.path.insert(0, str(root))
        try:
            for policy in ("strict", "adapter"):
                for mode in ("filesystem", "entry_points"):
                    for fail in (False, True):
                        _verify_case(root, policy, mode, fail)
        finally:
            sys.path.remove(str(root))
            for name in tuple(sys.modules):
                if name.startswith("depdigest_installed_concurrent_"):
                    sys.modules.pop(name, None)
            importlib.invalidate_caches()


if __name__ == "__main__":
    verify_concurrent_registry()
    print("installed concurrent registry contract verified")
