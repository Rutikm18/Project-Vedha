"""
os_fingerprint.py — OS/stack fingerprinting via ICMP + TTL (Tier 2.1 + 2.2).

TWO CAPABILITIES:
  (2.2) ICMP multi-probe discovery + TTL harvest — send ICMP echo (and,
        optionally, timestamp / address-mask) and read the reply. A host that
        drops all TCP may still answer ICMP; and the reply's IP TTL is a strong
        OS-family signal.
  (2.1) OS fingerprint — infer the OS family from the observed TTL (rounded up to
        the sender's initial TTL of 64/128/255) plus, when available, TCP window
        size and MSS gathered by other scanners. Pure heuristic scoring.

WHY TTL WORKS: hosts set a fixed initial TTL — Linux/Unix/macOS 64, Windows 128,
many network devices/Solaris 255 — decremented once per hop. Rounding the
observed TTL up to the nearest of {64,128,255} recovers the initial value (and
the difference estimates hop count).

COLLECTION ONLY: sends benign ICMP requests and reads replies. No exploitation.

PRIVILEGE/PLATFORM: ICMP needs a raw socket (root) or an ICMP datagram socket
(SOCK_DGRAM+IPPROTO_ICMP — unprivileged on macOS, and on Linux when
net.ipv4.ping_group_range permits). When neither is available the scanner
degrades to "icmp unavailable" and can still fingerprint from injected TCP hints.
"""

from __future__ import annotations

import asyncio
import os
import socket
import struct
import sys
import time

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    resolve, inet_checksum, setup_logging, base_argparser, main_entrypoint, LOG,
    probe_payload,
)

# ICMP message types
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIMESTAMP_REQUEST = 13
ICMP_TIMESTAMP_REPLY = 14
ICMP_ADDRMASK_REQUEST = 17
ICMP_ADDRMASK_REPLY = 18

# The three initial-TTL values essentially every stack uses.
_INITIAL_TTLS = (64, 128, 255)

# Well-known default TCP receive windows by OS family (small, indicative set).
_LINUX_WINDOWS = {5840, 14600, 29200, 64240, 65535}
_WINDOWS_WINDOWS = {8192, 16384, 65535, 64240}


# ── ICMP packet construction ──────────────────────────────────────────────────

def _icmp(type_: int, code: int, rest: bytes) -> bytes:
    """Build an ICMP message (header + rest) with a valid checksum."""
    header = struct.pack("!BBH", type_, code, 0) + rest
    chk = inet_checksum(header)
    return struct.pack("!BBH", type_, code, chk) + rest


def build_icmp_echo(identifier: int, seq: int, payload: bytes = b"") -> bytes:
    return _icmp(ICMP_ECHO_REQUEST, 0, struct.pack("!HH", identifier, seq) + payload)


def build_icmp_timestamp(identifier: int, seq: int) -> bytes:
    # id, seq, originate/receive/transmit timestamps (all zero on request)
    rest = struct.pack("!HHIII", identifier, seq, 0, 0, 0)
    return _icmp(ICMP_TIMESTAMP_REQUEST, 0, rest)


def build_icmp_addrmask(identifier: int, seq: int) -> bytes:
    rest = struct.pack("!HHI", identifier, seq, 0)   # id, seq, mask=0
    return _icmp(ICMP_ADDRMASK_REQUEST, 0, rest)


def parse_icmp_reply(raw: bytes) -> dict | None:
    """
    Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header
    present -> TTL available) and datagram-ICMP delivery (ICMP only -> ttl None).
    """
    if len(raw) < 8:
        return None
    ttl = None
    icmp = raw
    if (raw[0] >> 4) == 4 and len(raw) >= 20:      # looks like an IPv4 header
        ihl = (raw[0] & 0x0F) * 4
        if ihl >= 20 and len(raw) >= ihl + 8:
            ttl = raw[8]
            icmp = raw[ihl:]
    if len(icmp) < 8:
        return None
    type_, code, _chk, ident, seq = struct.unpack("!BBHHH", icmp[:8])
    return {"type": type_, "code": code, "id": ident, "seq": seq, "ttl": ttl}


def accept_echo_reply(src_ip: str | None, parsed: dict | None, target_ip: str) -> bool:
    """True only for an ICMP ECHO reply that actually came FROM the probed host.

    A raw ICMP socket receives every ICMP packet on the box, so a reply meant for
    another target (or another probe) can arrive on our socket; accepting it would
    attribute the wrong host's TTL — a wrong-host OS fingerprint. Requiring the
    source address to equal the target closes that. (Datagram-ICMP also delivers
    the peer address, so the same check works there.)"""
    if not parsed or parsed.get("type") != ICMP_ECHO_REPLY:
        return False
    return src_ip is None or src_ip == target_ip


# ── TTL inference + OS mapping ────────────────────────────────────────────────

def infer_initial_ttl(observed_ttl: int | None) -> int | None:
    """Round the observed TTL up to the nearest standard initial TTL."""
    if observed_ttl is None:
        return None
    for base in _INITIAL_TTLS:
        if observed_ttl <= base:
            return base
    return 255


def hop_estimate(observed_ttl: int | None) -> int | None:
    init = infer_initial_ttl(observed_ttl)
    if init is None or observed_ttl is None:
        return None
    return init - observed_ttl


def os_family_from_ttl(observed_ttl: int | None) -> str:
    init = infer_initial_ttl(observed_ttl)
    return {
        64: "Linux/Unix/macOS",
        128: "Windows",
        255: "Network/Embedded",
    }.get(init, "unknown")


def fingerprint_os(*, ttl: int | None = None, tcp_window: int | None = None,
                   mss: int | None = None) -> dict:
    """
    Combine available stack signals into a best-guess OS family with a calibrated
    confidence. Confidence is the share of evidence pointing at the winner, but
    CAPPED by how many *independent* signals corroborate it: a lone TTL is only a
    hint (<=0.5) and can never reach absolute certainty, since a single stack
    value is trivially spoofed and NAT/proxies rewrite it. Two agreeing signals
    -> strong; three+ -> high, but never 1.0. Returns {os_guess, confidence,
    signals} where signals (incl. support_count) exposes what backed the guess.
    """
    signals: dict = {}
    scores = {"Linux/Unix/macOS": 0, "Windows": 0, "Network/Embedded": 0}
    # Count of independent signal families backing each family (drives the cap).
    support = {"Linux/Unix/macOS": 0, "Windows": 0, "Network/Embedded": 0}

    if ttl is not None:
        init = infer_initial_ttl(ttl)
        signals["initial_ttl"] = init
        signals["observed_ttl"] = ttl
        signals["hop_estimate"] = hop_estimate(ttl)
        if init == 64:
            scores["Linux/Unix/macOS"] += 2
            support["Linux/Unix/macOS"] += 1
        elif init == 128:
            scores["Windows"] += 2
            support["Windows"] += 1
        elif init == 255:
            scores["Network/Embedded"] += 2
            support["Network/Embedded"] += 1

    if tcp_window is not None:
        signals["tcp_window"] = tcp_window
        # Windows-specific first (65535/64240 overlap both, so don't double-count).
        if tcp_window in _WINDOWS_WINDOWS and tcp_window not in _LINUX_WINDOWS:
            scores["Windows"] += 1
            support["Windows"] += 1
        elif tcp_window in _LINUX_WINDOWS:
            scores["Linux/Unix/macOS"] += 1
            support["Linux/Unix/macOS"] += 1

    if mss is not None:
        signals["mss"] = mss
        # MSS = MTU - IPv4(20) - TCP(20) headers. Recover the path MTU and classify
        # the link. A sub-1500 MTU means the path is encapsulated — VPN/PPPoE/overlay
        # — which is real reachability intel (feeds vantage/segmentation), not an OS
        # signal, so it deliberately does NOT touch the OS scores. (MSS 1460 is the
        # Ethernet default on every OS, so it isn't OS-distinctive anyway.)
        mtu = mss + 40
        signals["mtu"] = mtu
        if mtu > 1500:
            signals["link_hint"] = "jumbo"
        elif mtu == 1500:
            signals["link_hint"] = "ethernet"
        elif mtu >= 1400:
            signals["link_hint"] = "tunnel_or_vpn"
        else:
            signals["link_hint"] = "constrained"

    total = sum(scores.values())
    if total == 0:
        return {"os_guess": "unknown", "confidence": 0.0, "signals": signals}
    best = max(scores, key=scores.get)
    # A single stack signal is a hint, not proof. Cap confidence by corroboration
    # so TTL-alone maxes at medium and nothing ever claims absolute certainty.
    n_support = support[best]
    ceiling = {0: 0.0, 1: 0.5, 2: 0.8}.get(n_support, 0.95)
    signals["support_count"] = n_support
    return {"os_guess": best,
            "confidence": round(min(scores[best] / total, ceiling), 2),
            "signals": signals}


# ── capability detection ──────────────────────────────────────────────────────

def icmp_supported(*, socket_factory=None) -> bool:
    """True if we can open an ICMP socket (datagram-ICMP or raw)."""
    if socket_factory is not None:
        try:
            s = socket_factory(); s.close(); return True
        except (PermissionError, OSError):
            return False
    for stype in (socket.SOCK_DGRAM, socket.SOCK_RAW):
        try:
            s = socket.socket(socket.AF_INET, stype, socket.IPPROTO_ICMP)
            s.close()
            return True
        except (PermissionError, OSError):
            continue
    return False


def _open_icmp_socket() -> tuple[socket.socket, bool] | None:
    """Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_ICMP)
        return s, False
    except (PermissionError, OSError):
        pass
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        return s, True
    except (PermissionError, OSError):
        return None


# ── scanner ───────────────────────────────────────────────────────────────────

class OSFingerprintScanner(BaseScanner):
    """
    ICMP-echo liveness + TTL harvest -> OS-family guess. Optionally accepts TCP
    window/MSS hints (from a prior SYN/connect result) to sharpen the guess.
    """
    name = "os_fingerprint"

    def __init__(self, *args, tcp_hints: dict[str, dict] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        # {target: {"tcp_window": int, "mss": int}} gathered elsewhere.
        self.tcp_hints = tcp_hints or {}

    def _icmp_echo_ttl(self, target: str) -> int | None | str:
        """Send one ICMP echo; return observed TTL, None (no TTL), or "down"."""
        opened = _open_icmp_socket()
        if opened is None:
            return "unavailable"
        sock, _is_raw = opened
        try:
            family, sockaddr = resolve(target, 0, proto="udp")
            if family != socket.AF_INET:
                return "unavailable"          # IPv4-only ICMP here
            target_ip = sockaddr[0]
            ident = os.getpid() & 0xFFFF
            sock.sendto(build_icmp_echo(ident, 1, probe_payload()), (target_ip, 0))
            # Read until THIS host's echo reply arrives or the timeout elapses,
            # skipping stray ICMP from other hosts (a raw socket receives all ICMP
            # on the box) so a neighbour's TTL is never mislabelled as the target's.
            deadline = time.monotonic() + self.timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return "down"
                sock.settimeout(remaining)
                raw, addr = sock.recvfrom(2048)
                parsed = parse_icmp_reply(raw)
                if accept_echo_reply(addr[0] if addr else None, parsed, target_ip):
                    return parsed["ttl"]
        except (socket.timeout, OSError):
            return "down"
        finally:
            sock.close()

    async def scan_target(self, target: str) -> list[ScanResult]:
        loop = asyncio.get_running_loop()
        await self.limiter.wait()
        async with self.sem:
            ttl = await loop.run_in_executor(None, self._icmp_echo_ttl, target)

        hints = self.tcp_hints.get(target, {})
        if ttl == "unavailable":
            # No ICMP; fingerprint from TCP hints alone if we have any.
            if hints:
                fp = fingerprint_os(**hints)
                return [ScanResult(self.name, target, status="observed",
                                   data={"icmp": "unavailable", **fp},
                                   evidence=f"OS guess {fp['os_guess']} (tcp hints only)")]
            return [ScanResult(self.name, target, status="observed",
                               data={"icmp": "unavailable"},
                               evidence="ICMP unavailable (need root or ping perms)")]
        if ttl == "down":
            return [ScanResult(self.name, target, status="filtered",
                               data={"alive": False, "icmp_reply": False},
                               evidence="no ICMP echo reply")]

        # ttl is an int (or None if the IP header wasn't delivered).
        fp = fingerprint_os(ttl=ttl if isinstance(ttl, int) else None,
                            tcp_window=hints.get("tcp_window"),
                            mss=hints.get("mss"))
        data = {"alive": True, "icmp_reply": True, "observed_ttl": ttl, **fp}
        return [ScanResult(
            self.name, target, status="open", data=data,
            evidence=f"ICMP reply ttl={ttl} -> {fp['os_guess']} "
                     f"(conf {fp['confidence']})")]


def main() -> None:
    parser = base_argparser("OS fingerprint via ICMP echo + TTL")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = OSFingerprintScanner(scope, rate=args.rate,
                                       concurrency=args.concurrency,
                                       timeout=args.timeout)
        if not icmp_supported():
            LOG.warning("[os_fingerprint] ICMP unavailable — run as root or grant "
                        "ping permissions; results will be limited")
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
