import inspect
from functools import wraps
from typing import Any, Callable, Dict, Optional
from .checker import check_dependency

def dep_digest(library: str, when: Optional[Dict[str, Any]] = None, config: Optional[Any] = None):
    """
    Decorator to declare and enforce a dependency.
    
    Parameters
    ----------
    library : str
        Name of the library (key in the project's dependency configuration).
    when : dict, optional
        Condition map {argument_name: value}. The dependency is checked ONLY 
        if the runtime argument matches this value.
    config : object, optional
        Project-specific configuration object that contains dependency metadata.
    """
    def decorator(func: Callable):
        # 1. Metadata Registration
        if not hasattr(func, '_dependencies'):
            func._dependencies = []
        func._dependencies.append({'library': library, 'when': when})

        # Pre-compute signature for performance
        sig = inspect.signature(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            should_check = True
            
            # 2. Conditional Logic
            if when is not None:
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                arguments = bound.arguments
                
                for arg_name, required_value in when.items():
                    if arg_name not in arguments or arguments[arg_name] != required_value:
                        should_check = False
                        break
            
            if should_check:
                # Use config if provided to get more details (like pypi name)
                pypi_name = None
                exc_class = ImportError
                
                if config and hasattr(config, 'get_dependency_info'):
                    info = config.get_dependency_info(library)
                    if info:
                        pypi_name = info.get('pypi')
                        # Could also use a custom exception class from config
                
                check_dependency(library, pypi_name=pypi_name, caller=func.__name__, exception_class=exc_class)
                
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
