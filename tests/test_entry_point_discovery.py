"""Protect the standard discovery decision against stale or narrowed shortcuts."""

from __future__ import annotations

import importlib.metadata as metadata
import importlib.util
import os
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "entry_point_discovery_probe", ROOT / "benchmarks/entry_point_discovery.py"
)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


def _metadata(name, value="plugin_that_must_not_load:register"):
    return {
        "METADATA": f"Metadata-Version: 2.1\nName: {name}\nVersion: 1.0\n",
        "entry_points.txt": (
            f"[ackredit.citations]\nshared = {value}\n"
            f"[ackredit.formats]\nshared = {value}\n"
        ),
    }


def _install_metadata(site, name, value="plugin_that_must_not_load:register"):
    directory = site / f"{name}-1.0.dist-info"
    directory.mkdir(parents=True)
    for filename, text in _metadata(name, value).items():
        (directory / filename).write_text(text)


def _identities(groups):
    return {
        group: [(ep.name, ep.value, ep.dist.name, ep.dist.version) for ep in entries]
        for group, entries in groups.items()
    }


def test_grouped_query_preserves_entry_point_identity_order_and_duplicates(
    tmp_path, monkeypatch
):
    _install_metadata(tmp_path, "first", "unimported_first:register")
    _install_metadata(tmp_path, "second", "unimported_second:register")
    monkeypatch.setattr(sys, "path", [str(tmp_path)])
    separate = probe.discover("separate")
    grouped = probe.discover("grouped")
    assert _identities(grouped) == _identities(separate)
    assert len(grouped[probe.GROUPS[0]]) == 2  # Same EP name in distinct distributions.
    assert all(ep.dist is not None for entries in grouped.values() for ep in entries)
    assert "unimported_first" not in sys.modules
    assert "unimported_second" not in sys.modules


def test_fresh_query_sees_late_provider_that_a_reused_snapshot_misses(
    tmp_path, monkeypatch
):
    _install_metadata(tmp_path, "initial")
    monkeypatch.setattr(sys, "path", [str(tmp_path)])
    stale = probe.discover("grouped")
    late_site = tmp_path / "new-site"
    _install_metadata(late_site, "late")
    sys.path.insert(0, str(late_site))
    fresh = probe.discover("grouped")
    assert [ep.dist.name for ep in stale[probe.GROUPS[1]]] == ["initial"]
    assert [ep.dist.name for ep in fresh[probe.GROUPS[1]]] == ["late", "initial"]


@pytest.mark.parametrize("mode", ["single", "grouped"])
def test_fresh_demand_sees_late_install_in_the_same_site(tmp_path, monkeypatch, mode):
    _install_metadata(tmp_path, "initial")
    monkeypatch.setattr(sys, "path", [str(tmp_path)])
    previous = probe.discover("grouped")
    before = tmp_path.stat()
    _install_metadata(tmp_path, "late")
    # Preserve the installation event on filesystems with coarse mtime resolution.
    os.utime(tmp_path, ns=(before.st_atime_ns, before.st_mtime_ns + 1_000_000_000))
    current = probe.discover(mode)
    assert {ep.dist.name for ep in previous[probe.GROUPS[1]]} == {"initial"}
    assert {ep.dist.name for ep in current[probe.GROUPS[1]]} == {"initial", "late"}


class _MemoryDistribution(metadata.Distribution):
    def __init__(self, name):
        self.data = _metadata(name)

    def read_text(self, filename):
        return self.data.get(filename)

    def locate_file(self, path):
        raise AssertionError("memory provider has no filesystem layout")


class _MemoryFinder(metadata.DistributionFinder):
    def __init__(self):
        self.names = ["memory_initial"]
        self.calls = 0

    def find_distributions(self, context=None):
        self.calls += 1
        return iter(_MemoryDistribution(name) for name in self.names)


def test_grouped_query_keeps_custom_provider_and_explicit_refresh(monkeypatch):
    finder = _MemoryFinder()
    monkeypatch.setattr(sys, "meta_path", [finder])
    snapshot = probe.discover("grouped")
    assert finder.calls == 1
    finder.names.append("memory_late")
    fresh = probe.discover("grouped")
    assert finder.calls == 2
    assert len(snapshot[probe.GROUPS[0]]) == 1
    assert [ep.dist.name for ep in fresh[probe.GROUPS[0]]] == [
        "memory_initial",
        "memory_late",
    ]
    assert "plugin_that_must_not_load" not in sys.modules


def test_grouped_query_preserves_zip_layout_and_duplicate_distribution_rule(
    tmp_path, monkeypatch
):
    archive = tmp_path / "pack.zip"
    with zipfile.ZipFile(archive, "w") as zipped:
        for filename, text in _metadata("same_dist", "zip_plugin:register").items():
            zipped.writestr(f"same_dist-1.0.dist-info/{filename}", text)
    site = tmp_path / "site"
    _install_metadata(site, "same_dist", "directory_plugin:register")
    monkeypatch.setattr(sys, "path", [str(archive), str(site)])
    separate = probe.discover("separate")
    grouped = probe.discover("grouped")
    assert _identities(grouped) == _identities(separate)
    assert len(grouped[probe.GROUPS[1]]) == 1
    assert grouped[probe.GROUPS[1]][0].value == "zip_plugin:register"
    assert "zip_plugin" not in sys.modules


def test_single_demand_does_one_fresh_query_and_does_not_select_other_group(
    monkeypatch,
):
    finder = _MemoryFinder()
    monkeypatch.setattr(sys, "meta_path", [finder])
    result = probe.discover("single")
    assert finder.calls == 1
    assert list(result) == [probe.GROUPS[1]]
    assert len(result[probe.GROUPS[1]]) == 1


def test_discovery_probe_refuses_an_unknown_mode():
    with pytest.raises(ValueError, match="Unsupported discovery mode"):
        probe.discover("cached_forever")
