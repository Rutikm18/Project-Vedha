"""
test_probe_next_features.py — the probe_next plan: run the improved main_scripts
scanners inside the probe, driven by manager use-cases + an intensity knob, with
richer facts riding the result payload.

Covers:
  * Phase C  — intensity presets (light/standard/deep) reach run_engagement and
               are recorded in applied_tuning; standard is a no-op baseline.
  * Phase B/D — new use-cases (device_inventory, full_port_audit, exposure_matrix)
               are advertised and wired, with device-role + vantage-exposure
               inference post-stages over the collected facts.
  * Phase E  — completeness/health + device/exposure rollups are surfaced at the
               top level of the result.
"""
from __future__ import annotations

import agent.engine as engine
from agent.use_cases import USE_CASES, resolve
from scanner.scanner_base import ScanResult
from workflow.cache import WorkflowCache
from workflow.intensity import (
    INTENSITY_PRESETS,
    intensity_port_override,
    resolve_intensity,
)


# ── Phase C: intensity presets ───────────────────────────────────────────────
def test_standard_intensity_is_a_noop_baseline():
    # standard must not override the profile catalog and its envelope must equal
    # the engine's historical defaults, so pre-intensity use-cases are unchanged.
    assert intensity_port_override("standard") is None
    p = resolve_intensity("standard")
    assert (p["rate"], p["concurrency"], p["timeout"]) == (200.0, 100, 3.0)


def test_light_and_deep_change_port_breadth():
    assert len(intensity_port_override("light")) == 15          # quick set
    assert len(intensity_port_override("deep")) == 65535         # whole TCP space


def test_none_intensity_defaults_to_standard():
    assert resolve_intensity(None) == INTENSITY_PRESETS["standard"]


def test_unknown_intensity_raises():
    import pytest
    with pytest.raises(ValueError, match="unknown intensity"):
        resolve_intensity("ludicrous")


def test_force_profile_overrides_intensity():
    # a full-port audit is the whole space no matter how light the intensity
    assert len(intensity_port_override("light", force_profile="full")) == 65535


# ── Phase B/D: new use-cases are advertised + wired ──────────────────────────
def test_new_use_cases_present_and_capable():
    for uc in ("uc_device_inventory", "uc_full_port_audit", "uc_exposure_matrix"):
        assert uc in USE_CASES
        scan_type = USE_CASES[uc]["scan_type"]
        assert scan_type in engine.CAPABILITIES


def test_full_port_audit_records_full_coverage_in_applied_tuning():
    # 10.0.0.1 is unreachable in CI, so no packets land — but the RESOLVED config
    # (deep intensity → whole TCP space) is recorded regardless.
    result = engine.run_scan("full_port_audit", {"targets": ["10.0.0.1"]})
    assert result["ok"] is True
    applied = result["run_stats"]["applied_tuning"]
    assert applied["intensity"] == "deep"
    assert applied["tcp_ports_scanned"] == 65535
    assert applied["retries"] == 2
    assert "scan_metrics" in result  # surfaced even when empty


def test_discovery_defaults_to_standard_intensity_no_override():
    result = engine.run_scan("discovery", {"targets": ["10.0.0.1"]})
    applied = result["run_stats"]["applied_tuning"]
    assert applied["intensity"] == "standard"
    assert applied["tcp_ports_scanned"] is None


def test_params_intensity_overrides_and_is_applied():
    result = engine.run_scan(
        "discovery", {"targets": ["10.0.0.1"], "intensity": "light"}
    )
    applied = result["run_stats"]["applied_tuning"]
    assert applied["intensity"] == "light"
    assert applied["tcp_ports_scanned"] == 15


def test_unsupported_intensity_is_rejected_before_scanning():
    result = engine.run_scan(
        "discovery", {"targets": ["10.0.0.1"], "intensity": "nope"}
    )
    assert result["ok"] is False
    assert result["error_code"] == "unsupported_intensity"
    assert result["facts"] == []


# ── Phase D: device-role inference post-stage ────────────────────────────────
def _cache_with(results: list[ScanResult]) -> WorkflowCache:
    cache = WorkflowCache()
    for r in results:
        cache.put(r)
    return cache


def test_device_inventory_post_stage_classifies_from_open_ports():
    # 88 (kerberos) + 389 (ldap) + 445 (smb) → a Domain Controller (server).
    cache = _cache_with([
        ScanResult(scanner="port_scan", target="10.0.0.5", port=88, proto="tcp", status="open"),
        ScanResult(scanner="port_scan", target="10.0.0.5", port=389, proto="tcp", status="open"),
        ScanResult(scanner="port_scan", target="10.0.0.5", port=445, proto="tcp", status="open"),
    ])
    extra, rollup = engine._derive_post_stage("device_inventory", cache)
    assert [r.scanner for r in extra] == ["device_classify"]
    assert extra[0].data["device_type"] == "server"
    assert extra[0].data["role_detail"] == "domain_controller"
    assert rollup["devices"][0]["ip"] == "10.0.0.5"


def test_device_inventory_skips_hosts_without_evidence():
    # Only a closed port → no role should be manufactured.
    cache = _cache_with([
        ScanResult(scanner="port_scan", target="10.0.0.9", port=80, proto="tcp", status="closed"),
    ])
    extra, rollup = engine._derive_post_stage("device_inventory", cache)
    assert extra == []
    assert rollup["devices"] == []


# ── Phase D: vantage-exposure inference post-stage ───────────────────────────
def test_exposure_matrix_flags_internet_reachable_ports():
    # An OPEN port seen from an external-named vantage is externally exposed.
    cache = _cache_with([
        ScanResult(scanner="port_scan", target="203.0.113.5", port=443, proto="tcp",
                   status="open", vantage="internet-edge"),
        ScanResult(scanner="port_scan", target="203.0.113.5", port=445, proto="tcp",
                   status="open", vantage="internet-edge"),
    ])
    extra, rollup = engine._derive_post_stage("exposure_matrix", cache)
    assert [r.scanner for r in extra] == ["exposure_matrix"]
    matrix = extra[0].data
    assert 443 in matrix["externally_exposed"]
    assert rollup["exposure"][0]["ip"] == "203.0.113.5"


def test_exposure_matrix_internal_only_from_lan_vantage():
    cache = _cache_with([
        ScanResult(scanner="port_scan", target="10.0.0.7", port=445, proto="tcp",
                   status="open", vantage="lan-probe"),
    ])
    extra, _rollup = engine._derive_post_stage("exposure_matrix", cache)
    matrix = extra[0].data
    assert matrix["externally_exposed"] == []
    assert 445 in matrix["internal_only"]


def test_no_post_stage_for_ordinary_scan_types():
    cache = _cache_with([
        ScanResult(scanner="port_scan", target="10.0.0.5", port=443, proto="tcp", status="open"),
    ])
    assert engine._derive_post_stage("assessment", cache) == ([], {})


# ── Phase F: invariants preserved for the new use-cases ──────────────────────
def test_new_scan_types_still_enforce_scope():
    # ScopeGuard is the same single entry point for every scan_type — a target
    # outside the authorized scope is refused before any packet, new UC or not.
    for scan_type in ("device_inventory", "full_port_audit", "exposure_matrix"):
        result = engine.run_scan(
            scan_type,
            {"targets": ["8.8.8.8"]},
            validated_scope=["10.0.0.0/8"],
        )
        assert result["ok"] is False, scan_type
        assert result["error_code"] == "no_authorized_targets", scan_type
        assert result["facts"] == [], scan_type


def test_new_use_cases_are_rejected_if_not_in_library():
    # The allowlist is unchanged: an unknown use_case_id never resolves.
    import pytest
    with pytest.raises(ValueError, match="Unknown use_case_id"):
        resolve("uc_device_inventory_typo", None, {})


# ── Track C1: wide sweeps route through the SYN scanner ───────────────────────
def test_scan_method_selection_rule():
    from workflow.intensity import intensity_port_override
    # Narrow catalogs stay on connect; a full/deep sweep switches to SYN.
    assert engine._scan_method_for(None) == "connect"                       # profile catalog
    assert engine._scan_method_for(intensity_port_override("light")) == "connect"   # 15 ports
    assert engine._scan_method_for(intensity_port_override("deep")) == "syn"         # 65535 ports
    assert engine._scan_method_for(list(range(1, 66))) == "connect"         # 65 ports, under threshold


def test_full_port_audit_advertises_syn_method():
    # No packets land (10.0.0.1 unreachable), but the RESOLVED method is recorded.
    result = engine.run_scan("full_port_audit", {"targets": ["10.0.0.1"]})
    assert result["run_stats"]["applied_tuning"]["scan_method"] == "syn"


def test_syn_scan_method_routes_through_syn_scanner():
    # run_engagement with scan_method="syn" must produce syn_scan facts; off
    # privileged Linux the SynScanner transparently reports connect_fallback,
    # so the OPEN port is still found and the method is stamped for auditability.
    import asyncio
    import socket
    import threading
    from scanner.scanner_base import ScopeGuard
    from workflow.cache import WorkflowCache
    from workflow.workflow_engine import run_engagement

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 0)); srv.listen(8)
    open_port = srv.getsockname()[1]
    threading.Thread(
        target=lambda: [c.close() for c in iter(lambda: srv.accept()[0], None)],
        daemon=True,
    ).start()
    cache = WorkflowCache()
    try:
        scope = ScopeGuard.from_list(["127.0.0.1/32"])
        asyncio.run(run_engagement(
            ["127.0.0.1"], scope, profile="it",
            port_override=[open_port], scan_method="syn",
            stage_ceiling="port_scan", cache=cache,
        ))
    finally:
        srv.close()

    results = [e.result for e in cache._store.values()]
    port_results = [r for r in results if r.scanner == "syn_scan" and r.port == open_port]
    assert port_results, "expected a syn_scan result for the open port"
    assert port_results[0].status == "open"
    # off privileged Linux the method is the transparent connect fallback
    assert port_results[0].data.get("method") in ("syn", "connect_fallback")

