```{eval-rst}
:html_theme.sidebar_secondary.remove:
```

% DepDigest

:::{figure} _static/logo.svg
:width: 50%
:align: center

Digesting dependencies into clear, actionable insight.

```{image} https://img.shields.io/badge/release-v0.2.0-white.svg
:target: https://github.com/uibcdf/depdigest/releases/tag/0.2.0
```
```{image} https://img.shields.io/badge/license-MIT-white.svg
:target: https://github.com/uibcdf/depdigest/blob/main/LICENSE
```
```{image} https://img.shields.io/badge/install%20with-conda-white.svg
:target: https://anaconda.org/uibcdf/depdigest
```
```{image} https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-white.svg
:target: https://www.python.org/downloads/
```
```{image} https://img.shields.io/badge/DOI-10.5281/8092688-white.svg
:target: https://zenodo.org/record/8092688
```

:::

<br>

## Install it

```bash
conda install -c uibcdf depdigest
```

## Use it

DepDigest lets you keep imports fast and dependency errors clear.
You declare what is optional, guard execution at runtime, and load heavy modules
only when they are really needed.

```python
from depdigest import dep_digest

@dep_digest("openmm")
def run_simulation(system):
    import openmm  # lazy import: only executed when function is called
    ...
```

What happens here:
- If `openmm` is installed, your function runs normally.
- If it is missing, DepDigest raises a readable error with installation hints.
- A structured [SMonitor](https://www.uibcdf.org/smonitor) event is emitted for diagnostics.


```{eval-rst}

.. toctree::
   :maxdepth: 2
   :hidden:

   content/about/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/showcase/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/user/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   content/developers/index.md

.. toctree::
   :maxdepth: 2
   :hidden:

   api/index.md

```
