from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

CATALOG = {
    "missing_dependency": {
        "code": "DEPDIGEST-MISSING-DEPENDENCY",
        "source": "depdigest.check_dependency",
        "category": "dependency",
        "level": "ERROR",
    }
}
