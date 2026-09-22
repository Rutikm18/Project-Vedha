"""
C1 — max_host_seconds must bound the WHOLE host, cleanup pass included.

THE HANG THIS REMOVES
---------------------
PortScanner.scan_target computes a per-host deadline and honours it in the main
sweep: `_worker` checks it before dequeuing, so a port is either fully probed or
never touched, and untouched ports are reported not_scanned rather than filtered.

The cleanup pass ran AFTER the workers and had no clock at all. On a host that
answers nothing, every one of its ports is ambiguous, so the cleanup re-probes
all of them at reprobe_rate (40 pps) with reprobe_retries+1 attempts each:

    65,535 ports x 4 attempts / 40 pps = 6,554 s

That is 1.8 hours for ONE host, and 91% of the default 7,200 s job ceiling —
while `deep` intensity's max_host_seconds=1800 sat there doing nothing. Two such
hosts exhausted the entire job before any other host was reached.

WHAT A TRUNCATED CLEANUP MEANS
------------------------------
Different from a truncated main sweep, and the distinction matters:

  * main sweep truncated  -> the port was NEVER probed -> not_scanned
  * cleanup truncated     -> the port WAS probed and stayed silent -> filtered,
                             it just never got its second, gentler look

So skipped ports keep their main-sweep verdict. What is lost is a confidence
upgrade, not an observation, and the summary records that so `filtered` can be
read with the right amount of trust.
"""
from __future__ import annotations

import asyncio
import time

import pytest

from scanner.port_scanner import PortScanner
from scanner.scanner_base import ScopeGuard

SCOPE = ScopeGuard.from_list(["10.0.0.0/24"])
TARGET = "10.0.0.1"


def _scanner(ports, **kw):
    kw.setdefault("rate", 10_000)          # the main sweep is never the subject
    kw.setdefault("concurrency", 50)
    kw.setdefault("timeout", 0.01)
    kw.setdefault("adaptive_timeout", False)
    kw.setdefault("congestion", False)
    return PortScanner(SCOPE, ports=ports, **kw)


def _silent(scanner, port, delay=0.0):
    """A `filtered / no_response` result — the one state cleanup may revisit."""
    async def _attempt(target, p, est=None, min_timeout=None):
        if delay:
            await asyncio.sleep(delay)
        return scanner._build(target, p, "filtered", "no_response", "silence")
    return _attempt


# ── the deadline reaches the cleanup pass ───────────────────────────────────

class TestTheCleanupIsBounded:
    @pytest.mark.asyncio
    async def test_reprobe_stops_once_the_budget_is_spent(self, monkeypatch):
        scanner = _scanner(list(range(1, 200)), reprobe_rate=1000.0,
                           reprobe_retries=1)
        monkeypatch.setattr(scanner, "_attempt",
                            _silent(scanner, None, delay=0.005))
        # A deadline already in the past: nothing may be re-probed.
        resolved, stats = await scanner._reprobe_ambiguous(
            TARGET, list(range(1, 200)), None,
            deadline=time.monotonic() - 1,
        )
        assert resolved == {}
        assert stats["skipped"] == 199
        assert stats["budget_exhausted"] is True

    @pytest.mark.asyncio
    async def test_a_generous_budget_reprobes_everything(self, monkeypatch):
        scanner = _scanner([1, 2, 3], reprobe_rate=1000.0, reprobe_retries=0)
        monkeypatch.setattr(scanner, "_attempt", _silent(scanner, None))
        _, stats = await scanner._reprobe_ambiguous(
            TARGET, [1, 2, 3], None, deadline=time.monotonic() + 30,
        )
        assert stats["skipped"] == 0
        assert stats["budget_exhausted"] is False

    @pytest.mark.asyncio
    async def test_no_deadline_keeps_the_old_unbounded_behaviour(self, monkeypatch):
        """light/standard set max_host_seconds=None on purpose — they are
        bounded by port BREADTH, so a clock would only ever cut them short."""
        scanner = _scanner([1, 2, 3], reprobe_rate=1000.0, reprobe_retries=0)
        monkeypatch.setattr(scanner, "_attempt", _silent(scanner, None))
        _, stats = await scanner._reprobe_ambiguous(TARGET, [1, 2, 3], None)
        assert stats["skipped"] == 0
        assert stats["budget_exhausted"] is False

    @pytest.mark.asyncio
    async def test_a_partial_cleanup_reports_what_it_skipped(self, monkeypatch):
        scanner = _scanner(list(range(1, 400)), reprobe_rate=200.0,
                           reprobe_retries=0, reprobe_concurrency=1)
        monkeypatch.setattr(scanner, "_attempt",
                            _silent(scanner, None, delay=0.002))
        _, stats = await scanner._reprobe_ambiguous(
            TARGET, list(range(1, 400)), None,
            deadline=time.monotonic() + 0.15,
        )
        assert stats["budget_exhausted"] is True
        assert 0 < stats["skipped"] < 399, stats      # some done, some not


# ── the end-to-end promise ──────────────────────────────────────────────────

class TestMaxHostSecondsBoundsTheWholeHost:
    @pytest.mark.asyncio
    async def test_a_silent_host_cannot_outrun_its_budget(self, monkeypatch):
        """The measured failure: every port ambiguous, so cleanup dominates.

        Before C1 this call ignored deadline_seconds entirely once the workers
        finished.
        """
        ports = list(range(1, 300))
        scanner = _scanner(ports, deadline_seconds=0.4, reprobe_rate=50.0,
                           reprobe_retries=3, reprobe_concurrency=2)
        monkeypatch.setattr(scanner, "_attempt",
                            _silent(scanner, None, delay=0.002))

        started = time.monotonic()
        results = await scanner.scan_target(TARGET)
        elapsed = time.monotonic() - started

        # Generous ceiling: the point is that it terminates on the budget at all,
        # not that it lands on a precise millisecond.
        assert elapsed < 5.0, f"cleanup ignored the host budget ({elapsed:.1f}s)"

        summary = next(r for r in results if r.status == "scan_summary")
        assert summary.data["reprobe"]["budget_exhausted"] is True

    @pytest.mark.asyncio
    async def test_skipped_ports_keep_their_filtered_verdict(self, monkeypatch):
        """They WERE probed. Only the second look was skipped, so downgrading
        them to not_scanned would be a different — and false — claim."""
        ports = list(range(1, 60))
        scanner = _scanner(ports, deadline_seconds=0.3, reprobe_rate=20.0,
                           reprobe_retries=3, reprobe_concurrency=1,
                           report_closed=True)
        monkeypatch.setattr(scanner, "_attempt",
                            _silent(scanner, None, delay=0.001))

        results = await scanner.scan_target(TARGET)
        summary = next(r for r in results if r.status == "scan_summary")
        assert summary.data["reprobe"]["budget_exhausted"] is True

        states = {r.status for r in results if r.port is not None}
        assert states == {"filtered"}, states
        assert "not_scanned" not in states

    @pytest.mark.asyncio
    async def test_the_summary_still_reports_the_usual_cleanup_counters(
        self, monkeypatch,
    ):
        scanner = _scanner([1, 2, 3], deadline_seconds=30, reprobe_rate=1000.0,
                           reprobe_retries=0)
        monkeypatch.setattr(scanner, "_attempt", _silent(scanner, None))
        results = await scanner.scan_target(TARGET)
        stats = next(r for r in results if r.status == "scan_summary").data["reprobe"]
        for key in ("candidates", "resolved", "remaining", "rate",
                    "skipped", "budget_exhausted"):
            assert key in stats, key


# ── structure: the cleanup must not allocate one coroutine per port ─────────

def test_the_cleanup_drains_a_queue_like_the_main_sweep_does():
    """`gather(*(_one(p) for p in ports))` built one coroutine per port — 65,535
    of them on a silent host, the exact allocation the main sweep's worker pool
    exists to avoid (see scan_target's docstring). Threading a deadline through
    a queue is also what makes the check natural: it is tested before each
    dequeue, so a port is either fully re-probed or never touched.
    """
    import inspect

    src = inspect.getsource(PortScanner._reprobe_ambiguous)
    assert "asyncio.gather(*(" not in src, \
        "cleanup still allocates a coroutine per candidate port"
    assert "Queue" in src


# ── C2: the candidate set is bounded by COUNT, not only by clock ────────────

class TestTheCandidateSetIsCapped:
    """Why a cap when C1 already bounds the pass by time.

    The cleanup's own docstring calls it "deliberately slow and NARROW", and
    the measured win it was built for was 69 ambiguous ports on a host that
    answered everything else. 60,000 candidates is not a narrow second look —
    it is a second full scan, at 40 pps.

    The clock alone would let such a host spend its ENTIRE host budget on a
    cleanup that is almost certainly hopeless (a wholly-silent host has nothing
    to contrast against), starving the ports that had real evidence. The cap
    keeps the pass proportionate, and prioritising top1000 means the candidates
    it does drop are the least likely to be services.
    """

    def test_a_small_candidate_set_is_untouched(self):
        scanner = _scanner([1, 2, 3])
        chosen, dropped = scanner._select_reprobe_candidates([1, 2, 3])
        assert chosen == [1, 2, 3]
        assert dropped == 0

    def test_an_oversized_candidate_set_is_truncated(self):
        scanner = _scanner([1], reprobe_max_candidates=100)
        chosen, dropped = scanner._select_reprobe_candidates(list(range(1, 1001)))
        assert len(chosen) == 100
        assert dropped == 900

    def test_service_ports_are_kept_in_preference_to_arbitrary_high_ones(self):
        """top1000 is the curated high-signal set; a false `filtered` there is
        a missed SERVICE, which is the whole point of the cleanup."""
        from scanner.port_scanner import resolve_profile

        top = set(resolve_profile("top1000"))
        # 50 well-known ports buried in 5,000 arbitrary high ones.
        wanted = sorted(list(top)[:50])
        noise = [p for p in range(50000, 56000) if p not in top][:5000]
        scanner = _scanner([1], reprobe_max_candidates=200)

        chosen, dropped = scanner._select_reprobe_candidates(
            sorted(wanted + noise))

        assert set(wanted) <= set(chosen), "a service port was dropped first"
        assert dropped == len(wanted) + len(noise) - 200

    def test_the_cap_is_configurable(self):
        scanner = _scanner([1], reprobe_max_candidates=7)
        chosen, _ = scanner._select_reprobe_candidates(list(range(1, 100)))
        assert len(chosen) == 7

    def test_zero_disables_the_cap(self):
        """An operator who really wants the whole set can still have it."""
        scanner = _scanner([1], reprobe_max_candidates=0)
        chosen, dropped = scanner._select_reprobe_candidates(list(range(1, 5000)))
        assert len(chosen) == 4999 and dropped == 0

    @pytest.mark.asyncio
    async def test_the_summary_separates_capped_from_budget_exhausted(
        self, monkeypatch,
    ):
        """Two different reasons a port went un-rechecked, two different fixes:
        raise the cap, or raise the host budget. Collapsing them would hide
        which one an operator needs."""
        ports = list(range(1, 500))
        scanner = _scanner(ports, deadline_seconds=30, reprobe_rate=100_000.0,
                           reprobe_retries=0, reprobe_max_candidates=50)
        monkeypatch.setattr(scanner, "_attempt", _silent(scanner, None))

        results = await scanner.scan_target(TARGET)
        stats = next(r for r in results if r.status == "scan_summary").data["reprobe"]

        assert stats["candidates"] == 499        # what was ambiguous
        assert stats["capped"] == 449            # dropped by the cap
        assert stats["budget_exhausted"] is False   # the clock was not the limit
