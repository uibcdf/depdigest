# Conditional Dependencies

Some dependencies are needed only for specific modes, engines, or output
formats. Use `when=...` to express that directly.

## Example

```python
from depdigest import dep_digest

@dep_digest("openmm.unit", when={"engine": "openmm"})
def convert(value, engine="native"):
    if engine == "openmm":
        import openmm.unit
    return value
```

## Behavior

- `convert(..., engine="native")`:
  dependency check is skipped.
- `convert(..., engine="openmm")`:
  dependency is enforced.

## When This Is Useful

- multiple backends in one API;
- optional exporters/importers;
- feature flags where only some paths need extra libraries.

## Practical Advice

- keep conditions simple and explicit;
- align `when` keys with real function arguments;
- keep optional imports inside the conditional path.

## Next

Continue with [Lazy Registry](lazy-registry.md) to scale this approach to
plugin-style modules.
