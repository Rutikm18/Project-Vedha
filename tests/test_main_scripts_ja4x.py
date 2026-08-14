"""
test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced
capability; FoxIO JA4+ suite, arXiv-grounded).

Pure-logic: OID→DER-hex correctness, JA4X format/determinism/order-sensitivity,
the empty-list sentinel, the cert adapter (via a fake cert, no `cryptography`
needed), an optional real-DER round-trip when `cryptography` is present, and the
JA4X threat-intel finding rule.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from main_scripts import findings as F
from main_scripts import ja4x


# ── oid_to_hex: interoperable DER encoding ───────────────────────────────────
def test_oid_to_hex_known_values():
    assert ja4x.oid_to_hex("2.5.4.6") == "550406"          # countryName
    assert ja4x.oid_to_hex("2.5.4.3") == "550403"          # commonName
    assert ja4x.oid_to_hex("2.5.4.10") == "55040a"         # organizationName
    # multi-byte arcs (base-128) — emailAddress
    assert ja4x.oid_to_hex("1.2.840.113549.1.9.1") == "2a864886f70d010901"


# ── JA4X assembly ────────────────────────────────────────────────────────────
def test_ja4x_format_is_three_12hex_fields():
    j = ja4x.ja4x_from_oid_lists(["2.5.4.6", "2.5.4.3"], ["2.5.4.3"],
                                 ["2.5.29.15", "2.5.29.19"])
    parts = j.split("_")
    assert len(parts) == 3
    assert all(len(p) == 12 and all(c in "0123456789abcdef" for c in p) for p in parts)


def test_empty_list_hashes_to_sentinel():
    j = ja4x.ja4x_from_oid_lists([], [], [])
    assert j == "000000000000_000000000000_000000000000"


def test_ja4x_is_deterministic_and_order_sensitive():
    a = ja4x.ja4x_from_oid_lists(["2.5.4.6", "2.5.4.3"], ["2.5.4.3"], ["2.5.29.19"])
    b = ja4x.ja4x_from_oid_lists(["2.5.4.6", "2.5.4.3"], ["2.5.4.3"], ["2.5.29.19"])
    c = ja4x.ja4x_from_oid_lists(["2.5.4.3", "2.5.4.6"], ["2.5.4.3"], ["2.5.29.19"])
    assert a == b                # deterministic
    assert a != c                # RDN order changes the fingerprint (as JA4X intends)


# ── cert adapter (no `cryptography` needed — fake cert) ──────────────────────
def _fake_cert(issuer, subject, exts):
    mk = lambda o: SimpleNamespace(oid=SimpleNamespace(dotted_string=o))
    return SimpleNamespace(issuer=[mk(o) for o in issuer],
                           subject=[mk(o) for o in subject],
                           extensions=[mk(o) for o in exts])


def test_ja4x_from_cert_matches_pure_core():
    issuer, subject, exts = ["2.5.4.6", "2.5.4.3"], ["2.5.4.3"], ["2.5.29.15"]
    assert ja4x.ja4x_from_cert(_fake_cert(issuer, subject, exts)) == \
        ja4x.ja4x_from_oid_lists(issuer, subject, exts)


def test_ja4x_from_cert_handles_garbage():
    assert ja4x.ja4x_from_cert(object()) is None
    assert ja4x.ja4x_from_der(None) is None
    assert ja4x.ja4x_from_der(b"not-a-cert") is None


# ── optional real-DER round-trip (only if cryptography is installed) ─────────
def test_real_self_signed_cert_round_trip():
    crypto = pytest.importorskip("cryptography")
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    import datetime as _dt

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "lab.local")])
    cert = (x509.CertificateBuilder()
            .subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(_dt.datetime(2020, 1, 1))
            .not_valid_after(_dt.datetime(2030, 1, 1))
            .sign(key, hashes.SHA256()))
    der = cert.public_bytes(crypto.hazmat.primitives.serialization.Encoding.DER)
    j = ja4x.ja4x_from_der(der)
    assert j and len(j.split("_")) == 3 and j == ja4x.ja4x_from_cert(cert)


# ── threat-intel matching + finding rule ─────────────────────────────────────
def test_match_suspicious_registry():
    assert ja4x.match_suspicious(None) is None
    assert ja4x.match_suspicious("nope_nope_nope") is None
    ja4x.SUSPICIOUS_JA4X["dead_beef_cafe"] = "unit-test C2 profile"
    try:
        assert ja4x.match_suspicious("dead_beef_cafe") == "unit-test C2 profile"
    finally:
        ja4x.SUSPICIOUS_JA4X.pop("dead_beef_cafe", None)


def test_suspicious_fingerprint_finding_fires_only_on_match():
    ja4x.SUSPICIOUS_JA4X["aaaa_bbbb_cccc"] = "unit-test tooling"
    try:
        hit = F.run_findings([{
            "scanner": "tls_scan", "target": "10.0.0.9", "port": 443, "status": "open",
            "data": {"accepted_versions": ["TLSv1.2"],
                     "certificate": {"ja4x": "aaaa_bbbb_cccc"}}}])
        f = next(x for x in hit if x.rule_id == "TLS-SUSPICIOUS-CERT-FINGERPRINT")
        assert f.severity == F.SEV_HIGH and f.data["match"] == "unit-test tooling"
        # a non-matching JA4X raises no fingerprint finding
        miss = F.run_findings([{
            "scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
            "data": {"accepted_versions": ["TLSv1.2"],
                     "certificate": {"ja4x": "1111_2222_3333"}}}])
        assert "TLS-SUSPICIOUS-CERT-FINGERPRINT" not in {x.rule_id for x in miss}
    finally:
        ja4x.SUSPICIOUS_JA4X.pop("aaaa_bbbb_cccc", None)


def test_self_signed_finding_carries_ja4x_for_correlation():
    fs = F.run_findings([{
        "scanner": "tls_scan", "target": "t", "port": 443, "status": "open",
        "data": {"accepted_versions": ["TLSv1.2"],
                 "certificate": {"self_signed": True, "ja4x": "1111_2222_3333"}}}])
    ss = next(x for x in fs if x.rule_id == "TLS-CERT-SELF-SIGNED")
    assert ss.data["ja4x"] == "1111_2222_3333"
