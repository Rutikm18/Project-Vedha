"""
port_scanner.py — TCP connect scan with an evidence-based state engine.

METHOD (collection only): a full TCP connect() per port via the OS stack
(unprivileged). No raw packets, no SYN/stealth (that needs root). For SYN
scanning at scale use syn_scanner.py / nmap_wrapper.py. This module is
deliberately self-contained — it depends on no other scanner — so its accuracy
is easy to measure in isolation.

WHAT "OPEN" MEANS HERE. For an exposure scanner the only fact this engine can
assert is reachability *from this vantage point*:

    OPEN = a connect() from this scanner to target:port received positive TCP
           evidence (the 3-way handshake completed / SYN-ACK).

That is a different fact from "the host has a socket in LISTEN". A service can
LISTEN on a host yet be FILTERED from here by a firewall or a routing path, so a
Windows box showing 20 LISTEN ports may expose only 5 remotely. We report the
remote truth, not the host's local belief.

STATE + REASON, NOT JUST A NUMBER. Every observation carries a *state* and a
machine-readable *reason* (in `data`), so a port that is not OPEN can still tell
you WHY:

    open         connect_success          handshake completed (SYN/ACK)
    closed       connection_refused       host reachable, RST returned
                 connection_reset         RST mid-handshake
    filtered     no_response              silence within timeout (medium conf.)
                 connection_aborted        reset by a middlebox
    unreachable  host_unreachable          ICMP host unreachable / EHOSTUNREACH
                 network_unreachable       ICMP net unreachable / ENETUNREACH
                 host_down                 EHOSTDOWN
    error        dns_error                 name did not resolve
                 local_resource_error      scanner ran out of fds/buffers
                 address_unavailable       source addressing problem
                 permission_denied         local policy blocked the socket
                 os_error                  unclassified OSError (kept visible)

The old behaviour collapsed *every* OSError into "filtered", which quietly
mislabels a scanner-side "too many open files" or a routing "no route to host"
as a target firewall. We classify by errno instead so those stay debuggable.

TIMEOUT IS NOT PROOF. Silence has many causes (firewall DROP, packet loss,
congestion, an overloaded scanner). We therefore label it `filtered /
no_response` with `confidence: medium` rather than claiming a firewall for
certain.

RETRANSMIT ON SILENCE. Because silence is often just one lost packet (SYN or
its SYN/ACK dropped by congestion / an RFC-1812 ICMP rate limit), a single
timeout is a weak reason to declare a port unreachable — that is a false
negative *manufactured by the scanner itself*. So a `no_response` gets a bounded
retransmit (like async_udp_probe_retry): a definitive RST/refused is never
retried, only silence, and the first positive answer wins. This is the direct
fix for "the scanner didn't find a port that is actually open."

IPv4 AND IPv6 ARE INDEPENDENT. A host can expose different ports on its v4 vs v6
address (Windows' dual-stack sockets are a classic example). Each observation
records the address family it actually reached, so the two are never conflated.

Run standalone (`python -m scanner.port_scanner ...`) and it emits newline-
delimited JSON you can diff against ground truth.
"""

from __future__ import annotations

import argparse
import asyncio
import ipaddress
import random
import socket
import struct
import time
from collections import Counter, deque
from dataclasses import dataclass, field

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser,
    main_entrypoint, classify_os_error, STATE_CONFIDENCE, jittered_delay,
    assess_tarpit, LOG, raise_fd_limit, safe_connect_concurrency,
    AdaptiveRateController, RateLimiter,
)
from .adaptive_timeout import AdaptiveTimeout

# The errno→(state,reason) classifier now lives in scanner_base (Phase 2 — one
# shared model). Local alias kept so existing references are unchanged.
_CONFIDENCE = STATE_CONFIDENCE


# _ERRNO_MAP, STATE_CONFIDENCE and classify_os_error moved to scanner_base
# (Phase 2 — one shared errno→state classifier for TCP, UDP and deeper scanners).


def _harvest_tcp_stack(sock) -> dict:
    """
    Peer TCP-stack signals readable from a COMPLETED connect(), for OS/link
    fingerprinting WITHOUT sending a single extra packet (p0f's core insight).

    Harvested:
      * `mss`     — the peer's ADVERTISED MSS, and only ever from Linux
                    `tcpi_advmss`. MSS+40 recovers the path MTU, which is how
                    os_fingerprint derives its `link_hint` (ethernet vs
                    tunnel/VPN vs constrained) — real segmentation intel.
      * `mss_effective` — `TCP_MAXSEG` on an ESTABLISHED connection. Reported for
                    completeness but deliberately kept OUT of `mss`, because it is
                    the negotiated segment size AFTER options, not the advertised
                    option value: a host with TCP timestamps enabled reports 1448
                    on a plain 1500-MTU Ethernet path. Feeding that to the MTU
                    inference yields mtu=1488 and a confident, WRONG
                    `link_hint="tunnel_or_vpn"` — the same failure mode as the
                    initial-window trap below, reached through a different door.
                    (Observed for real: 192.168.1.65 over LAN, 2026-09-03.)
      * `wscale`  — the window-scale factor the PEER advertised in its SYN/ACK
                    (`tcpi_snd_wscale` is the shift we apply to the peer's window).
                    A genuine p0f discriminator.
      * `rtt_us`  — the KERNEL's smoothed RTT for this connection. Strictly better
                    than the scanner's wall-clock timing, which also contains
                    event-loop scheduling delay and so inflates the estimate.

    DELIBERATELY NOT HARVESTED — the peer's initial receive window. Once the
    handshake completes the kernel only exposes the CURRENT, window-scaled send
    window, which has already drifted from the value the peer put in its SYN/ACK.
    `os_fingerprint` matches `tcp_window` against INITIAL-window tables
    (`_LINUX_WINDOWS` / `_WINDOWS_WINDOWS`), so feeding it a post-handshake window
    would manufacture confident-but-WRONG OS attributions — worse than no signal.
    The raw SYN path reads the true SYN/ACK window and is the right place for it.

    Everything is best-effort: a non-Linux kernel, a short `struct tcp_info`, or a
    closed socket simply yields fewer keys. Never raises.
    """
    out: dict = {}
    if sock is None:
        return out
    try:
        eff = sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_MAXSEG)
        if isinstance(eff, int) and 0 < eff < 65536:
            # NOT `mss`: this is the post-options effective segment size.
            out["mss_effective"] = eff
    except (OSError, AttributeError, ValueError):
        pass

    # struct tcp_info (Linux): 8 x u8 then a run of u32s. We only read fields at
    # offsets that have been stable since 2.6, and bail out if the buffer is short.
    tcp_info = getattr(socket, "TCP_INFO", None)
    if tcp_info is None:
        return out
    try:
        raw = sock.getsockopt(socket.IPPROTO_TCP, tcp_info, 256)
    except (OSError, AttributeError, ValueError):
        return out
    _U32_RTT, _U32_ADVMSS = 15, 19          # tcpi_rtt, tcpi_advmss
    need = 8 + 4 * (_U32_ADVMSS + 1)
    if len(raw) < need:
        return out
    try:
        flags = struct.unpack_from("8B", raw, 0)
        u32 = struct.unpack_from("%dI" % (_U32_ADVMSS + 1), raw, 8)
    except struct.error:
        return out
    # tcpi_snd_wscale is the low nibble of byte 6 (bitfield, little-endian ABI).
    wscale = flags[6] & 0x0F
    if 0 < wscale <= 14:
        out["wscale"] = wscale
    rtt_us = u32[_U32_RTT]
    if 0 < rtt_us < 60_000_000:
        out["rtt_us"] = rtt_us
    advmss = u32[_U32_ADVMSS]
    if 0 < advmss < 65536:
        # The ONLY trustworthy advertised-MSS source, hence the only one allowed
        # to drive path-MTU/link inference downstream.
        out["mss"] = advmss
    return out


def _family_of(ip: str | None) -> str | None:
    """Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)."""
    if not ip:
        return None
    try:
        return "ipv6" if ipaddress.ip_address(ip).version == 6 else "ipv4"
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Coverage profiles. Named, reproducible port sets so an operator declares
# intent ("full", "top1000") instead of an ad-hoc -p string they must remember,
# and so scan completeness can be asserted against a known request size.
# --------------------------------------------------------------------------- #
ALL_TCP_PORTS = list(range(1, 65536))          # the whole TCP space, once

# nmap's canonical top-100 TCP ports (frequency-ranked). Notably includes the
# Windows dynamic-RPC low block (49152-49157), 3389, 5357, 1900 — high value here.
_NMAP_TOP_100 = [
    7, 9, 13, 21, 22, 23, 25, 26, 37, 53, 79, 80, 81, 88, 106, 110, 111, 113,
    119, 135, 139, 143, 144, 179, 199, 389, 427, 443, 444, 445, 465, 513, 514,
    515, 543, 544, 548, 554, 587, 631, 646, 873, 990, 993, 995, 1025, 1026,
    1027, 1028, 1029, 1110, 1433, 1720, 1723, 1755, 1900, 2000, 2001, 2049,
    2121, 2717, 3000, 3128, 3306, 3389, 3986, 4899, 5000, 5009, 5051, 5060,
    5101, 5190, 5357, 5432, 5631, 5666, 5800, 5900, 6000, 6001, 6646, 7070,
    8000, 8008, 8009, 8080, 8081, 8443, 8888, 9100, 9999, 10000, 32768, 49152,
    49153, 49154, 49155, 49156, 49157,
]

_QUICK = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 3389]

# Enterprise/Windows high-value ports that internet-frequency lists under-rank,
# but which this ground truth showed listening: 2179 (VMRC), 5040, 7680 (Delivery
# Optimization), WinRM (5985/5986/47001), and the 49664+ dynamic RPC block.
_WINDOWS_EXTRA = [2179, 5040, 5985, 5986, 7680, 8443, 47001, *range(49664, 49700)]


def resolve_profile(name: str, custom: list[int] | None = None) -> list[int]:
    """Resolve a named scan profile to a concrete, de-duplicated port list.

    'full' is the entire TCP space; 'custom' defers to an explicit -p list. The
    de-dup keeps the completeness invariant honest (requested == unique ports).
    """
    if name == "quick":
        return list(dict.fromkeys(_QUICK))
    if name == "top100":
        return list(dict.fromkeys(_NMAP_TOP_100))
    if name == "top1000":
        # ~1000 high-value ports: well-known 1-1024 + nmap top-100 + the Windows
        # high ports above. This is deliberately NOT nmap's exact frequency
        # top-1000 (documented, so no false precision) — it is tuned for the
        # enterprise/Windows exposure this ground truth exhibits.
        return sorted(set(range(1, 1025)) | set(_NMAP_TOP_100) | set(_WINDOWS_EXTRA))
    if name == "full":
        return list(ALL_TCP_PORTS)
    if name == "custom":
        if not custom:
            raise ValueError("profile 'custom' requires an explicit -p/--ports list")
        return list(dict.fromkeys(custom))
    raise ValueError(f"unknown profile: {name!r}")


@dataclass
class ScanMetrics:
    """Per-target scan accounting — the completeness + self-health record.

    It lets a consumer tell a *clean* empty result from a *degraded* one, and
    (crucially for false-negative hunting) separate NOT-SCANNED ports from
    SCANNED-but-not-open ports. Every attempted port is tallied here BEFORE any
    --report-closed output filtering, so the engine never loses evidence.
    """
    target: str
    vantage: str
    ports_requested: int = 0
    ports_attempted: int = 0
    open: int = 0
    closed: int = 0
    filtered: int = 0
    unreachable: int = 0
    error: int = 0
    retries: int = 0
    local_resource_errors: int = 0
    duration_s: float = 0.0
    # Set-based completeness (Epic 4): the ports we were asked to scan, and a
    # per-port hit counter. Count-based completeness can be fooled by a skip+dup
    # pair (attempted still == requested); the SET cannot.
    requested_ports: set = field(default_factory=set)
    port_hits: Counter = field(default_factory=Counter)

    _STATES = ("open", "closed", "filtered", "unreachable", "error")

    def record(self, result: "ScanResult") -> None:
        """Tally exactly one terminal per-port observation."""
        self.ports_attempted += 1
        if result.port is not None:
            self.port_hits[result.port] += 1
        if result.status in self._STATES:
            setattr(self, result.status, getattr(self, result.status) + 1)
        data = result.data or {}
        attempts = data.get("attempts", 1)
        if attempts > 1:
            self.retries += attempts - 1
        if data.get("reason") == "local_resource_error":
            self.local_resource_errors += 1

    @property
    def classified(self) -> int:
        return self.open + self.closed + self.filtered + self.unreachable + self.error

    @property
    def missing_ports(self) -> list:
        """Requested ports that were never recorded — the silent-skip proof."""
        if not self.requested_ports:
            return []
        return sorted(self.requested_ports - set(self.port_hits))

    @property
    def duplicate_ports(self) -> list:
        """Ports recorded more than once (a port must get exactly one verdict)."""
        return sorted(p for p, c in self.port_hits.items() if c > 1)

    @property
    def complete(self) -> bool:
        # SET-based when the requested port set is known: every requested port was
        # classified exactly once (no missing, no duplicates) AND all states sum to
        # the request. This can't be fooled by a skip+dup pair the way counts can.
        if self.requested_ports:
            return (not self.missing_ports and not self.duplicate_ports
                    and self.classified == self.ports_requested)
        # Fallback for directly-constructed metrics without a requested set.
        return (self.ports_attempted == self.ports_requested
                and self.classified == self.ports_requested)

    @property
    def degraded(self) -> bool:
        # Local-side failures (fd/buffer exhaustion) manufacture false negatives,
        # so a scan that hit any is untrustworthy until re-run with lower limits.
        return self.local_resource_errors > 0

    def summary(self) -> dict:
        return {
            "vantage": self.vantage,
            "ports_requested": self.ports_requested,
            "ports_attempted": self.ports_attempted,
            "ports_not_scanned": self.ports_requested - self.ports_attempted,
            "classified": self.classified,
            "open": self.open, "closed": self.closed, "filtered": self.filtered,
            "unreachable": self.unreachable, "error": self.error,
            "retries": self.retries,
            "local_resource_errors": self.local_resource_errors,
            "missing": len(self.missing_ports),
            "missing_ports": self.missing_ports[:64],   # capped sample for evidence
            "duplicates": len(self.duplicate_ports),
            "duplicate_ports": self.duplicate_ports[:64],
            "duration_s": self.duration_s,
            "complete": self.complete,
            "health": "degraded" if self.degraded else "ok",
            # Flag hosts that answer on an implausible share of ports: their "open"
            # results are phantom (tarpit/honeypot/middlebox), not real services.
            "tarpit": assess_tarpit(self.open, self.ports_attempted),
        }


class PortScanner(BaseScanner):
    name = "port_scan"

    def __init__(self, *args, ports: list[int] | None = None,
                 report_closed: bool = False, vantage: str | None = None,
                 retries: int = 1, emit_summary: bool = True,
                 adaptive_timeout: bool = True, source_port: int | None = None,
                 randomize: bool = False, scan_delay: float = 0.0,
                 congestion: bool = True, delivery_floor: float = 0.35,
                 reprobe: bool = True,
                 reprobe_rate: float = 40.0, reprobe_concurrency: int = 10,
                 reprobe_retries: int = 3,
                 scan_meta: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        # Audit context (profile, fd ulimit, concurrency actually used) folded into
        # the scan_summary so a paid engagement's coverage decisions are on record.
        self.scan_meta = scan_meta or {}
        # Fixed TCP source port (e.g. 53/88) to bypass naive stateless ACLs; None =
        # OS-chosen ephemeral. Bound per-connect below (best-effort under concurrency).
        self.source_port = source_port
        # Evasion: randomize probe order + add a jittered per-probe delay so the scan
        # isn't a fixed-cadence, sequential-port pattern an IDS can flag.
        self.randomize = randomize
        self.scan_delay = max(0.0, scan_delay)
        # Emit a terminal scan_summary result carrying the completeness/health
        # metrics. On by default — it is how a caller detects a partial scan.
        self.emit_summary = emit_summary
        # Default to nmap's top-100 (not the 35-port TOP_TCP_PORTS) so a no-arg
        # scan doesn't silently miss common services — a recall win for
        # standalone/default runs. Explicit -p/--profile still overrides.
        self.ports = list(_NMAP_TOP_100 if ports is None else ports)
        # Per-host RTT-adaptive probe timeout (Jacobson/Karels, like TCP's RTO).
        # A fixed timeout is too short on a slow WAN host (its OPEN ports get
        # mislabeled filtered) and needlessly long on a fast LAN. When on, the
        # first probe uses `timeout` as the base, then each host's timeout tracks
        # its own SRTT+4*RTTVAR. Off = the old fixed-timeout behaviour.
        self.adaptive_timeout = adaptive_timeout
        # Extra connect attempts on silence only (no_response). 0 = single probe
        # (old behaviour). A definitive RST / refused is conclusive and never
        # retried; only ambiguous silence — which one dropped packet can fake —
        # gets another chance, cutting scanner-manufactured false negatives.
        self.retries = max(0, retries)
        # AIMD congestion control over the in-flight probe window (per host).
        # The fixed RateLimiter keeps a CONSTANT rate, so when a target starts
        # dropping SYNs -- because its own RFC-1812 ICMP error budget is
        # saturated, or a middlebox is shedding load -- the scanner keeps
        # hammering, causing more drops, each of which is reported `filtered`.
        # AIMD reads that loss and backs off, which RAISES recall. It starts at
        # full concurrency, so a healthy LAN scan is not slowed down.
        self.congestion = congestion
        # Fraction of recent probes that must still get a DEFINITIVE answer for
        # the path to count as healthy. Above it, silence is read as host policy
        # (do not throttle); below it, delivery has genuinely collapsed and AIMD
        # backs off. 0.35 sits well clear of both measured regimes: an
        # RST-suppressing Windows host still answers ~97% of probes definitively,
        # while a path under 60% induced packet loss falls far below it.
        self.delivery_floor = max(0.0, min(1.0, delivery_floor))
        self._probe_window: deque[bool] = deque()
        self._probe_window_size = 256
        self._probe_window_min = 32
        # Cleanup pass over ports still ambiguous after the main sweep.
        #
        # WHY (measured, 192.168.1.65 over LAN, 2026-09-03): a fast sweep
        # (rate 300 / concurrency 200) reported 69 ports `filtered`. Re-probing
        # only those at rate 40 / concurrency 10 resolved ALL 69 as `closed`
        # (connection_refused) in 5.4s — every one had been a FALSE NEGATIVE.
        # The host was rate-limiting its RSTs; the fast pass outran them.
        #
        # AIMD already detects that loss and backs the window off, but the
        # per-port retries are spent EARLY, at the aggressive rate, before the
        # controller has converged. So the converged rate is knowledge we
        # acquire and then throw away. This pass spends it: ambiguous ports get
        # one more, deliberately gentle look. `filtered` should mean "a firewall
        # swallowed this", not "we probed too fast to hear the refusal".
        self.reprobe = reprobe
        self.reprobe_rate = max(1.0, reprobe_rate)
        self.reprobe_concurrency = max(1, reprobe_concurrency)
        self.reprobe_retries = max(0, reprobe_retries)
        # off by default: only emit OPEN. When on, every non-open state
        # (closed/filtered/unreachable/error) is preserved with its reason so
        # you can answer "why wasn't 902 reported open?" — a UI can still hide
        # them, but the engine no longer throws the evidence away.
        self.report_closed = report_closed
        # Which scanner/host produced this observation. Exposure is path-
        # dependent, so the vantage is part of the evidence: the same port can
        # be OPEN from one network and FILTERED from another.
        self.vantage = vantage or socket.gethostname()

    def _build(self, target: str, port: int, state: str, reason: str,
               evidence: str | None, *, rtt_ms: float | None = None,
               error: str | None = None, errno_val: int | None = None,
               src_ip: str | None = None, family: str | None = None,
               attempts: int = 1, stack: dict | None = None) -> ScanResult:
        data: dict = {
            "reason": reason,
            "method": "connect",
            "vantage": self.vantage,
            "confidence": _CONFIDENCE.get(state, "low"),
        }
        if family:
            data["family"] = family      # ipv4 / ipv6 the observation reached
        if rtt_ms is not None:
            data["rtt_ms"] = rtt_ms
        if errno_val is not None:
            data["errno"] = errno_val
        if src_ip:
            data["src_ip"] = src_ip       # local address that reached the target
        if attempts > 1:
            data["attempts"] = attempts   # how many probes it took (retransmit)
        if stack:
            # Peer TCP-stack signals (MSS/wscale/kernel RTT) harvested from the
            # handshake we already completed — no extra packets. Downstream
            # os_fingerprint turns mss into a path-MTU/link hint and wscale into
            # a p0f-style stack discriminator.
            data["tcp_stack"] = stack
            if "mss" in stack:
                data["mss"] = stack["mss"]
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status=state, data=data, evidence=evidence, error=error)

    async def _attempt(self, target: str, port: int,
                       est: AdaptiveTimeout | None = None,
                       min_timeout: float | None = None) -> ScanResult:
        """One connect() and its classification. Always returns a ScanResult
        (open or otherwise); retry/emit decisions belong to `_scan_port`.

        `est`, when given, supplies the per-host adaptive timeout and is fed the
        RTT of every DEFINITIVE answer (a completed handshake or an RST) — never
        a timeout, whose duration is not a real round-trip."""
        to = est.timeout() if est is not None else self.timeout
        if min_timeout is not None:
            # The cleanup pass raises the floor: a converged estimator can be
            # tuned to a fast path that was, in fact, dropping our packets.
            to = max(to, min_timeout)
        t0 = time.monotonic()
        try:
            local_addr = ("", self.source_port) if self.source_port else None
            fut = asyncio.open_connection(target, port, local_addr=local_addr)
            reader, writer = await asyncio.wait_for(fut, timeout=to)
            rtt_ms = round((time.monotonic() - t0) * 1000, 2)
            src_ip = peer_ip = None
            stack: dict = {}
            try:
                sockname = writer.get_extra_info("sockname")
                if sockname:
                    src_ip = sockname[0]
                peername = writer.get_extra_info("peername")
                if peername:
                    peer_ip = peername[0]
                # Free OS/link intel off the socket we already opened.
                stack = _harvest_tcp_stack(writer.get_extra_info("socket"))
            except Exception:
                pass
            if est is not None:
                # Prefer the KERNEL's smoothed RTT when the platform exposes it:
                # our wall-clock figure also contains event-loop scheduling delay,
                # which inflates the estimate and so lengthens every later timeout.
                kernel_rtt_us = stack.get("rtt_us")
                est.observe(kernel_rtt_us / 1_000_000.0 if kernel_rtt_us
                            else rtt_ms / 1000.0)
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            return self._build(
                target, port, "open", "connect_success",
                "tcp connect completed (3-way handshake)",
                rtt_ms=rtt_ms, src_ip=src_ip, stack=stack,
                family=_family_of(peer_ip) or _family_of(target))
        except asyncio.TimeoutError:
            # Our wait_for fired: no answer at all within the deadline. Silence
            # is ambiguous, so this is filtered/no_response, not a guaranteed
            # firewall — medium confidence (see _CONFIDENCE). Eligible for retry.
            # NOT fed to `est`: a timeout's duration is the deadline, not an RTT.
            rtt_ms = round((time.monotonic() - t0) * 1000, 2)
            return self._build(
                target, port, "filtered", "no_response",
                f"no response within {to:g}s",
                rtt_ms=rtt_ms, family=_family_of(target))
        except OSError as exc:
            rtt_ms = round((time.monotonic() - t0) * 1000, 2)
            state, reason = classify_os_error(exc)
            if est is not None and state == "closed":
                est.observe(rtt_ms / 1000.0)   # an RST is a real round-trip too
            return self._build(
                target, port, state, reason, None,
                rtt_ms=rtt_ms, error=str(exc),
                errno_val=getattr(exc, "errno", None),
                family=_family_of(target))

    async def _scan_port(self, target: str, port: int,
                         est: AdaptiveTimeout | None = None,
                         cwnd: AdaptiveRateController | None = None) -> ScanResult:
        """One port's terminal result, gated by the rate limiter and (when
        enabled) the per-host AIMD congestion window.

        `cwnd` bounds how many probes are in flight to THIS host and shrinks
        multiplicatively when probes come back silent, so a host that has started
        shedding our packets is probed more gently instead of harder. Every
        `acquire()` is matched by exactly one success/loss report in `finally`,
        or the window would leak and eventually deadlock the worker pool."""
        await self.limiter.wait()
        if cwnd is not None:
            await cwnd.acquire()
        result: ScanResult | None = None
        try:
            async with self.sem:
                result = await self._attempt(target, port, est)
                # Retransmit ONLY on silence — a lost packet can fake it. A
                # definitive RST/refused/unreachable is conclusive; don't waste
                # probes re-confirming it. The retry re-reads est.timeout(), so a
                # slow host that warmed up the estimator gets a longer second chance.
                attempt = 1
                while (attempt <= self.retries
                       and result.status == "filtered"
                       and (result.data or {}).get("reason") == "no_response"):
                    attempt += 1
                    await self.limiter.wait()
                    result = await self._attempt(target, port, est)
                if attempt > 1:
                    result.data["attempts"] = attempt
            # Always return the terminal result; output filtering (open-only vs
            # --report-closed) happens in the worker so metrics see every port.
            return result
        finally:
            if cwnd is not None:
                # A definitive answer proves the path carried our packets.
                # Silence is AMBIGUOUS: it may be congestion, or it may simply be
                # this host's RST policy. Only treat it as congestion when recent
                # delivery has actually fallen off (see _note_probe_outcome) —
                # otherwise a host that suppresses RSTs throttles us to a crawl.
                definitive = not (result is None
                                  or (result.status == "filtered"
                                      and (result.data or {}).get("reason")
                                      == "no_response"))
                lost = not self._note_probe_outcome(definitive)
                try:
                    await (cwnd.report_loss() if lost else cwnd.report_success())
                except asyncio.CancelledError:
                    raise
                except Exception:      # never let telemetry break a scan
                    LOG.debug("congestion window report failed", exc_info=True)

    def _note_probe_outcome(self, definitive: bool) -> bool:
        """Record one probe and answer: is the PATH still delivering?

        WHY THIS EXISTS (measured regression, 2026-09-05). The congestion window
        originally treated every silent port as a loss signal. On a host that
        rate-limits its RSTs — which is common, and which this codebase already
        documents — a large, roughly CONSTANT fraction of ports go silent as a
        matter of host POLICY, not path congestion. Because multiplicative
        decrease (/2) far outpaces additive increase (+1/cwnd), that constant
        background of "loss" ratchets the window to its floor and it never
        recovers. Measured against a real Windows host: a bounded 1121-port scan
        ran at 13.3 ports/sec, while the SAME envelope over the full 65,535-port
        range collapsed to 0.62 ports/sec — a 24-hour scan.

        Congestion control must react to a CHANGE in delivery, not to a steady
        rate of non-answers. So we keep a rolling window of recent outcomes and
        only call it loss when definitive answers (SYN-ACK / RST / unreachable)
        genuinely dry up. A host that keeps answering most probes is delivering,
        whatever its RST policy; a genuinely lossy path stops answering at all
        and still trips the backoff (verified with 60% netem loss).
        """
        self._probe_window.append(definitive)
        if len(self._probe_window) > self._probe_window_size:
            self._probe_window.popleft()
        # Below the sample floor we have no opinion yet — never throttle on noise.
        if len(self._probe_window) < self._probe_window_min:
            return True
        delivered = sum(self._probe_window) / len(self._probe_window)
        return delivered >= self.delivery_floor

    @staticmethod
    def _is_ambiguous(result: ScanResult) -> bool:
        """True for the one state a retry can legitimately change: silence."""
        return (result.status == "filtered"
                and (result.data or {}).get("reason") == "no_response")

    async def _reprobe_ambiguous(self, target: str, ports: list[int],
                                 est: AdaptiveTimeout | None) -> dict[int, ScanResult]:
        """Gentle second look at ports that stayed silent through the main sweep.

        Deliberately slow and narrow — low rate, small window, extra retries and
        a raised timeout floor. Silence under load is ambiguous; silence when we
        are barely touching the host is real evidence. Only ports that resolve
        DEFINITIVELY are returned, so this can correct a false `filtered` but can
        never invent one."""
        resolved: dict[int, ScanResult] = {}
        limiter = RateLimiter(self.reprobe_rate)
        sem = asyncio.Semaphore(min(self.reprobe_concurrency, max(1, len(ports))))
        floor = max(self.timeout, 3.0)

        async def _one(port: int) -> None:
            async with sem:
                for attempt in range(1, self.reprobe_retries + 2):
                    await limiter.wait()
                    r = await self._attempt(target, port, est, min_timeout=floor)
                    if not self._is_ambiguous(r):
                        r.data["reprobe"] = {"attempts": attempt,
                                             "rate": self.reprobe_rate}
                        resolved[port] = r
                        return

        await asyncio.gather(*(_one(p) for p in ports))
        return resolved

    async def scan_target(self, target: str) -> list[ScanResult]:
        """Bounded worker-pool scan of every requested port.

        A fixed pool of `concurrency` workers drains a queue of ports, so a full
        65,535-port scan keeps at most `concurrency` per-port coroutines live at
        once instead of allocating one task per port up front (bounded memory +
        natural backpressure). Every port is dequeued exactly once and produces
        exactly one terminal result, tallied in ScanMetrics before any output
        filtering — so the engine can prove requested == attempted == classified.
        """
        t0 = time.monotonic()
        metrics = ScanMetrics(target=target, vantage=self.vantage,
                              ports_requested=len(self.ports),
                              requested_ports=set(self.ports))
        # One adaptive-timeout estimator PER host: exposure and path RTT are
        # per-target, so ports of the same host share (and warm up) one timer.
        est = None
        if self.adaptive_timeout:
            est = AdaptiveTimeout(
                base=self.timeout,
                minimum=min(0.3, self.timeout),
                maximum=max(self.timeout, 8.0),
            )
        # One AIMD congestion window PER host, for the same reason the timer is
        # per host: loss is a property of the path to THAT target. It starts at
        # full concurrency (so a healthy scan runs at today's speed) and only
        # shrinks if this host starts swallowing probes.
        # Delivery history is a property of the path to THIS host, exactly like
        # the congestion window and the RTT estimator. Carrying it across targets
        # would let one quiet host throttle the next.
        self._probe_window.clear()
        cwnd = None
        if self.congestion:
            cwnd = AdaptiveRateController(
                init_window=max(1, self._concurrency),
                # Never serialise completely. A window of 1 turns a 65,535-port
                # sweep into a 12-hour crawl, and the extra politeness buys
                # nothing: a host that is rate-limiting will rate-limit whether
                # we have 1 probe in flight or 8. Backing off 80 -> 8 is still a
                # 10x reduction, which is a real and sufficient concession.
                min_window=max(1, self._concurrency // 10),
                max_window=max(1, self._concurrency),
            )
        queue: asyncio.Queue[int] = asyncio.Queue()
        # Evasion: shuffle the probe order so it isn't a sequential-port sweep.
        _order = random.sample(self.ports, len(self.ports)) if self.randomize else self.ports
        for p in _order:
            queue.put_nowait(p)
        emitted: list[ScanResult] = []
        # Collected first, recorded after the cleanup pass, so ScanMetrics sees
        # each port exactly once carrying its FINAL state (re-recording a
        # corrected port would register as a duplicate and fail completeness).
        collected: dict[int, ScanResult] = {}

        async def _worker() -> None:
            while True:
                try:
                    port = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                try:
                    result = await self._scan_port(target, port, est, cwnd)
                    collected[port] = result
                finally:
                    queue.task_done()
                    if self.scan_delay:              # jittered per-probe pause (evasion)
                        await asyncio.sleep(jittered_delay(self.scan_delay))

        n_workers = max(1, min(self._concurrency, len(self.ports)))
        workers = [asyncio.create_task(_worker()) for _ in range(n_workers)]
        try:
            await asyncio.gather(*workers)
        except asyncio.CancelledError:            # clean cancellation on interrupt
            for w in workers:
                w.cancel()
            raise
        # --- cleanup pass -------------------------------------------------
        ambiguous = sorted(p for p, r in collected.items() if self._is_ambiguous(r))
        reprobe_stats: dict | None = None
        if self.reprobe and ambiguous:
            recovered = await self._reprobe_ambiguous(target, ambiguous, est)
            collected.update(recovered)
            reprobe_stats = {
                "candidates": len(ambiguous),
                "resolved": len(recovered),
                "remaining": len(ambiguous) - len(recovered),
                "rate": self.reprobe_rate,
            }
            if recovered:
                LOG.info("[port_scan] cleanup pass resolved %d/%d ambiguous ports "
                         "on %s (were reported filtered)",
                         len(recovered), len(ambiguous), target)

        # Record FINAL states, then apply output filtering.
        for port in sorted(collected):
            result = collected[port]
            metrics.record(result)
            if result.status == "open" or self.report_closed:
                emitted.append(result)

        metrics.duration_s = round(time.monotonic() - t0, 3)
        if self.emit_summary:
            summ = metrics.summary()
            if self.scan_meta:
                summ["audit"] = self.scan_meta        # profile + ulimit + concurrency
            if reprobe_stats is not None:
                # A high `resolved` count means the main sweep was too aggressive
                # for this host: those ports would have been reported `filtered`.
                summ["reprobe"] = reprobe_stats
            if cwnd is not None:
                # A window that ended far below the starting concurrency means the
                # path was shedding probes: the operator needs to know the scan was
                # throttled, because it changes how much to trust `filtered`.
                summ["congestion"] = {
                    "final_window": cwnd.window,
                    "max_window": cwnd.max_window,
                    "throttled": cwnd.window < cwnd.max_window,
                }
            ev = (f"{metrics.ports_attempted}/{metrics.ports_requested} "
                  f"ports scanned, {metrics.open} open, "
                  f"health={'degraded' if metrics.degraded else 'ok'}")
            if summ["tarpit"]["likely_tarpit"]:
                ev += " — LIKELY TARPIT/HONEYPOT (open ports unreliable)"
            emitted.append(ScanResult(
                self.name, target, proto="tcp", status="scan_summary",
                data=summ, evidence=ev))
        return emitted


def main() -> None:
    parser = base_argparser("TCP connect port scanner (evidence-based states)")
    parser.add_argument("-p", "--ports", default=None,
                        help="ports e.g. '22,80,443,8000-8100' (default: nmap top-100)")
    parser.add_argument("--fixed-timeout", action="store_true",
                        help="disable per-host RTT-adaptive timeout; use the fixed "
                             "--timeout for every probe (old behaviour)")
    parser.add_argument("--no-reprobe", action="store_true",
                        help="skip the gentle cleanup pass over ports that stayed "
                             "silent (faster, but a host that rate-limits its RSTs "
                             "will have those ports reported 'filtered')")
    parser.add_argument("--no-congestion", action="store_true",
                        help="disable the per-host AIMD congestion window (probe "
                             "at constant concurrency even when the target starts "
                             "dropping probes)")
    parser.add_argument("-A", "--all-ports", action="store_true",
                        help="scan the full TCP range 1-65535 (first-class mode)")
    parser.add_argument("--report-closed", action="store_true",
                        help="also emit closed/filtered/unreachable/error states "
                             "with their reason (noisier, but explains WHY a port "
                             "was not reported open)")
    parser.add_argument("--vantage", default=None,
                        help="label for this scanner's network vantage point "
                             "(default: hostname) — exposure is path-dependent")
    parser.add_argument("--retries", type=int, default=1,
                        help="extra connect attempts on silence only (default 1; "
                             "0 = single probe). RST/refused is never retried.")
    parser.add_argument("--profile",
                        choices=["quick", "top100", "top1000", "full", "custom"],
                        default=None,
                        help="named coverage profile (quick/top100/top1000/full/"
                             "custom). 'custom' uses -p. Overrides -p/-A unless "
                             "'custom'. 'full' == 1-65535.")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        profile_name = None
        if args.profile:
            custom = parse_ports(args.ports) if args.ports else None
            ports = resolve_profile(args.profile, custom)
            profile_name = args.profile
        elif args.all_ports:
            ports = ALL_TCP_PORTS
            profile_name = "full"
        elif args.ports:
            ports = parse_ports(args.ports)
            profile_name = "custom"
        else:
            ports = None
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)

        # Size concurrency below the fd ceiling (raising it first) so a full-range
        # scan never silently loses ports to EMFILE. Log the values for audit.
        fd_soft, fd_hard = raise_fd_limit()
        concurrency = safe_connect_concurrency(args.concurrency)
        n_ports = len(ports) if ports is not None else "default"
        LOG.info("port scan: profile=%s ports=%s fd_ulimit soft=%d hard=%d "
                 "concurrency=%d (requested %d)",
                 profile_name, n_ports, fd_soft, fd_hard, concurrency, args.concurrency)
        scan_meta = {"profile": profile_name, "fd_soft": fd_soft, "fd_hard": fd_hard,
                     "concurrency": concurrency, "concurrency_requested": args.concurrency}

        scanner = PortScanner(scope, rate=args.rate, concurrency=concurrency,
                              timeout=args.timeout, ports=ports,
                              report_closed=args.report_closed,
                              vantage=args.vantage, retries=args.retries,
                              adaptive_timeout=not args.fixed_timeout,
                              congestion=not args.no_congestion,
                              reprobe=not args.no_reprobe,
                              source_port=args.source_port,
                              randomize=args.randomize, scan_delay=args.scan_delay,
                              scan_meta=scan_meta)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
