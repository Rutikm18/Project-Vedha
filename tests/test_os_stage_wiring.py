"""
test_os_stage_wiring.py — the OS-identification stage in the agent workflow.

Before this stage existed, `os_fingerprint` never ran for a manager job: the only
OS signal reaching the manager was a side effect of the SYN scanner, which is only
chosen for wide sweeps. A standard-intensity network_va therefore produced NO OS
fact at all, leaving device classification and every OS-reading rule blind.

Covers: the gate, the stage's position in the plan, SYN/ACK stack hints flowing
from the port stage into the OS scanner, the conditional SMB2-build probe, cache
reuse, and the OS fact landing on the Asset.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from scanner.scanner_base import ScanResult, ScopeGuard
from workflow.asset import Asset, PortFact
from workflow.cache import WorkflowCache, classify_certainty
from workflow.execution import ExecutionTrace, planned_components
from workflow.gates import gate_4b_os_fingerprint
from workflow.modes import STAGE_HOST_DISCOVERY, STAGE_PORT_SCAN
from workflow.workflow_engine import run_engagement


def _asset(**kw) -> Asset:
    return Asset(host="10.0.0.1", **kw)


def _open(port: int) -> PortFact:
    return PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))


class TestGate:
    def test_alive_host_is_eligible(self):
        assert gate_4b_os_fingerprint(_asset(last_seen_alive=datetime.now(timezone.utc)), "it") is True

    def test_dead_host_is_not(self):
        assert gate_4b_os_fingerprint(_asset(), "it") is False

    def test_passive_profile_never_probes(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert gate_4b_os_fingerprint(a, "ot") is False

    def test_no_open_ports_still_eligible(self):
        # ICMP/TTL identification does not need an open TCP port.
        assert gate_4b_os_fingerprint(_asset(last_seen_alive=datetime.now(timezone.utc)), "iot") is True


class TestPlan:
    def test_os_stage_planned_from_the_port_stage_up(self):
        plan = planned_components("it", service_filter=None, stop_after_banner=False,
                                  ssh_enabled=False, windows_enabled=False,
                                  stage_ceiling=STAGE_PORT_SCAN)
        assert plan == ["host_discovery", "port_scan", "os_fingerprint"]

    def test_not_planned_for_liveness_only(self):
        plan = planned_components("it", service_filter=None, stop_after_banner=False,
                                  ssh_enabled=False, windows_enabled=False,
                                  stage_ceiling=STAGE_HOST_DISCOVERY)
        assert "os_fingerprint" not in plan

    def test_not_planned_for_a_udp_only_job(self):
        plan = planned_components("it", service_filter={"udp"}, stop_after_banner=False,
                                  ssh_enabled=False, windows_enabled=False)
        assert "os_fingerprint" not in plan

    def test_full_assessment_includes_it(self):
        plan = planned_components("it", service_filter=None, stop_after_banner=False,
                                  ssh_enabled=False, windows_enabled=False)
        assert plan.index("os_fingerprint") == plan.index("port_scan") + 1
        assert plan.index("os_fingerprint") < plan.index("service_banner")


class TestAssetMerge:
    def test_syn_stack_hints_harvested_from_open_port(self):
        a = _asset()
        a.merge_result(ScanResult(scanner="syn_scan", target="10.0.0.1", port=445,
                                  proto="tcp", status="open",
                                  data={"ip_ttl": 128, "tcp_window": 65535, "mss": 1460,
                                        "tcp_wscale": 8, "tcp_olayout": "MNWNNS"}))
        assert a.tcp_stack_hints == {"ttl": 128, "tcp_window": 65535, "mss": 1460,
                                     "wscale": 8, "olayout": "MNWNNS"}

    def test_connect_scan_without_stack_signals_leaves_hints_empty(self):
        a = _asset()
        a.merge_result(ScanResult(scanner="port_scan", target="10.0.0.1", port=80,
                                  proto="tcp", status="open", data={"reason": "connect_success"}))
        assert a.tcp_stack_hints == {}

    def test_closed_port_contributes_no_hints(self):
        a = _asset()
        a.merge_result(ScanResult(scanner="port_scan", target="10.0.0.1", port=81,
                                  proto="tcp", status="closed", data={"ip_ttl": 64}))
        assert a.tcp_stack_hints == {}

    def test_os_fact_stored_and_ntlm_name_becomes_alias(self):
        a = _asset()
        a.merge_result(ScanResult(scanner="os_fingerprint", target="10.0.0.1",
                                  status="open", data={"os_guess": "Windows",
                                                       "os_build": "26100",
                                                       "hostname": "DESKTOP-34M18MB"}))
        assert a.os_fact["os_build"] == "26100"
        assert "DESKTOP-34M18MB" in a.aliases

    def test_os_fact_is_cacheable_as_deterministic(self):
        r = ScanResult(scanner="os_fingerprint", target="10.0.0.1", status="open", data={})
        assert classify_certainty(r) == "deterministic"


# ── end-to-end through run_engagement ────────────────────────────────────────

def _wire(monkeypatch, captured, *, port_data, os_data=None):
    def fake(component_id, data, *, port=None, status="open"):
        class Scanner:
            name = component_id

            def __init__(self, *args, **kwargs):
                captured.setdefault(component_id, []).append(kwargs)

            async def scan_target(self, host):
                return [ScanResult(scanner=component_id, target=host, port=port,
                                   proto="tcp" if port else None, status=status,
                                   data=data)]
        return Scanner

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                        fake("host_discovery", {"alive": True}))
    monkeypatch.setattr("workflow.workflow_engine.PortScanner",
                        fake("port_scan", port_data, port=445))
    monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                        fake("os_fingerprint", os_data if os_data is not None
                             else {"os_guess": "Windows", "confidence": 0.5}))


def test_os_stage_runs_for_a_port_stage_job(monkeypatch):
    captured: dict = {}
    _wire(monkeypatch, captured, port_data={"reason": "connect_success"})
    trace = ExecutionTrace(planned_components(
        "it", service_filter=None, stop_after_banner=False, ssh_enabled=False,
        windows_enabled=False, stage_ceiling=STAGE_PORT_SCAN))

    assets = asyncio.run(run_engagement(
        ["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
        stage_ceiling=STAGE_PORT_SCAN, port_override=[445], trace=trace))

    assert assets["10.0.0.1"].os_fact["os_guess"] == "Windows"
    runs = {r["id"]: r for r in trace.as_list()}
    assert runs["os_fingerprint"]["status"] == "completed"
    assert runs["os_fingerprint"]["fact_count"] == 1
    # 445 was observed open, so the exact-build SMB2 probe is worth attempting.
    assert captured["os_fingerprint"][0]["smb_build"] is True


def test_stack_hints_from_syn_scan_reach_the_os_scanner(monkeypatch):
    captured: dict = {}
    _wire(monkeypatch, captured,
          port_data={"ip_ttl": 64, "tcp_window": 29200, "mss": 1460})
    monkeypatch.setattr("workflow.workflow_engine.SynScanner",
                        type("S", (), {"name": "syn_scan"}))

    asyncio.run(run_engagement(
        ["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
        stage_ceiling=STAGE_PORT_SCAN, port_override=[445]))

    assert captured["os_fingerprint"][0]["tcp_hints"] == {
        "10.0.0.1": {"ttl": 64, "tcp_window": 29200, "mss": 1460}}


def test_smb_build_probe_skipped_when_445_is_closed(monkeypatch):
    captured: dict = {}

    def fake(component_id, data, *, port=None, status="open"):
        class Scanner:
            name = component_id

            def __init__(self, *args, **kwargs):
                captured.setdefault(component_id, []).append(kwargs)

            async def scan_target(self, host):
                return [ScanResult(scanner=component_id, target=host, port=port,
                                   proto="tcp" if port else None, status=status, data=data)]
        return Scanner

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                        fake("host_discovery", {"alive": True}))
    monkeypatch.setattr("workflow.workflow_engine.PortScanner",
                        fake("port_scan", {}, port=80))
    monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                        fake("os_fingerprint", {"os_guess": "Linux"}))

    asyncio.run(run_engagement(["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
                               stage_ceiling=STAGE_PORT_SCAN, port_override=[80]))
    assert captured["os_fingerprint"][0]["smb_build"] is False


def test_dead_host_is_never_os_probed(monkeypatch):
    captured: dict = {}

    def fake(component_id, data, status="filtered"):
        class Scanner:
            name = component_id

            def __init__(self, *args, **kwargs):
                captured.setdefault(component_id, []).append(kwargs)

            async def scan_target(self, host):
                return [ScanResult(scanner=component_id, target=host, status=status, data=data)]
        return Scanner

    monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                        fake("host_discovery", {"alive": False}))
    monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                        fake("os_fingerprint", {"os_guess": "Windows"}))

    asyncio.run(run_engagement(["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
                               stage_ceiling=STAGE_PORT_SCAN))
    assert "os_fingerprint" not in captured


def test_cached_os_fact_is_reused_not_reprobed(monkeypatch):
    captured: dict = {}
    _wire(monkeypatch, captured, port_data={})
    cache = WorkflowCache()
    cache.put(ScanResult(scanner="os_fingerprint", target="10.0.0.1", status="open",
                         data={"os_guess": "Linux", "confidence": 0.5}))

    assets = asyncio.run(run_engagement(
        ["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
        stage_ceiling=STAGE_PORT_SCAN, port_override=[445], cache=cache))

    assert "os_fingerprint" not in captured          # served from cache
    assert assets["10.0.0.1"].os_fact["os_guess"] == "Linux"


def test_rescan_mode_reprobes_a_stale_os_fact(monkeypatch):
    captured: dict = {}
    _wire(monkeypatch, captured, port_data={})
    cache = WorkflowCache()
    old = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    cache.put(ScanResult(scanner="os_fingerprint", target="10.0.0.1", status="open",
                         timestamp=old, data={"os_guess": "Linux"}))

    assets = asyncio.run(run_engagement(
        ["10.0.0.1"], ScopeGuard.from_list(["10.0.0.0/24"]),
        stage_ceiling=STAGE_PORT_SCAN, port_override=[445], cache=cache,
        force_recheck_after=timedelta(hours=24)))

    assert "os_fingerprint" in captured
    assert assets["10.0.0.1"].os_fact["os_guess"] == "Windows"
