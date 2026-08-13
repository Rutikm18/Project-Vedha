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
import errno as _errno
import ipaddress
import socket
import time

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, TOP_TCP_PORTS, setup_logging, base_argparser,
    main_entrypoint,
)


# --------------------------------------------------------------------------- #
# errno -> (state, reason). The heart of the state engine: the OS kernel does
# the packet-level TCP work for us and hands back an errno; we translate that
# into exposure truth instead of flattening everything to "filtered".
# --------------------------------------------------------------------------- #
_ERRNO_MAP: dict[int, tuple[str, str]] = {
    _errno.ECONNREFUSED:  ("closed",      "connection_refused"),   # RST
    _errno.ECONNRESET:    ("closed",      "connection_reset"),
    _errno.ETIMEDOUT:     ("filtered",    "no_response"),          # kernel timeout
    _errno.ECONNABORTED:  ("filtered",    "connection_aborted"),
    _errno.EHOSTUNREACH:  ("unreachable", "host_unreachable"),     # ICMP host unreach
    _errno.ENETUNREACH:   ("unreachable", "network_unreachable"),  # ICMP net unreach
    _errno.EHOSTDOWN:     ("unreachable", "host_down"),
    _errno.EACCES:        ("error",       "permission_denied"),
    _errno.EPERM:         ("error",       "permission_denied"),
    _errno.EMFILE:        ("error",       "local_resource_error"), # out of fds
    _errno.ENFILE:        ("error",       "local_resource_error"),
    _errno.ENOBUFS:       ("error",       "local_resource_error"),
    _errno.ENOMEM:        ("error",       "local_resource_error"),
    _errno.EADDRNOTAVAIL: ("error",       "address_unavailable"),
    _errno.EADDRINUSE:    ("error",       "address_in_use"),
    _errno.ENETDOWN:      ("error",       "interface_down"),
    _errno.ENETRESET:     ("error",       "interface_error"),
}

# Rough confidence per state — silence and ICMP inferences are weaker evidence
# than a completed handshake or an explicit RST.
_CONFIDENCE: dict[str, str] = {
    "open":        "high",
    "closed":      "high",
    "filtered":    "medium",
    "unreachable": "medium",
    "error":       "low",
}


def _family_of(ip: str | None) -> str | None:
    """Return 'ipv4'/'ipv6' for an IP literal, else None (unresolved hostname)."""
    if not ip:
        return None
    try:
        return "ipv6" if ipaddress.ip_address(ip).version == 6 else "ipv4"
    except ValueError:
        return None


def classify_os_error(exc: OSError) -> tuple[str, str]:
    """
    Map a connect()-time OSError to (state, reason).

    DNS failures (socket.gaierror, a subclass of OSError whose .errno uses the
    unrelated EAI_* namespace) are caught first. Anything we don't recognize
    stays visible as ('error', 'os_error') rather than being mislabeled
    'filtered' — an unknown local failure is not evidence of a target firewall.
    """
    if isinstance(exc, socket.gaierror):
        return "error", "dns_error"
    mapped = _ERRNO_MAP.get(exc.errno)
    if mapped is not None:
        return mapped
    return "error", "os_error"


class PortScanner(BaseScanner):
    name = "port_scan"

    def __init__(self, *args, ports: list[int] | None = None,
                 report_closed: bool = False, vantage: str | None = None,
                 retries: int = 1, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = list(TOP_TCP_PORTS if ports is None else ports)
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

    async def _attempt(self, target: str, port: int) -> ScanResult:
        """One connect() and its classification. Always returns a ScanResult
        (open or otherwise); retry/emit decisions belong to `_scan_port`."""
        t0 = time.monotonic()
        try:
            fut = asyncio.open_connection(target, port)
            reader, writer = await asyncio.wait_for(fut, timeout=self.timeout)
            rtt_ms = round((time.monotonic() - t0) * 1000, 2)
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
            rtt_ms = round((time.monotonic() - t0) * 1000, 2)
            return self._build(
                target, port, "filtered", "no_response",
                f"no response within {self.timeout:g}s",
                rtt_ms=rtt_ms, family=_family_of(target))
        except OSError as exc:
            rtt_ms = round((time.monotonic() - t0) * 1000, 2)
            state, reason = classify_os_error(exc)
            return self._build(
                target, port, state, reason, None,
                rtt_ms=rtt_ms, error=str(exc),
                errno_val=getattr(exc, "errno", None),
                family=_family_of(target))

    async def _scan_port(self, target: str, port: int) -> ScanResult | None:
        await self.limiter.wait()
        async with self.sem:
            result = await self._attempt(target, port)
            # Retransmit ONLY on silence — a lost packet can fake it. A
            # definitive RST/refused/unreachable is conclusive; don't waste
            # probes re-confirming it.
            attempt = 1
            while (attempt <= self.retries
                   and result.status == "filtered"
                   and (result.data or {}).get("reason") == "no_response"):
                attempt += 1
                await self.limiter.wait()
                result = await self._attempt(target, port)
            if attempt > 1:
                result.data["attempts"] = attempt

        if result.status == "open" or self.report_closed:
            return result
        return None

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]


# Full TCP port space, materialized once so --all-ports is a first-class mode
# rather than an ad-hoc "-p 1-65535" string the operator has to remember.
ALL_TCP_PORTS = list(range(1, 65536))


def main() -> None:
    parser = base_argparser("TCP connect port scanner (evidence-based states)")
    parser.add_argument("-p", "--ports", default=None,
                        help="ports e.g. '22,80,443,8000-8100' (default: top ports)")
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
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        if args.all_ports:
            ports = ALL_TCP_PORTS
        elif args.ports:
            ports = parse_ports(args.ports)
        else:
            ports = None
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = PortScanner(scope, rate=args.rate, concurrency=args.concurrency,
                              timeout=args.timeout, ports=ports,
                              report_closed=args.report_closed,
                              vantage=args.vantage, retries=args.retries)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
