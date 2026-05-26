# Proposal: High-Frequency In-Memory Dependency Caching

## Abstract

We propose introducing a thread-safe, sub-microsecond in-memory caching mechanism for `@dep_digest` checks. This guarantees that repeated dependency checks inside hot scientific loops (e.g., rendering loops or coordinate-update steps) have absolutely zero latency overhead.

---

## The Problem

`@dep_digest` validates the presence of optional dependencies (e.g., `numpy`, `pyunitwizard`) dynamically when functions are called.
Although checking if a module exists in `sys.modules` is generally fast in Python, calling package utilities, checking conda/pypi registry maps, or running validation wrappers repeatedly in high-frequency scientific loops (like processing thousands of atom selections or rendering visual frames at 60 FPS) introduces minor CPU overhead that accumulates over time.

---

## Proposed Solution

Introduce a fast caching registry layer inside `depdigest` to store resolved package availability states.

### 1. The Cache Architecture
* Maintain a simple, thread-safe in-memory cache dictionary (`dict[str, bool]`) recording package installation status:
  ```python
  # depdigest/core.py (Concept)
  _INSTALLATION_CACHE: dict[str, bool] = {}
  ```

### 2. Fast-Path Resolution
When `@dep_digest` or `is_installed` is called:
1. It first checks if the library key exists in `_INSTALLATION_CACHE`.
2. If yes, it returns the boolean status instantly (sub-microsecond execution time).
3. If no (cache miss), it runs the standard validation checks (inspecting `sys.modules`, resolving paths), registers the result in the cache, and returns.

### 3. Cache Invalidation
Since Python packages are rarely installed or uninstalled *mid-session*, the cache can remain persistent throughout the library's import lifespan. If needed, a helper `depdigest.clear_cache()` can be exposed.

---

## Benefits

* **High-Frequency Performance**: Bypasses all validation overhead in recursive, inner scientific loop calls.
* **Safer Integrations**: Encourages developers to keep `@dep_digest` on public wrappers and hot interior functions without fearing a performance regression.
