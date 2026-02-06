"""smonitor adapters for DepDigest (private)."""

from .runtime import ensure_configured
from .emitter import emit_missing_dependency

__all__ = ["ensure_configured", "emit_missing_dependency"]
