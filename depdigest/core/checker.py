from importlib.util import find_spec
from functools import lru_cache
from typing import List, Dict, Any
import json
import logging
from smonitor import signal

logger = logging.getLogger(__name__)

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
                    "pip_install": f"pip install {lib_name}",
                    "conda_install": f"conda install -c conda-forge {lib_name}",
                }),
            )
        except Exception as emit_error:
            logger.warning(
                "SMonitor emission failed in check_dependency: signal=missing_dependency caller=%s library=%s error=%s",
                caller or "",
                lib_name,
                emit_error,
            )
        msg = f"The library '{lib_name}' is required"
        if caller:
            msg += f" for '{caller}'"
        msg += ". Please install it."
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
    for key, info in cfg.libraries.items():
        pypi_name = info.get("pypi", key)
        conda_name = info.get("conda", key)
        installed = is_installed(key)
        deps.append(
            {
                "library": key,
                "installed": installed,
                "status": "Installed" if installed else "Not Installed",
                "type": info.get("type", "soft"),
                "install": {
                    "pypi": f"pip install {pypi_name}",
                    "conda": f"conda install -c conda-forge {conda_name}",
                },
            }
        )

    output = {
        "module_path": module_path,
        "dependencies": deps,
    }

    if format == "table":
        rows = []
        for dep in deps:
            rows.append(
                {
                    "Library": dep["library"],
                    "Status": dep["status"],
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
