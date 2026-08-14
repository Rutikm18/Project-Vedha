"""
syn_scanner.py — stateless TCP SYN (half-open) scan, pure Python (Tier 1.1).

WHY: a full TCP connect() completes the 3-way handshake — slow, heavily logged,
and it ties up an OS socket per port. A SYN scan sends a lone SYN and reads the
reply: SYN/ACK = open, RST = closed, silence = filtered. It never sends the final
ACK, so the connection is never established (the kernel, having no socket for our
hand-crafted SYN, tears down any SYN/ACK with an automatic RST). Far faster and
quieter, and it needs only one packet out + one in per port.

STATELESS DESIGN (masscan technique): we do NOT keep a table of outstanding
probes. Instead the TCP initial sequence number (ISN) of each SYN is a keyed hash
— a "SYN cookie" — of (dst_ip, dst_port, src_port). A genuine SYN/ACK reply
acknowledges our ISN+1, so `reply.ack - 1` must equal the cookie recomputed from
the reply's own addressing. This validates replies with zero per-probe state and
rejects stray/forged packets.

PLATFORM REALITY (why there's a fallback):
  * Raw sockets require root / CAP_NET_RAW.
  * BSD/macOS raw sockets CANNOT receive TCP (the kernel consumes it before it
    reaches a raw socket) — so the SYN path is Linux-only in practice.
Therefore `syn_scan_supported()` gates on Linux + a usable raw socket, and when
it is False the scanner transparently falls back to the unprivileged connect
scan (PortScanner). Same ScanResult schema either way; results carry
data["method"] = "syn" | "connect_fallback" so accuracy is measurable per path.

COLLECTION ONLY: sends SYNs and reads replies. No handshake completion, no
payload, no exploitation.
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import os
import random
import socket
import struct
import sys
import time

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, resolve, TOP_TCP_PORTS, setup_logging, base_argparser,
    main_entrypoint, LOG, inet_checksum as _checksum,
)
from .port_scanner import PortScanner

# TCP flag bits
TCP_FIN = 0x01
TCP_SYN = 0x02
TCP_RST = 0x04
TCP_PSH = 0x08
TCP_ACK = 0x10


# ── packet crafting ───────────────────────────────────────────────────────────

def build_ip_header(src_ip: str, dst_ip: str, payload_len: int, *,
                    ttl: int = 64, proto: int = socket.IPPROTO_TCP,
                    ident: int | None = None) -> bytes:
    """
    Build a 20-byte IPv4 header with a valid checksum.

    NOTE (BSD caveat): on macOS/BSD, IP_HDRINCL sends expect total-length and
    fragment-offset in HOST byte order. This builder uses network byte order,
    which is correct for Linux (the only platform where the SYN send path runs).
    """
    version_ihl = (4 << 4) | 5
    tos = 0
    total_len = 20 + payload_len
    ident = random.randint(0, 0xFFFF) if ident is None else ident
    flags_frag = 0x4000                       # Don't Fragment
    zero_checksum = struct.pack(
        "!BBHHHBBH4s4s", version_ihl, tos, total_len, ident, flags_frag,
        ttl, proto, 0, socket.inet_aton(src_ip), socket.inet_aton(dst_ip))
    chk = _checksum(zero_checksum)
    return struct.pack(
        "!BBHHHBBH4s4s", version_ihl, tos, total_len, ident, flags_frag,
        ttl, proto, chk, socket.inet_aton(src_ip), socket.inet_aton(dst_ip))


def build_tcp_syn(src_ip: str, dst_ip: str, src_port: int, dst_port: int,
                  seq: int, *, window: int = 1024) -> bytes:
    """Build a 20-byte TCP SYN segment with a valid checksum (pseudo-header)."""
    data_offset = (5 << 4)                    # 5 * 4 = 20 bytes, no options
    flags = TCP_SYN
    seq &= 0xFFFFFFFF
    header = struct.pack("!HHIIBBHHH", src_port, dst_port, seq, 0,
                         data_offset, flags, window, 0, 0)
    pseudo = (socket.inet_aton(src_ip) + socket.inet_aton(dst_ip) +
              struct.pack("!BBH", 0, socket.IPPROTO_TCP, len(header)))
    chk = _checksum(pseudo + header)
    return struct.pack("!HHIIBBHHH", src_port, dst_port, seq, 0,
                       data_offset, flags, window, chk, 0)


def build_syn_packet(src_ip: str, dst_ip: str, src_port: int, dst_port: int,
                     seq: int, *, window: int = 1024) -> bytes:
    tcp = build_tcp_syn(src_ip, dst_ip, src_port, dst_port, seq, window=window)
    ip = build_ip_header(src_ip, dst_ip, payload_len=len(tcp))
    return ip + tcp


def parse_packet(raw: bytes) -> dict | None:
    """Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket)."""
    if len(raw) < 20:
        return None
    ihl = (raw[0] & 0x0F) * 4
    if ihl < 20 or len(raw) < ihl + 20:
        return None
    ip_src = socket.inet_ntoa(raw[12:16])
    ip_dst = socket.inet_ntoa(raw[16:20])
    tcp = raw[ihl:ihl + 20]
    (src_port, dst_port, seq, ack, _off, flags, _win, _chk,
     _urg) = struct.unpack("!HHIIBBHHH", tcp)
    return {"ip_src": ip_src, "ip_dst": ip_dst, "src_port": src_port,
            "dst_port": dst_port, "seq": seq, "ack": ack, "flags": flags}


def classify(flags: int) -> str | None:
    """SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)."""
    if (flags & TCP_SYN) and (flags & TCP_ACK):
        return "open"
    if flags & TCP_RST:
        return "closed"
    return None


# ── stateless SYN cookie ──────────────────────────────────────────────────────

def syn_cookie(dst_ip: str, dst_port: int, src_port: int, key: bytes) -> int:
    """Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1."""
    msg = f"{dst_ip}|{dst_port}|{src_port}".encode()
    digest = hmac.new(key, msg, hashlib.sha256).digest()
    return int.from_bytes(digest[:4], "big")


def verify_reply_cookie(parsed: dict, our_src_port: int, key: bytes) -> bool:
    """
    A genuine reply to our SYN acknowledges ISN+1. The reply's own source
    (ip_src, src_port) is the (host, port) we probed, so recomputing the cookie
    from the reply and comparing to ack-1 validates it with no stored state.
    """
    expected = syn_cookie(parsed["ip_src"], parsed["src_port"], our_src_port, key)
    return parsed["ack"] == ((expected + 1) & 0xFFFFFFFF)


# ── capability detection ──────────────────────────────────────────────────────

def syn_scan_supported(*, platform: str | None = None,
                       socket_factory=None) -> bool:
    """
    True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't
    receive TCP) AND a raw socket can actually be created (root/CAP_NET_RAW).
    Dependency-injected for testing.
    """
    platform = platform if platform is not None else sys.platform
    if not platform.startswith("linux"):
        return False
    if socket_factory is None:
        def socket_factory():
            return socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                 socket.IPPROTO_TCP)
    try:
        s = socket_factory()
        s.close()
        return True
    except (PermissionError, OSError):
        return False


def _local_source_ip(dst_ip: str) -> str:
    """Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((dst_ip, 80))
        return s.getsockname()[0]
    except OSError:
        return "0.0.0.0"
    finally:
        s.close()


# ── scanner ───────────────────────────────────────────────────────────────────

class SynScanner(BaseScanner):
    """
    SYN scan on privileged Linux; transparent connect-scan fallback elsewhere.
    """
    name = "syn_scan"

    def __init__(self, *args, ports: list[int] | None = None,
                 key: bytes | None = None, report_closed: bool = False,
                 force_fallback: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = list(TOP_TCP_PORTS if ports is None else ports)
        self.report_closed = report_closed
        self._key = key or os.urandom(16)
        self._rate = kwargs.get("rate", 200.0)
        self._supported = (not force_fallback) and syn_scan_supported()
        self._fallback: PortScanner | None = None
        if not self._supported:
            self._fallback = PortScanner(
                self.scope, rate=self._rate, concurrency=self._concurrency,
                timeout=self.timeout, ports=self.ports,
                report_closed=self.report_closed)

    async def scan_target(self, target: str) -> list[ScanResult]:
        if self._supported:
            try:
                return await self._syn_scan_target(target)
            except (PermissionError, OSError) as exc:
                # Lost the capability mid-run (e.g. dropped privileges) — degrade
                # to a connect scan rather than failing the target.
                LOG.warning("syn scan unavailable (%s); falling back to connect", exc)
                self._supported = False
                self._fallback = PortScanner(
                    self.scope, rate=self._rate, concurrency=self._concurrency,
                    timeout=self.timeout, ports=self.ports,
                    report_closed=self.report_closed)
        return await self._fallback_scan(target)

    async def _fallback_scan(self, target: str) -> list[ScanResult]:
        results = await self._fallback.scan_target(target)
        for r in results:
            r.scanner = self.name
            r.data = {**(r.data or {}), "method": "connect_fallback"}
        return results

    # -- SYN path (Linux, privileged; not exercised in the macOS/dev test env) --
    async def _syn_scan_target(self, target: str) -> list[ScanResult]:
        loop = asyncio.get_running_loop()
        await self.limiter.wait()
        return await loop.run_in_executor(None, self._syn_scan_blocking, target)

    def _syn_scan_blocking(self, target: str) -> list[ScanResult]:
        family, sockaddr = resolve(target, 0, proto="tcp")
        if family != socket.AF_INET:
            # This raw implementation is IPv4-only; signal fallback.
            raise OSError("syn scan is IPv4-only")
        dst_ip = sockaddr[0]
        src_ip = _local_source_ip(dst_ip)
        src_port = random.randint(40000, 60000)

        send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_RAW)
        send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_TCP)
        recv_sock.setblocking(False)

        try:
            # Blast one SYN per port (stateless — ISN carries the cookie).
            for port in self.ports:
                seq = syn_cookie(dst_ip, port, src_port, self._key)
                pkt = build_syn_packet(src_ip, dst_ip, src_port, port, seq)
                try:
                    send_sock.sendto(pkt, (dst_ip, 0))
                except OSError as exc:
                    LOG.debug("send SYN %s:%d failed: %s", dst_ip, port, exc)

            # Collect replies within a bounded window.
            states: dict[int, str] = {}
            deadline = time.monotonic() + max(self.timeout, 1.0)
            while time.monotonic() < deadline and len(states) < len(self.ports):
                try:
                    raw = recv_sock.recv(65535)
                except BlockingIOError:
                    time.sleep(0.005)
                    continue
                except OSError:
                    break
                parsed = parse_packet(raw)
                if not parsed or parsed["ip_src"] != dst_ip:
                    continue
                if parsed["dst_port"] != src_port:
                    continue
                if not verify_reply_cookie(parsed, src_port, self._key):
                    continue
                verdict = classify(parsed["flags"])
                if verdict:
                    states.setdefault(parsed["src_port"], verdict)
        finally:
            send_sock.close()
            recv_sock.close()

        results: list[ScanResult] = []
        for port in self.ports:
            state = states.get(port)
            if state == "open":
                results.append(ScanResult(
                    self.name, target, port=port, proto="tcp", status="open",
                    data={"method": "syn"}, evidence="syn/ack received"))
            elif state == "closed" and self.report_closed:
                results.append(ScanResult(
                    self.name, target, port=port, proto="tcp", status="closed",
                    data={"method": "syn"}, evidence="rst received"))
            elif state is None and self.report_closed:
                results.append(ScanResult(
                    self.name, target, port=port, proto="tcp", status="filtered",
                    data={"method": "syn"}, evidence="no reply (open|filtered)"))
        return results


def main() -> None:
    parser = base_argparser("Stateless TCP SYN scanner (connect-scan fallback)")
    parser.add_argument("-p", "--ports", default=None,
                        help="ports e.g. '22,80,443,8000-8100' (default: top ports)")
    parser.add_argument("--report-closed", action="store_true",
                        help="also emit closed/filtered results (noisier)")
    parser.add_argument("--force-fallback", action="store_true",
                        help="skip the raw SYN path and use the connect scan")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else None
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = SynScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports,
                             report_closed=args.report_closed,
                             force_fallback=args.force_fallback)
        if scanner._supported:
            LOG.info("[syn_scan] raw SYN path active")
        else:
            LOG.info("[syn_scan] using connect-scan fallback (unprivileged/non-Linux)")
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
