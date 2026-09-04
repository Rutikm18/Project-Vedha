"""
test_posture_rules.py — the manager posture/config detection engine.

Covers: the trust tier (validated scanner → CONFIRMED, else SUSPECTED), each rule's
positive + negative case, the exposure-shaped risk model, and the unified
run_full_detection entry point. Ground truth: DESKTOP-34M18MB / 192.168.1.77 is a
HARDENED host — a correct engine raises no critical posture finding against it.
"""
from __future__ import annotations

from models import Asset, Fact, SourceConfidence
import posture_rules as P


def _fact(scanner, port, data, status="open", target="192.168.1.77"):
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred,
                source_file="s.jsonl", source_line=1)


def _asset(*facts, ip="192.168.1.77"):
    a = Asset(ip=ip, is_ip_keyed=True)
    for f in facts:
        a.add_fact(f)
    return a


# ── trust tier ────────────────────────────────────────────────────────────────
class TestTrustTier:
    def test_validated_scanner_confirms(self):
        a = _asset(_fact("smb_scan", 445, {"smb2_supported": True, "signing_required": False}))
        f = P.detect_posture(a)[0]
        assert f.rule_id == "POSTURE-SMB-SIGNING-OFF" and f.state == "confirmed"
        assert f.confidence >= 85

    def test_unvalidated_scanner_only_suspects(self):
        # snmp_scan is NOT in the validated tier → suspected, not confirmed.
        a = _asset(_fact("snmp_scan", 161, {"community": "public"}))
        f = P.detect_posture(a)[0]
        assert f.rule_id == "POSTURE-SNMP-DEFAULT-COMMUNITY" and f.state == "suspected"

    def test_registry_contains_user_validated_set(self):
        for s in ("smb_scan", "rdp_scan", "tls_scan", "msrpc_scan", "udp_scan",
                  "port_scan", "host_discovery", "rpc_reconcile"):
            assert P.is_validated(s)


# ── ground truth: hardened host raises nothing critical ───────────────────────
class TestHardenedGroundTruth:
    def _host(self):
        return _asset(
            _fact("rdp_scan", 3389, {"rdp_confirmed": True, "nla": True, "tls": True,
                                     "nla_required": True, "selected_protocol": 8}),
            _fact("smb_scan", 445, {"smbv1_enabled": False, "smb2_supported": True,
                                    "signing_required": True, "negotiated_dialect": "0x0311"}),
            _fact("msrpc_scan", 135, {"msrpc": True, "endpoint_count": 166}))

    def test_no_critical_or_high_findings(self):
        fs = P.detect_posture(self._host())
        assert not any(f.priority in ("critical", "high") for f in fs)

    def test_rdp_exposed_is_low_because_nla_required(self):
        rdp = [f for f in P.detect_posture(self._host()) if f.rule_id == "POSTURE-RDP-EXPOSED"][0]
        assert rdp.auth_enforced is True and rdp.risk_score <= 15 and rdp.priority == "low"

    def test_hardened_smb_and_rdp_raise_no_misconfig(self):
        ids = {f.rule_id for f in P.detect_posture(self._host())}
        assert "POSTURE-SMB-V1-ENABLED" not in ids
        assert "POSTURE-SMB-SIGNING-OFF" not in ids
        assert "POSTURE-RDP-NO-NLA" not in ids


# ── vulnerable host: confirmed high/critical with correct risk ────────────────
class TestVulnerableHost:
    def test_smbv1_is_confirmed_critical(self):
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}))
        f = [x for x in P.detect_posture(a) if x.rule_id == "POSTURE-SMB-V1-ENABLED"][0]
        assert f.state == "confirmed" and f.severity == "critical"
        assert f.priority in ("critical", "high") and f.cwe == "CWE-477" and f.mitre == "T1210"

    def test_rdp_no_nla_confirmed_high_and_unauth(self):
        a = _asset(_fact("rdp_scan", 3389, {"rdp_confirmed": True, "nla": False,
                                            "tls": False, "standard_rdp_security": True,
                                            "nla_required": False, "selected_protocol": 0}))
        f = [x for x in P.detect_posture(a) if x.rule_id == "POSTURE-RDP-NO-NLA"][0]
        assert f.state == "confirmed" and f.auth_enforced is False
        assert f.priority in ("high", "critical")

    def test_deprecated_tls_version(self):
        a = _asset(_fact("tls_scan", 443, {"accepted_versions": ["TLSv1.0", "TLS 1.2"]}))
        f = [x for x in P.detect_posture(a) if x.rule_id == "POSTURE-TLS-DEPRECATED-VERSION"][0]
        assert f.evidence["deprecated_versions"] == ["TLSV1.0"]

    def test_deprecated_tls_version_underscore_labels(self):
        """The live tls_scanner labels its probe list "TLSv1_0"/"TLSv1_1" (from
        ssl.TLSVersion names) while cipher_by_version, the captured probe corpus
        and this rule all use the dotted "TLSv1.0" form. The separator mismatch
        meant a server that genuinely accepted TLS 1.0 produced no finding. The
        rule must accept both spellings — including for facts already stored."""
        a = _asset(_fact("tls_scan", 443,
                         {"accepted_versions": ["TLSv1_2", "TLSv1_1", "TLSv1_0"]}))
        f = [x for x in P.detect_posture(a) if x.rule_id == "POSTURE-TLS-DEPRECATED-VERSION"][0]
        assert f.evidence["deprecated_versions"] == ["TLSV1.0", "TLSV1.1"]

    def test_modern_only_tls_raises_nothing(self):
        a = _asset(_fact("tls_scan", 443,
                         {"accepted_versions": ["TLSv1_2", "TLSv1_3"]}))
        ids = {x.rule_id for x in P.detect_posture(a)}
        assert "POSTURE-TLS-DEPRECATED-VERSION" not in ids

    def test_self_signed_and_expired_cert(self):
        a = _asset(_fact("tls_scan", 443, {"certificate": {"self_signed": True,
                                                           "expired": True, "subject": "CN=x"}}))
        ids = {f.rule_id for f in P.detect_posture(a)}
        assert "POSTURE-TLS-SELF-SIGNED" in ids and "POSTURE-TLS-EXPIRED-CERT" in ids


# ── UDP honesty carries into detection ────────────────────────────────────────
class TestUdpHonesty:
    def test_amplifier_fires_only_when_it_answered(self):
        answered = _asset(_fact("udp_scan", 161, {"service": "snmp", "responded": True}))
        assert any(f.rule_id == "POSTURE-UDP-AMPLIFIER" for f in P.detect_posture(answered))

    def test_no_reply_udp_raises_nothing(self):
        silent = _asset(_fact("udp_scan", 161, {"service": "snmp", "responded": False},
                              status="open|filtered"))
        assert not any(f.rule_id == "POSTURE-UDP-AMPLIFIER" for f in P.detect_posture(silent))


# ── risk model ────────────────────────────────────────────────────────────────
class TestRiskModel:
    def test_auth_enforced_deescalates(self):
        s_no, _ = P.compute_risk("high", "confirmed", None, None)
        s_auth, _ = P.compute_risk("high", "confirmed", None, True)
        assert s_auth < s_no

    def test_internet_facing_unauth_escalates(self):
        s_base, _ = P.compute_risk("high", "confirmed", None, None)
        s_exposed, _ = P.compute_risk("high", "confirmed", True, False)
        assert s_exposed >= s_base

    def test_suspected_scores_below_confirmed(self):
        s_conf, _ = P.compute_risk("high", "confirmed", None, None)
        s_susp, _ = P.compute_risk("high", "suspected", None, None)
        assert s_susp < s_conf

    def test_priority_buckets(self):
        assert P.compute_risk("critical", "confirmed", True, False)[1] == "critical"
        assert P.compute_risk("low", "suspected", None, True)[1] == "low"


# ── invariants + dedup ────────────────────────────────────────────────────────
class TestInvariants:
    def test_deterministic_id_across_runs(self):
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}))
        id1 = P.detect_posture(a)[0].finding_id
        id2 = P.detect_posture(a)[0].finding_id
        assert id1 == id2

    def test_dedup_same_rule_same_port(self):
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}),
                   _fact("smb_scan", 445, {"smbv1_enabled": True}))
        smbv1 = [f for f in P.detect_posture(a) if f.rule_id == "POSTURE-SMB-V1-ENABLED"]
        assert len(smbv1) == 1

    def test_detect_all_sorts_by_risk_desc(self):
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}),           # critical
                   _fact("msrpc_scan", 135, {"msrpc": True, "endpoint_count": 5}))  # medium
        fs = P.detect_all({a.ip: a})
        assert fs[0].risk_score >= fs[-1].risk_score
