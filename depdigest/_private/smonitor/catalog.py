from __future__ import annotations

from pathlib import Path

from .meta import DOC_URL, ISSUES_URL, API_URL

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

META = {
    "doc_url": DOC_URL,
    "issues_url": ISSUES_URL,
    "api_url": API_URL,
}

CATALOG = {
    "missing_dependency": {
        "code": "DEP-ERR-MISS-001",
        "source": "depdigest.error.missing_dependency",
        "category": "dependency",
        "level": "ERROR",
    },
    "plugin_load_failed": {
        "code": "DEP-DBG-LOAD-001",
        "source": "depdigest.debug.plugin_load_failed",
        "category": "loader",
        "level": "DEBUG",
    },
}

CODES = {
    "DEP-ERR-MISS-001": {
        "title": "Missing Dependency",
        "user_message": "Required library '{library}' not found.",
        "user_hint": "Install it via:\n  {pip_install}\n  {conda_install}\nDocs: {doc_url}",
        "dev_message": "Dependency '{library}' missing in '{caller}'.",
        "dev_hint": "Add to requirements or environment. Docs: {doc_url}",
    },
    "DEP-DBG-LOAD-001": {
        "title": "Plugin load failed",
        "user_message": "An optional plugin failed to load and was skipped.",
        "user_hint": "No action is required unless you expected that plugin to be available.",
        "dev_message": "Plugin '{plugin}' failed to load in '{caller}': {error}.",
        "dev_hint": "Check dependency gates and import errors for optional plugins.",
    },
}

SIGNALS = {
    "depdigest.error.missing_dependency": {"extra_required": ["library", "caller", "pip_install", "conda_install"]},
    "depdigest.debug.plugin_load_failed": {"extra_required": ["plugin", "caller", "error"]},
}
