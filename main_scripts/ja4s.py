#!/usr/bin/env python3
"""
ja4s.py — JA4S TLS ServerHello fingerprint (FoxIO JA4+ suite).

The server side of the JA4 TLS fingerprint: how a server RESPONDS to a ClientHello
— the TLS version and cipher it picks, the extensions it returns, and the ALPN it
selects. That selection behaviour is a stable property of the server's TLS stack,
so JA4S identifies the server software / load-balancer / C2 framework and
correlates infrastructure. It is the ServerHello complement to the certificate
fingerprint in `ja4x.py` and the modern successor to the JARM digest this probe
already computes (`tls_fingerprint.py`).

Reuse: the raw ClientHello construction + ServerHello parsing already live in
`tls_fingerprint.py` (`build_client_hello`, `parse_server_hello`). JA4S is computed
from `parse_server_hello`'s output — no new handshake machinery.

Research grounding (arXiv, cs.CR): JA4-family TLS fingerprinting is the current
approach for actor/traffic identification — e.g. arXiv:2602.09606 (2026, bad-bot
detection via JA4) and arXiv:2410.03817 (2024, TLS-fingerprint similarity for
unknown-malicious discovery).

Format (interoperable with the FoxIO reference):
    JA4S = (proto)(tls_ver)(ext_count)(alpn) _ (cipher) _ (sha256(exts)[:12])
      * proto     : 't' (TCP) or 'q' (QUIC)
      * tls_ver   : 13/12/11/10/s3/s2  (negotiated version)
      * ext_count : 2-digit count of ServerHello extensions
      * alpn      : first+last char of the chosen ALPN, or '00'
      * cipher    : 4-hex chosen cipher suite
      * exts hash : sha256 of the extension types (hex, in order, comma-joined),
                    first 12 chars; no extensions -> '000000000000'
    e.g. t130200_1301_234ea6891581
"""
from __future__ import annotations

import hashlib
import struct

_EMPTY = "000000000000"

_TLS_VERSION_STR = {
    0x0304: "13", 0x0303: "12", 0x0302: "11", 0x0301: "10",
    0x0300: "s3", 0x0002: "s2",
}

# A standard, non-GREASE ClientHello for canonical JA4S capture.
_STD_SPEC = {"use_grease": False, "alpn": [b"h2", b"http/1.1"],
             "supported_versions": [0x0304, 0x0303]}

_ALPN_EXT = 0x0010


def _version_str(version: int | None) -> str:
    return _TLS_VERSION_STR.get(version or 0, "00")


def _walk_extensions(ext_blob: bytes):
    """Yield (type, value) for each extension in a ServerHello extensions blob."""
    j = 0
    while j + 4 <= len(ext_blob):
        etype, elen = struct.unpack("!HH", ext_blob[j:j + 4])
        yield etype, ext_blob[j + 4:j + 4 + elen]
        j += 4 + elen


def _ext_types(ext_blob: bytes) -> list[int]:
    return [t for t, _ in _walk_extensions(ext_blob)]


def _selected_alpn(ext_blob: bytes) -> bytes:
    """The single ALPN protocol the server chose (b'' if none)."""
    for etype, val in _walk_extensions(ext_blob):
        if etype == _ALPN_EXT and len(val) >= 3:
            name_len = val[2]
            return val[3:3 + name_len]
    return b""


def _alpn_code(alpn: bytes) -> str:
    if not alpn:
        return "00"
    s = alpn.decode("latin-1", errors="replace")
    return (s[0] + s[-1]) if s else "00"


def ja4s_from_fields(*, protocol: str, version: int | None, cipher: int | None,
                     ext_types: list[int], alpn: bytes = b"") -> str:
    """Pure JA4S from already-extracted ServerHello fields."""
    part_a = (protocol + _version_str(version)
              + f"{min(len(ext_types), 99):02d}" + _alpn_code(alpn))
    part_b = f"{(cipher or 0):04x}"
    if ext_types:
        joined = ",".join(f"{t:04x}" for t in ext_types)
        part_c = hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]
    else:
        part_c = _EMPTY
    return f"{part_a}_{part_b}_{part_c}"


def ja4s_from_parsed(parsed: dict, protocol: str = "t") -> str | None:
    """JA4S from `parse_server_hello`'s output ({version, cipher, extensions})."""
    if not parsed:
        return None
    ext_blob = parsed.get("extensions") or b""
    return ja4s_from_fields(
        protocol=protocol, version=parsed.get("version"), cipher=parsed.get("cipher"),
        ext_types=_ext_types(ext_blob), alpn=_selected_alpn(ext_blob))


def ja4s_from_serverhello(raw: bytes, protocol: str = "t") -> str | None:
    """JA4S from raw ServerHello record bytes (reuses the JARM parser)."""
    from main_scripts.tls_fingerprint import parse_server_hello
    return ja4s_from_parsed(parse_server_hello(raw), protocol=protocol)


def compute_ja4s(host: str, ip: str, port: int, timeout: float = 4.0,
                 protocol: str = "t") -> str | None:
    """Do one standard TLS handshake and compute the server's JA4S. Reuses the
    JARM probe machinery; best-effort (None on any failure). LIVE — verify against
    a real target."""
    from main_scripts.tls_fingerprint import _one_probe
    return ja4s_from_parsed(_one_probe(host, ip, port, _STD_SPEC, timeout),
                            protocol=protocol)


# ── threat-intel matching (extensible; curated references only) ─────────────
SUSPICIOUS_JA4S: dict[str, str] = {
    # "t130200_1301_...": "example: known C2 server-hello profile",
}


def match_suspicious(ja4s: str | None) -> str | None:
    if not ja4s:
        return None
    return SUSPICIOUS_JA4S.get(ja4s)
