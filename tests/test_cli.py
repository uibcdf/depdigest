import json

from depdigest.cli import main


def test_cli_audit_returns_nonzero_when_violations_found(tmp_path):
    src = tmp_path / "pkg"
    src.mkdir()
    (src / "bad.py").write_text("import openmm\n", encoding="utf-8")

    rc = main(["audit", "--src-root", str(src), "--soft-deps", "openmm"])
    assert rc == 1


def test_cli_audit_returns_zero_when_clean(tmp_path):
    src = tmp_path / "pkg"
    src.mkdir()
    (src / "ok.py").write_text("import os\n", encoding="utf-8")

    rc = main(["audit", "--src-root", str(src), "--soft-deps", "openmm"])
    assert rc == 0


def test_cli_audit_json_output(tmp_path, capsys):
    src = tmp_path / "pkg"
    src.mkdir()
    (src / "bad.py").write_text("from mdtraj import load\n", encoding="utf-8")

    rc = main(["audit", "--src-root", str(src), "--soft-deps", "mdtraj", "--json"])
    assert rc == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["violation_count"] == 1


def test_cli_audit_allow_violations_returns_zero(tmp_path):
    src = tmp_path / "pkg"
    src.mkdir()
    (src / "bad.py").write_text("import openmm\n", encoding="utf-8")

    rc = main(
        [
            "audit",
            "--src-root",
            str(src),
            "--soft-deps",
            "openmm",
            "--allow-violations",
        ]
    )
    assert rc == 0


def test_cli_reports_nested_module_imports_with_source_lines(tmp_path, capsys):
    src = tmp_path / "pkg"
    src.mkdir()
    path = src / "__init__.py"
    path.write_text(
        "from typing import TYPE_CHECKING\n"
        "if TYPE_CHECKING:\n"
        "    import openmm\n"
        "try:\n"
        "    from mdtraj import load\n"
        "except ImportError:\n"
        "    pass\n",
        encoding="utf-8",
    )
    arguments = [
        "audit",
        "--src-root",
        str(src),
        "--soft-deps",
        "openmm,mdtraj",
        "--json",
    ]
    assert main(arguments) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["violation_count"] == 1
    assert payload["violations"] == {str(path): [{"line": 5, "module": "mdtraj"}]}
    assert main([*arguments, "--allow-violations"]) == 0
    allowed = json.loads(capsys.readouterr().out)
    assert allowed == payload
