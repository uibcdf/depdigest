# FAQ

## Do I need `_depdigest.py` to start?

No. You can start with just `@dep_digest(...)`.  
But for a real library, `_depdigest.py` is strongly recommended.

## Should I use dependency keys or package install names?

Use importable module names as keys (for example `openmm.unit`).
Use `pypi`/`conda` fields only for install hints.

## Can I use DepDigest with custom exceptions?

Yes. Set `EXCEPTION_CLASS` in `_depdigest.py`.

## Is LazyRegistry mandatory?

No. Use it only if you have many optional modules/plugins and startup cost
matters.

## Does DepDigest replace package managers?

No. It does not install dependencies. It checks availability and reports clear
actions to users.

## How does this relate to SMonitor?

DepDigest integrates with SMonitor for structured diagnostics and breadcrumb
traceability.
