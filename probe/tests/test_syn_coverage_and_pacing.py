"""
test_syn_coverage_and_pacing.py — Wave D: make the raw SYN path truthful
about coverage, and make it hold its configured packet rate across
concurrent hosts.

Defects pinned here:

  R1  The raw path emitted no scan_summary at all. On a privileged Linux
      probe a host cut short by the job's tail budget was indistinguishable
      from one that finished — the exact false-completeness this whole
      workstream removes on the connect path.
  R2  `attempts_by_port` used to count a port BEFORE the sendto() that could
      fail, so a port whose every send raised OSError still looked "probed"
      and, under --report-closed, was reported `filtered` — a scanner-side
      failure dressed up as a target firewall.
  R3  `SendPacer.max_rate` defaulted to 4x the requested rate, so admission's
      approved envelope was not actually the ceiling. `pace()` also read and
      wrote `self._next` without a lock, so threads sharing one pacer could
      compute the SAME slot and fire together.
  R4  AIMD ran on the scanner's ONE shared pacer, so a single host that
      silently drops closed-port SYNs (routine for a Windows firewall) halved
      the rate for every other host scanned beside it.

Raw sockets can't run in CI, so the send/receive path is driven through the
same fake-socket harness the existing SYN tests use (`_syn_scan_blocking`),
and `_build_results` is exercised directly wherever no socket is needed at
all.
"""
from __future__ import annotations

import socket
import threading
import time

import pytest

from scanner import syn_scanner as ss
from scanner.scanner_base import ScopeGuard, SendPacer

KEY = b"0123456789abcdef"


def _scope():
    return ScopeGuard.from_list(["10.0.0.0/8"])


def _scanner(ports, **kw):
    return ss.SynScanner(_scope(), ports=ports, force_fallback=True,
                         key=KEY, **kw)


def _summary(results):
    summaries = [r for r in results if r.status == "scan_summary"]
    assert len(summaries) == 1, (
        f"expected exactly one scan_summary, got {len(summaries)}")
    return summaries[0]


# ── R1: the per-host coverage summary ────────────────────────────────────────

class TestBuildResultsCoverageSummary:
    def test_port_states_match_open_closed_filtered_and_not_scanned(self):
        """10 requested ports: one open, one closed, one silent-but-sent
        (filtered), the rest never sent at all (not_scanned)."""
        ports = list(range(1, 11))
        states = {1: "open", 2: "closed", 3: None}
        attempts = {1: 1, 2: 1, 3: 2}          # 4..10 have no entry: never sent
        sc = _scanner(ports, report_closed=True)

        summ = _summary(sc._build_results("10.0.0.5", states, attempts, {}))

        port_states = summ.data["port_states"]
        assert port_states["open"] == [[1, 1]]
        assert port_states["closed"] == [[2, 2]]
        assert port_states["filtered"] == [[3, 3]]
        assert port_states["not_scanned"] == [[4, 10]]

    def test_ports_not_scanned_equals_the_unreached_count(self):
        ports = list(range(1, 21))             # 20 requested
        states = {p: "closed" for p in range(1, 6)}
        attempts = {p: 1 for p in range(1, 6)}  # 5 probed, 15 never touched
        sc = _scanner(ports)

        summ = _summary(sc._build_results("10.0.0.5", states, attempts, {}))
        assert summ.data["ports_not_scanned"] == 15
        assert summ.data["ports_attempted"] == 5
        assert summ.data["ports_requested"] == 20

    def test_budget_exhausted_true_when_a_budget_was_set_and_ports_unreached(self):
        ports = list(range(1, 6))
        sc = _scanner(ports)

        summ = _summary(sc._build_results(
            "10.0.0.5", {1: "open"}, {1: 1}, {}, budget_active=True))
        assert summ.data["budget_exhausted"] is True

    def test_budget_exhausted_false_with_no_budget_even_if_ports_are_short(self):
        """No budget was ever set, so a short port count is not the budget's
        doing (e.g. a caller constructed states/attempts directly)."""
        ports = list(range(1, 6))
        sc = _scanner(ports)

        summ = _summary(sc._build_results(
            "10.0.0.5", {1: "open"}, {1: 1}, {}, budget_active=False))
        assert summ.data["budget_exhausted"] is False

    def test_budget_exhausted_false_when_the_budget_covered_every_port(self):
        ports = [1, 2]
        sc = _scanner(ports)

        summ = _summary(sc._build_results(
            "10.0.0.5", {1: "open", 2: "closed"}, {1: 1, 2: 1}, {},
            budget_active=True))
        assert summ.data["budget_exhausted"] is False

    def test_method_duration_and_pacing_are_recorded(self):
        sc = _scanner([80])
        stats = {"initial_rate": 50.0, "final_rate": 25.0, "rounds": 3,
                 "backoffs": 1}

        summ = _summary(sc._build_results(
            "10.0.0.5", {80: "open"}, {80: 1}, {},
            duration_s=1.5, pacer_stats=stats))

        assert summ.data["method"] == "syn"
        assert summ.data["duration_s"] == 1.5
        assert summ.data["pacing"] == stats

    def test_no_pacing_key_when_pacing_never_ran(self):
        sc = _scanner([80])
        summ = _summary(sc._build_results("10.0.0.5", {80: "open"}, {80: 1}, {}))
        assert "pacing" not in summ.data

    def test_evidence_string_matches_portscanner_style(self):
        sc = _scanner([80, 443])
        summ = _summary(sc._build_results(
            "10.0.0.5", {80: "open", 443: "closed"}, {80: 1, 443: 1}, {}))
        assert summ.evidence == "2/2 ports scanned, 1 open, health=ok"


class TestEmitSummaryToggle:
    def test_true_by_default(self):
        sc = _scanner([80])
        results = sc._build_results("10.0.0.5", {80: "open"}, {80: 1}, {})
        assert any(r.status == "scan_summary" for r in results)

    def test_false_emits_no_summary(self):
        sc = _scanner([80, 443], emit_summary=False)
        results = sc._build_results("10.0.0.5", {80: "open"}, {80: 1}, {})
        assert all(r.status != "scan_summary" for r in results)
        # Per-port emission is otherwise unaffected.
        assert {r.port for r in results} == {80}


# ── R2: a failed send is never a target verdict ─────────────────────────────

class TestLocalSendFailureNeverBecomesFiltered:
    def test_error_state_in_summary_with_degraded_health(self):
        sc = _scanner([80])

        results = sc._build_results("10.0.0.5", {}, {}, {}, send_failed={80: 3})

        summ = _summary(results)
        assert summ.data["error"] == 1
        assert summ.data["health"] == "degraded"
        assert summ.data["local_resource_errors"] == 1
        assert summ.data["port_states"]["error"] == [[80, 80]]

    def test_never_filtered_in_per_port_output_under_report_closed(self):
        sc = _scanner([80], report_closed=True)

        results = sc._build_results("10.0.0.5", {}, {}, {}, send_failed={80: 2})

        per_port = [r for r in results if r.status != "scan_summary"]
        assert all(r.status != "filtered" for r in per_port)
        assert len(per_port) == 1
        assert per_port[0].status == "error"
        assert per_port[0].data["reason"] == "local_resource_error"

    def test_omitted_from_per_port_output_without_report_closed(self):
        """report_closed=False (the default): still never `filtered`, and per
        R1's "either emit as error or omit" choice, this path omits it."""
        sc = _scanner([80], report_closed=False)

        results = sc._build_results("10.0.0.5", {}, {}, {}, send_failed={80: 2})

        per_port = [r for r in results if r.status != "scan_summary"]
        assert per_port == []
        assert _summary(results).data["health"] == "degraded"

    def test_a_port_with_one_successful_send_is_not_an_error(self):
        """attempts_by_port having an entry means at least one send DID
        succeed — earlier failed sends before that success must not taint
        the eventual verdict."""
        sc = _scanner([80], report_closed=True)

        results = sc._build_results(
            "10.0.0.5", {80: "closed"}, {80: 1}, {}, send_failed={80: 2})

        per_port = [r for r in results if r.status != "scan_summary"]
        assert per_port[0].status == "closed"
        summ = _summary(results)
        assert summ.data["error"] == 0
        assert summ.data["health"] == "ok"

    def test_never_probed_port_with_no_failures_stays_not_scanned(self):
        """No attempts and no failures at all: budget ran out before this
        port was even tried. Not an error, not filtered — simply absent."""
        sc = _scanner([80])
        results = sc._build_results("10.0.0.5", {}, {}, {})
        assert [r for r in results if r.status != "scan_summary"] == []
        summ = _summary(results)
        assert summ.data["port_states"]["not_scanned"] == [[80, 80]]
        assert summ.data["error"] == 0


# ── R3: SendPacer's hard ceiling ─────────────────────────────────────────────

class TestSendPacerHardCeiling:
    def test_max_rate_defaults_to_the_requested_rate(self):
        assert SendPacer(100.0).max_rate == 100.0

    def test_rate_never_exceeds_the_default_ceiling_after_many_clean_rounds(self):
        p = SendPacer(100.0)
        for _ in range(500):
            p.observe_round(sent=10, answered=10)
        assert p.rate <= 100.0
        assert p.rate == pytest.approx(100.0)

    def test_recovery_after_backoff_climbs_toward_but_never_past_the_ceiling(self):
        p = SendPacer(100.0)
        p.observe_round(sent=100, answered=0)          # backoff
        assert p.rate < 100.0
        for _ in range(500):
            p.observe_round(sent=10, answered=10)       # recover
        assert p.rate == pytest.approx(100.0)
        assert p.rate <= p.max_rate

    def test_explicit_max_rate_still_works(self):
        p = SendPacer(100.0, max_rate=250.0)
        assert p.max_rate == 250.0
        for _ in range(500):
            p.observe_round(sent=10, answered=10)
        assert p.rate <= 250.0
        assert p.rate == pytest.approx(250.0)


# ── R3: SendPacer.pace() is thread-safe ──────────────────────────────────────

class TestPaceIsThreadSafe:
    def test_k_threads_sharing_one_pacer_hold_the_schedule(self):
        """8 threads call pace() 15 times each on ONE shared pacer.

        Lower bounds only (a slower CI only widens these, never narrows
        them): elapsed >= (M-1)/rate — the schedule was actually held, not
        skipped — via wall-clock timing.

        The no-burst half is checked as an EQUIVALENT deterministic
        invariant on the schedule itself rather than by sampling wake-up
        instants: sub-millisecond OS thread-wake jitter is the same order of
        magnitude as a short interval, which made a wall-clock "were any two
        wake-ups suspiciously close together" check flaky by construction,
        independent of whether pacing was correct. `_next` is reserved
        under the lock as `max(now, self._next) + interval`, so M calls with
        no lost update must advance it by at least `M * interval` beyond
        wherever it started — a race that let two threads read the SAME
        `_next` before either wrote it (the exact bug: two threads compute
        the same slot and fire together) collapses two reservations into
        one and the schedule falls short of that bound.
        """
        rate = 400.0                      # 2.5 ms interval
        interval = 1.0 / rate
        pacer = SendPacer(rate)
        n_threads, calls_per_thread = 8, 15
        total_calls = n_threads * calls_per_thread

        now_before = time.monotonic()

        def _worker():
            for _ in range(calls_per_thread):
                pacer.pace()

        threads = [threading.Thread(target=_worker) for _ in range(n_threads)]
        t0 = time.monotonic()
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        elapsed = time.monotonic() - t0

        assert elapsed >= (total_calls - 1) * interval - 0.05

        assert pacer._next >= now_before + total_calls * interval - 1e-3, (
            "the reserved schedule fell short of M whole intervals — some "
            "reservation was lost to a race")

    def test_observe_round_is_also_safe_under_concurrent_pace_calls(self):
        """No crash / no lost update under contention: run pace() and
        observe_round() from many threads at once and check the accounting
        is internally consistent afterwards."""
        pacer = SendPacer(1000.0, min_rate=1.0)
        errors: list[Exception] = []

        def _pacer_worker():
            try:
                for _ in range(50):
                    pacer.pace()
            except Exception as exc:                # pragma: no cover
                errors.append(exc)

        def _observe_worker():
            try:
                for _ in range(50):
                    pacer.observe_round(sent=10, answered=10)
            except Exception as exc:                # pragma: no cover
                errors.append(exc)

        threads = ([threading.Thread(target=_pacer_worker) for _ in range(4)]
                  + [threading.Thread(target=_observe_worker) for _ in range(4)])
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert pacer.rounds == 200
        assert pacer.rate <= pacer.max_rate


# ── R4: congestion is host-local; the aggregate cap is shared ───────────────

class TestHostLocalAIMDDoesNotThrottleTheSharedPacer:
    """Drives the real send loop with a fake, wholly-silent raw socket (raw
    sockets can't run in CI) and checks the aggregate cap versus the
    host-local pacer that AIMD actually ran on.
    """

    def _patch_silent_host(self, monkeypatch):
        monkeypatch.setattr(ss.random, "randint", lambda a, b: 50000)
        monkeypatch.setattr(
            ss, "resolve",
            lambda t, p, proto="tcp", family=None: (socket.AF_INET, (t, 0)))
        monkeypatch.setattr(ss, "_local_source_ip", lambda dst: "10.0.0.1")

        class _Send:
            def setsockopt(self, *a): pass
            def sendto(self, pkt, addr): pass
            def close(self): pass

        class _Recv:
            def setblocking(self, *a): pass
            def setsockopt(self, *a): pass
            def recv(self, n): raise OSError("no data")   # never answers
            def close(self): pass

        def _factory(family, stype, proto):
            return _Recv() if proto == socket.IPPROTO_TCP else _Send()
        monkeypatch.setattr(ss.socket, "socket", _factory)

    def test_one_silent_host_leaves_the_aggregate_pacer_at_the_requested_rate(
            self, monkeypatch):
        """The shared self._pacer is the aggregate hard cap and must never be
        fed observe_round: a firewalled host's ~100% loss must leave it
        exactly at the requested rate, not halved."""
        self._patch_silent_host(monkeypatch)
        sc = ss.SynScanner(_scope(), ports=list(range(1, 21)), key=KEY,
                           retries=2, timeout=0.01, rate=2000.0)

        results = sc._syn_scan_blocking("10.0.0.5")

        assert sc._pacer.rate == 2000.0
        assert sc._pacer.rounds == 0        # observe_round never called on it

        # The HOST-LOCAL pacer, by contrast, backed off — its stats travel in
        # the summary because it is built fresh inside this one call, not
        # kept as a scanner attribute.
        summ = _summary(results)
        assert summ.data["pacing"]["backoffs"] >= 1
        assert summ.data["pacing"]["final_rate"] < 2000.0

    def test_pacing_is_absent_when_pace_sends_is_off(self, monkeypatch):
        self._patch_silent_host(monkeypatch)
        sc = ss.SynScanner(_scope(), ports=[80], key=KEY, retries=0,
                           timeout=0.01, pace_sends=False)

        results = sc._syn_scan_blocking("10.0.0.5")

        assert sc._pacer is None
        assert "pacing" not in _summary(results).data
