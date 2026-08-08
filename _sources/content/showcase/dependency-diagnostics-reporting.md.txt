# User-Facing Dependency Diagnostics

This showcase focuses on helping users understand optional capability availability in their current environment.

## Problem

Support requests are slower when users cannot quickly tell which optional dependencies are installed.

## Pattern

Expose dependency status from your package API or CLI:

```python
from depdigest import get_info

def dependency_status():
    return get_info("my_pkg")
```

You can present this output in:
- a CLI command (`my_pkg deps`);
- a notebook help cell;
- a support/debug report.

## Why this works

- users can self-diagnose missing capabilities;
- maintainers receive clearer bug reports;
- dependency expectations become transparent.

## Optional addition

If your package already uses SMonitor, pair this report with diagnostics links so users can jump from status output to remediation guidance.
