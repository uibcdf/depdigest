"""Compatibility boundaries an optimization of successful checks must preserve."""

from importlib.machinery import ModuleSpec

import pytest

from depdigest import DepConfig, dep_digest, is_installed, temporary_package_config
from depdigest.core import checker

PACKAGE = __name__.split(".")[0]


@pytest.fixture(autouse=True)
def isolate_availability(monkeypatch):
    is_installed.cache_clear()
    events = []
    monkeypatch.setattr(
        "smonitor.integrations.emit_from_catalog",
        lambda entry, **kwargs: events.append((entry, kwargs["extra"])),
    )
    yield events
    is_installed.cache_clear()


def test_warm_decorator_observes_in_place_dependency_kind_change(monkeypatch):
    config = DepConfig(libraries={"json": {"kind": "python"}})
    calls = []

    @dep_digest("json")
    def operation():
        calls.append(True)
        return "completed"

    with temporary_package_config(PACKAGE, config):
        assert operation() == "completed"
        config.libraries["json"].update(
            kind="executable", executable="changed-command", pypi=None, conda=None
        )
        monkeypatch.setattr(checker.shutil, "which", lambda command: None)
        with pytest.raises(ImportError, match="executable"):
            operation()

    assert calls == [True]


def test_warm_decorator_honors_explicit_python_probe_cache_clear(monkeypatch):
    available = True
    monkeypatch.setattr(
        checker,
        "find_spec",
        lambda name: ModuleSpec(name, loader=None) if available else None,
    )

    @dep_digest("cache_contract_python")
    def operation():
        return "completed"

    with temporary_package_config(PACKAGE, DepConfig()):
        assert operation() == "completed"
        available = False
        # The existing Python discovery cache remains deliberately sticky.
        assert operation() == "completed"
        is_installed.cache_clear()
        with pytest.raises(ImportError, match="cache_contract_python"):
            operation()


def test_warm_executable_decorator_rechecks_availability(monkeypatch):
    available = True
    probes = []

    def which(command):
        probes.append(command)
        return command if available else None

    monkeypatch.setattr(checker.shutil, "which", which)
    config = DepConfig(
        libraries={"engine": {"kind": "executable", "executable": "engine-command"}}
    )

    @dep_digest("engine")
    def operation():
        return "completed"

    with temporary_package_config(PACKAGE, config):
        assert operation() == "completed"
        available = False
        with pytest.raises(ImportError, match="executable"):
            operation()

    assert probes == ["engine-command", "engine-command"]


def test_conditions_are_evaluated_on_each_successful_call():
    comparisons = []

    class Selection:
        def __eq__(self, expected):
            comparisons.append(expected)
            return True

    @dep_digest("json", when={"backend": "external"})
    def operation(backend):
        return "completed"

    with temporary_package_config(PACKAGE, DepConfig()):
        selection = Selection()
        assert operation(selection) == "completed"
        assert operation(selection) == "completed"

    assert comparisons == ["external", "external"]


def test_nonmatching_condition_never_probes_the_dependency(monkeypatch):
    def unexpected_probe(*args, **kwargs):
        raise AssertionError("A local route must not probe the optional engine")

    monkeypatch.setattr(checker, "find_spec", unexpected_probe)

    @dep_digest("cache_contract_absent", when={"backend": "external"})
    def operation(backend="local"):
        return "completed"

    with temporary_package_config(PACKAGE, DepConfig()):
        assert operation() == "completed"
        assert operation() == "completed"


def test_every_missing_call_retains_the_consumer_diagnostic(
    monkeypatch, isolate_availability
):
    monkeypatch.setattr(checker, "find_spec", lambda name: None)
    config = DepConfig(
        libraries={"cache_contract_absent": {"pypi": None, "conda": None}},
        doc_url="https://consumer.example/dependencies",
    )

    @dep_digest("cache_contract_absent")
    def operation():
        raise AssertionError("An absent engine must prevent execution")

    with temporary_package_config(PACKAGE, config):
        for _ in range(2):
            with pytest.raises(ImportError) as caught:
                operation()
            assert "https://consumer.example/dependencies" in str(caught.value)
            assert "pip install" not in str(caught.value)
            assert "conda install" not in str(caught.value)

    assert len(isolate_availability) == 2
    for entry, extra in isolate_availability:
        assert entry["code"]
        assert extra["caller"] == "operation"
        assert extra["library"] == "cache_contract_absent"
        assert extra["doc_url"] == config.doc_url
