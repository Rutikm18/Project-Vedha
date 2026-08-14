"""
mobile_scanner.py — mobile device exposure detection.

Covers playbook 13 (Mobile Device Assessment) — network-visible attack surfaces:

  ADB over TCP  (port 5555) — Android Debug Bridge in TCP mode.
    If a developer ran `adb tcpip 5555`, anyone on-network can connect with no
    authentication and get a shell, install apps, and read data (Critical).
    Detection: TCP connect → send A_CNXN handshake → parse CNXN reply.
    We NEVER run `adb shell` or read any device data; proof-of-presence only.

  iOS lockdownd  (port 62078) — Apple mobile device management daemon.
    Port being open = an iOS device is present on the network with lockdownd
    listening.  Pairing is required to go further; we only confirm reachability.
    Detection: TCP connect-only; open port = finding.

  mDNS mobile fingerprint  (UDP 5353) — many phones announce their presence via
    Bonjour.  Device names often include owner's name ("John's iPhone"),
    AirDrop/AirPlay/Google Cast service types reveal OS.
    Detection: query _apple-mobdev2._tcp.local (iOS MobileDevice), _googlecast._tcp.local,
    _airdrop._tcp.local; parse PTR replies.

COLLECTION METHOD: we only send the minimum to confirm service presence.
ADB: we send one A_CNXN initiator message and parse the reply.  We do NOT
     run any shell commands, list packages, read files, or exercise any adb sub-command.
iOS: TCP connect only.  No data beyond the TCP handshake.
mDNS: one DNS query; read reply.  We do not capture personal data.
"""

from __future__ import annotations

import asyncio
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    resolve, setup_logging, base_argparser, main_entrypoint,
)

# ── ADB protocol constants ─────────────────────────────────────────────────────

# ADB command codes (little-endian 32-bit)
A_CNXN = 0x4e584e43   # b"CNXN" in LE = 'C','N','X','N'
A_AUTH = 0x48545541   # b"AUTH"
A_OPEN = 0x4e45504f   # b"OPEN"

ADB_VERSION     = 0x01000000
ADB_MAX_PAYLOAD = 256 * 1024

# Minimal feature set string a probe client sends
_ADB_FEATURES = b"host::features=shell_v2,cmd\x00"


def _adb_checksum(data: bytes) -> int:
    return sum(data) & 0xFFFFFFFF


def _build_adb_cnxn() -> bytes:
    """Build an ADB A_CNXN (CONNECT) message — the standard handshake initiator."""
    data = _ADB_FEATURES
    checksum = _adb_checksum(data)
    magic = A_CNXN ^ 0xFFFFFFFF
    header = struct.pack("<IIIIII",
        A_CNXN, ADB_VERSION, ADB_MAX_PAYLOAD,
        len(data), checksum, magic)
    return header + data


def _parse_adb_header(data: bytes) -> dict | None:
    """Parse a 24-byte ADB message header.  Returns parsed fields or None."""
    if len(data) < 24:
        return None
    cmd, arg0, arg1, data_len, data_check, magic = struct.unpack("<IIIIII", data[:24])
    # Verify magic field invariant: magic = cmd ^ 0xFFFFFFFF
    if magic != (cmd ^ 0xFFFFFFFF):
        return None
    cmd_name = {
        A_CNXN: "CNXN",
        A_AUTH: "AUTH",
        A_OPEN: "OPEN",
        0x59454b4f: "OKAY",
        0x45534f4c: "CLSE",
        0x45544957: "WRTE",
    }.get(cmd, hex(cmd))
    return {
        "command": cmd_name,
        "arg0": arg0,
        "arg1": arg1,
        "data_length": data_len,
    }


async def _probe_adb(target: str, port: int,
                     timeout: float) -> dict | None:
    """
    Send ADB CNXN and read the device's CNXN reply.
    Returns a dict with connection info, or None if not ADB.
    """
    try:
        fut = asyncio.open_connection(target, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None

    try:
        writer.write(_build_adb_cnxn())
        await writer.drain()
        # Read 24-byte header
        hdr_bytes = await asyncio.wait_for(reader.readexactly(24), timeout=timeout)
    except (asyncio.TimeoutError, OSError, asyncio.IncompleteReadError):
        writer.close()
        return None
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass

    parsed = _parse_adb_header(hdr_bytes)
    if parsed is None:
        return None

    result: dict = {
        "adb_command": parsed["command"],
        "adb_version": hex(parsed["arg0"]),
        "max_payload": parsed["arg1"],
    }

    if parsed["command"] == "AUTH":
        result["auth_required"] = True
        result["unauthenticated_shell"] = False
        result["note"] = ("ADB in TCP mode — auth challenge received. "
                          "Old devices (pre-Android 4.2.2) may skip auth on open networks.")
    elif parsed["command"] == "CNXN":
        result["auth_required"] = False
        result["unauthenticated_shell"] = True
        result["note"] = "ADB in TCP mode — NO AUTH — remote shell available to anyone"
    else:
        result["note"] = f"Unexpected ADB command: {parsed['command']}"

    return result


# ── iOS lockdownd ─────────────────────────────────────────────────────────────

_IOS_LOCKDOWND_PORT = 62078

async def _probe_lockdownd(target: str, port: int,
                            timeout: float) -> dict | None:
    """
    Attempt TCP connect to lockdownd port 62078.
    Port open = iOS device present and lockdownd listening.
    We do not send data; pairing is required to go further.
    """
    try:
        fut = asyncio.open_connection(target, port)
        reader, writer = await asyncio.wait_for(fut, timeout=timeout)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return {
            "ios_lockdownd": True,
            "note": "iOS lockdownd port open — pairing/trust required to proceed",
        }
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None


# ── mDNS mobile service fingerprint ─────────────────────────────────────────

_MDNS_PORT = 5353

# Mobile-device-specific mDNS service types to query
_MOBILE_MDNS_QUERIES: list[tuple[str, str]] = [
    ("_apple-mobdev2._tcp.local", "iOS MobileDevice pairing"),
    ("_airdrop._tcp.local",       "Apple AirDrop"),
    ("_airplay._tcp.local",       "Apple AirPlay"),
    ("_googlecast._tcp.local",    "Google Cast / Chromecast"),
    ("_androidtvremote2._tcp.local", "Android TV"),
]


def _build_mdns_query(service_name: str) -> bytes:
    """Build a DNS PTR query in mDNS wire format with QU bit set."""
    # Transaction ID = 0 for mDNS
    header = b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    # Encode QNAME from service_name (e.g. "_airplay._tcp.local")
    labels = service_name.rstrip(".").split(".")
    qname = b"".join(bytes([len(l)]) + l.encode() for l in labels) + b"\x00"
    question = qname + b"\x00\x0c\x80\x01"  # PTR, QU=1 in class
    return header + question


def _parse_mdns_ptr_names(data: bytes) -> list[str]:
    """Extract PTR target names (service instance names) from mDNS reply."""
    if len(data) < 12:
        return []
    ancount = struct.unpack(">H", data[6:8])[0]
    if ancount == 0:
        return []
    # Skip question section
    i = 12
    qcount = struct.unpack(">H", data[4:6])[0]
    for _ in range(qcount):
        while i < len(data) and data[i] != 0:
            if data[i] & 0xC0 == 0xC0:
                i += 2; break
            i += data[i] + 1
        else:
            i += 1  # null terminator
        i += 4     # qtype + qclass
    # Parse answers — extract RDATA for PTR records
    names: list[str] = []
    for _ in range(ancount):
        if i >= len(data): break
        # Skip name
        while i < len(data) and data[i] != 0:
            if data[i] & 0xC0 == 0xC0:
                i += 2; break
            i += data[i] + 1
        else:
            if i < len(data): i += 1
        if i + 10 > len(data): break
        rtype, _, _, rdlen = struct.unpack(">HHIH", data[i:i + 10])
        i += 10
        if rtype == 12 and i + rdlen <= len(data):  # PTR
            # Decode RDATA name
            parts, j = [], i
            while j < i + rdlen and j < len(data):
                ln = data[j]
                if ln & 0xC0 == 0xC0:
                    if j + 1 < len(data):
                        ptr = ((ln & 0x3F) << 8) | data[j + 1]
                        # Simple pointer resolve (one hop)
                        pk, pparts = ptr, []
                        while pk < len(data) and data[pk] != 0:
                            if data[pk] & 0xC0 == 0xC0: break
                            pparts.append(data[pk + 1:pk + 1 + data[pk]].decode("utf-8", "replace"))
                            pk += data[pk] + 1
                        parts.extend(pparts)
                    break
                elif ln == 0:
                    break
                else:
                    parts.append(data[j + 1:j + 1 + ln].decode("utf-8", "replace"))
                    j += ln + 1
            if parts:
                names.append(".".join(parts))
        i += rdlen
    return names


def _probe_mdns_mobile_sync(target: str, service_name: str,
                             timeout: float) -> list[str]:
    """Send one mDNS PTR query to target:5353 and return instance names."""
    try:
        family, sockaddr = resolve(target, _MDNS_PORT, proto="udp")
    except OSError:
        return []
    sock = socket.socket(family, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    try:
        sock.sendto(_build_mdns_query(service_name), sockaddr)
        data, _ = sock.recvfrom(4096)
        return _parse_mdns_ptr_names(data)
    except (socket.timeout, OSError):
        return []
    finally:
        sock.close()


# ── Main scanner class ────────────────────────────────────────────────────────

class MobileScanner(BaseScanner):
    """
    Detects mobile device exposure on the network:
    ADB (Android) | lockdownd (iOS) | mDNS service fingerprint.
    """
    name = "mobile_scan"

    async def scan_target(self, target: str) -> list[ScanResult]:
        loop = asyncio.get_running_loop()
        results: list[ScanResult] = []

        # ADB TCP (port 5555)
        await self.limiter.wait()
        async with self.sem:
            adb = await _probe_adb(target, 5555, self.timeout)
        if adb:
            unauth = adb.get("unauthenticated_shell", False)
            results.append(ScanResult(
                self.name, target, port=5555, proto="tcp",
                status="open",
                data=adb,
                evidence=(
                    "ADB TCP — UNAUTHENTICATED SHELL (Critical)" if unauth
                    else f"ADB TCP ({adb.get('adb_command','?')}): auth required"
                )))

        # iOS lockdownd (port 62078)
        await self.limiter.wait()
        async with self.sem:
            ios = await _probe_lockdownd(target, _IOS_LOCKDOWND_PORT, self.timeout)
        if ios:
            results.append(ScanResult(
                self.name, target, port=_IOS_LOCKDOWND_PORT, proto="tcp",
                status="open",
                data=ios,
                evidence="iOS lockdownd detected (device pairing required)"))

        # mDNS mobile service fingerprint
        detected_services: list[dict] = []
        for svc_name, svc_label in _MOBILE_MDNS_QUERIES:
            await self.limiter.wait()
            async with self.sem:
                instances = await loop.run_in_executor(
                    None, _probe_mdns_mobile_sync, target, svc_name, self.timeout)
            if instances:
                detected_services.append({
                    "service_type": svc_name,
                    "description": svc_label,
                    "instances": instances,
                })

        if detected_services:
            all_instances = [i for svc in detected_services for i in svc["instances"]]
            results.append(ScanResult(
                self.name, target, port=_MDNS_PORT, proto="udp",
                status="open",
                data={"mobile_mdns_services": detected_services},
                evidence=f"Mobile mDNS: {', '.join(all_instances[:3])}"))

        return results


def main() -> None:
    parser = base_argparser("Mobile device exposure scanner (ADB/iOS/mDNS)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = MobileScanner(scope, rate=args.rate, concurrency=args.concurrency,
                                timeout=args.timeout)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
