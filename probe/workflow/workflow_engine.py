"""
workflow_engine.py — the async DAG executor. Loops through gates, checks
preconditions (gates.py), invokes the REAL scanner_module classes with
their real constructor signatures, merges results into Asset (asset.py)
and the cache (cache.py), and consults router.py for dynamic Gate-5
branch routing.

Every scanner is invoked via its real `scan_target(host) -> list[ScanResult]`
method directly (not its `.run(targets, writer)` fan-out helper) so this
engine can make per-host gating decisions between stages — `.run()`'s
internal asyncio.create_task fan-out has no hook for that. This means the
workflow engine, not BaseScanner, owns concurrency-across-hosts; each gate
below still scans its target list with bounded concurrency via
asyncio.gather over scan_target calls.

This module imports scanner_module's existing scanner/* classes as-is —
nothing in scanner/ is modified.
"""
from __future__ import annotations

import asyncio
from datetime import timedelta

from scanner.scanner_base import ScanResult, ScopeGuard
from scanner.host_discovery import HostDiscoveryScanner
from scanner.port_scanner import PortScanner
from scanner.syn_scanner import SynScanner
from scanner.service_banner import ServiceBannerScanner
from scanner.tls_scanner import TLSScanner
from scanner.web_scanner import WebScanner
from scanner.smb_scanner import SMBScanner
from scanner.snmp_scanner import SNMPScanner
from scanner.db_scanner import DBScanner, DEFAULT_DB_PORTS
from scanner.mcp_ai_scanner import MCPAIScanner
from scanner.udp_scanner import UDPScanner
from scanner.ssh_scanner import SSHScanner
from scanner.smb_enum_scanner import SMBEnumScanner
from scanner.ldap_scanner import LDAPScanner
from scanner.dns_scanner import DNSScanner
from scanner.nfs_scanner import NFSScanner
from scanner.ftp_scanner import FTPScanner
from scanner.rsync_scanner import RsyncScanner
from scanner.vnc_scanner import VNCScanner
from scanner.ipmi_scanner import IPMIScanner
from scanner.smtp_scanner import SMTPScanner
from scanner.msrpc_scanner import MSRPCScanner
from scanner.rdp_scanner import RDPScanner
from scanner.printer_scanner import PrinterScanner
from scanner.passive_collector import PassiveCollector
from scanner.ssh_collector import SSHCollector
from scanner.windows_collector import WindowsCollector

from .asset import Asset
from .cache import WorkflowCache
from .gates import (
    PROFILE_PORTS, PROFILE_DEEP_BRANCHES,
    TLS_PORTS, WEB_PORTS, SMB_PORTS, DB_PORTS, AI_PORTS, UDP_PORTS, SNMP_PORTS, SSH_PORTS, LDAP_PORTS, SMB_ENUM_PORTS, DNS_PORTS, NFS_PORTS, FTP_PORTS, RSYNC_PORTS, VNC_PORTS, IPMI_PORTS, SMTP_PORTS, MSRPC_PORTS, RDP_PORTS, PRINTER_PORTS,
    gate_0_is_passive_profile, gate_2_host_discovery, gate_3_port_scan,
    gate_4_service_banner, gate_5_branch_eligible, gate_6_credentialed_collection,
)
from .execution import ExecutionTrace, scanner_failure_result
from .modes import (
    STAGE_DEEP_SCAN,
    STAGE_PORT_SCAN,
    STAGE_SERVICE_BANNER,
    includes_stage,
    resolve_stage_ceiling,
)
from .router import route_branches


async def _scan_one(scanner, host: str) -> list[ScanResult]:
    """Run one component without allowing a target-specific bug to abort peers."""
    try:
        results = await scanner.scan_target(host)
        if results is None:
            raise TypeError("scan_target returned None instead of a result list")
        return list(results)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        return [scanner_failure_result(scanner.name, host, exc)]


async def _gather_per_host(
    scanner,
    hosts: list[str],
    *,
    max_in_flight: int = 100,
) -> list[ScanResult]:
    """Run per-host probes with bounded fan-out and failure isolation."""
    if not hosts:
        return []
    results: list[ScanResult] = []
    batch_size = max(1, int(max_in_flight))
    for offset in range(0, len(hosts), batch_size):
        batches = await asyncio.gather(*(
            _scan_one(scanner, host)
            for host in hosts[offset:offset + batch_size]
        ))
        results.extend(result for batch in batches for result in batch)
    return results


def _split_cached(cache: WorkflowCache, host: str, candidate_ports: list[int],
                  scanner_name: str, force_recheck_after: timedelta | None = None
                  ) -> tuple[list[int], list[ScanResult]]:
    """Splits candidate_ports into (ports that actually need a fresh probe,
    ScanResults that can be reused from cache) — the mechanism that makes
    deterministic facts collected once per engagement, not once per gate
    pass. force_recheck_after lets re-scan mode override even deterministic
    entries once they're old enough (see cache.py's should_recheck).
    """
    to_scan, reused = [], []
    for port in candidate_ports:
        if cache.should_recheck(host, port, scanner_name, force_recheck_after=force_recheck_after):
            to_scan.append(port)
        else:
            reused.append(cache.get(host, port, scanner_name).result)
    return to_scan, reused


def _port_candidates(profile: str, service_filter: set[str] | None,
                     *, port_override: list[int] | None = None) -> list[int]:
    """Return TCP ports worth scanning for this profile and requested branch set.

    Unfiltered assessments use the profile catalog plus every allowed branch
    catalog. A service-specific run uses only its requested TCP branch
    catalogs. UDP-only SNMP/UDP jobs therefore do not accidentally fall back
    to a broad TCP scan.

    `port_override` (from the intensity knob / a full-port audit) REPLACES the
    profile's own catalog as the base TCP set for unfiltered scans — it never
    touches the branch port tables, so a service-specific job's coverage stays
    defined by its branch(es), only its rate/timeout change with intensity.
    """
    allowed = PROFILE_DEEP_BRANCHES.get(profile, set())
    requested = allowed if service_filter is None else (service_filter & allowed)
    if service_filter is None:
        base = port_override if port_override is not None else PROFILE_PORTS.get(profile, [])
        ports = set(base)
    else:
        ports = set()
    if "tls" in requested:
        ports.update(TLS_PORTS)
    if "web" in requested:
        ports.update(WEB_PORTS)
    if "smb" in requested:
        ports.update(SMB_PORTS)
    if "db" in requested:
        ports.update(DB_PORTS)
    if "mcp_ai" in requested:
        ports.update(AI_PORTS)
    if "ssh" in requested:
        ports.update(SSH_PORTS)
    if "ldap" in requested:
        ports.update(LDAP_PORTS)
    if "smb_enum" in requested:
        ports.update(SMB_ENUM_PORTS)
    if "dns" in requested:
        ports.update(DNS_PORTS)
    if "nfs" in requested:
        ports.update(NFS_PORTS)
    if "ftp" in requested:
        ports.update(FTP_PORTS)
    if "rsync" in requested:
        ports.update(RSYNC_PORTS)
    if "vnc" in requested:
        ports.update(VNC_PORTS)
    if "smtp" in requested:
        ports.update(SMTP_PORTS)
    if "msrpc" in requested:
        ports.update(MSRPC_PORTS)
    if "rdp" in requested:
        ports.update(RDP_PORTS)
    if "printer" in requested:
        ports.update(PRINTER_PORTS)
    return sorted(ports)


class _Sink:
    """In-memory ResultWriter stand-in — PassiveCollector/SSHCollector/
    WindowsCollector are NOT BaseScanner subclasses (confirmed by reading
    each directly): they only expose .run(writer) / .run(targets, writer),
    never .scan_target(), so they can't be driven the same way the
    BaseScanner-derived scanners above are. This sink lets the engine
    capture their output the same way without writing to disk.
    """
    def __init__(self):
        self.results: list[ScanResult] = []
    def write(self, r: ScanResult):
        self.results.append(r)
    def close(self):
        pass


async def _run_passive(
    scope: ScopeGuard,
    listen_seconds: float,
) -> tuple[list[ScanResult], dict | None]:
    try:
        collector = PassiveCollector(scope, listen_seconds=listen_seconds)
        sink = _Sink()
        coverage = await collector.run(sink)
        return sink.results, coverage
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        return [
            scanner_failure_result("passive_collect", "<passive-listener>", exc)
        ], None


async def _run_inventory(component_id: str, host: str, collector_factory) -> list[ScanResult]:
    try:
        collector = collector_factory()
        sink = _Sink()
        await collector.run([host], sink)
        return sink.results
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        return [scanner_failure_result(component_id, host, exc)]


def _store_results(
    results: list[ScanResult],
    *,
    assets: dict[str, Asset],
    cache: WorkflowCache,
    profile: str,
) -> None:
    for result in results:
        assets.setdefault(
            result.target,
            Asset(host=result.target, profile=profile),
        ).merge_result(result)
        cache.put(result)


def _record(
    trace: ExecutionTrace | None,
    component_id: str,
    *,
    target_count: int,
    results: list[ScanResult],
    coverage: dict | None = None,
) -> None:
    if trace is not None:
        trace.record(
            component_id,
            target_count=target_count,
            results=results,
            coverage=coverage,
        )


def _record_reused(
    trace: ExecutionTrace | None,
    component_id: str,
    results: list[ScanResult],
) -> None:
    if trace is not None and results:
        trace.reused(component_id, results)


def _finalize_trace(trace: ExecutionTrace | None) -> None:
    if trace is not None:
        trace.finalize()


async def run_engagement(targets: list[str], scope: ScopeGuard, *, profile: str = "it",
                         rate: float = 200.0, concurrency: int = 100, timeout: float = 3.0,
                         disc_timeout: float = 1.5, retries: int = 1,
                         port_override: list[int] | None = None,
                         scan_method: str = "connect",
                         cache: WorkflowCache | None = None,
                         assets: dict[str, Asset] | None = None,
                         service_filter: set[str] | None = None,
                         stop_after_banner: bool = False,
                         stage_ceiling: str | None = None,
                         force_recheck_after: timedelta | None = None,
                         ssh_creds: dict | None = None, win_creds: dict | None = None,
                         passive_listen_seconds: float = 60.0,
                         trace: ExecutionTrace | None = None) -> dict[str, Asset]:
    """Runs gates 0/2-6 (in order) across `targets`, mutating and returning
    the Asset dict. Pass a pre-loaded `assets`/`cache` (e.g. from a prior
    engagement's JSONL) to get re-scan/delta behavior for free — gates and
    cache.should_recheck() naturally skip work that's still fresh.
    """
    cache = cache or WorkflowCache()
    stage_ceiling = resolve_stage_ceiling(
        stage_ceiling,
        stop_after_banner=stop_after_banner,
    )
    # HARD scope allowlist. The per-host gates below call scan_target()
    # directly, which bypasses BaseScanner._guarded() (where the scope check
    # normally lives), so scope MUST be enforced here at the single entry
    # point or out-of-scope hosts would be scanned. Found via testing.
    targets = list(scope.filter(targets))
    assets = assets if assets is not None else {t: Asset(host=t, profile=profile) for t in targets}
    for t in targets:
        assets.setdefault(t, Asset(host=t, profile=profile))

    # --- Gate 0: OT passive-only hard stop ------------------------------
    if gate_0_is_passive_profile(profile):
        results, coverage = await _run_passive(scope, passive_listen_seconds)
        _record(
            trace,
            "passive_collect",
            target_count=1,
            results=results,
            coverage=coverage,
        )
        _store_results(results, assets=assets, cache=cache, profile=profile)
        _finalize_trace(trace)
        return assets

    ports = _port_candidates(profile, service_filter, port_override=port_override)
    allowed_branches = PROFILE_DEEP_BRANCHES.get(profile, set())
    direct_datagram = (
        service_filter is not None
        and (
            "udp" in service_filter
            or "snmp" in (service_filter & allowed_branches)
        )
    )
    skip_tcp_discovery = direct_datagram and not ports

    # --- Gate 2: host discovery (per-host precondition) -----------------
    disc_targets = [] if skip_tcp_discovery else [
        t for t in targets if gate_2_host_discovery(assets[t], profile)
    ]
    if disc_targets:
        discovery_ports = ports if service_filter is not None else None
        disc = HostDiscoveryScanner(
            scope,
            ports=discovery_ports,
            rate=rate,
            concurrency=concurrency,
            timeout=disc_timeout,
        )
        results = await _gather_per_host(
            disc,
            disc_targets,
            max_in_flight=concurrency,
        )
        _record(
            trace,
            "host_discovery",
            target_count=len(disc_targets),
            results=results,
        )
        _store_results(results, assets=assets, cache=cache, profile=profile)

    live_hosts = [t for t in targets if assets[t].last_seen_alive is not None]

    if not includes_stage(stage_ceiling, STAGE_PORT_SCAN):
        _finalize_trace(trace)
        return assets

    # --- Gate 3: port scan ------------------------------------------------
    port_targets = [t for t in live_hosts if gate_3_port_scan(assets[t], profile)]
    if port_targets and ports:
        # Wide sweeps (full-port audit / deep intensity) go through the stateless
        # SYN scanner — far cheaper than 65k connect() calls per host. It
        # transparently falls back to a connect scan off privileged Linux, so the
        # port state + completeness metrics are identical everywhere; only the
        # method (syn vs connect_fallback) differs. Narrow scans stay on connect.
        if scan_method == "syn":
            scanner = SynScanner(scope, ports=ports, rate=rate,
                                 concurrency=concurrency, timeout=timeout)
        else:
            scanner = PortScanner(scope, ports=ports, rate=rate, concurrency=concurrency,
                                  timeout=timeout, retries=retries)
        results = await _gather_per_host(
            scanner,
            port_targets,
            max_in_flight=concurrency,
        )
        _record(
            trace,
            "port_scan",
            target_count=len(port_targets),
            results=results,
        )
        _store_results(results, assets=assets, cache=cache, profile=profile)

    if not includes_stage(stage_ceiling, STAGE_SERVICE_BANNER):
        _finalize_trace(trace)
        return assets

    # --- Gate 4: service banner ------------------------------------------
    for host in live_hosts:
        asset = assets[host]
        if not gate_4_service_banner(asset):
            continue
        candidate_ports = asset.open_ports_for_deep_scan()
        if service_filter is not None:
            candidate_ports &= set(ports)
        candidate_ports = sorted(candidate_ports)
        to_scan, reused = _split_cached(cache, host, candidate_ports, "service_banner", force_recheck_after)
        for r in reused:
            asset.merge_result(r)
        _record_reused(trace, "service_banner", reused)
        if to_scan:
            banner = ServiceBannerScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
            results = await _scan_one(banner, host)
            _record(trace, "service_banner", target_count=1, results=results)
            _store_results(results, assets=assets, cache=cache, profile=profile)

    if not includes_stage(stage_ceiling, STAGE_DEEP_SCAN):
        _finalize_trace(trace)
        return assets

    # --- Gate 5: dynamic routing + deep-scan branches ---------------------
    branch_hosts = targets if direct_datagram else live_hosts
    for host in branch_hosts:
        asset = assets[host]
        routed = route_branches(asset)

        tls_dynamic = {p for p, b in routed.items() if "tls" in b}
        web_dynamic = {p for p, b in routed.items() if "web" in b}

        if gate_5_branch_eligible("tls", asset, profile, service_filter, bool(tls_dynamic)):
            ports = sorted((asset.open_ports_for_deep_scan() & TLS_PORTS) | tls_dynamic)
            to_scan, reused = _split_cached(cache, host, ports, "tls_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "tls_scan", reused)
            if to_scan:
                tls = TLSScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(tls, host)
                _record(trace, "tls_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("web", asset, profile, service_filter, bool(web_dynamic)):
            ports = sorted((asset.open_ports_for_deep_scan() & WEB_PORTS) | web_dynamic)
            to_scan, reused = _split_cached(cache, host, ports, "web_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "web_scan", reused)
            if to_scan:
                web = WebScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(web, host)
                _record(trace, "web_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("smb", asset, profile, service_filter):
            # host-level, not per-port (see asset.py's _merge_smb_scan)
            if cache.should_recheck(host, None, "smb_scan", force_recheck_after=force_recheck_after):
                smb = SMBScanner(scope, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(smb, host)
                _record(trace, "smb_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)
            else:
                reused = [cache.get(host, None, "smb_scan").result]
                asset.merge_result(reused[0])
                _record_reused(trace, "smb_scan", reused)

        db_dynamic = {p for p, b in routed.items() if "db" in b}
        if gate_5_branch_eligible("db", asset, profile, service_filter, bool(db_dynamic)):
            ports = sorted((asset.open_ports_for_deep_scan() & DB_PORTS) | db_dynamic)
            to_scan, reused = _split_cached(cache, host, ports, "db_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "db_scan", reused)
            if to_scan:
                known = {p: DEFAULT_DB_PORTS[p] for p in to_scan if p in DEFAULT_DB_PORTS}
                unknown = [p for p in to_scan if p not in DEFAULT_DB_PORTS]
                if known:
                    db = DBScanner(scope, port_map=known, rate=rate, concurrency=concurrency, timeout=timeout)
                    results = await _scan_one(db, host)
                    _record(trace, "db_scan", target_count=1, results=results)
                    _store_results(results, assets=assets, cache=cache, profile=profile)
                if unknown:
                    # Non-standard port routed by banner signature: try every DB probe.
                    db2 = DBScanner(scope, port_map={p: "" for p in unknown},
                                    try_all_on_port=True, rate=rate,
                                    concurrency=concurrency, timeout=timeout)
                    results = await _scan_one(db2, host)
                    _record(trace, "db_scan", target_count=1, results=results)
                    _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("mcp_ai", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & AI_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "mcp_ai_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "mcp_ai_scan", reused)
            if to_scan:
                ai = MCPAIScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(ai, host)
                _record(trace, "mcp_ai_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        ssh_dynamic = {p for p, b in routed.items() if "ssh" in b}
        if gate_5_branch_eligible("ssh", asset, profile, service_filter, bool(ssh_dynamic)):
            ports = sorted((asset.open_ports_for_deep_scan() & SSH_PORTS) | ssh_dynamic)
            to_scan, reused = _split_cached(cache, host, ports, "ssh_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "ssh_scan", reused)
            if to_scan:
                ssh = SSHScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(ssh, host)
                _record(trace, "ssh_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("smb_enum", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & SMB_ENUM_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "smb_enum_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "smb_enum_scan", reused)
            if to_scan:
                smbe = SMBEnumScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(smbe, host)
                _record(trace, "smb_enum_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("ldap", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & LDAP_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "ldap_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "ldap_scan", reused)
            if to_scan:
                ldp = LDAPScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(ldp, host)
                _record(trace, "ldap_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("dns", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & DNS_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "dns_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "dns_scan", reused)
            if to_scan:
                dns = DNSScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(dns, host)
                _record(trace, "dns_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("nfs", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & NFS_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "nfs_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "nfs_scan", reused)
            if to_scan:
                nfs = NFSScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(nfs, host)
                _record(trace, "nfs_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("ftp", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & FTP_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "ftp_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "ftp_scan", reused)
            if to_scan:
                ftp = FTPScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(ftp, host)
                _record(trace, "ftp_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("rsync", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & RSYNC_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "rsync_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "rsync_scan", reused)
            if to_scan:
                rsync = RsyncScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(rsync, host)
                _record(trace, "rsync_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("vnc", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & VNC_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "vnc_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "vnc_scan", reused)
            if to_scan:
                vnc = VNCScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(vnc, host)
                _record(trace, "vnc_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("smtp", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & SMTP_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "smtp_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "smtp_scan", reused)
            if to_scan:
                smtp = SMTPScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(smtp, host)
                _record(trace, "smtp_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("msrpc", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & MSRPC_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "msrpc_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "msrpc_scan", reused)
            if to_scan:
                msrpc = MSRPCScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(msrpc, host)
                _record(trace, "msrpc_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        # RDP: the confirming X.224 + NLA-posture scanner (verified). Without this
        # branch the agent's network_va never assessed 3389, so RDP-without-NLA and
        # RDP-exposed weaknesses the scripts catch never reached the manager.
        if gate_5_branch_eligible("rdp", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & RDP_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "rdp_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "rdp_scan", reused)
            if to_scan:
                rdp = RDPScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(rdp, host)
                _record(trace, "rdp_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("printer", asset, profile, service_filter):
            ports = sorted(asset.open_ports_for_deep_scan() & PRINTER_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "printer_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "printer_scan", reused)
            if to_scan:
                printer = PrinterScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(printer, host)
                _record(trace, "printer_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("snmp", asset, profile, service_filter):
            ports = sorted(SNMP_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "snmp_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "snmp_scan", reused)
            if to_scan:
                snmp = SNMPScanner(scope, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(snmp, host)
                _record(trace, "snmp_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if gate_5_branch_eligible("ipmi", asset, profile, service_filter):
            ports = sorted(IPMI_PORTS)
            to_scan, reused = _split_cached(cache, host, ports, "ipmi_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "ipmi_scan", reused)
            if to_scan:
                ipmi = IPMIScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(ipmi, host)
                _record(trace, "ipmi_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

        if service_filter is None or "udp" in service_filter:
            udp_ports = sorted(UDP_PORTS)
            to_scan, reused = _split_cached(cache, host, udp_ports, "udp_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "udp_scan", reused)
            if to_scan:
                udp = UDPScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                results = await _scan_one(udp, host)
                _record(trace, "udp_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

    # --- Gate 6: credentialed collection -----------------------------------
    for host in live_hosts:
        asset = assets[host]
        if gate_6_credentialed_collection(asset, bool(ssh_creds), bool(win_creds)):
            if ssh_creds:
                results = await _run_inventory(
                    "ssh_inventory",
                    host,
                    lambda: SSHCollector(scope, **ssh_creds),
                )
                _record(trace, "ssh_inventory", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)
            if win_creds:
                results = await _run_inventory(
                    "windows_inventory",
                    host,
                    lambda: WindowsCollector(scope, **win_creds),
                )
                _record(trace, "windows_inventory", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

    _finalize_trace(trace)
    return assets
