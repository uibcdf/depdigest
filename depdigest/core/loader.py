import os
import logging
from importlib import import_module
from typing import Dict, Any, Optional, Callable
from .checker import is_installed
from .config import resolve_config
from smonitor import signal

logger = logging.getLogger(__name__)

class LazyRegistry(dict):
    """
    A dictionary-like registry that populates itself lazily.
    """
    def __init__(self, 
                 package_prefix: str, 
                 directory: str, 
                 attr_name: str = 'form_name'):
        super().__init__()
        self._package_prefix = package_prefix
        self._directory = directory
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

    @signal(tags=["loader"])
    def _scan_and_load(self):
        if not os.path.exists(self._directory):
            return

        cfg = resolve_config(self._package_prefix)

        for entry in os.scandir(self._directory):
            if entry.is_dir() and entry.name not in ['__pycache__']:
                
                lib_key = cfg.mapping.get(entry.name)
                if lib_key and not cfg.show_all_capabilities:
                    lib_info = cfg.libraries.get(lib_key, {})
                    if lib_info.get('type') == 'soft' and not is_installed(lib_key):
                        continue

                try:
                    module_path = f"{self._package_prefix}.{entry.name}"
                    mod = import_module(module_path)
                    identity = getattr(mod, self._attr_name, None)
                    if identity:
                        self[identity] = mod
                except Exception as e:
                    from smonitor.integrations import emit_from_catalog, merge_extra
                    from .._private.smonitor.catalog import CATALOG, META, PACKAGE_ROOT

                    try:
                        emit_from_catalog(
                            CATALOG["plugin_load_failed"],
                            package_root=PACKAGE_ROOT,
                            extra=merge_extra(
                                META,
                                {
                                    "plugin": entry.name,
                                    "caller": "depdigest.core.loader.LazyRegistry._scan_and_load",
                                    "error": str(e),
                                },
                            ),
                        )
                    except Exception as emit_error:
                        logger.warning(
                            "SMonitor emission failed in LazyRegistry._scan_and_load: signal=plugin_load_failed plugin=%s error=%s",
                            entry.name,
                            emit_error,
                        )
                    logger.debug(f"Failed to load plugin {entry.name}: {e}")

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
