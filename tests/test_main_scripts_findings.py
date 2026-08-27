"""
test_main_scripts_findings.py — the findings interpretation layer.

Pure-logic, no network. Each rule is checked with a positive fact (finding fires,
correct severity/category/evidence) AND a negative/ambiguous fact (no finding).
Also covers the cross-cutting invariants: `open|filtered` never raises exposure,
findings are evidence-backed, deduped, and severity-sorted, and nothing emits a
`cve_id` (CVE detection stays on the manager).
"""
from __future__ import annotations

from main_scripts import findings as F


def _run(*facts):
    return F.run_findings(list(facts))


def _ids(findings):
    return {f.rule_id for f in findings}


# ── TLS ──────────────────────────────────────────────────────────────────────
def test_tls_obsolete_protocol_is_high():
    fs = _run({"scanner": "tls_scan", "target": "10.0.0.5", "port": 443, "status": "open",
               "data": {"accepted_versions": ["SSLv3", "TLSv1.2"]}})
    hit = [f for f in fs if f.rule_id == "TLS-OBSOLETE-PROTO"]
    assert hit and hit[0].severity == F.SEV_HIGH
    assert hit[0].category == F.CAT_WEAK_CRYPTO
    assert "SSLV3" in hit[0].evidence.upper()


def test_tls_legacy_protocol_is_medium_and_not_double_reported_with_obsolete():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.0", "TLSv1.2"]}})
    assert "TLS-LEGACY-PROTO" in _ids(fs)
    assert "TLS-OBSOLETE-PROTO" not in _ids(fs)
    assert next(f for f in fs if f.rule_id == "TLS-LEGACY-PROTO").severity == F.SEV_MEDIUM


def test_tls_modern_only_produces_no_crypto_finding():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2", "TLSv1.3"], "cipher_analysis": []}})
    assert not (_ids(fs) & {"TLS-OBSOLETE-PROTO", "TLS-LEGACY-PROTO", "TLS-WEAK-CIPHER"})


def test_tls_weak_cipher_is_high_with_reasons():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2"],
                        "cipher_analysis": [{"name": "RC4-SHA", "weak": True, "weak_reasons": ["rc4"]}]}})
    hit = next(f for f in fs if f.rule_id == "TLS-WEAK-CIPHER")
    assert hit.severity == F.SEV_HIGH and "RC4" in hit.evidence.upper()


def test_tls_expired_and_self_signed_cert():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2"],
                        "certificate": {"expired": True, "self_signed": True, "not_after": "2020-01-01"}}})
    assert {"TLS-CERT-EXPIRED", "TLS-CERT-SELF-SIGNED"} <= _ids(fs)


def test_tls_weak_signature_hash_is_flagged():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2"],
                        "certificate": {"sig_algorithm": "sha1"}}})
    hit = next(f for f in fs if f.rule_id == "TLS-CERT-WEAK-SIGNATURE")
    assert hit.severity == F.SEV_MEDIUM and hit.category == F.CAT_WEAK_CRYPTO
    assert "SHA1" in hit.evidence.upper()


def test_tls_strong_signature_hash_is_not_flagged():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2"],
                        "certificate": {"sig_algorithm": "sha256"}}})
    assert "TLS-CERT-WEAK-SIGNATURE" not in _ids(fs)


def test_tls_under_strength_rsa_key_is_flagged():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2"],
                        "certificate": {"public_key_type": "RSA", "public_key_bits": 1024}}})
    hit = next(f for f in fs if f.rule_id == "TLS-CERT-WEAK-KEY")
    assert hit.severity == F.SEV_MEDIUM and hit.category == F.CAT_WEAK_CRYPTO
    assert "1024" in hit.evidence


def test_tls_strong_rsa_key_is_not_flagged():
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2"],
                        "certificate": {"public_key_type": "RSA", "public_key_bits": 2048}}})
    assert "TLS-CERT-WEAK-KEY" not in _ids(fs)


def test_tls_small_ec_key_is_not_treated_as_weak():
    # A 256-bit EC key is ~3072-bit-RSA strong; the bit count must NOT be compared.
    fs = _run({"scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
               "data": {"accepted_versions": ["TLSv1.2"],
                        "certificate": {"public_key_type": "EC", "public_key_bits": 256}}})
    assert "TLS-CERT-WEAK-KEY" not in _ids(fs)


# ── SMB ──────────────────────────────────────────────────────────────────────
def test_smbv1_enabled_is_high():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": True, "negotiated_dialect": "0x0202"}})
    hit = next(f for f in fs if f.rule_id == "SMB-V1-ENABLED")
    assert hit.severity == F.SEV_HIGH and hit.category == F.CAT_MISCONFIG


def test_smb_signing_not_required_is_medium():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": False, "signing_required": False, "signing_supported": True}})
    assert "SMB-SIGNING-NOT-REQUIRED" in _ids(fs)
    assert "SMB-V1-ENABLED" not in _ids(fs)


def test_smb_hardened_host_no_finding():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": False, "signing_required": True, "signing_supported": True}})
    assert not (_ids(fs) & {"SMB-V1-ENABLED", "SMB-SIGNING-NOT-REQUIRED"})


# ── SNMP ─────────────────────────────────────────────────────────────────────
def test_snmp_default_community_is_high():
    fs = _run({"scanner": "snmp_scan", "target": "t", "port": 161, "status": "open",
               "data": {"community": "public", "snmpv3_present": False}})
    hit = next(f for f in fs if f.rule_id == "SNMP-COMMUNITY-READABLE")
    assert hit.severity == F.SEV_HIGH and hit.category == F.CAT_DEFAULT_CRED


def test_snmp_nondefault_community_is_medium():
    fs = _run({"scanner": "snmp_scan", "target": "t", "port": 161, "status": "open",
               "data": {"community": "s3cr3t-str1ng"}})
    assert next(f for f in fs if f.rule_id == "SNMP-COMMUNITY-READABLE").severity == F.SEV_MEDIUM


def test_snmp_amplification():
    fs = _run({"scanner": "snmp_scan", "target": "t", "port": 161, "status": "open",
               "data": {"amplification_factor": 6.4}})
    assert "SNMP-AMPLIFICATION" in _ids(fs)


def test_snmpv3_only_no_finding():
    fs = _run({"scanner": "snmp_scan", "target": "t", "port": 161, "status": "open",
               "data": {"snmpv3_present": True, "v1v2c_community": None}})
    assert not _ids(fs)


# ── UDP amplification ────────────────────────────────────────────────────────
def test_ntp_monlist_and_dns_open_recursion():
    fs = _run(
        {"scanner": "udp_scan", "target": "t", "port": 123, "status": "open",
         "data": {"service": "ntp", "monlist_enabled": True}},
        {"scanner": "udp_scan", "target": "t", "port": 53, "status": "open",
         "data": {"service": "dns", "open_recursion": True}},
    )
    assert {"UDP-NTP-MONLIST", "UDP-DNS-OPEN-RESOLVER"} <= _ids(fs)


def test_udp_no_amplification_when_not_reflecting():
    fs = _run({"scanner": "udp_scan", "target": "t", "port": 123, "status": "open",
               "data": {"service": "ntp", "monlist_enabled": False}})
    assert not _ids(fs)


# ── cleartext + exposure ─────────────────────────────────────────────────────
def test_telnet_is_high_cleartext():
    fs = _run({"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"})
    hit = next(f for f in fs if f.rule_id == "SVC-TELNET-CLEARTEXT")
    assert hit.severity == F.SEV_HIGH and hit.category == F.CAT_CLEARTEXT


def test_exposed_redis_is_high_exposure_medium_confidence():
    fs = _run({"scanner": "port_scan", "target": "t", "port": 6379, "proto": "tcp", "status": "open"})
    hit = next(f for f in fs if f.rule_id == "SVC-DATASTORE-EXPOSED")
    assert hit.severity == F.SEV_HIGH and hit.confidence == F.CONF_MEDIUM
    assert "Redis" in hit.title


def test_rdp_exposed_medium():
    fs = _run({"scanner": "port_scan", "target": "t", "port": 3389, "proto": "tcp", "status": "open"})
    assert next(f for f in fs if f.rule_id == "SVC-RDP-EXPOSED").severity == F.SEV_MEDIUM


def test_open_filtered_never_raises_exposure():
    # The core anti-false-positive invariant: an unproven port is not an exposure.
    fs = _run({"scanner": "port_scan", "target": "t", "port": 6379, "proto": "tcp",
               "status": "open|filtered"})
    assert not _ids(fs)


def test_closed_port_no_finding():
    fs = _run({"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "closed"})
    assert not _ids(fs)


# ── service-confirmed findings (port is only a hint; behaviour confirms) ─────
def test_build_service_index_extracts_confirmed_services():
    idx = F.build_service_index([
        {"scanner": "service_banner", "target": "t", "port": 7000, "status": "open",
         "data": {"service": "redis", "product": "Redis", "version": "7.0.1"}},
        {"scanner": "service_banner", "target": "t", "port": 80, "status": "open",
         "data": {"service": "http", "product": "nginx"}},
        {"scanner": "service_banner", "target": "t", "port": 9, "status": "open", "data": {}},
        {"scanner": "port_scan", "target": "t", "port": 22, "status": "open"},
    ])
    assert idx[("t", 7000)]["service"] == "redis" and idx[("t", 7000)]["version"] == "7.0.1"
    assert idx[("t", 80)]["service"] == "http"
    assert ("t", 9) not in idx and ("t", 22) not in idx


def test_confirmed_redis_is_high_confidence_even_on_nonstandard_port():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 7000, "proto": "tcp", "status": "open"},
        {"scanner": "service_banner", "target": "t", "port": 7000, "status": "open",
         "data": {"service": "redis", "product": "Redis"}},
    )
    hit = next(f for f in fs if f.rule_id == "SVC-DATASTORE-EXPOSED" and f.port == 7000)
    assert hit.severity == F.SEV_HIGH and hit.confidence == F.CONF_HIGH
    assert "confirm" in hit.evidence.lower() and hit.data["confirmed"] is True


def test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed():
    fs = _run({"scanner": "port_scan", "target": "t", "port": 6379, "proto": "tcp", "status": "open"})
    hit = next(f for f in fs if f.rule_id == "SVC-DATASTORE-EXPOSED")
    assert hit.severity == F.SEV_HIGH and hit.confidence == F.CONF_MEDIUM
    assert "not confirmed" in hit.evidence.lower() and hit.data["confirmed"] is False


def test_confirmed_ftp_cleartext_is_high_confidence():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 21, "proto": "tcp", "status": "open"},
        {"scanner": "service_banner", "target": "t", "port": 21, "status": "open",
         "data": {"service": "ftp", "product": "vsftpd"}},
    )
    assert next(f for f in fs if f.rule_id == "SVC-FTP-CLEARTEXT").confidence == F.CONF_HIGH


def test_confirmed_and_port_hint_do_not_double_report():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 6379, "proto": "tcp", "status": "open"},
        {"scanner": "service_banner", "target": "t", "port": 6379, "status": "open",
         "data": {"service": "redis"}},
    )
    hits = [f for f in fs if f.rule_id == "SVC-DATASTORE-EXPOSED" and f.port == 6379]
    assert len(hits) == 1 and hits[0].confidence == F.CONF_HIGH


# ── web ──────────────────────────────────────────────────────────────────────
def test_dangerous_http_methods_medium():
    fs = _run({"scanner": "web_scan", "target": "t", "port": 80, "status": "open",
               "data": {"dangerous_methods": ["PUT", "DELETE"]}})
    assert next(f for f in fs if f.rule_id == "WEB-DANGEROUS-METHODS").severity == F.SEV_MEDIUM


def test_server_version_disclosure_is_info():
    fs = _run({"scanner": "web_scan", "target": "t", "port": 80, "status": "open",
               "data": {"server": "Apache/2.4.29"}})
    assert next(f for f in fs if f.rule_id == "WEB-SERVER-VERSION-DISCLOSURE").severity == F.SEV_INFO


def test_missing_security_headers_is_low():
    fs = _run({"scanner": "web_scan", "target": "t", "port": 443, "status": "open",
               "data": {"security_headers_missing":
                        ["strict-transport-security", "content-security-policy", "referrer-policy"]}})
    hit = next(f for f in fs if f.rule_id == "WEB-MISSING-SECURITY-HEADERS")
    assert hit.severity == F.SEV_LOW
    # only the high-value headers are counted (referrer-policy ignored)
    assert set(hit.data["missing"]) == {"strict-transport-security", "content-security-policy"}


def test_all_security_headers_present_no_finding():
    fs = _run({"scanner": "web_scan", "target": "t", "port": 443, "status": "open",
               "data": {"security_headers_missing": ["referrer-policy"]}})
    assert "WEB-MISSING-SECURITY-HEADERS" not in _ids(fs)


def test_x_powered_by_disclosure_is_info():
    fs = _run({"scanner": "web_scan", "target": "t", "port": 80, "status": "open",
               "data": {"x_powered_by": "PHP/5.6.40"}})
    assert next(f for f in fs if f.rule_id == "WEB-XPOWEREDBY-DISCLOSURE").severity == F.SEV_INFO


# ── engine invariants ────────────────────────────────────────────────────────
def test_findings_are_deduped_by_rule_target_port():
    dup = {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"}
    fs = _run(dup, dict(dup))
    assert len([f for f in fs if f.rule_id == "SVC-TELNET-CLEARTEXT"]) == 1


def test_findings_sorted_most_severe_first():
    fs = _run(
        {"scanner": "web_scan", "target": "t", "port": 80, "status": "open", "data": {"server": "nginx/1.1"}},
        {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"},
    )
    assert F._SEV_ORDER[fs[0].severity] >= F._SEV_ORDER[fs[-1].severity]


def test_no_finding_carries_a_cve_id():
    fs = _run({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smbv1_enabled": True}})
    assert fs and all("cve" not in f.to_dict() for f in fs)


def test_every_finding_is_evidence_backed():
    fs = _run(
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open", "data": {"smbv1_enabled": True}},
        {"scanner": "snmp_scan", "target": "t", "port": 161, "status": "open", "data": {"community": "public"}},
    )
    assert fs and all(f.evidence and f.data for f in fs)


def test_summarize_counts_by_severity_and_actionable():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 23, "proto": "tcp", "status": "open"},   # high
        {"scanner": "web_scan", "target": "t", "port": 80, "status": "open", "data": {"server": "nginx/1.1"}},  # info
    )
    s = F.summarize(fs)
    assert s["total"] == 2 and s["by_severity"]["high"] == 1 and s["actionable"] == 1


def test_accepts_scanresult_objects_not_just_dicts():
    from main_scripts.scanner_base import ScanResult
    r = ScanResult("smb_scan", "t", port=445, proto="tcp", status="open",
                   data={"smbv1_enabled": True})
    fs = F.run_findings([r])
    assert "SMB-V1-ENABLED" in _ids(fs)
