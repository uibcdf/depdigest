from pathlib import Path

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
