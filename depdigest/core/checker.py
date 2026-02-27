from importlib.util import find_spec
from functools import lru_cache
from typing import List, Dict, Any
import json
import logging
from smonitor import signal

logger = logging.getLogger(__name__)
GET_INFO_SCHEMA_VERSION = "1.0"


def _default_package_name(module_name: str) -> str:
    return module_name.split(".")[0]

@lru_cache(maxsize=None)
def is_installed(module_name: str) -> bool:
    """Check if a module is installed (cached)."""
    try:
        return find_spec(module_name) is not None
    except (ImportError, ModuleNotFoundError):
        return False

@signal(tags=["dependency"], exception_level="DEBUG")
def check_dependency(module_name: str, pypi_name: str = None, caller: str = None, exception_class: type = ImportError):
    """
    Check if a dependency is installed. Raises the specified exception if missing.
    """
    if not is_installed(module_name):
        install_name = pypi_name or _default_package_name(module_name)
        conda_name = _default_package_name(module_name)
        lib_name = pypi_name or module_name
        from smonitor.integrations import emit_from_catalog, merge_extra
        from .._private.smonitor.catalog import CATALOG, PACKAGE_ROOT, META

        try:
            emit_from_catalog(
                CATALOG["missing_dependency"],
                package_root=PACKAGE_ROOT,
                extra=merge_extra(META, {
                    "library": lib_name,
                    "caller": caller or "",
                    "pip_install": f"pip install {install_name}",
                    "conda_install": f"conda install -c conda-forge {conda_name}",
                }),
            )
        except Exception as emit_error:
            logger.warning(
                "SMonitor emission failed in check_dependency: signal=missing_dependency caller=%s library=%s error=%s",
                caller or "",
                lib_name,
                emit_error,
            )

        msg = f"The library '{module_name}' is required"
        if caller:
            msg += f" for '{caller}'"
        if install_name != module_name:
            msg += f". Install package '{install_name}'."
        else:
            msg += "."
        msg += (
            f"\nInstall with:\n"
            f"  conda install -c conda-forge {conda_name}\n"
            f"  pip install {install_name}"
        )
        if META.get("doc_url"):
            msg += f"\nDocumentation: {META['doc_url']}"

        try:
            raise exception_class(library=lib_name, caller=caller, message=msg)
        except TypeError:
            try:
                raise exception_class(library=lib_name, caller=caller)
            except TypeError:
                raise exception_class(msg)

def get_info(module_path: str, format: str = "table") -> Any:
    """
    Return dependency information for a given package root.

    Parameters
    ----------
    module_path
        Package root or module path used to resolve `_depdigest.py`.
    format
        One of:
        - "table": legacy row-oriented output (default).
        - "dict": structured dictionary output.
        - "json": JSON string of the structured dictionary output.
    """
    valid_formats = {"table", "dict", "json"}
    if format not in valid_formats:
        raise ValueError("Unsupported format. Use one of: 'table', 'dict', 'json'.")

    from .config import resolve_config
    cfg = resolve_config(module_path)

    deps = []
    for key, info in sorted(cfg.libraries.items(), key=lambda item: item[0]):
        default_name = _default_package_name(key)
        pypi_name = info.get("pypi", default_name)
        conda_name = info.get("conda", default_name)
        installed = is_installed(key)
        deps.append(
            {
                "library": key,
                "installed": installed,
                "status": "installed" if installed else "missing",
                "type": info.get("type", "soft"),
                "package_name": {
                    "pypi": pypi_name,
                    "conda": conda_name,
                },
                "install": {
                    "pypi": f"pip install {pypi_name}",
                    "conda": f"conda install -c conda-forge {conda_name}",
                },
            }
        )

    output = {
        "schema": {
            "name": "depdigest.get_info",
            "version": GET_INFO_SCHEMA_VERSION,
        },
        "module_path": module_path,
        "dependency_count": len(deps),
        "installed_count": sum(1 for dep in deps if dep["installed"]),
        "missing_count": sum(1 for dep in deps if not dep["installed"]),
        "dependencies": deps,
    }

    if format == "table":
        rows = []
        for dep in deps:
            rows.append(
                {
                    "Library": dep["library"],
                    "Status": "Installed" if dep["installed"] else "Not Installed",
                    "Type": dep["type"].capitalize(),
                    "Install (PyPI)": dep["install"]["pypi"],
                    "Install (Conda)": dep["install"]["conda"],
                }
            )
        return rows
    if format == "dict":
        return output
    if format == "json":
        return json.dumps(output, indent=2, sort_keys=True)
