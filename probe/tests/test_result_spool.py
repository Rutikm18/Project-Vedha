"""Tests for agent/result_spool.py"""
from __future__ import annotations

import json

import pytest

from agent.result_spool import ResultSpool


@pytest.fixture
def spool(tmp_path):
    """ResultSpool with tiny retry delay for fast tests."""
    return ResultSpool(spool_dir=tmp_path / "spool", max_retries=3, retry_delay_sec=0.05)


class TestResultSpool:
    def test_save_and_load(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        payload = {"success": True, "result": {"hosts": []}}
        spool.save("job-123", payload)
        loaded = spool.load("job-123")
        assert loaded == payload

    def test_save_is_atomic_no_temp_leftover(self, tmp_path):
        # Atomic write: final file present + loadable, no orphan .tmp, and the
        # temp file is excluded from the spool count / globs.
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        payload = {"success": True, "result": {"facts": [1, 2, 3]}}
        p = spool.save("job-atomic", payload)
        assert p.exists()
        assert not (spool.spool_dir / "job-atomic.json.tmp").exists()
        assert spool.load("job-atomic") == payload
        assert spool.spool_count == 1

    def test_load_missing(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        assert spool.load("nonexistent") is None

    def test_load_corrupt(self, tmp_path):
        d = tmp_path / "spool"
        d.mkdir(parents=True)
        (d / "bad.json").write_text("not-json")
        spool = ResultSpool(spool_dir=d)
        assert spool.load("bad") is None

    def test_exists(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        spool.save("job-1", {})
        assert spool.exists("job-1") is True
        assert spool.exists("nonexistent") is False

    def test_remove(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        spool.save("job-1", {})
        spool.remove("job-1")
        assert spool.exists("job-1") is False

    def test_remove_missing(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        spool.remove("nonexistent")  # should not raise

    def test_spool_count(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        assert spool.spool_count == 0
        spool.save("job-1", {})
        spool.save("job-2", {})
        assert spool.spool_count == 2

    def test_submit_with_retry_success(self, spool):
        calls = []

        def upload_fn(jid, payload):
            calls.append((jid, payload))
            return True

        result = spool.submit_with_retry("job-1", {"data": 42}, upload_fn)
        assert result is True
        assert len(calls) == 1
        # Spool file should be removed after success
        assert spool.exists("job-1") is False

    def test_submit_with_retry_failure(self, spool):
        calls = []

        def upload_fn(jid, payload):
            calls.append((jid, payload))
            return False

        result = spool.submit_with_retry("job-1", {"data": 42}, upload_fn)
        assert result is False
        assert len(calls) == spool.max_retries
        # Spool file should remain
        assert spool.exists("job-1") is True

    def test_submit_with_retry_exception(self, spool):
        def upload_fn(jid, payload):
            raise ConnectionError("network down")

        result = spool.submit_with_retry("job-1", {"data": 42}, upload_fn)
        assert result is False
        assert spool.exists("job-1") is True

    def test_flush_spool_empty(self, spool):
        flushed = spool.flush_spool(lambda jid, p: True)
        assert flushed == 0

    def test_flush_spool_with_pending(self, spool):
        spool.save("job-1", {"result": 1})
        spool.save("job-2", {"result": 2})

        uploaded = set()

        def upload_fn(jid, payload):
            uploaded.add(jid)
            return True

        flushed = spool.flush_spool(upload_fn)
        assert flushed == 2
        assert uploaded == {"job-1", "job-2"}
        assert spool.spool_count == 0

    def test_flush_spool_partial(self, spool):
        spool.save("job-1", {"result": 1})
        spool.save("job-2", {"result": 2})

        def upload_fn(jid, payload):
            return jid == "job-1"

        flushed = spool.flush_spool(upload_fn)
        assert flushed == 1
        assert spool.exists("job-1") is False
        assert spool.exists("job-2") is True

    def test_max_retries_uses_class_default(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool")
        assert spool.max_retries == 5

    def test_custom_retry_config(self, tmp_path):
        spool = ResultSpool(spool_dir=tmp_path / "spool", max_retries=2, retry_delay_sec=0.1)
        assert spool.max_retries == 2
