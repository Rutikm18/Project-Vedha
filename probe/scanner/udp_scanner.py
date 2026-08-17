"""
udp_scanner.py — detect common UDP services via protocol-specific probes.

METHOD (collection only, playbook 11):
UDP has no handshake — a bare empty datagram is ambiguous.  We send a small,
valid, READ-ONLY protocol request and look for a positive reply:

  DNS    (53)   — A-query for 'example.com'; recursion + open-resolver flag
  NTP    (123)  — mode-3 client request; follows with monlist check (amplification)
  SNMP   (161)  — SNMPv1 GET sysDescr, community 'public'
  NetBIOS(137)  — node-status wildcard request
  IKE    (500)  — minimal IKEv2 IKE_SA_INIT probe; version fingerprint
  IKE-NAT(4500) — IKE-in-UDP-encapsulation (RFC 3948)
  SIP    (5060) — SIP OPTIONS request; server header extraction
  TFTP   (69)   — RRQ for a known-nonexistent file; error reply confirms service
  IPMI   (623)  — RMCP Ping (ASF); Pong confirms BMC present
  SSDP   (1900) — UPnP M-SEARCH (unicast to target); extracts Location header
  mDNS   (5353) — PTR query for _services._dns-sd._udp.local
  memcached(11211)— stats command; unauth read = finding

A reply = service is open and speaking.  No reply = open|filtered (ambiguous).
All probes are standard read operations.  Nothing is modified on the target.
"""

from __future__ import annotations

import asyncio
import struct

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint, LOG,
    async_udp_probe, async_udp_probe_retry, _UDP_CLOSED, AdaptiveRateController,
)


# ── Probe builders ────────────────────────────────────────────────────────────

def _dns_probe() -> bytes:
    tid = b"\x13\x37"
    header = tid + b"\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    qname = b"\x03www\x07example\x03com\x00"
    return header + qname + b"\x00\x01\x00\x01"  # type A, class IN


def _ntp_probe() -> bytes:
    return b"\x1b" + b"\x00" * 47  # NTP v3, mode 3 (client)


def _ntp_monlist_probe() -> bytes:
    return b"\x17\x00\x03\x2a" + b"\x00" * 4  # NTP mode-7 MON_GETLIST_1


def _snmp_probe(community: bytes = b"public") -> bytes:
    oid = b"\x2b\x06\x01\x02\x01\x01\x01\x00"
    varbind = b"\x30" + bytes([len(oid) + 4]) + b"\x06" + bytes([len(oid)]) + oid + b"\x05\x00"
    vbl = b"\x30" + bytes([len(varbind)]) + varbind
    pdu_body = b"\x02\x01\x01\x02\x01\x00\x02\x01\x00" + vbl
    pdu = b"\xa0" + bytes([len(pdu_body)]) + pdu_body
    comm_tlv = b"\x04" + bytes([len(community)]) + community
    msg = b"\x02\x01\x00" + comm_tlv + pdu
    return b"\x30" + bytes([len(msg)]) + msg


def _netbios_probe() -> bytes:
    tid = b"\x80\x00"
    flags = b"\x00\x10"
    counts = b"\x00\x01" + b"\x00\x00" + b"\x00\x00" + b"\x00\x00"
    encoded = b"\x20" + b"CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + b"\x00"
    return tid + flags + counts + encoded + b"\x00\x21\x00\x01"


def _memcached_stats_probe() -> bytes:
    return b"\x00\x00\x00\x00\x00\x01\x00\x00" + b"stats\r\n"


def _ike_probe() -> bytes:
    """
    Minimal IKEv2 IKE_SA_INIT probe.  Sends a real SA payload proposing
    AES-256-CBC/SHA-256/PSK/DH-14 so well-behaved daemons send a real response
    (COOKIE_REQUIRED, INVALID_KE, or an actual SA_INIT reply).
    """
    init_spi = b"\xde\xad\xbe\xef\xca\xfe\xba\xbe"  # fixed test cookie

    # Transform sub-structures (all fixed-length)
    # T1: ENCR_AES_CBC (id=12), Key-Length=256 attr (0x800e0100)
    t1 = struct.pack("!BBHBBH", 3, 0, 12, 0x00, 0x0c, 4) + b"\x80\x0e\x01\x00"
    # T2: PRF_HMAC_SHA2_256 (id=5)
    t2 = struct.pack("!BBHBBH", 3, 0, 8, 0x00, 0x02, 0) + struct.pack("!H", 5)
    # T3: AUTH_HMAC_SHA2_256_128 (id=12)
    t3 = struct.pack("!BBHBBH", 3, 0, 8, 0x00, 0x03, 0) + struct.pack("!H", 12)
    # T4 (last): D-H Group 14/2048-MODP (id=14) — next=0
    t4 = struct.pack("!BBHBBH", 0, 0, 8, 0x00, 0x04, 0) + struct.pack("!H", 14)

    transforms = t1 + t2 + t3 + t4
    # Proposal sub-structure: proposal#=1, proto=IKE, SPI-size=0, #transforms=4
    prop_hdr = struct.pack("!BBHBBBB", 0, 0, 8 + len(transforms), 1, 1, 0, 4)
    prop = prop_hdr + transforms

    # SA payload header: next=0 (we'll fix below), critical=0, length
    sa_payload_body = prop
    sa_hdr = struct.pack("!BBH", 0, 0, 4 + len(sa_payload_body))
    sa = sa_hdr + sa_payload_body

    total = 28 + len(sa)
    # IKEv2 header (28 bytes):
    #   init_spi(8) + resp_spi(8) + next(1) + ver(1) + exch(1) + flags(1) + msg_id(4) + len(4)
    hdr = (init_spi + b"\x00" * 8
           + struct.pack("!BBBBII", 33, 0x20, 34, 0x08, 0, total))
    return hdr + sa


def _sip_probe(target: str) -> bytes:
    """SIP OPTIONS request — safe fingerprint method."""
    lines = [
        f"OPTIONS sip:probe@{target} SIP/2.0",
        f"Via: SIP/2.0/UDP {target}:5060;branch=z9hG4bKvedha0001",
        "Max-Forwards: 70",
        f"To: <sip:probe@{target}>",
        "From: <sip:vedha@vedha.internal>;tag=vedha0001",
        "Call-ID: vedha-scan-001@vedha.internal",
        "CSeq: 1 OPTIONS",
        "Contact: <sip:vedha@vedha.internal>",
        "Accept: application/sdp",
        "Content-Length: 0",
        "",
        "",
    ]
    return "\r\n".join(lines).encode()


def _tftp_probe() -> bytes:
    """TFTP RRQ for a non-existent file.  Error reply confirms TFTP service."""
    # Opcode 1 = RRQ, filename, NUL, mode, NUL. Filename is a neutral non-existent
    # name (no tool signature) — any TFTP server errors on it, proving the service.
    return b"\x00\x01" + b"test.txt\x00" + b"octet\x00"


def _ipmi_probe() -> bytes:
    """RMCP Ping (ASF Presence Ping) to detect IPMI/BMC."""
    # RMCP header: version=0x06, reserved=0x00, seq=0xFF, class=0x06 (ASF)
    # ASF data: IANA=0x000011BE, MsgType=0x80 (Presence Ping), Tag=0, Reserved=0, DataLen=0
    return b"\x06\x00\xff\x06" + struct.pack("!IBBBB", 0x000011BE, 0x80, 0x00, 0x00, 0x00)


def _ssdp_probe() -> bytes:
    """UPnP/SSDP M-SEARCH — unicast to target:1900."""
    return (
        b"M-SEARCH * HTTP/1.1\r\n"
        b"HOST: 239.255.255.250:1900\r\n"
        b'MAN: "ssdp:discover"\r\n'
        b"MX: 3\r\n"
        b"ST: ssdp:all\r\n"
        b"\r\n"
    )


def _mdns_probe() -> bytes:
    """mDNS PTR query for _services._dns-sd._udp.local (unicast to :5353)."""
    # Standard DNS query, QU bit set in qclass (multicast unicast)
    header = b"\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00"
    name = (b"\x09_services\x07_dns-sd\x04_udp\x05local\x00")
    question = name + b"\x00\x0c\x80\x01"  # PTR, QU=1 in class
    return header + question


# ── Response interpreters ─────────────────────────────────────────────────────

def interpret_ntp_monlist(reply: bytes) -> bool:
    return bool(reply) and bool(reply[0] & 0x80) and (reply[0] & 0x07) == 7


def interpret_dns_recursion(reply: bytes) -> dict:
    if len(reply) < 12:
        return {"responded": False, "recursion_available": False, "open_recursion": False}
    flags = struct.unpack(">H", reply[2:4])[0]
    rcode = flags & 0x000F
    ra = bool(flags & 0x0080)
    ancount = struct.unpack(">H", reply[6:8])[0]
    return {"responded": True, "recursion_available": ra,
            "open_recursion": ra and rcode == 0 and ancount > 0}


def interpret_memcached_stats(reply: bytes) -> bool:
    return b"STAT " in (reply or b"")


def interpret_ike(reply: bytes) -> dict:
    """Parse IKEv1 or IKEv2 response header."""
    if len(reply) < 28:
        return {"version": "unknown"}
    ver = reply[17]
    major, minor = ver >> 4, ver & 0x0F
    exchange = reply[18]
    if major == 2:
        return {"version": f"IKEv{major}.{minor}", "exchange_type": exchange,
                "vendor_fingerprint": "ikev2"}
    elif major == 1:
        return {"version": f"IKEv{major}.{minor}", "exchange_type": exchange,
                "vendor_fingerprint": "ikev1"}
    return {"version": "unknown", "raw_ver_byte": ver}


def interpret_sip(reply: bytes) -> dict:
    """Extract SIP version + server header from a SIP response."""
    text = reply.decode("latin-1", "replace")
    first_line = text.split("\r\n")[0] if text else ""
    server = ""
    for line in text.split("\r\n"):
        if line.lower().startswith("server:"):
            server = line.split(":", 1)[1].strip()
            break
        if line.lower().startswith("user-agent:"):
            server = line.split(":", 1)[1].strip()
            break
    return {"sip_response": first_line, "server": server}


def interpret_ipmi(reply: bytes) -> dict:
    """Parse RMCP Pong; extract supported entities and IPMI capabilities."""
    if len(reply) < 12:
        return {}
    entities_supported = reply[10] if len(reply) > 10 else 0
    ipmi_supported = bool(entities_supported & 0x20)
    return {
        "rmcp_pong": True,
        "entities_supported": hex(entities_supported),
        "ipmi_supported": ipmi_supported,
    }


def interpret_ssdp(reply: bytes) -> dict:
    """Extract Location and Server from SSDP response."""
    text = reply.decode("latin-1", "replace")
    location, server, st = "", "", ""
    for line in text.split("\r\n"):
        ll = line.lower()
        if ll.startswith("location:"):
            location = line.split(":", 1)[1].strip()
        elif ll.startswith("server:"):
            server = line.split(":", 1)[1].strip()
        elif ll.startswith("st:"):
            st = line.split(":", 1)[1].strip()
    return {"location": location, "server": server, "st": st}


def interpret_mdns(reply: bytes) -> dict:
    """Return byte count and check QR bit (1 = response)."""
    if len(reply) < 4:
        return {}
    flags = struct.unpack(">H", reply[2:4])[0]
    is_response = bool(flags & 0x8000)
    ancount = struct.unpack(">H", reply[6:8])[0] if len(reply) >= 8 else 0
    return {"mdns_response": is_response, "answer_count": ancount}


# ── Probe registry ────────────────────────────────────────────────────────────

# (service_name, payload_bytes)
# Note: SIP payload depends on target, so it's None here and computed at scan time
UDP_PROBES: dict[int, tuple[str, bytes | None]] = {
    53:    ("dns",       _dns_probe()),
    69:    ("tftp",      _tftp_probe()),
    123:   ("ntp",       _ntp_probe()),
    137:   ("netbios-ns", _netbios_probe()),
    161:   ("snmp",      _snmp_probe()),
    500:   ("ike",       _ike_probe()),
    623:   ("ipmi",      _ipmi_probe()),
    1900:  ("ssdp",      _ssdp_probe()),
    4500:  ("ike-nat",   _ike_probe()),  # IKE over UDP encapsulation
    5060:  ("sip",       None),          # built per-target
    5353:  ("mdns",      _mdns_probe()),
    11211: ("memcached", _memcached_stats_probe()),
}


class UDPScanner(BaseScanner):
    name = "udp_scan"

    def __init__(self, *args, ports: list[int] | None = None,
                 max_retries: int = 2, adaptive: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or list(UDP_PROBES.keys())
        self.max_retries = max_retries
        # When adaptive, an AIMD window replaces the fixed semaphore as the
        # concurrency gate, self-tuning to loss / ICMP rate limits.
        self.rate_ctl = (AdaptiveRateController(max_window=self._concurrency)
                         if adaptive else None)

    async def _gated_probe(self, target: str, port: int, payload: bytes):
        """Acquire the concurrency gate (adaptive window or fixed semaphore),
        run the retransmitting probe, and (when adaptive) release with the
        loss/success outcome so the window can grow or shrink."""
        if self.rate_ctl is not None:
            await self.rate_ctl.acquire()
            data = None
            try:
                data = await async_udp_probe_retry(
                    target, port, payload, self.timeout,
                    max_retries=self.max_retries)
            finally:
                if data is None:
                    await self.rate_ctl.report_loss()
                else:
                    await self.rate_ctl.report_success()
            return data
        async with self.sem:
            return await async_udp_probe_retry(
                target, port, payload, self.timeout,
                max_retries=self.max_retries)

    async def _probe(self, target: str, port: int) -> ScanResult | None:
        if port not in UDP_PROBES:
            return None
        svc, payload = UDP_PROBES[port]

        # Build target-specific payloads
        if svc == "sip":
            payload = _sip_probe(target)

        await self.limiter.wait()
        data = await self._gated_probe(target, port, payload)

        if data is _UDP_CLOSED:
            # ICMP port-unreachable — definitively closed (not the usual UDP
            # open|filtered ambiguity). Surfacing this is the accuracy win from
            # the event-loop-native transport.
            return ScanResult(self.name, target, port=port, proto="udp",
                              status="closed",
                              data={"service_guess": svc, "responded": False},
                              evidence="ICMP port-unreachable (closed)")

        if data is None:
            # Silence is genuinely ambiguous on UDP: no reply can mean the port
            # is open and the service ignored our probe, OR a firewall silently
            # dropped it. We MUST NOT collapse that to a definitive "filtered"
            # (the prior bug) — the honest state is the open|filtered pair.
            return ScanResult(self.name, target, port=port, proto="udp",
                              status="open|filtered",
                              data={"service_guess": svc, "responded": False,
                                    "reason": "no_response"},
                              evidence="no UDP or ICMP response (open|filtered)")

        result_data: dict = {"service": svc, "responded": True,
                             "reply_bytes": len(data),
                             "reply_hex_head": data[:48].hex()}

        if svc == "ntp":
            await self.limiter.wait()
            async with self.sem:
                mon = await async_udp_probe(
                    target, port, _ntp_monlist_probe(), self.timeout)
            mon_bytes = mon if isinstance(mon, (bytes, bytearray)) else b""
            result_data["monlist_enabled"] = interpret_ntp_monlist(mon_bytes)
        elif svc == "dns":
            result_data.update(interpret_dns_recursion(data))
        elif svc == "memcached":
            result_data["exposed_unauthenticated"] = interpret_memcached_stats(data)
        elif svc in ("ike", "ike-nat"):
            result_data.update(interpret_ike(data))
        elif svc == "sip":
            result_data.update(interpret_sip(data))
        elif svc == "ipmi":
            result_data.update(interpret_ipmi(data))
        elif svc == "ssdp":
            result_data.update(interpret_ssdp(data))
        elif svc == "mdns":
            result_data.update(interpret_mdns(data))

        return ScanResult(
            self.name, target, port=port, proto="udp", status="open",
            data=result_data,
            evidence=f"{svc} replied with {len(data)} bytes",
        )

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._probe(target, p) for p in self.ports]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]


def main() -> None:
    parser = base_argparser(
        "UDP service scanner (DNS/NTP/SNMP/NetBIOS/IKE/SIP/TFTP/IPMI/SSDP/mDNS)")
    parser.add_argument("-p", "--ports", default=None,
                        help="UDP ports to probe (default: all known ports)")
    parser.add_argument("--max-retries", type=int, default=2,
                        help="per-port retransmits on silence (default 2) — "
                             "resolves UDP open|filtered under packet loss")
    parser.add_argument("--adaptive", action="store_true",
                        help="AIMD congestion window instead of fixed concurrency "
                             "(self-tunes to loss / ICMP rate limits)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        if args.ports:
            requested = set(parse_ports(args.ports))
            ports = [p for p in sorted(requested) if p in UDP_PROBES]
            unknown = sorted(requested - set(UDP_PROBES))
            if unknown:
                LOG.warning("no UDP probe defined for %s — skipping (supported: %s)",
                            unknown, sorted(UDP_PROBES))
            if not ports:
                LOG.error("none of the requested UDP ports have a probe")
                return
        else:
            ports = list(UDP_PROBES.keys())
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = UDPScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports,
                             max_retries=args.max_retries, adaptive=args.adaptive)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
