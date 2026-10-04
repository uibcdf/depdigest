import pytest

from depdigest.utils.ast_tools import check_top_level_imports, validate_codebase


def test_check_top_level_imports_detects_import_and_from_import(tmp_path):
    file_path = tmp_path / "sample.py"
    file_path.write_text(
        "import os\n"
        "import openmm\n"
        "from mdtraj import load\n"
        "def fn():\n"
        "    import openmm\n",
        encoding="utf-8",
    )

    violations = check_top_level_imports(str(file_path), {"openmm", "mdtraj"})

    assert (2, "openmm") in violations
    assert (3, "mdtraj") in violations
    assert len(violations) == 2


def test_check_top_level_imports_ignores_syntax_error_file(tmp_path):
    file_path = tmp_path / "broken.py"
    file_path.write_text("def bad(:\n", encoding="utf-8")

    assert check_top_level_imports(str(file_path), {"openmm"}) == []


def test_validate_codebase_respects_exemptions(tmp_path):
    src_root = tmp_path / "pkg"
    src_root.mkdir()
    (src_root / "ok.py").write_text("import os\n", encoding="utf-8")
    (src_root / "bad.py").write_text("import openmm\n", encoding="utf-8")

    exempt_dir = src_root / "exempt"
    exempt_dir.mkdir()
    (exempt_dir / "skip.py").write_text("import openmm\n", encoding="utf-8")

    violations = validate_codebase(
        src_root=str(src_root),
        soft_deps={"openmm"},
        exempt_files={str(src_root / "bad.py")},
        exempt_dirs=[str(exempt_dir)],
    )

    assert violations == {}


@pytest.mark.parametrize(
    "source",
    [
        "if enabled:\n    import openmm\n",
        "try:\n    import openmm\nexcept ImportError:\n    pass\n",
        "try:\n    pass\nexcept ImportError:\n    import openmm\n",
        "try:\n    pass\nexcept ImportError:\n    pass\nelse:\n    import openmm\n",
        "try:\n    pass\nfinally:\n    import openmm\n",
        "try:\n    pass\nexcept* ImportError:\n    import openmm\n",
        "for item in items:\n    import openmm\n",
        "for item in items:\n    pass\nelse:\n    import openmm\n",
        "while enabled:\n    import openmm\n",
        "with manager:\n    import openmm\n",
        "match backend:\n    case 'external':\n        import openmm\n",
        "class Adapter:\n    if enabled:\n        import openmm\n",
    ],
)
def test_module_level_blocks_are_audited(source, tmp_path):
    path = tmp_path / "eager.py"
    path.write_text(source, encoding="utf-8")
    findings = check_top_level_imports(str(path), {"openmm"})
    assert len(findings) == 1
    line, module = findings[0]
    assert module == "openmm"
    assert source.splitlines()[line - 1].strip() == "import openmm"


def test_function_bodies_and_their_nested_classes_remain_delayed(tmp_path):
    path = tmp_path / "delayed.py"
    path.write_text(
        "def operation():\n"
        "    if enabled:\n"
        "        import openmm\n"
        "    class LocalAdapter:\n"
        "        import openmm\n"
        "async def async_operation():\n"
        "    import openmm\n"
        "class Adapter:\n"
        "    def method(self):\n"
        "        import openmm\n",
        encoding="utf-8",
    )
    assert check_top_level_imports(str(path), {"openmm"}) == []


@pytest.mark.parametrize(
    ("declaration", "flag"),
    [
        ("from typing import TYPE_CHECKING", "TYPE_CHECKING"),
        ("from typing import TYPE_CHECKING as TC", "TC"),
        ("import typing", "typing.TYPE_CHECKING"),
        ("import typing as t", "t.TYPE_CHECKING"),
    ],
)
def test_typing_only_branches_are_excluded_but_runtime_branches_are_audited(
    declaration, flag, tmp_path
):
    path = tmp_path / "typing_only.py"
    path.write_text(
        f"{declaration}\n"
        f"if {flag}:\n"
        "    import openmm\n"
        "else:\n"
        "    import mdtraj\n"
        f"if not {flag}:\n"
        "    from mdtraj import load\n"
        "else:\n"
        "    from openmm import app\n",
        encoding="utf-8",
    )
    assert check_top_level_imports(str(path), {"openmm", "mdtraj"}) == [
        (5, "mdtraj"),
        (7, "mdtraj"),
    ]


@pytest.mark.parametrize(
    "source",
    [
        "TYPE_CHECKING = True\nif TYPE_CHECKING:\n    import openmm\n",
        "from other import TYPE_CHECKING\nif TYPE_CHECKING:\n    import openmm\n",
        "from typing import TYPE_CHECKING as TC\nTC = True\nif TC:\n    import openmm\n",
        "import typing as t\nt.TYPE_CHECKING = True\nif t.TYPE_CHECKING:\n    import openmm\n",
        "import typing as t\nt = other\nif t.TYPE_CHECKING:\n    import openmm\n",
        "from typing import TYPE_CHECKING\nclass Adapter:\n    TYPE_CHECKING = True\n    if TYPE_CHECKING:\n        import openmm\n",
        "from typing import TYPE_CHECKING\nfrom other import *\nif TYPE_CHECKING:\n    import openmm\n",
        "from typing import TYPE_CHECKING as TC\nfor TC in flags:\n    if TC:\n        import openmm\n",
        "from typing import TYPE_CHECKING as TC\ntry:\n    pass\nexcept ImportError as TC:\n    if TC:\n        import openmm\n",
        "from typing import TYPE_CHECKING as TC\ndef TC():\n    pass\nif TC:\n    import openmm\n",
        "from typing import TYPE_CHECKING as TC\nmatch value:\n    case TC:\n        if TC:\n            import openmm\n",
        "from typing import TYPE_CHECKING as TC\nmatch value:\n    case [*TC]:\n        if TC:\n            import openmm\n",
        "from typing import TYPE_CHECKING as TC\nmatch value:\n    case {'key': item, **TC}:\n        if TC:\n            import openmm\n",
    ],
)
def test_unproven_or_rebound_typing_guards_do_not_hide_imports(source, tmp_path):
    path = tmp_path / "runtime_guard.py"
    path.write_text(source, encoding="utf-8")
    assert len(check_top_level_imports(str(path), {"openmm"})) == 1


def test_delayed_rebinding_does_not_disable_a_typing_only_guard(tmp_path):
    path = tmp_path / "typing_only.py"
    path.write_text(
        "from typing import TYPE_CHECKING as TC\n"
        "def operation():\n"
        "    TC = True\n"
        "    import openmm\n"
        "class Adapter:\n"
        "    if TC:\n"
        "        import openmm\n"
        "    else:\n"
        "        import mdtraj\n",
        encoding="utf-8",
    )
    assert check_top_level_imports(str(path), {"openmm", "mdtraj"}) == [(9, "mdtraj")]
