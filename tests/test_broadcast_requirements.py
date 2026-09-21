from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_broadcast_runs_from_repo_root_and_preserves_jinja(tmp_path):
    shutil.copytree(ROOT / "devtools", tmp_path / "devtools")

    completed = subprocess.run(
        [sys.executable, "devtools/broadcast_requirements.py"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr

    recipe = (tmp_path / "devtools" / "conda-build" / "meta.yaml").read_text(
        encoding="utf-8"
    )
    assert "version: \"{{ environ['GIT_DESCRIBE_TAG'] }}\"" in recipe
    assert (
        "number: \"{{ environ.get('DEPDIGEST_CONDA_BUILD_NUMBER', '0') }}\"" in recipe
    )
