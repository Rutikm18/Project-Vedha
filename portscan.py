#!/usr/bin/env python3
"""
portscan.py — self-contained TCP connect port scanner (core engine only).

No scope file, no other scripts, no third-party packages — just Python 3.11+
stdlib. You give it a target IP/host; it tells you, for every port, whether it
is remotely reachable FROM THIS MACHINE and WHY.

    OPEN = a TCP connect() from here to target:port completed (SYN/ACK).
That is remote-reachability truth, not "the host has a socket in LISTEN".

States + reasons (a port that is not open still tells you why):
    open         connect_success        3-way handshake completed
    closed       connection_refused     host reachable, sent RST
    filtered     no_response            silence within timeout (retried)
    unreachable  host_unreachable       ICMP / EHOSTUNREACH, ENETUNREACH ...
    error        dns_error / local_resource_error / os_error (scanner-side)

Silence is retried (one dropped packet shouldn't fake "filtered"); a definitive
RST is never retried. IPv4 and IPv6 are scanned independently.

USAGE
    python3 portscan.py 192.168.1.68                 # all 65535 ports
    python3 portscan.py 192.168.1.68 -p 1-1024,3389  # specific ports
    python3 portscan.py example.com -p 22,80,443 --show-closed
    python3 portscan.py 192.168.1.68 -o result.jsonl # also write JSONL

    Tuning:  --timeout 2  --retries 1  --concurrency 800  --rate 1000

AUTHORIZATION: only scan hosts you own or are explicitly permitted to test.
"""

from __future__ import annotations

import argparse
import asyncio
import errno as _errno
import ipaddress
import json
import socket
import sys
import time
from datetime import datetime, timezone

# --------------------------------------------------------------------------- #
# errno -> (state, reason): the OS kernel does the packet-level TCP work and
# hands back an errno; we translate it into exposure truth instead of flattening
# everything to "filtered".
# --------------------------------------------------------------------------- #
_ERRNO_MAP: dict[int, tuple[str, str]] = {
    _errno.ECONNREFUSED:  ("closed",      "connection_refused"),   # RST
    _errno.ECONNRESET:    ("closed",      "connection_reset"),
    _errno.ETIMEDOUT:     ("filtered",    "no_response"),          # kernel timeout
    _errno.ECONNABORTED:  ("filtered",    "connection_aborted"),
    _errno.EHOSTUNREACH:  ("unreachable", "host_unreachable"),
    _errno.ENETUNREACH:   ("unreachable", "network_unreachable"),
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
_CONFIDENCE = {"open": "high", "closed": "high",
               "filtered": "medium", "unreachable": "medium", "error": "low"}


def classify_os_error(exc: OSError) -> tuple[str, str]:
    """Map a connect()-time OSError to (state, reason). Unknown stays visible
    as ('error', 'os_error') — an unknown local failure is NOT proof of a
    target firewall."""
    if isinstance(exc, socket.gaierror):
        return "error", "dns_error"
    mapped = _ERRNO_MAP.get(exc.errno)
    return mapped if mapped is not None else ("error", "os_error")


def family_of(ip: str | None) -> str | None:
    if not ip:
        return None
    try:
        return "ipv6" if ipaddress.ip_address(ip).version == 6 else "ipv4"
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Simple global rate limiter — at most `rate` connect attempts per second.
# --------------------------------------------------------------------------- #
class RateLimiter:
    def __init__(self, rate: float):
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


class PortScanner:
    def __init__(self, target: str, ports: list[int], *, timeout: float = 2.0,
                 retries: int = 1, concurrency: int = 500, rate: float = 1000.0,
                 vantage: str | None = None):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.retries = max(0, retries)
        self.sem = asyncio.Semaphore(concurrency)
        self.limiter = RateLimiter(rate)
        self.vantage = vantage or socket.gethostname()

    def _record(self, port, state, reason, evidence, *, rtt_ms=None, error=None,
                errno_val=None, src_ip=None, family=None, attempts=1) -> dict:
        data = {"reason": reason, "method": "connect", "vantage": self.vantage,
                "confidence": _CONFIDENCE.get(state, "low")}
        if family:
            data["family"] = family
        if rtt_ms is not None:
            data["rtt_ms"] = rtt_ms
        if errno_val is not None:
            data["errno"] = errno_val
        if src_ip:
            data["src_ip"] = src_ip
        if attempts > 1:
            data["attempts"] = attempts
        return {
            "scanner": "portscan", "target": self.target,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "port": port, "proto": "tcp", "status": state,
            "data": data, "evidence": evidence, "error": error,
        }

    async def _attempt(self, port: int) -> dict:
        t0 = time.monotonic()
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.target, port), timeout=self.timeout)
            rtt = round((time.monotonic() - t0) * 1000, 2)
            src_ip = peer_ip = None
            try:
                sn = writer.get_extra_info("sockname")
                pn = writer.get_extra_info("peername")
                src_ip = sn[0] if sn else None
                peer_ip = pn[0] if pn else None
            except Exception:
                pass
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            return self._record(port, "open", "connect_success",
                                 "tcp connect completed (3-way handshake)",
                                 rtt_ms=rtt, src_ip=src_ip,
                                 family=family_of(peer_ip) or family_of(self.target))
        except asyncio.TimeoutError:
            rtt = round((time.monotonic() - t0) * 1000, 2)
            return self._record(port, "filtered", "no_response",
                                 f"no response within {self.timeout:g}s",
                                 rtt_ms=rtt, family=family_of(self.target))
        except OSError as exc:
            rtt = round((time.monotonic() - t0) * 1000, 2)
            state, reason = classify_os_error(exc)
            return self._record(port, state, reason, None, rtt_ms=rtt,
                                 error=str(exc), errno_val=getattr(exc, "errno", None),
                                 family=family_of(self.target))

    async def scan_port(self, port: int) -> dict:
        async with self.sem:
            await self.limiter.wait()
            result = await self._attempt(port)
            attempt = 1
            # retransmit ONLY on silence — one lost packet can fake it.
            while (attempt <= self.retries and result["status"] == "filtered"
                   and result["data"].get("reason") == "no_response"):
                attempt += 1
                await self.limiter.wait()
                result = await self._attempt(port)
            if attempt > 1:
                result["data"]["attempts"] = attempt
            return result

    async def run(self):
        return await asyncio.gather(*(self.scan_port(p) for p in self.ports))


def parse_ports(spec: str) -> list[int]:
    ports: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a, b = int(a), int(b)
        else:
            a = b = int(part)
        if not (0 < a < 65536 and 0 < b < 65536) or b < a:
            raise ValueError(f"bad port token {part!r}")
        ports.update(range(a, b + 1))
    return sorted(ports)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Self-contained TCP connect port scanner (core engine).")
    ap.add_argument("target", help="IP or hostname to scan")
    ap.add_argument("-p", "--ports", default=None,
                    help="e.g. '22,80,443,8000-8100' (default: ALL 1-65535)")
    ap.add_argument("--timeout", type=float, default=2.0,
                    help="per-port seconds before calling it filtered (default 2)")
    ap.add_argument("--retries", type=int, default=1,
                    help="extra attempts on silence only (default 1; RST never retried)")
    ap.add_argument("--concurrency", type=int, default=500,
                    help="max concurrent sockets (default 500; keep < ulimit -n)")
    ap.add_argument("--rate", type=float, default=1000.0,
                    help="max connect attempts/sec (default 1000)")
    ap.add_argument("--vantage", default=None, help="label for this scan point")
    ap.add_argument("--show-closed", action="store_true",
                    help="also print non-open ports with their reason")
    ap.add_argument("-o", "--output", help="write full JSONL to this file")
    args = ap.parse_args()

    ports = parse_ports(args.ports) if args.ports else list(range(1, 65536))

    scanner = PortScanner(args.target, ports, timeout=args.timeout,
                          retries=args.retries, concurrency=args.concurrency,
                          rate=args.rate, vantage=args.vantage)

    print(f"scanning {args.target}: {len(ports)} port(s), timeout={args.timeout}s, "
          f"retries={args.retries}, concurrency={args.concurrency}, "
          f"rate={args.rate:g}/s  (vantage: {scanner.vantage})", file=sys.stderr)
    t0 = time.monotonic()
    try:
        results = asyncio.run(scanner.run())
    except KeyboardInterrupt:
        print("\ninterrupted", file=sys.stderr)
        sys.exit(130)
    elapsed = time.monotonic() - t0

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            for r in results:
                fh.write(json.dumps(r, default=str) + "\n")

    open_ports = sorted((r for r in results if r["status"] == "open"),
                        key=lambda r: r["port"])
    print(f"\nPORT      STATE   FAMILY  RTT      REASON")
    for r in open_ports:
        d = r["data"]
        print(f"{r['port']:<9} {'open':<7} {d.get('family',''):<7} "
              f"{str(d.get('rtt_ms',''))+'ms':<8} {d.get('reason')}")
    if args.show_closed:
        for r in results:
            if r["status"] != "open":
                d = r["data"]
                print(f"{r['port']:<9} {r['status']:<7} {d.get('family',''):<7} "
                      f"{str(d.get('rtt_ms',''))+'ms':<8} {d.get('reason')}")

    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"\n{len(open_ports)} open of {len(ports)} scanned in {elapsed:.1f}s  "
          f"[{summary}]", file=sys.stderr)


if __name__ == "__main__":
    main()
