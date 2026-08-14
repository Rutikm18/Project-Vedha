#!/usr/bin/env python3
"""
ja4x.py — JA4X X.509 certificate fingerprinting (the FoxIO JA4+ suite).

An advanced, research-backed fingerprint of a certificate's STRUCTURE — the
ordered OIDs of its issuer RDNs, subject RDNs and extensions — independent of the
field VALUES. Two certificates minted by the same tooling/CA share a JA4X even
with different names, so it is a strong signal for identifying the software that
generated a cert (including malware C2 frameworks that auto-generate certs) and
for correlating infrastructure across a fleet or across runs.

Why this is the right advanced capability here: the scanner already does the
OLDER active TLS fingerprint (JARM, 2020, `tls_fingerprint.py`). JA4X is the
modern successor and — unlike JARM — needs no extra probing: it is computed from
the certificate `tls_scanner` already collects. Pure, deterministic, offline,
read-only.

Research grounding (arXiv, cs.CR): JA4-family TLS fingerprinting is the current
approach for actor/traffic identification — e.g. arXiv:2602.09606 (2026,
"Detecting Web Bad Bots via TLS Fingerprints", JA4 + gradient boosting) and
arXiv:2410.03817 (2024, TLS-fingerprint feature-expansion + MinHash similarity to
surface unknown-malicious infrastructure). JA4X extends that to the certificate.

Algorithm (interoperable with the FoxIO reference implementation):
  * take three ordered OID lists — issuer RDN OIDs, subject RDN OIDs, extension
    OIDs — in the order they appear in the certificate;
  * hex-encode each OID's DER content octets ('2.5.4.6' -> '550406');
  * for each list: sha256(",".join(hex_oids)).hexdigest()[:12];
    an EMPTY list hashes to the sentinel '000000000000';
  * JA4X = "<issuer12>_<subject12>_<extensions12>".
"""
from __future__ import annotations

import hashlib

_EMPTY = "000000000000"


def oid_to_hex(oid: str) -> str:
    """DER-encode an OID's content octets and hex-encode them.

    '2.5.4.6' -> '550406'; '1.2.840.113549.1.9.1' -> '2a864886f70d010901'.
    First two arcs pack into one octet (40*a + b); the rest are base-128,
    big-endian, with the continuation bit set on every group but the last.
    """
    parts = [int(p) for p in oid.split(".") if p != ""]
    if not parts:
        return ""
    body = bytearray()
    if len(parts) >= 2:
        body.append(40 * parts[0] + parts[1])
        rest = parts[2:]
    else:
        body.append(parts[0])
        rest = []
    for arc in rest:
        if arc < 0:
            raise ValueError(f"negative OID arc: {arc}")
        groups = [arc & 0x7F]           # least-significant 7 bits (no cont bit)
        arc >>= 7
        while arc > 0:
            groups.append((arc & 0x7F) | 0x80)   # more-significant groups get cont bit
            arc >>= 7
        body.extend(reversed(groups))            # emit big-endian
    return body.hex()


def _hash_oids(oids: list[str]) -> str:
    if not oids:
        return _EMPTY
    joined = ",".join(oid_to_hex(o) for o in oids)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]


def ja4x_from_oid_lists(issuer_oids: list[str], subject_oids: list[str],
                        extension_oids: list[str]) -> str:
    """Pure JA4X from the three ordered OID lists (dotted-decimal strings)."""
    return (f"{_hash_oids(issuer_oids)}_{_hash_oids(subject_oids)}_"
            f"{_hash_oids(extension_oids)}")


def ja4x_from_cert(cert) -> str | None:
    """JA4X from a `cryptography` x509 Certificate object. None if unusable."""
    try:
        issuer = [a.oid.dotted_string for a in cert.issuer]
        subject = [a.oid.dotted_string for a in cert.subject]
        exts = [e.oid.dotted_string for e in cert.extensions]
    except Exception:
        return None
    return ja4x_from_oid_lists(issuer, subject, exts)


def ja4x_from_der(der: bytes | None) -> str | None:
    """JA4X from raw DER bytes. `cryptography` is imported lazily so this module
    stays importable — and its pure core testable — without it installed."""
    if not der:
        return None
    try:
        from cryptography import x509
    except Exception:
        return None
    try:
        return ja4x_from_cert(x509.load_der_x509_certificate(der))
    except Exception:
        return None


# ── threat-intel matching (extensible; curated references only) ─────────────
# Map JA4X -> short label. Intentionally small and explicit: a scanner must NOT
# invent malware attributions from thin air. Populate this from a vetted feed;
# what matters here is the match MECHANISM (tested), not a bundled blocklist.
SUSPICIOUS_JA4X: dict[str, str] = {
    # "3b2b1a2c9d4e_...": "example: auto-generated C2 default-profile cert",
}


def match_suspicious(ja4x: str | None) -> str | None:
    """Return a threat-intel label if this JA4X is a known-suspicious fingerprint,
    else None. Matching is exact against the curated registry."""
    if not ja4x:
        return None
    return SUSPICIOUS_JA4X.get(ja4x)
