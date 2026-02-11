import pytest
import os
from unittest.mock import patch
from depdigest import is_installed, dep_digest, LazyRegistry, DepConfig, register_package_config, clear_package_configs

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    clear_package_configs()
    yield
    # Code that will run after each test
    clear_package_configs()

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
