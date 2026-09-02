"""
test_exposed_services.py — the exposed-service / suspicious-port detection layer.

Covers the long tail of risky open ports that have no dedicated scanner: backdoor/C2
listeners, unauth-prone data stores, container APIs, databases, cleartext protocols,
and admin UIs — findable from the open port + banner + exposure the validated
scanners already emit. Ground-truthed against the real 192.168.1.72 lab data.
"""
from __future__ import annotations

from models import Asset, Fact, SourceConfidence
import posture_rules as P
import port_intel as PI


def _fact(scanner, port, data, status="open", proto="tcp", target="10.0.0.5"):
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto=proto,
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred, source_file="s", source_line=1)


def _asset(*facts, ip="10.0.0.5"):
    a = Asset(ip=ip, is_ip_keyed=True)
    for f in facts:
        a.add_fact(f)
    return a


def _by_port(findings):
    return {f.port: f for f in findings}


# ── the port-intel catalog ────────────────────────────────────────────────────
class TestClassify:
    def test_backdoor_ports(self):
        for p in (4444, 31337, 12345, 27374, 6667, 5555, 2323):
            r = PI.classify_port(p)
            assert r and r.category == "backdoor", p

    def test_container_apis_are_high(self):
        for p in (2375, 6443, 10250, 2379):
            r = PI.classify_port(p)
            assert r and r.category == "container" and r.severity == "high", p

    def test_unauth_data_stores(self):
        for p in (6379, 27017, 9200, 11211, 5984):
            r = PI.classify_port(p)
            assert r and r.category == "datastore", p

    def test_databases(self):
        for p in (3306, 5432, 1433, 1521, 50000):
            assert PI.classify_port(p).category == "database", p

    def test_cleartext_telnet_is_high(self):
        assert PI.classify_port(23).category == "cleartext"
        assert PI.classify_port(23).severity == "high"

    def test_banner_confirms_backdoor_on_any_port(self):
        # a non-catalog port whose banner screams shell → backdoor
        r = PI.classify_port(54321, banner="Windows Meterpreter session")
        assert r and r.category == "backdoor"

    def test_benign_port_is_none(self):
        assert PI.classify_port(80) is None or PI.classify_port(80).category == "admin_ui" \
            or PI.classify_port(80) is None
        assert PI.classify_port(54321) is None      # no catalog, no banner

    def test_escalate(self):
        assert PI.escalate("medium") == "high"
        assert PI.escalate("high") == "critical"
        assert PI.escalate("critical") == "critical"   # clamped


# ── the detector on real-shaped facts ─────────────────────────────────────────
class TestDetect:
    def test_backdoor_4444_is_high_internal(self):
        a = _asset(_fact("syn_scan", 4444, {}))
        f = _by_port(P.detect_exposed_services(a))[4444]
        assert f.severity == "high" and f.category == "exposure"
        assert "backdoor" in f.title.lower() and f.state == "confirmed"

    def test_internet_facing_escalates_severity(self):
        a = _asset(_fact("syn_scan", 4444, {}), _fact("syn_scan", 3306, {}),
                   _fact("exposure_matrix", None, {"externally_exposed": [4444, 3306],
                                                   "internal_only": []},
                         status="observed", proto=None))
        by = _by_port(P.detect_exposed_services(a))
        assert by[4444].severity == "critical" and by[4444].internet_facing is True
        assert by[3306].severity == "high"

    def test_banner_carried_as_evidence(self):
        a = _asset(_fact("syn_scan", 4444, {}),
                   _fact("service_banner", 4444, {"banner": "VEDHA-LAB-CRITICAL-TCP-4444"}))
        f = _by_port(P.detect_exposed_services(a))[4444]
        assert f.evidence.get("banner") == "VEDHA-LAB-CRITICAL-TCP-4444"

    def test_dedicated_ports_not_double_reported(self):
        # 445/3389/135 have their own deep rules → the generic layer skips them.
        a = _asset(_fact("syn_scan", 445, {}), _fact("syn_scan", 3389, {}),
                   _fact("syn_scan", 135, {}))
        ports = {f.port for f in P.detect_exposed_services(a)}
        assert ports.isdisjoint({445, 3389, 135})

    def test_udp_ports_ignored(self):
        # exposed-service layer is TCP-only (UDP has its own amplifier rule).
        a = _asset(_fact("udp_scan", 161, {"responded": False}, status="open|filtered", proto="udp"))
        assert P.detect_exposed_services(a) == []

    def test_real_lab_host_produces_expected_findings(self):
        # the actual 192.168.1.72 open set → 4444 HIGH + DBs + ES + dev UIs.
        ports = [3306, 4444, 5432, 8081, 9200, 50000]
        facts = [_fact("syn_scan", p, {}) for p in ports]
        facts.append(_fact("exposure_matrix", None,
                           {"externally_exposed": [], "internal_only": ports},
                           status="observed", proto=None))
        by = _by_port(P.detect_exposed_services(_asset(*facts)))
        assert by[4444].severity == "high"                     # backdoor
        assert by[3306].category == "exposure" and by[3306].severity == "medium"  # DB internal
        assert by[9200].severity == "medium"                   # elasticsearch
        assert set(by) == set(ports)


# ── end-to-end through detect_posture (exposed findings flow with the rules) ───
def test_exposed_findings_flow_through_detect_posture():
    a = _asset(_fact("syn_scan", 4444, {}),
               _fact("smb_scan", 445, {"smbv1_enabled": True}))   # a real posture rule too
    findings = P.detect_posture(a)
    rule_ids = {f.rule_id for f in findings}
    assert "POSTURE-SMB-V1-ENABLED" in rule_ids            # the per-fact rule
    assert any(r.startswith("POSTURE-EXPOSED-BACKDOOR") for r in rule_ids)   # the new layer


# ── observed-protocol evidence from service_banner (v3 soft-match) ────────────
class TestObservedServiceSignals:
    def test_shell_label_is_backdoor_on_any_port(self):
        r = PI.classify_port(40123, banner="bash-5.1$ ", service="shell")
        assert r.category == "backdoor" and r.severity == "high"
        assert "shell" in r.service

    def test_telnet_label_off_port_23_is_cleartext(self):
        r = PI.classify_port(2323 + 40000, banner="\xff\xfd\x18login: ", service="telnet")
        assert r.category == "cleartext" and r.severity == "high"

    def test_basic_auth_over_plaintext_is_cleartext_medium(self):
        r = PI.classify_port(8181, banner="HTTP/1.0 401 Unauthorized",
                             basic_auth_cleartext=True)
        assert r.category == "cleartext" and r.severity == "medium"
        assert "Basic" in r.service

    def test_plain_http_label_on_benign_port_is_none(self):
        assert PI.classify_port(8181, banner="HTTP/1.1 200 OK", service="http") is None

    def test_catalog_port_still_wins_its_own_class(self):
        # 23 is already the cleartext catalog entry — no duplicate/override path.
        assert PI.classify_port(23, service="telnet").category == "cleartext"

    def test_detect_uses_service_label_and_flag(self):
        a = _asset(
            _fact("port_scan", 40123, {}),
            _fact("service_banner", 40123, {"banner": "bash-5.1$ ", "service": "shell"}),
            _fact("port_scan", 8181, {}),
            _fact("service_banner", 8181, {"banner": "HTTP/1.0 401 Unauthorized",
                                           "service": "http", "http_status": 401,
                                           "http_auth_scheme": "basic",
                                           "http_basic_auth_cleartext": True}),
            _fact("port_scan", 8182, {}),
            _fact("service_banner", 8182, {"banner": "HTTP/1.0 401 Unauthorized",
                                           "service": "http", "tls": True,
                                           "http_auth_scheme": "basic"}),
        )
        by = _by_port(P.detect_exposed_services(a))
        assert by[40123].rule_id == "POSTURE-EXPOSED-BACKDOOR"
        assert by[40123].evidence["observed_service"] == "shell"
        assert by[8181].rule_id == "POSTURE-EXPOSED-CLEARTEXT"
        assert 8182 not in by          # Basic over TLS is not cleartext


def test_ingest_aliases_from_host_discovery_names():
    from ingest import _extract_aliases
    assert _extract_aliases("host_discovery", {"hostname": "fs01.corp.example",
                                               "netbios_name": "FS01"}) == \
        ["fs01.corp.example", "FS01"]
    assert _extract_aliases("host_discovery", {"alive": True}) == []
    assert _extract_aliases("host_discovery", {"hostname": 42, "netbios_name": " "}) == []


# ── observation beats the port-number hypothesis ─────────────────────────────
class TestPortHypothesisContradiction:
    """A catalog entry is a guess about what a port means. When service_banner
    positively identifies a different, known-benign occupant, the guess is
    disproven — reporting it anyway is a confidently-wrong finding.

    Real case: macOS ships an AirPlay receiver on 5000 and 7000, so every Mac in
    scope produced "Docker registry exposed" (high) and "Cassandra internode
    exposed" (medium). Both were false. Found by scanning a real host.
    """

    def test_airplay_suppresses_the_docker_registry_guess(self):
        assert PI.classify_port(5000) is not None          # bare port still flags
        assert PI.classify_port(5000, product="AirTunes", service="http") is None

    def test_airplay_suppresses_the_cassandra_guess(self):
        assert PI.classify_port(7000) is not None
        assert PI.classify_port(7000, product="AirTunes", service="http") is None

    def test_an_unrelated_product_does_not_suppress(self):
        r = PI.classify_port(7000, product="nginx", service="http")
        assert r is not None and r.category == "datastore"

    def test_backdoor_evidence_is_never_suppressed(self):
        """A shell answering on a benign-listed port is still a backdoor: the
        contradiction check runs only on the port-number hypothesis."""
        r = PI.classify_port(5000, banner="bash-5.1$ ", service="shell",
                             product="AirTunes")
        assert r is not None and r.category == "backdoor"

    def test_contradiction_helper_is_case_and_format_insensitive(self):
        assert PI.contradicts_port_hypothesis(5000, "AirTunes/940.23.1") is True
        assert PI.contradicts_port_hypothesis(5000, "airplay") is True
        assert PI.contradicts_port_hypothesis(5000, None) is False
        assert PI.contradicts_port_hypothesis(9999, "AirTunes") is False

    def test_detect_records_the_observed_product(self):
        a = _asset(
            _fact("port_scan", 2379, {}),
            _fact("service_banner", 2379, {"banner": "HTTP/1.1 404", "service": "etcd",
                                           "product": "etcd"}),
            _fact("port_scan", 7000, {}),
            _fact("service_banner", 7000, {"banner": "HTTP/1.1 403",
                                           "service": "http", "product": "AirTunes"}),
        )
        by = _by_port(P.detect_exposed_services(a))
        assert by[2379].evidence["observed_product"] == "etcd"
        assert 7000 not in by            # AirPlay, not Cassandra
