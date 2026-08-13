"""
Tests for the P1+P2 performance optimization of the detection engine.

P1 — version comparison runs in-process (pure-Python), never shelling out to
     the `dpkg` binary per comparison; a load-time guard cross-checks
     pure-Python against dpkg once per snapshot.
P2 — the pinned snapshots (OSV / KEV / EPSS) are loaded once and memoized by
     file mtime, not re-parsed + re-hashed on every call.

See docs/superpowers/specs/2026-08-10-detection-engine-perf-optimization-design.md
"""
import json
import os
import time

import pytest

import enrichment_db
import version_compare as vc
import vuln_db


# ---------------------------------------------------------------------------
# Phase 1 — P1 hot path: dpkg_compare must not spawn a subprocess
# ---------------------------------------------------------------------------
def test_dpkg_compare_does_not_call_the_binary(monkeypatch):
    """dpkg_compare must use the pure-Python comparator in the hot path.
    Shelling out to `dpkg --compare-versions` is ~2,753x slower per call and
    runs in the matcher's innermost loop."""
    def _forbidden(a, b):
        raise AssertionError(
            "dpkg_compare shelled out to the dpkg binary in the hot path")
    monkeypatch.setattr(vc, "_dpkg_compare_via_binary", _forbidden)

    # Correctness is preserved without the binary — including the fiddly rules
    # (tilde pre-release, epoch dominance) that motivated preferring dpkg.
    assert vc.dpkg_compare("1.0", "1.1") == -1
    assert vc.dpkg_compare("1.0", "1.0") == 0
    assert vc.dpkg_compare("2.0", "1.0") == 1
    assert vc.dpkg_compare("1.0~beta1", "1.0") == -1
    assert vc.dpkg_compare("1:1.0", "2.0") == 1
    assert vc.dpkg_compare("8.4p1-5+deb11u1", "8.4p1-6+deb11u1") == -1


# ---------------------------------------------------------------------------
# Phase 2 — P1 load-time guard: verify_pure_python_matches_dpkg
# ---------------------------------------------------------------------------
@pytest.fixture
def clean_guard_cache(tmp_path, monkeypatch):
    """Isolate the guard's in-memory + on-disk validation cache per test."""
    monkeypatch.setattr(vc, "_VALIDATION_MARKER_PATH", tmp_path / ".dpkg_validation.json")
    vc._clear_validation_cache()
    yield
    vc._clear_validation_cache()


def test_guard_is_noop_without_dpkg(clean_guard_cache, monkeypatch):
    """No dpkg binary → nothing to cross-check against; return [] and never
    attempt to call the binary (pure-Python is all there is anyway)."""
    monkeypatch.setattr(vc, "_HAVE_DPKG", False)
    def _forbidden(a, b):
        raise AssertionError("guard called the dpkg binary while _HAVE_DPKG is False")
    monkeypatch.setattr(vc, "_dpkg_compare_via_binary", _forbidden)
    assert vc.verify_pure_python_matches_dpkg(["1.0", "2.0"], cache_key="k") == []


def test_guard_passes_when_pure_python_agrees_with_dpkg(clean_guard_cache):
    if not vc._HAVE_DPKG:
        pytest.skip("dpkg not installed on this machine")
    versions = ["1.0", "1.1", "2.4.52-1", "2.4.54-1", "1.0~beta1",
                "8.4p1-5+deb11u1", "1:3.9p1-1"]
    assert vc.verify_pure_python_matches_dpkg(versions, cache_key="agree") == []


def test_guard_reports_divergence_and_warns(clean_guard_cache, monkeypatch, caplog):
    """When the binary disagrees with pure-Python on an adjacent pair, that pair
    is returned and a loud warning is logged (detection is NOT broken)."""
    monkeypatch.setattr(vc, "_HAVE_DPKG", True)
    monkeypatch.setattr(vc, "_dpkg_compare_via_binary", lambda a, b: 1)  # always "a>b"
    with caplog.at_level("WARNING"):
        div = vc.verify_pure_python_matches_dpkg(["1.0", "2.0"], cache_key="diverge")
    assert ("1.0", "2.0") in div
    assert "divergence" in caplog.text


def test_guard_validates_once_per_cache_key(clean_guard_cache, monkeypatch):
    calls = {"n": 0}
    def _counting(a, b):
        calls["n"] += 1
        return (a > b) - (a < b)
    monkeypatch.setattr(vc, "_HAVE_DPKG", True)
    monkeypatch.setattr(vc, "_dpkg_compare_via_binary", _counting)
    vc.verify_pure_python_matches_dpkg(["1.0", "2.0", "3.0"], cache_key="once")
    first = calls["n"]
    assert first > 0
    vc.verify_pure_python_matches_dpkg(["1.0", "2.0", "3.0"], cache_key="once")
    assert calls["n"] == first  # second call short-circuited by the cache


# ---------------------------------------------------------------------------
# Phase 3 — P2: snapshot loaders memoize by file mtime
# ---------------------------------------------------------------------------
def _write_snapshot(path, records):
    snap = {
        "fetched_at": "2026-01-01T00:00:00Z",
        "ecosystem": "Debian:12",
        "products": sorted(records),
        "content_hash": vuln_db._content_hash(records),
        "records": records,
    }
    path.write_text(json.dumps(snap))


def test_load_snapshot_memoized_returns_same_instance(tmp_path):
    vuln_db._clear_caches()
    p = tmp_path / "snap.json"
    _write_snapshot(p, {"nginx": []})
    assert vuln_db.load_snapshot(p) is vuln_db.load_snapshot(p)


def test_load_snapshot_reloads_after_file_change(tmp_path):
    vuln_db._clear_caches()
    p = tmp_path / "snap.json"
    _write_snapshot(p, {"nginx": []})
    db1 = vuln_db.load_snapshot(p)
    _write_snapshot(p, {"nginx": [], "openssl": []})
    os.utime(p, (time.time() + 5, time.time() + 5))  # ensure a distinctly newer mtime
    db2 = vuln_db.load_snapshot(p)
    assert db2 is not db1
    assert db2.covers("openssl")


def test_clear_caches_forces_reload(tmp_path):
    vuln_db._clear_caches()
    p = tmp_path / "snap.json"
    _write_snapshot(p, {"nginx": []})
    db1 = vuln_db.load_snapshot(p)
    vuln_db._clear_caches()
    assert vuln_db.load_snapshot(p) is not db1


def test_load_kev_and_epss_memoized(tmp_path):
    enrichment_db._clear_caches()
    kev = tmp_path / "kev.json"
    kev.write_text(json.dumps({"cve_ids": ["CVE-2021-1"], "fetched_at": "t"}))
    assert enrichment_db.load_kev(kev) is enrichment_db.load_kev(kev)

    epss = tmp_path / "epss.json"
    epss.write_text(json.dumps(
        {"scores": {"CVE-2021-1": {"epss": 0.5, "percentile": 0.9}}, "fetched_at": "t"}))
    assert enrichment_db.load_epss(epss) is enrichment_db.load_epss(epss)


def test_load_snapshot_runs_dpkg_guard_once_keyed_by_content_hash(tmp_path, monkeypatch):
    vuln_db._clear_caches()
    calls = []
    monkeypatch.setattr(vuln_db, "verify_pure_python_matches_dpkg",
                        lambda versions, cache_key: calls.append((set(versions), cache_key)) or [])
    p = tmp_path / "snap.json"
    records = {"nginx": [{"id": "CVE-x", "affected": [
        {"package": {"name": "nginx"},
         "ranges": [{"type": "ECOSYSTEM",
                     "events": [{"introduced": "1.0"}, {"fixed": "1.2"}]}]}]}]}
    _write_snapshot(p, records)
    db = vuln_db.load_snapshot(p)

    assert len(calls) == 1
    boundary_versions, cache_key = calls[0]
    assert {"1.0", "1.2"} <= boundary_versions
    assert cache_key == db.meta.content_hash
