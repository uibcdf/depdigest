"""Delegate dependency and exact-candidate controls to the pinned suite provider."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = "devtools/dependency_routes.toml"


def checked_tool(suite_root: Path, commit: str) -> Path:
    """Refuse a changed or dirty provider before executing its shared operation."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("shared dependency tool needs a reviewed full commit")
    suite_root = suite_root.resolve()
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=suite_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if head != commit:
        raise ValueError(f"shared tool checkout is {head}; expected {commit}")
    changed = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "devtools"],
        cwd=suite_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if changed:
        raise ValueError("shared tool's devtools inputs are modified or untracked")
    tool = suite_root / "devtools/scripts/dependency_routes.py"
    if not tool.is_file():
        raise ValueError("pinned checkout does not provide dependency_routes.py")
    return tool


def source_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()


def required_jobs(plan: dict) -> dict:
    workflows, jobs = plan["required_workflows"], plan.get("gate_jobs", {})
    if (
        not workflows
        or set(workflows) != set(jobs)
        or any(not jobs[path] for path in workflows)
    ):
        raise ValueError("Every required workflow needs executed-job requirements")
    return jobs


def require_qualification(result: dict, *, candidate: bool) -> None:
    expected = "declared-only" if candidate else "declared-and-installed-public-bounds"
    if result.get("qualification") != expected:
        raise ValueError(
            f"Unexpected dependency qualification: {result.get('qualification')}"
        )


NATIVE_READER = """
import json, os, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root), str(root / 'devtools/scripts')]
from preflight_conda_release import acquire_gates
assert pathlib.Path(acquire_gates.__code__.co_filename).resolve() == root / 'devtools/scripts/preflight_conda_release.py'
request = json.load(sys.stdin)
try:
    result = acquire_gates(request['repository'], request['candidate'], request['workflows'], os.environ.get('GH_TOKEN', ''), request['jobs'])
except (ValueError, OSError, KeyError) as error:
    print(f'Native source gates rejected: {error}', file=sys.stderr)
    raise SystemExit(1)
print(json.dumps(result))
"""


def verify_candidate(root: Path, suite_root: Path, candidate: str, plan: dict) -> list:
    if not re.fullmatch(r"[0-9a-f]{40}", candidate) or source_head(root) != candidate:
        raise ValueError("Exact candidate differs from the checked-out source")
    subprocess.run(["git", "diff", "--quiet", "HEAD", "--"], cwd=root, check=True)
    jobs = required_jobs(plan)
    request = {
        "repository": "uibcdf/depdigest",
        "candidate": candidate,
        "workflows": plan["required_workflows"],
        "jobs": jobs,
    }
    response = subprocess.run(
        [sys.executable, "-B", "-c", NATIVE_READER, str(suite_root.resolve())],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        check=False,
    )
    if response.returncode:
        raise ValueError(
            response.stderr.strip() or "Native source gate acquisition failed"
        )
    return json.loads(response.stdout)


def installed_jobs() -> dict:
    """Owner profile: existing producer check and exact-file smoke in twelve cells."""
    jobs = {
        "Verify the immutable producer evidence": [
            "Download and verify the exact staging run receipts"
        ]
    }
    for runner in ("ubuntu-latest", "macos-latest", "windows-latest"):
        for minor in ("3.11", "3.12", "3.13", "3.14"):
            jobs[f"Install {runner} / Python {minor}"] = [
                "Create a clean environment from the exact staged build",
                "Verify installed artifact and smoke test outside the source checkout",
            ]
    return jobs


INSTALLED_READER = """
import json, os, pathlib, sys
root = pathlib.Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root), str(root / 'devtools/scripts')]
from verify_installed_matrix import verify_native_gate
assert pathlib.Path(verify_native_gate.__code__.co_filename).resolve() == root / 'devtools/scripts/verify_installed_matrix.py'
request = json.load(sys.stdin)
result = verify_native_gate('uibcdf/depdigest', request['run_id'], request['candidate'], '.github/workflows/test_staged_conda_package.yaml', request['jobs'], os.environ.get('GH_TOKEN', ''), title=request['title'], exact_jobs=True, event='workflow_dispatch')
print(json.dumps(result))
"""


def verify_installed(
    suite_root: Path, run_id: int, candidate: str, plan: dict, digest: str
) -> dict:
    if run_id < 1 or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ValueError("Installed qualification needs a native run and exact SHA-256")
    filename = f"depdigest-{plan['version']}-py_{plan['build_number']}.tar.bz2"
    request = dict(
        run_id=run_id,
        candidate=candidate,
        jobs=installed_jobs(),
        title=f"Installed {filename} {digest}",
    )
    response = subprocess.run(
        [sys.executable, "-B", "-c", INSTALLED_READER, str(suite_root.resolve())],
        input=json.dumps(request),
        capture_output=True,
        text=True,
        check=False,
    )
    if response.returncode:
        raise ValueError(response.stderr.strip() or "Installed gate acquisition failed")
    return dict(
        native=json.loads(response.stdout),
        filename=filename,
        sha256=digest,
        scope="exact-file-installed-smoke; not a full installed pytest suite",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite-root", required=True, type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--candidate-sha")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--version")
    parser.add_argument("--build-number", type=int)
    parser.add_argument("--installed-run-id", type=int)
    parser.add_argument("--sha256")
    args = parser.parse_args()
    try:
        inventory = tomllib.loads((args.root / INVENTORY).read_text())
        tool = checked_tool(args.suite_root, inventory["shared_tool"]["commit"])
        command = [
            sys.executable,
            "-B",
            str(tool),
            "--root",
            str(args.root),
            "--inventory",
            INVENTORY,
        ]
        if args.candidate_sha:
            command.append("--declared-only")
        response = subprocess.run(command, capture_output=True, text=True, check=False)
        if response.returncode:
            print(response.stdout + response.stderr, file=sys.stderr)
            return response.returncode
        proof = json.loads(response.stdout)
        require_qualification(proof, candidate=bool(args.candidate_sha))
        if (args.installed_run_id is not None or args.sha256) and not (
            args.candidate_sha and args.installed_run_id and args.sha256
        ):
            raise ValueError(
                "Installed qualification requires candidate, run ID and digest together"
            )
        if args.candidate_sha:
            plan = tomllib.loads(
                (args.root / "devtools/conda-build/release_plan.toml").read_text()
            )
            if (
                args.version != plan["version"]
                or args.build_number != plan["build_number"]
            ):
                raise ValueError(
                    "Candidate version/build differ from the committed recipe context"
                )
            proof["executed_source_gates"] = verify_candidate(
                args.root, args.suite_root, args.candidate_sha, plan
            )
            proof["candidate_sha"] = args.candidate_sha
            proof["qualification"] = "declared-and-executed-candidate-public-bounds"
        if args.installed_run_id:
            proof["installed_gate"] = verify_installed(
                args.suite_root,
                args.installed_run_id,
                args.candidate_sha,
                plan,
                args.sha256,
            )
        proof["provider_commit"] = inventory["shared_tool"]["commit"]
        if args.output:
            args.output.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
        print(
            f"Verified {len(proof['routes'])} distribution input routes: {proof['qualification']}"
        )
        return 0
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print(f"DepDigest dependency preflight rejected: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
