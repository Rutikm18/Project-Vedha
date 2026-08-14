"""
snmp_scanner.py — full SNMP enumeration: community discovery, targeted MIB walk,
amplification measurement, and SNMPv3 presence check.

COLLECTION METHOD (read-only, playbook 12):
  Phase 1 — community discovery: SNMPv1 GET-request for sysDescr.0 with each
             candidate community string.  First successful reply establishes it.
  Phase 2 — targeted MIB walk (if valid community found), via GETNEXT (v1):
             • System group  : sysDescr, sysName, sysUpTime, sysContact, sysLocation
             • Interface table : ifDescr, ifPhysAddress, ifOperStatus  (first 20)
             • ARP/neighbor  : ipNetToMediaPhysAddress  (first 30) — maps LAN
             • IP address table: ipAdEntAddr
             • Running procs : hrSWRunName  (first 30)
             • TCP conn table: tcpConnLocalPort  (open services without scanning)
  Phase 3 — amplification check: one SNMPv2c GETBULK request; measure
             response_bytes / request_bytes.  Never looped, never source-spoofed.
  Phase 4 — SNMPv3 detect: send a USM discovery message; any reply = v3 capable.

No SETs.  No credential guessing beyond the explicit community list.
"""

from __future__ import annotations

import socket
import struct
import asyncio

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    resolve, setup_logging, base_argparser, main_entrypoint,
)

COMMON_COMMUNITIES = ["public", "private", "community", "manager", "snmp"]

# ── BER primitives ────────────────────────────────────────────────────────────

def _ber_len(n: int) -> bytes:
    if n < 0x80:
        return bytes([n])
    if n < 0x100:
        return bytes([0x81, n])
    return bytes([0x82, (n >> 8) & 0xFF, n & 0xFF])


def _encode_oid(dotted: str) -> bytes:
    """Dotted-notation OID string → BER-encoded bytes."""
    parts = [int(x) for x in dotted.split(".")]
    encoded = [40 * parts[0] + parts[1]]
    for p in parts[2:]:
        if p == 0:
            encoded.append(0)
        else:
            buf: list[int] = []
            while p:
                buf.append(p & 0x7F)
                p >>= 7
            buf.reverse()
            for i, b in enumerate(buf):
                encoded.append(b | (0x80 if i < len(buf) - 1 else 0))
    return bytes(encoded)


def _decode_oid(data: bytes) -> str:
    """BER-encoded OID bytes → dotted-notation string."""
    if not data:
        return ""
    result = [str(data[0] // 40), str(data[0] % 40)]
    i, val = 1, 0
    while i < len(data):
        b = data[i]; i += 1
        val = (val << 7) | (b & 0x7F)
        if not (b & 0x80):
            result.append(str(val))
            val = 0
    return ".".join(result)


def _decode_value(tag: int, val: bytes) -> str:
    """Human-readable SNMP value for common ASN.1/SNMP types."""
    if tag == 0x02:                              # INTEGER
        return str(int.from_bytes(val, "big", signed=True)) if val else "0"
    if tag == 0x04:                              # OCTET STRING
        try:
            return val.decode("utf-8")
        except Exception:
            return val.decode("latin-1", "replace")
    if tag == 0x06:                              # OID
        return _decode_oid(val)
    if tag == 0x40:                              # IpAddress
        return ".".join(str(b) for b in val) if len(val) == 4 else val.hex()
    if tag in (0x41, 0x42, 0x43, 0x47):         # Counter32/Gauge32/TimeTicks/Unsigned32
        return str(int.from_bytes(val, "big"))
    if tag == 0x46:                              # Counter64
        return str(int.from_bytes(val, "big"))
    if tag == 0x80:
        return "noSuchObject"
    if tag == 0x81:
        return "noSuchInstance"
    if tag == 0x82:
        return "endOfMibView"
    return val.hex()


def _ber_parse(data: bytes, offset: int = 0) -> list[tuple[int, bytes]]:
    """Shallow parse of BER TLVs starting at offset. Returns [(tag, value), ...]."""
    result: list[tuple[int, bytes]] = []
    n, i = len(data), offset
    while i + 1 < n:
        tag = data[i]; i += 1
        if data[i] & 0x80:
            nb = data[i] & 0x7F
            if not nb or i + nb >= n:
                break
            i += 1
            ln = int.from_bytes(data[i:i + nb], "big")
            i += nb
        else:
            ln = data[i]; i += 1
        if i + ln > n:
            break
        result.append((tag, data[i:i + ln]))
        i += ln
    return result


def _parse_varbinds(response: bytes) -> list[tuple[str, int, bytes]]:
    """Extract (oid_dotted, value_tag, value_bytes) from a GET/GETNEXT/GETBULK response."""
    outer = _ber_parse(response)
    if not outer or outer[0][0] != 0x30:
        return []
    msg_parts = _ber_parse(outer[0][1])
    # Find PDU: GetResponse (0xa2) or report (0xa8)
    pdu_bytes = next((v for t, v in msg_parts if t in (0xa2, 0xa8)), None)
    if pdu_bytes is None:
        return []
    pdu_parts = _ber_parse(pdu_bytes)
    if len(pdu_parts) < 4:
        return []
    _, vbl_bytes = pdu_parts[3]
    result: list[tuple[str, int, bytes]] = []
    for _, vb_bytes in _ber_parse(vbl_bytes):
        vb_parts = _ber_parse(vb_bytes)
        if len(vb_parts) < 2:
            continue
        oid_tag, oid_bytes = vb_parts[0]
        val_tag, val_bytes = vb_parts[1]
        if oid_tag != 0x06:
            continue
        result.append((_decode_oid(oid_bytes), val_tag, val_bytes))
    return result


# ── PDU builders ─────────────────────────────────────────────────────────────

def _oid_tlv(oid_bytes: bytes) -> bytes:
    return b"\x06" + _ber_len(len(oid_bytes)) + oid_bytes


def _varbind(oid_bytes: bytes) -> bytes:
    inner = _oid_tlv(oid_bytes) + b"\x05\x00"
    return b"\x30" + _ber_len(len(inner)) + inner


def _varbind_list(*oid_bytes_list: bytes) -> bytes:
    content = b"".join(_varbind(ob) for ob in oid_bytes_list)
    return b"\x30" + _ber_len(len(content)) + content


def _snmp_msg(version: int, community: str, pdu_tag: int, pdu_body: bytes) -> bytes:
    comm = community.encode()
    comm_tlv = b"\x04" + _ber_len(len(comm)) + comm
    ver_tlv = b"\x02\x01" + bytes([version])
    pdu = bytes([pdu_tag]) + _ber_len(len(pdu_body)) + pdu_body
    msg = ver_tlv + comm_tlv + pdu
    return b"\x30" + _ber_len(len(msg)) + msg


def _req_id_tlv(req_id: int = 1) -> bytes:
    rb = req_id.to_bytes(2, "big")
    return b"\x02" + bytes([len(rb)]) + rb


def _build_get(community: str, oid: bytes, req_id: int = 1) -> bytes:
    vbl = _varbind_list(oid)
    pdu_body = _req_id_tlv(req_id) + b"\x02\x01\x00\x02\x01\x00" + vbl
    return _snmp_msg(0, community, 0xa0, pdu_body)  # 0xa0 = GetRequest


def _build_getnext(community: str, oid: bytes, req_id: int = 1) -> bytes:
    vbl = _varbind_list(oid)
    pdu_body = _req_id_tlv(req_id) + b"\x02\x01\x00\x02\x01\x00" + vbl
    return _snmp_msg(0, community, 0xa1, pdu_body)  # 0xa1 = GetNextRequest (v1)


def _build_getbulk_v2c(community: str, oid: bytes,
                        max_reps: int = 20, req_id: int = 1) -> bytes:
    vbl = _varbind_list(oid)
    non_rep = b"\x02\x01\x00"
    max_rep = b"\x02\x01" + bytes([max_reps])
    pdu_body = _req_id_tlv(req_id) + non_rep + max_rep + vbl
    return _snmp_msg(1, community, 0xa5, pdu_body)  # 0xa5 = GetBulkRequest (v2c)


_SNMPv3_DISCOVERY = (
    b"\x30\x3a"
    b"\x02\x01\x03"                       # msgVersion = 3
    b"\x30\x0f"                           # msgGlobalData
    b"\x02\x04\x00\x00\x00\x01"          #   msgID
    b"\x02\x02\x05\xdc"                   #   msgMaxSize = 1500
    b"\x04\x01\x04"                       #   msgFlags = reportable
    b"\x02\x01\x03"                       #   msgSecurityModel = USM
    b"\x04\x10"                           # msgSecurityParameters (empty USM)
    b"\x30\x00\x02\x01\x00\x02\x01\x00"
    b"\x04\x00\x04\x00\x04\x00"
    b"\x30\x12"                           # ScopedPDU
    b"\x04\x00\x04\x00"                   #   contextEngineID, contextName
    b"\xa0\x0a"                           #   GetRequest PDU
    b"\x02\x01\x01\x02\x01\x00\x02\x01\x00\x30\x00"
)

# ── High-value OID subtrees for targeted walk ────────────────────────────────

_WALK_SUBTREES: dict[str, str] = {
    "sysName":      "1.3.6.1.2.1.1.5",
    "sysContact":   "1.3.6.1.2.1.1.4",
    "sysLocation":  "1.3.6.1.2.1.1.6",
    "sysUpTime":    "1.3.6.1.2.1.1.3",
    "ifDescr":      "1.3.6.1.2.1.2.2.1.2",
    "ifPhysAddr":   "1.3.6.1.2.1.2.2.1.6",
    "ifOperStatus": "1.3.6.1.2.1.2.2.1.8",
    "ipAddrTable":  "1.3.6.1.2.1.4.20.1.1",
    "arpTable":     "1.3.6.1.2.1.4.22.1.2",
    "tcpConnPorts": "1.3.6.1.2.1.6.13.1.3",
    "hrSWRunName":  "1.3.6.1.2.1.25.4.2.1.2",
}

_SYSDESCR_OID = _encode_oid("1.3.6.1.2.1.1.1.0")


def _oid_in_subtree(child: str, parent: str) -> bool:
    c, p = child.split("."), parent.split(".")
    return len(c) > len(p) and c[:len(p)] == p


class SNMPScanner(BaseScanner):
    """
    Phase 1 (community discovery) + Phase 2 (targeted MIB walk) +
    Phase 3 (amplification check) + Phase 4 (SNMPv3 detection).
    """
    name = "snmp_scan"

    def __init__(self, *args, port: int = 161,
                 communities: list[str] | None = None,
                 walk: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = port
        self.communities = communities or COMMON_COMMUNITIES
        self.walk = walk

    def _udp(self, target: str, payload: bytes,
             recvbuf: int = 8192) -> bytes | None:
        try:
            family, sockaddr = resolve(target, self.port, proto="udp")
        except OSError:
            return None
        sock = socket.socket(family, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        try:
            sock.sendto(payload, sockaddr)
            data, _ = sock.recvfrom(recvbuf)
            return data
        except (socket.timeout, OSError):
            return None
        finally:
            sock.close()

    def _discover_community(self, target: str) -> tuple[str, str | None] | None:
        """Return (community, sysdescr) for the first responding community, or None."""
        for comm in self.communities:
            pkt = _build_get(comm, _SYSDESCR_OID)
            resp = self._udp(target, pkt)
            if resp:
                varbinds = _parse_varbinds(resp)
                sysdescr = next(
                    (_decode_value(t, v) for _, t, v in varbinds if t == 0x04),
                    None)
                return comm, sysdescr
        return None

    def _walk_subtree(self, target: str, community: str,
                      subtree_oid: str, max_rows: int = 30) -> list[tuple[str, str]]:
        """GETNEXT walk of one OID subtree.  Returns [(oid, value_str), ...]."""
        current_oid = _encode_oid(subtree_oid)
        current_dotted = subtree_oid
        rows: list[tuple[str, str]] = []
        for _ in range(max_rows):
            pkt = _build_getnext(community, current_oid)
            resp = self._udp(target, pkt, recvbuf=4096)
            if not resp:
                break
            varbinds = _parse_varbinds(resp)
            if not varbinds:
                break
            oid_str, val_tag, val_bytes = varbinds[0]
            if val_tag in (0x80, 0x81, 0x82):  # noSuch*/endOfMibView
                break
            if not _oid_in_subtree(oid_str, subtree_oid):
                break
            rows.append((oid_str, _decode_value(val_tag, val_bytes)))
            current_dotted = oid_str
            current_oid = _encode_oid(oid_str)
        return rows

    def _amplification_factor(self, target: str, community: str) -> float | None:
        """One GETBULK request — measure response/request size ratio."""
        # Walk interface table as a representative payload
        oid = _encode_oid("1.3.6.1.2.1.2.2.1.2")
        pkt = _build_getbulk_v2c(community, oid, max_reps=20)
        resp = self._udp(target, pkt, recvbuf=16384)
        if not resp or not pkt:
            return None
        return round(len(resp) / len(pkt), 2)

    def _snmpv3_present(self, target: str) -> bool:
        """Send a SNMPv3 Discover. Any reply = v3 agent present."""
        resp = self._udp(target, _SNMPv3_DISCOVERY)
        return resp is not None and len(resp) > 4

    async def scan_target(self, target: str) -> list[ScanResult]:
        loop = asyncio.get_running_loop()

        # Phase 1 — community discovery
        await self.limiter.wait()
        async with self.sem:
            found = await loop.run_in_executor(
                None, self._discover_community, target)

        if not found:
            # Phase 4 — SNMPv3 check even if v1/v2c failed
            await self.limiter.wait()
            async with self.sem:
                v3 = await loop.run_in_executor(
                    None, self._snmpv3_present, target)
            if v3:
                return [ScanResult(
                    self.name, target, port=self.port, proto="udp",
                    status="open",
                    data={"snmpv3_present": True, "v1v2c_community": None},
                    evidence="SNMPv3 agent detected (v1/v2c communities did not match)")]
            # No SNMP reply is NOT proof of a firewall: the agent may simply
            # reject our communities/versions while the UDP port is open. Absent
            # an ICMP unreachable, the only honest state is the open|filtered pair
            # (matches the udp_scanner semantics — do not overclaim "filtered").
            return [ScanResult(
                self.name, target, port=self.port, proto="udp",
                status="open|filtered",
                data={"responded": False, "reason": "no_snmp_response"},
                evidence="no SNMP reply to common communities (open|filtered)")]

        community, sysdescr = found
        data: dict = {
            "community": community,
            "sysdescr": sysdescr,
            "responded": True,
        }

        if self.walk:
            # Phase 2 — targeted MIB walk
            mib_data: dict[str, list] = {}
            for name, oid in _WALK_SUBTREES.items():
                await self.limiter.wait()
                async with self.sem:
                    rows = await loop.run_in_executor(
                        None, self._walk_subtree, target, community, oid)
                if rows:
                    # Return only values (drop OID path) for readability
                    mib_data[name] = [v for _, v in rows]
            data["mib"] = mib_data

            # Phase 3 — amplification factor
            await self.limiter.wait()
            async with self.sem:
                baf = await loop.run_in_executor(
                    None, self._amplification_factor, target, community)
            data["amplification_factor"] = baf

            # Phase 4 — SNMPv3 presence
            await self.limiter.wait()
            async with self.sem:
                v3 = await loop.run_in_executor(
                    None, self._snmpv3_present, target)
            data["snmpv3_present"] = v3

        evidence = (f"community '{community}'"
                    + (f" -> {sysdescr[:100]}" if sysdescr else ""))
        return [ScanResult(
            self.name, target, port=self.port, proto="udp",
            status="open", data=data, evidence=evidence)]


def main() -> None:
    parser = base_argparser("SNMP enumeration scanner (read-only, MIB walk)")
    parser.add_argument("--port", type=int, default=161)
    parser.add_argument("--communities", default=None,
                        help="comma-separated community strings (default: common list)")
    parser.add_argument("--no-walk", action="store_true",
                        help="skip MIB walk (community discovery only)")
    args = parser.parse_args()
    setup_logging(args.verbose)
    communities = (args.communities.split(",") if args.communities
                   else COMMON_COMMUNITIES)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = SNMPScanner(scope, rate=args.rate, concurrency=args.concurrency,
                              timeout=args.timeout, port=args.port,
                              communities=communities, walk=not args.no_walk)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
