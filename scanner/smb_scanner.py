"""
smb_scanner.py — detect which SMB dialects a host supports.

METHOD (collection only): we perform SMB protocol NEGOTIATION, nothing more.
  * Send an SMBv1 SMB_COM_NEGOTIATE listing the legacy "NT LM 0.12" dialect.
    A valid SMBv1 negotiate response = SMBv1 is ENABLED on this host (a fact
    worth recording; legacy SMBv1 is widely deprecated).
  * Send an SMB2 NEGOTIATE. A response = SMB2/3 supported.
We only read the negotiate response. We do NOT authenticate, do NOT access
shares, do NOT exploit anything (no MS17-010 trigger). This is pure capability
detection — equivalent to nmap's smb-protocols, hand-rolled so output is yours.

NOTE: raw SMB framing is fiddly; for production-grade reliability you may prefer
nmap_wrapper.py (smb-protocols NSE). This module is intentionally minimal and
clearly scoped so you can measure its accuracy against nmap.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    resolve, resolve_candidates, resolve_ip_candidates,
    setup_logging, base_argparser, main_entrypoint,
)


def _netbios_session(payload: bytes) -> bytes:
    # Direct-hosted SMB over TCP/445 uses a 4-byte length prefix (NBT session).
    return struct.pack(">I", len(payload)) + payload


def parse_smb2_security_mode(response: bytes | None) -> dict:
    """Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.

    Wire layout (including the 4-byte Direct-TCP/NBT transport header):
        abs 4    ProtocolId          b"\\xfeSMB"
        abs 12   Status (u32)        0 on a successful response
        abs 16   Command (u16)       0 = NEGOTIATE
        abs 68   body StructureSize  65 on a successful NEGOTIATE
        abs 70   SecurityMode (u16)
        abs 72   DialectRevision (u16)

    An SMB2 *error* response (e.g. STATUS_INVALID_PARAMETER, which Windows returns
    when 3.1.1 is offered without a preauth-integrity context) reuses the header
    but its body StructureSize is 9 and it carries NO SecurityMode/DialectRevision.
    Reading offsets 70/72 out of that error body produced the confirmed bug
    (signing=false, negotiated_dialect 0x0000). We therefore validate that the
    response is a genuine, successful NEGOTIATE before trusting those fields, and
    we NEVER fabricate signing/dialect from anything else. Read-only.
    """
    if not response or len(response) < 74 or response[4:8] != b"\xfeSMB":
        return {"signing_parsed": False, "reason": "no_smb2_header",
                "negotiated_dialect": None}
    status = struct.unpack_from("<I", response, 12)[0]        # SMB2 header Status
    command = struct.unpack_from("<H", response, 16)[0]       # SMB2 header Command
    body_structure_size = struct.unpack_from("<H", response, 68)[0]
    if command != 0x0000 or status != 0x00000000 or body_structure_size != 65:
        # Not a successful NEGOTIATE — do NOT invent signing/dialect from it.
        return {
            "signing_parsed": False,
            "reason": "not_a_successful_negotiate",
            "smb2_status": f"0x{status:08x}",
            "smb2_command": command,
            "body_structure_size": body_structure_size,
            "negotiated_dialect": None,
        }
    security_mode = struct.unpack_from("<H", response, 70)[0]
    dialect = struct.unpack_from("<H", response, 72)[0]
    signing_supported = bool(security_mode & 0x0001)   # SMB2_NEGOTIATE_SIGNING_ENABLED
    signing_required = bool(security_mode & 0x0002)    # SMB2_NEGOTIATE_SIGNING_REQUIRED
    return {
        "signing_parsed": True,
        # Protocol-precise names (Step 13): what the negotiation actually exposed,
        # distinct from the host's configured EnableSecuritySignature setting.
        "signing_supported": signing_supported,
        "signing_required": signing_required,
        # Deprecated ambiguous alias, retained for backward compatibility.
        "signing_enabled": signing_supported,
        "negotiated_dialect": f"0x{dialect:04x}",
        "security_mode_raw": f"0x{security_mode:04x}",
    }


# ── SMB2 SESSION_SETUP → NTLMSSP Type-2 → exact Windows build ──────────────────
# A pre-auth SMB2 SESSION_SETUP carrying an NTLMSSP NEGOTIATE (Type-1) makes the
# server answer with an NTLMSSP CHALLENGE (Type-2). When the client sets
# NEGOTIATE_VERSION, Windows fills the CHALLENGE's 8-byte Version field (MS-NLMP
# 2.2.2.10) at fixed offset 48 with its real major/minor/BUILD. That build number
# is authoritative — it names the exact release (26100 = Win11 24H2) far more
# precisely than a TTL heuristic — and it is obtained with NO credentials and NO
# authentication (the exchange is the pre-auth handshake). Read-only.
NTLMSSP_SIG = b"NTLMSSP\x00"
NTLMSSP_NEGOTIATE_VERSION = 0x02000000
_SPNEGO_OID = bytes.fromhex("06062b0601050502")            # 1.3.6.1.5.5.2
_NTLMSSP_OID = bytes.fromhex("060a2b06010401823702020a")   # 1.3.6.1.4.1.311.2.2.10


def _der_len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return bytes([0x80 | len(b)]) + b


def _der(tag: int, val: bytes) -> bytes:
    return bytes([tag]) + _der_len(len(val)) + val


def build_ntlmssp_negotiate() -> bytes:
    """NTLMSSP NEGOTIATE (Type-1). Sets NEGOTIATE_VERSION so the server discloses
    its own Version block in the CHALLENGE. No domain/workstation supplied."""
    flags = (0x00000001 |   # UNICODE
             0x00000004 |   # REQUEST_TARGET
             0x00000200 |   # NTLM
             0x00008000 |   # ALWAYS_SIGN
             0x00080000 |   # EXTENDED_SESSIONSECURITY
             0x20000000 |   # 128-bit
             NTLMSSP_NEGOTIATE_VERSION |
             0x80000000)    # 56-bit
    version = bytes([10, 0]) + struct.pack("<H", 0) + b"\x00\x00\x00" + b"\x0f"
    return (NTLMSSP_SIG + struct.pack("<I", 1) + struct.pack("<I", flags) +
            struct.pack("<HHI", 0, 0, 0) +      # DomainName fields (empty)
            struct.pack("<HHI", 0, 0, 0) +      # Workstation fields (empty)
            version)


def _spnego_init(ntlm_type1: bytes) -> bytes:
    """Wrap an NTLMSSP Type-1 in a minimal SPNEGO NegTokenInit (GSS-API)."""
    mech_types = _der(0xA0, _der(0x30, _NTLMSSP_OID))       # [0] SEQ OF mechType
    mech_token = _der(0xA2, _der(0x04, ntlm_type1))         # [2] OCTET STRING
    neg_init = _der(0xA0, _der(0x30, mech_types + mech_token))
    return _der(0x60, _SPNEGO_OID + neg_init)               # [APPLICATION 0]


def windows_release_from_build(major: int, minor: int, build: int) -> dict:
    """Map an NT major.minor.build to a friendly release. Client and server share
    some builds (26100 = Win11 24H2 AND Server 2025); we return the client name and
    surface the server alternative rather than guessing the SKU here."""
    if major == 10 and minor == 0:
        client = {26100: "Windows 11 24H2", 22631: "Windows 11 23H2",
                  22621: "Windows 11 22H2", 22000: "Windows 11 21H2",
                  19045: "Windows 10 22H2", 19044: "Windows 10 21H2",
                  19043: "Windows 10 21H1", 19042: "Windows 10 20H2",
                  19041: "Windows 10 2004", 18363: "Windows 10 1909",
                  17763: "Windows 10 1809", 16299: "Windows 10 1709",
                  15063: "Windows 10 1703", 10240: "Windows 10 1507"}
        server = {26100: "Windows Server 2025", 20348: "Windows Server 2022",
                  17763: "Windows Server 2019", 14393: "Windows Server 2016"}
        if build in client:
            out = {"os_release": client[build], "os_confidence": 0.97}
            if build in server:
                out["os_release_alt"] = server[build]   # SKU disambiguates client/server
            return out
        if build in server:
            return {"os_release": server[build], "os_confidence": 0.9}
        if build >= 22000:
            return {"os_release": f"Windows 11 (build {build})", "os_confidence": 0.85}
        return {"os_release": f"Windows 10 (build {build})", "os_confidence": 0.85}
    legacy = {(6, 3): "Windows 8.1 / Server 2012 R2",
              (6, 2): "Windows 8 / Server 2012",
              (6, 1): "Windows 7 / Server 2008 R2",
              (6, 0): "Windows Vista / Server 2008",
              (5, 2): "Windows XP x64 / Server 2003", (5, 1): "Windows XP"}
    if (major, minor) in legacy:
        return {"os_release": legacy[(major, minor)], "os_confidence": 0.75}
    return {"os_release": f"Windows {major}.{minor} (build {build})",
            "os_confidence": 0.6}


def parse_ntlm_challenge(blob: bytes) -> dict | None:
    """Parse an NTLMSSP CHALLENGE (Type-2) out of any containing buffer (SPNEGO or
    raw). Returns the server name and — when the Version field is present — the
    exact major/minor/build. Returns None if no CHALLENGE is present."""
    i = blob.find(NTLMSSP_SIG)
    if i < 0:
        return None
    msg = blob[i:]
    if len(msg) < 48 or struct.unpack_from("<I", msg, 8)[0] != 2:   # MessageType == 2
        return None
    flags = struct.unpack_from("<I", msg, 20)[0]
    out: dict = {"ntlm_challenge": True, "negotiate_flags": f"0x{flags:08x}"}
    tn_len = struct.unpack_from("<H", msg, 12)[0]
    tn_off = struct.unpack_from("<I", msg, 16)[0]
    if tn_len and tn_off + tn_len <= len(msg):
        out["target_name"] = msg[tn_off:tn_off + tn_len].decode("utf-16-le", "replace")
    if (flags & NTLMSSP_NEGOTIATE_VERSION) and len(msg) >= 56:
        major, minor = msg[48], msg[49]
        build = struct.unpack_from("<H", msg, 50)[0]
        out.update({"os_major": major, "os_minor": minor, "os_build": build,
                    "ntlm_revision": msg[55],
                    "os_version": f"{major}.{minor}.{build}",
                    "method": "smb2_ntlm_version"})
        out.update(windows_release_from_build(major, minor, build))
    return out


def _smb2_session_setup(security_blob: bytes) -> bytes:
    """SMB2 SESSION_SETUP request (MessageId 1, SessionId 0) carrying `security_blob`."""
    header = (b"\xfeSMB" + struct.pack("<H", 64) + b"\x00" * 2 +   # structsize, creditcharge
              b"\x00" * 4 +                                        # status
              struct.pack("<H", 0x0001) +                          # command SESSION_SETUP
              struct.pack("<H", 1) +                               # credit request
              b"\x00" * 4 +                                        # flags
              b"\x00" * 4 +                                        # next command
              struct.pack("<Q", 1) +                               # message id
              b"\x00" * 4 +                                        # reserved
              b"\x00" * 4 +                                        # tree id
              b"\x00" * 8 +                                        # session id (0 = first)
              b"\x00" * 16)                                        # signature
    sec_off = 64 + 24                                              # header + fixed body
    body = (struct.pack("<H", 25) +                                # structure size
            b"\x00" +                                              # flags
            b"\x01" +                                              # security mode (signing on)
            b"\x00" * 4 +                                          # capabilities
            b"\x00" * 4 +                                          # channel
            struct.pack("<H", sec_off) +                          # security buffer offset
            struct.pack("<H", len(security_blob)) +               # security buffer length
            b"\x00" * 8 +                                          # previous session id
            security_blob)
    return header + body


def _smb1_negotiate() -> bytes:
    # SMBv1 header: 0xFF 'SMB' + command 0x72 (NEGOTIATE) + zeroed fields.
    header = b"\xffSMB" + b"\x72" + b"\x00" * 4 + b"\x18\x53\xc8" + \
             b"\x00" * 2 + b"\x00" * 8 + b"\x00" * 2 + b"\x00" * 2 + \
             b"\x00" * 2 + b"\x00" * 2 + b"\x00" * 2
    # Dialect list (each: 0x02 + ascii name + null). Include legacy NT LM 0.12.
    dialects = b"".join(
        b"\x02" + d + b"\x00" for d in (
            b"PC NETWORK PROGRAM 1.0",
            b"LANMAN1.0",
            b"Windows for Workgroups 3.1a",
            b"LM1.2X002",
            b"LANMAN2.1",
            b"NT LM 0.12",
        )
    )
    body = b"\x00" + struct.pack("<H", len(dialects)) + dialects  # wordcount, bytecount
    return header + body


def _align8(b: bytes) -> bytes:
    """Pad to the 8-byte boundary MS-SMB2 requires between negotiate contexts."""
    return b + b"\x00" * ((-len(b)) % 8)


def _preauth_integrity_context() -> bytes:
    """SMB2_PREAUTH_INTEGRITY_CAPABILITIES (MS-SMB2 2.2.3.1.1): mandatory for any
    client that offers 3.1.1. Advertises SHA-512 with a random 32-byte salt."""
    salt = os.urandom(32)
    data = (struct.pack("<H", 1) +          # HashAlgorithmCount
            struct.pack("<H", len(salt)) +  # SaltLength
            struct.pack("<H", 0x0001) +     # SHA-512
            salt)
    return struct.pack("<H", 0x0001) + struct.pack("<H", len(data)) + b"\x00" * 4 + data


def _encryption_context() -> bytes:
    """SMB2_ENCRYPTION_CAPABILITIES (MS-SMB2 2.2.3.1.2): offer AES-128-GCM/CCM so
    the server's response reveals its negotiated cipher (EncryptData capability)."""
    ciphers = (0x0002, 0x0001)              # AES-128-GCM, AES-128-CCM
    data = struct.pack("<H", len(ciphers)) + b"".join(struct.pack("<H", c) for c in ciphers)
    return struct.pack("<H", 0x0002) + struct.pack("<H", len(data)) + b"\x00" * 4 + data


def _smb2_negotiate() -> bytes:
    # SMB2 header (64 bytes) with NEGOTIATE command (0x0000).
    proto = b"\xfeSMB"
    structure_size = struct.pack("<H", 64)
    header = (proto + structure_size + b"\x00" * 2 +    # credit charge
              b"\x00" * 4 +                              # status
              struct.pack("<H", 0x0000) +               # command NEGOTIATE
              b"\x00" * 2 +                              # credit request
              b"\x00" * 4 +                              # flags
              b"\x00" * 4 +                              # next command
              b"\x00" * 8 +                              # message id
              b"\x00" * 4 +                              # reserved
              b"\x00" * 4 +                              # tree id
              b"\x00" * 8 +                              # session id
              b"\x00" * 16)                              # signature
    # Offer the FULL dialect array incl. 3.1.1. MS-SMB2 3.3.5.4: the server selects
    # the GREATEST common dialect, so omitting 3.1.1 (as before) forced modern hosts
    # down to 3.0.2 — an under-report. 3.1.1 MUST carry a preauth-integrity context
    # (else STATUS_INVALID_PARAMETER), so we append it plus an encryption context.
    dialects = [0x0202, 0x0210, 0x0300, 0x0302, 0x0311]
    client_guid = os.urandom(16)
    dialect_bytes = b"".join(struct.pack("<H", d) for d in dialects)

    # NegotiateContextOffset is measured from the SMB2 header start and must be
    # 8-byte aligned: header(64) + fixed body(36) + dialects, rounded up.
    dialects_end = 64 + 36 + len(dialect_bytes)
    pad = (-dialects_end) % 8
    neg_ctx_offset = dialects_end + pad
    contexts = _align8(_preauth_integrity_context()) + _encryption_context()

    body = (struct.pack("<H", 36) +                      # structure size
            struct.pack("<H", len(dialects)) +           # dialect count
            struct.pack("<H", 0x0001) +                  # security mode (signing enabled)
            b"\x00" * 2 +                                # reserved
            b"\x00" * 4 +                                # capabilities
            client_guid +                                # client guid
            struct.pack("<I", neg_ctx_offset) +          # NegotiateContextOffset
            struct.pack("<H", 2) +                       # NegotiateContextCount
            b"\x00" * 2 +                                # Reserved2
            dialect_bytes + b"\x00" * pad + contexts)
    return header + body


def _recv_smb_frame(sock: socket.socket) -> bytes | None:
    """Read one length-prefixed (Direct-TCP/NBT) SMB frame in full, STRIPPING the
    4-byte NBT prefix (so the returned bytes start at the SMB2 ProtocolId)."""
    hdr = b""
    while len(hdr) < 4:
        chunk = sock.recv(4 - len(hdr))
        if not chunk:
            return None
        hdr += chunk
    length = struct.unpack(">I", hdr)[0] & 0x00FFFFFF
    if length == 0 or length > 0x20000:                # sanity bound (128 KiB)
        return None
    buf = b""
    while len(buf) < length:
        chunk = sock.recv(length - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def ntlm_os_build(ip: str, port: int = 445, timeout: float = 5.0) -> dict:
    """Pre-auth SMB2 NEGOTIATE → SESSION_SETUP → parse the NTLMSSP CHALLENGE Version
    for the exact Windows build. Shared by SMBScanner and os_fingerprint so there is
    ONE implementation. Best-effort: any failure → {}. Read-only, unauthenticated."""
    try:
        sock = socket.create_connection((ip, port), timeout=timeout)
    except OSError:
        return {}
    sock.settimeout(timeout)
    try:
        sock.sendall(_netbios_session(_smb2_negotiate()))
        neg = _recv_smb_frame(sock)
        if not neg or neg[:4] != b"\xfeSMB":           # header at offset 0 (NBT stripped)
            return {}
        sock.sendall(_netbios_session(_smb2_session_setup(_spnego_init(build_ntlmssp_negotiate()))))
        resp = _recv_smb_frame(sock)
        if not resp:
            return {}
        return parse_ntlm_challenge(resp) or {}
    except OSError:
        return {}
    finally:
        sock.close()


class SMBScanner(BaseScanner):
    name = "smb_scan"

    def __init__(self, *args, port: int = 445, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = port

    def _negotiate(self, target: str, payload: bytes) -> bytes | None:
        """SMB negotiate against the first address that actually answers.

        Walks every resolved family rather than only getaddrinfo's first result:
        on a dual-stack host whose AAAA sorts first but whose IPv6 path is
        black-holed, taking only the first address reports the share as
        unreachable when IPv4 would have answered instantly."""
        try:
            candidates = resolve_candidates(target, self.port, proto="tcp")
        except OSError:
            return None
        for family, sockaddr in candidates:
            sock = socket.socket(family, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            try:
                sock.connect(sockaddr)
                sock.sendall(_netbios_session(payload))
                return sock.recv(1024)
            except OSError:
                continue          # this family is unreachable — try the next
            finally:
                sock.close()
        return None

    def _ntlm_fingerprint(self, target: str) -> dict:
        """Best-effort: SMB2 NEGOTIATE then a pre-auth SESSION_SETUP to harvest the
        server's NTLMSSP Version (exact Windows build). Any failure → {} (the SMB
        result is still emitted without a build). Read-only, unauthenticated."""
        for ip in resolve_ip_candidates(target, self.port, proto="tcp"):
            build = ntlm_os_build(ip, self.port, self.timeout)
            if build:
                return build      # first address that answers wins
        return {}

    async def scan_target(self, target: str) -> list[ScanResult]:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()

        async with self.sem:
            smb1 = await loop.run_in_executor(
                None, self._negotiate, target, _smb1_negotiate())
            smb2 = await loop.run_in_executor(
                None, self._negotiate, target, _smb2_negotiate())

        smb1_enabled = bool(smb1 and len(smb1) > 8 and smb1[4:8] == b"\xffSMB")
        smb2_supported = bool(smb2 and len(smb2) > 8 and smb2[4:8] == b"\xfeSMB")

        if not smb1 and not smb2:
            return [ScanResult(self.name, target, port=self.port, proto="tcp",
                               status="filtered",
                               evidence="no SMB response on 445")]

        data = {
            "smbv1_enabled": smb1_enabled,
            "smb2_supported": smb2_supported,
        }
        data.update(parse_smb2_security_mode(smb2))

        # Authoritative OS build via the pre-auth NTLMSSP CHALLENGE (only worth a
        # second round-trip when SMB2 is actually up).
        os_evidence = ""
        method = None
        if smb2_supported:
            async with self.sem:
                fp = await loop.run_in_executor(None, self._ntlm_fingerprint, target)
            if fp:
                data.update(fp)
                method = fp.get("method")
                if fp.get("os_release"):
                    os_evidence = (f", os={fp['os_release']} (build {fp.get('os_build')}, "
                                   f"conf {fp.get('os_confidence')})")
                elif fp.get("target_name"):
                    os_evidence = f", server={fp['target_name']}"

        return [ScanResult(
            self.name, target, port=self.port, proto="tcp", status="open",
            method=method, data=data,
            evidence=(f"SMBv1={'on' if smb1_enabled else 'off'}, "
                      f"SMB2={'on' if smb2_supported else 'off'}, "
                      f"signing_required={data.get('signing_required')}" + os_evidence),
        )]


def main() -> None:
    parser = base_argparser("SMB dialect detection (SMBv1/SMB2 negotiate)")
    parser.add_argument("--port", type=int, default=445)
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = SMBScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, port=args.port)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
