"""Provider contracts for selective discovery, loading and registry mutation."""

import sys
from types import SimpleNamespace

import pytest

from depdigest import DeclaredRegistry, DepConfig, temporary_package_config


@pytest.fixture
def plugins(tmp_path, monkeypatch):
    root = tmp_path / "declared_host"
    directory = root / "plugins"
    directory.mkdir(parents=True)
    (root / "__init__.py").write_text("")
    (directory / "__init__.py").write_text("")
    monkeypatch.syspath_prepend(str(tmp_path))
    with temporary_package_config("declared_host", DepConfig()):
        yield directory
    for name in tuple(sys.modules):
        if name == "declared_host" or name.startswith("declared_host."):
            sys.modules.pop(name)


def write_plugin(directory, name, source):
    path = directory / name
    path.mkdir()
    (path / "__init__.py").write_text(source)


def registry(directory, declarations):
    return DeclaredRegistry("declared_host.plugins", directory, declarations)


def test_metadata_and_requested_load_leave_unrelated_sentinel_unimported(plugins):
    write_plugin(plugins, "target", "form_name = 'Target'\n")
    write_plugin(plugins, "sentinel", "raise AssertionError('unrelated import')\n")
    entries = registry(plugins, {"Target": "target", "Sentinel": "sentinel"})
    assert list(entries) == list(entries.keys()) == ["Target", "Sentinel"]
    assert len(entries) == 2
    assert "Target" in entries and "Unknown" not in entries
    assert entries.declared_keys() == ("Target", "Sentinel")
    assert entries.loaded_keys() == ()
    assert "declared_host.plugins.target" not in sys.modules
    assert entries["Target"].form_name == "Target"
    assert entries["Target"] is sys.modules["declared_host.plugins.target"]
    assert entries.loaded_keys() == ("Target",)
    assert "declared_host.plugins.sentinel" not in sys.modules


def test_value_views_materialize_and_failures_do_not_change_declarations(plugins):
    write_plugin(plugins, "good", "form_name = 'Good'\n")
    write_plugin(plugins, "bad", "raise RuntimeError('broken')\n")
    entries = registry(plugins, {"Good": "good", "Bad": "bad"})
    values = iter(entries.values())
    assert next(values).form_name == "Good"
    with pytest.raises(KeyError) as caught:
        next(values)
    assert isinstance(caught.value.__cause__, RuntimeError)
    assert list(entries.keys()) == ["Good", "Bad"]
    assert entries.get("Bad", "default") == "default"
    assert entries.loaded_keys() == ("Good",)
    items = iter(entries.items())
    assert next(items)[0] == "Good"
    with pytest.raises(KeyError):
        next(items)


@pytest.mark.parametrize("show_all", [True, False])
@pytest.mark.parametrize("kind", ["python", "executable"])
def test_visibility_and_missing_dependency_diagnostics(
    plugins, monkeypatch, show_all, kind
):
    write_plugin(plugins, "optional", "raise AssertionError('must gate import')\n")
    cfg = DepConfig(
        libraries={"absent_engine": {"type": "soft", "kind": kind}},
        mapping={"optional": "absent_engine"},
        show_all_capabilities=show_all,
    )
    events = []
    monkeypatch.setattr(
        "smonitor.integrations.emit_from_catalog",
        lambda signal, **kw: events.append((signal, kw)),
    )
    monkeypatch.setattr("depdigest.core.checker.is_installed", lambda name: False)
    monkeypatch.setattr("depdigest.core.checker.shutil.which", lambda name: None)
    with temporary_package_config("declared_host", cfg):
        entries = registry(plugins, {"Optional": "optional"})
        assert list(entries) == (["Optional"] if show_all else [])
        with pytest.raises(KeyError):
            entries["Optional"]
        assert entries.loaded_keys() == ()
    assert "declared_host.plugins.optional" not in sys.modules
    codes = [signal["code"] for signal, _ in events]
    assert ("DEP-ERR-MISS-001" in codes) is show_all


def test_config_overrides_apply_to_existing_loaded_registry(plugins, monkeypatch):
    write_plugin(plugins, "target", "form_name = 'Target'\n")
    entries = registry(plugins, {"Target": "target"})
    loaded = entries["Target"]
    restricted = DepConfig(
        libraries={"absent": {"type": "soft"}},
        mapping={"target": "absent"},
        show_all_capabilities=False,
    )
    monkeypatch.setattr("depdigest.core.checker.is_installed", lambda name: False)
    with temporary_package_config("declared_host", restricted):
        assert list(entries) == []
        with pytest.raises(KeyError):
            entries["Target"]
        assert sys.modules["declared_host.plugins.target"] is loaded
    assert entries["Target"] is loaded


def test_failure_is_cached_until_explicit_retry(plugins, monkeypatch):
    write_plugin(plugins, "target", "form_name = 'Target'\n")
    attempts = []

    def load(name):
        attempts.append(name)
        if len(attempts) == 1:
            raise RuntimeError("temporarily broken")
        return SimpleNamespace(form_name="Target")

    monkeypatch.setattr("depdigest.core.registry.import_module", load)
    entries = registry(plugins, {"Target": "target"})
    for _ in range(2):
        with pytest.raises(KeyError):
            entries["Target"]
    assert len(attempts) == 1
    assert entries.retry("Target").form_name == "Target"
    entries.refresh()
    assert entries["Target"].form_name == "Target"
    assert len(attempts) == 2


@pytest.mark.parametrize("source", ["form_name = 'Other'", "pass"])
def test_mismatched_or_missing_identity_is_not_admitted(plugins, source):
    write_plugin(plugins, "target", source)
    entries = registry(plugins, {"Target": "target"})
    with pytest.raises(KeyError) as caught:
        entries["Target"]
    assert isinstance(caught.value.__cause__, ValueError)
    assert entries.loaded_keys() == ()
    assert entries.declared_keys() == ("Target",)


def test_missing_plugin_remains_declared(plugins):
    entries = registry(plugins, {"Absent": "absent"})
    assert "Absent" in entries
    with pytest.raises(KeyError) as caught:
        entries["Absent"]
    assert isinstance(caught.value.__cause__, LookupError)


def test_dynamic_overrides_and_delete_clear_do_not_load(plugins):
    write_plugin(plugins, "sentinel", "raise AssertionError('unrelated import')")
    entries = registry(plugins, {"Sentinel": "sentinel"})
    override = object()
    entries["Sentinel"] = override
    entries.update({"Dynamic": override})
    assert list(entries) == ["Sentinel", "Dynamic"]
    assert dict(entries.items()) == {"Sentinel": override, "Dynamic": override}
    assert entries.loaded_keys() == ("Sentinel", "Dynamic")
    del entries["Sentinel"]
    assert "Sentinel" not in entries
    entries.clear()
    assert len(entries) == 0
    assert "declared_host.plugins.sentinel" not in sys.modules


@pytest.mark.parametrize(
    "declarations",
    [
        [("A", "a"), ("A", "b")],
        [("A", "a"), ("B", "a")],
        {"": "a"},
        {"A": "../escape"},
        {"A": "a.b"},
    ],
)
def test_invalid_or_duplicate_declarations_rejected(plugins, declarations):
    with pytest.raises(ValueError):
        registry(plugins, declarations)


def test_undeclared_fallback_is_explicit_ordered_and_preserves_overrides(plugins):
    write_plugin(plugins, "declared", "form_name = 'Declared'")
    write_plugin(plugins, "b_duplicate", "form_name = 'Dynamic'")
    write_plugin(plugins, "a_new", "form_name = 'New'")
    entries = registry(plugins, {"Declared": "declared"})
    override = object()
    entries["Dynamic"] = override
    assert list(entries) == ["Declared", "Dynamic"]
    assert entries.discover() == ("Declared", "New")
    assert entries["Dynamic"] is override
    assert entries.loaded_keys() == ("New", "Dynamic")
    assert "declared_host.plugins.declared" not in sys.modules
    assert entries["Declared"].form_name == "Declared"


class EntryPoint:
    def __init__(self, name, identity=None):
        self.name = name
        self.value = f"implementation:{name}"
        self.calls = 0
        self.identity = identity

    def load(self):
        self.calls += 1
        if self.name == "sentinel":
            raise AssertionError("unrelated entry point")
        return SimpleNamespace(form_name=self.identity) if self.identity else object()


@pytest.mark.parametrize("modern", [True, False])
def test_entrypoints_selective_load_and_explicit_metadata_refresh(
    plugins, monkeypatch, modern
):
    target = EntryPoint("target", "Target")
    sentinel = EntryPoint("sentinel", "Sentinel")
    current = [target, sentinel]

    class Collection:
        def select(self, *, group):
            assert group == "host.plugins"
            return current

    monkeypatch.setattr(
        "depdigest.core.loader.entry_points",
        lambda: Collection() if modern else {"host.plugins": current},
    )
    entries = DeclaredRegistry(
        "declared_host.plugins",
        "/unused",
        {"Target": "target", "Later": "later"},
        discovery_mode="entry_points",
        entrypoint_group="host.plugins",
    )
    assert list(entries.keys()) == ["Target", "Later"]
    assert target.calls == sentinel.calls == 0
    assert entries["Target"].form_name == "Target"
    assert target.calls == 1 and sentinel.calls == 0
    with pytest.raises(KeyError):
        entries["Later"]
    later = EntryPoint("later", "Later")
    current = [target, sentinel, later]
    with pytest.raises(KeyError):
        entries.retry("Later")
    entries.refresh()
    assert entries["Later"].form_name == "Later"
    assert target.calls == 1 and sentinel.calls == 0 and later.calls == 1


def test_duplicate_entrypoint_names_rejected_without_loading(plugins, monkeypatch):
    a, b = EntryPoint("target", "Target"), EntryPoint("target", "Target")
    monkeypatch.setattr("depdigest.core.loader.entry_points", lambda: {"group": [a, b]})
    entries = DeclaredRegistry(
        "declared_host.plugins",
        "/unused",
        {"Target": "target"},
        discovery_mode="entry_points",
        entrypoint_group="group",
    )
    with pytest.raises(KeyError) as caught:
        entries["Target"]
    assert isinstance(caught.value.__cause__, LookupError)
    assert a.calls == b.calls == 0


def test_success_and_failure_diagnostics_identify_request_and_trigger(
    plugins, monkeypatch
):
    write_plugin(plugins, "target", "form_name = 'Target'")
    write_plugin(plugins, "bad", "raise RuntimeError('broken')")
    events = []
    monkeypatch.setattr(
        "smonitor.integrations.emit_from_catalog",
        lambda signal, **kw: events.append((signal, kw["extra"])),
    )
    entries = registry(plugins, {"Target": "target", "Bad": "bad"})
    entries["Target"]
    with pytest.raises(KeyError):
        entries["Bad"]
    success = next(
        extra for signal, extra in events if signal["code"] == "DEP-DBG-LOAD-002"
    )
    failure = next(
        extra for signal, extra in events if signal["code"] == "DEP-DBG-LOAD-001"
    )
    assert success["plugin"] == "target" and success["trigger"] == "Target"
    assert failure["plugin"] == "bad" and failure["trigger"] == "Bad"
    assert success["caller"].startswith(__file__ + ":")
    assert failure["caller"].startswith(__file__ + ":")


def test_diagnostic_failure_keeps_success_and_original_load_error(plugins, monkeypatch):
    write_plugin(plugins, "target", "form_name = 'Target'")
    write_plugin(plugins, "bad", "raise RuntimeError('original error')")

    def broken_emitter(*args, **kwargs):
        raise ValueError("emitter failure")

    monkeypatch.setattr("smonitor.integrations.emit_from_catalog", broken_emitter)
    entries = registry(plugins, {"Target": "target", "Bad": "bad"})
    assert entries["Target"].form_name == "Target"
    with pytest.raises(KeyError) as caught:
        entries["Bad"]
    assert str(caught.value.__cause__) == "original error"


def test_entrypoint_identity_fallback_and_undeclared_duplicate_order(
    plugins, monkeypatch
):
    first = EntryPoint("a", "Shared")
    second = EntryPoint("b", "Shared")
    bare = EntryPoint("bare")
    monkeypatch.setattr(
        "depdigest.core.loader.entry_points", lambda: {"group": [second, bare, first]}
    )
    entries = DeclaredRegistry(
        "declared_host.plugins",
        "/unused",
        {"bare": "bare"},
        discovery_mode="entry_points",
        entrypoint_group="group",
    )
    entries["bare"]
    assert entries.discover() == ("bare", "Shared")
    assert entries["Shared"].form_name == "Shared"
    entries.discover()
    assert (first.calls, second.calls, bare.calls) == (1, 1, 1)


def test_discovery_failure_does_not_poison_a_declared_identity(plugins):
    write_plugin(plugins, "other", "form_name = 'broken'")
    write_plugin(plugins, "broken", "raise RuntimeError('discovery failure')")
    entries = registry(plugins, {"broken": "other"})
    entries.discover()
    assert entries["broken"].form_name == "broken"


def test_recursive_request_fails_boundedly_and_independent_nested_load_survives(
    plugins, monkeypatch
):
    write_plugin(plugins, "a", "form_name = 'A'")
    write_plugin(plugins, "b", "form_name = 'B'")
    entries = registry(plugins, {"A": "a", "B": "b"})

    def load(name):
        if name.endswith(".a"):
            with pytest.raises(KeyError, match="Recursive"):
                entries["A"]
            assert entries["B"].form_name == "B"
            return SimpleNamespace(form_name="A")
        return SimpleNamespace(form_name="B")

    monkeypatch.setattr("depdigest.core.registry.import_module", load)
    assert entries["A"].form_name == "A"
    assert entries.loaded_keys() == ("A", "B")


def test_executable_visibility_tracks_path_and_retry_after_installation(
    plugins, monkeypatch
):
    write_plugin(plugins, "engine", "form_name = 'Engine'")
    available = False
    monkeypatch.setattr(
        "depdigest.core.checker.shutil.which",
        lambda name: "/engine" if available else None,
    )
    cfg = DepConfig(
        libraries={"engine": {"type": "soft", "kind": "executable"}},
        mapping={"engine": "engine"},
        show_all_capabilities=False,
    )
    with temporary_package_config("declared_host", cfg):
        entries = registry(plugins, {"Engine": "engine"})
        assert "Engine" not in entries
        available = True
        assert "Engine" in entries
        assert entries["Engine"].form_name == "Engine"
        available = False
        assert "Engine" not in entries
        entries["Engine"] = "manual"
        assert entries["Engine"] == "manual"


@pytest.mark.parametrize("mode, group", [("invalid", None), ("entry_points", None)])
def test_invalid_discovery_options_rejected(plugins, mode, group):
    with pytest.raises(ValueError):
        DeclaredRegistry(
            "declared_host.plugins",
            plugins,
            {},
            discovery_mode=mode,
            entrypoint_group=group,
        )
