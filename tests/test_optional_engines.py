"""Reusable optional-engine contract for Python packages and executables."""

from unittest.mock import patch

import pytest

from depdigest import (
    DepConfig,
    check_dependency,
    dep_digest,
    get_info,
    is_installed,
    temporary_package_config,
)


def test_pip_only_dependency_never_suggests_conda():
    with patch("depdigest.core.checker.is_installed", return_value=False):
        with pytest.raises(ImportError) as caught:
            check_dependency("pocketeer", pypi_name="pocketeer", conda_name=None)
    assert "pip install pocketeer" in str(caught.value)
    assert "conda install" not in str(caught.value)


def test_inventory_respects_disabled_installers_and_declared_channel():
    config = DepConfig(
        libraries={
            "pocketeer": {"type": "soft", "pypi": "pocketeer", "conda": None},
            "fpocket": {
                "type": "soft",
                "kind": "executable",
                "pypi": None,
                "conda": "fpocket",
                "channel": "conda-forge",
            },
            "other": {
                "type": "soft",
                "pypi": None,
                "conda": "other",
                "channel": "uibcdf",
            },
        }
    )
    with temporary_package_config("engine_consumer", config):
        rows = {
            row["library"]: row
            for row in get_info("engine_consumer", "dict")["dependencies"]
        }
    assert rows["pocketeer"]["install"] == {
        "pypi": "pip install pocketeer",
        "conda": None,
    }
    assert rows["fpocket"]["install"] == {
        "pypi": None,
        "conda": "conda install -c conda-forge fpocket",
    }
    assert rows["other"]["install"]["conda"] == "conda install -c uibcdf other"


def test_executable_check_does_not_import_a_python_package(tmp_path, monkeypatch):
    executable = tmp_path / "engine-command"
    executable.write_text("#!/bin/sh\nexit 0\n")
    executable.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path))
    with patch(
        "depdigest.core.checker.is_installed",
        side_effect=AssertionError("Python probe"),
    ):
        check_dependency("engine", kind="executable", executable="engine-command")


def test_executable_availability_follows_current_path(tmp_path, monkeypatch):
    executable = tmp_path / "engine-command"
    executable.write_text("#!/bin/sh\nexit 0\n")
    executable.chmod(0o755)
    check_dependency("engine", kind="executable", executable=str(executable))
    executable.chmod(0o644)
    with pytest.raises(ImportError):
        check_dependency("engine", kind="executable", executable=str(executable))


def test_missing_executable_has_conda_only_hint_and_structured_event(monkeypatch):
    monkeypatch.setenv("PATH", "")
    with patch("smonitor.integrations.emit_from_catalog") as emit:
        with pytest.raises(ImportError) as caught:
            check_dependency(
                "fpocket", kind="executable", pypi_name=None, conda_name="fpocket"
            )
    assert "conda install -c conda-forge fpocket" in str(caught.value)
    assert "pip install" not in str(caught.value)
    extra = emit.call_args.kwargs["extra"]
    assert extra["kind"] == "executable"
    assert extra["executable"] == "fpocket"


def test_conditional_executable_dependency_guards_only_selected_backend(monkeypatch):
    config = DepConfig(
        libraries={
            "engine": {
                "type": "soft",
                "kind": "executable",
                "executable": "engine-command",
                "pypi": None,
                "conda": "engine-package",
                "channel": "uibcdf",
            }
        }
    )

    @dep_digest("engine", when={"backend": "external"})
    def analyze(*, backend="native"):
        return "available"

    with temporary_package_config(__name__.split(".")[0], config):
        monkeypatch.setenv("PATH", "")
        assert analyze() == "available"
        with pytest.raises(ImportError) as caught:
            analyze(backend="external")
    assert "conda install -c uibcdf engine-package" in str(caught.value)


def test_executable_inventory_uses_path_not_find_spec(tmp_path, monkeypatch):
    executable = tmp_path / "engine-command"
    executable.write_text("#!/bin/sh\nexit 0\n")
    executable.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path))
    config = DepConfig(
        libraries={
            "engine": {
                "kind": "executable",
                "executable": "engine-command",
                "pypi": None,
            }
        }
    )
    with temporary_package_config("engine_consumer", config):
        rows = get_info("engine_consumer", "dict")["dependencies"]
    assert rows[0]["installed"] is True


def test_no_install_route_does_not_invent_a_command():
    with patch("depdigest.core.checker.is_installed", return_value=False):
        with pytest.raises(ImportError) as caught:
            check_dependency("proprietary_engine", pypi_name=None, conda_name=None)
    assert "pip install" not in str(caught.value)
    assert "conda install" not in str(caught.value)


def test_invalid_dependency_kind_fails_explicitly():
    with pytest.raises(ValueError, match="kind"):
        check_dependency("engine", kind="unknown")


def test_registry_routes_executable_plugins_through_same_availability_probe(
    tmp_path, monkeypatch
):
    from depdigest import LazyRegistry

    command = tmp_path / "engine-command"
    command.write_text("#!/bin/sh\nexit 0\n")
    command.chmod(0o755)
    monkeypatch.setenv("PATH", str(tmp_path))
    config = DepConfig(
        libraries={
            "engine": {
                "type": "soft",
                "kind": "executable",
                "executable": "engine-command",
            }
        },
        mapping={"plugin": "engine"},
        show_all_capabilities=False,
    )
    registry = LazyRegistry("consumer.plugins", str(tmp_path))
    assert registry._plugin_allowed("plugin", config)
    command.chmod(0o644)
    assert not registry._plugin_allowed("plugin", config)


def test_dotted_module_preserves_transitive_import_failure():
    original = ModuleNotFoundError(
        "missing internal dependency", name="internal_dependency"
    )
    is_installed.cache_clear()
    with patch("depdigest.core.checker.find_spec", side_effect=original):
        with pytest.raises(ModuleNotFoundError) as caught:
            is_installed("engine.backend")
    assert caught.value is original


def test_dotted_module_with_absent_parent_is_missing():
    original = ModuleNotFoundError("missing engine", name="engine")
    is_installed.cache_clear()
    with patch("depdigest.core.checker.find_spec", side_effect=original):
        assert not is_installed("engine.backend")
    is_installed.cache_clear()
