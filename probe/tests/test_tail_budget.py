"""
The port tail runs inside the JOB's time budget, not only each host's.

`deep` sweeps all 65,535 ports in two phases: a first pass over the high-signal
ports, which every later stage assesses, then the remaining ~64,000 as a tail.
Admission sizes a phased job by its first pass, so a /24 aggressive scan is
admitted on a ~32-minute first pass. The tail was bounded only per host
(max_host_seconds), so that /24 queued ~30 hours of tail behind a 2-hour
ceiling and always ended as job_deadline_exceeded, with the stages after the
tail (liveness verdicts, credentialed collection) never run.

The contract pinned here:

  * the engine gives the tail a deadline that leaves a reserve inside the
    ceiling for everything after it;
  * each host's tail budget is fixed when that host STARTS: the time left,
    capped by max_host_seconds, and never 0, because both scanners read a
    falsy budget as unbounded;
  * the tail keeps ONE shared scanner, because its rate limiter, socket
    semaphore and SYN pacer are what hold the stage to the admitted envelope;
    the per-host budget travels per call instead;
  * nothing is cancelled: the scanners stop sending at their budget, and the
    ports they did not reach are reported not_scanned;
  * the recorded estimate says when it covers only the first pass.
"""
from __future__ import annotations

import asyncio
import socket
import time
import types
from dataclasses import dataclass

import pytest

from agent import engine
from agent import feasibility as fz
from scanner import port_scanner as ps
from scanner import syn_scanner as ss
from scanner.scanner_base import ScanResult, ScopeGuard
from workflow import workflow_engine as we
from workflow.branches import BRANCHES

SCOPE = ScopeGuard.from_list(["10.91.0.0/24"], strict=True)
HOSTS = ["10.91.0.1", "10.91.0.2", "10.91.0.3"]
OUTSIDE = "10.92.0.1"                      # not in SCOPE
REQUESTED = list(range(1, 4001))           # the breadth the job asked for
FAST = [22, 80, 445]                       # the caller's high-signal list
TAIL_MARKER = 3999                         # swept only by the tail
SSH_CREDS = {"user": "svc", "password": "x"}

_NOT_GIVEN = object()


@dataclass
class _TailCall:
    scanner: object
    host: str
    budget: float | None
    started: float


class _Record:
    def __init__(self):
        self.tail_instances: list[object] = []
        self.tail_calls: list[_TailCall] = []
        self.scanned_hosts: list[str] = []
        self.collected: list[str] = []


def _wire(monkeypatch, rec: _Record, *, tail_delay: float = 0.0):
    """Stub every scanner and collector the engine builds.

    The port scanners report the budget a sweep would actually run under: the
    per-call `deadline_seconds` when one is passed, the instance attribute
    otherwise, which is how the real scanners resolve it.
    """

    def _port_scanner(kind):
        class Scanner:
            name = kind

            def __init__(self, *a, ports=None, deadline_seconds=None, **kw):
                self.ports = sorted(ports or [])
                self.deadline_seconds = deadline_seconds
                self.is_tail = TAIL_MARKER in self.ports
                if self.is_tail:
                    rec.tail_instances.append(self)

            async def scan_target(self, host, *, deadline_seconds=_NOT_GIVEN):
                rec.scanned_hosts.append(host)
                budget = (self.deadline_seconds if deadline_seconds is _NOT_GIVEN
                          else deadline_seconds)
                if self.is_tail:
                    rec.tail_calls.append(
                        _TailCall(self, host, budget, time.monotonic()))
                    if tail_delay:
                        await asyncio.sleep(tail_delay)
                    return []
                return [ScanResult("port_scan", host, port=22, proto="tcp",
                                   status="open",
                                   data={"reason": "connect_success"})]
        return Scanner

    class _Discovery:
        name = "host_discovery"

        def __init__(self, *a, **kw):
            pass

        async def scan_target(self, host):
            rec.scanned_hosts.append(host)
            return [ScanResult("host_discovery", host, status="open",
                               data={"alive": True})]

    def _inert(component):
        class Inert:
            name = component

            def __init__(self, *a, **kw):
                pass

            async def scan_target(self, host):
                return []
        return Inert

    class _Collector:
        """Not a BaseScanner: the real collectors expose .run(targets, sink)."""

        def __init__(self, *a, **kw):
            pass

        async def run(self, targets, sink):
            for host in targets:
                rec.collected.append(host)
                sink.write(ScanResult("ssh_inventory", host, status="observed",
                                      data={"os": "linux"}))

    monkeypatch.setattr(we, "HostDiscoveryScanner", _Discovery)
    monkeypatch.setattr(we, "PortScanner", _port_scanner("port_scan"))
    monkeypatch.setattr(we, "SynScanner", _port_scanner("syn_scan"))
    monkeypatch.setattr(we, "ServiceBannerScanner", _inert("service_banner"))
    monkeypatch.setattr(we, "OSFingerprintScanner", _inert("os_fingerprint"))
    monkeypatch.setattr(we, "UDPScanner", _inert("udp_scan"))
    # Host-level and datagram branches run whether or not a TCP port is open,
    # so every branch has to be inert or the test probes the real network.
    for spec in BRANCHES:
        monkeypatch.setattr(we, spec.scanner, _inert(spec.component))
    monkeypatch.setattr(we, "SSHCollector", _Collector)


def _run(targets=None, **kwargs):
    defaults = dict(profile="it", port_override=REQUESTED,
                    first_pass_ports=FAST, stage_ceiling="deep_scan",
                    host_concurrency=2, rate=100_000, concurrency=10,
                    timeout=0.01, disc_timeout=0.01, retries=0)
    defaults.update(kwargs)
    return asyncio.run(we.run_engagement(list(targets or HOSTS), SCOPE,
                                         **defaults))


# ── the reported case: a tail that cannot fit ───────────────────────────────

class TestATailThatCannotFit:
    def test_every_host_gets_a_vanishing_positive_budget(self, monkeypatch):
        """Deadline already passed. A zero budget would read as UNBOUNDED in
        both scanners and sweep the whole tail; a vanishing positive one
        probes nothing and reports those ports not_scanned."""
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(tail_deadline=time.monotonic() - 5, max_host_seconds=1800)

        assert sorted(c.host for c in rec.tail_calls) == sorted(HOSTS)
        for call in rec.tail_calls:
            assert call.budget is not None and 0 < call.budget <= 0.01, (
                f"{call.host} got a tail budget of {call.budget!r} after the "
                f"job's tail deadline had passed")

    def test_the_job_finishes_and_the_stages_after_the_tail_still_run(
            self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        assets = _run(tail_deadline=time.monotonic() - 5,
                      max_host_seconds=1800, ssh_creds=SSH_CREDS)

        assert set(assets) >= set(HOSTS), "run_engagement did not return"
        assert sorted(rec.collected) == sorted(HOSTS), (
            "credentialed collection, which runs after the tail, never ran")


# ── the budget each host gets ───────────────────────────────────────────────

class TestTheBudgetEachHostGets:
    def test_no_tail_deadline_leaves_the_per_host_budget_unchanged(
            self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(max_host_seconds=1800)

        assert rec.tail_calls, "the tail never ran"
        assert {c.budget for c in rec.tail_calls} == {1800}

    def test_no_tail_deadline_and_no_host_budget_stays_unbounded(
            self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(max_host_seconds=None)

        assert rec.tail_calls, "the tail never ran"
        assert {c.budget for c in rec.tail_calls} == {None}

    def test_the_time_left_binds_when_it_is_shorter(self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(tail_deadline=time.monotonic() + 100, max_host_seconds=1800)

        for call in rec.tail_calls:
            assert 90 < call.budget <= 100, (
                f"{call.host}: expected ~100 s left, got {call.budget}")

    def test_the_host_budget_binds_when_it_is_shorter(self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(tail_deadline=time.monotonic() + 10_000, max_host_seconds=1800)

        assert {c.budget for c in rec.tail_calls} == {1800}

    def test_without_a_host_budget_the_time_left_is_the_budget(
            self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(tail_deadline=time.monotonic() + 50, max_host_seconds=None)

        for call in rec.tail_calls:
            assert 40 < call.budget <= 50, call.budget

    def test_the_budget_is_fixed_when_each_host_starts(self, monkeypatch):
        """One host at a time, each taking 0.2 s: a later host has less time
        left, so its budget is smaller by at least the time it waited.

        Lower-bound assertions only: a real `asyncio.sleep(0.2)` between hosts
        only ever runs LATE on a loaded box, never early, so a slower CI only
        widens every gap checked here. A tight `abs(...) < 0.05` equality
        against wall-clock timing used to flake for exactly that reason.
        """
        rec = _Record()
        _wire(monkeypatch, rec, tail_delay=0.2)
        deadline = time.monotonic() + 100

        _run(tail_deadline=deadline, max_host_seconds=1800,
             host_concurrency=1)

        calls = sorted(rec.tail_calls, key=lambda c: c.started)
        assert len(calls) == len(HOSTS)
        for call in calls:
            assert call.budget is not None and 0 < call.budget <= 100
        for earlier, later in zip(calls, calls[1:]):
            assert later.budget < earlier.budget, (
                "a host that starts later must get a smaller budget")
        assert calls[-1].budget <= calls[0].budget - 0.35


# ── one shared scanner, scope unchanged ─────────────────────────────────────

class TestTheTailKeepsOneSharedScanner:
    def test_every_host_is_swept_by_the_same_scanner(self, monkeypatch):
        """The rate limiter, socket semaphore and SYN pacer live on the
        scanner INSTANCE. One per host would multiply the tail's send rate
        by the number of hosts in flight."""
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(tail_deadline=time.monotonic() + 100, max_host_seconds=1800)

        assert len(rec.tail_instances) == 1, (
            f"{len(rec.tail_instances)} tail scanners built; the tail must "
            f"share one")
        assert {id(c.scanner) for c in rec.tail_calls} == \
            {id(rec.tail_instances[0])}

    def test_the_syn_path_also_shares_one_scanner(self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        _run(tail_deadline=time.monotonic() + 100, max_host_seconds=1800,
             scan_method="syn")

        assert len(rec.tail_instances) == 1
        assert rec.tail_instances[0].name == "syn_scan"
        assert len(rec.tail_calls) == len(HOSTS)


class TestScopeIsUnchanged:
    def test_an_out_of_scope_target_is_never_swept(self, monkeypatch):
        rec = _Record()
        _wire(monkeypatch, rec)

        _run([*HOSTS, OUTSIDE], tail_deadline=time.monotonic() + 100,
             max_host_seconds=1800)

        assert OUTSIDE not in rec.scanned_hosts
        assert sorted(c.host for c in rec.tail_calls) == sorted(HOSTS)

    def test_the_wrapper_forwards_only_the_host_it_is_given(self):
        """It delegates to scan_target, the method _scan_one calls on any
        scanner, so it takes exactly the path every per-host stage takes;
        scope is enforced where run_engagement filters its targets."""
        calls = []

        class _Shared:
            name = "syn_scan"

            async def scan_target(self, host, *, deadline_seconds):
                calls.append((host, deadline_seconds))
                return []

        budgets = iter([7.0, 3.0])
        wrapper = we._BudgetedScan(_Shared(), lambda: next(budgets))

        asyncio.run(we._gather_per_host(wrapper, HOSTS[:2], max_in_flight=1))

        assert wrapper.name == "syn_scan"
        assert calls == [(HOSTS[0], 7.0), (HOSTS[1], 3.0)]


# ── the scanners take a per-call budget ─────────────────────────────────────

def _virtual_clock(monkeypatch, module):
    """Replace ONE module's `time` so each monotonic() read advances 1 s.

    Only that module sees it — the event loop keeps the real clock — and the
    budget is spent before the first worker can dequeue a port, whatever the
    speed of the machine running the test.
    """
    offset = {"now": 0.0}

    def _monotonic():
        offset["now"] += 1.0
        return time.monotonic() + offset["now"]
    monkeypatch.setattr(module, "time",
                        types.SimpleNamespace(monotonic=_monotonic))


def _summary(results):
    return next(r.data for r in results if r.status == "scan_summary")


def _closed_probe(probed):
    async def _probe(target, port, *a, **kw):
        probed.append(port)
        return ScanResult("port_scan", target, port=port, proto="tcp",
                          status="closed", data={"reason": "refused"})
    return _probe


class TestPortScannerPerCallBudget:
    def test_a_vanishing_per_call_budget_probes_nothing(self, monkeypatch):
        probed: list[int] = []
        sc = ps.PortScanner(SCOPE, ports=list(range(1, 201)), timeout=0.05)
        sc._scan_port = _closed_probe(probed)
        _virtual_clock(monkeypatch, ps)

        results = asyncio.run(sc.scan_target(HOSTS[0], deadline_seconds=0.001))

        summary = _summary(results)
        assert probed == []
        assert summary["ports_attempted"] == 0
        assert summary["ports_not_scanned"] == 200
        assert summary["budget_exhausted"] is True
        assert [r for r in results if r.status != "scan_summary"] == [], (
            "a port the clock stopped must not be reported with a state")

    def test_the_instance_budget_is_never_mutated(self, monkeypatch):
        """Calls run concurrently on one shared instance."""
        sc = ps.PortScanner(SCOPE, ports=[1, 2], timeout=0.05,
                            deadline_seconds=1800)
        sc._scan_port = _closed_probe([])
        _virtual_clock(monkeypatch, ps)

        asyncio.run(sc.scan_target(HOSTS[0], deadline_seconds=0.001))

        assert sc.deadline_seconds == 1800

    def test_without_the_keyword_behaviour_is_unchanged(self):
        probed: list[int] = []
        sc = ps.PortScanner(SCOPE, ports=list(range(1, 21)), timeout=0.05)
        sc._scan_port = _closed_probe(probed)

        results = asyncio.run(sc.scan_target(HOSTS[0]))

        summary = _summary(results)
        assert sorted(probed) == list(range(1, 21))
        assert summary["ports_attempted"] == 20
        assert summary["budget_exhausted"] is False


class TestSynScannerPerCallBudget:
    def test_the_connect_fallback_honours_it(self, monkeypatch):
        """The fallback is built at construction with the instance budget, so
        only a per-call value that is passed through can reach it."""
        probed: list[int] = []
        sc = ss.SynScanner(SCOPE, ports=list(range(1, 51)),
                           force_fallback=True, timeout=0.05)
        sc._fallback._scan_port = _closed_probe(probed)
        _virtual_clock(monkeypatch, ps)

        results = asyncio.run(sc.scan_target(HOSTS[0], deadline_seconds=0.001))

        summary = _summary(results)
        assert probed == []
        assert summary["ports_attempted"] == 0
        assert summary["ports_not_scanned"] == 50
        assert summary["method"] == "connect_fallback"
        assert sc._fallback.deadline_seconds is None

    def test_the_raw_path_receives_it(self):
        seen = []
        sc = ss.SynScanner(SCOPE, ports=[80], deadline_seconds=1800)
        sc._supported = True

        def _blocking(target, deadline_seconds=None):
            seen.append((target, deadline_seconds))
            return []
        sc._syn_scan_blocking = _blocking

        asyncio.run(sc.scan_target(HOSTS[0], deadline_seconds=7.0))

        assert seen == [(HOSTS[0], 7.0)]
        assert sc.deadline_seconds == 1800

    def test_the_raw_send_loop_stops_at_it(self, monkeypatch):
        """Driven with fake sockets (raw sockets cannot run in CI) and a clock
        that advances 1 s per packet: a 10 s per-call budget truncates a
        100-port sweep that has no instance budget at all."""
        sc = ss.SynScanner(SCOPE, ports=list(range(1, 101)), key=b"\x01" * 16,
                           retries=0, timeout=0.01, pace_sends=False)
        sent: list[int] = []
        monkeypatch.setattr(ss.random, "randint", lambda a, b: 50000)
        monkeypatch.setattr(
            ss, "resolve",
            lambda t, p, proto="tcp", family=None: (socket.AF_INET, (t, 0)))
        monkeypatch.setattr(ss, "_local_source_ip", lambda dst: "10.91.0.250")
        clock = {"now": 0.0}
        real_monotonic = ss.time.monotonic
        monkeypatch.setattr(ss.time, "monotonic",
                            lambda: real_monotonic() + clock["now"])

        class _Send:
            def setsockopt(self, *a): pass

            def sendto(self, pkt, addr):
                sent.append(ss.parse_packet(pkt)["dst_port"])
                clock["now"] += 1.0

            def close(self): pass

        class _Recv:
            def setblocking(self, *a): pass
            def setsockopt(self, *a): pass

            def recv(self, n):
                raise OSError("no data")

            def close(self): pass

        def _factory(family, stype, proto):
            return _Recv() if proto == socket.IPPROTO_TCP else _Send()
        monkeypatch.setattr(ss.socket, "socket", _factory)

        sc._syn_scan_blocking(HOSTS[0], 10)

        assert 0 < len(sent) < 100, (
            f"expected a truncated sweep, sent {len(sent)} of 100 ports")


# ── the engine's policy and wiring ──────────────────────────────────────────

class TestTheEnginePolicy:
    def test_the_reserve_is_fifteen_percent_of_a_two_hour_ceiling(self):
        assert engine._tail_deadline(1000.0, 7200.0) == 1000.0 + 7200.0 - 1080.0

    def test_the_reserve_never_drops_below_five_minutes(self):
        assert engine._tail_deadline(1000.0, 1200.0) == 1000.0 + 1200.0 - 300.0

    def test_a_ceiling_shorter_than_the_reserve_leaves_the_tail_nothing(self):
        assert engine._tail_deadline(1000.0, 60.0) == 1000.0

    def test_run_scan_hands_the_tail_a_deadline_inside_the_ceiling(
            self, monkeypatch):
        seen: dict = {}

        async def _fake(targets, scope, *, cache, trace, **kwargs):
            seen.update(kwargs)
            trace.finalize()
            return {}
        monkeypatch.setattr(engine, "run_engagement", _fake)

        before = time.monotonic()
        result = engine.run_scan(
            "discovery", {"target": "10.0.0.1", "max_runtime_seconds": 3600},
            validated_scope=["10.0.0.0/24"])
        after = time.monotonic()

        ceiling = result["run_stats"]["applied_tuning"]["max_runtime_seconds"]
        reserve = max(300.0, 0.15 * ceiling)
        assert before + ceiling - reserve <= seen["tail_deadline"] \
            <= after + ceiling - reserve


class TestTheEstimateSaysWhatItCovers:
    def test_the_default_scope_is_the_full_sweep(self):
        est = fz.estimate(hosts=1, ports=100, rate=100, ceiling_seconds=60)
        assert fz.as_run_stats(est)["scope"] == "full_sweep"

    def test_a_phased_job_records_a_first_pass_estimate(self):
        # deep_port_sweep phases the full 65,535-port range: admission is sized by
        # the first pass, so the estimate records scope="first_pass". (network_va
        # aggressive is the bounded enterprise set now — a single full_sweep.)
        result = engine.run_scan("deep_port_sweep", {
            "targets": ["10.77.0.1", "10.77.0.2", "10.77.0.3"],
            "scope_cidrs": ["10.77.0.0/24"],
            "intensity": "deep",
            "max_runtime_seconds": 1,
        })
        assert result["error_code"] == "job_cannot_finish"
        assert result["facts"] == []
        assert result["run_stats"]["timing"]["estimate"]["scope"] == "first_pass"

    def test_an_unphased_job_records_a_full_sweep_estimate(self):
        result = engine.run_scan("full_port_audit", {
            "targets": ["10.77.0.1"],
            "scope_cidrs": ["10.77.0.0/22"],
            "intensity": "deep",
            "rate": 600,
            "concurrency": 300,
            "max_runtime_seconds": 30,
        })
        assert result["error_code"] == "job_cannot_finish"
        assert result["run_stats"]["timing"]["estimate"]["scope"] == "full_sweep"
