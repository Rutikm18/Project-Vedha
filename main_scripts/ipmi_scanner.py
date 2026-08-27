"""
ipmi_scanner.py — IPMI 2.0 cipher-zero authentication-bypass detection
(VA checklist: exposed BMC / lights-out management with broken auth).

METHOD (collection, read-only DETECTION): send a single IPMI 2.0 RMCP+ "Open
Session Request" (UDP/623) that offers authentication algorithm 0 — "cipher zero"
(RAKP-none). A BMC that answers with an Open Session Response of status
"no errors" is telling us it will establish an *administrative* session with NO
authentication whatsoever — a full auth bypass (CVE-2013-4786 class) that lets an
attacker reset passwords and power-cycle hardware.

We ONLY read the Open Session Response status. We do NOT complete the RAKP
exchange, do NOT request a RAKP2 HMAC (the offline-crackable password-hash
disclosure), and send no credentials — this is a capability observation, not an
exploitation or a credential attack, so it stays inside the probe's invariants.

SAFETY: one UDP datagram, bounded response read, guarded; the request is a fixed,
well-formed packet (no fuzzing).
"""

from __future__ import annotations

import asyncio
import socket
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_IPMI_PORTS = [623]
_CONSOLE_SESSION_ID = b"\xa4\xa3\xa2\xa0"   # arbitrary remote-console session id


def build_open_session_request() -> bytes:
    """A fixed RMCP+ Open Session Request offering cipher suite 0 (auth=0,
    integrity=0, confidentiality=0) — the cipher-zero probe."""
    rmcp = bytes([0x06, 0x00, 0xFF, 0x07])       # RMCP: v6, seq 0xff, class IPMI
    # RMCP+ session header: auth_type 0x06, payload_type 0x10 (Open Session Req),
    # session id 0, session seq 0, payload length (LE).
    payload = (
        bytes([0x00, 0x00, 0x00, 0x00]) + _CONSOLE_SESSION_ID  # tag, priv, rsvd, console SID
        + bytes([0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00])  # auth payload, algo 0
        + bytes([0x01, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00])  # integrity payload, algo 0
        + bytes([0x02, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00])  # confidentiality, algo 0
    )
    session = bytes([0x06, 0x10]) + b"\x00" * 8 + struct.pack("<H", len(payload))
    return rmcp + session + payload


def parse_open_session_response(resp: bytes) -> dict | None:
    """Parse an RMCP+ Open Session Response; None if it isn't one.
    resp[0]=RMCP ver, resp[5]=payload type (0x11 = Open Session Response),
    resp[17]=RMCP+ status code (0x00 = no errors => cipher zero accepted)."""
    if not resp or len(resp) < 18:
        return None
    if resp[0] != 0x06 or resp[5] != 0x11:
        return None
    status = resp[17]
    return {"open_session_response": True, "rmcp_status": status,
            "cipher_zero": status == 0x00}


class IPMIScanner(BaseScanner):
    name = "ipmi_scan"

    def __init__(self, *args, ports: list[int] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_IPMI_PORTS

    def _probe(self, target: str, port: int) -> dict:
        """Blocking: one RMCP+ Open Session Request, parse the response.
        Monkeypatchable for tests."""
        packet = build_open_session_request()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        try:
            sock.sendto(packet, (target, port))
            resp, _ = sock.recvfrom(1024)
        except OSError:
            return {"ipmi": None, "reason": "no_ipmi"}
        finally:
            sock.close()
        parsed = parse_open_session_response(resp)
        if parsed is None:
            return {"ipmi": None, "reason": "not_ipmi_response"}
        return {"ipmi": True, **parsed}

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="udp",
                                  status="error", error=str(exc))
        if not data.get("ipmi"):
            return ScanResult(self.name, target, port=port, proto="udp",
                              status="filtered", reason=data.get("reason", "no_ipmi"),
                              data=data)
        evidence = (f"ipmi2.0 cipher_zero={data.get('cipher_zero')} "
                    f"rmcp_status={data.get('rmcp_status')}")
        return ScanResult(self.name, target, port=port, proto="udp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("IPMI 2.0 cipher-zero auth-bypass detection")
    parser.add_argument("-p", "--ports", default=None, help="IPMI ports (default: 623)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_IPMI_PORTS
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = IPMIScanner(scope, rate=args.rate, concurrency=args.concurrency,
                              timeout=args.timeout, ports=ports)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
