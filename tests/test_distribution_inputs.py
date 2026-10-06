"""Maintained route and publication guards for the DepDigest-owned integration."""

import importlib.util
import subprocess
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "depdigest_distribution", ROOT / "devtools/check_distribution_inputs.py"
)
preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preflight)


def test_qualification_cannot_hide_an_incomplete_installed_check():
    with pytest.raises(ValueError, match="qualification"):
        preflight.require_qualification(
            {"qualification": "declared-only"}, candidate=False
        )
    preflight.require_qualification({"qualification": "declared-only"}, candidate=True)


def test_every_source_workflow_requires_executed_jobs():
    plan = tomllib.loads((ROOT / "devtools/conda-build/release_plan.toml").read_text())
    assert sum(len(jobs) for jobs in preflight.required_jobs(plan).values()) == 13
    bad = dict(plan, gate_jobs={})
    with pytest.raises(ValueError, match="executed"):
        preflight.required_jobs(bad)


def test_candidate_mismatch_fails_before_evidence_acquisition(monkeypatch):
    monkeypatch.setattr(preflight, "source_head", lambda root: "1" * 40)
    with pytest.raises(ValueError, match="candidate"):
        preflight.verify_candidate(ROOT, ROOT, "0" * 40, {})


def test_promotion_profile_requires_all_twelve_cells_and_prepare():
    profile = preflight.installed_jobs()
    assert len(profile) == 13
    assert profile["Verify the immutable producer evidence"] == [
        "Download and verify the exact staging run receipts"
    ]
    assert all(
        len(steps) == 2
        for name, steps in profile.items()
        if name.startswith("Install ")
    )


def test_default_failure_retains_nonzero_status(monkeypatch, capsys):
    monkeypatch.setattr(preflight, "checked_tool", lambda root, commit: Path("tool.py"))
    monkeypatch.setattr(
        preflight.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 7, "bad public floor", ""
        ),
    )
    monkeypatch.setattr(preflight.sys, "argv", ["preflight", "--suite-root", "."])
    assert preflight.main() == 7
    assert "bad public floor" in capsys.readouterr().err


def test_source_calls_check_actual_installed_public_bounds_before_use():
    for name, marker in [
        ("CI.yaml", "- name: Install package"),
        ("CI_full_matrix.yaml", "- name: Install package"),
        ("ci_python314_feasibility.yaml", "- name: Test checkout source"),
        ("sphinx_docs_to_gh_pages.yaml", "- name: Installing the library"),
    ]:
        text = (ROOT / ".github/workflows" / name).read_text()
        assert text.index("- name: Check distribution inputs") < text.index(marker)
        assert "--declared-only" not in text
        assert "channel_priority: strict" in text


def test_mutation_requires_exact_source_and_retained_evidence():
    build = (
        ROOT / ".github/workflows/build_and_upload_conda_packages.yaml"
    ).read_text()
    assert build.index("--candidate-sha") < build.index(
        "- name: Build, test, and upload the staging candidate"
    )
    assert build.index("distribution-candidate-") < build.index(
        "- name: Build, test, and upload the unstaged release"
    )
    promote = (ROOT / ".github/workflows/promote_conda_package.yaml").read_text()
    assert "installed_run_id:" in promote
    assert promote.index("--installed-run-id") < promote.index(
        "- name: Promote the verified staged artifact"
    )
    assert promote.index("distribution-promotion-") < promote.index(
        "- name: Promote the verified staged artifact"
    )
    assert '--version "$RELEASE_VERSION" --build-number "$BUILD_NUMBER"' in build
    assert '--version "$RELEASE_VERSION" --build-number "$BUILD_NUMBER"' in promote


def test_installed_title_and_prepare_bind_the_same_candidate_and_archive():
    text = (ROOT / ".github/workflows/test_staged_conda_package.yaml").read_text()
    assert (
        "run-name: Installed depdigest-${{ inputs.version }}-py_${{ inputs.build_number }}.tar.bz2 ${{ inputs.sha256 }}"
        in text
    )
    assert 'test "$sha256" = "$EXPECTED_SHA256"' in text
    assert 'test "$GITHUB_SHA" = "$CANDIDATE_SHA"' in text
    assert text.count("ref: ${{ inputs.candidate_sha }}") == 2
    assert "channel_priority: flexible" in text
    assert "pip install" not in text


def test_provider_identity_and_dirty_tools_are_refused(tmp_path):
    tool = tmp_path / "devtools/scripts/dependency_routes.py"
    tool.parent.mkdir(parents=True)
    tool.write_text("# fixture\n")
    for args in [
        ["init", "-q"],
        ["add", "devtools"],
        [
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-qm",
            "fixture",
        ],
    ]:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True
    ).strip()
    assert preflight.checked_tool(tmp_path, commit) == tool
    with pytest.raises(ValueError, match="expected"):
        preflight.checked_tool(tmp_path, "0" * 40)
    tool.write_text("# changed\n")
    with pytest.raises(ValueError, match="modified"):
        preflight.checked_tool(tmp_path, commit)


def test_installed_failure_cannot_be_reported_as_verified(monkeypatch):
    monkeypatch.setattr(
        preflight.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0], 1, "", "required job skipped"
        ),
    )
    with pytest.raises(ValueError, match="skipped"):
        preflight.verify_installed(
            ROOT, 1, "1" * 40, {"version": "0.13.0", "build_number": 0}, "a" * 64
        )


@pytest.mark.parametrize(
    ("path", "before", "after", "diagnostic"),
    [
        (
            "devtools/conda-build/meta.yaml",
            "- smonitor >=0.13.0",
            "",
            "smonitor",
        ),
        (
            "devtools/conda-envs/test_env.yaml",
            "smonitor >=0.13.0",
            "smonitor >=0.12.0",
            "smonitor",
        ),
        (
            "devtools/conda-envs/production_env.yaml",
            "python >=3.11,<3.15",
            "python >=3.10,<3.15",
            "python",
        ),
        ("depdigest/cli.py", None, None, "depdigest/cli.py"),
        (
            "pyproject.toml",
            'file = "depdigest/_version.py"',
            'file = "depdigest/wrong_version.py"',
            "version target",
        ),
    ],
)
def test_real_provider_rejects_changed_dependencies_and_resources(
    tmp_path, path, before, after, diagnostic
):
    import os
    import shutil
    import sys

    suite_root = Path(
        os.environ.get("MOLSYSSUITE_TOOL_ROOT", ROOT / ".suite-tools/molsyssuite")
    )
    if not suite_root.is_dir():
        pytest.skip(
            "Pinned shared checkout required; source CI supplies it before tests"
        )
    for directory in ("devtools", "depdigest", ".github"):
        shutil.copytree(ROOT / directory, tmp_path / directory)
    shutil.copyfile(ROOT / "pyproject.toml", tmp_path / "pyproject.toml")
    target = tmp_path / path
    if before is None:
        target.unlink()
    else:
        original = target.read_text()
        assert before in original
        target.write_text(original.replace(before, after))
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "devtools/check_distribution_inputs.py"),
            "--suite-root",
            str(suite_root),
            "--root",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert diagnostic in result.stdout + result.stderr
