# Integrating in Your Library

Use this page as an implementation blueprint after reading:

- `Quick Start`
- `Mini Library Walkthrough`

Those pages teach the flow end-to-end.
This one helps you map that flow onto a real existing codebase.

## 1. Read the Canonical Contract First

In this repository, the canonical integration contract is:

- `standards/DEPDIGEST_GUIDE.md`

Use that file as the source of truth for:
- expected configuration structure,
- required lazy-import behavior,
- recommended integration patterns.

## 2. Integration Blueprint (Copy Then Adapt)

Create `_depdigest.py` in your package root.

Template:

```python
# my_library/_depdigest.py

LIBRARIES = {
    "numpy": {"type": "hard", "pypi": "numpy"},
    "mdtraj": {"type": "soft", "pypi": "mdtraj"},
    "openmm.unit": {"type": "soft", "pypi": "openmm", "conda": "openmm"},
}

MAPPING = {
    "mdtraj_form": "mdtraj",
    "openmm_form": "openmm.unit",
}

SHOW_ALL_CAPABILITIES = True

# Optional
# EXCEPTION_CLASS = MyLibraryDependencyError
```

Then apply this mapping:

- Code paths that need optional libraries:
  wrap with `@dep_digest(...)`.
- Argument-dependent optional paths:
  use `when={...}`.
- Plugin-heavy folders:
  use `LazyRegistry` + `MAPPING`.
- User diagnostics:
  expose `get_info(...)` via CLI/help command.

## 3. Adoption Strategy for Existing Libraries

Recommended rollout:

1. Start with one optional backend and one guarded function.
2. Add `_depdigest.py` with minimal `LIBRARIES`.
3. Add tests for missing dependency behavior.
4. Expand to additional optional paths.
5. Add `LazyRegistry` where import fan-out is large.
6. Add dependency status command for users/support.

This reduces migration risk and makes regressions easier to isolate.

## 4. Real-World Reference

For a complete ecosystem implementation example, you can review:

- `https://github.com/uibcdf/molsysmt`
