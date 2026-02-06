from __future__ import annotations

from typing import Optional


def emit_missing_dependency(*, library: str, caller: Optional[str] = None) -> None:
    import smonitor

    smonitor.emit(
        "ERROR",
        "",
        source="depdigest.check_dependency",
        code="DEPDIGEST-MISSING-DEPENDENCY",
        category="dependency",
        extra={
            "library": library,
            "caller": caller or "",
            "pip_install": f"pip install {library}",
            "conda_install": f"conda install -c conda-forge {library}",
        },
    )
