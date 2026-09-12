"""
A host's scan must not hold one result object per PORT.

`scan_target` filtered its results down to "open + summary" only at the END, so
until a host finished it kept a full ScanResult — reason, evidence string, errno,
rtt, family, vantage — for every port it had probed. Measured on the real deep
envelope: 47 MB for ONE host's 65,535 ports. The port stage runs every live host
at once, so that is 1.2 GB at 25 hosts and 4.7 GB at 100 — the probe is killed by
the OS with no traceback, and the job restarts from zero.

Only two kinds of result actually have to survive the sweep:
  * OPEN — it is emitted;
  * AMBIGUOUS silence — the cleanup pass re-probes it and may correct it.
A closed/unreachable/error verdict is final the moment it arrives: tally it and
let it go.

The tallies must not change. Coverage accounting (`complete`, missing/duplicate
ports) is the accuracy guarantee, and it is set-based, so recording a definitive
port when it finishes rather than at the end is equivalent — these tests pin that.
"""
from __future__ import annotations

import asyncio
import gc
import weakref

from scanner.port_scanner import PortScanner
from scanner.scanner_base import ScopeGuard

PORTS = 5000
OPEN_PORTS = {22, 80, 443, 3389, 8080}
CONCURRENCY = 64


def _scanner(**kw):
    return PortScanner(ScopeGuard.from_list(["127.0.0.0/8"]),
                       ports=list(range(1, PORTS + 1)), timeout=0.01,
                       concurrency=CONCURRENCY, rate=1_000_000,
                       adaptive_timeout=False, congestion=False, **kw)


def _live_probe(scanner, *, silent_ports=frozenset()):
    """Returns (attempt_fn, live_at_end) where live_at_end is filled in with the
    number of result objects still alive when the LAST port is probed — i.e. the
    scan's real peak retention, not what survives after it returns."""
    # ScanResult is an unhashable dataclass, so hold plain weak references and
    # count the ones still alive rather than using a WeakSet.
    refs: list[weakref.ref] = []
    probed = {"n": 0}
    live_at_end: dict = {}

    async def _attempt(target, port, est=None, min_timeout=None):
        if port in OPEN_PORTS:
            r = scanner._build(target, port, "open", "connect_success",
                               "tcp connect completed (3-way handshake)",
                               rtt_ms=0.9, family="ipv4")
        elif port in silent_ports:
            r = scanner._build(target, port, "filtered", "no_response",
                               "no response within 0.01s", rtt_ms=10.0,
                               family="ipv4")
        else:
            r = scanner._build(target, port, "closed", "connection_refused",
                               None, rtt_ms=0.4, error="[Errno 61] Connect call "
                               f"failed ('127.0.0.1', {port})", errno_val=61,
                               family="ipv4")
        alive.add(r)
        probed["n"] += 1
        if probed["n"] == PORTS:
            gc.collect()
            live_at_end["count"] = len(alive)
        return r

    return _attempt, live_at_end


def _summary(out):
    return [r for r in out if r.status == "scan_summary"][0].data


class TestRetention:
    def test_definitive_results_are_not_held_for_the_whole_sweep(self):
        sc = _scanner(reprobe=False)
        sc._attempt, live_at_end = _live_probe(sc)

        asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 120))

        # Open results + whatever is genuinely in flight. Nowhere near one per port.
        assert live_at_end["count"] < len(OPEN_PORTS) + CONCURRENCY + 50, (
            f"{live_at_end['count']} of {PORTS} results still live mid-scan — "
            "closed ports are being retained")

    def test_ambiguous_results_are_still_retained_for_the_cleanup_pass(self):
        """Silence is the ONE state a re-probe can legitimately change, so it
        must survive the sweep. Dropping it would disable the cleanup pass that
        turns false `filtered` back into `closed`."""
        silent = {1000, 1001, 1002}
        sc = _scanner(reprobe=True, reprobe_rate=1_000_000, reprobe_retries=0)
        sc._attempt, _ = _live_probe(sc, silent_ports=silent)

        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 120))

        summary = _summary(out)
        assert summary["reprobe"]["candidates"] == len(silent)


class TestAccountingIsUnchanged:
    def test_every_port_is_classified_exactly_once(self):
        sc = _scanner(reprobe=False)
        sc._attempt, _ = _live_probe(sc)

        summary = _summary(asyncio.run(
            asyncio.wait_for(sc.scan_target("127.0.0.1"), 120)))

        assert summary["ports_attempted"] == PORTS
        assert summary["classified"] == PORTS
        assert summary["missing"] == 0
        assert summary["duplicates"] == 0
        assert summary["complete"] is True

    def test_state_tallies_match_the_probes(self):
        sc = _scanner(reprobe=False)
        sc._attempt, _ = _live_probe(sc)

        summary = _summary(asyncio.run(
            asyncio.wait_for(sc.scan_target("127.0.0.1"), 120)))

        assert summary["open"] == len(OPEN_PORTS)
        assert summary["closed"] == PORTS - len(OPEN_PORTS)
        assert summary["filtered"] == 0

    def test_only_open_ports_and_the_summary_are_emitted(self):
        sc = _scanner(reprobe=False)
        sc._attempt, _ = _live_probe(sc)

        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 120))

        assert {r.port for r in out if r.status == "open"} == OPEN_PORTS
        assert len(out) == len(OPEN_PORTS) + 1        # + scan_summary

    def test_report_closed_still_emits_every_port(self):
        """The audit path deliberately keeps everything; retention must follow
        the request, not silently drop evidence someone asked for."""
        sc = _scanner(reprobe=False, report_closed=True)
        sc._attempt, _ = _live_probe(sc)

        out = asyncio.run(asyncio.wait_for(sc.scan_target("127.0.0.1"), 120))

        assert len([r for r in out if r.status != "scan_summary"]) == PORTS
