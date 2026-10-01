# Showcase

This section provides three realistic integration showcases. Each example targets a different use case so you can adapt the pattern that best matches your library.

## Example Catalog

| Showcase | What you will find |
|---|---|
| [Optional Backend Routing](optional-backend-routing.md) | Conditional dependency enforcement with `@dep_digest(..., when=...)` and lazy imports for backend-specific execution paths. |
| [Plugin Ecosystem with LazyRegistry](plugin-ecosystem-lazyregistry.md) | A scalable plugin architecture where discovery is cheap and optional plugin dependencies are enforced only on access. |
| [User-Facing Dependency Diagnostics](dependency-diagnostics-reporting.md) | A practical pattern to expose dependency status to end users (CLI/notebook/support workflows) using introspection APIs. |

```{toctree}
:maxdepth: 1
:hidden:

optional-backend-routing.md
plugin-ecosystem-lazyregistry.md
dependency-diagnostics-reporting.md
```
