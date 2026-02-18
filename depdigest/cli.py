import argparse
import json
from typing import Iterable, List, Set

from .utils.ast_tools import validate_codebase


def _collect_soft_deps(values: Iterable[str]) -> Set[str]:
    deps: Set[str] = set()
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                deps.add(item)
    return deps


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="depdigest")
    subparsers = parser.add_subparsers(dest="command")

    audit = subparsers.add_parser(
        "audit",
        help="Detect top-level imports of soft dependencies.",
    )
    audit.add_argument(
        "--src-root",
        default=".",
        help="Source root to scan (default: current directory).",
    )
    audit.add_argument(
        "--soft-deps",
        action="append",
        required=True,
        help="Soft dependency names (repeatable or comma-separated).",
    )
    audit.add_argument(
        "--exempt-file",
        action="append",
        default=[],
        help="File path to exempt from checks (repeatable).",
    )
    audit.add_argument(
        "--exempt-dir",
        action="append",
        default=[],
        help="Directory prefix to exempt from checks (repeatable).",
    )
    audit.add_argument(
        "--json",
        action="store_true",
        help="Emit results as JSON.",
    )
    audit.add_argument(
        "--allow-violations",
        action="store_true",
        help="Return exit code 0 even when violations are found.",
    )
    return parser


def _run_audit(args: argparse.Namespace) -> int:
    soft_deps = _collect_soft_deps(args.soft_deps)
    if not soft_deps:
        raise SystemExit("At least one soft dependency must be provided.")

    violations = validate_codebase(
        src_root=args.src_root,
        soft_deps=soft_deps,
        exempt_files=set(args.exempt_file),
        exempt_dirs=args.exempt_dir,
    )

    if args.json:
        payload = {
            "src_root": args.src_root,
            "soft_deps": sorted(soft_deps),
            "violations": {
                path: [{"line": line, "module": module} for line, module in items]
                for path, items in sorted(violations.items())
            },
            "violation_count": sum(len(v) for v in violations.values()),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if not violations:
            print("No top-level soft-dependency imports found.")
        else:
            print("Top-level soft-dependency import violations:")
            for path in sorted(violations):
                print(f"- {path}")
                for line, module in violations[path]:
                    print(f"  line {line}: {module}")

    has_violations = bool(violations)
    if has_violations and not args.allow_violations:
        return 1
    return 0


def main(argv: List[str] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "audit":
        return _run_audit(args)

    parser.print_help()
    return 0

