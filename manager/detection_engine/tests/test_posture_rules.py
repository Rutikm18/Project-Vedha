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


def _fact(scanner, port, data, status="open", target="192.168.1.77", proto="tcp"):
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto=proto,
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

    def test_snmp_default_community_is_confirmed(self):
        # snmp_scan was promoted into the validated tier (M5) after the lab-rig verification.
        a = _asset(_fact("snmp_scan", 161, {"community": "public"}))
        f = P.detect_posture(a)[0]
        assert f.rule_id == "POSTURE-SNMP-DEFAULT-COMMUNITY" and f.state == "confirmed"

    def test_unvalidated_scanner_only_suspects(self):
        # A scanner outside the validated tier can only SUSPECT.
        assert not P.is_validated("web_scan")
        assert P._state_for("web_scan") == "suspected"

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
    def test_plain_answer_is_not_an_amplifier(self):
        """M4: answering a normal query (DNS recursion off, stock SNMP) is exposure only."""
        for svc, port, extra in (("dns", 53, {"recursion_available": False, "open_recursion": False}),
                                 ("snmp", 161, {}), ("ntp", 123, {"monlist_enabled": False})):
            a = _asset(_fact("udp_scan", port, {"service": svc, "responded": True, **extra}))
            assert not any(f.rule_id == "POSTURE-UDP-AMPLIFIER" for f in P.detect_posture(a)), svc

    def test_amplifier_fires_on_protocol_proof(self):
        for svc, port, extra in (("dns", 53, {"open_recursion": True}),
                                 ("ntp", 123, {"monlist_enabled": True}),
                                 ("memcached", 11211, {"exposed_unauthenticated": True}),
                                 ("chargen", 19, {})):
            a = _asset(_fact("udp_scan", port, {"service": svc, "responded": True, **extra}))
            assert any(f.rule_id == "POSTURE-UDP-AMPLIFIER" for f in P.detect_posture(a)), svc

    def test_amplifier_measured_factor_gate(self):
        def fires(svc, port, factor):
            a = _asset(_fact("udp_scan", port, {"service": svc, "responded": True,
                                                "amplification_factor": factor}))
            return any(f.rule_id == "POSTURE-UDP-AMPLIFIER" for f in P.detect_posture(a))
        assert fires("ssdp", 1900, 31.0) and not fires("ssdp", 1900, 12.0)
        assert fires("dns", 53, 40.0) and not fires("dns", 53, 3.0)

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


# ── M2: state follows evidence strength, not scanner membership ───────────────
class TestEvidenceBasis:
    def test_inference_is_never_confirmed_even_from_a_validated_scanner(self):
        assert P.is_validated("port_scan")
        assert P._state_for("port_scan", P.BASIS_PORT_INFERENCE) == "suspected"
        assert P._state_for("port_scan", P.BASIS_BANNER_INFERENCE) == "suspected"
        assert P._state_for("port_scan", P.BASIS_PROTOCOL_OBSERVED) == "confirmed"

    def test_unvalidated_scanner_cannot_confirm_even_with_protocol_basis(self):
        assert P._state_for("web_scan", P.BASIS_PROTOCOL_OBSERVED) == "suspected"

    def test_every_rule_declares_a_known_basis(self):
        assert all(r.evidence_basis in P.EVIDENCE_BASES for r in P.RULES)

    def test_dedicated_rule_findings_carry_their_basis(self):
        a = _asset(_fact("smb_scan", 445, {"smb2_supported": True, "signing_required": False}))
        f = P.detect_posture(a)[0]
        assert f.evidence["evidence_basis"] == "protocol_observed" and f.state == "confirmed"


# ── M1: canonical condition key ───────────────────────────────────────────────
def test_engine_rules_stamp_canonical_keys():
    assert P.condition_key_for("POSTURE-EXPOSED-CLEARTEXT", "exposure", 23) == "exposed:23"
    # dedicated NFS scanner and the port-intel NFS row are the SAME condition
    assert P.condition_key_for("POSTURE-NFS-WORLD-READABLE-EXPORT", "misconfiguration", 2049) == "exposed:2049"
    # amplifier + exposure on SNMP collapse; default-community is a different weakness
    assert (P.condition_key_for("POSTURE-SNMP-AMPLIFIER", "amplification", 161, "udp")
            == P.condition_key_for("POSTURE-UDP-AMPLIFIER", "amplification", 161, "udp"))
    assert (P.condition_key_for("POSTURE-SNMP-DEFAULT-COMMUNITY", "default_credentials", 161, "udp")
            != P.condition_key_for("POSTURE-SNMP-AMPLIFIER", "amplification", 161, "udp"))
    # two different weak-crypto weaknesses on 443 stay apart
    assert (P.condition_key_for("POSTURE-TLS-WEAK-CIPHER", "weak_crypto", 443)
            != P.condition_key_for("POSTURE-TLS-DEPRECATED-VERSION", "weak_crypto", 443))


def test_engine_stamps_dedup_key_on_findings():
    a = _asset(_fact("smb_scan", 445, {"smb2_supported": True, "signing_required": False}))
    f = P.detect_posture(a)[0]
    assert f.evidence["dedup_key"] == "smb-signing-off:445"


# ── M6: rules for facts the agent already collects ────────────────────────────
class TestUdpServiceRules:
    @staticmethod
    def _rules(*facts):
        return {f.rule_id for f in P.detect_posture(_asset(*facts))}

    def test_sip_needs_a_real_sip_status_line(self):
        sip = _fact("udp_scan", 5060, {"service": "sip", "responded": True,
                                       "sip_response": "SIP/2.0 200 OK", "server": "x"})
        junk = _fact("udp_scan", 5060, {"service": "sip", "responded": True, "sip_response": "garbage"})
        assert "POSTURE-SIP-EXPOSED" in self._rules(sip)
        assert "POSTURE-SIP-EXPOSED" not in self._rules(junk)

    def test_netbios_and_mdns(self):
        nb = _fact("udp_scan", 137, {"service": "netbios-ns", "responded": True})
        md = _fact("udp_scan", 5353, {"service": "mdns", "responded": True, "mdns_response": True})
        md_query = _fact("udp_scan", 5353, {"service": "mdns", "responded": True, "mdns_response": False})
        assert "POSTURE-NETBIOS-EXPOSED" in self._rules(nb)
        assert "POSTURE-MDNS-EXPOSED" in self._rules(md)
        assert "POSTURE-MDNS-EXPOSED" not in self._rules(md_query)

    def test_silence_never_raises_them(self):
        silent = _fact("udp_scan", 137, {"service": "netbios-ns", "responded": False},
                       status="open|filtered")
        assert not (self._rules(silent) & {"POSTURE-NETBIOS-EXPOSED", "POSTURE-SIP-EXPOSED",
                                            "POSTURE-MDNS-EXPOSED"})

    def test_ike_aggressive_only_on_the_observed_exchange(self):
        agg = _fact("udp_scan", 500, {"service": "ike", "responded": True,
                                      "version": "IKEv1.0", "exchange_type": 4})
        main = _fact("udp_scan", 500, {"service": "ike", "responded": True,
                                       "version": "IKEv1.0", "exchange_type": 2})
        v2 = _fact("udp_scan", 500, {"service": "ike", "responded": True,
                                     "version": "IKEv2.0", "exchange_type": 34})
        assert "POSTURE-IKE-AGGRESSIVE-MODE" in self._rules(agg)
        assert "POSTURE-IKE-AGGRESSIVE-MODE" not in self._rules(main)
        assert "POSTURE-IKE-AGGRESSIVE-MODE" not in self._rules(v2)

    def test_exposure_rules_share_the_exposed_class_with_port_intel(self):
        assert P.weakness_class_for("POSTURE-SIP-EXPOSED", "exposure") == "exposed"
        assert P.weakness_class_for("POSTURE-IKE-AGGRESSIVE-MODE", "weak_crypto") == "ike-aggressive-mode"

    def test_new_findings_are_confirmed_protocol_observations(self):
        nb = _fact("udp_scan", 137, {"service": "netbios-ns", "responded": True}, proto="udp")
        f = next(f for f in P.detect_posture(_asset(nb)) if f.rule_id == "POSTURE-NETBIOS-EXPOSED")
        assert f.state == "confirmed" and f.evidence["dedup_key"] == "exposed:137/udp"


# ── A4/B7: an open port nothing identified ────────────────────────────────────
class TestUnidentifiedService:
    @staticmethod
    def _rules(*facts):
        return {f.rule_id for f in P.detect_posture(_asset(*facts))}

    def test_fires_when_the_banner_stage_found_nothing(self):
        f = _fact("service_banner", 6100, {"banner": None, "identified": False, "raw_hex": "00ff"})
        assert "POSTURE-UNIDENTIFIED-SERVICE" in self._rules(f)
        finding = next(x for x in P.detect_posture(_asset(f)) if x.rule_id == "POSTURE-UNIDENTIFIED-SERVICE")
        assert finding.severity == "low" and finding.state == "suspected"
        assert finding.evidence["dedup_key"] == "exposed:6100"

    def test_a_probe_build_without_the_flag_is_not_read_as_unidentified(self):
        assert "POSTURE-UNIDENTIFIED-SERVICE" not in self._rules(
            _fact("service_banner", 6100, {"banner": None}))

    def test_identified_services_never_fire(self):
        assert "POSTURE-UNIDENTIFIED-SERVICE" not in self._rules(
            _fact("service_banner", 6100, {"banner": "x", "identified": True}))

    def test_silent_by_design_catalog_and_ephemeral_ports_are_excluded(self):
        for port in (445, 3389, 135, 4444, 6379, 50000, 60000):
            assert "POSTURE-UNIDENTIFIED-SERVICE" not in self._rules(
                _fact("service_banner", port, {"identified": False})), port


# ── A3: SNMPv3 noAuth user and anonymous FTP write ────────────────────────────
class TestA3Rules:
    @staticmethod
    def _rules(*facts):
        return {f.rule_id for f in P.detect_posture(_asset(*facts))}

    def test_snmpv3_noauth_user(self):
        hit = _fact("snmp_scan", 161, {"snmpv3_present": True, "snmpv3_noauth_user": "initial"}, proto="udp")
        miss = _fact("snmp_scan", 161, {"snmpv3_present": True, "snmpv3_noauth_user": None}, proto="udp")
        old_probe = _fact("snmp_scan", 161, {"snmpv3_present": True}, proto="udp")
        assert "POSTURE-SNMPV3-NOAUTH-USER" in self._rules(hit)
        assert "POSTURE-SNMPV3-NOAUTH-USER" not in self._rules(miss)
        assert "POSTURE-SNMPV3-NOAUTH-USER" not in self._rules(old_probe)

    def test_snmpv3_noauth_is_a_confirmed_high(self):
        f = next(x for x in P.detect_posture(_asset(_fact(
            "snmp_scan", 161, {"snmpv3_noauth_user": "admin"}, proto="udp")))
            if x.rule_id == "POSTURE-SNMPV3-NOAUTH-USER")
        assert (f.severity, f.state) == ("high", "confirmed")

    def test_ftp_anonymous_write_needs_a_proven_upload(self):
        base = {"ftp": True, "anonymous_login": True, "anon_read": True, "software": "vsftpd"}
        assert "POSTURE-FTP-ANONYMOUS-WRITE" in self._rules(_fact("ftp_scan", 21, {**base, "anon_write": True}))
        for value in (False, None):
            assert "POSTURE-FTP-ANONYMOUS-WRITE" not in self._rules(
                _fact("ftp_scan", 21, {**base, "anon_write": value}))
        assert "POSTURE-FTP-ANONYMOUS-WRITE" not in self._rules(_fact("ftp_scan", 21, base))

    def test_leftover_file_is_reported(self):
        f = next(x for x in P.detect_posture(_asset(_fact("ftp_scan", 21, {
            "ftp": True, "anonymous_login": True, "anon_write": True,
            "anon_write_leftover": "vedha-write-test-ab12.txt"})))
            if x.rule_id == "POSTURE-FTP-ANONYMOUS-WRITE")
        assert f.severity == "critical" and f.evidence["leftover_file"] == "vedha-write-test-ab12.txt"

    def test_measured_amplification_factor_flows_to_the_amplifier_rule(self):
        fact = _fact("udp_scan", 1900, {"service": "ssdp", "responded": True,
                                        "request_bytes": 100, "reply_bytes": 3200,
                                        "amplification_factor": 32.0}, proto="udp")
        assert "POSTURE-UDP-AMPLIFIER" in self._rules(fact)


def test_unidentified_service_is_not_raised_for_a_port_another_scanner_explained():
    banner = _fact("service_banner", 1883, {"banner": None, "identified": False})
    mqtt = _fact("iot_scan", 1883, {"mqtt_connack": True, "unauthenticated_access": True})
    rules = {f.rule_id for f in P.detect_posture(_asset(banner, mqtt))}
    assert "POSTURE-MQTT-UNAUTHENTICATED" in rules
    assert "POSTURE-UNIDENTIFIED-SERVICE" not in rules
    # …and still fires when nothing else saw the port.
    assert "POSTURE-UNIDENTIFIED-SERVICE" in {f.rule_id for f in P.detect_posture(_asset(banner))}


def test_catalogued_long_tail_ports_are_named_not_unidentified():
    """Smart Install, Radmin, EPMD, BGP, SLP and AFP are in the exposure catalog, so a silent
    listener on them is that finding — never the generic 'unidentified service'."""
    for port in (4786, 4899, 4369, 179, 427, 548):
        f = _fact("service_banner", port, {"banner": None, "identified": False})
        assert "POSTURE-UNIDENTIFIED-SERVICE" not in {x.rule_id for x in P.detect_posture(_asset(f))}
