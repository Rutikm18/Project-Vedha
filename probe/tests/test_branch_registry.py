"""
test_branch_registry.py — the deep-scan branch registry and the invariants it
exists to enforce.

The engine used to spell out twenty near-identical branch blocks, and three
other places kept their own hand-maintained copy of "which branches exist":
gates.PROFILE_DEEP_BRANCHES, execution._BRANCH_COMPONENT, and
execution.COMPONENT_CATALOG. They drifted — the catalog was 13 branches behind
the engine, so a service-specific rdp/ssh/ldap job planned nothing and its
coverage report could not say what had been skipped. These tests pin every one
of those maps to the single registry so the drift cannot come back.
"""

from __future__ import annotations

import asyncio
import inspect
from datetime import datetime, timezone

import pytest

from scanner.scanner_base import ScanResult, ScopeGuard
import workflow.workflow_engine as we
from workflow.asset import Asset, PortFact
from workflow.asset import _MERGE_DISPATCH
from workflow.branches import BRANCH_BY_NAME, BRANCH_COMPONENT, BRANCHES
from workflow.cache import FACT_CERTAINTY
from workflow.execution import COMPONENT_CATALOG, planned_components
from workflow.gates import PROFILE_DEEP_BRANCHES, _BRANCH_PORT_TABLE


# ── the registry agrees with every map derived from or paired with it ────────

class TestRegistryConsistency:
    def test_every_branch_is_gateable(self):
        """A spec the profile tables don't know about could never run."""
        every_allowed = set().union(*PROFILE_DEEP_BRANCHES.values())
        assert {s.branch for s in BRANCHES} == every_allowed

    def test_port_tables_match_gates(self):
        """gate_5 intersects open ports with its own table; the engine uses the
        spec's. If they disagreed, a branch could pass the gate and then scan a
        different port set."""
        for spec in BRANCHES:
            if spec.host_level:
                continue
            assert set(spec.ports) == set(_BRANCH_PORT_TABLE[spec.branch]), spec.branch

    def test_every_branch_has_a_scanner_the_engine_can_resolve(self):
        for spec in BRANCHES:
            assert hasattr(we, spec.scanner), f"{spec.branch}: {spec.scanner} not imported"

    def test_every_component_is_in_the_plan_catalog(self):
        ids = {c["id"] for c in COMPONENT_CATALOG}
        for spec in BRANCHES:
            assert spec.component in ids, spec.component

    def test_catalog_entries_are_labelled(self):
        for c in COMPONENT_CATALOG:
            assert c["label"] and c["role"], c["id"]

    def test_branch_component_map_is_derived(self):
        assert BRANCH_COMPONENT == {s.branch: s.component for s in BRANCHES}

    def test_every_component_can_be_merged_into_an_asset(self):
        """A fact whose scanner name has no merge handler is collected, cached,
        shipped — and silently dropped from the Asset the gates reason about."""
        for spec in BRANCHES:
            assert spec.component in _MERGE_DISPATCH, spec.component

    def test_every_component_has_a_cache_certainty(self):
        """An unlisted scanner falls back to 'uncertain' (re-probed every pass).
        That is safe but wasteful, so the table must name each branch."""
        for spec in BRANCHES:
            assert spec.component in FACT_CERTAINTY, spec.component

    def test_components_are_unique(self):
        comps = [s.component for s in BRANCHES]
        assert len(comps) == len(set(comps))

    def test_kwargs_builders_have_the_expected_signature(self):
        for spec in BRANCHES:
            params = list(inspect.signature(spec.kwargs).parameters)
            assert params == ["asset", "to_scan"], spec.branch


# ── the drift this fixes: plan vs what the engine actually runs ──────────────

def _fake(cid, calls, port=None, data=None):
    class Scanner:
        name = cid

        def __init__(self, *a, **k):
            pass

        async def scan_target(self, host):
            calls.append(cid)
            return [ScanResult(scanner=cid, target=host, port=port,
                               proto="tcp" if port else None, status="open",
                               data=data if data is not None else {"alive": True})]
    return Scanner


@pytest.mark.parametrize("branch,scanner_attr,port", [
    ("rdp", "RDPScanner", 3389),
    ("ssh", "SSHScanner", 22),
    ("ldap", "LDAPScanner", 389),
    ("printer", "PrinterScanner", 9100),
    ("smtp", "SMTPScanner", 25),
])
def test_service_specific_plan_matches_what_the_engine_runs(monkeypatch, branch,
                                                            scanner_attr, port):
    """Before the registry, these five planned NOTHING while the engine ran five
    components — so the coverage roll-up had no way to report them."""
    calls: list[str] = []
    monkeypatch.setattr(we, "HostDiscoveryScanner", _fake("host_discovery", calls))
    monkeypatch.setattr(we, "PortScanner", _fake("port_scan", calls, port=port, data={}))
    monkeypatch.setattr(we, "ServiceBannerScanner",
                        _fake("service_banner", calls, port=port, data={}))
    monkeypatch.setattr(we, "OSFingerprintScanner",
                        _fake("os_fingerprint", calls, data={"os_guess": "Linux"}))
    monkeypatch.setattr(we, scanner_attr,
                        _fake(BRANCH_BY_NAME[branch].component, calls, port=port, data={}))

    asyncio.run(we.run_engagement(["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
                                  service_filter={branch}))
    plan = planned_components("it", service_filter={branch}, stop_after_banner=False,
                              ssh_enabled=False, windows_enabled=False)
    assert calls == plan


def test_full_assessment_plans_every_branch():
    plan = planned_components("it", service_filter=None, stop_after_banner=False,
                              ssh_enabled=False, windows_enabled=False)
    for spec in BRANCHES:
        assert spec.component in plan, spec.component
    # Branch order in the plan follows the registry order the engine runs.
    ordered = [s.component for s in BRANCHES]
    assert [c for c in plan if c in ordered] == ordered


def test_datagram_branches_need_no_tcp_stage():
    """An SNMP-only job must not fall back to a broad TCP sweep."""
    assert planned_components("it", service_filter={"snmp"}, stop_after_banner=False,
                              ssh_enabled=False, windows_enabled=False) == ["snmp_scan"]


# ── behaviour the table-driven runner must preserve ──────────────────────────

def _asset_with(port: int, **kw) -> Asset:
    return Asset(host="10.0.0.1", last_seen_alive=datetime.now(timezone.utc),
                 open_ports={port: PortFact(proto="tcp", status="open",
                                            last_scan_time=datetime.now(timezone.utc))},
                 **kw)


def test_host_level_branch_is_cached_under_a_null_port(monkeypatch):
    """smb's fact describes the host, so it must be keyed by (host, None) — not
    by whichever port happened to be open."""
    calls: list[str] = []
    monkeypatch.setattr(we, "HostDiscoveryScanner", _fake("host_discovery", calls))
    monkeypatch.setattr(we, "PortScanner", _fake("port_scan", calls, port=445, data={}))
    monkeypatch.setattr(we, "ServiceBannerScanner",
                        _fake("service_banner", calls, port=445, data={}))
    monkeypatch.setattr(we, "OSFingerprintScanner", _fake("os_fingerprint", calls, data={}))
    monkeypatch.setattr(we, "SMBScanner",
                        _fake("smb_scan", calls, data={"smbv1_enabled": True}))

    from workflow.cache import WorkflowCache
    cache = WorkflowCache()
    assets = asyncio.run(we.run_engagement(
        ["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
        service_filter={"smb"}, cache=cache))

    assert assets["10.0.0.1"].smb_state["smbv1_enabled"] is True
    assert cache.get("10.0.0.1", None, "smb_scan") is not None
    # A second engagement over the same cache reuses it instead of re-probing.
    before = calls.count("smb_scan")
    asyncio.run(we.run_engagement(["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
                                  service_filter={"smb"}, cache=cache))
    assert calls.count("smb_scan") == before


def test_db_branch_splits_known_and_router_discovered_ports():
    """The database branch is the one spec that runs its scanner twice: known
    engines by port, plus every probe on a port the router flagged by banner."""
    spec = BRANCH_BY_NAME["db"]
    asset = _asset_with(3306)
    runs = spec.kwargs(asset, [3306, 47000])
    assert len(runs) == 2
    assert runs[0]["port_map"] == {3306: "mysql"}
    assert runs[1] == {"port_map": {47000: ""}, "try_all_on_port": True}
    # Only known ports -> a single invocation.
    assert len(spec.kwargs(asset, [3306])) == 1


def test_web_branch_passes_observed_tls_ports():
    spec = BRANCH_BY_NAME["web"]
    asset = _asset_with(9000, services={9000: {"tls": True}, 8080: {}})
    assert spec.kwargs(asset, [9000, 8080]) == [
        {"ports": [9000, 8080], "tls_ports": {9000}}]


def test_snmp_scanner_is_constructed_without_a_ports_kwarg():
    """SNMPScanner's signature has no `ports`; passing one would TypeError."""
    assert BRANCH_BY_NAME["snmp"].kwargs(_asset_with(161), [161]) == [{}]
    assert BRANCH_BY_NAME["ipmi"].kwargs(_asset_with(623), [623]) == [{"ports": [623]}]
