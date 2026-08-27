"""
scan_funnel.py — per-host scan orchestrator (the assessment pipeline, Playbook 02).

WHY THIS EXISTS:
  Every scanner in this package is independent and, run on its own, re-derives
  liveness and re-probes ports the others already found. On a real engagement you
  want ONE coherent pass per host that funnels wide→narrow:

      all targets → live hosts → open ports → the RIGHT deep scanner per port

  so the TLS scanner only touches ports the port scan proved open, the DB scanner
  only fires when a DB port is actually listening, and a dead host is never
  port-scanned at all. This is the classic funnel: cheap broad stages gate the
  expensive narrow ones, cutting packets, time, and target-side noise.

DESIGN (dependency-injected for testability):
  The funnel owns no scanning logic — it composes existing scanners through three
  seams:
    * discovery              — a scanner-like object with async scan_target()
    * port_scanner_factory   — factory(candidate_ports) -> port scanner
    * deep_scanner_factories — {route_name: factory(open_ports) -> scanner}
  Every deep scanner is constructed scoped to exactly the open ports routed to it,
  so it cannot re-scan the whole host. Injecting factories lets tests verify the
  routing/gating with fakes and no network.

COLLECTION ONLY: the funnel enforces scope, then delegates to scanners that are
themselves collection-only. It performs no exploitation and adds no new probes.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Callable, Protocol

from .scanner_base import (
    ScanResult, ScopeGuard, ResultWriter, expand_targets,
    setup_logging, base_argparser, main_entrypoint, LOG,
)


# ── port → deep-scanner routing table ─────────────────────────────────────────
# A port may appear in more than one route (e.g. 443 → both TLS and web); each
# matched route's scanner is dispatched with the subset of open ports it handles.
DEFAULT_PORT_ROUTES: dict[str, list[int]] = {
    "tls": [443, 8443, 993, 995, 465, 636, 990, 5986],
    "db":  [3306, 33060, 5432, 1433, 6379, 27017, 1521],
    "smb": [445],
    "web": [80, 8080, 8000, 8443, 443, 8888],
    "ai":  [11434, 9200, 6333, 8000, 8888],
    "ssh": [22, 2222],
    "smb_enum": [445],
    "ldap": [389, 636, 3268, 3269],
    "dns": [53],
    "nfs": [111, 2049],
    "ftp": [21],
    "rsync": [873],
    "vnc": [5900, 5901],
    "smtp": [25, 587],
    "msrpc": [135],
    "printer": [9100, 631],
}


def route_ports(open_ports: list[int],
                routes: dict[str, list[int]] | None = None) -> dict[str, list[int]]:
    """
    Map a host's open ports onto the deep-scanner routes that handle them.
    Returns {route_name: [matched open ports, sorted]} for routes with ≥1 match.
    """
    routes = routes or DEFAULT_PORT_ROUTES
    open_set = set(open_ports)
    out: dict[str, list[int]] = {}
    for name, route_ports_list in routes.items():
        matched = sorted(open_set & set(route_ports_list))
        if matched:
            out[name] = matched
    return out


# ── funnel result ─────────────────────────────────────────────────────────────
@dataclass
class FunnelResult:
    """The full outcome of funnelling one host."""
    target: str
    alive: bool
    open_tcp_ports: list[int]
    results: list[ScanResult]
    stages_run: list[str] = field(default_factory=list)


# ── scan-stage contract ───────────────────────────────────────────────────────
class _Scanner(Protocol):
    async def scan_target(self, target: str) -> list[ScanResult]: ...


def _candidate_ports(routes: dict[str, list[int]]) -> list[int]:
    """The port set worth scanning = union of every route's ports (deduped)."""
    ports: set[int] = set()
    for rp in routes.values():
        ports.update(rp)
    return sorted(ports)


def _is_alive(discovery_results: list[ScanResult]) -> bool:
    return any((r.data or {}).get("alive") for r in discovery_results)


class ScanFunnel:
    """
    Orchestrates discovery → port scan → routed deep scanners for each host.

    Parameters
    ----------
    scope                  authorization allowlist (checked before any stage)
    discovery              liveness scanner (async scan_target)
    port_scanner_factory   callable(candidate_ports) -> port scanner
    deep_scanner_factories {route: callable(open_ports) -> deep scanner}
    udp_scanner            optional pre-built UDP scanner run after the port scan
    routes                 port→route table (defaults to DEFAULT_PORT_ROUTES)
    force                  if True, port-scan even hosts discovery marks dead
    """
    name = "scan_funnel"

    def __init__(self, scope: ScopeGuard, *,
                 discovery: _Scanner,
                 port_scanner_factory: Callable[[list[int]], _Scanner],
                 deep_scanner_factories: dict[str, Callable[[list[int]], _Scanner]],
                 udp_scanner: _Scanner | None = None,
                 routes: dict[str, list[int]] | None = None,
                 force: bool = False,
                 concurrency: int = 64):
        self.scope = scope
        self.discovery = discovery
        self.port_scanner_factory = port_scanner_factory
        self.deep_scanner_factories = deep_scanner_factories
        self.udp_scanner = udp_scanner
        self.routes = routes or DEFAULT_PORT_ROUTES
        self.force = force
        self._concurrency = concurrency

    async def run_host(self, target: str) -> FunnelResult:
        results: list[ScanResult] = []
        stages: list[str] = []

        # Stage 0 — scope gate.
        if not self.scope.in_scope(target):
            return FunnelResult(
                target, False, [],
                [ScanResult(self.name, target, status="error",
                            error=f"target {target!r} is NOT in authorized scope")],
                stages)

        # Stage 1 — discovery.
        disc = await self.discovery.scan_target(target)
        results.extend(disc)
        stages.append("discovery")
        alive = _is_alive(disc)

        if not alive and not self.force:
            return FunnelResult(target, False, [], results, stages)

        # Stage 2 — port scan (only the ports we can actually act on).
        port_scanner = self.port_scanner_factory(_candidate_ports(self.routes))
        port_results = await port_scanner.scan_target(target)
        results.extend(port_results)
        stages.append("port_scan")
        open_ports = sorted({
            r.port for r in port_results
            if r.status == "open" and r.proto == "tcp" and r.port is not None
        })

        # Stage 2b — optional UDP sweep (its own port set; independent of TCP).
        if self.udp_scanner is not None:
            udp_results = await self.udp_scanner.scan_target(target)
            results.extend(udp_results)
            stages.append("udp_scan")

        # Stage 3 — routed deep scanners, each scoped to its open ports only.
        for route_name, ports in route_ports(open_ports, self.routes).items():
            factory = self.deep_scanner_factories.get(route_name)
            if factory is None:
                continue
            scanner = factory(ports)
            deep = await scanner.scan_target(target)
            results.extend(deep)
            stages.append(route_name)

        return FunnelResult(target, alive, open_ports, results, stages)

    async def run(self, targets, writer) -> None:
        """Funnel many hosts with bounded concurrency, writing every result."""
        in_scope = [t for t in targets if self.scope.in_scope(t)]
        LOG.info("[%s] funnelling %d in-scope host(s)", self.name, len(in_scope))
        sem = asyncio.Semaphore(self._concurrency)

        async def _one(t: str) -> FunnelResult:
            async with sem:
                try:
                    return await self.run_host(t)
                except Exception as exc:   # one host never aborts the sweep
                    LOG.debug("funnel error %s: %s", t, exc)
                    return FunnelResult(
                        t, False, [],
                        [ScanResult(self.name, t, status="error",
                                    error=f"{type(exc).__name__}: {exc}")], [])

        for fut in asyncio.as_completed([_one(t) for t in in_scope]):
            fr = await fut
            for r in fr.results:
                writer.write(r)


# ── default wiring: compose the real scanners ─────────────────────────────────
def build_default_funnel(scope: ScopeGuard, *, rate: float = 200.0,
                         concurrency: int = 100, timeout: float = 3.0,
                         force: bool = False,
                         with_udp: bool = False) -> ScanFunnel:
    """
    Wire the funnel with the package's real scanners. Imported lazily so the
    funnel's core logic (and its tests) don't depend on every scanner module.
    """
    from .host_discovery import HostDiscoveryScanner
    from .syn_scanner import SynScanner
    from .tls_scanner import TLSScanner
    from .db_scanner import DBScanner
    from .smb_scanner import SMBScanner
    from .web_scanner import WebScanner
    from .mcp_ai_scanner import MCPAIScanner
    from .udp_scanner import UDPScanner
    from .ssh_scanner import SSHScanner
    from .smb_enum_scanner import SMBEnumScanner
    from .ldap_scanner import LDAPScanner
    from .dns_scanner import DNSScanner
    from .nfs_scanner import NFSScanner
    from .ftp_scanner import FTPScanner
    from .rsync_scanner import RsyncScanner
    from .vnc_scanner import VNCScanner
    from .smtp_scanner import SMTPScanner
    from .msrpc_scanner import MSRPCScanner
    from .printer_scanner import PrinterScanner

    common = dict(rate=rate, concurrency=concurrency, timeout=timeout)

    discovery = HostDiscoveryScanner(scope, **common)

    def port_factory(ports):
        # SYN scan on privileged Linux; auto connect-scan fallback everywhere else.
        return SynScanner(scope, ports=ports, **common)

    def tls_factory(ports):
        return TLSScanner(scope, ports=ports, **common)

    def db_factory(ports):
        return DBScanner(scope, port_map={p: "" for p in ports},
                         try_all_on_port=True, **common)

    def smb_factory(ports):
        return SMBScanner(scope, **common)

    def web_factory(ports):
        return WebScanner(scope, ports=ports, **common)

    def ai_factory(ports):
        return MCPAIScanner(scope, ports=ports, **common)

    def ssh_factory(ports):
        return SSHScanner(scope, ports=ports, **common)

    def smb_enum_factory(ports):
        return SMBEnumScanner(scope, ports=ports, **common)

    def ldap_factory(ports):
        return LDAPScanner(scope, ports=ports, **common)

    def dns_factory(ports):
        return DNSScanner(scope, ports=ports, **common)

    def nfs_factory(ports):
        return NFSScanner(scope, ports=ports, **common)

    def ftp_factory(ports):
        return FTPScanner(scope, ports=ports, **common)

    def rsync_factory(ports):
        return RsyncScanner(scope, ports=ports, **common)

    def vnc_factory(ports):
        return VNCScanner(scope, ports=ports, **common)

    def smtp_factory(ports):
        return SMTPScanner(scope, ports=ports, **common)

    def msrpc_factory(ports):
        return MSRPCScanner(scope, ports=ports, **common)

    def printer_factory(ports):
        return PrinterScanner(scope, ports=ports, **common)

    return ScanFunnel(
        scope,
        discovery=discovery,
        port_scanner_factory=port_factory,
        deep_scanner_factories={
            "tls": tls_factory,
            "db": db_factory,
            "smb": smb_factory,
            "web": web_factory,
            "ai": ai_factory,
            "ssh": ssh_factory,
            "smb_enum": smb_enum_factory,
            "ldap": ldap_factory,
            "dns": dns_factory,
            "nfs": nfs_factory,
            "ftp": ftp_factory,
            "rsync": rsync_factory,
            "vnc": vnc_factory,
            "smtp": smtp_factory,
            "msrpc": msrpc_factory,
            "printer": printer_factory,
        },
        udp_scanner=UDPScanner(scope, **common) if with_udp else None,
        force=force,
    )


def main() -> None:
    parser = base_argparser(
        "Per-host scan funnel: discovery → ports → routed deep scanners")
    parser.add_argument("--force", action="store_true",
                        help="port-scan even hosts discovery marks as down")
    parser.add_argument("--with-udp", action="store_true",
                        help="also run the UDP service sweep per host")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        funnel = build_default_funnel(
            scope, rate=args.rate, concurrency=args.concurrency,
            timeout=args.timeout, force=args.force, with_udp=args.with_udp)
        writer = ResultWriter(args.output, also_stdout=True)
        try:
            await funnel.run(targets, writer)
        finally:
            writer.close()

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
