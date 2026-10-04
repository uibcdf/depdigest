import ast
import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def _typing_guard_truth(node, modules, flags):
    if isinstance(node, ast.Name) and node.id in flags:
        return False
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id in modules
        and node.attr == "TYPE_CHECKING"
    ):
        return False
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        value = _typing_guard_truth(node.operand, modules, flags)
        return None if value is None else not value
    return None


def _eager_nodes(node, guards=None):
    """Visit source scopes that can execute on import; never enter a function."""
    yield node
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
        return
    if isinstance(node, ast.If) and guards is not None:
        truth = _typing_guard_truth(node.test, *guards)
        if truth is not None:
            for statement in node.body if truth else node.orelse:
                yield from _eager_nodes(statement, guards)
            return
    for child in ast.iter_child_nodes(node):
        yield from _eager_nodes(child, guards)


def _typing_guard_names(tree):
    """Recognize explicit typing imports conservatively in unrebound source."""
    modules, flags, rebound = set(), set(), set()
    wildcard = False
    for node in _eager_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                if alias.name == "typing":
                    modules.add(name)
                else:
                    rebound.add(name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                if (
                    node.level == 0
                    and node.module == "typing"
                    and alias.name == "TYPE_CHECKING"
                ):
                    flags.add(name)
                elif alias.name == "*":
                    wildcard = True
                else:
                    rebound.add(name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            rebound.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            rebound.add(node.name)
        elif isinstance(node, (ast.ExceptHandler, ast.MatchAs, ast.MatchStar)):
            if node.name:
                rebound.add(node.name)
        elif isinstance(node, ast.MatchMapping) and node.rest:
            rebound.add(node.rest)
        elif (
            isinstance(node, ast.Attribute)
            and isinstance(node.ctx, (ast.Store, ast.Del))
            and isinstance(node.value, ast.Name)
            and node.attr == "TYPE_CHECKING"
        ):
            rebound.add(node.value.id)
    if wildcard:
        return set(), set()
    rebound.update(modules & flags)
    return modules - rebound, flags - rebound


def check_top_level_imports(
    file_path: str, soft_deps: Set[str]
) -> List[Tuple[int, str]]:
    """
    Find imports in eager source scopes, including module/class control flow.

    Function bodies are delayed. Simple guards using explicit, unrebound typing
    TYPE_CHECKING imports (including aliases and negation) exclude their typing
    branch. Other conditions are conservatively scanned without execution.
    Syntax-error files retain the historical empty result.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            return []

    violations = []
    guards = _typing_guard_names(tree)
    for node in _eager_nodes(tree, guards):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split(".")[0]
                if root_module in soft_deps:
                    violations.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_module = node.module.split(".")[0]
                if root_module in soft_deps:
                    violations.append((node.lineno, node.module))
    return violations


def validate_codebase(
    src_root: str,
    soft_deps: Set[str],
    exempt_files: Set[str] = None,
    exempt_dirs: List[str] = None,
) -> Dict[str, List[Tuple[int, str]]]:
    """
    Walks through a codebase and detects violations of the lazy-import rule.
    """
    all_violations = defaultdict(list)
    exempt_files = exempt_files or set()
    exempt_dirs = exempt_dirs or []

    for root, _, files in os.walk(src_root):
        for file in files:
            if not file.endswith(".py"):
                continue

            file_path = os.path.join(root, file)

            # Check exemptions
            if file_path in exempt_files:
                continue
            if any(file_path.startswith(d) for d in exempt_dirs):
                continue

            violations = check_top_level_imports(file_path, soft_deps)
            if violations:
                all_violations[file_path] = violations

    return dict(all_violations)
