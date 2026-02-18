# Mini Library Walkthrough

This is a full integration story using a fictional package: `mylib`.

Goal:
- keep startup fast,
- support optional backends cleanly,
- expose dependency status to users,
- release with confidence.

## Step 0: Project Shape

Assume this structure:

```text
mylib/
  __init__.py
  _depdigest.py
  api/
    convert.py
  plugins/
    openmm_form/
      __init__.py
```

## Step 1: Define Dependency Policy (`_depdigest.py`)

Copy this:

```python
# mylib/_depdigest.py
LIBRARIES = {
    "numpy": {"type": "hard", "pypi": "numpy"},
    "openmm.unit": {"type": "soft", "pypi": "openmm", "conda": "openmm"},
}

MAPPING = {
    "openmm_form": "openmm.unit",
}

SHOW_ALL_CAPABILITIES = True
```

Adapt this:
- replace keys with your importable module names;
- adjust `pypi`/`conda` hints to your ecosystem;
- map your plugin folder names in `MAPPING`.

## Step 2: Guard an Optional API Path

Copy this:

```python
# mylib/api/convert.py
from depdigest import dep_digest

@dep_digest("openmm.unit")
def to_openmm(value):
    import openmm.unit
    return value * openmm.unit.nanometer
```

Adapt this:
- function names and return types;
- selected dependency key.

Critical rule:
- keep optional imports inside guarded functions.

## Step 3: Add Conditional Enforcement

Copy this:

```python
from depdigest import dep_digest

@dep_digest("openmm.unit", when={"backend": "openmm"})
def convert(value, backend="native"):
    if backend == "openmm":
        import openmm.unit
    return value
```

Adapt this:
- `when` keys to your function arguments;
- dependency key to your backend/tool.

## Step 4: Add a Lazy Registry

Copy this:

```python
from depdigest import LazyRegistry

plugins = LazyRegistry(
    package_prefix="mylib.plugins",
    directory="mylib/plugins",
    attr_name="plugin_name",
)
```

Add this in plugin module:

```python
# mylib/plugins/openmm_form/__init__.py
plugin_name = "openmm"
```

## Step 5: Expose Dependency Status

Copy this:

```python
from depdigest import get_info

def dependency_status():
    return get_info("mylib")
```

Use this in:
- CLI diagnostics,
- support output,
- issue templates.

## Step 6: Validate Behavior

Test these scenarios:
- missing optional dependency raises clear error;
- non-optional paths still run;
- plugin loading does not crash when optional plugin import fails.

## Step 7: Move to Production

Before release, run the `Production Checklist` page in this section.

For a large real-world implementation reference:
- `https://github.com/uibcdf/molsysmt`
