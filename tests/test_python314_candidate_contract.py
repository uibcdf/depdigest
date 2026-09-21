import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / ".github" / "workflows" / "CI_full_matrix.yaml"


def test_candidate_metadata_and_required_ci_cover_python314():
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert metadata["project"]["requires-python"] == ">=3.11.0,<3.15.0"

    workflow = MATRIX.read_text(encoding="utf-8")
    cells = set(
        re.findall(
            r'^\s*-\s*\{\s*os:\s*([\w-]+),\s*python-version:\s*"(\d+\.\d+)"\s*\}\s*$',
            workflow,
            flags=re.MULTILINE,
        )
    )
    assert cells == {
        (operating_system, python_version)
        for operating_system in ("ubuntu-latest", "macos-latest", "windows-latest")
        for python_version in ("3.11", "3.12", "3.13", "3.14")
    }
    assert "python -m pytest --receptor=llm -n 4" in workflow
    assert "export PYTHONPATH" not in workflow


def test_requirements_source_and_derived_recipe_agree():
    source = (ROOT / "devtools" / "requirements.yaml").read_text(encoding="utf-8")
    recipe = (ROOT / "devtools" / "conda-build" / "meta.yaml").read_text(
        encoding="utf-8"
    )
    test_env = (ROOT / "devtools" / "conda-envs" / "test_env.yaml").read_text(
        encoding="utf-8"
    )
    assert source.count("python >=3.11,<3.15") == 2
    assert "pytest-receptor >=1.1.0" in source
    assert "- pyyaml" in source
    assert "- pyyaml" in test_env
    assert recipe.count("python >=3.11,<3.15") == 2


def test_ci_invokes_pytest_as_a_module_without_platform_specific_pythonpath():
    for filename in ("CI.yaml", "CI_full_matrix.yaml"):
        workflow = (ROOT / ".github" / "workflows" / filename).read_text(
            encoding="utf-8"
        )
        assert "python -m pytest --receptor=llm -n 4" in workflow
        assert "export PYTHONPATH" not in workflow


def test_public_badge_and_requirements_reflect_admitted_python314():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-" in readme
    assert "Published `0.11.0`: Python `>=3.11,<3.15`" in readme
