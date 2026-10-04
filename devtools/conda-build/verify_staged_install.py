"""Verify an immutable staged Conda candidate and its clean installation."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE = "depdigest"
PUBLIC_DEPENDENCY = "smonitor"
PUBLIC_DEPENDENCY_VERSION = "0.16.0"
PUBLIC_DEPENDENCY_BUILD = "py_1"
STAGING_CHANNEL = "https://conda.anaconda.org/uibcdf/label/staging/noarch"
PUBLIC_CHANNEL = "https://conda.anaconda.org/uibcdf/noarch"
PRODUCER_WORKFLOW = ".github/workflows/build_and_upload_conda_packages.yaml"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_identity(sha: str, version: str, build_number: int, run_id: int) -> None:
    _require(bool(re.fullmatch(r"[0-9a-f]{40}", sha)), "Invalid candidate SHA")
    _require(
        bool(re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version)),
        "Invalid candidate version",
    )
    _require(build_number >= 0, "Invalid build number")
    _require(run_id > 0, "Invalid staging run ID")


def verify_receipts(
    run: dict,
    evidence_dir: Path,
    sha: str,
    version: str,
    build_number: int,
    run_id: int,
) -> str:
    """Return the package digest only if the run and both receipts agree."""
    validate_identity(sha, version, build_number, run_id)
    _require(run.get("id") == run_id, "Staging run ID mismatch")
    _require(run.get("event") == "workflow_dispatch", "Not a staging dispatch")
    _require(run.get("conclusion") == "success", "Staging run did not succeed")
    _require(run.get("head_sha") == sha, "Staging run built a different commit")
    _require(run.get("path") == PRODUCER_WORKFLOW, "Unexpected producer workflow")
    attempt = run.get("run_attempt")
    _require(isinstance(attempt, int) and attempt > 0, "Invalid run attempt")

    routes = list(evidence_dir.rglob("depdigest-conda-route.json"))
    producers = list(evidence_dir.rglob("gh-run-receptor-events.json"))
    _require(len(routes) == 1 and len(producers) == 1, "Expected exactly two receipts")
    route = _read_json(routes[0])
    producer = _read_json(producers[0])
    _require(
        route.get("schema") == "depdigest.conda-route@1", "Unexpected route schema"
    )
    _require(route.get("candidate_sha") == sha, "Route commit mismatch")
    _require(route.get("version") == version, "Route version mismatch")
    _require(route.get("route") == "staged", "Not a staged release route")
    _require(route.get("gates"), "No CI gate recorded")
    _require(
        producer.get("schema") == "gh-run-receptor.events@1", "Unexpected event schema"
    )
    subject = producer.get("subject", {})
    _require(
        subject.get("repository") == "uibcdf/depdigest", "Wrong producer repository"
    )
    _require(subject.get("head_sha") == sha, "Producer commit mismatch")
    _require(subject.get("run_id") == run_id, "Producer run mismatch")
    _require(subject.get("run_attempt") == attempt, "Producer attempt mismatch")
    _require(
        subject.get("job_key") == "conda_deployment_with_new_tag", "Wrong producer job"
    )
    events = producer.get("events", [])
    _require(len(events) == 1, "Expected exactly one package event")
    event = events[0]
    filename = f"{PACKAGE}-{version}-py_{build_number}.tar.bz2"
    _require(event.get("kind") == "conda.package", "Wrong artifact kind")
    _require(event.get("artifact") == filename, "Wrong artifact filename")
    _require(event.get("platform") == "noarch", "Wrong artifact platform")
    _require(event.get("build") == "success", "Build failed")
    _require(event.get("upload") == "success", "Upload failed")
    digest = event.get("sha256")
    _require(
        isinstance(digest, str) and bool(re.fullmatch(r"[0-9a-f]{64}", digest)),
        "Invalid digest",
    )
    return digest


def verify_installed(
    prefix: Path, sha256: str, version: str, build_number: int, python_version: str
) -> None:
    """Check the installed bytes, source channels, interpreter, import, and CLI."""
    _require(bool(re.fullmatch(r"[0-9a-f]{64}", sha256)), "Invalid expected digest")
    _require(
        f"{sys.version_info.major}.{sys.version_info.minor}" == python_version,
        "Wrong Python",
    )
    _require(prefix.resolve() == Path(sys.prefix).resolve(), "Wrong environment prefix")
    build = f"py_{build_number}"
    package_record = _read_json(
        prefix / "conda-meta" / f"{PACKAGE}-{version}-{build}.json"
    )
    dependency_record = _read_json(
        prefix
        / "conda-meta"
        / f"{PUBLIC_DEPENDENCY}-{PUBLIC_DEPENDENCY_VERSION}-{PUBLIC_DEPENDENCY_BUILD}.json"
    )
    _require(package_record.get("name") == PACKAGE, "Wrong package record")
    _require(
        package_record.get("version") == version, "Wrong installed package version"
    )
    _require(package_record.get("build") == build, "Wrong installed package build")
    _require(package_record.get("subdir") == "noarch", "Package not noarch")
    _require(
        package_record.get("sha256") == sha256, "Installed package digest mismatch"
    )
    _require(
        package_record.get("url")
        == f"{STAGING_CHANNEL}/{PACKAGE}-{version}-{build}.tar.bz2",
        "Wrong package URL",
    )
    _require(
        dependency_record.get("name") == PUBLIC_DEPENDENCY, "Wrong dependency record"
    )
    _require(
        dependency_record.get("version") == PUBLIC_DEPENDENCY_VERSION,
        "Wrong dependency version",
    )
    _require(
        dependency_record.get("build") == PUBLIC_DEPENDENCY_BUILD,
        "Wrong dependency build",
    )
    _require(
        dependency_record.get("url")
        == f"{PUBLIC_CHANNEL}/{PUBLIC_DEPENDENCY}-{PUBLIC_DEPENDENCY_VERSION}-{PUBLIC_DEPENDENCY_BUILD}.tar.bz2",
        "Dependency not from public channel",
    )

    _require(
        importlib.metadata.version(PACKAGE) == version, "Distribution version mismatch"
    )
    import depdigest

    _require(depdigest.__version__ == version, "Imported module version mismatch")
    _require(
        Path(depdigest.__file__).resolve().is_relative_to(prefix.resolve()),
        "Imported the source checkout instead of the installed package",
    )
    verify_launcher(prefix)
    if tuple(map(int, version.split("."))) >= (0, 12, 0):
        verify_optional_engine_contract()
    if tuple(map(int, version.split("."))) >= (0, 13, 0):
        verify_audit_contract()


def verify_audit_contract() -> None:
    """Check expanded scope, typing exclusion and exit behavior in installed CLI."""
    with tempfile.TemporaryDirectory() as temporary:
        source = Path(temporary) / "pkg"
        source.mkdir()
        path = source / "__init__.py"
        path.write_text(
            "from typing import TYPE_CHECKING\n"
            "if TYPE_CHECKING:\n"
            "    import release_typing_only\n"
            "if True:\n"
            "    import release_eager\n"
            "class Adapter:\n"
            "    import release_class\n"
            "def delayed():\n"
            "    import release_delayed\n",
            encoding="utf-8",
        )
        arguments = [
            sys.executable,
            "-m",
            PACKAGE,
            "audit",
            "--src-root",
            str(source),
            "--soft-deps",
            "release_typing_only,release_eager,release_class,release_delayed",
            "--json",
        ]
        expected = {
            str(path): [
                {"line": 5, "module": "release_eager"},
                {"line": 7, "module": "release_class"},
            ]
        }
        payloads = []
        for options, expected_status in (([], 1), (["--allow-violations"], 0)):
            result = subprocess.run(
                [*arguments, *options],
                cwd=temporary,
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
            _require(result.returncode == expected_status, "Wrong audit exit status")
            payload = json.loads(result.stdout)
            _require(payload.get("violation_count") == 2, "Wrong audit finding count")
            _require(payload.get("violations") == expected, "Wrong audit scope/lines")
            payloads.append(payload)
        _require(payloads[0] == payloads[1], "Allow-violations hid audit findings")


def verify_optional_engine_contract() -> None:
    """Exercise the 0.12.0 contract through the already verified installed import."""
    import depdigest

    with tempfile.TemporaryDirectory() as temporary:
        missing = str(Path(temporary) / "absent_release_engine")
        try:
            depdigest.check_dependency(
                "release_available",
                kind="executable",
                executable=sys.executable,
                pypi_name=None,
                conda_name=None,
            )
        except ImportError as error:
            raise ValueError("Ignoring the configured executable") from error
        libraries = {
            "release_available": {
                "type": "soft",
                "kind": "executable",
                "executable": sys.executable,
                "pypi": None,
                "conda": None,
            },
            "release_missing": {
                "type": "soft",
                "kind": "executable",
                "executable": missing,
                "pypi": None,
                "conda": "fpocket",
                "channel": "conda-forge",
            },
        }
        with depdigest.temporary_package_config(
            "depdigest_release_gate", depdigest.DepConfig(libraries=libraries)
        ):
            inventory = depdigest.get_info("depdigest_release_gate", format="dict")
        rows = {row["library"]: row for row in inventory["dependencies"]}
        _require(rows["release_available"]["installed"], "Wrong executable inventory")
        _require(not rows["release_missing"]["installed"], "Wrong missing inventory")
        _require(
            all(row["install"]["pypi"] is None for row in rows.values())
            and rows["release_available"]["install"]["conda"] is None,
            "Invented disabled installer in the installed inventory",
        )
        command = "conda install -c conda-forge fpocket"
        _require(
            rows["release_missing"]["install"]["conda"] == command,
            "Installed inventory ignored declared channel",
        )
        try:
            depdigest.check_dependency(
                "release_missing",
                kind="executable",
                executable=missing,
                pypi_name=None,
                conda_name="fpocket",
                conda_channel="conda-forge",
            )
        except ImportError as error:
            _require(
                command in str(error) and "pip install" not in str(error),
                "Installed diagnostic ignored disabled installer or channel",
            )
        else:
            raise ValueError("Installed guard accepted a missing executable")


def verify_launcher(prefix: Path) -> None:
    """Run the command installed by Conda, including its Windows launcher."""
    launcher = shutil.which(PACKAGE)
    _require(launcher is not None, "Installed depdigest launcher is missing")
    _require(
        Path(launcher).resolve().is_relative_to(prefix.resolve()),
        "depdigest launcher is outside the installed environment",
    )
    command = subprocess.run(
        [launcher, "--help"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    _require(command.returncode == 0, f"Installed launcher failed: {command.stderr}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)
    receipts = subparsers.add_parser("receipts")
    receipts.add_argument("--run", type=Path, required=True)
    receipts.add_argument("--evidence-dir", type=Path, required=True)
    receipts.add_argument("--sha", required=True)
    receipts.add_argument("--version", required=True)
    receipts.add_argument("--build-number", type=int, required=True)
    receipts.add_argument("--run-id", type=int, required=True)
    installed = subparsers.add_parser("installed")
    installed.add_argument("--prefix", type=Path, required=True)
    installed.add_argument("--sha256", required=True)
    installed.add_argument("--version", required=True)
    installed.add_argument("--build-number", type=int, required=True)
    installed.add_argument("--python-version", required=True)
    args = parser.parse_args()
    if args.mode == "receipts":
        digest = verify_receipts(
            _read_json(args.run),
            args.evidence_dir,
            args.sha,
            args.version,
            args.build_number,
            args.run_id,
        )
        print(digest)
    else:
        verify_installed(
            args.prefix,
            args.sha256,
            args.version,
            args.build_number,
            args.python_version,
        )
        print(
            "PASS: exact staged package, public dependency, import, CLI, "
            "and version-applicable optional-engine/audit contracts"
        )


if __name__ == "__main__":
    main()
