import os
import logging
from importlib import import_module
from typing import Dict, Any, Optional, Callable
from .checker import is_installed

logger = logging.getLogger(__name__)

class LazyRegistry(dict):
    """
    A dictionary-like registry that populates itself lazily by scanning a directory.
    """
    def __init__(self, 
                 package_prefix: str, 
                 directory: str, 
                 config_provider: Optional[Any] = None,
                 attr_name: str = 'form_name'):
        super().__init__()
        self._package_prefix = package_prefix
        self._directory = directory
        self._config_provider = config_provider
        self._attr_name = attr_name
        self._initialized = False
        self._initializing = False

    def _ensure_initialized(self):
        if self._initialized or self._initializing:
            return
        
        self._initializing = True
        try:
            self._scan_and_load()
            self._initialized = True
        finally:
            self._initializing = False

    def _scan_and_load(self):
        if not os.path.exists(self._directory):
            logger.warning(f"Registry directory not found: {self._directory}")
            return

        for entry in os.scandir(self._directory):
            if entry.is_dir() and entry.name not in ['__pycache__']:
                
                # Check visibility/dependency via config provider
                if self._config_provider and hasattr(self._config_provider, 'should_load_plugin'):
                    if not self._config_provider.should_load_plugin(entry.name):
                        continue

                try:
                    module_path = f"{self._package_prefix}.{entry.name}"
                    mod = import_module(module_path)
                    
                    # Get the identity of the plugin (e.g. form_name)
                    identity = getattr(mod, self._attr_name, None)
                    if identity:
                        self[identity] = mod
                except Exception as e:
                    logger.debug(f"Failed to load plugin {entry.name}: {e}")

    # --- Proxy dict methods ---
    def __getitem__(self, key):
        self._ensure_initialized()
        return super().__getitem__(key)

    def __contains__(self, key):
        self._ensure_initialized()
        return super().__contains__(key)

    def keys(self):
        self._ensure_initialized()
        return super().keys()

    def values(self):
        self._ensure_initialized()
        return super().values()

    def items(self):
        self._ensure_initialized()
        return super().items()

    def get(self, key, default=None):
        self._ensure_initialized()
        return super().get(key, default)
