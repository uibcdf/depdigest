from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_conda_recipe_preserves_the_smonitor_runtime_floor():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    recipe = (ROOT / "devtools/conda-build/meta.yaml").read_text(encoding="utf-8")

    assert '"smonitor>=0.13.0"' in pyproject
    assert "- smonitor >=0.13.0" in recipe
