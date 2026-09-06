from importlib.metadata import PackageNotFoundError, version

from .core.checker import check_dependency, get_info, is_installed
from .core.config import (
    DepConfig,
    clear_package_configs,
    register_package_config,
    resolve_config,
    temporary_package_config,
    unregister_package_config,
)
from .core.decorator import dep_digest
from .core.loader import LazyRegistry

try:
    __version__ = version("depdigest")
except PackageNotFoundError:
    # Package is not installed
    try:
        from ._version import __version__
    except ImportError:
        __version__ = "0.0.0+unknown"

from smonitor.integrations import ensure_configured as _ensure_smonitor_configured

from ._private.smonitor import PACKAGE_ROOT as _SMONITOR_PACKAGE_ROOT

_ensure_smonitor_configured(_SMONITOR_PACKAGE_ROOT)

__all__ = [
    "is_installed",
    "check_dependency",
    "get_info",
    "dep_digest",
    "LazyRegistry",
    "DepConfig",
    "resolve_config",
    "register_package_config",
    "unregister_package_config",
    "temporary_package_config",
    "clear_package_configs",
]
