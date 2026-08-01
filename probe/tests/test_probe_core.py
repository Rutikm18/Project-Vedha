"""
Probe test suite — unit tests for the probe's pure-logic modules.
Covers: ScopeGuard, expand_targets, parse_ports, ScanResult, gates,
router, modes, Asset merge, WorkflowCache, classify_certainty,
agent/engine, agent/use_cases.
"""
from __future__ import annotations

import asyncio
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from scanner.scanner_base import (
    ScopeGuard, ScopeError, expand_targets, parse_ports, ScanResult,
    RateLimiter, ResultWriter,
)
from workflow.gates import (
    gate_0_is_passive_profile, gate_2_host_discovery, gate_3_port_scan,
    gate_4_service_banner, gate_5_branch_eligible, gate_6_credentialed_collection,
    LIVENESS_RECHECK_THRESHOLD,
)
from workflow.router import looks_like_http, looks_like_tls, route_branches
from workflow.modes import (
    EngagementMode, triage, assessment, service_specific, re_scan,
    VALID_SERVICES,
)
from workflow.asset import Asset, PortFact
from workflow.cache import WorkflowCache, CacheEntry, classify_certainty, FACT_CERTAINTY
from agent.engine import (
    resolve_scan_type, _clamp, _targets, _tuning_from_params,
    _count_open_port_facts, _hosts_from_facts, CAPABILITIES,
)
from agent.use_cases import resolve, USE_CASES


def _scan_result(scanner="port_scan", target="10.0.0.1", port=22,
                 proto="tcp", status="open", data=None, error=None,
                 timestamp=None, evidence=None):
    return ScanResult(
        scanner=scanner, target=target, port=port, proto=proto,
        status=status, data=data or {}, error=error, evidence=evidence,
        timestamp=timestamp or datetime.now(timezone.utc).isoformat(),
    )


def _asset(host="10.0.0.1", **kw):
    return Asset(host=host, **kw)


# ═══════════════════════════════════════════════════════════════════════════
# scanner_base.py — ScopeGuard
# ═══════════════════════════════════════════════════════════════════════════

class TestScopeGuard:
    def test_from_list_ip_in_cidr(self):
        sg = ScopeGuard.from_list(["10.0.0.0/24"])
        assert sg.in_scope("10.0.0.1") is True
        assert sg.in_scope("10.0.1.1") is False

    def test_from_list_single_ip(self):
        sg = ScopeGuard.from_list(["192.168.1.50"])
        assert sg.in_scope("192.168.1.50") is True
        assert sg.in_scope("192.168.1.51") is False

    def test_from_list_hostname(self):
        sg = ScopeGuard.from_list(["scanme.example.com"])
        assert sg.in_scope("scanme.example.com") is True
        assert sg.in_scope("other.example.com") is False

    def test_hostname_case_insensitive(self):
        sg = ScopeGuard.from_list(["ScanMe.Example.COM"])
        assert sg.in_scope("scanme.example.com") is True

    def test_excludes_override_allowlist(self):
        sg = ScopeGuard.from_list(["10.0.0.0/24"], excludes=["10.0.0.5/32"])
        assert sg.in_scope("10.0.0.5") is False
        assert sg.in_scope("10.0.0.1") is True

    def test_excludes_larger_subnet(self):
        sg = ScopeGuard.from_list(["10.0.0.0/16"], excludes=["10.0.1.0/24"])
        assert sg.in_scope("10.0.1.5") is False
        assert sg.in_scope("10.0.2.5") is True

    def test_assert_in_scope_raises(self):
        sg = ScopeGuard.from_list(["10.0.0.0/24"])
        with pytest.raises(ScopeError, match="NOT in authorized scope"):
            sg.assert_in_scope("192.168.1.1")

    def test_assert_in_scope_passes(self):
        sg = ScopeGuard.from_list(["10.0.0.0/24"])
        sg.assert_in_scope("10.0.0.1")

    def test_filter_yields_only_in_scope(self):
        sg = ScopeGuard.from_list(["10.0.0.0/24"])
        result = list(sg.filter(["10.0.0.1", "192.168.1.1", "10.0.0.2"]))
        assert result == ["10.0.0.1", "10.0.0.2"]

    def test_from_file(self, tmp_path):
        p = tmp_path / "scope.txt"
        p.write_text("10.0.0.0/24\nscanme.example.com\n# comment\n")
        sg = ScopeGuard.from_file(p)
        assert sg.in_scope("10.0.0.1") is True
        assert sg.in_scope("scanme.example.com") is True

    def test_from_file_empty_raises(self, tmp_path):
        p = tmp_path / "empty.txt"
        p.write_text("# just a comment\n")
        with pytest.raises(ScopeError, match="no valid entries"):
            ScopeGuard.from_file(p)

    def test_from_file_missing_raises(self):
        with pytest.raises(ScopeError, match="cannot read"):
            ScopeGuard.from_file("/nonexistent/path.txt")


# ═══════════════════════════════════════════════════════════════════════════
# scanner_base.py — expand_targets
# ═══════════════════════════════════════════════════════════════════════════

class TestExpandTargets:
    def test_single_ip(self):
        assert expand_targets(["10.0.0.1"]) == ["10.0.0.1"]

    def test_cidr_24(self):
        result = expand_targets(["10.0.0.0/24"])
        assert len(result) == 254
        assert "10.0.0.1" in result
        assert "10.0.0.254" in result

    def test_hostname_passthrough(self):
        assert expand_targets(["web01.example.com"]) == ["web01.example.com"]

    def test_range(self):
        result = expand_targets(["10.0.0.1-10.0.0.3"])
        assert result == ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

    def test_range_reversed_raises(self):
        with pytest.raises(ValueError, match="end address before start"):
            expand_targets(["10.0.0.3-10.0.0.1"])

    def test_dedup(self):
        result = expand_targets(["10.0.0.1", "10.0.0.1"])
        assert result == ["10.0.0.1"]

    def test_safety_cap_cidr(self):
        with pytest.raises(ValueError, match="safety cap"):
            expand_targets(["10.0.0.0/8"], max_hosts=100)

    def test_safety_cap_range(self):
        with pytest.raises(ValueError, match="safety cap"):
            expand_targets(["10.0.0.1-10.0.1.0"], max_hosts=100)

    def test_empty_input(self):
        assert expand_targets([]) == []

    def test_whitespace_entries(self):
        assert expand_targets(["  10.0.0.1  "]) == ["10.0.0.1"]


# ═══════════════════════════════════════════════════════════════════════════
# scanner_base.py — parse_ports
# ═══════════════════════════════════════════════════════════════════════════

class TestParsePorts:
    def test_single_port(self):
        assert parse_ports("22") == [22]

    def test_comma_separated(self):
        assert parse_ports("22,80,443") == [22, 80, 443]

    def test_range(self):
        assert parse_ports("8000-8003") == [8000, 8001, 8002, 8003]

    def test_mixed(self):
        assert parse_ports("22,80,8000-8002") == [22, 80, 8000, 8001, 8002]

    def test_duplicates_removed(self):
        assert parse_ports("22,22,80") == [22, 80]

    def test_sorted(self):
        assert parse_ports("443,22,80") == [22, 80, 443]

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError, match="out of range"):
            parse_ports("0")
        with pytest.raises(ValueError, match="out of range"):
            parse_ports("70000")

    def test_bad_token_raises(self):
        with pytest.raises(ValueError, match="invalid port token"):
            parse_ports("abc")

    def test_reversed_range_raises(self):
        with pytest.raises(ValueError, match="end before start"):
            parse_ports("100-50")


# ═══════════════════════════════════════════════════════════════════════════
# scanner_base.py — ScanResult
# ═══════════════════════════════════════════════════════════════════════════

class TestScanResult:
    def test_to_json_roundtrip(self):
        r = _scan_result(scanner="port_scan", port=443)
        d = json.loads(r.to_json())
        assert d["scanner"] == "port_scan"
        assert d["port"] == 443

    def test_default_timestamp_present(self):
        r = ScanResult(scanner="s", target="t")
        assert r.timestamp is not None

    def test_default_status_observed(self):
        r = ScanResult(scanner="s", target="t")
        assert r.status == "observed"


# ═══════════════════════════════════════════════════════════════════════════
# scanner_base.py — RateLimiter
# ═══════════════════════════════════════════════════════════════════════════

class TestRateLimiter:
    def test_min_interval(self):
        rl = RateLimiter(rate=100)
        assert rl.min_interval == pytest.approx(0.01)

    def test_zero_rate(self):
        rl = RateLimiter(rate=0)
        assert rl.min_interval == 0.0

    def test_wait_returns_immediately_at_zero_rate(self):
        rl = RateLimiter(rate=0)
        asyncio.run(rl.wait())


# ═══════════════════════════════════════════════════════════════════════════
# gates.py
# ═══════════════════════════════════════════════════════════════════════════

class TestGate0:
    def test_ot_is_passive(self):
        assert gate_0_is_passive_profile("ot") is True

    def test_it_not_passive(self):
        assert gate_0_is_passive_profile("it") is False

    def test_iot_not_passive(self):
        assert gate_0_is_passive_profile("iot") is False


class TestGate2:
    def test_never_seen_alive(self):
        a = _asset(last_seen_alive=None)
        assert gate_2_host_discovery(a, "it") is True

    def test_recently_seen_alive(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert gate_2_host_discovery(a, "it") is False

    def test_stale_seen_alive(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc) - timedelta(hours=2))
        assert gate_2_host_discovery(a, "it") is True

    def test_ot_always_false(self):
        a = _asset(last_seen_alive=None)
        assert gate_2_host_discovery(a, "ot") is False


class TestGate3:
    def test_requires_alive(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert gate_3_port_scan(a, "it") is True

    def test_not_alive(self):
        a = _asset(last_seen_alive=None)
        assert gate_3_port_scan(a, "it") is False

    def test_ot_always_false(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert gate_3_port_scan(a, "ot") is False


class TestGate4:
    def test_with_open_ports(self):
        a = _asset(open_ports={22: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_4_service_banner(a) is True

    def test_no_open_ports(self):
        a = _asset()
        assert gate_4_service_banner(a) is False

    def test_all_closed(self):
        a = _asset(open_ports={22: PortFact(proto="tcp", status="closed", last_scan_time=datetime.now(timezone.utc))})
        assert gate_4_service_banner(a) is False


class TestGate5:
    def test_it_profile_tls_with_tls_port(self):
        a = _asset(open_ports={443: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_5_branch_eligible("tls", a, "it", None) is True

    def test_iot_profile_no_smb(self):
        a = _asset(open_ports={445: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_5_branch_eligible("smb", a, "iot", None) is False

    def test_ot_no_branches(self):
        a = _asset(open_ports={443: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_5_branch_eligible("tls", a, "ot", None) is False

    def test_service_filter_blocks(self):
        a = _asset(open_ports={443: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_5_branch_eligible("tls", a, "it", {"web"}) is False

    def test_service_filter_allows(self):
        a = _asset(open_ports={443: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_5_branch_eligible("tls", a, "it", {"tls"}) is True

    def test_dynamically_routed_overrides_port(self):
        a = _asset()
        assert gate_5_branch_eligible("tls", a, "it", None, dynamically_routed=True) is True

    def test_no_matching_ports(self):
        a = _asset(open_ports={22: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_5_branch_eligible("tls", a, "it", None) is False

    def test_mcp_ai_allowed_on_it_ai_port(self):
        a = _asset(open_ports={11434: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        assert gate_5_branch_eligible("mcp_ai", a, "it", None) is True

    def test_snmp_allowed_on_live_it_host(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert gate_5_branch_eligible("snmp", a, "it", None) is True

    def test_explicit_snmp_does_not_require_tcp_liveness(self):
        a = _asset(last_seen_alive=None)
        assert gate_5_branch_eligible("snmp", a, "it", {"snmp"}) is True

    def test_snmp_not_allowed_on_iot_profile(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert gate_5_branch_eligible("snmp", a, "iot", None) is False


class TestGate6:
    def test_no_creds(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert gate_6_credentialed_collection(a, False, False) is False

    def test_ssh_creds_alive_uncollected(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc), cred_collected=False)
        assert gate_6_credentialed_collection(a, True, False) is True

    def test_already_collected(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc), cred_collected=True)
        assert gate_6_credentialed_collection(a, True, False) is False

    def test_not_alive(self):
        a = _asset(last_seen_alive=None, cred_collected=False)
        assert gate_6_credentialed_collection(a, True, False) is False


# ═══════════════════════════════════════════════════════════════════════════
# router.py
# ═══════════════════════════════════════════════════════════════════════════

class TestLooksLikeHttp:
    def test_http_1_1(self):
        assert looks_like_http({"first_line": "HTTP/1.1 200 OK"}) is True

    def test_http_2(self):
        assert looks_like_http({"first_line": "HTTP/2 200"}) is True

    def test_not_http(self):
        assert looks_like_http({"first_line": "SSH-2.0-OpenSSH_8.9"}) is False

    def test_empty(self):
        assert looks_like_http({}) is False
        assert looks_like_http(None) is False


class TestLooksLikeTls:
    def test_silent_non_client_first_port(self):
        assert looks_like_tls(9443, {"banner": None}) is True

    def test_client_first_port_not_tls(self):
        assert looks_like_tls(443, {"banner": None}) is False

    def test_no_banner_attempt(self):
        assert looks_like_tls(9443, None) is False

    def test_banner_present(self):
        assert looks_like_tls(9443, {"banner": "SSH-2.0"}) is False


class TestRouteBranches:
    def test_http_banner_routes_web(self):
        a = _asset(open_ports={80: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))},
                    services={80: {"first_line": "HTTP/1.1 200 OK"}})
        routed = route_branches(a)
        assert 80 in routed
        assert "web" in routed[80]

    def test_silent_nonstandard_port_routes_tls(self):
        a = _asset(open_ports={9443: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))},
                    services={9443: {"banner": None}})
        routed = route_branches(a)
        assert 9443 in routed
        assert "tls" in routed[9443]

    def test_no_banners_no_routing(self):
        a = _asset(open_ports={22: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc))})
        routed = route_branches(a)
        assert routed == {}


# ═══════════════════════════════════════════════════════════════════════════
# modes.py
# ═══════════════════════════════════════════════════════════════════════════

class TestEngagementModes:
    def test_triage(self):
        m = triage()
        assert m.name == "triage"
        assert m.stop_after_banner is True
        assert m.service_filter is None

    def test_assessment(self):
        m = assessment()
        assert m.name == "assessment"
        assert m.stop_after_banner is False

    def test_service_specific_valid(self):
        m = service_specific({"tls", "web"})
        assert m.service_filter == {"tls", "web"}

    def test_service_specific_invalid_raises(self):
        with pytest.raises(ValueError, match="unknown service"):
            service_specific({"tls", "ftp"})

    def test_re_scan(self):
        td = timedelta(hours=24)
        m = re_scan(td)
        assert m.force_recheck_after == td
        assert m.requires_prior_engagement is True


# ═══════════════════════════════════════════════════════════════════════════
# asset.py — Asset + merge_result
# ═══════════════════════════════════════════════════════════════════════════

class TestAssetNeedsRecheckLive:
    def test_never_seen(self):
        a = _asset(last_seen_alive=None)
        assert a.needs_recheck_live(timedelta(hours=1)) is True

    def test_recently_seen(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc))
        assert a.needs_recheck_live(timedelta(hours=1)) is False

    def test_stale(self):
        a = _asset(last_seen_alive=datetime.now(timezone.utc) - timedelta(hours=2))
        assert a.needs_recheck_live(timedelta(hours=1)) is True


class TestAssetOpenPortsForDeepScan:
    def test_only_open(self):
        a = _asset(open_ports={
            22: PortFact(proto="tcp", status="open", last_scan_time=datetime.now(timezone.utc)),
            80: PortFact(proto="tcp", status="closed", last_scan_time=datetime.now(timezone.utc)),
        })
        assert a.open_ports_for_deep_scan() == {22}

    def test_empty(self):
        a = _asset()
        assert a.open_ports_for_deep_scan() == set()


class TestAssetMergeHostDiscovery:
    def test_alive_sets_timestamp(self):
        a = _asset()
        ts = "2026-01-15T10:30:00+00:00"
        a.merge_result(_scan_result(scanner="host_discovery", data={"alive": True},
                                    timestamp=ts))
        assert a.last_seen_alive is not None

    def test_responding_ports(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="host_discovery",
                                    data={"alive": True, "responding_ports": [
                                        {"port": 80, "state": "open"},
                                        {"port": 443, "state": "open"},
                                    ]}))
        assert 80 in a.open_ports
        assert a.open_ports[80].status == "open"


class TestAssetMergePortScan:
    def test_tcp_open(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="port_scan", port=22, status="open"))
        assert a.open_ports[22].status == "open"
        assert a.open_ports[22].certainty == "deterministic"

    def test_udp_uncertain(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="port_scan", port=53, proto="udp", status="open"))
        assert a.open_ports[53].certainty == "uncertain"


class TestAssetMergeServiceBanner:
    def test_banner_stored(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="service_banner", port=22,
                                    data={"first_line": "SSH-2.0-OpenSSH_8.9p1"}))
        assert 22 in a.services
        assert a.services[22]["first_line"] == "SSH-2.0-OpenSSH_8.9p1"


class TestAssetMergeTlsScan:
    def test_tls_facts_stored(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="tls_scan", port=443,
                                    data={"version": "TLSv1.3"}))
        assert 443 in a.tls_facts


class TestAssetMergeWebScan:
    def test_web_facts_stored(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="web_scan", port=80,
                                    data={"server": "nginx/1.25.3"}))
        assert 80 in a.web_facts


class TestAssetMergeSmbScan:
    def test_smb_state_host_level(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="smb_scan", port=445,
                                    data={"smbv1_enabled": True}))
        assert a.smb_state is not None
        assert a.smb_state["smbv1_enabled"] is True


class TestAssetMergeCredentialed:
    def test_ssh_inventory(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="ssh_inventory", data={"hostname": "web01"}))
        assert a.credential_inventory is not None
        assert a.cred_collected is True
        assert a.credential_inventory["_via"] == "ssh"

    def test_windows_inventory(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="windows_inventory", data={"hostname": "win01"}))
        assert a.cred_collected is True
        assert a.credential_inventory["_via"] == "windows"


class TestAssetMergePassiveCollect:
    def test_passive_facts_appended(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="passive_collect",
                                    data={"source": "mdns", "device_hints": ["printer.local"]}))
        assert len(a.passive_facts) == 1
        assert "printer.local" in a.aliases


class TestAssetMergeUnknownScanner:
    def test_unknown_scanner_ignored(self):
        a = _asset()
        a.merge_result(_scan_result(scanner="unknown_scanner"))
        assert len(a.passive_facts) == 0
        assert not a.open_ports


# ═══════════════════════════════════════════════════════════════════════════
# agent/engine.py — result summary accuracy
# ═══════════════════════════════════════════════════════════════════════════

class TestEngineSummary:
    def test_open_port_count_excludes_host_liveness(self):
        facts = [
            {"scanner": "host_discovery", "target": "127.0.0.1", "status": "open"},
            {"scanner": "port_scan", "target": "127.0.0.1", "port": 22, "status": "closed"},
            {"scanner": "port_scan", "target": "127.0.0.1", "port": 443, "status": "open"},
        ]
        assert _count_open_port_facts(facts) == 1

    def test_open_port_count_deduplicates_confirming_scanners(self):
        facts = [
            {
                "scanner": "port_scan",
                "target": "127.0.0.1",
                "port": 443,
                "proto": "tcp",
                "status": "open",
            },
            {
                "scanner": "service_banner",
                "target": "127.0.0.1",
                "port": 443,
                "proto": "tcp",
                "status": "open",
            },
            {
                "scanner": "tls_scan",
                "target": "127.0.0.1",
                "port": 443,
                "proto": "tcp",
                "status": "open",
            },
            {
                "scanner": "udp_scan",
                "target": "127.0.0.1",
                "port": 443,
                "proto": "udp",
                "status": "open",
            },
        ]
        assert _count_open_port_facts(facts) == 2

    def test_negative_or_ambiguous_facts_do_not_create_hosts(self):
        facts = [
            {
                "scanner": "host_discovery",
                "target": "10.0.0.10",
                "status": "filtered",
                "data": {"alive": False},
            },
            {
                "scanner": "port_scan",
                "target": "10.0.0.11",
                "port": 443,
                "proto": "tcp",
                "status": "closed",
            },
            {
                "scanner": "udp_scan",
                "target": "10.0.0.12",
                "port": 53,
                "proto": "udp",
                "status": "filtered",
                "data": {"responded": False},
            },
        ]
        assert _hosts_from_facts(facts) == []

    def test_affirmative_fact_creates_one_deduplicated_host(self):
        facts = [
            {
                "scanner": "port_scan",
                "target": "10.0.0.10",
                "port": 443,
                "proto": "tcp",
                "status": "open",
                "data": {},
            },
            {
                "scanner": "tls_scan",
                "target": "10.0.0.10",
                "port": 443,
                "proto": "tcp",
                "status": "open",
                "data": {"service": "https"},
            },
        ]
        assert _hosts_from_facts(facts) == [{
            "ip": "10.0.0.10",
            "hostname": None,
            "ports": [{
                "port": 443,
                "protocol": "tcp",
                "service": "https",
            }],
        }]


# ═══════════════════════════════════════════════════════════════════════════
# cache.py — classify_certainty + WorkflowCache
# ═══════════════════════════════════════════════════════════════════════════

class TestClassifyCertainty:
    def test_tcp_port_scan_deterministic(self):
        r = _scan_result(scanner="port_scan", proto="tcp")
        assert classify_certainty(r) == "deterministic"

    def test_udp_port_scan_uncertain(self):
        r = _scan_result(scanner="port_scan", proto="udp")
        assert classify_certainty(r) == "uncertain"

    def test_service_banner_deterministic(self):
        r = _scan_result(scanner="service_banner")
        assert classify_certainty(r) == "deterministic"

    def test_host_discovery_uncertain(self):
        r = _scan_result(scanner="host_discovery")
        assert classify_certainty(r) == "uncertain"

    def test_error_overrides(self):
        r = _scan_result(scanner="service_banner", status="error", error="timeout")
        assert classify_certainty(r) == "uncertain"

    def test_unknown_scanner_conservative(self):
        r = _scan_result(scanner="something_new")
        assert classify_certainty(r) == "uncertain"


class TestCacheEntry:
    def test_roundtrip(self):
        r = _scan_result(scanner="tls_scan", port=443)
        entry = CacheEntry(host="10.0.0.1", port=443, proto="tcp",
                           scanner="tls_scan", result=r,
                           collected_at=r.timestamp, fact_certainty="deterministic")
        d = entry.to_jsonl_dict()
        entry2 = CacheEntry.from_jsonl_dict(d)
        assert entry2.host == "10.0.0.1"
        assert entry2.scanner == "tls_scan"
        assert entry2.result.port == 443


class TestWorkflowCache:
    def test_put_get(self):
        c = WorkflowCache()
        r = _scan_result(scanner="port_scan", port=22)
        c.put(r)
        entry = c.get("10.0.0.1", 22, "port_scan")
        assert entry is not None
        assert entry.result.port == 22

    def test_get_missing(self):
        c = WorkflowCache()
        assert c.get("10.0.0.1", 22, "port_scan") is None

    def test_should_recheck_missing(self):
        c = WorkflowCache()
        assert c.should_recheck("10.0.0.1", 22, "port_scan") is True

    def test_should_recheck_uncertain_always(self):
        c = WorkflowCache()
        r = _scan_result(scanner="host_discovery")
        c.put(r)
        assert c.should_recheck("10.0.0.1", None, "host_discovery") is True

    def test_should_recheck_deterministic_fresh(self):
        c = WorkflowCache()
        r = _scan_result(scanner="service_banner", port=22)
        c.put(r)
        assert c.should_recheck("10.0.0.1", 22, "service_banner") is False

    def test_should_recheck_force_expired(self):
        c = WorkflowCache()
        old_ts = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
        r = _scan_result(scanner="service_banner", port=22, timestamp=old_ts)
        c.put(r)
        assert c.should_recheck("10.0.0.1", 22, "service_banner",
                                force_recheck_after=timedelta(hours=24)) is True

    def test_all_entries_for_host(self):
        c = WorkflowCache()
        c.put(_scan_result(scanner="port_scan", port=22, target="10.0.0.1"))
        c.put(_scan_result(scanner="port_scan", port=80, target="10.0.0.1"))
        c.put(_scan_result(scanner="port_scan", port=22, target="10.0.0.2"))
        assert len(c.all_entries_for_host("10.0.0.1")) == 2
        assert len(c.all_entries_for_host("10.0.0.2")) == 1

    def test_save_and_load_roundtrip(self, tmp_path):
        c = WorkflowCache(path=tmp_path / "cache.jsonl")
        c.put(_scan_result(scanner="port_scan", port=22))
        c.put(_scan_result(scanner="tls_scan", port=443))
        c.save()

        c2 = WorkflowCache(path=tmp_path / "cache.jsonl")
        assert c2.get("10.0.0.1", 22, "port_scan") is not None
        assert c2.get("10.0.0.1", 443, "tls_scan") is not None

    def test_save_raises_without_path(self):
        c = WorkflowCache()
        with pytest.raises(ValueError, match="no path configured"):
            c.save()

    def test_load_handles_corrupt_lines(self, tmp_path):
        p = tmp_path / "corrupt.jsonl"
        p.write_text('{"host":"10.0.0.1","port":22,"proto":"tcp","scanner":"port_scan","collected_at":"t","fact_certainty":"deterministic","result":{"scanner":"port_scan","target":"10.0.0.1","timestamp":"t","port":22,"proto":"tcp","status":"open","data":{}}}\nnot-json\n')
        c = WorkflowCache(path=p)
        assert c.get("10.0.0.1", 22, "port_scan") is not None


# ═══════════════════════════════════════════════════════════════════════════
# agent/engine.py — pure functions
# ═══════════════════════════════════════════════════════════════════════════

class TestResolveScanType:
    def test_from_params(self):
        assert resolve_scan_type(None, {"scan_type": "tls_scan"}) == "tls_scan"

    def test_from_job_type(self):
        assert resolve_scan_type("assessment", {}) == "assessment"

    def test_default(self):
        assert resolve_scan_type(None, {}) == "discovery"

    def test_params_override_job_type(self):
        assert resolve_scan_type("port_scan", {"scan_type": "tls_scan"}) == "tls_scan"


class TestClamp:
    def test_in_range(self):
        assert _clamp(50, 1, 100, 10) == 50.0

    def test_clamped_high(self):
        assert _clamp(200, 1, 100, 10) == 100.0

    def test_clamped_low(self):
        assert _clamp(0, 1, 100, 10) == 1.0

    def test_bad_value_uses_default(self):
        assert _clamp("abc", 1, 100, 50) == 50

    def test_none_uses_default(self):
        assert _clamp(None, 1, 100, 50) == 50


class TestTargets:
    def test_list(self):
        assert _targets({"targets": ["10.0.0.1", "10.0.0.2"]}) == ["10.0.0.1", "10.0.0.2"]

    def test_single_string(self):
        assert _targets({"target": "10.0.0.1"}) == ["10.0.0.1"]

    def test_scope_cidrs(self):
        assert _targets({"scope_cidrs": ["10.0.0.0/24"]}) == ["10.0.0.0/24"]

    def test_empty(self):
        assert _targets({}) == []


class TestTuningFromParams:
    def test_defaults(self):
        t = _tuning_from_params({})
        assert t["rate"] == 200.0
        assert t["concurrency"] == 100
        assert t["timeout"] == 3.0

    def test_clamped_rate(self):
        t = _tuning_from_params({"rate": 1e9})
        assert t["rate"] == 2000.0

    def test_ssh_creds(self):
        t = _tuning_from_params({"ssh_creds": {"user": "admin", "password": "pass"}})
        assert t["ssh_creds"]["user"] == "admin"

    def test_no_ssh_creds_without_user(self):
        t = _tuning_from_params({"ssh_creds": {"password": "pass"}})
        assert "ssh_creds" not in t

    def test_win_creds(self):
        t = _tuning_from_params({"win_creds": {"user": "admin", "password": "pass"}})
        assert t["win_creds"]["user"] == "admin"

    def test_recheck_hours(self):
        t = _tuning_from_params({"recheck_hours": 48})
        assert t["force_recheck_after"] == timedelta(hours=48)

    def test_passive_listen_seconds(self):
        t = _tuning_from_params({"passive_listen_seconds": 120})
        assert t["passive_listen_seconds"] == 120.0


class TestCapabilities:
    def test_capabilities_sorted(self):
        assert CAPABILITIES == sorted(CAPABILITIES)

    def test_known_scan_types(self):
        assert "discovery" in CAPABILITIES
        assert "assessment" in CAPABILITIES
        assert "tls_scan" in CAPABILITIES
        assert "web_tls_scan" in CAPABILITIES
        assert "mcp_discovery" in CAPABILITIES
        assert "snmp_scan" in CAPABILITIES
        assert "passive_discovery" in CAPABILITIES


# ═══════════════════════════════════════════════════════════════════════════
# agent/use_cases.py
# ═══════════════════════════════════════════════════════════════════════════

class TestUseCasesResolve:
    def test_valid_use_case(self):
        st, profile = resolve("uc_discovery_only", None, {})
        assert st == "discovery"
        assert profile == "it"

    def test_full_assessment(self):
        st, profile = resolve("uc_full_assessment", None, {})
        assert st == "assessment"
        assert profile == "it"

    def test_ot_passive(self):
        st, profile = resolve("uc_ot_passive", None, {})
        assert st == "passive_discovery"
        assert profile == "ot"

    def test_unknown_use_case_raises(self):
        with pytest.raises(ValueError, match="Unknown use_case_id"):
            resolve("uc_nonexistent", None, {})

    def test_fallback_to_scan_type(self):
        st, profile = resolve(None, None, {"scan_type": "tls_scan", "profile": "iot"})
        assert st == "tls_scan"
        assert profile == "iot"

    def test_fallback_to_job_type(self):
        st, profile = resolve(None, "assessment", {})
        assert st == "assessment"

    def test_default_discovery(self):
        st, profile = resolve(None, None, {})
        assert st == "discovery"

    def test_use_cases_count(self):
        assert len(USE_CASES) == 12
