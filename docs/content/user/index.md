# User

Welcome. This guide is organized as a tutorial path so you can integrate
DepDigest in your library without friction.

If you follow the pages in order, you will go from a minimal setup to advanced
patterns and edge cases.

Before implementing, keep this contract at hand:
- [DEPDIGEST_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/standards/DEPDIGEST_GUIDE.md)

If you want to contribute to DepDigest itself (not only integrate it in your own library), continue in the [Developers section](../developers/index.md).

Recommended practice:
- place a copy of `DEPDIGEST_GUIDE.md` in your project root, so humans and AI agents follow the same contract.

## Learning Path

1. [Quick Start](quickstart.md): first working integration in minutes.
2. [Mini Library Walkthrough](mini-library-walkthrough.md): complete narrative from zero to production.
3. [Configuration](configuration.md): how `_depdigest.py` defines your dependency policy.
4. [Hard vs Soft](hard-vs-soft.md): what each dependency type means in practice.
5. [Integrating in Your Library](integrating-your-library.md): implementation blueprint for real codebases.
6. [Conditional Dependencies](conditional-deps.md): enforce dependencies only when needed.
7. [Lazy Registry](lazy-registry.md): lazy plugin/module loading at scale.
8. [Introspection](introspection.md): expose dependency status to your users.
9. [SMonitor Integration](smonitor.md): understand diagnostics behavior and controls.
10. [Edge Cases](edge-cases.md): recovecos you should know before production.
11. [Troubleshooting](troubleshooting.md): fast diagnosis for common integration failures.
12. [Audit CLI](audit-cli.md): detect top-level imports of soft dependencies before release.
13. [Production Checklist](production-checklist.md): final verification before release.
14. [FAQ](faq.md): short answers to common integration questions.

```{toctree}
:maxdepth: 1
:hidden:

quickstart.md
mini-library-walkthrough.md
configuration.md
hard-vs-soft.md
integrating-your-library.md
conditional-deps.md
lazy-registry.md
introspection.md
smonitor.md
edge-cases.md
troubleshooting.md
audit-cli.md
production-checklist.md
faq.md
```
