from importlib.util import find_spec
from functools import lru_cache

@lru_cache(maxsize=None)
def is_installed(module_name: str) -> bool:
    """Check if a module is installed (cached)."""
    # module_name should be the importable name (e.g. 'openmm')
    return find_spec(module_name) is not None

def check_dependency(module_name: str, pypi_name: str = None, caller: str = None, exception_class: type = ImportError):
    """
    Check if a dependency is installed. Raises the specified exception if missing.
    """
    if not is_installed(module_name):
        lib_name = pypi_name or module_name
        msg = f"The library '{lib_name}' is required"
        if caller:
            msg += f" for '{caller}'"
        msg += ". Please install it."
        raise exception_class(msg)
