import os
import ast
from collections import defaultdict
from typing import Set, List, Dict, Tuple

def check_top_level_imports(file_path: str, soft_deps: Set[str]) -> List[Tuple[int, str]]:
    """
    Scans a python file for top-level imports of given soft dependencies.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            return []

    violations = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split('.')[0]
                if root_module in soft_deps:
                    violations.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_module = node.module.split('.')[0]
                if root_module in soft_deps:
                    violations.append((node.lineno, node.module))
    return violations

def validate_codebase(src_root: str, soft_deps: Set[str], exempt_files: Set[str] = None, exempt_dirs: List[str] = None) -> Dict[str, List[Tuple[int, str]]]:
    """
    Walks through a codebase and detects violations of the lazy-import rule.
    """
    all_violations = defaultdict(list)
    exempt_files = exempt_files or set()
    exempt_dirs = exempt_dirs or []

    for root, _, files in os.walk(src_root):
        for file in files:
            if not file.endswith('.py'):
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
