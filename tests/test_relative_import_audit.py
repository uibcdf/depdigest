"""Relative adapter imports do not name external optional dependencies."""

import json

import pytest

from depdigest.cli import main
from depdigest.utils.ast_tools import check_top_level_imports


@pytest.mark.parametrize(
    "statement",
    [
        "from .vina import VinaBackend",
        "from ..vina.api import VinaBackend",
        "from .vina import *",
        "from . import vina",
        "from .. import vina",
    ],
)
@pytest.mark.parametrize("scope", ["module", "if", "class", "try"])
def test_relative_adapter_imports_are_internal(statement, scope, tmp_path):
    if scope == "module":
        source = statement + "\n"
    elif scope == "if":
        source = f"if enabled:\n    {statement}\n"
    elif scope == "class":
        source = f"class Adapter:\n    {statement}\n"
    else:
        source = f"try:\n    {statement}\nexcept ImportError:\n    pass\n"
    path = tmp_path / "adapter.py"
    path.write_text(source)
    assert check_top_level_imports(str(path), {"vina"}) == []


@pytest.mark.parametrize(
    "statement,module",
    [
        ("import vina", "vina"),
        ("import vina.api as engine", "vina.api"),
        ("from vina import Vina", "vina"),
        ("from vina.api import Vina", "vina.api"),
    ],
)
def test_absolute_engine_imports_still_report_source_lines(statement, module, tmp_path):
    path = tmp_path / "external.py"
    path.write_text(statement + "\n")
    assert check_top_level_imports(str(path), {"vina"}) == [(1, module)]


def test_mixed_scopes_keep_absolute_findings_and_delay_functions(tmp_path):
    path = tmp_path / "mixed.py"
    path.write_text(
        "from .vina import VinaBackend\n"
        "if enabled:\n"
        "    from ..vina.api import Adapter\n"
        "    from vina import Vina\n"
        "class Adapter:\n"
        "    from .openmm import helper\n"
        "    from openmm.app import PDBFile\n"
        "def run():\n"
        "    import vina\n"
        "async def run_async():\n"
        "    from openmm import app\n"
    )
    assert check_top_level_imports(str(path), {"vina", "openmm"}) == [
        (4, "vina"),
        (7, "openmm.app"),
    ]


def test_cli_relative_only_fixture_is_clean(tmp_path, capsys):
    path = tmp_path / "adapter.py"
    path.write_text("from .vina import VinaBackend\n")
    assert (
        main(["audit", "--src-root", str(tmp_path), "--soft-deps", "vina", "--json"])
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "src_root": str(tmp_path),
        "soft_deps": ["vina"],
        "violation_count": 0,
        "violations": {},
    }


def test_cli_mixed_fixture_retains_json_exit_and_exact_exemption(tmp_path, capsys):
    path = tmp_path / "adapter.py"
    path.write_text("from .vina import VinaBackend\nimport vina\n")
    arguments = ["audit", "--src-root", str(tmp_path), "--soft-deps", "vina", "--json"]
    assert main(arguments) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["violation_count"] == 1
    assert payload["violations"] == {str(path): [{"line": 2, "module": "vina"}]}
    assert main([*arguments, "--allow-violations"]) == 0
    assert json.loads(capsys.readouterr().out) == payload
    assert main([*arguments, "--exempt-file", str(path)]) == 0
    exempted = json.loads(capsys.readouterr().out)
    assert exempted["violation_count"] == 0
    assert exempted["violations"] == {}
