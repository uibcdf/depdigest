from __future__ import annotations
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any, Dict, Optional, Type
from contextlib import contextmanager
from functools import lru_cache

@dataclass(frozen=True)
class DepConfig:
    libraries: Dict[str, Dict[str, str]] = field(default_factory=dict)
    mapping: Dict[str, str] = field(default_factory=dict)
    show_all_capabilities: bool = True
    exception_class: Type[Exception] = ImportError

_PACKAGE_CONFIGS: Dict[str, DepConfig] = {}

def register_package_config(package_name: str, config: DepConfig):
    """Manually register a configuration for a package root."""
    if not package_name or not isinstance(package_name, str):
        raise ValueError("package_name must be a non-empty string")
    if not isinstance(config, DepConfig):
        raise TypeError("config must be an instance of DepConfig")
    _PACKAGE_CONFIGS[package_name] = config
    resolve_config.cache_clear()

def unregister_package_config(package_name: str):
    """Remove a manually registered package configuration if present."""
    _PACKAGE_CONFIGS.pop(package_name, None)
    resolve_config.cache_clear()

def clear_package_configs():
    """Clear all manually registered configurations. Useful for testing."""
    _PACKAGE_CONFIGS.clear()
    resolve_config.cache_clear()

@contextmanager
def temporary_package_config(package_name: str, config: DepConfig):
    """
    Temporarily register a package config within a context.

    Restores previous state after context exit.
    """
    had_previous = package_name in _PACKAGE_CONFIGS
    previous = _PACKAGE_CONFIGS.get(package_name)
    register_package_config(package_name, config)
    try:
        yield
    finally:
        if had_previous:
            _PACKAGE_CONFIGS[package_name] = previous
        else:
            _PACKAGE_CONFIGS.pop(package_name, None)
        resolve_config.cache_clear()

@lru_cache(maxsize=128)
def resolve_config(module_path: Optional[str]) -> DepConfig:
    if not module_path:
        return DepConfig()

    package_root = module_path.split('.')[0]
    
    if package_root in _PACKAGE_CONFIGS:
        return _PACKAGE_CONFIGS[package_root]

    config_module_path = f"{package_root}._depdigest"
    try:
        module = import_module(config_module_path)
        return DepConfig(
            libraries=getattr(module, "LIBRARIES", {}),
            mapping=getattr(module, "MAPPING", {}),
            show_all_capabilities=getattr(module, "SHOW_ALL_CAPABILITIES", True),
            exception_class=getattr(module, "EXCEPTION_CLASS", ImportError)
        )
    except ModuleNotFoundError as exc:
        if exc.name == config_module_path:
            return DepConfig()
        raise
