from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ci_python314_feasibility.yaml"
RECEPTOR = ROOT / ".github" / "gh-run-receptor.yaml"


def test_python314_probe_is_source_only_and_non_claiming():
    workflow = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch:" in workflow
    assert "release:" not in workflow
    assert "push:" not in workflow
    assert "python=3.14" in workflow
    assert "smonitor=0.16.0=py_1" in workflow
    assert "pytest-receptor=1.1.0=py_1" in workflow
    assert "ubuntu-latest, macos-latest, windows-latest" in workflow
    assert 'export PYTHONPATH="$GITHUB_WORKSPACE"' in workflow
    assert "pip install" not in workflow
    assert "--receptor=ci" in workflow
    assert "uibcdf/label/staging" not in workflow


def test_python314_probe_has_explicit_ci_receptor_profile():
    receptor = RECEPTOR.read_text(encoding="utf-8")
    assert (
        "path: .github/workflows/ci_python314_feasibility.yaml\n    profile: ci"
        in receptor
    )
