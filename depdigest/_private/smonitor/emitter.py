from __future__ import annotations

"""Library-level diagnostic bundle helpers for optional warnings."""

from smonitor.integrations import DiagnosticBundle
from .catalog import CATALOG, META, PACKAGE_ROOT

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve
