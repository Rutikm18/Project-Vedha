"""
A deep scan must not make every host wait for all 65,535 ports before ANY of
them is assessed.

The port stage scanned the whole requested range, and only then did banner, OS
and the deep branches run. At the aggressive envelope that is ~109s of pure
sending per host at best (measured 280-2,728s), so on a /24 nothing was assessed
for hours — and if the job was then cut short, the facts that existed were port
states with no service assessment behind them.

Two phases fix the ordering without narrowing coverage:

  * FIRST the high-signal set (the branch catalogs plus the caller's fast list).
    Banner, OS, the deep branches and UDP all run on that, so every host has a
    real assessment within minutes.
  * THEN the remaining requested ports as a budgeted tail. A port only the tail
    finds still gets its banner, and hosts that gained ports get another pass at
    the deep branches (the router can send a newly-banner'd port to a branch).

Coverage is identical — the same ports are scanned, in a different order.
"""
from __future__ import annotations

import asyncio

import pytest

from scanner.scanner_base import ScanResult, ScopeGuard
from workflow.branches import BRANCHES
from workflow.gates import SSH_PORTS
from workflow.workflow_engine import _port_candidates
from workflow.workflow_engine import run_engagement

HOST = "10.0.0.1"
SCOPE = ScopeGuard.from_list(["10.0.0.0/24"])
REQUESTED = list(range(1, 4001))          # what the operator asked to cover
FAST = [22, 80, 445]                      # the caller's high-signal list
TAIL_ONLY_OPEN = 3999                     # opens only when the tail reaches it


class _Log:
    """Ordered record of what ran, so phase ORDER can be asserted."""

    def __init__(self):
        self.events: list[tuple[str, tuple]] = []

    def add(self, name, payload=()):
        self.events.append((name, payload))

    def names(self):
        return [n for n, _ in self.events]

    def ports_for(self, name):
        return [p for n, p in self.events if n == name]


def _wire(monkeypatch, log, *, open_in_first=(22,), open_in_tail=()):
    """Stub every scanner the engine builds; port scanners report per-phase opens."""

    def _port_scanner(kind):
        class Scanner:
            name = kind

            def __init__(self, *args, ports=None, **kwargs):
                self.ports = sorted(ports or [])
                self.kwargs = kwargs

            # The tail passes each host's budget per call, as the real port
            # scanners accept it.
            async def scan_target(self, host, *, deadline_seconds=None):
                log.add(f"{kind}:construct", tuple(self.ports))
                opens = [p for p in self.ports
                         if p in (open_in_tail if TAIL_ONLY_OPEN in self.ports
                                  else open_in_first)]
                return [ScanResult(scanner="port_scan", target=host, port=p,
                                   proto="tcp", status="open",
                                   data={"reason": "connect_success"})
                        for p in opens]
        return Scanner

    class _Discovery:
        name = "host_discovery"

        def __init__(self, *a, **kw):
            pass

        async def scan_target(self, host):
            return [ScanResult(scanner="host_discovery", target=host,
                               status="open", data={"alive": True})]

    class _Banner:
        name = "service_banner"

        def __init__(self, *a, ports=None, **kw):
            self.ports = sorted(ports or [])

        async def scan_target(self, host):
            log.add("service_banner", tuple(self.ports))
            return [ScanResult(scanner="service_banner", target=host, port=p,
                               proto="tcp", status="open",
                               data={"service": "unknown"})
                    for p in self.ports]

    class _OS:
        name = "os_fingerprint"

        def __init__(self, *a, **kw):
            pass

        async def scan_target(self, host):
            return [ScanResult(scanner="os_fingerprint", target=host,
                               status="observed", data={"os_guess": "Linux"})]

    class _Branch:
        name = "ssh_scan"

        def __init__(self, *a, ports=None, **kw):
            self.ports = sorted(ports or [])

        async def scan_target(self, host):
            log.add("ssh_scan", tuple(self.ports))
            return [ScanResult(scanner="ssh_scan", target=host,
                               port=(self.ports or [22])[0], proto="tcp",
                               status="open", data={})]

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner", _Discovery)
    monkeypatch.setattr("workflow.workflow_engine.PortScanner", _port_scanner("port_scan"))
    monkeypatch.setattr("workflow.workflow_engine.SynScanner", _port_scanner("syn_scan"))
    monkeypatch.setattr("workflow.workflow_engine.ServiceBannerScanner", _Banner)
    monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner", _OS)
    class _UDP:
        name = "udp_scan"

        def __init__(self, *a, ports=None, **kw):
            pass

        async def scan_target(self, host):
            return []

    def _inert(component):
        class Inert:
            name = component

            def __init__(self, *a, **kw):
                pass

            async def scan_target(self, host):
                return []
        return Inert

    # Host-level and datagram branches run whether or not a TCP port is open, so
    # every branch has to be inert or the test probes the real network.
    for spec in BRANCHES:
        monkeypatch.setattr(f"workflow.workflow_engine.{spec.scanner}",
                            _inert(spec.component))
    monkeypatch.setattr("workflow.workflow_engine.SSHScanner", _Branch)
    monkeypatch.setattr("workflow.workflow_engine.UDPScanner", _UDP)


def _run(**kwargs):
    defaults = dict(profile="it", port_override=REQUESTED,
                    stage_ceiling="deep_scan", host_concurrency=2)
    defaults.update(kwargs)
    return asyncio.run(run_engagement([HOST], SCOPE, **defaults))


class TestPhaseOrder:
    def test_the_deep_stage_runs_before_the_tail(self, monkeypatch):
        log = _Log()
        _wire(monkeypatch, log)

        _run(first_pass_ports=FAST)

        names = log.names()
        sweeps = [i for i, n in enumerate(names) if n.endswith(":construct")]
        assert len(sweeps) >= 2, f"expected a fast pass and a tail, got {names}"
        assert "ssh_scan" in names, "the deep branch never ran"
        assert names.index("ssh_scan") < sweeps[-1], (
            "the deep branch waited for the whole range — that is the bug "
            f"({names})")

    def test_the_fast_pass_covers_the_branch_catalogs_and_the_caller_list(
            self, monkeypatch):
        log = _Log()
        _wire(monkeypatch, log)

        _run(first_pass_ports=FAST)

        first = set(log.ports_for("port_scan:construct")[0])
        assert set(FAST) <= first
        assert SSH_PORTS <= first, (
            "a fast pass without the branch ports cannot assess anything")
        assert len(first) < len(REQUESTED)

    def test_the_two_phases_cover_exactly_the_requested_range(self, monkeypatch):
        log = _Log()
        _wire(monkeypatch, log)

        _run(first_pass_ports=FAST)

        sweeps = (log.ports_for("port_scan:construct")
                  + log.ports_for("syn_scan:construct"))
        scanned = set().union(*(set(s) for s in sweeps))
        # Exactly what a single-phase run of the same request would cover: the
        # requested range UNION the branch catalogs.
        expected = set(_port_candidates("it", None, port_override=REQUESTED))
        assert scanned == expected, "phasing changed the coverage"
        # No port is probed twice across the phases.
        assert sum(len(s) for s in sweeps) == len(scanned)


class TestTailFindings:
    def test_a_port_found_only_by_the_tail_still_gets_a_banner(self, monkeypatch):
        log = _Log()
        _wire(monkeypatch, log, open_in_first=(22,),
              open_in_tail=(TAIL_ONLY_OPEN,))

        _run(first_pass_ports=FAST)

        bannered = set().union(*(set(p) for p in log.ports_for("service_banner")))
        assert TAIL_ONLY_OPEN in bannered, (
            "the tail's open port was never fingerprinted, so it reaches the "
            "manager as a bare port number")

    def test_the_tail_open_ports_reach_the_asset(self, monkeypatch):
        log = _Log()
        _wire(monkeypatch, log, open_in_first=(22,),
              open_in_tail=(TAIL_ONLY_OPEN,))

        assets = _run(first_pass_ports=FAST)

        assert TAIL_ONLY_OPEN in assets[HOST].open_ports_for_deep_scan()


class TestUnphasedRunsAreUnchanged:
    def test_no_fast_list_means_a_single_sweep(self, monkeypatch):
        log = _Log()
        _wire(monkeypatch, log)

        _run()

        sweeps = (log.ports_for("port_scan:construct")
                  + log.ports_for("syn_scan:construct"))
        assert len(sweeps) == 1
        assert set(REQUESTED) <= set(sweeps[0])

    def test_a_port_stage_only_job_is_not_phased(self, monkeypatch):
        """Nothing runs after the port stage, so splitting it buys nothing and
        would only add a second scanner setup."""
        log = _Log()
        _wire(monkeypatch, log)

        _run(first_pass_ports=FAST, stage_ceiling="port_scan")

        sweeps = (log.ports_for("port_scan:construct")
                  + log.ports_for("syn_scan:construct"))
        assert len(sweeps) == 1
        assert set(REQUESTED) <= set(sweeps[0])


class TestTailRefreshesTheBuffer:
    """A host committed BEFORE the tail holds pre-tail evidence. If the job then
    dies, the manager promotes a result that understates what was scanned — so
    every host is re-committed once the tail has run.

    Counted by COMPLETE commits, not by calls. Evidence is now also committed at
    every stage boundary (see test_stage_boundary_commits.py), so raw call
    counts no longer isolate this behaviour — but those are partial, and only a
    complete commit says "this host is finished", which is the thing the tail
    has to refresh.
    """

    def _complete_commits(self, monkeypatch, **kw) -> int:
        log = _Log()
        _wire(monkeypatch, log)
        commits: list[tuple[str, bool]] = []

        def _sink(host, facts, *, complete=True):
            commits.append((host, complete))

        _run(on_host_complete=_sink, **kw)
        return sum(1 for host, done in commits if host == HOST and done)

    def test_every_host_is_committed_again_after_the_tail(self, monkeypatch):
        assert self._complete_commits(monkeypatch, first_pass_ports=FAST) == 2, (
            "expected a final commit after the assessment AND after the tail")

    def test_an_unphased_run_commits_once_per_host(self, monkeypatch):
        """No tail, so no second pass to refresh."""
        assert self._complete_commits(monkeypatch) == 1
