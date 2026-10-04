"""Run the maintained integration probe without changing pytest's process state."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_OVERRIDE = os.environ.get("DEPDIGEST_INTEGRATION_WORKSPACE")
WORKSPACE = Path(WORKSPACE_OVERRIDE) if WORKSPACE_OVERRIDE else ROOT.parent
SIBLINGS_AVAILABLE = all(
    (WORKSPACE / name / name / "__init__.py").is_file()
    for name in ("smonitor", "argdigest", "pyunitwizard")
)


@pytest.mark.skipif(
    not SIBLINGS_AVAILABLE and not WORKSPACE_OVERRIDE,
    reason="Sibling repos are not available; set DEPDIGEST_INTEGRATION_WORKSPACE",
)
@pytest.mark.parametrize(
    "arguments",
    [
        ["--case", "contracts"],
        *[
            ["--case", "imports", "--package", name]
            for name in ("depdigest", "smonitor", "argdigest", "pyunitwizard")
        ],
    ],
)
def test_collective_error_path_and_optional_import_boundaries(arguments, tmp_path):
    receipt = tmp_path / "integration.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-I",
            str(ROOT / "devtools" / "integration_probe.py"),
            "--workspace",
            str(WORKSPACE),
            "--output",
            str(receipt),
            *arguments,
        ],
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stdout == ""
    evidence = json.loads(receipt.read_text(encoding="utf-8"))
    assert evidence["schema"] == "depdigest.integration_probe@1"
    assert evidence["sources"]["depdigest"]["root"] == str(ROOT.resolve())
    package = "depdigest" if arguments[1] == "contracts" else arguments[-1]
    package_root = ROOT if package == "depdigest" else WORKSPACE / package
    assert evidence["sources"][package]["origin"] == str(
        (package_root / package / "__init__.py").resolve()
    )
