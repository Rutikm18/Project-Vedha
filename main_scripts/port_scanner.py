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
import time
from collections import Counter
from dataclasses import dataclass, field

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser,
    main_entrypoint, classify_os_error, STATE_CONFIDENCE, jittered_delay,
    assess_tarpit, LOG, raise_fd_limit, safe_connect_concurrency,
)
from .adaptive_timeout import AdaptiveTimeout

# The errno→(state,reason) classifier now lives in scanner_base (Phase 2 — one
# shared model). Local alias kept so existing references are unchanged.
_CONFIDENCE = STATE_CONFIDENCE


# _ERRNO_MAP, STATE_CONFIDENCE and classify_os_error moved to scanner_base
# (Phase 2 — one shared errno→state classifier for TCP, UDP and deeper scanners).


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
               attempts: int = 1) -> ScanResult:
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
        return ScanResult(self.name, target, port=port, proto="tcp",
                          status=state, data=data, evidence=evidence, error=error)

    async def _attempt(self, target: str, port: int,
                       est: AdaptiveTimeout | None = None) -> ScanResult:
        """One connect() and its classification. Always returns a ScanResult
        (open or otherwise); retry/emit decisions belong to `_scan_port`.

        `est`, when given, supplies the per-host adaptive timeout and is fed the
        RTT of every DEFINITIVE answer (a completed handshake or an RST) — never
        a timeout, whose duration is not a real round-trip."""
        to = est.timeout() if est is not None else self.timeout
        t0 = time.monotonic()
        try:
            local_addr = ("", self.source_port) if self.source_port else None
            fut = asyncio.open_connection(target, port, local_addr=local_addr)
            reader, writer = await asyncio.wait_for(fut, timeout=to)
            rtt_ms = round((time.monotonic() - t0) * 1000, 2)
            if est is not None:
                est.observe(rtt_ms / 1000.0)   # real RTT: SYN→SYN/ACK
            src_ip = peer_ip = None
            try:
                sockname = writer.get_extra_info("sockname")
                if sockname:
                    src_ip = sockname[0]
                peername = writer.get_extra_info("peername")
                if peername:
                    peer_ip = peername[0]
            except Exception:
                pass
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            return self._build(
                target, port, "open", "connect_success",
                "tcp connect completed (3-way handshake)",
                rtt_ms=rtt_ms, src_ip=src_ip,
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
                         est: AdaptiveTimeout | None = None) -> ScanResult:
        await self.limiter.wait()
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
        queue: asyncio.Queue[int] = asyncio.Queue()
        # Evasion: shuffle the probe order so it isn't a sequential-port sweep.
        _order = random.sample(self.ports, len(self.ports)) if self.randomize else self.ports
        for p in _order:
            queue.put_nowait(p)
        emitted: list[ScanResult] = []

        async def _worker() -> None:
            while True:
                try:
                    port = queue.get_nowait()
                except asyncio.QueueEmpty:
                    return
                try:
                    result = await self._scan_port(target, port, est)
                    metrics.record(result)           # count EVERY attempt
                    if result.status == "open" or self.report_closed:
                        emitted.append(result)       # output filtering only
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
        metrics.duration_s = round(time.monotonic() - t0, 3)
        if self.emit_summary:
            summ = metrics.summary()
            if self.scan_meta:
                summ["audit"] = self.scan_meta        # profile + ulimit + concurrency
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
