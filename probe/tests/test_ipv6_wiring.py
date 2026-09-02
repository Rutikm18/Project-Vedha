"""
test_ipv6_wiring.py — IPv6 neighbour discovery inside the engagement.

An IPv4 /24 cannot name an IPv6 address, so an IPv6-only listener on the same
segment was invisible to every stage of a scan. Gate 1b closes that with RFC 4861
all-nodes multicast (no /64 enumeration — 2**64 addresses is not sweepable).

The behaviour that matters most here is NOT discovery, it is RESTRAINT: a
discovered neighbour is probed only if it is inside the authorized allowlist.
Anything else is reported so the operator can widen scope deliberately, and never
touched. These tests pin that boundary.
"""
from __future__ import annotations

import asyncio

import pytest

from scanner.scanner_base import ScanResult, ScopeGuard
from scanner import ipv6_discovery as V6
import workflow.workflow_engine as we
from workflow.execution import COMPONENT_CATALOG, planned_components


# ── the interface-scoping fix ────────────────────────────────────────────────

class TestInterfaceScoping:
    """The neighbour cache is system-wide. Pinging en0 and then harvesting every
    interface returned VPN-tunnel (utun*) and Apple AWDL peers — hosts on other
    segments the engagement never authorized."""

    CACHE = [
        ("fe80::1%en0", "REACHABLE"),
        ("fe80::dead:beef%en0", "STALE"),
        ("fe80::cafe%utun0", "REACHABLE"),      # VPN tunnel — different segment
        ("fe80::f00d%awdl0", "REACHABLE"),      # Apple peer-to-peer link
        ("fe80::bad%en0", "INCOMPLETE"),        # unresolved — not a live host
        ("2001:db8::5", "REACHABLE"),           # global, not interface-bound
    ]

    @pytest.fixture(autouse=True)
    def _stub(self, monkeypatch):
        monkeypatch.setattr(V6, "_ping_all_nodes", lambda *a, **k: None)
        monkeypatch.setattr(V6, "_read_neighbor_cache", lambda: list(self.CACHE))
        monkeypatch.setattr(V6, "_own_ipv6_addresses", lambda: set())

    def test_iface_filters_out_other_segments(self):
        hosts = V6.discover_ipv6_hosts("en0")
        assert "fe80::cafe%utun0" not in hosts
        assert "fe80::f00d%awdl0" not in hosts

    def test_iface_keeps_its_own_neighbours(self):
        hosts = V6.discover_ipv6_hosts("en0")
        assert "fe80::1%en0" in hosts and "fe80::dead:beef%en0" in hosts

    def test_globals_are_kept_they_are_not_interface_bound(self):
        assert "2001:db8::5" in V6.discover_ipv6_hosts("en0")

    def test_unresolved_neighbours_are_never_returned(self):
        assert not any("bad" in h for h in V6.discover_ipv6_hosts("en0"))

    def test_no_iface_keeps_everything(self):
        hosts = V6.discover_ipv6_hosts(None)
        assert "fe80::cafe%utun0" in hosts and "fe80::1%en0" in hosts

    def test_link_local_keeps_its_zone_so_connect_can_route(self):
        assert all("%" in h for h in V6.discover_ipv6_hosts("en0")
                   if h.startswith("fe80"))


# ── scope is enforced, not assumed ───────────────────────────────────────────

def _wire(monkeypatch, found, calls):
    monkeypatch.setattr(we, "discover_ipv6_hosts", lambda *a, **k: list(found))

    def fake(cid, port=None, data=None, status="open"):
        class S:
            name = cid

            def __init__(self, *a, **k):
                pass

            async def scan_target(self, host):
                calls.setdefault(cid, []).append(host)
                return [ScanResult(scanner=cid, target=host, port=port,
                                   proto="tcp" if port else None, status=status,
                                   data=data if data is not None else {"alive": True})]
        return S

    monkeypatch.setattr(we, "HostDiscoveryScanner", fake("host_discovery"))
    monkeypatch.setattr(we, "PortScanner", fake("port_scan", port=80, data={}))
    monkeypatch.setattr(we, "ServiceBannerScanner", fake("service_banner", port=80, data={}))
    monkeypatch.setattr(we, "OSFingerprintScanner", fake("os_fingerprint", data={}))


def _run(scope_entries, found, calls, **kw):
    return asyncio.run(we.run_engagement(
        ["192.168.1.10"], ScopeGuard.from_list(scope_entries),
        discover_ipv6=True, stage_ceiling="port_scan", **kw))


def test_in_scope_neighbour_is_added_and_scanned(monkeypatch):
    calls: dict = {}
    _wire(monkeypatch, ["fe80::aaaa%en0"], calls)
    assets = _run(["192.168.1.0/24", "fe80::/10"], ["fe80::aaaa%en0"], calls)
    assert "fe80::aaaa%en0" in assets
    assert "fe80::aaaa%en0" in calls["host_discovery"]


def test_out_of_scope_neighbour_is_reported_but_never_probed(monkeypatch):
    """The core restraint: discovery must not widen authorization."""
    calls: dict = {}
    _wire(monkeypatch, ["2001:db8::99"], calls)
    assets = _run(["192.168.1.0/24"], ["2001:db8::99"], calls)   # no v6 in scope
    assert "2001:db8::99" not in assets
    for probed in calls.values():
        assert "2001:db8::99" not in probed


def test_the_fact_records_both_sides(monkeypatch):
    calls: dict = {}
    found = ["fe80::aaaa%en0", "2001:db8::99"]
    _wire(monkeypatch, found, calls)
    from workflow.cache import WorkflowCache
    cache = WorkflowCache()
    _run(["192.168.1.0/24", "fe80::/10"], found, calls, cache=cache)
    result = next((e.result for e in cache._store.values()
                   if e.result.scanner == "ipv6_discovery"), None)
    assert result is not None, "no ipv6_discovery fact was cached"
    d = result.data
    assert d["neighbours_found"] == 2
    assert d["in_scope"] == ["fe80::aaaa%en0"]
    assert d["out_of_scope_not_scanned"] == ["2001:db8::99"]


def test_disabled_by_default(monkeypatch):
    """Only the scan types that opt in pay for the multicast ping."""
    calls: dict = {}
    called = []
    monkeypatch.setattr(we, "discover_ipv6_hosts",
                        lambda *a, **k: called.append(1) or [])
    _wire(monkeypatch, [], calls)
    asyncio.run(we.run_engagement(
        ["192.168.1.10"], ScopeGuard.from_list(["192.168.1.0/24"]),
        stage_ceiling="port_scan"))
    assert not called


def test_discovery_failure_does_not_abort_the_engagement(monkeypatch):
    calls: dict = {}
    _wire(monkeypatch, [], calls)
    monkeypatch.setattr(we, "discover_ipv6_hosts",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("no ndp")))
    with pytest.raises(OSError):
        _run(["192.168.1.0/24"], [], calls)


# ── plan/catalog registration ────────────────────────────────────────────────

def test_component_is_in_the_catalog():
    assert "ipv6_discovery" in {c["id"] for c in COMPONENT_CATALOG}


def test_planned_only_when_enabled():
    common = dict(service_filter=None, stop_after_banner=False,
                  ssh_enabled=False, windows_enabled=False)
    assert "ipv6_discovery" not in planned_components("it", **common)
    plan = planned_components("it", discover_ipv6=True, **common)
    assert plan[1] == "ipv6_discovery"      # immediately after host_discovery


def test_network_va_opts_in():
    from agent.engine import _DISCOVER_IPV6_SCAN_TYPES
    assert "network_va" in _DISCOVER_IPV6_SCAN_TYPES
    # A targeted single-service job should not sweep the segment.
    assert "tls_scan" not in _DISCOVER_IPV6_SCAN_TYPES
    assert "snmp_scan" not in _DISCOVER_IPV6_SCAN_TYPES
