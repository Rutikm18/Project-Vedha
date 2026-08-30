"""
test_posture_confidence.py — calibrated, auditable posture confidence with
cross-signal attack-chain corroboration.

Properties proved:
  * confidence is SEPARATE from impact (risk/severity/state untouched);
  * every factor is recorded (auditable, like verifier.py's checks{});
  * a corroborated attack chain FLOORS confidence higher — but a LONE member does not
    (no partner → no inflation);
  * downgrades (unconfirmed reachability, deception) only ever lower.
"""
from __future__ import annotations

from models import Asset, Fact, SourceConfidence
import posture_rules as P
import posture_confidence as C


def _fact(scanner, port, data, status="open", target="10.0.0.5"):
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred,
                source_file="s.jsonl", source_line=1)


def _asset(*facts, ip="10.0.0.5"):
    a = Asset(ip=ip, is_ip_keyed=True)
    for f in facts:
        a.add_fact(f)
    return a


def _by_rule(findings):
    return {f.rule_id: f for f in findings}


# ── the pure assessor ─────────────────────────────────────────────────────────
class TestAssessor:
    def test_validated_base_higher_than_unvalidated(self):
        cv, _ = C.assess_confidence(rule_id="R", scanner="smb_scan", evidence_ref_count=1,
                                    reachable=True, host_rule_ids={"R"})
        cu, _ = C.assess_confidence(rule_id="R", scanner="snmp_scan", evidence_ref_count=1,
                                    reachable=True, host_rule_ids={"R"})
        assert cv == C._VALIDATED_BASE and cu == C._UNVALIDATED_BASE and cv > cu

    def test_unreachable_downgrades_and_is_recorded(self):
        c, f = C.assess_confidence(rule_id="R", scanner="smb_scan", evidence_ref_count=1,
                                   reachable=False, host_rule_ids={"R"})
        assert c == C._VALIDATED_BASE - C._PENALTY_UNREACHABLE
        assert f["reachability_unconfirmed"] == -C._PENALTY_UNREACHABLE

    def test_lone_chain_member_gets_no_floor(self):
        # SMBv1 alone (no SMB-signing partner) → no corroboration inflation.
        c, f = C.assess_confidence(rule_id="POSTURE-SMB-V1-ENABLED", scanner="smb_scan",
                                   evidence_ref_count=1, reachable=True,
                                   host_rule_ids={"POSTURE-SMB-V1-ENABLED"})
        assert "chain_corroboration" not in f
        assert c == C._VALIDATED_BASE

    def test_deception_penalty(self):
        c, f = C.assess_confidence(rule_id="R", scanner="smb_scan", evidence_ref_count=1,
                                   reachable=True, host_rule_ids={"R"}, deception=0.6)
        assert f["deception_suspected"] == -C._PENALTY_DECEPTION_HI
        assert c == C._VALIDATED_BASE - C._PENALTY_DECEPTION_HI

    def test_final_is_clamped_and_recorded(self):
        c, f = C.assess_confidence(rule_id="R", scanner="snmp_scan", evidence_ref_count=1,
                                   reachable=False, host_rule_ids={"R"}, deception=0.6)
        assert 0 <= c <= 100 and f["final"] == c


# ── corroboration matrix ──────────────────────────────────────────────────────
class TestChains:
    def test_ntlm_relay_chain_floors_both(self):
        host = {"POSTURE-SMB-V1-ENABLED", "POSTURE-SMB-SIGNING-OFF"}
        chains = C.corroborating_chains("POSTURE-SMB-V1-ENABLED", host)
        assert ("ntlm_relay_surface", 92) in chains
        c, f = C.assess_confidence(rule_id="POSTURE-SMB-V1-ENABLED", scanner="smb_scan",
                                   evidence_ref_count=1, reachable=True, host_rule_ids=host)
        assert c == 92 and "ntlm_relay_surface" in f["chain_corroboration"]["chains"]

    def test_chain_floor_never_lowers_confidence(self):
        # if base already exceeds the floor, the floor applies 0 (never a downgrade).
        c, f = C.assess_confidence(rule_id="POSTURE-TLS-DEPRECATED-VERSION", scanner="tls_scan",
                                   evidence_ref_count=3, reachable=True,
                                   host_rule_ids={"POSTURE-TLS-DEPRECATED-VERSION",
                                                  "POSTURE-TLS-WEAK-CIPHER"})
        # base 85 + multi_evidence 5 = 90 > weak_tls floor 85 → applied 0
        assert c == 90 and f["chain_corroboration"]["applied"] == 0


# ── end-to-end through detect_posture_traced ──────────────────────────────────
class TestEndToEnd:
    def test_corroborated_host_gets_floored_confidence_and_factors(self):
        # SMBv1 + SMB-signing-off on one host → both findings floored at 92.
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True, "smb2_supported": True,
                                           "signing_required": False}))
        findings, _tr = P.detect_posture_traced(a)
        by = _by_rule(findings)
        smbv1 = by["POSTURE-SMB-V1-ENABLED"]
        signing = by["POSTURE-SMB-SIGNING-OFF"]
        assert smbv1.confidence == 92 and signing.confidence == 92
        assert smbv1.precision_factors["chain_corroboration"]["floor"] == 92
        # impact is untouched — confidence and risk are separate axes
        assert smbv1.severity == "critical" and smbv1.risk_score > 0

    def test_lone_finding_keeps_base_confidence(self):
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}))
        findings, _tr = P.detect_posture_traced(a)
        smbv1 = _by_rule(findings)["POSTURE-SMB-V1-ENABLED"]
        assert smbv1.confidence == C._VALIDATED_BASE           # no partner → no floor
        assert "chain_corroboration" not in smbv1.precision_factors

    def test_filtered_port_lowers_confidence(self):
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}, status="filtered"))
        findings, _tr = P.detect_posture_traced(a)
        smbv1 = _by_rule(findings)["POSTURE-SMB-V1-ENABLED"]
        assert smbv1.confidence == C._VALIDATED_BASE - C._PENALTY_UNREACHABLE
        assert smbv1.precision_factors["reachability_unconfirmed"] < 0

    def test_confidence_is_serialized(self):
        a = _asset(_fact("smb_scan", 445, {"smbv1_enabled": True}))
        findings, _tr = P.detect_posture_traced(a)
        d = findings[0].to_dict()
        assert "precision_factors" in d and d["confidence"] == C._VALIDATED_BASE
