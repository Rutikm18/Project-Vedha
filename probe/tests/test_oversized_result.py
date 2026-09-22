"""
B3 — an oversized result must be quarantined, not retried forever.

THE WEDGE THIS REMOVES
----------------------
413 was classified retryable, alongside 401/403. For those two that is right:
a token refresh makes the next attempt succeed. For 413 it cannot, because
nothing about the attempt changes — the payload is the same size and the
manager's ceiling is the same ceiling (32 MB compressed / 128 MB inflated, see
main.py _GZIP_MAX_*). So the probe retried an impossible upload on every poll:

    submit_result -> 413 -> False -> stays spooled -> retried -> 413 -> ...

The spool then filled (512 MB / 1024 files), and `ResultSpool.at_capacity`
stops the poll loop claiming ANY new job:

    if spool.at_capacity: say("...pausing new jobs until uploads recover.")
    else:                 jobs = _poll_jobs_or_empty(...)

One oversized result therefore took the probe out of service permanently. It
kept heartbeating and looked online, and did nothing, forever.

WHY QUARANTINE IS NOT DATA LOSS
-------------------------------
The existing test that pinned 413 as retryable justified it as "no data loss".
Quarantine preserves that property by a different route: the payload is MOVED
to <spool>/rejected/<job>.json, intact, where an operator can resubmit it after
raising the limit. What it stops being is a permanent blocker on the retry
queue. Crucially the rejected/ subdirectory is outside the `*.json` glob that
feeds spool_count/spool_bytes, so quarantining genuinely frees capacity.
"""
from __future__ import annotations

import json
import logging
from unittest.mock import MagicMock

import pytest

from agent.result_spool import PERMANENT_REJECTION, ResultSpool
from agent.transport import Transport


@pytest.fixture
def transport():
    tr = Transport.__new__(Transport)
    tr._agent_id = "a1"
    tr._compress_over = 0
    tr._client = MagicMock()
    return tr


@pytest.fixture(autouse=True)
def _no_auth(monkeypatch):
    monkeypatch.setattr(Transport, "auth_header", property(lambda self: {}))
    monkeypatch.setattr(Transport, "ensure_device_access", lambda self: True)


# ── classification ──────────────────────────────────────────────────────────

def test_413_is_permanent_not_retryable(transport):
    """The headline. Retrying an unchanged payload cannot change the verdict."""
    transport._client.post.return_value = MagicMock(status_code=413)
    assert transport.submit_result("job-1", {"success": True}) == PERMANENT_REJECTION


def test_401_and_403_stay_retryable(transport):
    """A refreshed token genuinely makes the next attempt succeed."""
    for code in (401, 403):
        transport._client.post.return_value = MagicMock(status_code=code)
        assert transport.submit_result("job-1", {"success": True}) is False, code


def test_5xx_stays_retryable(transport):
    transport._client.post.return_value = MagicMock(status_code=500)
    assert transport.submit_result("job-1", {"success": True}) is False


def test_the_other_permanent_codes_are_unchanged(transport):
    for code in (400, 404, 409, 422):
        transport._client.post.return_value = MagicMock(status_code=code)
        assert (transport.submit_result("job-1", {"success": True})
                == PERMANENT_REJECTION), code


def test_the_413_log_says_how_big_and_where_it_went(transport, caplog):
    """An operator has to act on this from the MANAGER side, so the message
    must carry the size that was refused and the path to the kept copy."""
    transport._client.post.return_value = MagicMock(status_code=413)
    with caplog.at_level(logging.ERROR, logger="transport"):
        transport.submit_result("job-1", {"success": True, "result": {"facts": []}})
    msg = " ".join(r.getMessage() for r in caplog.records)
    assert "413" in msg or "too large" in msg.lower()
    assert "bytes" in msg.lower()
    assert "rejected" in msg.lower() or "quarantin" in msg.lower()


# ── the wedge is gone ───────────────────────────────────────────────────────

class TestTheProbeKeepsWorking:
    def _spool(self, tmp_path, **kw):
        return ResultSpool(tmp_path / "spool", max_retries=2,
                           retry_delay_sec=0, **kw)

    def test_an_oversized_result_is_quarantined_on_the_first_attempt(self, tmp_path):
        spool = self._spool(tmp_path)
        attempts = []

        def _upload(job_id, payload):
            attempts.append(job_id)
            return PERMANENT_REJECTION

        assert spool.submit_with_retry("job-1", {"a": 1}, _upload) is False
        assert len(attempts) == 1, "a permanent rejection must not be retried"

    def test_the_payload_is_preserved_for_resubmission(self, tmp_path):
        spool = self._spool(tmp_path)
        spool.submit_with_retry("job-1", {"facts": ["keep me"]},
                                lambda j, p: PERMANENT_REJECTION)
        kept = tmp_path / "spool" / "rejected" / "job-1.json"
        assert kept.exists(), "quarantine must not destroy the evidence"
        assert json.loads(kept.read_text())["facts"] == ["keep me"]

    def test_quarantined_results_do_not_count_toward_capacity(self, tmp_path):
        """The whole point: the probe must still accept new jobs."""
        spool = self._spool(tmp_path, max_files=3)
        for n in range(10):
            spool.submit_with_retry(f"job-{n}", {"n": n},
                                    lambda j, p: PERMANENT_REJECTION)
        assert spool.spool_count == 0
        assert spool.at_capacity is False

    def test_by_contrast_retryable_failures_do_fill_the_spool(self, tmp_path):
        """Pinning the contrast: this is the behaviour 413 used to get, and it
        is correct for a real outage — you should stop taking on new work you
        cannot deliver. It is only wrong when retrying can never succeed."""
        spool = self._spool(tmp_path, max_files=3)
        for n in range(4):
            spool.submit_with_retry(f"job-{n}", {"n": n}, lambda j, p: False)
        assert spool.spool_count == 4
        assert spool.at_capacity is True

    def test_a_flushed_spool_also_quarantines_instead_of_looping(self, tmp_path):
        """The poll loop re-flushes spooled results every cycle; that path
        needs the same verdict or the loop just moves there."""
        spool = self._spool(tmp_path)
        spool.save("job-1", {"a": 1})
        assert spool.spool_count == 1
        spool.flush_spool(lambda j, p: PERMANENT_REJECTION)
        assert spool.spool_count == 0
        assert (tmp_path / "spool" / "rejected" / "job-1.json").exists()
