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

from .adaptive_timeout import AdaptiveTimeout
from .os_fingerprint import fingerprint_os
from .port_scanner import _NMAP_TOP_100, PortScanner
from .scanner_base import (
    LOG,
    BaseScanner,
    ResultWriter,
    ScanResult,
    ScopeGuard,
    base_argparser,
    choose_source_port,
    expand_targets,
    main_entrypoint,
    parse_ports,
    resolve,
    setup_logging,
)
from .scanner_base import (
    inet_checksum as _checksum,
)

# TCP option kinds we harvest from a SYN/ACK.
_TCP_OPT_EOL = 0
_TCP_OPT_NOP = 1
_TCP_OPT_MSS = 2
_TCP_OPT_WSCALE = 3
_TCP_OPT_SACKOK = 4
_TCP_OPT_TIMESTAMP = 8

# p0f "olayout" tokens: a compact, order-preserving encoding of the TCP option
# sequence. The ORDER and presence of options is one of p0f v3's strongest OS
# discriminators (Windows, Linux and the BSDs each emit a characteristic layout),
# so we preserve it rather than only extracting MSS.
_OPT_TOKEN = {_TCP_OPT_EOL: "E", _TCP_OPT_NOP: "N", _TCP_OPT_MSS: "M",
              _TCP_OPT_WSCALE: "W", _TCP_OPT_SACKOK: "S", _TCP_OPT_TIMESTAMP: "T"}

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


def parse_tcp_options(opts: bytes) -> dict:
    """Walk a TCP options field into a p0f-style profile.

    Returns {mss, wscale, sack_ok, timestamps, olayout} where `olayout` is the
    order-preserving token string (e.g. "MSTNW" for the classic Linux SYN/ACK).
    Bounds-checked and tolerant of attacker-controlled bytes: EOL ends the walk,
    NOP is a single byte, every other option is stepped by its own length; a
    malformed tail simply truncates the profile — it never raises.
    """
    out: dict = {"mss": None, "wscale": None, "sack_ok": False,
                 "timestamps": False, "olayout": ""}
    layout: list[str] = []
    i, n = 0, len(opts)
    while i < n:
        kind = opts[i]
        layout.append(_OPT_TOKEN.get(kind, "?"))
        if kind == _TCP_OPT_EOL:
            break
        if kind == _TCP_OPT_NOP:
            i += 1
            continue
        if i + 1 >= n:
            break
        length = opts[i + 1]
        if length < 2 or i + length > n:
            break
        if kind == _TCP_OPT_MSS and length == 4:
            out["mss"] = int.from_bytes(opts[i + 2:i + 4], "big")
        elif kind == _TCP_OPT_WSCALE and length == 3:
            out["wscale"] = opts[i + 2]
        elif kind == _TCP_OPT_SACKOK and length == 2:
            out["sack_ok"] = True
        elif kind == _TCP_OPT_TIMESTAMP and length == 10:
            out["timestamps"] = True
        i += length
    out["olayout"] = "".join(layout)
    return out


def _parse_mss(opts: bytes) -> int | None:
    """Back-compat shim: MSS only. New code uses parse_tcp_options()."""
    return parse_tcp_options(opts)["mss"]


def parse_packet(raw: bytes) -> dict | None:
    """Parse a raw IPv4+TCP packet (as received on a raw IPPROTO_TCP socket).

    Also surfaces the sender's stack signals — IP TTL, TCP window, and the MSS
    option when present — which are free OS-fingerprint hints on a SYN/ACK.
    """
    if len(raw) < 20:
        return None
    ihl = (raw[0] & 0x0F) * 4
    if ihl < 20 or len(raw) < ihl + 20:
        return None
    ttl = raw[8]
    ip_src = socket.inet_ntoa(raw[12:16])
    ip_dst = socket.inet_ntoa(raw[16:20])
    tcp = raw[ihl:ihl + 20]
    (src_port, dst_port, seq, ack, off, flags, win, _chk,
     _urg) = struct.unpack("!HHIIBBHHH", tcp)
    # TCP options (present when the data offset exceeds the 20-byte base header)
    # carry MSS, window scale, SACK/timestamp support and — crucially — their
    # ORDER, a strong p0f OS signal. Parse the full profile defensively.
    opts: dict = {"mss": None, "wscale": None, "sack_ok": False,
                  "timestamps": False, "olayout": ""}
    data_off = (off >> 4) * 4
    if data_off > 20 and len(raw) >= ihl + data_off:
        opts = parse_tcp_options(raw[ihl + 20:ihl + data_off])
    return {"ip_src": ip_src, "ip_dst": ip_dst, "src_port": src_port,
            "dst_port": dst_port, "seq": seq, "ack": ack, "flags": flags,
            "window": win, "ttl": ttl, "mss": opts["mss"],
            "wscale": opts["wscale"], "sack_ok": opts["sack_ok"],
            "timestamps": opts["timestamps"], "olayout": opts["olayout"]}


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
                 force_fallback: bool = False, retries: int = 2,
                 adaptive_timeout: bool = True, source_port: int | None = None,
                 randomize: bool = False, scan_delay: float = 0.0, **kwargs):
        super().__init__(*args, **kwargs)
        # Default to nmap top-100 (not the 35-port TOP_TCP_PORTS): a no-arg scan
        # shouldn't silently miss common services.
        self.ports = list(_NMAP_TOP_100 if ports is None else ports)
        self.report_closed = report_closed
        # Per-host RTT-adaptive recv window (Jacobson/Karels), matching the
        # connect path. Without it the SYN path used a FIXED timeout and thus
        # mislabeled slow-WAN OPEN ports as filtered (and wasted time on LAN).
        self.adaptive_timeout = adaptive_timeout
        # A raw SYN gets ZERO kernel retransmit (unlike connect(), where the OS
        # stack resends the SYN several times). So a lone dropped SYN/SYN-ACK is
        # a false `filtered` unless WE resend. Retransmit silent ports only, for
        # `retries` extra rounds; a definitive SYN-ACK/RST ends a port early.
        # Default 2 (higher than the connect scan's 1, which rides on kernel
        # retransmits) to match connect-scan reliability.
        self.retries = max(0, retries)
        self.source_port = source_port          # fixed TCP src port, or None = random
        self._key = key or os.urandom(16)
        self._rate = kwargs.get("rate", 200.0)
        self._supported = (not force_fallback) and syn_scan_supported()
        self._fallback: PortScanner | None = None
        if not self._supported:
            self._fallback = PortScanner(
                self.scope, rate=self._rate, concurrency=self._concurrency,
                timeout=self.timeout, ports=self.ports,
                report_closed=self.report_closed, source_port=source_port,
                randomize=randomize, scan_delay=scan_delay)

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
        src_port = choose_source_port(self.source_port)

        send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_RAW)
        send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_TCP)
        recv_sock.setblocking(False)

        # One adaptive timer per host: it warms from each SYN-ACK/RST round-trip,
        # so later rounds wait exactly as long as this path actually needs.
        est = (AdaptiveTimeout(base=self.timeout,
                               minimum=min(0.3, self.timeout),
                               maximum=max(self.timeout, 8.0))
               if self.adaptive_timeout else None)

        states: dict[int, str] = {}
        attempts_by_port: dict[int, int] = {}
        # Per-port harvested intel: rtt_ms + the SYN/ACK's stack signals.
        meta: dict[int, dict] = {}
        try:
            # Retransmit loop: each round SYNs only the still-silent ports, then
            # collects replies. A definitive SYN-ACK/RST resolves a port and drops
            # it from `pending`; only silence carries to the next round. This is
            # the direct fix for the SYN path's false negatives — a lost SYN or
            # SYN-ACK gets another chance instead of being reported `filtered`.
            #
            # Ports are shuffled: a randomized order spreads the burst across the
            # target's port range (fewer self-induced drops) and defeats trivial
            # sequential-scan detection — masscan/nmap do the same.
            pending = random.sample(self.ports, len(self.ports))
            rounds = self.retries + 1
            for _round in range(rounds):
                if not pending:
                    break
                # Send a SYN per pending port (stateless — ISN carries the cookie).
                # Record the send instant so a reply yields a real round-trip time.
                send_at: dict[int, float] = {}
                for port in pending:
                    attempts_by_port[port] = attempts_by_port.get(port, 0) + 1
                    seq = syn_cookie(dst_ip, port, src_port, self._key)
                    pkt = build_syn_packet(src_ip, dst_ip, src_port, port, seq)
                    try:
                        send_sock.sendto(pkt, (dst_ip, 0))
                        send_at[port] = time.monotonic()
                    except OSError as exc:
                        LOG.debug("send SYN %s:%d failed: %s", dst_ip, port, exc)

                # Collect replies for this round within the adaptive window.
                pending_set = set(pending)
                window = est.timeout() if est is not None else self.timeout
                deadline = time.monotonic() + max(window, 1.0)
                while time.monotonic() < deadline and pending_set:
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
                    if not verdict:
                        continue
                    rport = parsed["src_port"]
                    states.setdefault(rport, verdict)
                    pending_set.discard(rport)
                    # Fold the real round-trip into the adaptive timer + record it.
                    sent = send_at.get(rport)
                    if sent is not None:
                        rtt_ms = round((time.monotonic() - sent) * 1000, 2)
                        if est is not None:
                            est.observe(rtt_ms / 1000.0)
                        meta.setdefault(rport, {})["rtt_ms"] = rtt_ms
                    # Harvest the SYN/ACK's stack signals — free OS-fingerprint
                    # data (window/TTL/MSS) that was previously parsed & discarded.
                    if verdict == "open":
                        m = meta.setdefault(rport, {})
                        m["tcp_window"] = parsed.get("window")
                        m["ip_ttl"] = parsed.get("ttl")
                        if parsed.get("mss") is not None:
                            m["mss"] = parsed["mss"]
                        if parsed.get("wscale") is not None:
                            m["wscale"] = parsed["wscale"]
                        if parsed.get("olayout"):
                            m["olayout"] = parsed["olayout"]
                # Only ports still unresolved go to the next round.
                pending = [p for p in pending if p not in states]
        finally:
            send_sock.close()
            recv_sock.close()

        return self._build_results(target, states, attempts_by_port, meta)

    def _build_results(self, target: str, states: dict[int, str],
                       attempts_by_port: dict[int, int],
                       meta: dict[int, dict]) -> list[ScanResult]:
        """Turn resolved port states + harvested intel into ScanResults. Pure —
        no sockets — so the emit logic (incl. the OS-fingerprint enrichment) is
        unit-testable without a raw socket."""
        results: list[ScanResult] = []
        for port in self.ports:
            state = states.get(port)
            attempts = attempts_by_port.get(port, 1)
            m = meta.get(port, {})
            if state == "open":
                data: dict = {"method": "syn"}
                if attempts > 1:
                    data["attempts"] = attempts
                if "rtt_ms" in m:
                    data["rtt_ms"] = m["rtt_ms"]
                # Attach the harvested stack signals and a best-guess OS family.
                win, ttl, mss = m.get("tcp_window"), m.get("ip_ttl"), m.get("mss")
                wscale, olayout = m.get("wscale"), m.get("olayout")
                if win is not None:
                    data["tcp_window"] = win
                if ttl is not None:
                    data["ip_ttl"] = ttl
                if mss is not None:
                    data["mss"] = mss
                if wscale is not None:
                    data["tcp_wscale"] = wscale
                if olayout:
                    data["tcp_olayout"] = olayout
                if win is not None or ttl is not None or mss is not None:
                    # TTL here is read from the SYN/ACK's IP header — tag it TCP so
                    # nothing downstream can present it as an ICMP-derived result.
                    fp = fingerprint_os(ttl=ttl, tcp_window=win, mss=mss,
                                        ttl_source="tcp_synack",
                                        wscale=wscale, olayout=olayout)
                    if fp["os_guess"] != "unknown":
                        data["os_guess"] = fp["os_guess"]
                        data["os_confidence"] = fp["confidence"]
                        # Provenance travels with the guess: this OS family was
                        # inferred from a TCP SYN/ACK, not an ICMP echo.
                        data["os_ttl_source"] = fp["signals"].get("ttl_source")
                    # p0f-style specific stack label (Linux/Windows/BSD/…), when
                    # the option layout matched a known signature.
                    if fp.get("stack_guess"):
                        data["os_stack"] = fp["stack_guess"]
                        data["os_stack_confidence"] = fp["signals"].get("stack_confidence")
                results.append(ScanResult(
                    self.name, target, port=port, proto="tcp", status="open",
                    data=data, evidence="syn/ack received"))
            elif state == "closed" and self.report_closed:
                data = {"method": "syn"}
                if attempts > 1:
                    data["attempts"] = attempts
                if "rtt_ms" in m:
                    data["rtt_ms"] = m["rtt_ms"]
                results.append(ScanResult(
                    self.name, target, port=port, proto="tcp", status="closed",
                    data=data, evidence="rst received"))
            elif state is None and self.report_closed:
                results.append(ScanResult(
                    self.name, target, port=port, proto="tcp", status="filtered",
                    data={"method": "syn", "attempts": attempts},
                    evidence=f"no reply after {attempts} SYN(s) (open|filtered)"))
        return results


def main() -> None:
    parser = base_argparser("Stateless TCP SYN scanner (connect-scan fallback)")
    parser.add_argument("-p", "--ports", default=None,
                        help="ports e.g. '22,80,443,8000-8100' (default: nmap top-100)")
    parser.add_argument("--report-closed", action="store_true",
                        help="also emit closed/filtered results (noisier)")
    parser.add_argument("--force-fallback", action="store_true",
                        help="skip the raw SYN path and use the connect scan")
    parser.add_argument("--retries", type=int, default=2,
                        help="extra SYN retransmit rounds on silence only "
                             "(default 2; 0 = single SYN). SYN-ACK/RST ends a "
                             "port early and is never retried.")
    parser.add_argument("--fixed-timeout", action="store_true",
                        help="disable the per-host RTT-adaptive recv window; use "
                             "the fixed --timeout instead")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else None
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = SynScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports,
                             report_closed=args.report_closed,
                             force_fallback=args.force_fallback,
                             retries=args.retries,
                             adaptive_timeout=not args.fixed_timeout,
                             source_port=args.source_port,
                             randomize=args.randomize, scan_delay=args.scan_delay)
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
