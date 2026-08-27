"""
dns_scanner.py — DNS server hygiene: zone transfer (AXFR), DNSSEC presence, and
version/hostname disclosure (VA checklist: DNS misconfiguration & info exposure).

METHOD (collection, read-only): against a host with DNS/53 open, ask three
questions a client legitimately can:
  * version.bind / hostname.bind — a CHAOS-class TXT query (RFC-era BIND
    convention) that many servers answer with their software version / hostname.
  * AXFR — request a full zone transfer over TCP/53. A public server SHOULD refuse
    this; if it succeeds it hands over the entire zone (every host, its addresses,
    internal naming) — a high-value misconfiguration.
  * DNSSEC presence — a shallow "is the zone signed?" check (DNSKEY present). Full
    chain-of-trust validation is deliberately out of scope (a project of its own);
    we only report presence/absence.

Open-recursion / open-resolver is intentionally NOT handled here — udp_scanner.py
already collects that (feeds the UDP-DNS-OPEN-RESOLVER finding); this module covers
the non-overlapping AXFR / DNSSEC / version surface.

ZONE DISCOVERY: AXFR and DNSSEC need a zone NAME, not just an IP. Zones come from
(in order) an explicit --zones list, a reverse-DNS (PTR) self-lookup against the
target, and heuristic derivation from a hostname target — all bounded.

SAFETY: dnspython is pure-Python (sealed-build friendly), imported lazily. Blocking
queries run in a worker thread. Everything is bounded — per-zone cap, a hard cap on
records read from a zone transfer (never a full dump of a huge zone), a small
evidence sample, and strict timeouts.
"""

from __future__ import annotations

import asyncio
import ipaddress
from typing import Iterable

from .scanner_base import (
    BaseScanner, ScanResult, ScopeGuard, ResultWriter, expand_targets,
    parse_ports, setup_logging, base_argparser, main_entrypoint,
)

DEFAULT_DNS_PORTS = [53]
MAX_ZONES = 8            # candidate zones to probe per host
MAX_AXFR_RECORDS = 5000  # stop reading a zone transfer here — never a full dump
MAX_SAMPLE = 40          # zone records kept as evidence


def _is_ip(s: str) -> bool:
    try:
        ipaddress.ip_address(str(s).strip())
        return True
    except ValueError:
        return False


def derive_zones(target: str, extra: Iterable[str] = ()) -> list[str]:
    """Candidate zone names to try AXFR / DNSSEC against, most-confident first.

    Explicit `extra` zones (from --zones or a PTR self-lookup) are used as-is and
    also reduced to their registrable/parent form; a hostname target is reduced
    the same way. Pure and bounded to MAX_ZONES.
    """
    out: list[str] = []
    seen: set[str] = set()

    def _push(z: str) -> None:
        z = (z or "").strip().rstrip(".").lower()
        if z and "." in z and not _is_ip(z) and z not in seen:
            seen.add(z)
            out.append(z)

    def _derive(host: str) -> None:
        host = (host or "").strip().rstrip(".")
        if not host or _is_ip(host):
            return
        labels = host.split(".")
        if len(labels) >= 2:
            _push(".".join(labels[-2:]))   # registrable-ish (example.com)
        if len(labels) >= 3:
            _push(".".join(labels[1:]))    # immediate parent (corp.example.com)

    for e in extra:
        _push(e)
        _derive(e)
    _derive(target)
    return out[:MAX_ZONES]


class DNSScanner(BaseScanner):
    name = "dns_scan"

    def __init__(self, *args, ports: list[int] | None = None,
                 zones: list[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = ports or DEFAULT_DNS_PORTS
        self.zones = list(zones or [])

    # ── individual dnspython probes (blocking) ────────────────────────────────
    def _chaos_txt(self, target: str, port: int, qname: str) -> str | None:
        import dns.message
        import dns.query
        import dns.rdataclass
        import dns.rdatatype
        try:
            q = dns.message.make_query(qname, dns.rdatatype.TXT, dns.rdataclass.CH)
            try:
                r = dns.query.udp(q, target, timeout=self.timeout, port=port)
            except Exception:
                r = dns.query.tcp(q, target, timeout=self.timeout, port=port)
            for rrset in r.answer:
                for item in rrset:
                    txt = getattr(item, "strings", None)
                    if txt:
                        return b" ".join(txt).decode("utf-8", "replace")
                    return item.to_text().strip('"')
        except Exception:
            return None
        return None

    def _ptr_self(self, target: str, port: int) -> str | None:
        """Ask the target (as a resolver) for the PTR of its own IP — a common way
        to learn a hostname from which to derive a forward zone."""
        if not _is_ip(target):
            return None
        import dns.message
        import dns.query
        import dns.rdatatype
        import dns.reversename
        try:
            rev = dns.reversename.from_address(target)
            q = dns.message.make_query(rev, dns.rdatatype.PTR)
            r = dns.query.udp(q, target, timeout=self.timeout, port=port)
            for rrset in r.answer:
                for item in rrset:
                    return item.to_text().rstrip(".")
        except Exception:
            return None
        return None

    def _axfr(self, target: str, port: int, zone: str) -> dict:
        """Attempt a zone transfer, reading incrementally and stopping at
        MAX_AXFR_RECORDS so a huge or hostile zone can't exhaust memory."""
        import dns.query
        records = 0
        sample: list[str] = []
        try:
            xfr = dns.query.xfr(target, zone, timeout=self.timeout,
                                lifetime=self.timeout * 3, port=port)
            for msg in xfr:
                for rrset in msg.answer:
                    records += len(rrset)
                    if len(sample) < MAX_SAMPLE:
                        sample.append(rrset.to_text()[:200])
                if records >= MAX_AXFR_RECORDS:
                    return {"transferred": True, "record_count": records,
                            "sample": sample, "capped": True}
        except Exception as exc:
            return {"transferred": False, "reason": type(exc).__name__}
        return {"transferred": records > 0, "record_count": records,
                "sample": sample, "capped": False}

    def _dnssec_present(self, target: str, port: int, zone: str) -> bool | None:
        import dns.flags
        import dns.message
        import dns.query
        import dns.rdatatype
        try:
            q = dns.message.make_query(zone, dns.rdatatype.DNSKEY, want_dnssec=True)
            try:
                r = dns.query.udp(q, target, timeout=self.timeout, port=port)
                if r.flags & dns.flags.TC:
                    r = dns.query.tcp(q, target, timeout=self.timeout, port=port)
            except Exception:
                r = dns.query.tcp(q, target, timeout=self.timeout, port=port)
            return any(rr.rdtype == dns.rdatatype.DNSKEY for rr in r.answer)
        except Exception:
            return None

    def _probe(self, target: str, port: int) -> dict:
        """Blocking orchestration of the DNS checks. Monkeypatchable for tests."""
        try:
            import dns.query  # noqa: F401  (probe the dependency lazily)
        except ImportError:
            return {"dns": None, "error": "dnspython_not_installed"}

        version_bind = self._chaos_txt(target, port, "version.bind")
        hostname_bind = self._chaos_txt(target, port, "hostname.bind")

        ptr = self._ptr_self(target, port)
        zones = derive_zones(target, extra=self.zones + ([ptr] if ptr else []))

        axfr: dict[str, dict] = {}
        dnssec: dict[str, bool | None] = {}
        transferred_any = False
        for zone in zones:
            res = self._axfr(target, port, zone)
            axfr[zone] = res
            if res.get("transferred"):
                transferred_any = True
            dnssec[zone] = self._dnssec_present(target, port, zone)

        answered = (version_bind is not None or hostname_bind is not None
                    or ptr is not None or transferred_any
                    or any(v is not None for v in dnssec.values()))
        return {
            "dns": True if answered else None,
            "version_bind": version_bind,
            "hostname_bind": hostname_bind,
            "ptr_self": ptr,
            "zones_tested": zones,
            "axfr": axfr,
            "zone_transfer": transferred_any,
            "dnssec": dnssec,
        }

    async def _scan_port(self, target: str, port: int) -> ScanResult:
        await self.limiter.wait()
        loop = asyncio.get_running_loop()
        async with self.sem:
            try:
                data = await loop.run_in_executor(None, self._probe, target, port)
            except Exception as exc:
                return ScanResult(self.name, target, port=port, proto="udp",
                                  status="error", error=str(exc))
        if data.get("error") == "dnspython_not_installed":
            return ScanResult(self.name, target, port=port, proto="udp",
                              status="error", error="dnspython not installed")
        if not data.get("dns"):
            return ScanResult(self.name, target, port=port, proto="udp",
                              status="filtered", reason="no_dns", data=data)
        xfer = [z for z, r in (data.get("axfr") or {}).items() if r.get("transferred")]
        evidence = (f"version.bind={data.get('version_bind')!r} "
                    f"zone_transfer={bool(xfer)}"
                    + (f" ({', '.join(xfer)})" if xfer else ""))
        return ScanResult(self.name, target, port=port, proto="udp",
                          status="open", data=data, evidence=evidence)

    async def scan_target(self, target: str) -> list[ScanResult]:
        tasks = [self._scan_port(target, p) for p in self.ports]
        return list(await asyncio.gather(*tasks))


def main() -> None:
    parser = base_argparser("DNS AXFR / DNSSEC / version.bind audit")
    parser.add_argument("-p", "--ports", default=None, help="DNS ports (default: 53)")
    parser.add_argument("--zones", default=None,
                        help="comma-separated zone names to test AXFR/DNSSEC against")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        ports = parse_ports(args.ports) if args.ports else DEFAULT_DNS_PORTS
        zones = [z.strip() for z in args.zones.split(",")] if args.zones else []
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        scanner = DNSScanner(scope, rate=args.rate, concurrency=args.concurrency,
                             timeout=args.timeout, ports=ports, zones=zones)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await scanner.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
