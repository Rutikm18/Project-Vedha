"""
test_service_posture_rules_v2.py — the P1 service-layer rules that consume facts
the probe already collected but no rule assessed (the silent-false-negative
backlog). Each test drives the real detector + the real detect_posture path.
"""
from __future__ import annotations

import posture_rules as P
from models import Asset, Fact, SourceConfidence


def _fact(scanner: str, data: dict, *, port: int = 0, status: str = "open") -> Fact:
    return Fact(scanner=scanner, target="10.0.0.5", timestamp="2026-09-01T00:00:00Z",
                port=port, proto="tcp", status=status, data=data, evidence=None,
                error=None, source_confidence=SourceConfidence.inferred,
                source_file="corpus.jsonl", source_line=1)


def _asset(*facts: Fact) -> Asset:
    a = Asset(ip="10.0.0.5")
    for f in facts:
        a.add_fact(f)
    return a


def _ids(findings):
    return {f.rule_id for f in findings}


# ── TLS weak key / signature ──────────────────────────────────────────────────
def test_tls_weak_rsa_key_fires():
    ev = P._tls_weak_key(_fact("tls_scan", {"certificate": {
        "public_key_type": "RSA", "public_key_bits": 1024, "subject": "CN=old"}}, port=443))
    assert ev and ev["public_key_bits"] == 1024 and ev["minimum_bits"] == 2048


def test_tls_strong_rsa_key_clean():
    assert P._tls_weak_key(_fact("tls_scan", {"certificate": {
        "public_key_type": "RSA", "public_key_bits": 2048}}, port=443)) is None


def test_tls_strong_ec_key_clean():
    assert P._tls_weak_key(_fact("tls_scan", {"certificate": {
        "public_key_type": "EC", "public_key_bits": 256}}, port=443)) is None


def test_tls_weak_ec_key_fires():
    ev = P._tls_weak_key(_fact("tls_scan", {"certificate": {
        "public_key_type": "ec", "public_key_bits": 160}}, port=443))
    assert ev and ev["minimum_bits"] == 256


def test_tls_degraded_parse_silent():
    # byte-count-only parse: no key fields -> must never accuse
    assert P._tls_weak_key(_fact("tls_scan", {"certificate": {"raw_der_bytes": 900}}, port=443)) is None
    assert P._tls_weak_key(_fact("tls_scan", {"certificate": {
        "public_key_type": "RSA", "public_key_bits": True}}, port=443)) is None


def test_tls_weak_sha1_signature_fires():
    ev = P._tls_weak_sig(_fact("tls_scan", {"certificate": {
        "sig_algorithm": "sha1", "self_signed": False}}, port=443))
    assert ev and ev["weak_hash"] == "sha1"


def test_tls_md5_signature_fires():
    ev = P._tls_weak_sig(_fact("tls_scan", {"certificate": {"sig_algorithm": "md5WithRSAEncryption"}}, port=443))
    assert ev and ev["weak_hash"] == "md5"


def test_tls_sha256_signature_clean():
    assert P._tls_weak_sig(_fact("tls_scan", {"certificate": {"sig_algorithm": "sha256"}}, port=443)) is None


# ── web ────────────────────────────────────────────────────────────────────────
def test_web_dangerous_methods_fires():
    ev = P._web_dangerous_methods(_fact("web_scan", {
        "dangerous_methods": ["PUT", "DELETE"], "allowed_methods": ["GET", "PUT", "DELETE"],
        "url": "http://10.0.0.5/"}, port=80))
    assert ev and "PUT" in ev["dangerous_methods"]


def test_web_no_dangerous_methods_clean():
    assert P._web_dangerous_methods(_fact("web_scan", {"dangerous_methods": []}, port=80)) is None


def test_web_missing_hsts_on_tls_fires():
    ev = P._web_missing_hsts(_fact("web_scan", {
        "tls": True, "security_headers_missing": ["strict-transport-security", "content-security-policy"],
        "url": "https://10.0.0.5/"}, port=443))
    assert ev and ev["missing_header"] == "strict-transport-security"


def test_web_missing_hsts_on_plaintext_clean():
    # not a TLS service -> HSTS is not applicable, must not fire
    assert P._web_missing_hsts(_fact("web_scan", {
        "tls": False, "security_headers_missing": ["strict-transport-security"]}, port=80)) is None


def test_web_hsts_present_clean():
    assert P._web_missing_hsts(_fact("web_scan", {
        "tls": True, "security_headers_missing": ["content-security-policy"]}, port=443)) is None


# ── DNS version disclosure ───────────────────────────────────────────────────
def test_dns_version_disclosure_fires():
    ev = P._dns_version_disclosure(_fact("dns_scan", {
        "dns": True, "version_bind": "9.11.3-1ubuntu1.17", "hostname_bind": "ns1"}, port=53))
    assert ev and ev["version_bind"].startswith("9.11.3")


def test_dns_version_refused_clean():
    assert P._dns_version_disclosure(_fact("dns_scan", {"dns": True, "version_bind": "refused"}, port=53)) is None
    assert P._dns_version_disclosure(_fact("dns_scan", {"dns": True, "version_bind": ""}, port=53)) is None


# ── LDAP anonymous search ────────────────────────────────────────────────────
def test_ldap_anonymous_search_fires():
    ev = P._ldap_anonymous_search(_fact("ldap_scan", {
        "ldap": True, "anonymous_search_allowed": True, "sample_entry_count": 42,
        "default_naming_context": "DC=corp,DC=local", "naming_contexts": ["DC=corp,DC=local"]}, port=389))
    assert ev and ev["sample_entry_count"] == 42


def test_ldap_bind_only_no_search_clean():
    assert P._ldap_anonymous_search(_fact("ldap_scan", {
        "ldap": True, "anonymous_bind": True, "anonymous_search_allowed": False}, port=389)) is None


# ── SNMP amplification ───────────────────────────────────────────────────────
def test_snmp_amplification_fires():
    ev = P._snmp_amplification(_fact("snmp_scan", {"community": "public", "amplification_factor": 11.4}, port=161, status="open"))
    assert ev and ev["amplification_factor"] == 11.4


def test_snmp_low_amplification_clean():
    assert P._snmp_amplification(_fact("snmp_scan", {"community": "public", "amplification_factor": 1.2}, port=161)) is None


def test_snmp_amplification_absent_silent():
    assert P._snmp_amplification(_fact("snmp_scan", {"community": "public"}, port=161)) is None


# ── IoT / mobile / AI ────────────────────────────────────────────────────────
def test_mqtt_unauth_fires():
    ev = P._iot_mqtt_unauth(_fact("iot_scan", {
        "mqtt_connack": True, "unauthenticated_access": True, "return_code_meaning": "Connection Accepted",
        "subscribe_all_granted": True}, port=1883))
    assert ev and ev["subscribe_all_granted"] is True


def test_mqtt_refused_clean():
    assert P._iot_mqtt_unauth(_fact("iot_scan", {
        "mqtt_connack": True, "unauthenticated_access": False, "return_code_meaning": "Refused: Not authorized"}, port=1883)) is None


def test_cwmp_exposed_fires():
    ev = P._iot_cwmp_exposed(_fact("iot_scan", {"cwmp_indicators": True, "server": "RomPager/4.07"}, port=7547))
    assert ev and ev["server"] == "RomPager/4.07"


def test_rtsp_exposed_fires():
    ev = P._iot_rtsp_exposed(_fact("iot_scan", {
        "rtsp_version": "RTSP/1.0", "public_methods": "OPTIONS, DESCRIBE, PLAY", "server": "Hipcam"}, port=554))
    assert ev and "DESCRIBE" in ev["public_methods"]


def test_adb_unauth_shell_fires():
    ev = P._adb_unauth_shell(_fact("mobile_scan", {
        "adb_command": "CNXN", "unauthenticated_shell": True, "adb_version": "0x1000000",
        "note": "NO AUTH"}, port=5555))
    assert ev and ev["adb_version"] == "0x1000000"


def test_adb_auth_required_clean():
    assert P._adb_unauth_shell(_fact("mobile_scan", {
        "adb_command": "AUTH", "unauthenticated_shell": False, "auth_required": True}, port=5555)) is None


def test_mcp_ai_unauth_fires():
    ev = P._mcp_ai_unauth(_fact("mcp_ai_scan", {
        "kind": "ollama", "path": "/api/tags", "unauthenticated_access": True,
        "auth_enforced": False, "model_count": 3}, port=11434))
    assert ev and ev["kind"] == "ollama" and ev["model_count"] == 3


def test_mcp_ai_auth_enforced_clean():
    assert P._mcp_ai_unauth(_fact("mcp_ai_scan", {
        "kind": "mcp", "unauthenticated_access": False, "auth_enforced": True}, port=8080)) is None


# ── end-to-end through detect_posture (state + risk wiring) ───────────────────
def test_detect_posture_wires_new_rules_as_suspected():
    asset = _asset(
        _fact("tls_scan", {"certificate": {"public_key_type": "RSA", "public_key_bits": 1024,
                                           "sig_algorithm": "sha1"}}, port=443),
        _fact("mobile_scan", {"adb_command": "CNXN", "unauthenticated_shell": True}, port=5555),
        _fact("mcp_ai_scan", {"unauthenticated_access": True, "auth_enforced": False, "kind": "ollama"}, port=11434),
    )
    findings = P.detect_posture(asset)
    by_id = {f.rule_id: f for f in findings}
    assert {"POSTURE-TLS-WEAK-KEY", "POSTURE-TLS-WEAK-SIGNATURE",
            "POSTURE-ADB-UNAUTHENTICATED", "POSTURE-AI-ENDPOINT-UNAUTHENTICATED"} <= set(by_id)
    # tls_scan IS in the validated trust tier -> its direct observations are CONFIRMED
    assert by_id["POSTURE-TLS-WEAK-KEY"].state == "confirmed"
    assert by_id["POSTURE-TLS-WEAK-SIGNATURE"].state == "confirmed"
    # mobile_scan / mcp_ai_scan are not validated -> SUSPECTED until they earn it
    assert by_id["POSTURE-ADB-UNAUTHENTICATED"].state == "suspected"
    assert by_id["POSTURE-AI-ENDPOINT-UNAUTHENTICATED"].state == "suspected"
    # the ADB unauth shell is critical-severity
    assert by_id["POSTURE-ADB-UNAUTHENTICATED"].severity == "critical"
