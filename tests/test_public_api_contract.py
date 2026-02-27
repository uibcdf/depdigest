import json

import depdigest
from depdigest import DepConfig, clear_package_configs, register_package_config


def test_public_api_exports_expected_symbols():
    expected = {
        "is_installed",
        "check_dependency",
        "get_info",
        "dep_digest",
        "LazyRegistry",
        "DepConfig",
        "resolve_config",
        "register_package_config",
        "unregister_package_config",
        "temporary_package_config",
        "clear_package_configs",
    }
    assert set(depdigest.__all__) == expected


def test_public_api_exports_are_available_as_attributes():
    for name in depdigest.__all__:
        assert hasattr(depdigest, name)


def test_get_info_schema_contract_is_stable():
    clear_package_configs()
    register_package_config(
        "contract_pkg",
        DepConfig(
            libraries={
                "a.module": {"type": "hard"},
                "b.module": {"type": "soft"},
            }
        ),
    )

    payload = depdigest.get_info("contract_pkg", format="dict")

    assert payload["schema"] == {"name": "depdigest.get_info", "version": "1.0"}
    assert set(payload.keys()) == {
        "schema",
        "module_path",
        "dependency_count",
        "installed_count",
        "missing_count",
        "dependencies",
    }
    assert isinstance(payload["dependencies"], list)
    first = payload["dependencies"][0]
    assert set(first.keys()) == {
        "library",
        "installed",
        "status",
        "type",
        "package_name",
        "install",
    }
    assert set(first["package_name"].keys()) == {"pypi", "conda"}
    assert set(first["install"].keys()) == {"pypi", "conda"}


def test_get_info_json_and_dict_are_semantically_equivalent():
    clear_package_configs()
    register_package_config(
        "contract_pkg_json",
        DepConfig(libraries={"a.module": {"type": "soft"}}),
    )

    as_dict = depdigest.get_info("contract_pkg_json", format="dict")
    as_json = depdigest.get_info("contract_pkg_json", format="json")

    assert json.loads(as_json) == as_dict

