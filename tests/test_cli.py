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

