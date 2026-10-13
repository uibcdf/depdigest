"""Control overlapping registry requests without scheduling sleeps or deadlocks."""

import importlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Event, RLock
from types import SimpleNamespace

import pytest

import depdigest
from depdigest import DeclaredRegistry, DepConfig, temporary_package_config


@pytest.fixture
def host(tmp_path, monkeypatch):
    root = tmp_path / "concurrent_registry_host"
    directory = root / "plugins"
    directory.mkdir(parents=True)
    (root / "__init__.py").write_text("")
    (directory / "__init__.py").write_text("")
    (root / "control.py").write_text(
        "from threading import Event\n"
        "entered = Event()\nrelease = Event()\n"
        "initializations = 0\nfail = False\nregistry = None\n"
    )
    plugin = directory / "observed"
    plugin.mkdir()
    (plugin / "__init__.py").write_text(
        "from concurrent_registry_host import control\n"
        "control.initializations += 1\ncontrol.entered.set()\n"
        "if not control.release.wait(10):\n"
        "    raise TimeoutError('test release missing')\n"
        "if control.fail:\n    raise RuntimeError('adapter initialization failed')\n"
        "form_name = 'Observed'\n"
    )
    sentinel = directory / "sentinel"
    sentinel.mkdir()
    marker = root / "sentinel-imported"
    (sentinel / "__init__.py").write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).touch()\n"
        "raise AssertionError('unrelated plugin imported')\n"
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    control = importlib.import_module("concurrent_registry_host.control")
    try:
        with temporary_package_config("concurrent_registry_host", DepConfig()):
            yield SimpleNamespace(directory=directory, control=control, marker=marker)
    finally:
        control.release.set()
        for name in tuple(sys.modules):
            if name == "concurrent_registry_host" or name.startswith(
                "concurrent_registry_host."
            ):
                sys.modules.pop(name)


class _ObservedLock:
    """Observe real contention, preserving the owner's chosen reentrant lock."""

    def __init__(self, lock, observed):
        self.lock = lock
        self.observed = observed

    def __enter__(self):
        if not self.lock.acquire(blocking=False):
            self.observed.set()
            self.lock.acquire()
        return self

    def __exit__(self, *_args):
        self.lock.release()


def _registry(host, monkeypatch, policy, mode):
    options = dict(load_policy=policy)
    if mode == "entry_points":
        points = [
            SimpleNamespace(
                name=name,
                value=f"concurrent_registry_host.plugins.{name}",
                load=lambda name=name: importlib.import_module(
                    f"concurrent_registry_host.plugins.{name}"
                ),
            )
            for name in ("observed", "sentinel")
        ]
        monkeypatch.setattr(
            "depdigest.core.loader.entry_points", lambda: {"concurrent.plugins": points}
        )
        options.update(discovery_mode=mode, entrypoint_group="concurrent.plugins")
    return DeclaredRegistry(
        "concurrent_registry_host.plugins",
        host.directory,
        {"Observed": "observed", "Sentinel": "sentinel"},
        **options,
    )


def _overlap(entries, control):
    observed, finished = Event(), Event()
    # Before the fix this attribute is unused: the second call completes with the
    # real false-recursion error. Afterward it signals actual lock contention,
    # rather than relying on a thread-start event plus a scheduling sleep.
    entries._access_lock = _ObservedLock(
        getattr(entries, "_access_lock", RLock()), observed
    )

    def second():
        try:
            return entries["Observed"]
        finally:
            finished.set()
            observed.set()

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(lambda: entries["Observed"])
        try:
            assert control.entered.wait(5), "first initialization never started"
            other = pool.submit(second)
            assert observed.wait(5), "second request neither waited nor completed"
            if finished.is_set():
                other.result(timeout=5)  # Surface the original false-recursion cause.
            assert not finished.is_set(), "request returned during initialization"
        finally:
            control.release.set()
    return first, other


@pytest.mark.parametrize("policy", ["strict", "adapter"])
@pytest.mark.parametrize("mode", ["filesystem", "entry_points"])
def test_overlapping_requests_share_one_initialization(host, monkeypatch, policy, mode):
    events = []
    monkeypatch.setattr(
        "smonitor.integrations.emit_from_catalog",
        lambda signal, **kw: events.append((signal["code"], kw["extra"])),
    )
    entries = _registry(host, monkeypatch, policy, mode)
    first, other = _overlap(entries, host.control)
    module = first.result(timeout=5)
    assert other.result(timeout=5) is module
    assert module.form_name == "Observed" and host.control.initializations == 1
    assert entries.loaded_keys() == ("Observed",)
    assert not host.marker.exists()
    loads = [extra for code, extra in events if code == "DEP-DBG-LOAD-002"]
    assert len(loads) == 1
    assert loads[0]["plugin"] == "observed" and loads[0]["trigger"] == "Observed"
    assert loads[0]["caller"].startswith(__file__ + ":")
    restricted = DepConfig(
        libraries={
            "missing": {
                "type": "soft",
                "kind": "executable",
                "executable": str(host.marker),
            }
        },
        mapping={"observed": "missing"},
        show_all_capabilities=False,
    )
    with temporary_package_config("concurrent_registry_host", restricted):
        assert "Observed" not in entries
        with pytest.raises(KeyError):
            entries["Observed"]
    assert entries["Observed"] is module


@pytest.mark.parametrize("policy", ["strict", "adapter"])
@pytest.mark.parametrize("mode", ["filesystem", "entry_points"])
def test_overlapping_failures_keep_one_cause_until_explicit_retry(
    host, monkeypatch, policy, mode
):
    host.control.fail = True
    events = []
    monkeypatch.setattr(
        "smonitor.integrations.emit_from_catalog",
        lambda signal, **kw: events.append((signal["code"], kw["extra"])),
    )
    entries = _registry(host, monkeypatch, policy, mode)
    futures = _overlap(entries, host.control)
    causes = []
    for future in futures:
        with pytest.raises(KeyError) as caught:
            future.result(timeout=5)
        causes.append(caught.value.__cause__)
    assert isinstance(causes[0], RuntimeError)
    assert causes[0] is causes[1]
    assert str(causes[0]) == "adapter initialization failed"
    assert host.control.initializations == 1 and entries.loaded_keys() == ()
    failures = [extra for code, extra in events if code == "DEP-DBG-LOAD-001"]
    assert len(failures) == 1 and failures[0]["trigger"] == "Observed"
    host.control.fail = False
    with pytest.raises(KeyError) as cached:
        entries["Observed"]
    assert cached.value.__cause__ is causes[0]
    module = entries.retry("Observed")
    assert module.form_name == "Observed" and host.control.initializations == 2
    assert entries["Observed"] is module
    assert not host.marker.exists()


@pytest.mark.parametrize("policy", ["strict", "adapter"])
def test_true_recursion_fails_in_a_bounded_process(host, policy):
    plugin = host.directory / "recursive"
    plugin.mkdir()
    (plugin / "__init__.py").write_text(
        "from concurrent_registry_host import control\n"
        "control.registry['Recursive']\nform_name = 'Recursive'\n"
    )
    script = """
import sys
sys.path[:0] = sys.argv[1:3]
from depdigest import DeclaredRegistry
from concurrent_registry_host import control
entries = DeclaredRegistry('concurrent_registry_host.plugins', sys.argv[3],
                          {'Recursive': 'recursive'}, load_policy=sys.argv[4])
control.registry = entries
try:
    entries['Recursive']
except KeyError as error:
    assert isinstance(error.__cause__, KeyError)
    assert 'Recursive load' in str(error.__cause__)
    assert entries.loaded_keys() == ()
else:
    raise AssertionError('recursive implementation admitted')
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            script,
            str(Path(depdigest.__file__).resolve().parent.parent),
            str(host.directory.parent.parent),
            str(host.directory),
            policy,
        ],
        capture_output=True,
        text=True,
        timeout=8,
    )
    assert result.returncode == 0, result.stdout + result.stderr
