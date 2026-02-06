from .core.checker import is_installed, check_dependency, get_info
from .core.decorator import dep_digest
from .core.loader import LazyRegistry
from .core.config import DepConfig, resolve_config, register_package_config

from ._private.smonitor import ensure_configured as _ensure_smonitor_configured

_ensure_smonitor_configured()

__all__ = [
    'is_installed',
    'check_dependency',
    'get_info',
    'dep_digest',
    'LazyRegistry',
    'DepConfig',
    'resolve_config',
    'register_package_config',
]
