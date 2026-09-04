"""
test_host_health.py — mid-scan target-offline detection.

The interesting cases here are all about NOT crying wolf. A firewalled host, a
host whose branches simply don't apply, and a host that answers with RST all look
like failure from a naive failure counter, and none of them are offline. The
tests below pin the distinctions that keep the feature trustworthy, plus the
safety property that makes it worth having: a host we stopped scanning is never
reported as a host with nothing wrong.
"""

from __future__ import annotations

import asyncio

import pytest

from scanner.scanner_base import ScanResult
from workflow.host_health import (
    HostHealthMonitor, VERDICT_FLAKY, VERDICT_OFFLINE,
)


def _r(status, *, scanner="smb_scan", target="10.0.0.5", port=445, **data):
    return ScanResult(scanner, target, port=port, status=status, data=data or {})


def _monitor(alive: bool, *, threshold=2, on_probe=None):
    async def probe(host):
        if on_probe:
            on_probe(host)
        return alive
    return HostHealthMonitor(probe, strike_threshold=threshold)


class TestSilenceDetection:
    def test_rst_is_contact_not_silence(self):
        """A closed port is the host's own stack answering — positive proof of
        life. Counting it as a failure would flag every hardened host."""
        assert HostHealthMonitor._is_silence([_r("closed")]) is False

    def test_open_and_observed_are_contact(self):
        assert HostHealthMonitor._is_silence([_r("open")]) is False
        assert HostHealthMonitor._is_silence([_r("observed")]) is False

    def test_unreachable_is_silence(self):
        assert HostHealthMonitor._is_silence([_r("unreachable")]) is True

    def test_filtered_is_silence_but_only_suspicion(self):
        assert HostHealthMonitor._is_silence([_r("filtered")]) is True

    def test_transport_error_code_is_silence(self):
        assert HostHealthMonitor._is_silence(
            [_r("error", error_code="scanner_timeout")]) is True

    def test_no_results_is_not_silence(self):
        """A branch that declined to run says nothing about the host."""
        assert HostHealthMonitor._is_silence([]) is False

    def test_any_contact_beats_many_failures(self):
        results = [_r("filtered"), _r("unreachable"), _r("open")]
        assert HostHealthMonitor._is_silence(results) is False


class TestStrikeAccounting:
    def test_strikes_must_be_consecutive(self):
        """A healthy host with many inapplicable branches must never accumulate
        its way to a verdict."""
        m = _monitor(alive=True, threshold=2)
        m.observe("10.0.0.5", "smb_scan", [_r("filtered")])
        m.observe("10.0.0.5", "ssh_scan", [_r("open")])       # contact resets
        m.observe("10.0.0.5", "ldap_scan", [_r("filtered")])
        assert m.suspect("10.0.0.5") is False

    def test_threshold_reached_raises_suspicion_only(self):
        m = _monitor(alive=True, threshold=2)
        m.observe("10.0.0.5", "smb_scan", [_r("filtered")])
        m.observe("10.0.0.5", "ssh_scan", [_r("unreachable")])
        assert m.suspect("10.0.0.5") is True
        assert m.is_offline("10.0.0.5") is False, "suspicion is not a verdict"


class TestVerdict:
    def test_firewalled_host_that_still_answers_is_flaky_not_offline(self):
        """The headline false positive: silence from every branch, but the host
        is up. Must NOT abort, and must say why."""
        m = _monitor(alive=True, threshold=2)
        m.observe("10.0.0.5", "smb_scan", [_r("filtered")])
        m.observe("10.0.0.5", "ssh_scan", [_r("filtered")])
        assert asyncio.run(m.confirm("10.0.0.5")) == VERDICT_FLAKY
        assert m.is_offline("10.0.0.5") is False
        assert m.offline_hosts() == []
        fact = m.finalize()[0]
        assert fact.data["went_offline"] is False
        assert fact.data["scan_complete"] is True
        assert "filtered" in fact.evidence or "throttled" in fact.evidence

    def test_host_that_stopped_answering_is_offline(self):
        m = _monitor(alive=False, threshold=2)
        m.observe("10.0.0.5", "smb_scan", [_r("unreachable")])
        m.observe("10.0.0.5", "ssh_scan", [_r("unreachable")])
        assert asyncio.run(m.confirm("10.0.0.5")) == VERDICT_OFFLINE
        assert m.is_offline("10.0.0.5") is True
        assert m.offline_hosts() == ["10.0.0.5"]

    def test_no_recheck_is_spent_below_threshold(self):
        calls: list[str] = []
        m = _monitor(alive=False, threshold=3, on_probe=calls.append)
        m.observe("10.0.0.5", "smb_scan", [_r("unreachable")])
        assert asyncio.run(m.confirm("10.0.0.5")) is None
        assert calls == [], "a re-check costs a probe; don't spend it on one strike"

    def test_a_broken_liveness_probe_never_aborts_the_scan(self):
        async def boom(host):
            raise OSError("no raw socket")
        m = HostHealthMonitor(boom, strike_threshold=1)
        m.observe("10.0.0.5", "smb_scan", [_r("unreachable")])
        assert asyncio.run(m.confirm("10.0.0.5")) is None
        assert m.is_offline("10.0.0.5") is False

    def test_flaky_host_can_be_suspected_again_later(self):
        """One false alarm must not disable the check for the rest of the scan."""
        m = _monitor(alive=True, threshold=1)
        m.observe("10.0.0.5", "smb_scan", [_r("filtered")])
        assert asyncio.run(m.confirm("10.0.0.5")) == VERDICT_FLAKY
        m.observe("10.0.0.5", "ldap_scan", [_r("filtered")])
        assert m.suspect("10.0.0.5") is True


class TestSafetyProperty:
    def test_offline_fact_marks_the_scan_incomplete_and_names_what_was_skipped(self):
        """The whole point: 'we stopped early' must never read as 'nothing found'."""
        m = _monitor(alive=False, threshold=1)
        m.observe("10.0.0.5", "smb_scan", [_r("open")])          # this one worked
        m.observe("10.0.0.5", "ssh_scan", [_r("unreachable")])
        asyncio.run(m.confirm("10.0.0.5"))
        m.note_skipped("10.0.0.5", "tls_scan")
        m.note_skipped("10.0.0.5", "web_scan")

        fact = [f for f in m.finalize() if f.data.get("went_offline")][0]
        assert fact.status == "unreachable"
        assert fact.data["scan_complete"] is False
        assert fact.data["error_code"] == "target_went_offline"
        assert fact.data["retryable"] is True
        assert fact.data["skipped_components"] == ["tls_scan", "web_scan"]
        assert "smb_scan" in fact.data["completed_components"]
        assert fact.data["remediation"]

    def test_offline_host_stops_accumulating_observations(self):
        m = _monitor(alive=False, threshold=1)
        m.observe("10.0.0.5", "smb_scan", [_r("unreachable")])
        asyncio.run(m.confirm("10.0.0.5"))
        m.observe("10.0.0.5", "ssh_scan", [_r("open")])
        assert m.is_offline("10.0.0.5") is True, "a verdict is not undone by later noise"

    def test_healthy_host_produces_no_facts_at_all(self):
        m = _monitor(alive=True, threshold=2)
        m.observe("10.0.0.5", "smb_scan", [_r("open")])
        m.observe("10.0.0.5", "ssh_scan", [_r("closed")])
        assert m.finalize() == []
        assert m.offline_hosts() == []

    def test_one_offline_host_does_not_implicate_its_peers(self):
        m = _monitor(alive=False, threshold=1)
        m.observe("10.0.0.5", "smb_scan", [_r("unreachable", target="10.0.0.5")])
        m.observe("10.0.0.9", "smb_scan", [_r("open", target="10.0.0.9")])
        asyncio.run(m.confirm("10.0.0.5"))
        assert m.offline_hosts() == ["10.0.0.5"]
        assert m.is_offline("10.0.0.9") is False


class TestConfiguration:
    def test_threshold_is_tunable_by_env(self, monkeypatch):
        monkeypatch.setenv("PROBE_OFFLINE_STRIKES", "5")
        m = HostHealthMonitor(lambda h: None)
        assert m._threshold == 5

    @pytest.mark.parametrize("bad", ["", "abc", "0", "-3"])
    def test_bad_threshold_falls_back_to_a_sane_value(self, monkeypatch, bad):
        monkeypatch.setenv("PROBE_OFFLINE_STRIKES", bad)
        m = HostHealthMonitor(lambda h: None)
        assert m._threshold >= 1


class TestUdpNoReplyIsNotContact:
    """Regression: "open|filtered" is the UDP no-reply verdict, not an open port.
    Reading it as contact (by splitting on the pipe) meant a host that had already
    been powered off still looked like it was answering, and the monitor never
    raised a strike. Caught by killing a lab container mid-scan and getting no
    detection at all."""

    def test_udp_no_reply_counts_as_silence(self):
        assert HostHealthMonitor._is_silence([_r("open|filtered")]) is True

    def test_a_real_open_port_still_counts_as_contact(self):
        assert HostHealthMonitor._is_silence([_r("open")]) is False

    def test_mixed_udp_silence_and_a_real_open_port_is_contact(self):
        assert HostHealthMonitor._is_silence([_r("open|filtered"), _r("open")]) is False


class TestHeartbeat:
    """The primary detector. Branch-failure evidence covers only the milliseconds
    the TCP branches take; the heartbeat covers the whole scan, including the
    datagram tail where most of the wall time actually goes."""

    def test_declares_offline_after_consecutive_misses(self):
        m = _monitor(alive=False, threshold=99)
        asyncio.run(m.watch("10.0.0.5", interval=0.01, misses=2))
        assert m.is_offline("10.0.0.5") is True
        fact = [f for f in m.finalize() if f.data.get("went_offline")][0]
        assert fact.data["detected_by"] == "heartbeat"
        assert "heartbeat" in fact.data["detection_reason"]

    def test_a_single_miss_is_not_enough(self):
        replies = iter([False, True, True, True])

        async def probe(host):
            return next(replies, True)

        m = HostHealthMonitor(probe, strike_threshold=99)

        async def _run():
            task = asyncio.create_task(m.watch("10.0.0.5", interval=0.01, misses=2))
            await asyncio.sleep(0.08)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(_run())
        assert m.is_offline("10.0.0.5") is False, "one blip must not condemn a host"

    def test_healthy_host_is_never_marked(self):
        m = _monitor(alive=True, threshold=99)

        async def _run():
            task = asyncio.create_task(m.watch("10.0.0.5", interval=0.01, misses=2))
            await asyncio.sleep(0.08)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(_run())
        assert m.is_offline("10.0.0.5") is False
        assert m.finalize() == []

    def test_cancellation_is_clean(self):
        m = _monitor(alive=True, threshold=99)

        async def _run():
            task = asyncio.create_task(m.watch("10.0.0.5", interval=5))
            await asyncio.sleep(0)
            task.cancel()
            await task          # watch() swallows CancelledError and returns

        asyncio.run(_run())

    def test_a_broken_probe_never_condemns_a_host(self):
        async def boom(host):
            raise OSError("no socket")
        m = HostHealthMonitor(boom, strike_threshold=99)

        async def _run():
            task = asyncio.create_task(m.watch("10.0.0.5", interval=0.01, misses=1))
            await asyncio.sleep(0.06)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        asyncio.run(_run())
        assert m.is_offline("10.0.0.5") is False


class TestOperatorVisibility:
    """An offline host must reach the operator's screen, not just the fact list.
    ExecutionTrace turns a result into an issues[] entry only when it carries an
    `error`, so without one the whole event was invisible in the run summary and
    the run still claimed outcome=completed."""

    def test_offline_fact_carries_an_error_so_it_becomes_an_issue(self):
        m = _monitor(alive=False, threshold=1)
        m.observe("10.0.0.5", "smb_scan", [_r("unreachable")])
        asyncio.run(m.confirm("10.0.0.5"))
        fact = [f for f in m.finalize() if f.data.get("went_offline")][0]
        assert fact.error, "no error field => no issues[] entry => invisible to the operator"
        assert "target_went_offline" in fact.error

    def test_flaky_note_is_not_an_error(self):
        """A host that is merely filtered is not a problem with the run."""
        m = _monitor(alive=True, threshold=1)
        m.observe("10.0.0.5", "smb_scan", [_r("filtered")])
        asyncio.run(m.confirm("10.0.0.5"))
        fact = m.finalize()[0]
        assert not fact.error
