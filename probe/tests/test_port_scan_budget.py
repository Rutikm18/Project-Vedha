"""
Per-host wall-clock budget with honest partial results.

"No checkpointing or chunking — there's no per-host time budget and no streaming
of partial results" was a verified gap, and we hit it live: a deep 65,535-port
sweep of one RST-suppressing host had an 11.9-hour ETA while two other jobs
queued behind it.

The budget bounds that. What matters is that stopping early stays HONEST:

  * Ports never dequeued are NOT reported `filtered`. `filtered` is a claim about
    the target ("something dropped our probe"); these were never probed at all.
    Conflating them would invent firewall evidence out of a clock running out —
    exactly the manufactured false negative the accuracy work exists to prevent.
  * The existing set-based accounting does this for free: an unscanned port is
    never recorded, so `classified < ports_requested` and `complete` is already
    False. The budget adds no new bookkeeping, only `budget_exhausted` so the
    REASON is explicit rather than inferred from a gap.
"""
from __future__ import annotations

import asyncio

from scanner.port_scanner import PortScanner
from scanner.scanner_base import ScopeGuard


def _sc(ports, **kw):
    return PortScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                       ports=ports, timeout=0.01, concurrency=4,
                       rate=10_000, reprobe=False, **kw)


def _summary(out):
    return [r for r in out if r.status == "scan_summary"][0].data


class TestBudgetStops:
    def test_budget_cuts_the_scan_short(self):
        sc = _sc(list(range(1, 3001)), deadline_seconds=0.25)

        async def _slow(target, port, est=None, min_timeout=None):
            await asyncio.sleep(0.05)
            return sc._build(target, port, "filtered", "no_response", "silence")
        sc._attempt = _slow

        summ = _summary(asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30)))
        assert summ["budget_exhausted"] is True
        assert summ["ports_not_scanned"] > 0
        assert summ["complete"] is False

    def test_accounting_stays_honest_when_cut_short(self):
        """Every requested port is accounted for as either attempted or
        not-scanned — a partial scan must never silently lose ports."""
        sc = _sc(list(range(1, 3001)), deadline_seconds=0.25)

        async def _slow(target, port, est=None, min_timeout=None):
            await asyncio.sleep(0.05)
            return sc._build(target, port, "closed", "connection_refused", "rst")
        sc._attempt = _slow

        summ = _summary(asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30)))
        assert summ["ports_attempted"] + summ["ports_not_scanned"] == summ["ports_requested"]

    def test_unscanned_ports_are_not_reported_filtered(self):
        """The core honesty property: running out of clock is not evidence of a
        firewall. Unreached ports must not inflate the filtered count."""
        sc = _sc(list(range(1, 3001)), deadline_seconds=0.25)

        async def _slow(target, port, est=None, min_timeout=None):
            await asyncio.sleep(0.05)
            return sc._build(target, port, "closed", "connection_refused", "rst")
        sc._attempt = _slow

        summ = _summary(asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30)))
        assert summ["filtered"] == 0
        assert summ["ports_not_scanned"] > 0


class TestNoBudget:
    def test_without_a_budget_everything_is_scanned(self):
        sc = _sc([80, 443, 8080], deadline_seconds=None)

        async def _fast(target, port, est=None, min_timeout=None):
            return sc._build(target, port, "closed", "connection_refused", "rst")
        sc._attempt = _fast

        summ = _summary(asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30)))
        assert summ["budget_exhausted"] is False
        assert summ["complete"] is True
        assert summ["ports_not_scanned"] == 0

    def test_generous_budget_does_not_interfere(self):
        """A budget that is never reached must behave exactly like no budget."""
        sc = _sc([80, 443], deadline_seconds=60.0)

        async def _fast(target, port, est=None, min_timeout=None):
            return sc._build(target, port, "open", "connect_success", "syn-ack")
        sc._attempt = _fast

        summ = _summary(asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30)))
        assert summ["budget_exhausted"] is False
        assert summ["complete"] is True
        assert summ["open"] == 2

    def test_budget_flag_is_always_present(self):
        """Consumers can branch on it without a key check."""
        sc = _sc([80])

        async def _fast(target, port, est=None, min_timeout=None):
            return sc._build(target, port, "closed", "connection_refused", "rst")
        sc._attempt = _fast

        assert "budget_exhausted" in _summary(
            asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 30)))
