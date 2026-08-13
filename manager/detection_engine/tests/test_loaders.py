"""
Tests for loader error paths in vuln_db.py and enrichment_db.py.

These are the boundary-condition cases that must never silently produce
wrong output:
  - missing file → FileNotFoundError
  - tampered snapshot (content_hash mismatch) → ValueError
  - completely malformed JSON → propagated as json.JSONDecodeError or
    similar (any exception other than a silent empty result is correct)

All tests use tmp_path fixtures — no real snapshot files are touched.
"""
from __future__ import annotations

import json

import pytest

import enrichment_db
import vuln_db
from vuln_db import _content_hash


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _valid_snapshot(records: dict) -> dict:
    return {
        "fetched_at": "2026-01-01T00:00:00Z",
        "ecosystem": "Debian:12",
        "products": sorted(records),
        "content_hash": _content_hash(records),
        "records": records,
    }


def _write_snapshot(path, records: dict) -> None:
    path.write_text(json.dumps(_valid_snapshot(records)))


def _valid_kev() -> dict:
    return {"cve_ids": ["CVE-2021-44228"], "fetched_at": "2026-01-01T00:00:00Z"}


def _valid_epss() -> dict:
    return {"scores": {"CVE-2021-44228": {"epss": 0.97, "percentile": 0.99}},
            "fetched_at": "2026-01-01T00:00:00Z"}


# ---------------------------------------------------------------------------
# C3-1: vuln_db.load_snapshot error paths
# ---------------------------------------------------------------------------

class TestLoadSnapshotErrors:
    def setup_method(self):
        vuln_db._clear_caches()

    def test_missing_file_raises_file_not_found(self, tmp_path):
        """A path that doesn't exist must raise FileNotFoundError with a
        helpful message (not a generic IOError or a silent empty result)."""
        with pytest.raises(FileNotFoundError):
            vuln_db.load_snapshot(tmp_path / "nonexistent.json")

    def test_content_hash_mismatch_raises_value_error(self, tmp_path):
        """A snapshot whose records don't match the stored content_hash must
        raise ValueError — the file was modified after being written and
        must not be trusted."""
        p = tmp_path / "snap.json"
        snap = _valid_snapshot({"nginx": []})
        # Tamper: change the hash so it no longer matches the records
        snap["content_hash"] = "deadbeef" * 8
        p.write_text(json.dumps(snap))
        with pytest.raises(ValueError, match="content-hash"):
            vuln_db.load_snapshot(p)

    def test_malformed_json_raises(self, tmp_path):
        """Completely broken JSON must propagate as an exception — never
        silently yield an empty database."""
        p = tmp_path / "snap.json"
        p.write_text("{this is not json}")
        with pytest.raises(Exception):  # json.JSONDecodeError or similar
            vuln_db.load_snapshot(p)

    def test_missing_required_key_raises(self, tmp_path):
        """A JSON file that is valid JSON but missing the 'records' key
        must raise (KeyError or similar), not silently return an empty db."""
        p = tmp_path / "snap.json"
        p.write_text(json.dumps({"fetched_at": "t", "content_hash": "x"}))
        with pytest.raises(Exception):
            vuln_db.load_snapshot(p)

    def test_valid_snapshot_loads_cleanly(self, tmp_path):
        """A well-formed snapshot must load without error and return a VulnDB
        that covers the products it was built with."""
        p = tmp_path / "snap.json"
        _write_snapshot(p, {"nginx": []})
        db = vuln_db.load_snapshot(p)
        assert db.covers("nginx")

    def test_error_message_mentions_re_sync(self, tmp_path):
        """The FileNotFoundError message should mention re-syncing, so
        operators know what to do (not just a generic 'file not found')."""
        with pytest.raises(FileNotFoundError, match="sync"):
            vuln_db.load_snapshot(tmp_path / "missing.json")

    def test_hash_mismatch_message_truncates_hash(self, tmp_path):
        """The ValueError for a hash mismatch must include truncated hashes
        in the message so operators can see at a glance what diverged."""
        p = tmp_path / "snap.json"
        snap = _valid_snapshot({"nginx": []})
        snap["content_hash"] = "a" * 64  # valid length, wrong value
        p.write_text(json.dumps(snap))
        with pytest.raises(ValueError) as exc_info:
            vuln_db.load_snapshot(p)
        msg = str(exc_info.value)
        assert "aaaaaaaaaaaa" in msg  # truncated expected hash appears


# ---------------------------------------------------------------------------
# C3-2: enrichment_db.load_kev error paths
# ---------------------------------------------------------------------------

class TestLoadKevErrors:
    def setup_method(self):
        enrichment_db._clear_caches()

    def test_missing_kev_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError)):
            enrichment_db.load_kev(tmp_path / "nonexistent_kev.json")

    def test_malformed_kev_json_raises(self, tmp_path):
        p = tmp_path / "kev.json"
        p.write_text("{bad json")
        with pytest.raises(Exception):
            enrichment_db.load_kev(p)

    def test_valid_kev_loads(self, tmp_path):
        p = tmp_path / "kev.json"
        p.write_text(json.dumps(_valid_kev()))
        db = enrichment_db.load_kev(p)
        assert db.is_kev("CVE-2021-44228")
        assert not db.is_kev("CVE-2099-99999")


# ---------------------------------------------------------------------------
# C3-3: enrichment_db.load_epss error paths
# ---------------------------------------------------------------------------

class TestLoadEpssErrors:
    def setup_method(self):
        enrichment_db._clear_caches()

    def test_missing_epss_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError)):
            enrichment_db.load_epss(tmp_path / "nonexistent_epss.json")

    def test_malformed_epss_json_raises(self, tmp_path):
        p = tmp_path / "epss.json"
        p.write_text("not-json-at-all")
        with pytest.raises(Exception):
            enrichment_db.load_epss(p)

    def test_valid_epss_loads(self, tmp_path):
        p = tmp_path / "epss.json"
        p.write_text(json.dumps(_valid_epss()))
        db = enrichment_db.load_epss(p)
        score = db.get("CVE-2021-44228")
        assert score is not None
        assert score["epss"] == pytest.approx(0.97)

    def test_epss_get_returns_none_for_unknown_cve(self, tmp_path):
        p = tmp_path / "epss.json"
        p.write_text(json.dumps(_valid_epss()))
        db = enrichment_db.load_epss(p)
        assert db.get("CVE-9999-00000") is None
