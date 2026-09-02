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
from scanner.ipv6_discovery import discover_ipv6_hosts
from scanner.os_fingerprint import OSFingerprintScanner
from scanner.port_scanner import PortScanner
from scanner.syn_scanner import SynScanner
from scanner.service_banner import ServiceBannerScanner
from scanner.udp_scanner import UDPScanner
from scanner.passive_collector import PassiveCollector

# ── deep-scan branch scanners ────────────────────────────────────────────────
# DO NOT let ruff/vulture strip these: they look unused because no line calls
# them by name — _run_branch resolves each one out of THIS module's globals()
# using BranchSpec.scanner. That indirection is deliberate: it keeps the import
# list (and therefore every `monkeypatch.setattr("workflow.workflow_engine.X")`
# in the test-suite) exactly where it has always been, while the branch table
# owns the wiring. Deleting one turns its branch into a KeyError at scan time.
# Same idiom as the `import X as X  # re-exported for tests` trap in
# manager/backend/app/routers/agents.py.
from scanner.tls_scanner import TLSScanner as TLSScanner
from scanner.web_scanner import WebScanner as WebScanner
from scanner.smb_scanner import SMBScanner as SMBScanner
from scanner.snmp_scanner import SNMPScanner as SNMPScanner
from scanner.db_scanner import DBScanner as DBScanner
from scanner.mcp_ai_scanner import MCPAIScanner as MCPAIScanner
from scanner.ssh_scanner import SSHScanner as SSHScanner
from scanner.smb_enum_scanner import SMBEnumScanner as SMBEnumScanner
from scanner.ldap_scanner import LDAPScanner as LDAPScanner
from scanner.dns_scanner import DNSScanner as DNSScanner
from scanner.nfs_scanner import NFSScanner as NFSScanner
from scanner.ftp_scanner import FTPScanner as FTPScanner
from scanner.rsync_scanner import RsyncScanner as RsyncScanner
from scanner.vnc_scanner import VNCScanner as VNCScanner
from scanner.ipmi_scanner import IPMIScanner as IPMIScanner
from scanner.smtp_scanner import SMTPScanner as SMTPScanner
from scanner.msrpc_scanner import MSRPCScanner as MSRPCScanner
from scanner.rdp_scanner import RDPScanner as RDPScanner
from scanner.printer_scanner import PrinterScanner as PrinterScanner
from scanner.ssh_collector import SSHCollector
from scanner.windows_collector import WindowsCollector

from .asset import Asset
from .branches import BRANCHES, BranchSpec
from .cache import WorkflowCache
from .gates import (
    PROFILE_PORTS, PROFILE_DEEP_BRANCHES, SMB_PORTS, UDP_PORTS,
    gate_0_is_passive_profile, gate_2_host_discovery, gate_3_port_scan,
    gate_4_service_banner, gate_4b_os_fingerprint,
    gate_5_branch_eligible, gate_6_credentialed_collection,
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
    for spec in BRANCHES:
        if spec.branch not in requested or spec.datagram:
            continue          # datagram branches need no TCP port in the sweep
        # smb is host-level for the deep scan, but its ports still belong in the
        # TCP sweep so the SMB stage has an open 445 to gate on.
        ports.update(SMB_PORTS if spec.host_level else spec.ports)
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


async def _run_branch(
    spec: BranchSpec,
    host: str,
    asset: Asset,
    routed: dict[int, set[str]],
    *,
    scope: ScopeGuard,
    assets: dict[str, Asset],
    cache: WorkflowCache,
    trace: ExecutionTrace | None,
    profile: str,
    service_filter: set[str] | None,
    force_recheck_after: timedelta | None,
    rate: float,
    concurrency: int,
    timeout: float,
) -> None:
    """Run ONE deep-scan branch for one host: the gate -> split-cache -> scan ->
    record -> store shape that all twenty branches used to spell out by hand.

    Three port shapes, all decided by the spec, never by a branch name:
      * host-level  — the fact describes the host, so it is cached under a null
                      port key and no port intersection happens;
      * datagram    — the probe is a UDP read at a fixed port, so the port set is
                      the spec's table and an open TCP port is not required;
      * per-port    — the spec's table intersected with this host's OPEN ports,
                      plus any port router.py routed here from observed content.
    """
    dynamic = ({p for p, b in routed.items() if spec.dynamic in b}
               if spec.dynamic else set())
    if not gate_5_branch_eligible(spec.branch, asset, profile, service_filter,
                                  bool(dynamic)):
        return

    if spec.host_level:
        # Cached under port=None: one fact per host, not per port.
        if not cache.should_recheck(host, None, spec.component,
                                    force_recheck_after=force_recheck_after):
            entry = cache.get(host, None, spec.component)
            asset.merge_result(entry.result)
            _record_reused(trace, spec.component, [entry.result])
            return
        ports: list[int] = []
    else:
        candidates = (sorted(spec.ports) if spec.datagram else
                      sorted((asset.open_ports_for_deep_scan() & spec.ports) | dynamic))
        ports, reused = _split_cached(cache, host, candidates, spec.component,
                                      force_recheck_after)
        for r in reused:
            asset.merge_result(r)
        _record_reused(trace, spec.component, reused)
        if not ports:
            return

    # Resolved from THIS module's namespace at call time, so tests that patch
    # workflow_engine.<Scanner> keep working exactly as they did.
    scanner_cls = globals()[spec.scanner]
    for extra in spec.kwargs(asset, ports):
        scanner = scanner_cls(scope, rate=rate, concurrency=concurrency,
                              timeout=timeout, **extra)
        results = await _scan_one(scanner, host)
        _record(trace, spec.component, target_count=1, results=results)
        _store_results(results, assets=assets, cache=cache, profile=profile)


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
                         discover_ipv6: bool = False,
                         ipv6_iface: str | None = None,
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

    # --- Gate 1b: IPv6 neighbour discovery -------------------------------
    # A /24 names IPv4 addresses only, so an IPv6-only listener on the same
    # segment was invisible to every stage below no matter how it was scanned.
    # RFC 4861's all-nodes multicast makes every live IPv6 host on the link
    # answer, which populates the neighbour cache — no enumeration of a /64.
    #
    # SCOPE IS ENFORCED, NOT ASSUMED: a discovered address is scanned only if it
    # is inside the authorized allowlist. Everything else is REPORTED as an
    # observation and never probed, so the operator learns those hosts exist
    # (and can widen scope deliberately) without the probe widening it for them.
    if discover_ipv6:
        found = await asyncio.to_thread(
            discover_ipv6_hosts, ipv6_iface, pings=2, timeout=disc_timeout)
        in_scope = [h for h in found if scope.in_scope(h)]
        out_of_scope = [h for h in found if h not in in_scope]
        added = [h for h in in_scope if h not in assets]
        for host in added:
            assets[host] = Asset(host=host, profile=profile)
            targets.append(host)
        result = ScanResult(
            "ipv6_discovery", ipv6_iface or "auto", status="observed",
            method="icmpv6_nd_multicast",
            data={"neighbours_found": len(found),
                  "in_scope": in_scope,
                  "out_of_scope_not_scanned": out_of_scope,
                  "added_to_engagement": added,
                  "interface": ipv6_iface},
            evidence=(f"{len(found)} IPv6 neighbour(s) via ND multicast; "
                      f"{len(added)} added to the scan, "
                      f"{len(out_of_scope)} outside scope (reported, not probed)"))
        _record(trace, "ipv6_discovery", target_count=1, results=[result])
        cache.put(result)

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

    # --- Gate 4b: OS identification --------------------------------------
    # Runs at the PORT stage, not the deep stage: the OS is an inventory fact
    # every consumer wants (device_classifier weights os_guess; the manager's
    # rules and CPE layer read the release/build), and a discovery-only or
    # device-inventory job must not come back OS-blind. Cheap: one ICMP echo
    # plus, when 445 is open, one SMB2 negotiate — and it degrades honestly to
    # the SYN/ACK stack hints when ICMP is filtered or unprivileged.
    os_targets = [t for t in live_hosts if gate_4b_os_fingerprint(assets[t], profile)]
    if os_targets:
        to_scan, reused = [], []
        for host in os_targets:
            if cache.should_recheck(host, None, "os_fingerprint",
                                    force_recheck_after=force_recheck_after):
                to_scan.append(host)
            else:
                reused.append(cache.get(host, None, "os_fingerprint").result)
        for r in reused:
            assets[r.target].merge_result(r)
        _record_reused(trace, "os_fingerprint", reused)
        if to_scan:
            hints = {t: assets[t].tcp_stack_hints for t in to_scan
                     if assets[t].tcp_stack_hints}
            osfp = OSFingerprintScanner(
                scope, tcp_hints=hints, rate=rate, concurrency=concurrency,
                timeout=timeout,
                # The SMB2 NTLM build probe only pays off where 445 is reachable;
                # asking every host for it would spend a connect per host for
                # nothing. Enabled when ANY target showed 445 open.
                smb_build=any(445 in assets[t].open_ports_for_deep_scan() for t in to_scan))
            results = await _gather_per_host(osfp, to_scan, max_in_flight=concurrency)
            _record(trace, "os_fingerprint", target_count=len(to_scan), results=results)
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
    # Every branch is a row in branches.BRANCHES; _run_branch below is the ONE
    # implementation of the gate -> split-cache -> scan -> record -> store shape
    # they all shared. Adding a service is now a table row, not ten more lines.
    branch_hosts = targets if direct_datagram else live_hosts
    for host in branch_hosts:
        asset = assets[host]
        routed = route_branches(asset)
        for spec in BRANCHES:
            await _run_branch(
                spec, host, asset, routed,
                scope=scope, assets=assets, cache=cache, trace=trace,
                profile=profile, service_filter=service_filter,
                force_recheck_after=force_recheck_after,
                rate=rate, concurrency=concurrency, timeout=timeout,
            )

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
