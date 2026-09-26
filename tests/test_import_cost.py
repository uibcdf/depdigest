"""Installed-style imports should not discover distribution metadata eagerly."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generated_version_path_does_not_import_metadata():
    program = f"""
import sys
import types
sys.path.insert(0, {str(ROOT)!r})
generated = types.ModuleType('depdigest._version')
generated.__version__ = '0.0.0+installed-test'
sys.modules['depdigest._version'] = generated
import depdigest
assert depdigest.__version__ == '0.0.0+installed-test'
assert 'importlib.metadata' not in sys.modules
"""
    subprocess.run(
        [sys.executable, "-I", "-c", program],
        check=True,
        capture_output=True,
        text=True,
    )
