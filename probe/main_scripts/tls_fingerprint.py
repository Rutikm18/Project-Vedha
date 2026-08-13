"""
tls_fingerprint.py — active TLS server fingerprint (Tier 2.3, JARM methodology).

WHAT: sends a matrix of deliberately-varied TLS ClientHellos and hashes how the
server responds (which version + cipher it picks, and the extensions it returns).
Because a server's selection behaviour across many odd ClientHellos is a stable
property of its TLS stack + configuration, the resulting fingerprint clusters
identical deployments and is a strong, stable host-identity signal for
internet-facing hosts that have no MAC (feeds delta_scanner's identity model).

METHOD: this follows the JARM technique (Salesforce, 2020) — 10 probes varying
TLS version, cipher list + ordering, GREASE, ALPN and extension order — and emits
a JARM-shaped 62-char fuzzy hash: 30 chars encoding the (cipher,version) chosen
for each of the 10 probes ("000" = no reply) + a 32-char truncated SHA-256 of the
cumulative server extensions. An all-silent target hashes to 62 zeros.

NOTE ON PARITY: the raw-TLS machinery (ClientHello build, ServerHello parse) is
verified against a live server; the digest layout is JARM-style. Exact
byte-for-byte parity with the reference JARM database should be validated against
the upstream tool before relying on cross-database matches.

COLLECTION ONLY: TLS handshakes are initiated and the ServerHello is read; no
data is sent post-handshake, nothing is exploited.
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, resolve, setup_logging, base_argparser, main_entrypoint, LOG,
)

# A stable, ordered cipher list (2-byte suite codes). Position in this list gives
# each cipher a compact code in the fingerprint. (Common TLS 1.2/1.3 suites.)
CIPHER_LIST: list[int] = [
    0x1301, 0x1302, 0x1303,                          # TLS 1.3
    0xC02B, 0xC02F, 0xC02C, 0xC030,                  # ECDHE-ECDSA/RSA AES-GCM
    0xCCA9, 0xCCA8,                                   # ECDHE CHACHA20-POLY1305
    0xC009, 0xC013, 0xC00A, 0xC014,                  # ECDHE AES-CBC
    0x009C, 0x009D, 0x002F, 0x0035,                  # RSA AES (GCM + CBC)
    0x000A,                                          # 3DES (SWEET32) — legacy probe
]

# GREASE values (RFC 8701) — advertise deliberate unknowns to detect intolerance.
_GREASE = [0x0A0A, 0x1A1A, 0x2A2A, 0x3A3A, 0x8A8A]

# TLS content types / handshake types
_CT_HANDSHAKE = 0x16
_HS_CLIENT_HELLO = 0x01
_HS_SERVER_HELLO = 0x02


# ── ClientHello construction ──────────────────────────────────────────────────

def _ext(ext_type: int, body: bytes) -> bytes:
    return struct.pack("!HH", ext_type, len(body)) + body


def _sni_extension(hostname: str) -> bytes:
    name = hostname.encode()
    server_name = b"\x00" + struct.pack("!H", len(name)) + name   # type host_name
    lst = struct.pack("!H", len(server_name)) + server_name
    return _ext(0x0000, lst)


def _supported_versions_ext(versions: list[int]) -> bytes:
    body = bytes([len(versions) * 2]) + b"".join(struct.pack("!H", v) for v in versions)
    return _ext(0x002B, body)


def _key_share_ext() -> bytes:
    # x25519 (group 29) — any 32 bytes is a valid X25519 public key. TLS 1.3
    # ClientHellos that offer 1.3 MUST carry key_share or the server replies with
    # a missing_extension alert instead of a ServerHello.
    entry = struct.pack("!HH", 29, 32) + os.urandom(32)
    return _ext(0x0033, struct.pack("!H", len(entry)) + entry)


def build_client_hello(hostname: str, ciphers: list[int], *,
                       client_version: int = 0x0303, use_grease: bool = False,
                       alpn: list[bytes] | None = None,
                       supported_versions: list[int] | None = None,
                       reverse_ciphers: bool = False) -> bytes:
    """Build a complete TLS ClientHello record (record layer + handshake)."""
    suites = list(ciphers)
    if reverse_ciphers:
        suites = list(reversed(suites))
    if use_grease:
        suites = [_GREASE[0]] + suites
    cipher_bytes = b"".join(struct.pack("!H", c) for c in suites)

    random_bytes = os.urandom(32)
    session_id = os.urandom(32)                      # non-empty (TLS 1.3 style)

    # Extensions
    exts = _sni_extension(hostname)
    # supported_groups: x25519(29), secp256r1(23), secp384r1(24)
    groups = [29, 23, 24]
    if use_grease:
        groups = [_GREASE[1]] + groups
    exts += _ext(0x000A, struct.pack("!H", len(groups) * 2)
                 + b"".join(struct.pack("!H", g) for g in groups))
    # ec_point_formats: uncompressed
    exts += _ext(0x000B, b"\x01\x00")
    # signature_algorithms (common set)
    sigs = [0x0403, 0x0804, 0x0401, 0x0503, 0x0805, 0x0501, 0x0806, 0x0601]
    exts += _ext(0x000D, struct.pack("!H", len(sigs) * 2)
                 + b"".join(struct.pack("!H", s) for s in sigs))
    if supported_versions:
        exts += _supported_versions_ext(supported_versions)
        if 0x0304 in supported_versions:
            exts += _key_share_ext()
    if alpn:
        proto_list = b"".join(bytes([len(p)]) + p for p in alpn)
        exts += _ext(0x0010, struct.pack("!H", len(proto_list)) + proto_list)

    body = (struct.pack("!H", client_version) + random_bytes +
            bytes([len(session_id)]) + session_id +
            struct.pack("!H", len(cipher_bytes)) + cipher_bytes +
            b"\x01\x00" +                             # compression: null
            struct.pack("!H", len(exts)) + exts)

    handshake = bytes([_HS_CLIENT_HELLO]) + struct.pack("!I", len(body))[1:] + body
    return bytes([_CT_HANDSHAKE]) + b"\x03\x01" + struct.pack("!H", len(handshake)) + handshake


# ── ServerHello parsing ───────────────────────────────────────────────────────

def parse_server_hello(data: bytes) -> dict | None:
    """Parse the negotiated version + cipher + extensions from a ServerHello."""
    if len(data) < 7 or data[0] != _CT_HANDSHAKE:
        return None
    rec_len = struct.unpack("!H", data[3:5])[0]
    hs = data[5:5 + rec_len]
    if len(hs) < 4 or hs[0] != _HS_SERVER_HELLO:
        return None
    hs_len = struct.unpack("!I", b"\x00" + hs[1:4])[0]
    body = hs[4:4 + hs_len]
    if len(body) < 35:
        return None
    legacy_version = struct.unpack("!H", body[0:2])[0]
    idx = 2 + 32                                     # skip version + random
    sid_len = body[idx]; idx += 1 + sid_len
    if idx + 3 > len(body):
        return None
    cipher = struct.unpack("!H", body[idx:idx + 2])[0]; idx += 2
    idx += 1                                         # compression method
    version = legacy_version
    extensions = b""
    if idx + 2 <= len(body):
        ext_total = struct.unpack("!H", body[idx:idx + 2])[0]; idx += 2
        extensions = body[idx:idx + ext_total]
        # supported_versions (43) in ServerHello carries the real TLS 1.3 version.
        j = 0
        while j + 4 <= len(extensions):
            etype, elen = struct.unpack("!HH", extensions[j:j + 4])
            eval_ = extensions[j + 4:j + 4 + elen]
            if etype == 43 and len(eval_) >= 2:
                version = struct.unpack("!H", eval_[:2])[0]
            j += 4 + elen
    return {"version": version, "cipher": cipher, "extensions": extensions}


# ── fingerprint digest ────────────────────────────────────────────────────────

def version_code(version: int | None) -> str:
    return {0x0301: "1", 0x0302: "2", 0x0303: "3", 0x0304: "4"}.get(version, "0")


def cipher_code(cipher: int | None) -> str:
    """2-char code from the cipher's position in CIPHER_LIST ('00' if unknown)."""
    if cipher in CIPHER_LIST:
        return format(CIPHER_LIST.index(cipher) + 1, "02x")
    return "00"


def _server_ext_types(raw: bytes) -> bytes:
    """
    Concatenate the ServerHello extension TYPE codes (2 bytes each). We hash types,
    not raw extension bytes, because values like the TLS 1.3 key_share are
    ephemeral (random per handshake) and would otherwise break determinism, while
    the set/order of extension types is a stable property of the server's stack.
    """
    out = b""
    j = 0
    while j + 4 <= len(raw):
        etype, elen = struct.unpack("!HH", raw[j:j + 4])
        out += struct.pack("!H", etype)
        j += 4 + elen
    return out


def jarm_style_digest(results: list[dict | None]) -> str:
    """
    JARM-shaped 62-char fuzzy hash: 3 chars per probe (cipher[2] + version[1]),
    then a 32-char truncated SHA-256 of the cumulative ServerHello extension TYPES.
    All-None -> 62 zeros.
    """
    part1 = "".join(
        (cipher_code(r["cipher"]) + version_code(r["version"])) if r else "000"
        for r in results)
    ext_blob = b"".join(_server_ext_types(r["extensions"] or b"")
                        for r in results if r)
    if not ext_blob:
        part2 = "0" * 32
    else:
        part2 = hashlib.sha256(ext_blob).hexdigest()[:32]
    return part1 + part2


# ── probe matrix (JARM-style: vary version/cipher-order/GREASE/ALPN) ──────────

def _probe_specs() -> list[dict]:
    h2 = [b"h2", b"http/1.1"]
    return [
        {"client_version": 0x0303, "supported_versions": [0x0304, 0x0303]},
        {"client_version": 0x0303, "supported_versions": [0x0304, 0x0303],
         "reverse_ciphers": True},
        {"client_version": 0x0303, "supported_versions": [0x0304, 0x0303],
         "use_grease": True, "alpn": h2},
        {"client_version": 0x0303, "supported_versions": [0x0303]},
        {"client_version": 0x0303, "supported_versions": [0x0303],
         "reverse_ciphers": True},
        {"client_version": 0x0302, "supported_versions": None},
        {"client_version": 0x0301, "supported_versions": None},
        {"client_version": 0x0303, "supported_versions": [0x0304],
         "alpn": [b"http/1.1"]},
        {"client_version": 0x0303, "supported_versions": [0x0304, 0x0303],
         "use_grease": True, "reverse_ciphers": True},
        {"client_version": 0x0303, "supported_versions": [0x0303, 0x0302, 0x0301]},
    ]


def _recv_first_record(sock) -> bytes:
    """Read exactly the first TLS record (the ServerHello or an alert) and stop —
    never block waiting for bytes that won't come until the peer's handshake
    timeout, which is what made naive reads pathologically slow."""
    data = b""
    while len(data) < 5:
        chunk = sock.recv(4096)
        if not chunk:
            return data
        data += chunk
    rec_len = struct.unpack("!H", data[3:5])[0]
    total = 5 + rec_len
    while len(data) < total:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data


def _one_probe(host: str, ip: str, port: int, spec: dict, timeout: float) -> dict | None:
    """Send one crafted ClientHello, read + parse the ServerHello. Sync."""
    hello = build_client_hello(host, CIPHER_LIST, **spec)
    try:
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(hello)
            data = _recv_first_record(sock)
    except (OSError, socket.timeout):
        return None
    return parse_server_hello(data)


def fingerprint_host(host: str, ip: str, port: int, timeout: float) -> tuple[str, list]:
    """Run all probes and return (62-char digest, per-probe results)."""
    results = [_one_probe(host, ip, port, spec, timeout) for spec in _probe_specs()]
    return jarm_style_digest(results), results


# ── scanner ───────────────────────────────────────────────────────────────────

class TLSFingerprintScanner(BaseScanner):
    name = "tls_fingerprint"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or [443]

    async def _scan_port(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                family, sockaddr = resolve(target, port, proto="tcp")
            except OSError:
                return None
            ip = sockaddr[0]
            digest, results = await loop.run_in_executor(
                None, fingerprint_host, target, ip, port, self.timeout)
        if digest == "0" * 62:
            return None                              # no TLS here / all silent
        responded = sum(1 for r in results if r)
        return ScanResult(
            self.name, target, port=port, proto="tcp", status="open",
            data={"tls_fingerprint": digest, "probes_answered": responded},
            evidence=f"tls fingerprint {digest} ({responded}/10 probes answered)")

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return [r for r in await asyncio.gather(*tasks) if r is not None]


def main() -> None:
    parser = base_argparser("Active TLS fingerprint (JARM methodology)")
    parser.add_argument("-p", "--ports", default=None,
                        help="TLS ports (default: 443)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else [443]
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = TLSFingerprintScanner(scope, rate=args.rate,
                                        concurrency=args.concurrency,
                                        timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
