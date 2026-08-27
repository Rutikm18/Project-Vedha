"""
vnc_scanner.py — VNC/RFB authentication exposure (VA checklist: unauthenticated
or weakly-authenticated remote desktop).

METHOD (collection, read-only): perform only the RFB version handshake (RFC 6143
§7.1) and read the security types the server OFFERS. We never send an
authentication response and never open a framebuffer session — reading the
advertised security types is exactly what an RFB client does before it decides
how (or whether) to authenticate.

Findings this feeds:
  * security type 1 (None)  → the desktop is reachable with NO authentication at
    all (critical).
  * security type 2 (VNC Authentication) → the legacy DES challenge/response,
    which truncates passwords to 8 chars and is offline-brute-forceable (weak).

POLICY BOUNDARY: reading the offered types is a pure observation — no credential
is sent, no auth is attempted. Strictly in-policy.

SAFETY: raw socket over BaseScanner timeouts; bounded reads; guarded.
"""

from __future__ import annotations

import asyncio
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_VNC_PORTS = [5900, 5901]

# RFB security-type registry (RFC 6143 + common vendor extensions).
_SECURITY_TYPES = {
    0: "Invalid", 1: "None", 2: "VNC", 5: "RA2", 6: "RA2ne", 7: "SSPI", 8: "SSPIne",
    16: "Tight", 17: "Ultra", 18: "TLS", 19: "VeNCrypt", 20: "SASL", 21: "MD5",
    22: "xvp", 23: "SecureTunnel", 24: "IntegratedSSH", 30: "AppleARD", 35: "AppleARD",
}
# Security types that constitute real, non-legacy authentication.
_STRONG_TYPES = {5, 6, 7, 8, 18, 19, 20, 23, 24, 30, 35}


def parse_rfb_version(data) -> tuple[int, int] | None:
    """Parse a 'RFB 003.008' banner into (major, minor), or None if not RFB."""
    if isinstance(data, (bytes, bytearray)):
        data = bytes(data).decode("latin-1", "replace")
    data = data.strip()
    if not data.startswith("RFB "):
        return None
    try:
        major_s, minor_s = data[4:].split(".", 1)
        return int(major_s), int(minor_s[:3])
    except ValueError:
        return None


def classify_security_types(types: list[int]) -> dict:
    """Turn a list of offered security-type ids into a verdict."""
    named = [{"id": t, "name": _SECURITY_TYPES.get(t, f"unknown-{t}")} for t in types]
    return {
        "security_types": named,
        "no_auth": 1 in types,
        "weak_auth": 2 in types,
        "has_strong_auth": any(t in _STRONG_TYPES for t in types),
    }


def _recv_exact(sock: socket.socket, n: int) -> bytes | None:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def _read_security_types(sock: socket.socket, major: int, minor: int) -> list[int]:
    """Read the offered security types, handling the RFB 3.3 (single 4-byte type)
    vs 3.7+ (count byte + list) forms."""
    if major > 3 or (major == 3 and minor >= 7):
        n = _recv_exact(sock, 1)
        if not n:
            return []
        count = n[0]
        if count == 0:                      # handshake failed: 4-byte reason len + text
            return []
        data = _recv_exact(sock, count)
        return list(data) if data else []
    # RFB 3.3: server dictates a single security type as a uint32
    data = _recv_exact(sock, 4)
    if not data:
        return []
    (t,) = struct.unpack(">I", data)
    return [t] if t != 0 else []


class VNCScanner(BaseScanner):
    name = "vnc_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_VNC_PORTS

    def _probe(self, target: str, port: int) -> dict:
        """Blocking: RFB version handshake + read offered security types.
        Monkeypatchable for tests."""
        try:
            with socket.create_connection((target, port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                banner = _recv_exact(s, 12)
                ver = parse_rfb_version(banner) if banner else None
                if ver is None:
                    return {"vnc": None, "reason": "no_vnc"}
                major, minor = ver
                s.sendall(banner)                 # echo the server's version verbatim
                types = _read_security_types(s, major, minor)
        except OSError as exc:
            return {"vnc": None, "reason": "no_vnc", "detail": str(exc)[:120]}
        data = {"vnc": True, "protocol_version": f"{major}.{minor}"}
        data.update(classify_security_types(types))
        return data

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="tcp",
                                  status="error", error=str(exc))
        if not data.get("vnc"):
            return ScanResult(self.name, target, port=port, proto="tcp",
                              status="filtered", reason=data.get("reason", "no_vnc"),
                              data=data)
        evidence = (f"rfb={data.get('protocol_version')} no_auth={data.get('no_auth')} "
                    f"weak_auth={data.get('weak_auth')}")
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("VNC/RFB authentication exposure check")
    parser.add_argument("-p", "--ports", default=None, help="VNC ports (default: 5900,5901)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_VNC_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = VNCScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
