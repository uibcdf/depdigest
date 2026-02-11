from importlib.util import find_spec
from functools import lru_cache
from typing import List, Dict, Any

@lru_cache(maxsize=None)
def is_installed(module_name: str) -> bool:
    """Check if a module is installed (cached)."""
    try:
        return find_spec(module_name) is not None
    except (ImportError, ModuleNotFoundError):
        return False

def check_dependency(module_name: str, pypi_name: str = None, caller: str = None, exception_class: type = ImportError):
    """
    Check if a dependency is installed. Raises the specified exception if missing.
    """
    if not is_installed(module_name):
        lib_name = pypi_name or module_name
        from smonitor.integrations import emit_from_catalog, merge_extra
        from .._private.smonitor.catalog import CATALOG, PACKAGE_ROOT, META

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

def get_info(module_path: str) -> List[Dict[str, Any]]:
    """
    Return raw dependency information for a given package root.
    """
    from .config import resolve_config
    cfg = resolve_config(module_path)
    
    rows = []
    for key, info in cfg.libraries.items():
        pypi_name = info.get('pypi', key)
        conda_name = info.get('conda', key)
        installed = is_installed(key)
        rows.append({
            'Library': key,
            'Status': 'Installed' if installed else 'Not Installed',
            'Type': info.get('type', 'soft').capitalize(),
            'Install (PyPI)': f"pip install {pypi_name}",
            'Install (Conda)': f"conda install -c conda-forge {conda_name}"
        })
    return rows
