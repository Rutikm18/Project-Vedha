"""
test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).

The funnel chains discovery → port scan → routed deep scanners, passing results
forward so deep scanners only probe ports the port scan already found open (the
"don't re-probe the same host" win). Tests use injected fake stages so the
orchestration logic is verified without any network I/O.
"""

from __future__ import annotations

import asyncio

import pytest

from scanner.scanner_base import ScanResult, ScopeGuard
from scanner.scan_funnel import (
    ScanFunnel, FunnelResult, route_ports, reconcile_ports,
)


# ── fakes (real objects with the scan_target contract, no mocks) ──────────────

class FakeDiscovery:
    def __init__(self, alive: bool = True):
        self.alive = alive
        self.calls: list[str] = []

    async def scan_target(self, target: str) -> list[ScanResult]:
        self.calls.append(target)
        return [ScanResult("host_discovery", target,
                           status="open" if self.alive else "filtered",
                           data={"alive": self.alive})]


class FakePortScanner:
    def __init__(self, open_ports: list[int]):
        self.open_ports = open_ports
        self.scanned: list[str] = []
        self.constructed_ports: list[int] | None = None

    async def scan_target(self, target: str) -> list[ScanResult]:
        self.scanned.append(target)
        return [ScanResult("port_scan", target, port=p, proto="tcp",
                           status="open")
                for p in self.open_ports]


class RecordingDeep:
    def __init__(self, name: str, ports: list[int]):
        self.name = name
        self.ports = list(ports)
        self.scanned: list[str] = []

    async def scan_target(self, target: str) -> list[ScanResult]:
        self.scanned.append(target)
        return [ScanResult(self.name, target,
                           port=(self.ports[0] if self.ports else None),
                           status="open", data={"scanned_ports": self.ports})]


def _scope() -> ScopeGuard:
    return ScopeGuard.from_list(["10.0.0.0/8", "127.0.0.0/8"])


def _make_funnel(open_ports, *, alive=True, force=False, routes=None):
    """Build a funnel with fakes; return (funnel, discovery, port_scanner, created)."""
    discovery = FakeDiscovery(alive=alive)
    port_scanner = FakePortScanner(open_ports)
    created: dict[str, RecordingDeep] = {}

    def _deep_factory(name):
        def factory(ports):
            inst = RecordingDeep(f"{name}_scan", ports)
            created[name] = inst
            return inst
        return factory

    deep_factories = {
        "tls": _deep_factory("tls"),
        "db": _deep_factory("db"),
        "smb": _deep_factory("smb"),
        "web": _deep_factory("web"),
        "ai": _deep_factory("ai"),
    }

    funnel = ScanFunnel(
        _scope(),
        discovery=discovery,
        port_scanner_factory=lambda ports: port_scanner,
        deep_scanner_factories=deep_factories,
        routes=routes,
        force=force,
    )
    return funnel, discovery, port_scanner, created


# ── route_ports (pure logic) ──────────────────────────────────────────────────

class TestRoutePorts:
    def test_intersection_only(self):
        routes = {"tls": [443, 8443], "db": [3306, 5432]}
        assert route_ports([443, 22, 3306], routes) == {"tls": [443], "db": [3306]}

    def test_no_match_returns_empty(self):
        routes = {"tls": [443]}
        assert route_ports([22, 80], routes) == {}

    def test_port_in_multiple_routes(self):
        routes = {"tls": [443], "web": [443, 80]}
        out = route_ports([443], routes)
        assert out == {"tls": [443], "web": [443]}

    def test_sorted_output(self):
        routes = {"web": [80, 8080, 443]}
        assert route_ports([8080, 80, 443], routes) == {"web": [80, 443, 8080]}


# ── funnel orchestration ──────────────────────────────────────────────────────

class TestScanFunnel:
    def test_dead_host_skips_port_scan(self):
        funnel, discovery, port_scanner, created = _make_funnel(
            [22, 443], alive=False, force=False)
        result = asyncio.run(funnel.run_host("10.0.0.1"))
        assert isinstance(result, FunnelResult)
        assert result.alive is False
        assert port_scanner.scanned == []          # never port-scanned a dead host
        assert result.stages_run == ["discovery"]
        assert created == {}                        # no deep scanners

    def test_dead_host_forced_runs_full(self):
        funnel, discovery, port_scanner, created = _make_funnel(
            [443], alive=False, force=True)
        result = asyncio.run(funnel.run_host("10.0.0.1"))
        assert port_scanner.scanned == ["10.0.0.1"]
        assert "port_scan" in result.stages_run

    def test_open_ports_extracted(self):
        funnel, _, _, _ = _make_funnel([22, 80, 443])
        result = asyncio.run(funnel.run_host("10.0.0.1"))
        assert result.open_tcp_ports == [22, 80, 443]

    def test_deep_scanner_receives_only_open_ports(self):
        # Open {22, 443}; tls route handles 443 (+others) -> tls gets exactly [443]
        funnel, _, _, created = _make_funnel([22, 443])
        asyncio.run(funnel.run_host("10.0.0.1"))
        assert "tls" in created
        assert created["tls"].ports == [443]        # NOT re-probing 22 or all TLS ports

    def test_db_scanner_not_invoked_without_db_port(self):
        funnel, _, _, created = _make_funnel([22, 443])
        asyncio.run(funnel.run_host("10.0.0.1"))
        assert "db" not in created                  # no db port open -> db skipped

    def test_db_scanner_invoked_with_db_port(self):
        funnel, _, _, created = _make_funnel([3306])
        asyncio.run(funnel.run_host("10.0.0.1"))
        assert "db" in created
        assert created["db"].ports == [3306]

    def test_no_open_ports_runs_no_deep_scanners(self):
        funnel, _, port_scanner, created = _make_funnel([])
        result = asyncio.run(funnel.run_host("10.0.0.1"))
        assert port_scanner.scanned == ["10.0.0.1"]  # port scan still ran
        assert created == {}                         # but nothing to route
        assert result.open_tcp_ports == []

    def test_results_aggregate_all_stages(self):
        funnel, _, _, _ = _make_funnel([443])
        result = asyncio.run(funnel.run_host("10.0.0.1"))
        scanners = {r.scanner for r in result.results}
        assert "host_discovery" in scanners
        assert "port_scan" in scanners
        assert "tls_scan" in scanners

    def test_out_of_scope_target(self):
        funnel, discovery, port_scanner, _ = _make_funnel([443])
        result = asyncio.run(funnel.run_host("8.8.8.8"))
        assert discovery.calls == []                 # never touched
        assert result.results[0].status == "error"

    def test_stages_run_order(self):
        funnel, _, _, _ = _make_funnel([443, 3306])
        result = asyncio.run(funnel.run_host("10.0.0.1"))
        assert result.stages_run[0] == "discovery"
        assert result.stages_run[1] == "port_scan"
        assert "tls" in result.stages_run
        assert "db" in result.stages_run


class TestBuildDefaultFunnel:
    def test_constructs_and_wires_real_scanners(self):
        # Verifies every factory produces a real scanner without arg errors —
        # exercises the actual class signatures (TLS/DB/SMB/Web/MCP-AI).
        from scanner.scan_funnel import build_default_funnel
        funnel = build_default_funnel(_scope(), with_udp=True)
        assert funnel.udp_scanner is not None
        for route, factory in funnel.deep_scanner_factories.items():
            scanner = factory([443] if route != "db" else [3306])
            assert hasattr(scanner, "scan_target")

    def test_port_scanner_is_syn_scanner(self):
        # The funnel's port stage should be the SYN scanner (which itself falls
        # back to a connect scan when raw sockets aren't available).
        from scanner.scan_funnel import build_default_funnel
        from scanner.syn_scanner import SynScanner
        funnel = build_default_funnel(_scope())
        port_stage = funnel.port_scanner_factory([443])
        assert isinstance(port_stage, SynScanner)

    def test_candidate_ports_cover_all_routes(self):
        from scanner.scan_funnel import _candidate_ports, DEFAULT_PORT_ROUTES
        cands = set(_candidate_ports(DEFAULT_PORT_ROUTES))
        for ports in DEFAULT_PORT_ROUTES.values():
            assert set(ports).issubset(cands)


# ── reconcile_ports (pure logic) ──────────────────────────────────────────────

class TestReconcilePorts:
    def test_union_dedup_sorted(self):
        assert reconcile_ports([135, 445, 3389], [49668, 49664]) == \
            [135, 445, 3389, 49664, 49668]

    def test_ignores_non_ints_and_empty(self):
        assert reconcile_ports(None, [80], [80, "x", 443]) == [80, 443]


# ── MSRPC endpoint-mapper reconciliation (Stage 3b) ───────────────────────────

class _OpenSetPortFactory:
    """Port-scanner factory whose scanners report a port open iff it is in
    `actually_open`. Records every port set requested, so a test can prove the
    ephemeral RPC range was actually scanned by the reconcile pass."""

    def __init__(self, actually_open):
        self.actually_open = set(actually_open)
        self.requested: list[list[int]] = []

    def __call__(self, ports):
        ports = list(ports)
        self.requested.append(sorted(ports))
        actually_open = self.actually_open

        class _PS:
            async def scan_target(self, target):
                return [ScanResult("port_scan", target, port=p, proto="tcp",
                                   status="open")
                        for p in ports if p in actually_open]
        return _PS()


class _FakeMSRPC:
    """A deep scanner on 135 that returns EPM-advertised dynamic ports."""

    def __init__(self, ports, advertised):
        self.advertised = advertised

    async def scan_target(self, target):
        return [ScanResult("msrpc_scan", target, port=135, proto="tcp",
                           status="open",
                           data={"msrpc": True, "dynamic_tcp_ports": self.advertised})]


class TestRpcReconcile:
    def _funnel(self, actually_open, advertised):
        factory = _OpenSetPortFactory(actually_open)
        return ScanFunnel(
            _scope(),
            discovery=FakeDiscovery(alive=True),
            port_scanner_factory=factory,
            deep_scanner_factories={
                "msrpc": lambda ports: _FakeMSRPC(ports, advertised)},
            routes={"msrpc": [135]},
        ), factory

    def test_advertised_ports_are_scanned_and_only_reachable_confirmed(self):
        # 135 open; EPM advertises 49664 (reachable) and 49668 (advertised but
        # NOT reachable from this vantage).
        funnel, factory = self._funnel(
            actually_open=[135, 49664], advertised=[49664, 49668])
        result = asyncio.run(funnel.run_host("10.0.0.7"))

        # The ephemeral range EPM advertised was actually port-scanned (the gap).
        assert [49664, 49668] in factory.requested
        assert "rpc_reconcile" in result.stages_run
        # Canonical open set = union of base scan + CONFIRMED dynamic ports only.
        # 49668 was advertised but unreachable → never labeled open (honesty rule).
        assert result.open_tcp_ports == [135, 49664]

        summary = next(r for r in result.results if r.scanner == "rpc_reconcile")
        assert summary.data["epm_advertised_dynamic_ports"] == [49664, 49668]
        assert summary.data["confirmed_open"] == [49664]
        assert summary.data["canonical_open_tcp_ports"] == [135, 49664]

    def test_no_dynamic_ports_no_reconcile_stage(self):
        funnel, _ = self._funnel(actually_open=[135], advertised=[])
        result = asyncio.run(funnel.run_host("10.0.0.7"))
        assert "rpc_reconcile" not in result.stages_run
        assert result.open_tcp_ports == [135]


class TestScanFunnelRun:
    def test_run_writes_all_results(self):
        funnel, _, _, _ = _make_funnel([443])

        class ListWriter:
            def __init__(self):
                self.results = []

            def write(self, r):
                self.results.append(r)

        writer = ListWriter()
        asyncio.run(funnel.run(["10.0.0.1", "10.0.0.2"], writer))
        scanners = {r.scanner for r in writer.results}
        assert "host_discovery" in scanners
        assert "port_scan" in scanners
        assert "tls_scan" in scanners
        targets = {r.target for r in writer.results}
        assert targets == {"10.0.0.1", "10.0.0.2"}
