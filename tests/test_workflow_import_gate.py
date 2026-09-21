"""Regression checks for the CI import smoke step's failure semantics."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
IMPORT_PROBE = (
    'import depdigest; print("Version of the package: {}".format('
    "depdigest.__version__))"
)


def _runner_bash() -> str:
    if os.name != "nt":
        return "bash"
    git = shutil.which("git")
    assert git is not None, "Git Bash is required by the Windows CI workflow"
    git_path = Path(git).resolve()
    candidates = [git_path.parent / "bash.exe"] + [
        parent / "bin" / "bash.exe" for parent in list(git_path.parents)[:3]
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise AssertionError(f"Git Bash not found beside {git_path}")


@pytest.mark.parametrize(
    ("filename", "job_name"),
    [("CI.yaml", "test"), ("CI_full_matrix.yaml", "full-test")],
)
def test_failed_import_cannot_be_hidden_by_trailing_echo(filename, job_name):
    workflow = yaml.safe_load(
        (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
    )
    steps = workflow["jobs"][job_name]["steps"]
    script = next(
        step["run"] for step in steps if step.get("name") == "Test import module"
    )
    assert script.count(IMPORT_PROBE) == 1

    failing_script = script.replace(IMPORT_PROBE, "raise SystemExit(17)")
    completed = subprocess.run(
        [_runner_bash(), "-c", failing_script],
        cwd=ROOT,
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 17, completed.stdout + completed.stderr
    assert "::endgroup::" not in completed.stdout
