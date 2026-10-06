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


def test_committed_profiles_are_generated_without_python_duplicates(tmp_path):
    import yaml

    shutil.copytree(ROOT / "devtools", tmp_path / "devtools")
    completed = subprocess.run(
        [sys.executable, "devtools/broadcast_requirements.py"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    paths = [
        Path("devtools/conda-build/meta.yaml"),
        *[
            path.relative_to(ROOT)
            for path in (ROOT / "devtools/conda-envs").glob("*_env.yaml")
        ],
    ]
    for path in paths:
        assert (tmp_path / path).read_bytes() == (ROOT / path).read_bytes(), (
            f"Regenerate {path} from requirements.yaml"
        )
    development = yaml.safe_load(
        (tmp_path / "devtools/conda-envs/development_env.yaml").read_text()
    )
    assert [
        item for item in development["dependencies"] if item.startswith("python ")
    ] == ["python =3.14"]
