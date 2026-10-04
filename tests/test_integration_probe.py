"""Integration validation must fail rather than silently certify a bad setup."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "devtools" / "integration_probe.py"


def test_probe_rejects_an_explicit_missing_workspace(tmp_path):
    result = subprocess.run(
        [sys.executable, "-I", str(PROBE), "--workspace", str(tmp_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 1
    assert "Missing source package" in result.stderr


def test_import_probe_detects_a_conditional_eager_optional_import(tmp_path):
    for name in ("smonitor", "argdigest", "pyunitwizard"):
        package = tmp_path / name / name
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
    package = tmp_path / "argdigest" / "argdigest"
    (package / "__init__.py").write_text(
        "if True:\n    import optional_probe_backend\n", encoding="utf-8"
    )
    (package / "_depdigest.py").write_text(
        "LIBRARIES = {'optional_probe_backend': {'type': 'soft'}}\n",
        encoding="utf-8",
    )
    (package.parent / "optional_probe_backend.py").write_text("", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            str(PROBE),
            "--workspace",
            str(tmp_path),
            "--case",
            "imports",
            "--package",
            "argdigest",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 1
    assert (
        "eagerly imported optional roots: ['optional_probe_backend']" in result.stderr
    )
