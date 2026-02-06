# Implementation Guide

This guide explains how to integrate **DepDigest** into a new Python library (e.g., `MyLibrary`).

## 1. Create the Configuration File

In the root of your package, create a file named `_depdigest.py`. This file serves as the Single Source of Truth for your project's dependencies.

```python
# MyLibrary/_depdigest.py

LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'mdtraj': {'type': 'soft', 'pypi': 'mdtraj'},
    'openmm': {'type': 'soft', 'pypi': 'openmm'},
}

# Optional: Map directories to libraries for the LazyRegistry
MAPPING = {
    'form_mdtraj': 'mdtraj',
    'form_openmm': 'openmm',
}

# Optional: Global visibility setting
SHOW_ALL_CAPABILITIES = True

# Optional: Use a custom exception class
# EXCEPTION_CLASS = MyLibraryCustomError
```

## 2. Using the `@dep_digest` Decorator

Decorate any function that requires an optional (soft) dependency. DepDigest will automatically find your `_depdigest.py` and enforce the rules.

```python
# MyLibrary/api/simulation.py
from depdigest import dep_digest

@dep_digest('openmm')
def run_simulation(system):
    # The import MUST be lazy (inside the function)
    import openmm
    # ...
```

### Conditional Enforcement
You can also enforce dependencies only when certain arguments are passed:

```python
@dep_digest('openmm', when={'engine': 'OpenMM'})
def compute_energy(item, engine='Native'):
    if engine == 'OpenMM':
        import openmm
        ...
```

## 3. Implementing a Lazy Registry

If your library has many optional plugins or formats, use `LazyRegistry` to avoid importing them all at startup.

```python
# MyLibrary/plugins/__init__.py
import os
from depdigest import LazyRegistry

current_dir = os.path.dirname(os.path.abspath(__file__))

# This registry will scan the current directory but only load 
# sub-modules whose dependencies (mapped in _depdigest.py) are met.
plugins = LazyRegistry(
    package_prefix='MyLibrary.plugins',
    directory=current_dir,
    attr_name='plugin_name' # The attribute in each module that defines its ID
)
```

## 4. Architecture Validation

To ensure your library remains "Lazy" and fast, use the validation tools in your CI pipeline.

```python
from depdigest.utils.ast_tools import validate_codebase

violations = validate_codebase(
    src_root='MyLibrary/',
    soft_deps={'mdtraj', 'openmm'},
    exempt_dirs=['MyLibrary/tests/']
)

if violations:
    print("Found top-level imports of soft dependencies!")
```

## 5. Summary Table for Users

Expose a function to help users see what they have installed:

```python
# MyLibrary/api/help.py
from depdigest import get_info

def dependency_status():
    data = get_info('MyLibrary')
    # Format and display the data (e.g., using Pandas or Tabulate)
    ...
```

## 6. smonitor Integration

DepDigest emits structured diagnostics for missing dependencies. Configuration
is loaded from `_smonitor.py` in the package root (`depdigest/_smonitor.py`), and
the catalog lives in `depdigest/_private/smonitor/catalog.py` with metadata in
`depdigest/_private/smonitor/meta.py`.
