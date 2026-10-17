"""
test_service_posture_rules.py — the service-layer rule pack.

These 14 rules cover the deep-branch scanners that previously had NO rule at all:
their facts were collected, shipped and stored, then never assessed — a guaranteed
silent false-negative regardless of scanner accuracy. Every fixture below is a real
captured shape (tests/fixtures/probe_corpus/), and every severity matches the
judgement the probe's own findings.py already made for the same weakness, so the
two layers cannot disagree about how serious something is.

Also pins the RDP fix: a live Windows 11 host proved NLA was not enforced via the
scanner's SECOND probe while the first returned RDP_NEG_FAILURE, and the rule read
only the first — reporting schema_drift instead of a high-severity finding.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from models import Asset, Fact, SourceConfidence
import posture_rules as P

CORPUS = Path(__file__).parent / "fixtures" / "probe_corpus"


def _fact(scanner, data, port=None, status="open", target="10.0.0.5"):
    return Fact(scanner=scanner, target=target, timestamp="", port=port, proto="tcp",
                status=status, data=data, evidence="e", error=None,
                source_confidence=SourceConfidence.inferred, source_file="s", source_line=1)


def _asset(*facts, ip="10.0.0.5"):
    a = Asset(ip=ip, is_ip_keyed=True)
    for f in facts:
        a.add_fact(f)
    return a


def _corpus(scanner):
    """The captured fact for one scanner, straight from the probe corpus."""
    for fp in sorted(CORPUS.glob("*.json")):
        for e in json.loads(fp.read_text()):
            if e["scanner"] == scanner and e["status"] == "open" and e.get("data"):
                return e["data"]
    raise AssertionError(f"no captured {scanner} fact in the corpus")


def _fire(rule_id, data, scanner, port=None):
    rule = next(r for r in P.RULES if r.rule_id == rule_id)
    return rule.detect(_fact(scanner, data, port=port))


# ── each rule fires on its REAL captured shape ───────────────────────────────

@pytest.mark.parametrize("rule_id,scanner", [
    ("POSTURE-FTP-ANONYMOUS-LOGIN", "ftp_scan"),
    ("POSTURE-DNS-ZONE-TRANSFER", "dns_scan"),
    ("POSTURE-NFS-WORLD-READABLE-EXPORT", "nfs_scan"),
    ("POSTURE-LDAP-ANONYMOUS-BIND", "ldap_scan"),
    ("POSTURE-VNC-NO-AUTH", "vnc_scan"),
    ("POSTURE-SMTP-USER-ENUMERATION", "smtp_scan"),
    ("POSTURE-SMTP-NO-STARTTLS", "smtp_scan"),
    ("POSTURE-RSYNC-ANONYMOUS-MODULE", "rsync_scan"),
    ("POSTURE-IPMI-CIPHER-ZERO", "ipmi_scan"),
])
def test_rule_fires_on_captured_shape(rule_id, scanner):
    assert _fire(rule_id, _corpus(scanner), scanner) is not None


def test_ssh_rules_against_live_capture():
    """The live Windows host offers OpenSSH 9.5 with strict-kex, so Terrapin must
    NOT fire — a rule that fires on a patched host is worse than no rule."""
    data = _corpus("ssh_scan")
    assert data.get("supports_strict_kex") is True
    assert _fire("POSTURE-SSH-TERRAPIN", data, "ssh_scan") is None


def test_ssh_terrapin_fires_when_strict_kex_absent():
    ev = _fire("POSTURE-SSH-TERRAPIN",
               {"ssh_confirmed": True, "terrapin_vulnerable": True,
                "supports_strict_kex": False, "software": "OpenSSH_8.9"}, "ssh_scan")
    assert ev["software"] == "OpenSSH_8.9"


def test_ssh_weak_algorithms():
    ev = _fire("POSTURE-SSH-WEAK-ALGORITHMS",
               {"ssh_confirmed": True, "software": "OpenSSH_7.4",
                "failures": [{"algorithm": "diffie-hellman-group1-sha1"},
                             {"algorithm": "hmac-sha1"}]}, "ssh_scan")
    assert ev["weak_count"] == 1                    # only group1 is broken; hmac-sha1 is legacy
    # An empty failure list is a clean host, not a finding.
    assert _fire("POSTURE-SSH-WEAK-ALGORITHMS",
                 {"ssh_confirmed": True, "failures": []}, "ssh_scan") is None


def test_smb_null_session_is_silent_on_the_live_host():
    """The live host REFUSED the null bind (STATUS_ACCESS_DENIED) — the secure
    outcome — so the rule must stay silent."""
    data = _corpus("smb_enum_scan")
    assert data["null_session"] is False
    assert _fire("POSTURE-SMB-NULL-SESSION", data, "smb_enum_scan") is None


def test_smb_null_session_fires_when_permitted():
    ev = _fire("POSTURE-SMB-NULL-SESSION",
               {"smb": True, "null_session": True, "guest_session": False,
                "share_count": 4, "user_count": 12,
                "shares": [{"name": "ADMIN$"}, {"name": "C$"}]}, "smb_enum_scan")
    assert ev["user_count"] == 12 and "ADMIN$" in ev["shares"]


# ── no-false-positive guards ─────────────────────────────────────────────────

class TestNegatives:
    def test_ftp_without_anonymous(self):
        assert _fire("POSTURE-FTP-ANONYMOUS-LOGIN",
                     {"ftp": True, "anonymous_login": False}, "ftp_scan") is None

    def test_dns_refused_transfer(self):
        assert _fire("POSTURE-DNS-ZONE-TRANSFER",
                     {"dns": True, "zone_transfer": False,
                      "axfr": {"x.test": {"transferred": False}}}, "dns_scan") is None

    def test_nfs_restricted_exports(self):
        assert _fire("POSTURE-NFS-WORLD-READABLE-EXPORT",
                     {"nfs": True, "world_readable_exports": []}, "nfs_scan") is None

    def test_ldap_bind_refused(self):
        assert _fire("POSTURE-LDAP-ANONYMOUS-BIND",
                     {"ldap": True, "anonymous_bind": False}, "ldap_scan") is None

    def test_vnc_weak_suppressed_when_no_auth_present(self):
        """no-auth is strictly worse and is reported instead."""
        assert _fire("POSTURE-VNC-WEAK-AUTH",
                     {"vnc": True, "weak_auth": True, "no_auth": True}, "vnc_scan") is None

    def test_vnc_weak_suppressed_when_strong_type_offered(self):
        assert _fire("POSTURE-VNC-WEAK-AUTH",
                     {"vnc": True, "weak_auth": True, "no_auth": False,
                      "has_strong_auth": True}, "vnc_scan") is None

    def test_vnc_weak_fires_when_it_is_the_only_option(self):
        assert _fire("POSTURE-VNC-WEAK-AUTH",
                     {"vnc": True, "weak_auth": True, "no_auth": False,
                      "has_strong_auth": False}, "vnc_scan") is not None

    def test_smtp_with_starttls(self):
        assert _fire("POSTURE-SMTP-NO-STARTTLS",
                     {"smtp": True, "starttls": True}, "smtp_scan") is None

    def test_rsync_auth_required(self):
        assert _fire("POSTURE-RSYNC-ANONYMOUS-MODULE",
                     {"rsync": True, "anon_modules": [], "module_count": 2},
                     "rsync_scan") is None

    def test_ipmi_cipher_zero_rejected(self):
        assert _fire("POSTURE-IPMI-CIPHER-ZERO",
                     {"ipmi": True, "cipher_zero": False, "rmcp_status": 1},
                     "ipmi_scan") is None


# ── the RDP false negative this pass fixed ───────────────────────────────────

class TestRdpNoNla:
    def test_fires_from_the_second_probe_when_the_first_failed(self):
        """The live-host case: negotiation returned RDP_NEG_FAILURE so no `nla`
        key exists, but the bare-RDP probe was ACCEPTED — proof NLA is not
        enforced. Reading only the first probe reported schema_drift instead."""
        data = _corpus("rdp_scan")
        assert data["negotiation"] == "failure" and "nla" not in data
        ev = _fire("POSTURE-RDP-NO-NLA", data, "rdp_scan", port=3389)
        assert ev is not None and ev["nla_required"] is False

    def test_fires_from_the_first_probe_when_it_negotiated(self):
        ev = _fire("POSTURE-RDP-NO-NLA",
                   {"rdp_confirmed": True, "negotiation": "response",
                    "nla": False, "selected_protocol": 0}, "rdp_scan", port=3389)
        assert ev is not None and "CredSSP" in ev["proof"]

    def test_silent_when_nla_is_required(self):
        assert _fire("POSTURE-RDP-NO-NLA",
                     {"rdp_confirmed": True, "negotiation": "failure",
                      "nla_required": True}, "rdp_scan", port=3389) is None

    def test_no_longer_reports_schema_drift(self):
        """The regression this fixes: `nla` was declared in `requires` even though
        a failed negotiation legitimately omits it, so every such host degraded the
        campaign verdict with a false drift signal."""
        rule = next(r for r in P.RULES if r.rule_id == "POSTURE-RDP-NO-NLA")
        assert "nla" not in rule.requires
        _f, traces = P.detect_posture_traced(_asset(_fact("rdp_scan", _corpus("rdp_scan"), port=3389)))
        rdp = [t for t in traces if t.rule_id == "POSTURE-RDP-NO-NLA"]
        assert rdp and all(t.outcome != P.OUTCOME_MISSING_INPUT for t in rdp)


class TestRdpNoTls:
    def test_fires_on_ssl_not_allowed(self):
        ev = _fire("POSTURE-RDP-NO-TLS", _corpus("rdp_scan"), "rdp_scan", port=3389)
        assert ev["failure"] == "SSL_NOT_ALLOWED_BY_SERVER"

    def test_ignores_uninterpreted_failure_codes(self):
        """Only codes carrying posture meaning fire; the rest are transport noise."""
        assert _fire("POSTURE-RDP-NO-TLS",
                     {"rdp_confirmed": True, "negotiation": "failure",
                      "failure_code": 4}, "rdp_scan", port=3389) is None

    def test_silent_when_negotiation_succeeded(self):
        assert _fire("POSTURE-RDP-NO-TLS",
                     {"rdp_confirmed": True, "negotiation": "response",
                      "nla": True, "tls": True}, "rdp_scan", port=3389) is None


# ── trust tier: experimental scanners stay SUSPECTED ─────────────────────────

def test_experimental_scanner_findings_are_suspected_not_confirmed():
    """None of the new service scanners is rig-validated, so their findings must
    NOT be presented as confirmed — that gating is what makes the trust tier real."""
    a = _asset(_fact("vnc_scan", _corpus("vnc_scan"), port=5900))
    findings = P.detect_posture(a)
    vnc = [f for f in findings if f.rule_id == "POSTURE-VNC-NO-AUTH"]
    assert vnc and vnc[0].state == "suspected"
    assert "vnc_scan" not in P.VALIDATED_SCANNERS


def test_new_rules_agree_with_probe_findings_severity():
    """The manager and the probe's own findings.py must not disagree about how
    serious the same weakness is."""
    expected = {
        "POSTURE-SSH-TERRAPIN": "medium", "POSTURE-SSH-WEAK-ALGORITHMS": "high",
        "POSTURE-FTP-ANONYMOUS-LOGIN": "high", "POSTURE-DNS-ZONE-TRANSFER": "high",
        "POSTURE-NFS-WORLD-READABLE-EXPORT": "high",
        "POSTURE-LDAP-ANONYMOUS-BIND": "low", "POSTURE-VNC-NO-AUTH": "critical",
        "POSTURE-VNC-WEAK-AUTH": "medium", "POSTURE-SMTP-USER-ENUMERATION": "medium",
        "POSTURE-SMTP-NO-STARTTLS": "low", "POSTURE-RSYNC-ANONYMOUS-MODULE": "high",
        "POSTURE-SMB-NULL-SESSION": "medium", "POSTURE-IPMI-CIPHER-ZERO": "critical",
    }
    actual = {r.rule_id: r.severity for r in P.RULES if r.rule_id in expected}
    assert actual == expected


def test_stock_openssh_with_only_sha1_is_legacy_not_high():
    """M/A5: OpenSSH 9.x still offers hmac-sha1; that must not read as the High finding."""
    facts = {"ssh_confirmed": True, "software": "OpenSSH_9.6",
             "failures": [{"category": "mac", "algorithm": "hmac-sha1",
                           "reasons": ["using broken SHA-1 hash algorithm"]}]}
    assert _fire("POSTURE-SSH-WEAK-ALGORITHMS", facts, "ssh_scan") is None
    ev = _fire("POSTURE-SSH-LEGACY-ALGORITHMS", facts, "ssh_scan")
    assert ev and ev["legacy_count"] == 1


def test_broken_algorithms_by_reason_are_the_high_rule_only():
    facts = {"ssh_confirmed": True,
             "failures": [{"category": "enc", "algorithm": "arcfour",
                           "reasons": ["using broken RC4 cipher"]},
                          {"category": "mac", "algorithm": "hmac-sha1",
                           "reasons": ["using broken SHA-1 hash algorithm"]}]}
    ev = _fire("POSTURE-SSH-WEAK-ALGORITHMS", facts, "ssh_scan")
    assert ev["weak_count"] == 1 and ev["weak"][0]["algorithm"] == "arcfour"
    assert _fire("POSTURE-SSH-LEGACY-ALGORITHMS", facts, "ssh_scan") is None   # not both


def test_legacy_rule_silent_without_failures():
    assert _fire("POSTURE-SSH-LEGACY-ALGORITHMS",
                 {"ssh_confirmed": True, "failures": []}, "ssh_scan") is None


# The exact `failures` list the probe's vendored ssh-audit (probe/scanner/ssh_kexdb.py)
# produces for a stock OpenSSH 9.6p1 server (Ubuntu 24.04 default offer): the NIST
# curves fail with the "suspected as being backdoored" reason, and SHA-1 MACs fail as
# broken SHA-1. Neither is a practical attack, so a default Linux host must not get the
# High rule (it did, on almost every Linux host, until the reason regex dropped
# "backdoored").
_NSA_CURVE = ("using elliptic curves that are suspected as being backdoored by the "
              "U.S. National Security Agency")
_STOCK_OPENSSH_96_FAILURES = [
    {"category": "kex", "algorithm": "ecdh-sha2-nistp256", "reasons": [_NSA_CURVE]},
    {"category": "kex", "algorithm": "ecdh-sha2-nistp384", "reasons": [_NSA_CURVE]},
    {"category": "kex", "algorithm": "ecdh-sha2-nistp521", "reasons": [_NSA_CURVE]},
    {"category": "key", "algorithm": "ecdsa-sha2-nistp256", "reasons": [_NSA_CURVE]},
    {"category": "mac", "algorithm": "hmac-sha1-etm@openssh.com",
     "reasons": ["using broken SHA-1 hash algorithm"]},
    {"category": "mac", "algorithm": "hmac-sha1",
     "reasons": ["using broken SHA-1 hash algorithm"]},
]


def test_stock_openssh_nist_curves_are_legacy_not_high():
    facts = {"ssh_confirmed": True, "software": "OpenSSH_9.6p1",
             "failures": _STOCK_OPENSSH_96_FAILURES}
    assert _fire("POSTURE-SSH-WEAK-ALGORITHMS", facts, "ssh_scan") is None
    ev = _fire("POSTURE-SSH-LEGACY-ALGORITHMS", facts, "ssh_scan")
    assert ev and ev["legacy_count"] == 6


def test_nist_curves_beside_a_broken_cipher_still_high():
    facts = {"ssh_confirmed": True,
             "failures": _STOCK_OPENSSH_96_FAILURES + [
                 {"category": "enc", "algorithm": "3des-cbc",
                  "reasons": ["using broken & deprecated 3DES cipher"]}]}
    ev = _fire("POSTURE-SSH-WEAK-ALGORITHMS", facts, "ssh_scan")
    assert ev["weak_count"] == 1 and ev["weak"][0]["algorithm"] == "3des-cbc"


# ── UPnP / SSDP (STATUS P1-4 item 2: the IoT scanner collected it, no rule read it) ──
_SSDP_CORPUS = {"upnp": True, "server": "Linux/3.14 UPnP/1.0", "st": "upnp:rootdevice",
                "location": "http://192.168.1.90:80/desc.xml"}       # probe_corpus/iot_scan.json


def _ssdp_fact(data, port=1900):
    return _fact("iot_scan", data, port=port)


def test_ssdp_responder_is_the_low_exposure_rule():
    ev = P._upnp_exposed(_ssdp_fact(_SSDP_CORPUS))
    assert ev and ev["server"] == "Linux/3.14 UPnP/1.0"
    assert P._upnp_igd_exposed(_ssdp_fact(_SSDP_CORPUS)) is None


def test_internet_gateway_device_is_its_own_rule_and_only_that():
    igd = {**_SSDP_CORPUS, "st": "urn:schemas-upnp-org:device:InternetGatewayDevice:1"}
    assert P._upnp_igd_exposed(_ssdp_fact(igd))["st"].endswith("InternetGatewayDevice:1")
    assert P._upnp_exposed(_ssdp_fact(igd)) is None
    via_description = {**_SSDP_CORPUS, "upnp_device": {
        "device_type": "urn:schemas-upnp-org:device:InternetGatewayDevice:2",
        "manufacturer": "ACME", "model_name": "R1"}}
    ev = P._upnp_igd_exposed(_ssdp_fact(via_description))
    assert ev["manufacturer"] == "ACME"


def test_no_ssdp_answer_or_other_port_never_fires():
    assert P._upnp_exposed(_ssdp_fact({"upnp": True})) is None          # no headers back
    assert P._upnp_exposed(_ssdp_fact(_SSDP_CORPUS, port=5353)) is None  # mDNS fact


def test_upnp_rules_fire_through_detect_posture():
    import posture_rules as PR
    a = _asset(_ssdp_fact({**_SSDP_CORPUS,
                           "usn": "uuid:1::urn:schemas-upnp-org:service:WANIPConnection:1"}))
    rules = sorted(f.rule_id for f in PR.detect_posture(a))
    assert rules == ["POSTURE-UPNP-IGD-EXPOSED"]
