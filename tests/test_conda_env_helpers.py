"""Exercise helper exit status and owned files through real controlled children."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("operation", ["create", "update"])
@pytest.mark.parametrize("manager_exit", [0, 23])
@pytest.mark.parametrize("spaces", [False, True])
def test_manager_result_arguments_and_resource_custody(
    tmp_path, operation, manager_exit, spaces
):
    work = tmp_path / ("caller with spaces" if spaces else "caller")
    work.mkdir()
    private = tmp_path / "private"
    private.mkdir()
    receipt = work / "receipt.json"
    spec = work / "input.yaml"
    original = "dependencies:\n  - python =3.11\n  - pip\n"
    spec.write_text(original, encoding="utf-8")
    sentinel = work / "caller-environment"
    sentinel.mkdir()
    (sentinel / "keep").write_text("caller-owned", encoding="utf-8")
    stub = work / "manager.py"
    stub.write_text(
        "import json, os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "flag = '-f' if args[1] == 'create' else '--file'\n"
        "spec = pathlib.Path(args[args.index(flag) + 1]).resolve()\n"
        "receipt = {'argv': args, 'cwd': str(pathlib.Path.cwd()), "
        "'spec_path': str(spec), 'spec': spec.read_text()}\n"
        "pathlib.Path(os.environ['HELPER_RECEIPT']).write_text(json.dumps(receipt))\n"
        "raise SystemExit(int(os.environ['HELPER_EXIT']))\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        manager = work / "conda.cmd"
        manager.write_text(f'@"{sys.executable}" "{stub}" %*\n', encoding="utf-8")
    else:
        manager = work / "conda"
        manager.write_text(
            f'#!/bin/sh\nexec "{sys.executable}" "{stub}" "$@"\n',
            encoding="utf-8",
        )
        manager.chmod(0o700)
    env = dict(
        os.environ,
        CONDA_EXE=str(manager),
        HELPER_RECEIPT=str(receipt),
        HELPER_EXIT=str(manager_exit),
        TMPDIR=str(private),
        TEMP=str(private),
        TMP=str(private),
    )
    args = ["-n", "requested-env", "-p", "3.14"] if operation == "create" else []
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / f"devtools/conda-envs/{operation}_conda_env.py"),
            *args,
            str(spec),
        ],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == manager_exit, result.stdout + result.stderr
    facts = json.loads(receipt.read_text(encoding="utf-8"))
    if operation == "create":
        assert facts["argv"] == [
            "env",
            "create",
            "-n",
            "requested-env",
            "-f",
            "temp_script.yaml",
        ]
        created_spec = Path(facts["spec_path"])
        assert created_spec.parent.parent == private
        assert not created_spec.parent.exists()
        assert yaml.safe_load(facts["spec"])["dependencies"] == ["python 3.14*", "pip"]
    else:
        assert facts["argv"] == ["env", "update", "--file", str(spec), "--prune"]
        assert Path(facts["cwd"]) == work
    assert list(private.iterdir()) == []
    assert spec.read_text(encoding="utf-8") == original
    assert (sentinel / "keep").read_text(encoding="utf-8") == "caller-owned"
