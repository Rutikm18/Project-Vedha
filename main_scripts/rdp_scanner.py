#!/usr/bin/env python3
"""
rdp_scanner.py — protocol-level RDP confirmation + security-layer detection.

Port 3389 being open does NOT confirm RDP (spec Phase 16/18: never trust the port
number). This does the real X.224 handshake: send a Connection Request with an RDP
Negotiation Request, read the Connection Confirm, and read which security protocol
the server selected.

Offensive value: a server that negotiates STANDARD RDP security (no NLA) is a
pre-authentication attack surface — brute-forceable and in the BlueKeep
(CVE-2019-0708) class. NLA (CredSSP/HYBRID) forces auth before the RDP stack is
reachable. This lets the finding say "RDP confirmed, NLA OFF" with evidence, not
"port 3389 open, probably RDP".

Read-only: one handshake, no credentials, no exploitation. ScopeGuard/rate limits
are enforced by BaseScanner.
"""
from __future__ import annotations

import asyncio
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, resolve, setup_logging, base_argparser, main_entrypoint,
)

# RDP security protocols (rdpNegReq/rdpNegRsp `requestedProtocols`/`selectedProtocol`)
PROTOCOL_RDP = 0x00          # standard RDP security — no NLA (weakest)
PROTOCOL_SSL = 0x01          # TLS
PROTOCOL_HYBRID = 0x02       # CredSSP == Network Level Authentication (NLA)
PROTOCOL_HYBRID_EX = 0x08

_TYPE_NEG_REQ = 0x01
_TYPE_NEG_RSP = 0x02
_TYPE_NEG_FAILURE = 0x03


def build_connection_request(
        requested_protocols: int = PROTOCOL_SSL | PROTOCOL_HYBRID | PROTOCOL_HYBRID_EX,
        cookie: str | None = None) -> bytes:
    """TPKT + X.224 Connection Request carrying an RDP Negotiation Request."""
    neg_req = struct.pack("<BBHI", _TYPE_NEG_REQ, 0x00, 0x0008, requested_protocols)
    variable = b""
    if cookie:
        variable += b"Cookie: mstshash=" + cookie.encode("latin-1") + b"\r\n"
    variable += neg_req
    li = 6 + len(variable)                       # X.224 fixed part (6) + variable
    x224 = bytes([li, 0xE0, 0x00, 0x00, 0x00, 0x00, 0x00]) + variable
    return struct.pack("!BBH", 0x03, 0x00, 4 + len(x224)) + x224


def parse_connection_confirm(data: bytes) -> dict | None:
    """Parse a Connection Confirm. Returns None if this isn't an X.224 CC (i.e.
    the peer doesn't speak RDP's transport)."""
    if len(data) < 11 or data[0] != 0x03:        # TPKT version
        return None
    tpkt_len = struct.unpack("!H", data[2:4])[0]
    x224 = data[4:tpkt_len] if tpkt_len else data[4:]
    if len(x224) < 7 or (x224[1] & 0xF0) != 0xD0:  # CC-CDT high nibble == 0xD
        return None
    var = x224[7:]                                # after LI + fixed 6
    if len(var) >= 8 and var[0] == _TYPE_NEG_RSP:
        selected = struct.unpack("<I", var[4:8])[0]
        return _posture_from_selected(selected, negotiation="response")
    if len(var) >= 8 and var[0] == _TYPE_NEG_FAILURE:
        return {"rdp_confirmed": True, "negotiation": "failure",
                "failure_code": struct.unpack("<I", var[4:8])[0]}
    # CC but no negotiation response -> legacy server that only speaks standard RDP.
    return _posture_from_selected(PROTOCOL_RDP, negotiation=None)


def _posture_from_selected(selected: int, *, negotiation: str | None) -> dict:
    """Map an RDP selectedProtocol bitmask to (nla, tls) posture.

    MS-RDPBCGR 5.4.5.2: CredSSP == Network Level Authentication is represented by
    BOTH PROTOCOL_HYBRID (0x02) AND PROTOCOL_HYBRID_EX (0x08); TLS underlies SSL
    (0x01), HYBRID and HYBRID_EX. The previous code tested only 0x02, so an
    Early-User-Auth server that selects 0x08 was mislabelled nla:false/tls:false —
    the exact inversion this fixes. standard_rdp_security is the 0x00 selection.
    """
    nla = bool(selected & (PROTOCOL_HYBRID | PROTOCOL_HYBRID_EX))
    tls = bool(selected & (PROTOCOL_SSL | PROTOCOL_HYBRID | PROTOCOL_HYBRID_EX))
    return {
        "rdp_confirmed": True, "negotiation": negotiation,
        "selected_protocol": selected,
        "nla": nla, "tls": tls,
        "standard_rdp_security": selected == PROTOCOL_RDP,
    }


def probe_rdp(ip: str, port: int, timeout: float,
              requested_protocols: int = PROTOCOL_SSL | PROTOCOL_HYBRID | PROTOCOL_HYBRID_EX
              ) -> dict | None:
    """One synchronous RDP handshake offering `requested_protocols`. Best-effort;
    None on any failure."""
    try:
        with socket.create_connection((ip, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(build_connection_request(requested_protocols))
            data = sock.recv(1024)
    except (OSError, socket.timeout):
        return None
    return parse_connection_confirm(data)


def probe_rdp_posture(ip: str, port: int, timeout: float) -> dict | None:
    """Two-probe RDP posture (MS-RDPBCGR 2.2.1.1.1 / 2.2.1.2.1).

    Probe A offers SSL|HYBRID|HYBRID_EX → what security the server *selects*.
    Probe B offers standard RDP only (0x00) → whether NLA is *required*: a server
    that REFUSES the RDP-only request with RDP_NEG_FAILURE is enforcing NLA, so the
    stack is NOT reachable pre-auth (BlueKeep does not apply). A single probe cannot
    prove 'required'; the RDP-only probe is what makes the claim honest.
    """
    a = probe_rdp(ip, port, timeout)
    if not a:
        return None
    b = probe_rdp(ip, port, timeout, requested_protocols=PROTOCOL_RDP)
    if b is not None:
        if b.get("negotiation") == "failure":
            a["nla_required"] = True
            a["nla_required_evidence"] = (
                f"server refused standard-RDP (RDP_NEG_FAILURE, "
                f"failure_code={b.get('failure_code')})")
        elif b.get("standard_rdp_security"):
            # Server accepted a bare-RDP session — NLA is not enforced.
            a["nla_required"] = False
    return a


class RDPScanner(BaseScanner):
    name = "rdp_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or [3389]

    async def _scan_port(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                _family, sockaddr = resolve(target, port, proto="tcp")
            except OSError:
                return None
            info = await loop.run_in_executor(
                None, probe_rdp_posture, sockaddr[0], port, self.timeout)
        if not info:
            return None
        sp = info.get("selected_protocol")
        sec = ("NLA" if info.get("nla") else "TLS" if info.get("tls")
               else "standard-rdp" if info.get("standard_rdp_security") else "?")
        req = info.get("nla_required")
        req_txt = ("; NLA required" if req is True
                   else "; NLA NOT required" if req is False else "")
        return ScanResult(
            self.name, target, port=port, proto="tcp", status="open", data=info,
            evidence=f"RDP confirmed; security={sec}" + req_txt
            + (f" (selected_protocol={sp})" if sp is not None else ""))

    async def scan_target(self, target: str) -> list[ScanResult]:
        results = [await self._scan_port(target, p) for p in self.ports]
        return [r for r in results if r is not None]


def main() -> None:
    parser = base_argparser("RDP protocol confirmation + NLA detection")
    parser.add_argument("-p", "--ports", default="3389", help="RDP ports (default: 3389)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        ports = parse_ports(args.ports)
        targets = expand_targets(args.targets)
        scanner = RDPScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
