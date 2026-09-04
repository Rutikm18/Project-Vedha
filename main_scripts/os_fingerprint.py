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
    resolve, resolve_ip_candidates, inet_checksum, setup_logging,
    base_argparser, main_entrypoint, LOG, probe_payload,
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


def _strip_ip_header(raw: bytes) -> tuple[int | None, bytes]:
    """Return (ttl, icmp_bytes). Raw-socket delivery prepends the full IPv4 header
    (so the TTL is available); datagram-ICMP delivers the ICMP message alone
    (ttl None). A leading nibble of 4 with a sane IHL marks the IPv4 case; an ICMP
    type byte (0/14/…) never has a high nibble of 4, so datagram frames fall through
    untouched."""
    if len(raw) >= 20 and (raw[0] >> 4) == 4:
        ihl = (raw[0] & 0x0F) * 4
        if ihl >= 20 and len(raw) >= ihl + 8:
            return raw[8], raw[ihl:]
    return None, raw


def parse_icmp_reply(raw: bytes) -> dict | None:
    """
    Parse an ICMP reply. Handles both raw-socket delivery (full IPv4 header
    present -> TTL available) and datagram-ICMP delivery (ICMP only -> ttl None).
    """
    if len(raw) < 8:
        return None
    ttl, icmp = _strip_ip_header(raw)
    if len(icmp) < 8:
        return None
    type_, code, _chk, ident, seq = struct.unpack("!BBHHH", icmp[:8])
    return {"type": type_, "code": code, "id": ident, "seq": seq, "ttl": ttl}


def parse_icmp_timestamps(raw: bytes) -> dict | None:
    """Parse an ICMP timestamp reply (type 14): id/seq/ttl plus the three 32-bit
    timestamps (originate/receive/transmit, ms since UTC midnight). Returns None
    unless the ICMP body is a full 20-byte timestamp message."""
    ttl, icmp = _strip_ip_header(raw)
    if len(icmp) < 20:
        return None
    type_, code, _chk, ident, seq, orig, recv, xmit = struct.unpack(
        "!BBHHHIII", icmp[:20])
    return {"type": type_, "code": code, "id": ident, "seq": seq, "ttl": ttl,
            "originate": orig, "receive": recv, "transmit": xmit}


def remote_clock(transmit_ms: int) -> dict:
    """Interpret a timestamp reply's transmit value. Per RFC 792 a *standard* value
    is milliseconds since UTC midnight with the high-order bit clear; a set high bit
    flags a non-standard clock we don't decode. The decoded wall-clock is real
    intel — it can expose the target's timezone and clock skew."""
    if transmit_ms & 0x80000000:
        return {"standard": False, "transmit_raw": transmit_ms}
    ms = transmit_ms % 86_400_000                 # clamp stray out-of-day values
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, msec = divmod(rem, 1000)
    return {"standard": True,
            "ms_since_utc_midnight": transmit_ms,
            "utc_time": f"{h:02d}:{m:02d}:{s:02d}.{msec:03d}"}


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


# ── p0f-style TCP/IP stack signatures ─────────────────────────────────────────
# Derived from p0f v3's fingerprint database (Zalewski). Each entry keys on the
# inferred initial TTL + the SYN/ACK TCP option LAYOUT (p0f "olayout": M=mss,
# W=wscale, S=sackOK, T=timestamps, N=nop, E=eol) and, optionally, the window
# scale — the combination that most reliably separates the major stacks. The
# order/presence of options is a far stronger discriminator than window size
# alone (which NAT/proxies rewrite), so this refines the coarse TTL family guess
# into a specific stack WITHOUT ever overriding it. Conservative by design: only
# widely-stable layouts are encoded; anything else yields no stack label rather
# than a fabricated one. Most specific (highest-confidence) match wins.
#   (initial_ttl, olayout | None, wscale | None, label, confidence)
_STACK_SIGNATURES: tuple = (
    (64,  "MSTNW", 7,    "Linux (kernel 3.11+ / 4.x-6.x)", 0.90),
    (64,  "MSTNW", None, "Linux (kernel 2.6.x / modern)", 0.82),
    (128, "MNWNNS", 8,   "Windows (NT 6.2+ — 8/10/11, Server 2012+)", 0.90),
    (128, "MNWNNS", None, "Windows (NT 6.x — Vista/7/8+)", 0.80),
    (128, "MNNS",  None, "Windows (NT 5.x — XP/Server 2003)", 0.75),
    (64,  "MNWNNTSE", None, "macOS / iOS (Darwin)", 0.85),
    (64,  "MNWNNTS",  None, "macOS / iOS (Darwin)", 0.83),
    (64,  "MNWST",  None, "FreeBSD", 0.80),
    (255, None,     None, "Network / embedded device (initial TTL 255)", 0.60),
)


def match_stack_signature(*, ttl: int | None = None, mss: int | None = None,
                          window: int | None = None, wscale: int | None = None,
                          olayout: str | None = None) -> dict | None:
    """p0f-style match on (initial TTL, option layout, window scale) → a specific
    stack label. Returns None when nothing matches (never guesses). Pure."""
    if ttl is None:
        return None
    init = infer_initial_ttl(ttl)
    best: dict | None = None
    for sig_ttl, sig_ol, sig_ws, label, conf in _STACK_SIGNATURES:
        if init != sig_ttl:
            continue
        if sig_ol is not None and olayout != sig_ol:
            continue
        if sig_ws is not None and wscale != sig_ws:
            continue
        if best is None or conf > best["stack_confidence"]:
            best = {"stack": label, "stack_confidence": conf,
                    "stack_source": "p0f_tcp_options"}
    return best


def fingerprint_os(*, ttl: int | None = None, tcp_window: int | None = None,
                   mss: int | None = None, ttl_source: str | None = None,
                   wscale: int | None = None, olayout: str | None = None) -> dict:
    """
    Combine available stack signals into a best-guess OS family with a calibrated
    confidence. Confidence is the share of evidence pointing at the winner, but
    CAPPED by how many *independent* signals corroborate it: a lone TTL is only a
    hint (<=0.5) and can never reach absolute certainty, since a single stack
    value is trivially spoofed and NAT/proxies rewrite it. Two agreeing signals
    -> strong; three+ -> high, but never 1.0. Returns {os_guess, confidence,
    signals} where signals (incl. support_count) exposes what backed the guess.

    PROVENANCE (honesty rule): a TTL harvested from a TCP SYN/ACK and a TTL from
    an ICMP echo produce the SAME os_guess but are NOT the same evidence — one is
    read through the firewall on a port that answered, the other needs the host to
    answer ICMP. `ttl_source` (e.g. "icmp_echo", "icmp_timestamp", "tcp_synack")
    is recorded in signals so no consumer can later mislabel a TCP-derived TTL as
    an ICMP result. It is advisory only and never changes the score.
    """
    signals: dict = {}
    scores = {"Linux/Unix/macOS": 0, "Windows": 0, "Network/Embedded": 0}
    # Count of independent signal families backing each family (drives the cap).
    support = {"Linux/Unix/macOS": 0, "Windows": 0, "Network/Embedded": 0}

    if ttl is not None:
        init = infer_initial_ttl(ttl)
        signals["initial_ttl"] = init
        signals["observed_ttl"] = ttl
        signals["ttl_source"] = ttl_source or "unspecified"
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

    # p0f-style refinement: a specific stack label from the TCP option layout.
    # Additive — it enriches, never overrides, the coarse family guess below.
    stack = match_stack_signature(ttl=ttl, mss=mss, window=tcp_window,
                                  wscale=wscale, olayout=olayout)
    stack_guess = None
    if stack:
        stack_guess = stack["stack"]
        signals["stack"] = stack["stack"]
        signals["stack_confidence"] = stack["stack_confidence"]
        signals["stack_source"] = stack["stack_source"]

    total = sum(scores.values())
    if total == 0:
        return {"os_guess": "unknown", "confidence": 0.0,
                "stack_guess": stack_guess, "signals": signals}
    best = max(scores, key=scores.get)
    # A single stack signal is a hint, not proof. Cap confidence by corroboration
    # so TTL-alone maxes at medium and nothing ever claims absolute certainty.
    n_support = support[best]
    ceiling = {0: 0.0, 1: 0.5, 2: 0.8}.get(n_support, 0.95)
    signals["support_count"] = n_support
    return {"os_guess": best,
            "confidence": round(min(scores[best] / total, ceiling), 2),
            "stack_guess": stack_guess, "signals": signals}


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

    def __init__(self, *args, tcp_hints: dict[str, dict] | None = None,
                 smb_build: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        # {target: {"tcp_window": int, "mss": int}} gathered elsewhere.
        self.tcp_hints = tcp_hints or {}
        # When True (default), enrich the guess with the exact Windows build from a
        # pre-auth SMB2 NTLM CHALLENGE if 445 is reachable — turning a TTL-only
        # "Windows, conf 0.5" into "Windows 11 24H2, build 26100, conf ≥0.95".
        self.smb_build = smb_build

    def _smb_build(self, target: str) -> dict:
        """Best-effort exact Windows build via SMB2 NTLM (shared impl). {} on any
        failure or when 445 is closed. Runs in a worker thread (blocking sockets)."""
        if not self.smb_build:
            return {}
        from .smb_scanner import ntlm_os_build
        for ip in resolve_ip_candidates(target, 445, proto="tcp"):
            build = ntlm_os_build(ip, 445, min(self.timeout, 5.0))
            if build:
                return build      # first address that answers wins
        return {}

    def _apply_smb_build(self, target: str, result: ScanResult) -> ScanResult:
        """Fuse an SMB2 NTLM build into an OS result: authoritative release + build,
        confidence >=0.95, method records both provenances. No-op if no build."""
        build = self._smb_build(target)
        if not build.get("os_build"):
            return result
        d = result.data or {}
        d.update({"os_guess": "Windows",
                  "os_release": build.get("os_release"),
                  "os_build": build.get("os_build"),
                  "os_version": build.get("os_version"),
                  "hostname": build.get("target_name"),
                  "confidence": max(d.get("confidence", 0.0) or 0.0,
                                    build.get("os_confidence", 0.97))})
        result.data = d
        result.confidence = d["confidence"]
        base_method = result.method or "icmp_echo"
        result.method = f"{base_method}+smb2_ntlm_version"
        result.evidence = (f"{result.evidence}; SMB2 NTLM build "
                           f"{build.get('os_build')} -> {build.get('os_release')} "
                           f"(conf {d['confidence']})")
        return result

    def _icmp_echo_ttl(self, target: str) -> int | None | str:
        """Send one ICMP echo; return observed TTL, None (no TTL), or "down"."""
        opened = _open_icmp_socket()
        if opened is None:
            return "unavailable"
        sock, _is_raw = opened
        try:
            family, sockaddr = resolve(target, 0, proto="udp", family=socket.AF_INET)
            if family != socket.AF_INET:
                return "unavailable"          # no IPv4 for this host — ICMP here is v4-only
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

    def _icmp_timestamp(self, target: str) -> dict | str:
        """Send an ICMP timestamp request (type 13); return {ttl, transmit} from a
        matching type-14 reply, else "down"/"unavailable". This reaches hosts that
        filter echo but not timestamp, and harvests the remote clock."""
        opened = _open_icmp_socket()
        if opened is None:
            return "unavailable"
        sock, _is_raw = opened
        try:
            family, sockaddr = resolve(target, 0, proto="udp", family=socket.AF_INET)
            if family != socket.AF_INET:
                return "unavailable"
            target_ip = sockaddr[0]
            ident = os.getpid() & 0xFFFF
            sock.sendto(build_icmp_timestamp(ident, 1), (target_ip, 0))
            deadline = time.monotonic() + self.timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return "down"
                sock.settimeout(remaining)
                raw, addr = sock.recvfrom(2048)
                if addr and addr[0] != target_ip:      # stray ICMP from another host
                    continue
                ts = parse_icmp_timestamps(raw)
                if ts and ts["type"] == ICMP_TIMESTAMP_REPLY:
                    return {"ttl": ts["ttl"], "transmit": ts["transmit"]}
        except (socket.timeout, OSError):
            return "down"
        finally:
            sock.close()

    def _tcp_ttl_result(self, target: str, hints: dict) -> ScanResult:
        """FIX 3b: aliveness/TTL came from a TCP SYN-ACK, not ICMP. Label the TTL
        source honestly as tcp_ttl — NEVER icmp_echo. Liveness is real (a TCP
        handshake elsewhere reached the host), but no ICMP echo was received."""
        fp = fingerprint_os(ttl=hints.get("ttl"), tcp_window=hints.get("tcp_window"),
                            mss=hints.get("mss"), wscale=hints.get("wscale"),
                            olayout=hints.get("olayout"), ttl_source="tcp_synack")
        data = {"alive": True, "icmp_reply": False, "icmp_echo_reply": False,
                "via": "tcp_synack", "observed_ttl": hints.get("ttl"), **fp}
        return ScanResult(
            self.name, target, status="observed", method="tcp_ttl", data=data,
            evidence=(f"no ICMP echo; TTL {hints.get('ttl')} derived from TCP SYN/ACK "
                      f"-> {fp['os_guess']} (method tcp_ttl)"))

    async def scan_target(self, target: str) -> list[ScanResult]:
        results = await self._icmp_scan_target(target)
        # Enrich the primary result with the exact Windows build (SMB2 NTLM) — the
        # single change that lifts standalone os_fingerprint from a TTL-only 0.5
        # guess to an authoritative build-backed identification when 445 is open.
        if results and self.smb_build:
            loop = asyncio.get_running_loop()
            results[0] = await loop.run_in_executor(
                None, self._apply_smb_build, target, results[0])
        return results

    async def _icmp_scan_target(self, target: str) -> list[ScanResult]:
        loop = asyncio.get_running_loop()
        await self.limiter.wait()
        async with self.sem:
            ttl = await loop.run_in_executor(None, self._icmp_echo_ttl, target)

        hints = self.tcp_hints.get(target, {})
        if ttl == "unavailable":
            # No ICMP. If a TCP-derived TTL is available, report it as tcp_ttl (never
            # icmp_echo). Otherwise fall back to window/MSS-only hints or say so.
            if hints.get("ttl") is not None:
                return [self._tcp_ttl_result(target, hints)]
            if hints:
                fp = fingerprint_os(ttl_source="tcp", **{
                    k: v for k, v in hints.items()
                    if k in ("tcp_window", "mss", "wscale", "olayout")})
                return [ScanResult(self.name, target, status="observed",
                                   method="tcp_hints",
                                   data={"icmp": "unavailable", **fp},
                                   evidence=f"OS guess {fp['os_guess']} (tcp hints only)")]
            return [ScanResult(self.name, target, status="observed",
                               method="tcp_hints",
                               data={"icmp": "unavailable"},
                               evidence="ICMP unavailable (need root or ping perms)")]
        if ttl == "down":
            # Echo filtered? A timestamp probe (type 13) frequently still elicits a
            # reply — proving liveness through the filter and leaking the remote
            # clock. (Answering timestamp-but-not-echo is itself a stack signal.)
            ts = await loop.run_in_executor(None, self._icmp_timestamp, target)
            if isinstance(ts, dict):
                t_ttl = ts.get("ttl")
                fp = fingerprint_os(ttl=t_ttl if isinstance(t_ttl, int) else None,
                                    tcp_window=hints.get("tcp_window"),
                                    mss=hints.get("mss"),
                                    ttl_source="icmp_timestamp")
                clock = remote_clock(ts["transmit"])
                data = {"alive": True, "icmp_reply": True, "icmp_echo_reply": False,
                        "icmp_timestamp_reply": True, "via": "icmp_timestamp",
                        "observed_ttl": t_ttl, "remote_clock": clock, **fp}
                ttl_txt = t_ttl if t_ttl is not None else "n/a (datagram socket)"
                ev = (f"ICMP timestamp reply (echo filtered) ttl={ttl_txt} "
                      f"-> {fp['os_guess']}")
                if clock.get("standard"):
                    ev += f"; remote clock {clock['utc_time']} UTC"
                return [ScanResult(self.name, target, status="open",
                                   method="icmp_timestamp", data=data, evidence=ev)]
            # Echo AND timestamp both silent. If a TCP-derived TTL exists, the host
            # is alive via TCP — report tcp_ttl, never a fabricated ICMP result.
            if hints.get("ttl") is not None:
                return [self._tcp_ttl_result(target, hints)]
            return [ScanResult(self.name, target, status="filtered",
                               data={"alive": False, "icmp_reply": False,
                                     "icmp_timestamp_reply": False},
                               evidence="no ICMP echo or timestamp reply")]

        # A real ICMP echo reply was accepted (accept_echo_reply). `ttl` is the
        # observed IP TTL on a raw socket, or None when a datagram-ICMP socket
        # delivered the reply without the IP header — in which case the OS guess
        # comes from the TCP hints, NOT from a fabricated ICMP TTL.
        has_ttl = isinstance(ttl, int)
        fp = fingerprint_os(ttl=ttl if has_ttl else None,
                            tcp_window=hints.get("tcp_window"),
                            mss=hints.get("mss"),
                            ttl_source="icmp_echo" if has_ttl else None)
        data = {"alive": True, "icmp_reply": True, "icmp_echo_reply": True,
                "observed_ttl": ttl, **fp}
        if has_ttl:
            ev = (f"ICMP echo reply ttl={ttl} -> {fp['os_guess']} "
                  f"(conf {fp['confidence']})")
        else:
            # Alive is proven by the echo reply; the TTL was not observable here.
            ev = (f"ICMP echo reply (alive); no TTL via datagram socket -> "
                  f"{fp['os_guess']} (conf {fp['confidence']})")
        return [ScanResult(
            self.name, target, status="open", method="icmp_echo",
            data=data, evidence=ev)]


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
