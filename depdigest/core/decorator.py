import inspect
from functools import wraps
from typing import Any, Callable, Dict, Optional
from .checker import check_dependency
from .config import resolve_config


def _condition_value_matches(value: Any, expected: Any) -> bool:
    """Return whether a runtime argument satisfies a conditional dependency.

    Scientific arguments can define vectorized equality. In those cases, ``==``
    returns an array-like object whose truth value is ambiguous. Treat those
    results as matching only when every comparison element is true.
    """

    if expected is None or value is None:
        return value is expected

    try:
        comparison = value == expected
    except Exception:
        return False

    if isinstance(comparison, bool):
        return comparison

    try:
        return bool(comparison)
    except (TypeError, ValueError):
        pass

    all_method = getattr(comparison, "all", None)
    if callable(all_method):
        try:
            return bool(all_method())
        except (TypeError, ValueError):
            return False

    return False


def _condition_parameter_sources(sig: inspect.Signature, names: set[str]):
    sources = {}
    positional_index = 0
    for name, parameter in sig.parameters.items():
        if parameter.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            if name in names:
                sources[name] = (positional_index, parameter.default)
            positional_index += 1
        elif parameter.kind is inspect.Parameter.KEYWORD_ONLY and name in names:
            sources[name] = (None, parameter.default)
    return sources


def _resolve_condition_value(source, name, args, kwargs):
    position, default = source
    if name in kwargs:
        if position is not None and position < len(args):
            return False, None
        return True, kwargs[name]
    if position is not None and position < len(args):
        return True, args[position]
    if default is not inspect.Parameter.empty:
        return True, default
    return False, None


def dep_digest(library: str, when: Optional[Dict[str, Any]] = None):
    """
    Decorator to declare and enforce a dependency.
    Resolved dynamically at runtime to support configuration changes.
    """
    def decorator(func: Callable):
        # 1. Metadata Registration (Still at definition time)
        if not hasattr(func, '_dependencies'):
            func._dependencies = []
        func._dependencies.append({'library': library, 'when': when})

        # Pre-compute signature
        sig = inspect.signature(func)
        condition_sources = _condition_parameter_sources(sig, set(when or {}))
        module_path = func.__module__

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 2. RESOLVE CONFIG AT RUNTIME
            # This allows tests to register config AFTER function definition
            cfg = resolve_config(module_path)
            
            should_check = True
            if when is not None:
                for k, v in when.items():
                    source = condition_sources.get(k)
                    if source is None:
                        bound = sig.bind(*args, **kwargs)
                        bound.apply_defaults()
                        matched = k in bound.arguments and _condition_value_matches(
                            bound.arguments[k], v
                        )
                    else:
                        found, value = _resolve_condition_value(
                            source, k, args, kwargs
                        )
                        matched = found and _condition_value_matches(value, v)
                    if not matched:
                        should_check = False
                        break
            
            if should_check:
                lib_info = cfg.libraries.get(library, {})
                pypi_name = lib_info.get('pypi')
                check_dependency(library, pypi_name=pypi_name, caller=func.__name__, 
                                 exception_class=cfg.exception_class)
                
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
