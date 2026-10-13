"""Keep bootstrap previews and rejected activation away from caller resources."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(
    os.name == "nt" or shutil.which("bash") is None,
    reason="POSIX Bash bootstrap custody; Windows shell execution is not qualified",
)


def _workspace(tmp_path):
    repo = tmp_path / "source with spaces"
    tools = repo / "devtools"
    tools.mkdir(parents=True)
    script = tools / "start_dev_env.sh"
    shutil.copyfile(ROOT / "devtools/start_dev_env.sh", script)
    profile = tools / "conda-envs/development_env.yaml"
    profile.parent.mkdir()
    profile.write_text("dependencies:\n  - python=3.14\n")
    caller = tmp_path / "caller with spaces"
    caller.mkdir()
    sentinel = caller / "keep"
    sentinel.write_text("caller-owned")
    binaries = tmp_path / "bin"
    binaries.mkdir()
    (binaries / "python").symlink_to(sys.executable)
    log = caller / "manager.jsonl"
    base = tmp_path / "manager-base"
    activation = base / "etc/profile.d/conda.sh"
    activation.parent.mkdir(parents=True)
    activation.write_text("# Controlled activation; no real environment is changed.\n")
    stub = binaries / "manager.py"
    stub.write_text(
        "import json, os, pathlib, sys\n"
        "args = sys.argv[1:]\n"
        "with pathlib.Path(os.environ['BOOTSTRAP_LOG']).open('a') as stream:\n"
        " stream.write(json.dumps({'manager': pathlib.Path(sys.argv[0]).name, "
        "'args': args, 'cwd': os.getcwd()}) + '\\n')\n"
        "if args == ['info', '--base']:\n"
        " print(os.environ['BOOTSTRAP_BASE'])\n"
        "if 'create' in args or 'update' in args:\n"
        " raise SystemExit(int(os.environ.get('BOOTSTRAP_EXIT', '0')))\n"
    )
    for manager in ("conda", "mamba", "micromamba"):
        command = binaries / manager
        command.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{stub}" "$@"\n')
        command.chmod(0o700)
    env = dict(
        os.environ,
        PATH=f"{binaries}:/usr/bin:/bin",
        BOOTSTRAP_LOG=str(log),
        BOOTSTRAP_BASE=str(base),
        REGISTER_KERNEL="0",
    )
    env.pop("USER_ENV_YAML", None)
    return script, repo, caller, sentinel, log, env


@pytest.mark.parametrize("explicit", [False, True])
@pytest.mark.parametrize("sourced", [False, True])
def test_print_preview_preserves_caller_without_running_tools(
    tmp_path, explicit, sourced
):
    script, _, caller, sentinel, log, env = _workspace(tmp_path)
    args = ["--mode", "print"] if explicit else []
    args += ["--env-name", "caller-env", "--python", "3.14", "--no-kernel"]
    command = (
        ["bash", "-c", 'source "$@"', "preview", str(script), *args]
        if sourced
        else ["bash", str(script), *args]
    )
    result = subprocess.run(
        command, cwd=caller, env=env, capture_output=True, text=True, timeout=20
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert not log.exists(), "preview invoked a manager, installer or activation"
    assert sentinel.read_text() == "caller-owned"
    assert "--mode persist" in result.stdout
    assert "caller-env" in result.stdout and "3.14" in result.stdout


def test_unsourced_persist_refuses_before_running_tools(tmp_path):
    script, _, caller, sentinel, log, env = _workspace(tmp_path)
    result = subprocess.run(
        ["bash", str(script), "--mode", "persist"],
        cwd=caller,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode != 0
    assert "source" in result.stdout.lower()
    assert not log.exists(), "rejected activation changed caller resources"
    assert sentinel.read_text() == "caller-owned"


@pytest.mark.parametrize("manager", ["micromamba", "mamba", "conda"])
def test_explicit_setup_installs_own_source_and_keeps_caller(tmp_path, manager):
    script, repo, caller, sentinel, log, env = _workspace(tmp_path)
    for alternative in ("micromamba", "mamba", "conda"):
        if alternative != manager:
            (Path(env["PATH"].split(":")[0]) / alternative).unlink()
    result = subprocess.run(
        ["bash", "-c", 'source "$@"', "setup", str(script), "--mode", "persist"],
        cwd=caller,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    calls = [json.loads(line)["args"] for line in log.read_text().splitlines()]
    installs = [args for args in calls if "--editable" in args]
    assert len(installs) == 1
    assert installs[0][-1] == str(repo), "setup installed the caller's directory"
    assert sentinel.read_text() == "caller-owned"


def test_failed_setup_does_not_install_after_manager_failure(tmp_path):
    script, _, caller, sentinel, log, env = _workspace(tmp_path)
    env["BOOTSTRAP_EXIT"] = "23"
    result = subprocess.run(
        [
            "bash",
            "-c",
            'source "$@"',
            "setup",
            str(script),
            "--mode",
            "persist",
            "--python",
            "3.14",
        ],
        cwd=caller,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 23, result.stdout + result.stderr
    calls = [json.loads(line)["args"] for line in log.read_text().splitlines()]
    assert not any("--editable" in args for args in calls)
    assert sentinel.read_text() == "caller-owned"
