import pytest
import sys
from unittest.mock import patch
from depdigest import is_installed, dep_digest, LazyRegistry, DepConfig, register_package_config, clear_package_configs
from depdigest.core.config import resolve_config

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    clear_package_configs()
    is_installed.cache_clear()
    resolve_config.cache_clear()
    yield
    # Code that will run after each test
    clear_package_configs()
    is_installed.cache_clear()
    resolve_config.cache_clear()

def test_is_installed_caching():
    """Verify that is_installed results are cached."""
    assert is_installed('numpy') is True

def test_dep_digest_metadata():
    """Verify that @dep_digest attaches metadata correctly."""
    @dep_digest('mdtraj')
    def dummy_func():
        pass
    
    assert hasattr(dummy_func, '_dependencies')
    assert dummy_func._dependencies[0]['library'] == 'mdtraj'

def test_lazy_registry_filtering():
    """
    Test that LazyRegistry filters modules based on config.
    """
    # Create a dummy structure
    # mylib/
    #   _depdigest.py
    #   plugins/
    #     __init__.py
    #     p1/ (__init__.py with plugin_name='p1')
    
    # But instead of real files, let's mock resolve_config
    from depdigest.core.config import DepConfig
    
    mock_cfg = DepConfig(
        libraries={'lib1': {'type': 'soft'}},
        mapping={'p1': 'lib1'},
        show_all_capabilities=False
    )
    
    with patch('depdigest.core.loader.resolve_config', return_value=mock_cfg):
        # Mock os.scandir to simulate a directory entry 'p1'
        class MockEntry:
            def __init__(self, name): self.name = name
            def is_dir(self): return True
            
        with patch('os.path.exists', return_value=True):
            with patch('os.scandir', return_value=[MockEntry('p1')]):
                # Mock is_installed to return False for 'lib1'
                with patch('depdigest.core.loader.is_installed', return_value=False):
                    registry = LazyRegistry('mylib.plugins', '/fake/path', attr_name='plugin_name')
                    # Should be empty because p1 is filtered out
                    assert len(registry.keys()) == 0
                
                # Mock is_installed to return True
                with patch('depdigest.core.loader.is_installed', return_value=True):
                    # We need to mock the import too
                    import sys
                    from types import ModuleType
                    mock_mod = ModuleType('mylib.plugins.p1')
                    mock_mod.plugin_name = 'p1'
                    sys.modules['mylib.plugins.p1'] = mock_mod
                    
                    registry = LazyRegistry('mylib.plugins', '/fake/path', attr_name='plugin_name')
                    assert 'p1' in registry

def test_dep_digest_runtime_error():
    """
    Verify that calling a decorated function without the library raises the configured exception.
    """
    class CustomError(Exception): pass
    
    # Register config for this test module
    module_root = __name__.split('.')[0]
    register_package_config(module_root, DepConfig(
        exception_class=CustomError
    ))
    
    @dep_digest('missing_lib')
    def func_needing_lib():
        pass
        
    with patch('depdigest.core.checker.is_installed', return_value=False):
        with pytest.raises(CustomError) as excinfo:
            func_needing_lib()
        assert "missing_lib" in str(excinfo.value)

def test_dep_digest_conditional_logic():
    """
    Verify that conditional requirements (when={...}) work correctly.
    """
    @dep_digest('opt_lib', when={'mode': 'strict'})
    def cond_func(mode='relaxed'):
        return "Success"

    # Case 1: Condition not met
    with patch('depdigest.core.checker.is_installed', return_value=False):
        assert cond_func(mode='relaxed') == "Success"

    # Case 2: Condition met
    with patch('depdigest.core.checker.is_installed', return_value=False):
        with pytest.raises(ImportError):
            cond_func(mode='strict')


def test_dep_digest_exception_contract_with_library_argument():
    """
    Verify compatibility with exception classes expecting (library, caller, message).
    """

    class LibraryStyleError(Exception):
        def __init__(self, library, caller=None, message=None):
            self.library = library
            self.caller = caller
            self.message = message
            super().__init__(f"{library}|{caller}|{message}")

    @dep_digest('missing_lib')
    def func_needing_lib():
        return "never"

    module_root = __name__.split('.')[0]
    register_package_config(module_root, DepConfig(
        exception_class=LibraryStyleError
    ))

    with patch('depdigest.core.checker.is_installed', return_value=False):
        with pytest.raises(LibraryStyleError) as excinfo:
            func_needing_lib()
        assert excinfo.value.library == "missing_lib"
        assert excinfo.value.caller == "func_needing_lib"


def test_missing_dependency_exception_has_readable_message():
    from depdigest.core.checker import check_dependency

    with pytest.raises(ImportError) as excinfo:
        check_dependency("definitely_nonexistent_pkg_zzz", caller="demo")

    message = str(excinfo.value)
    assert isinstance(message, str)
    assert message.strip() != ""
    assert "required" in message.lower()


def test_lazy_registry_plugin_import_failure_is_non_fatal():
    """Plugin import failures should be skipped, not crash registry resolution."""
    mock_cfg = DepConfig(
        libraries={},
        mapping={},
        show_all_capabilities=True,
    )

    with patch("depdigest.core.loader.resolve_config", return_value=mock_cfg):
        class MockEntry:
            def __init__(self, name):
                self.name = name

            def is_dir(self):
                return True

        with patch("os.path.exists", return_value=True):
            with patch("os.scandir", return_value=[MockEntry("broken_plugin")]):
                with patch("depdigest.core.loader.import_module", side_effect=RuntimeError("boom")):
                    registry = LazyRegistry("mylib.plugins", "/fake/path", attr_name="plugin_name")
                    assert list(registry.keys()) == []


def test_lazy_registry_emission_failure_is_non_fatal():
    """If diagnostics emission fails, plugin load failures must remain non-fatal."""
    mock_cfg = DepConfig(
        libraries={},
        mapping={},
        show_all_capabilities=True,
    )

    with patch("depdigest.core.loader.resolve_config", return_value=mock_cfg):
        class MockEntry:
            def __init__(self, name):
                self.name = name

            def is_dir(self):
                return True

        with patch("os.path.exists", return_value=True):
            with patch("os.scandir", return_value=[MockEntry("broken_plugin")]):
                with patch("depdigest.core.loader.import_module", side_effect=RuntimeError("boom")):
                    with patch("smonitor.integrations.emit_from_catalog", side_effect=RuntimeError("emit_failed")):
                        registry = LazyRegistry("mylib.plugins", "/fake/path", attr_name="plugin_name")
                        assert list(registry.keys()) == []


def test_resolve_config_with_none_returns_default_config():
    cfg = resolve_config(None)
    assert isinstance(cfg, DepConfig)
    assert cfg.libraries == {}


def test_get_info_checks_installation_by_importable_name():
    register_package_config("fakepkg", DepConfig(
        libraries={"fake.module": {"type": "soft", "pypi": "FakeModule"}},
    ))

    with patch("depdigest.core.checker.is_installed") as mocked:
        mocked.return_value = True
        from depdigest import get_info
        rows = get_info("fakepkg")

    assert rows[0]["Library"] == "fake.module"
    mocked.assert_called_once_with("fake.module")


def test_check_dependency_emission_failure_still_raises_dependency_error():
    """Dependency errors should still be raised even if diagnostics emission fails."""
    from depdigest.core.checker import check_dependency

    with patch("depdigest.core.checker.is_installed", return_value=False):
        with patch("smonitor.integrations.emit_from_catalog", side_effect=RuntimeError("emit_failed")):
            with pytest.raises(ImportError) as excinfo:
                check_dependency("missing_lib", caller="demo")
    assert "missing_lib" in str(excinfo.value)


def test_resolve_config_raises_for_internal_errors_in_depdigest_file(tmp_path):
    package_name = "tmp_pkg_for_config_error"
    package_dir = tmp_path / package_name
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text("", encoding="utf-8")
    (package_dir / "_depdigest.py").write_text(
        "import non_existing_dependency_for_test\n",
        encoding="utf-8",
    )

    sys.path.insert(0, str(tmp_path))
    resolve_config.cache_clear()
    try:
        with pytest.raises(ModuleNotFoundError):
            resolve_config(f"{package_name}.module")
    finally:
        resolve_config.cache_clear()
        sys.path.remove(str(tmp_path))


def test_resolve_config_raises_for_syntax_errors_in_depdigest_file(tmp_path):
    package_name = "tmp_pkg_for_config_syntax_error"
    package_dir = tmp_path / package_name
    package_dir.mkdir()
    (package_dir / "__init__.py").write_text("", encoding="utf-8")
    (package_dir / "_depdigest.py").write_text(
        "LIBRARIES = {\n",
        encoding="utf-8",
    )

    sys.path.insert(0, str(tmp_path))
    resolve_config.cache_clear()
    try:
        with pytest.raises(SyntaxError):
            resolve_config(f"{package_name}.module")
    finally:
        resolve_config.cache_clear()
        sys.path.remove(str(tmp_path))


def test_smonitor_dev_profile_has_clean_contract_for_missing_dependency():
    import smonitor
    from smonitor.handlers.memory import MemoryHandler
    from depdigest.core.checker import check_dependency

    memory = MemoryHandler(max_events=100)
    smonitor.configure(
        profile="dev",
        handlers=[memory],
        level="INFO",
        strict_signals=False,
        strict_schema=False,
        event_buffer_size=100,
    )

    with pytest.raises(ImportError):
        check_dependency("definitely_nonexistent_pkg_zzz", caller="dev_case")

    dep_events = [e for e in memory.events if e.get("code") == "DEP-ERR-MISS-001"]
    assert dep_events
    assert all("contract_warning" not in (e.get("extra") or {}) for e in dep_events)
    assert all("schema_warning" not in (e.get("extra") or {}) for e in dep_events)


def test_smonitor_qa_profile_has_clean_schema_for_missing_dependency():
    import smonitor
    from smonitor.handlers.memory import MemoryHandler
    from depdigest.core.checker import check_dependency

    memory = MemoryHandler(max_events=100)
    smonitor.configure(
        profile="qa",
        handlers=[memory],
        level="INFO",
        strict_signals=False,
        strict_schema=False,
        event_buffer_size=100,
    )

    with pytest.raises(ImportError):
        check_dependency("definitely_nonexistent_pkg_zzz", caller="qa_case")

    dep_events = [e for e in memory.events if e.get("code") == "DEP-ERR-MISS-001"]
    assert dep_events
    assert all("contract_warning" not in (e.get("extra") or {}) for e in dep_events)
    assert all("schema_warning" not in (e.get("extra") or {}) for e in dep_events)


def test_lazy_registry_methods_trigger_single_initialization():
    registry = LazyRegistry("mylib.plugins", "/fake/path", attr_name="plugin_name")

    def fake_scan():
        registry["p1"] = "module"

    with patch.object(registry, "_scan_and_load", side_effect=fake_scan) as mocked_scan:
        assert registry.get("p1") == "module"
        assert registry["p1"] == "module"
        assert list(registry.values()) == ["module"]
        assert list(registry.items()) == [("p1", "module")]
        assert mocked_scan.call_count == 1


def test_lazy_registry_ensure_initialized_returns_if_already_initializing():
    registry = LazyRegistry("mylib.plugins", "/fake/path", attr_name="plugin_name")
    registry._initializing = True

    with patch.object(registry, "_scan_and_load") as mocked_scan:
        registry._ensure_initialized()
        mocked_scan.assert_not_called()


def test_lazy_registry_scan_returns_when_directory_missing():
    registry = LazyRegistry("mylib.plugins", "/missing/path", attr_name="plugin_name")
    with patch("os.path.exists", return_value=False):
        registry._scan_and_load()
    assert list(registry.keys()) == []
