# Optional scientific engines

An engine can be a Python distribution or an executable. Keep it out of your
mandatory package dependencies when only a selected backend needs it. DepDigest
checks availability when that backend is called; SMonitor owns the diagnostic
event. Neither installs software for the user.

## Declare the dependency and its actual installation routes

```python
LIBRARIES = {
    "pocketeer": {
        "type": "soft",
        "pypi": "pocketeer",
        "conda": None,
    },
    "fpocket": {
        "type": "soft",
        "kind": "executable",
        "executable": "fpocket",
        "pypi": None,
        "conda": "fpocket",
        "channel": "conda-forge",
    },
}
DOC_URL = "https://your-project.example/docs/engines"
```

`kind` defaults to `python`. Python availability uses the import name, which may
differ from the PyPI distribution name. Executables use `shutil.which` against
the current PATH; an absolute executable path is also accepted. This probe
does not execute a command or guarantee that the engine's version, native
libraries, transitive imports, or scientific configuration will work.

An explicit `conda: None` disables the Conda route. An explicit `pypi: None`
disables pip. Omitted names in the inventory retain the legacy import-root
defaults; declare both routes explicitly in new integrations. `get_info` returns
`None` for a disabled installation command instead of inventing a package name.
The checker, decorator, and inventory use the same declared Conda channel.

## Guard the narrowest backend and import lazily

```python
from depdigest import dep_digest


@dep_digest("pocketeer")
def analyze_with_pocketeer(system):
    import pocketeer

    return pocketeer.find_pockets(system)


@dep_digest("fpocket")
def analyze_with_fpocket(pdb_file):
    import subprocess

    return subprocess.run(["fpocket", "-f", str(pdb_file)], check=True)
```

If an adapter already implements source loading through `upstream_root`, use
`@dep_digest('pocketeer', when={'upstream_root': None})` to guard its installed
route. The condition does not implement source loading. DepDigest does not
modify `sys.path`, discover source layouts,
launch processes, contact servers, normalize results, or select a replacement
engine. Those operations belong to the consumer adapter.

Keep native implementations and persisted-result loaders outside these guards.
A server adapter normally needs a client library and service configuration;
service reachability, authentication, and job failure are separate runtime
conditions, not a missing Python distribution.

## Diagnostics and verification

An absent requested dependency emits `DEP-ERR-MISS-001` with library, caller,
installation hint, and dependency kind. An executable failure additionally
records the requested executable. `EXCEPTION_CLASS` may select a consumer error;
its constructor must accept the documented library/caller/message contract.
Use SMonitor's `CatalogException` and a registered catalog code when the consumer
also needs its own structured diagnostic. Preserve message-first construction
so exception and warning reconstruction through `args` remains valid.

Availability is not execution health. Preserve transitive import failures and
subprocess failures rather than relabeling them as an absent engine. Document
engine versions, additional runtime requirements, and installation commands in
the consuming library.
For dotted Python names, discovery may import the parent; DepDigest preserves a
failure in the parent's internal dependency instead of treating it as absence.

Verify these behaviors:

- The consuming package imports when all optional engines are absent.
- A requested absent backend fails before input preparation with usable guidance.
- Other backends, native implementations, and result loaders still work.
- Disabled package managers never appear in diagnostics or the inventory.
- Executable probes follow changes to PATH and executable permissions.
- An installed engine returns the same scientific results through the adapter
  as a direct upstream call on the same submitted input.

The reusable provider regression tests are `tests/test_optional_engines.py`.
TopoMT is the initial scientific consumer; future DockingMT or ElastNetMT
adapters can use the same declaration and guard without copying discovery logic.
