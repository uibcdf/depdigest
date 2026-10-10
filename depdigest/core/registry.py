"""Declaration-based plugin lookup, independent of implementation imports."""

import os
from collections.abc import Mapping, MutableMapping
from inspect import currentframe

from .checker import check_dependency
from .config import resolve_config
from .loader import _RegistrySupport, import_module


class DeclaredRegistry(_RegistrySupport, MutableMapping):
    """Map declared identities to selectively loaded implementations.

    ``declarations`` is a mapping or iterable of ``(identity, plugin_key)`` pairs.
    Keys/iteration/membership describe visible declarations, not successful imports.
    Values/items load implementations as their views are iterated. Failed imports
    raise KeyError with their cause retained; use ``retry`` to attempt them again.
    """

    def __init__(
        self,
        package_prefix,
        directory,
        declarations,
        attr_name="form_name",
        discovery_mode="filesystem",
        entrypoint_group=None,
    ):
        if discovery_mode not in {"filesystem", "entry_points"}:
            raise ValueError("discovery_mode must be 'filesystem' or 'entry_points'")
        if discovery_mode == "entry_points" and not entrypoint_group:
            raise ValueError("entrypoint_group is required for entry_points")
        self._package_prefix = package_prefix
        self._directory = directory
        self._attr_name = attr_name
        self._discovery_mode = discovery_mode
        self._entrypoint_group = entrypoint_group
        self._declarations = {}
        pairs = (
            declarations.items() if isinstance(declarations, Mapping) else declarations
        )
        plugins = set()
        for identity, plugin in pairs:
            if not isinstance(identity, str) or not identity:
                raise ValueError("Declared identities must be nonempty strings")
            if not isinstance(plugin, str) or not plugin:
                raise ValueError("Plugin keys must be nonempty strings")
            if discovery_mode == "filesystem" and not plugin.isidentifier():
                raise ValueError("Filesystem plugin keys must be package names")
            if identity in self._declarations or plugin in plugins:
                raise ValueError("Duplicate identity or plugin declaration")
            self._declarations[identity] = plugin
            plugins.add(plugin)
        self._loaded = {}
        self._overrides = {}
        self._failures = {}
        self._discovery_failures = set()
        self._loading_plugins = set()
        self._entrypoint_snapshot = None
        self._load_trigger = "<direct load>"
        self._load_caller = "<unknown>"
        self._failure_caller = "<unknown>"

    def __iter__(self):
        cfg = resolve_config(self._package_prefix)
        return iter(
            tuple(
                key
                for key in dict.fromkeys((*self._declarations, *self._overrides))
                if key in self._overrides
                or self._plugin_allowed(self._declarations[key], cfg)
            )
        )

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, key):
        if key in self._overrides:
            return True
        return key in self._declarations and self._plugin_allowed(
            self._declarations[key], resolve_config(self._package_prefix)
        )

    def declared_keys(self):
        """Return all declared identities, including currently hidden ones."""
        return tuple(self._declarations)

    def loaded_keys(self):
        """Return visible identities with a cached implementation or override."""
        return tuple(
            key for key in self if key in self._loaded or key in self._overrides
        )

    def __getitem__(self, key):
        if key in self._overrides:
            return self._overrides[key]
        if key not in self:
            raise KeyError(key)
        if key in self._loaded:
            return self._loaded[key]
        if key in self._failures:
            raise KeyError(key) from self._failures[key]
        frame = currentframe()
        try:
            caller = frame.f_back if frame is not None else None
            location = (
                f"{caller.f_code.co_filename}:{caller.f_lineno}"
                if caller
                else "<unknown>"
            )
        finally:
            del frame
        return self._load(key, key, location)

    def _candidates(self):
        if self._discovery_mode == "filesystem":
            if not os.path.isdir(self._directory):
                return []
            with os.scandir(self._directory) as entries:
                return sorted(
                    entry.name
                    for entry in entries
                    if entry.is_dir() and entry.name != "__pycache__"
                )
        if self._entrypoint_snapshot is None:
            self._entrypoint_snapshot = tuple(self._resolve_entry_points())
        return sorted({ep.name for ep in self._entrypoint_snapshot})

    def _implementation(self, plugin):
        if self._discovery_mode == "filesystem":
            # Import only an immediate plugin of the supplied directory.
            if not os.path.isdir(os.path.join(self._directory, plugin)):
                raise LookupError(f"No filesystem plugin {plugin!r}")
            module = f"{self._package_prefix}.{plugin}"
            return import_module(module), module
        self._candidates()
        matches = [ep for ep in self._entrypoint_snapshot if ep.name == plugin]
        if len(matches) != 1:
            raise LookupError(
                f"Expected one entry point named {plugin!r}; found {len(matches)}"
            )
        ep = matches[0]
        return ep.load(), getattr(ep, "value", ep.name)

    def _load(self, key, trigger, caller, *, undeclared=False):
        plugin = self._declarations[key] if not undeclared else key
        if plugin in self._loading_plugins:
            raise KeyError(f"Recursive load of plugin {plugin!r}")
        previous = self._load_trigger, self._load_caller, self._failure_caller
        self._load_trigger, self._load_caller, self._failure_caller = (
            trigger,
            caller,
            caller,
        )
        self._loading_plugins.add(plugin)
        try:
            cfg = resolve_config(self._package_prefix)
            library = cfg.mapping.get(plugin)
            info = cfg.libraries.get(library, {})
            if library and info.get("type") == "soft":
                check_dependency(
                    library,
                    pypi_name=info.get("pypi"),
                    conda_name=info.get("conda", library.split(".")[0]),
                    conda_channel=info.get("channel"),
                    doc_url=cfg.doc_url,
                    exception_class=cfg.exception_class,
                    caller=caller,
                    kind=info.get("kind", "python"),
                    executable=info.get("executable"),
                )
            implementation, module = self._implementation(plugin)
            identity = getattr(implementation, self._attr_name, None)
            if self._discovery_mode == "entry_points":
                identity = identity or plugin
            if undeclared:
                if not isinstance(identity, str) or not identity:
                    raise ValueError(f"Plugin {plugin!r} has no identity")
                if identity in self._declarations or identity in self._overrides:
                    raise ValueError(
                        f"Plugin {plugin!r} duplicates identity {identity!r}"
                    )
                self._declarations[identity] = plugin
            elif identity != key:
                raise ValueError(
                    f"Declared identity {key!r} disagrees with {identity!r}"
                )
            self._loaded[identity] = implementation
            self._emit_plugin_loaded(plugin, module)
            return self._overrides.get(identity, implementation)
        except Exception as error:
            if undeclared:
                self._discovery_failures.add(plugin)
            else:
                self._failures[key] = error
            self._emit_plugin_load_failed(plugin, error)
            raise KeyError(key) from error
        finally:
            self._loading_plugins.discard(plugin)
            self._load_trigger, self._load_caller, self._failure_caller = previous

    def retry(self, key):
        """Clear a recorded failure and request the identity again."""
        self._failures.pop(key, None)
        return self[key]

    def refresh(self):
        """Forget failed loads and entry-point metadata, retaining implementations.

        Config overrides are resolved on every access. Python dependency discovery
        still uses ``is_installed``'s cache; clear that separately after installation.
        """
        self._failures.clear()
        self._discovery_failures.clear()
        self._entrypoint_snapshot = None

    def discover(self):
        """Explicitly import eligible undeclared plugins and add their identities.

        Candidates are ordered by plugin key. The first discovered identity wins;
        duplicate identities and load failures are diagnosed and skipped. Repeated
        calls skip successful declarations and failures until ``refresh()``.
        """
        cfg = resolve_config(self._package_prefix)
        declared_plugins = set(self._declarations.values())
        for plugin in self._candidates():
            if (
                plugin in declared_plugins
                or plugin in self._discovery_failures
                or plugin in self._loading_plugins
            ):
                continue
            if not self._plugin_allowed(plugin, cfg):
                continue
            try:
                self._load(
                    plugin, "discover()", "DeclaredRegistry.discover", undeclared=True
                )
            except KeyError:
                continue
        return self.declared_keys()

    def __setitem__(self, key, value):
        if not isinstance(key, str) or not key:
            raise ValueError("Registry identities must be nonempty strings")
        self._overrides[key] = value
        self._failures.pop(key, None)

    def __delitem__(self, key):
        if key not in self._declarations and key not in self._overrides:
            raise KeyError(key)
        self._declarations.pop(key, None)
        self._overrides.pop(key, None)
        self._loaded.pop(key, None)
        self._failures.pop(key, None)

    def clear(self):
        """Remove declarations, overrides and caches without importing plugins."""
        self._declarations.clear()
        self._overrides.clear()
        self._loaded.clear()
        self._failures.clear()
        self._discovery_failures.clear()
