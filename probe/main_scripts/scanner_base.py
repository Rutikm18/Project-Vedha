"""
scanner_base.py — shared foundation for every scanner module.

SCOPE OF THIS MODULE (read before use):
  * This is a COLLECTION / SCANNING layer only. It observes and records.
  * It does NOT exploit, brute-force, spray credentials, or modify any target.
  * It does NOT do correlation, CVE matching, or risk scoring — that is a
    separate layer. Each scanner here only reports what it directly observed.

Every scanner inherits from BaseScanner, which enforces three things before any
network operation touches a host:
  1. ScopeGuard  — the target must be inside the authorized allowlist.
  2. RateLimiter — global pacing so a scan never floods a network.
  3. ScanResult  — one normalized output schema, so you can measure accuracy
                   and false-positive rate per scanner consistently.

Run any scanner standalone (e.g. `python -m scanner.port_scanner ...`) and it
will emit newline-delimited JSON (JSONL) you can diff against ground truth.
"""

from __future__ import annotations

import argparse
import asyncio
import errno as _errno
import ipaddress
import json
import logging
import os
import socket
import struct
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

LOG = logging.getLogger("scanner")


# ── wire identity (anti-attribution) ──────────────────────────────────────────
# What the scanner puts in packets a defender can SEE. Defaults are deliberately
# generic so the tool never signs its own traffic with a brand string a blue team
# can grep, alert on, or attribute to the engagement. Override per-engagement via
# env when you WANT to be identifiable (authorized/cooperative assessments).
_DEFAULT_USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/125.0.0.0 Safari/537.36")
# Windows ping's default 32-byte payload — blends in as ordinary ICMP echo traffic.
_DEFAULT_PROBE_PAYLOAD = b"abcdefghijklmnopqrstuvwabcdefghi"


def user_agent() -> str:
    """HTTP/RTSP User-Agent to send — a generic browser UA by default so it does
    not attribute the scan. Override with the VEDHA_SCAN_UA env var."""
    return os.environ.get("VEDHA_SCAN_UA") or _DEFAULT_USER_AGENT


def probe_payload() -> bytes:
    """Benign, non-attributing payload for ICMP/UDP probes — looks like ordinary
    ping traffic by default. Override with the VEDHA_SCAN_PAYLOAD env var."""
    override = os.environ.get("VEDHA_SCAN_PAYLOAD")
    return override.encode() if override is not None else _DEFAULT_PROBE_PAYLOAD


# --------------------------------------------------------------------------- #
# Result schema — identical across every scanner.
# --------------------------------------------------------------------------- #
# ── canonical scan-state model (Phase 1) ────────────────────────────────────
# ONE normalized state vocabulary shared by TCP, UDP and the deeper scanners.
# `status` is the classification; `reason` is WHY — they are always separate.
# Values are kept wire-compatible with the existing JSONL output on purpose
# (renaming them would break saved scans and downstream parsers).
OPEN = "open"
CLOSED = "closed"
FILTERED = "filtered"
OPEN_FILTERED = "open|filtered"   # no app response AND no ICMP — undecidable
UNREACHABLE = "unreachable"
ERROR = "error"
SCAN_SUMMARY = "scan_summary"

CANONICAL_STATES = frozenset({OPEN, CLOSED, FILTERED, OPEN_FILTERED, UNREACHABLE, ERROR})

# State-semantic fields that belong at the top level, never hidden in `data`.
_PROMOTED_FIELDS = ("reason", "method", "confidence", "family", "src_ip",
                    "interface", "vantage", "attempts", "rtt_ms", "errno")


# ── shared OS-error → state classifier (Phase 2) ────────────────────────────
# The kernel does the packet-level TCP work and hands back an errno; we translate
# that to (state, reason) so a scanner-side / OS failure is NEVER mislabeled as a
# target "filtered". ONE map, shared by TCP, UDP and the deeper scanners so every
# module classifies identically. Reason strings are kept stable (consumers and
# the health metrics key off them).
_ERRNO_MAP: dict[int, tuple[str, str]] = {
    _errno.ECONNREFUSED:  (CLOSED,      "connection_refused"),   # RST
    _errno.ECONNRESET:    (CLOSED,      "connection_reset"),
    _errno.ETIMEDOUT:     (FILTERED,    "no_response"),          # kernel timeout
    _errno.ECONNABORTED:  (FILTERED,    "connection_aborted"),
    _errno.EHOSTUNREACH:  (UNREACHABLE, "host_unreachable"),     # ICMP host unreach
    _errno.ENETUNREACH:   (UNREACHABLE, "network_unreachable"),  # ICMP net unreach
    _errno.EHOSTDOWN:     (UNREACHABLE, "host_down"),
    _errno.EACCES:        (ERROR,       "permission_denied"),
    _errno.EPERM:         (ERROR,       "permission_denied"),
    _errno.EMFILE:        (ERROR,       "local_resource_error"), # out of fds
    _errno.ENFILE:        (ERROR,       "local_resource_error"),
    _errno.ENOBUFS:       (ERROR,       "local_resource_error"),
    _errno.ENOMEM:        (ERROR,       "local_resource_error"),
    _errno.EADDRNOTAVAIL: (ERROR,       "address_unavailable"),
    _errno.EADDRINUSE:    (ERROR,       "address_in_use"),
    _errno.ENETDOWN:      (ERROR,       "interface_down"),
    _errno.ENETRESET:     (ERROR,       "interface_error"),
}

# Confidence per state — silence/ICMP inferences are weaker evidence than a
# completed handshake or an explicit RST.
STATE_CONFIDENCE: dict[str, str] = {
    OPEN: "high", CLOSED: "high", FILTERED: "medium",
    UNREACHABLE: "medium", ERROR: "low",
}


def classify_os_error(exc: OSError) -> tuple[str, str]:
    """Map a connect()/socket-time OSError to (state, reason).

    DNS failures (``socket.gaierror``, whose ``.errno`` uses the unrelated EAI_*
    namespace) are caught first. An UNKNOWN errno stays visible as
    ``('error', 'socket_error_<errno>')`` — never mislabeled 'filtered', because a
    local/OS failure is not evidence of a target firewall.
    """
    if isinstance(exc, socket.gaierror):
        return ERROR, "dns_error"
    mapped = _ERRNO_MAP.get(exc.errno)
    if mapped is not None:
        return mapped
    return ERROR, (f"socket_error_{exc.errno}" if exc.errno else "os_error")


def describe_os_error(exc: OSError) -> dict[str, Any]:
    """Full, debuggable classification for attaching to a ScanResult: state,
    reason, errno, exception type and a human message — so a scanner-side failure
    is fully visible and never hidden inside a bare 'filtered'."""
    state, reason = classify_os_error(exc)
    return {
        "status": state,
        "reason": reason,
        "errno": getattr(exc, "errno", None),
        "exc_type": type(exc).__name__,
        "error": str(exc) or type(exc).__name__,
    }


@dataclass
class ScanResult:
    """One observation about one target. Pure fact, no interpretation.

    Network-state semantics are FIRST-CLASS fields (Phase 1): a reader never has
    to dig into `data` to learn the state, reason, family, vantage, timing or the
    scanner-side errno. `data` remains for scanner-specific parsed detail only.
    """
    scanner: str                      # which module produced this
    target: str                       # ip or host the observation is about
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    port: int | None = None           # if the observation is port-scoped
    proto: str | None = None          # tcp / udp
    status: str = "observed"          # a CANONICAL_STATES value (+ observed/scan_summary)
    data: dict[str, Any] = field(default_factory=dict)   # scanner-specific parsed fields
    evidence: str | None = None       # raw bytes/banner that justify the result
    error: str | None = None
    # ── first-class network-state semantics (appended to preserve positional
    #    construction compatibility of the fields above) ──
    reason: str | None = None         # why this state: connect_success, tcp_rst, no_response, ...
    method: str | None = None         # how it was probed: connect, syn, udp_probe, ...
    confidence: float | None = None   # 0..1 certainty in the classification
    family: str | None = None         # ipv4 | ipv6
    src_ip: str | None = None         # local address that completed the probe
    interface: str | None = None      # scanning interface
    vantage: str | None = None        # scanner position identity
    attempts: int | None = None       # how many probes were sent
    rtt_ms: float | None = None       # round-trip time of the deciding probe
    errno: int | None = None          # OS errno for a scanner-side / OS result

    def __post_init__(self) -> None:
        # Bridge for existing scanners that still record these inside `data`:
        # promote them to first-class fields (non-destructive — `data` is left
        # intact) so every result exposes state semantics uniformly.
        if isinstance(self.data, dict):
            for k in _PROMOTED_FIELDS:
                if getattr(self, k) is None and self.data.get(k) is not None:
                    setattr(self, k, self.data[k])

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str, ensure_ascii=False)


# --------------------------------------------------------------------------- #
# ScopeGuard — the authorization allowlist. Nothing is scanned unless allowed.
# --------------------------------------------------------------------------- #
class ScopeError(Exception):
    pass


class ScopeGuard:
    """
    Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target
    is in scope. This is the safety control: the scanner refuses to touch
    anything not explicitly authorized.

    Allowlist file format (one entry per line, '#' for comments):
        10.0.0.0/24
        192.168.1.50
        scanme.example.com
    """

    def __init__(self, networks: list[ipaddress._BaseNetwork],
                 hostnames: set[str],
                 excludes: list[ipaddress._BaseNetwork] | None = None):
        self._networks = networks
        self._hostnames = {h.lower() for h in hostnames}
        # Exclusions are subtracted from the allowlist and take precedence over
        # it: a target inside an excluded range is out of scope even if it also
        # falls inside an allowed range. This is the per-job "carve-out" the
        # operator sets in the Scanner UI (e.g. scan 10.0.0.0/24 EXCEPT the
        # fragile PLC at 10.0.0.5).
        self._excludes = excludes or []

    @classmethod
    def from_file(cls, path: str | Path) -> "ScopeGuard":
        try:
            text = Path(path).read_text()
        except OSError as exc:
            raise ScopeError(f"cannot read scope file {str(path)!r}: {exc}") from exc

        nets: list[ipaddress._BaseNetwork] = []
        hosts: set[str] = set()
        for raw in text.splitlines():
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            try:
                nets.append(ipaddress.ip_network(line, strict=False))
            except ValueError:
                hosts.add(line.lower())
        if not nets and not hosts:
            raise ScopeError(f"scope file {str(path)!r} contained no valid entries")
        LOG.info("scope loaded: %d network(s), %d hostname(s)",
                 len(nets), len(hosts))
        return cls(nets, hosts)

    @classmethod
    def from_list(cls, entries: Iterable[str],
                  excludes: Iterable[str] | None = None) -> "ScopeGuard":
        nets, hosts = [], set()
        for line in entries:
            line = line.strip()
            if not line:
                continue
            try:
                nets.append(ipaddress.ip_network(line, strict=False))
            except ValueError:
                hosts.add(line.lower())
        exc_nets: list[ipaddress._BaseNetwork] = []
        for line in (excludes or []):
            line = line.strip()
            if not line:
                continue
            try:
                exc_nets.append(ipaddress.ip_network(line, strict=False))
            except ValueError:
                # a bare excluded hostname can't be range-matched; skip it
                pass
        if exc_nets:
            LOG.info("scope excludes: %d network(s)", len(exc_nets))
        return cls(nets, hosts, exc_nets)

    def in_scope(self, target: str) -> bool:
        t = target.strip().lower()
        try:
            ip = ipaddress.ip_address(t)
        except ValueError:
            ip = None
        # Exclusions win over the allowlist — checked first.
        if ip is not None and any(ip in net for net in self._excludes):
            return False
        if t in self._hostnames:
            return True
        if ip is None:
            # a hostname not explicitly listed is out of scope by default
            return False
        return any(ip in net for net in self._networks)

    def assert_in_scope(self, target: str) -> None:
        if not self.in_scope(target):
            raise ScopeError(f"target {target!r} is NOT in authorized scope")

    def filter(self, targets: Iterable[str]) -> Iterator[str]:
        for t in targets:
            if self.in_scope(t):
                yield t
            else:
                LOG.warning("dropping out-of-scope target: %s", t)

    @property
    def networks(self) -> list[ipaddress._BaseNetwork]:
        """Read-only view of allowed networks (for CIDR-level engines)."""
        return list(self._networks)

    @property
    def excludes(self) -> list[ipaddress._BaseNetwork]:
        """Read-only view of excluded networks (to build masscan --exclude)."""
        return list(self._excludes)


# --------------------------------------------------------------------------- #
# RateLimiter — global pacing across all concurrent tasks.
# --------------------------------------------------------------------------- #
class RateLimiter:
    """Simple async rate limiter: at most `rate` operations per second."""

    def __init__(self, rate: float = 200.0):
        self.min_interval = 1.0 / rate if rate > 0 else 0.0
        self._lock = asyncio.Lock()
        self._next = 0.0

    async def wait(self) -> None:
        if self.min_interval <= 0:
            return
        async with self._lock:
            now = time.monotonic()
            if now < self._next:
                await asyncio.sleep(self._next - now)
                now = time.monotonic()
            self._next = now + self.min_interval


def inet_checksum(data: bytes) -> int:
    """
    Standard 16-bit one's-complement Internet checksum (RFC 1071), used for IP,
    ICMP and TCP headers. Verifying a buffer that already contains its correct
    checksum yields 0. Shared by the SYN and ICMP packet crafters.
    """
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack("!%dH" % (len(data) // 2), data))
    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16
    return ~total & 0xFFFF


# --------------------------------------------------------------------------- #
# AdaptiveRateController — AIMD in-flight window (congestion control).
# --------------------------------------------------------------------------- #
class AdaptiveRateController:
    """
    A self-tuning concurrency window, modelled on TCP congestion control (AIMD),
    for scanning under loss and RFC-1812 ICMP rate limits (see playbook 11).

    Unlike the fixed `RateLimiter` (a constant token bucket), this GROWS the
    number of in-flight probes while replies keep arriving and MULTIPLICATIVELY
    SHRINKS it the moment probes start being lost — the classic signal that the
    network or the target's ICMP-error rate limit is saturated. It therefore
    goes as fast as the path allows without hammering fragile hosts.

    Phases (like TCP):
      * slow start (cwnd < ssthresh): +1 per success  -> ~doubles per RTT.
      * congestion avoidance (cwnd >= ssthresh): +1/cwnd per success -> +1/RTT.
      * on loss: ssthresh = cwnd/2, cwnd = cwnd/2 (bounded by min_window).

    Gate probes with `await acquire()`, then call `report_success()` or
    `report_loss()` exactly once per acquire.
    """

    def __init__(self, *, init_window: int = 10, min_window: int = 1,
                 max_window: int = 300, ssthresh: float | None = None):
        self.min_window = max(1, min_window)
        self.max_window = max(self.min_window, max_window)
        self.cwnd: float = float(min(max(init_window, self.min_window),
                                     self.max_window))
        self.ssthresh: float = float(ssthresh) if ssthresh is not None \
            else float(self.max_window)
        self._in_flight = 0
        self._cond = asyncio.Condition()

    @property
    def window(self) -> int:
        """Current integer window (>= min_window)."""
        return max(self.min_window, int(self.cwnd))

    def _on_success(self) -> None:
        if self.cwnd < self.ssthresh:
            self.cwnd += 1                       # slow start
        else:
            self.cwnd += 1.0 / self.cwnd          # congestion avoidance
        self.cwnd = min(self.cwnd, float(self.max_window))

    def _on_loss(self) -> None:
        self.ssthresh = max(float(self.min_window), self.cwnd / 2.0)
        self.cwnd = max(float(self.min_window), self.cwnd / 2.0)

    async def acquire(self) -> None:
        async with self._cond:
            while self._in_flight >= self.window:
                await self._cond.wait()
            self._in_flight += 1

    async def report_success(self) -> None:
        async with self._cond:
            self._in_flight = max(0, self._in_flight - 1)
            self._on_success()
            self._cond.notify_all()

    async def report_loss(self) -> None:
        async with self._cond:
            self._in_flight = max(0, self._in_flight - 1)
            self._on_loss()
            self._cond.notify_all()


# --------------------------------------------------------------------------- #
# Target expansion — CIDR / range / single host -> list of host strings.
# --------------------------------------------------------------------------- #
def expand_targets(specs: Iterable[str], *, max_hosts: int = 200_000) -> list[str]:
    """
    Accepts CIDRs ('10.0.0.0/24'), single IPs, hostnames, and simple ranges
    ('10.0.0.1-10.0.0.20'). Returns a de-duplicated ordered list of hosts.

    `max_hosts` is a safety net against accidental catastrophic ranges (e.g. a
    typo'd /8): anything that would expand past it raises ValueError instead of
    silently trying to materialize millions of host strings / asyncio tasks.
    For genuinely large sweeps, use mass_scan.py, which scans CIDRs directly
    without pre-expanding them.
    """
    out: list[str] = []
    seen: set[str] = set()

    def add(x: str):
        if x not in seen:
            seen.add(x)
            out.append(x)

    for spec in specs:
        spec = spec.strip()
        if not spec:
            continue
        if "-" in spec and "/" not in spec:
            lo, hi = spec.split("-", 1)
            try:
                start = ipaddress.ip_address(lo.strip())
                end = ipaddress.ip_address(hi.strip())
            except ValueError:
                start = end = None
            if start is not None and end is not None:
                if int(end) < int(start):
                    raise ValueError(
                        f"invalid range {spec!r}: end address before start")
                span = int(end) - int(start) + 1
                if span > max_hosts:
                    raise ValueError(
                        f"range {spec!r} spans {span} hosts, exceeding the "
                        f"{max_hosts}-host safety cap — narrow it or use "
                        f"mass_scan.py for large sweeps")
                for cur in range(int(start), int(end) + 1):
                    add(str(ipaddress.ip_address(cur)))
                continue
        try:
            net = ipaddress.ip_network(spec, strict=False)
        except ValueError:
            add(spec)  # not an IP/CIDR -> treat as hostname
            continue
        if net.num_addresses > max_hosts:
            raise ValueError(
                f"{spec} contains {net.num_addresses} addresses, exceeding the "
                f"{max_hosts}-host safety cap — narrow the CIDR or use "
                f"mass_scan.py for large sweeps")
        if net.num_addresses == 1:
            add(str(net.network_address))
        else:
            for ip in net.hosts():
                add(str(ip))
    return out


def resolve(target: str, port: int, *, proto: str = "tcp"):
    """
    Resolve `target` to a concrete (family, sockaddr) covering IPv4, IPv6, and
    hostnames. Raw-socket scanners MUST use this instead of hardcoding AF_INET
    or they silently miss every IPv6 target. getaddrinfo orders results per RFC
    6724; we take the first usable result. Raises OSError if unresolvable.
    """
    socktype = socket.SOCK_DGRAM if proto == "udp" else socket.SOCK_STREAM
    infos = socket.getaddrinfo(target, port, socket.AF_UNSPEC, socktype)
    if not infos:
        raise OSError(f"cannot resolve {target!r}")
    family, _stype, _proto, _canon, sockaddr = infos[0]
    return family, sockaddr


# --------------------------------------------------------------------------- #
# True-async UDP probe — event-loop native, no thread pool.
# --------------------------------------------------------------------------- #
# Sentinel: an ICMP port-unreachable came back, so the port is *definitively*
# closed — distinct from `None` (no reply = the ambiguous open|filtered state
# that plagues UDP scanning, see playbook 11).
_UDP_CLOSED = object()


class _UDPProbeProtocol(asyncio.DatagramProtocol):
    """
    One-shot datagram protocol backing `async_udp_probe`. Resolves its future
    with the first datagram received, or with `_UDP_CLOSED` when the OS reports
    an ICMP port-unreachable (surfaced as ConnectionRefusedError in
    `error_received`). Everything runs on the event loop — there is no blocking
    `recvfrom` and no executor thread, so thousands of probes are genuinely
    concurrent rather than bounded by the default thread pool.
    """

    def __init__(self, future: "asyncio.Future"):
        self._future = future

    def datagram_received(self, data: bytes, addr) -> None:
        if not self._future.done():
            self._future.set_result(data)

    def error_received(self, exc: Exception) -> None:
        if self._future.done():
            return
        # ICMP port-unreachable => closed. Any other transport error => treat as
        # no usable reply (ambiguous), matching a timeout.
        if isinstance(exc, ConnectionRefusedError):
            self._future.set_result(_UDP_CLOSED)
        else:
            self._future.set_result(None)

    def connection_lost(self, exc) -> None:
        if not self._future.done():
            self._future.set_result(None)


async def async_udp_probe(target: str, port: int, payload: bytes,
                          timeout: float):
    """
    Send one UDP datagram and await the first reply — fully on the event loop.

    Returns a tri-state (see playbook 11's open|filtered problem):
        bytes         the reply (service is OPEN and speaking)
        _UDP_CLOSED   ICMP port-unreachable (port is CLOSED)
        None          no reply within `timeout` (OPEN|FILTERED, ambiguous)

    Resolution (IPv4/IPv6/hostname) is delegated to asyncio's
    create_datagram_endpoint; an unresolvable/again-unavailable target yields
    None rather than raising, so one bad target never aborts a sweep.
    """
    loop = asyncio.get_running_loop()
    fut: "asyncio.Future" = loop.create_future()
    try:
        transport, _ = await loop.create_datagram_endpoint(
            lambda: _UDPProbeProtocol(fut), remote_addr=(target, port))
    except (OSError, socket.gaierror):
        return None
    try:
        transport.sendto(payload)
        try:
            return await asyncio.wait_for(fut, timeout=timeout)
        except asyncio.TimeoutError:
            return None
    finally:
        transport.close()


async def async_udp_probe_retry(target: str, port: int, payload: bytes,
                                timeout: float, *, max_retries: int = 2):
    """
    `async_udp_probe` with bounded per-port retransmit.

    Returns on the FIRST definitive answer — bytes (open) or `_UDP_CLOSED`
    (closed) — and only retries on silence (`None`). This directly attacks UDP's
    open|filtered ambiguity: a genuine reply lost to UDP's unreliability, or an
    ICMP-unreachable dropped by RFC-1812 rate limiting, gets another chance
    instead of being mislabelled. After `max_retries` extra attempts still-silent
    ports return `None` (open|filtered, reported honestly).
    """
    result = None
    for _ in range(max(0, max_retries) + 1):
        result = await async_udp_probe(target, port, payload, timeout)
        if result is not None:
            return result
    return result


def bracket_host(target: str) -> str:
    """Wrap an IPv6 literal in [] for a URL authority; leave v4/hostnames as-is.
    'http://::1:80/' is invalid — it must be 'http://[::1]:80/'."""
    if ":" in target and not target.startswith("["):
        try:
            ipaddress.ip_address(target)
            return f"[{target}]"
        except ValueError:
            return target
    return target


def parse_ports(spec: str) -> list[int]:
    """Parse '22,80,443,8000-8100' into a sorted unique port list (1-65535)."""
    ports: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            if "-" in part:
                a_str, b_str = part.split("-", 1)
                a, b = int(a_str), int(b_str)
            else:
                a = b = int(part)
        except ValueError:
            raise ValueError(
                f"invalid port token {part!r} in port spec {spec!r}") from None
        if not (0 < a < 65536) or not (0 < b < 65536):
            raise ValueError(
                f"port token {part!r} out of range — ports must be 1-65535")
        if b < a:
            raise ValueError(f"invalid port range {part!r}: end before start")
        ports.update(range(a, b + 1))
    return sorted(ports)


# Commonly-useful default port sets (kept small and explicit on purpose).
TOP_TCP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 389, 443, 445, 465,
    587, 636, 993, 995, 1433, 1521, 2049, 3306, 3389, 5432, 5900, 5985,
    5986, 6379, 8000, 8080, 8443, 8888, 9200, 11211, 11434, 27017,
]


# --------------------------------------------------------------------------- #
# Output writer.
# --------------------------------------------------------------------------- #
class ResultWriter:
    """Writes ScanResult objects as JSONL to a file and/or stdout."""

    def __init__(self, path: str | None = None, also_stdout: bool = True):
        self._fh = None
        if path:
            parent = Path(path).parent
            if str(parent) not in ("", "."):
                parent.mkdir(parents=True, exist_ok=True)
            self._fh = open(path, "w", encoding="utf-8")
        self._stdout = also_stdout
        self.count = 0

    def write(self, result: ScanResult) -> None:
        line = result.to_json()
        if self._fh:
            self._fh.write(line + "\n")
            self._fh.flush()
        if self._stdout:
            print(line, flush=True)
        self.count += 1

    def close(self) -> None:
        if self._fh:
            self._fh.close()


# --------------------------------------------------------------------------- #
# BaseScanner — the contract every scanner module follows.
# --------------------------------------------------------------------------- #
class BaseScanner:
    """
    Subclasses implement `scan_target(self, target)` (async), returning a list
    of ScanResult. The base handles scope enforcement, rate limiting, and
    concurrency so every scanner behaves identically and is measurable.

    `self.sem` bounds the number of concurrent network operations — NOT
    targets. Subclasses must acquire it (`async with self.sem:`) around each
    individual socket operation (one port check, one banner grab, ...), never
    once per target. A single target can legitimately fan out across hundreds
    or thousands of ports; bounding only the target loop would still let
    `--concurrency 100` against a wide port range open tens of thousands of
    sockets at once (e.g. 100 targets x 65535 ports). Sharing one semaphore
    across both the target loop and every scanner's internal port fan-out
    keeps the total in-flight operation count equal to `--concurrency`,
    matching what the flag's help text promises.
    """

    name = "base"

    def __init__(self, scope: ScopeGuard, *, rate: float = 200.0,
                 concurrency: int = 100, timeout: float = 3.0):
        self.scope = scope
        self.limiter = RateLimiter(rate)
        self.timeout = timeout
        self.sem = asyncio.Semaphore(concurrency)
        self._concurrency = concurrency

    async def scan_target(self, target: str) -> list[ScanResult]:
        raise NotImplementedError

    async def _guarded(self, target: str) -> list[ScanResult]:
        try:
            self.scope.assert_in_scope(target)
        except ScopeError as exc:
            return [ScanResult(self.name, target, status="error", error=str(exc))]
        try:
            return await self.scan_target(target)
        except Exception as exc:  # never let one target kill the run
            LOG.debug("scan error %s: %s", target, exc)
            return [ScanResult(self.name, target, status="error",
                               error=f"{type(exc).__name__}: {exc}")]

    async def run(self, targets: Iterable[str], writer: ResultWriter) -> None:
        in_scope = list(self.scope.filter(targets))
        LOG.info("[%s] scanning %d in-scope target(s)", self.name, len(in_scope))
        if not in_scope:
            return

        # Sliding window: keep only `window` targets in flight at once so a huge
        # target list doesn't allocate hundreds of thousands of task objects (plus
        # their per-target port fan-out) simultaneously. self.sem still caps the
        # total number of concurrent sockets; this is a separate, target-level bound.
        window = max(self._concurrency, 64)
        it = iter(in_scope)
        inflight: set[asyncio.Task] = set()

        def _fill() -> None:
            while len(inflight) < window:
                try:
                    t = next(it)
                except StopIteration:
                    return
                inflight.add(asyncio.create_task(self._guarded(t)))

        _fill()
        while inflight:
            done, _ = await asyncio.wait(
                inflight, return_when=asyncio.FIRST_COMPLETED)
            for fut in done:
                inflight.discard(fut)
                for result in fut.result():   # _guarded never raises
                    writer.write(result)
            _fill()


# --------------------------------------------------------------------------- #
# Shared CLI scaffolding so each scanner file gets the same flags.
# --------------------------------------------------------------------------- #
def base_argparser(description: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=description)
    p.add_argument("-t", "--targets", nargs="+", required=True,
                   help="targets: CIDR, IP, hostname, or range a-b")
    p.add_argument("-s", "--scope", required=True,
                   help="path to authorization allowlist file (REQUIRED)")
    p.add_argument("-o", "--output", help="write JSONL results to this file")
    p.add_argument("--rate", type=float, default=200.0,
                   help="max operations per second (default 200)")
    p.add_argument("--concurrency", type=int, default=100,
                   help="max concurrent operations (default 100)")
    p.add_argument("--timeout", type=float, default=3.0,
                   help="per-operation timeout seconds (default 3.0)")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )


def main_entrypoint(fn) -> None:
    """
    Run a scanner CLI's body with consistent, operator-friendly error handling.

    `fn` is a zero-argument callable. It may run synchronously and/or return a
    coroutine (e.g. `fn` can itself be an `async def` function passed by
    reference — calling it just creates the coroutine, which is then driven
    here). This lets every scanner's `main()` funnel both its argument
    validation (scope file, port specs, target expansion) and its async scan
    loop through one place, so none of them leak a raw Python traceback to the
    terminal for routine operator mistakes (bad scope file, bad -p spec,
    missing output directory, Ctrl+C mid-scan).
    """
    try:
        result = fn()
        if asyncio.iscoroutine(result):
            asyncio.run(result)
    except ScopeError as exc:
        LOG.error("scope error: %s", exc)
        sys.exit(1)
    except (OSError, ValueError) as exc:
        LOG.error("%s: %s", type(exc).__name__, exc)
        sys.exit(1)
    except KeyboardInterrupt:
        LOG.warning("interrupted by user — partial results (if any) were flushed")
        sys.exit(130)


async def run_cli(scanner_cls, args) -> None:
    """Wire argparse args into a scanner instance and execute it."""
    scope = ScopeGuard.from_file(args.scope)
    targets = expand_targets(args.targets)
    scanner = scanner_cls(
        scope,
        rate=args.rate,
        concurrency=args.concurrency,
        timeout=args.timeout,
    )
    writer = ResultWriter(args.output, also_stdout=True)
    try:
        await scanner.run(targets, writer)
    finally:
        writer.close()
        LOG.info("[%s] done — %d result(s)", scanner.name, writer.count)
