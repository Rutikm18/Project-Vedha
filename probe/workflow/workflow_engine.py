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

from contextlib import contextmanager

import asyncio
import inspect
import logging
import os
import time
from dataclasses import asdict
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
from .host_health import HostHealthMonitor
from .gates import (
    PROFILE_PORTS, PROFILE_DEEP_BRANCHES, SMB_PORTS, UDP_PORTS,
    gate_0_is_passive_profile, gate_2_host_discovery, gate_3_port_scan,
    gate_4_service_banner, gate_4b_os_fingerprint,
    gate_5_branch_eligible, gate_6_credentialed_collection,
)
from .execution import ExecutionTrace, scanner_failure_result
from .modes import (
    STAGE_DEEP_SCAN,
    STAGE_HOST_DISCOVERY,
    STAGE_PORT_SCAN,
    STAGE_SERVICE_BANNER,
    includes_stage,
    resolve_stage_ceiling,
)
from .router import route_branches

LOG = logging.getLogger("workflow")

# Hosts whose stage-boundary chunks upload at once. Small on purpose: this
# is network I/O between scan stages, not scanning, and a wide fan-out here
# would compete with the very scan it is protecting.
_COMMIT_CONCURRENCY = 8


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
    on_results=None,
) -> list[ScanResult]:
    """Run per-host probes with bounded fan-out and failure isolation.

    `on_results` receives ONE host's results the moment that host finishes. A job
    cut short — runtime ceiling reached, lease revoked — cancels this gather, and
    everything it was still holding died with it, so a scan that had genuinely
    finished twenty hosts reported none of them. Handing each host over as it
    completes is what makes the partial-result paths in agent/engine.py real.

    Slots are a semaphore rather than fixed batches for the same reason: a batch
    could not release a finished host until its slowest peer was done.
    """
    if not hosts:
        return []
    slots = asyncio.Semaphore(max(1, int(max_in_flight)))
    per_host: list[list[ScanResult]] = [[] for _ in hosts]

    async def _one(index: int, host: str) -> None:
        async with slots:
            out = await _scan_one(scanner, host)
        per_host[index] = out
        if on_results is not None:
            on_results(out)

    await asyncio.gather(*(_one(i, h) for i, h in enumerate(hosts)))
    # Returned in HOST order, not completion order: callers (and their tests)
    # read this list positionally against the target list.
    return [result for batch in per_host for result in batch]


# The smallest tail budget a host is ever given. Both port scanners read a
# falsy budget (0 or None) as UNBOUNDED, so a host that starts after the job's
# tail deadline must get a tiny POSITIVE one: the scanner then probes nothing
# and its scan_summary reports those ports not_scanned.
_MIN_TAIL_BUDGET = 0.001


class _BudgetedScan:
    """ONE shared scanner, driven with a budget chosen as each host starts.

    The port tail's hosts share one scanner because its rate limiter, socket
    semaphore and SYN send pacer are what hold the stage to the envelope the
    job was admitted under; a scanner per host would multiply all three by the
    hosts in flight. Only the budget differs per host, so it travels per call.

    Exposes what _scan_one uses — `name` and `scan_target(host)` — and calls
    the shared scanner's scan_target for exactly the host it was given, which
    is the call every per-host stage makes. Scope is enforced where
    run_engagement filters its targets, so the path is unchanged.
    """

    def __init__(self, scanner, budget_for):
        self._scanner = scanner
        self._budget_for = budget_for
        self.name = scanner.name

    async def scan_target(self, host: str) -> list[ScanResult]:
        # Evaluated HERE, after _gather_per_host has granted this host a slot,
        # so the budget reflects when the host's sweep actually starts.
        return await self._scanner.scan_target(
            host, deadline_seconds=self._budget_for())


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


def _default_host_concurrency(concurrency: int) -> int:
    """Hosts scanned in parallel during the deep-branch stage.

    Env override: PROBE_HOST_CONCURRENCY. Capped hard, because the deep stage is
    dominated by waiting rather than bandwidth — a modest fan-out reclaims nearly
    all of the wall time, while a large one just multiplies simultaneous load on
    the customer network for no gain.
    """
    raw = (os.environ.get("PROBE_HOST_CONCURRENCY") or "").strip()
    if raw:
        try:
            return max(1, min(64, int(raw)))
        except ValueError:
            LOG.warning("ignoring non-numeric PROBE_HOST_CONCURRENCY=%r", raw)
    # Each host makes several calls on asyncio's default thread pool, which is
    # min(32, cpu + 4) workers. More hosts than workers just queue and starve
    # each other (the saturation _recheck_alive documents), and a small customer
    # machine has few cores, so the default follows the pool when it is smaller.
    pool = min(32, (os.cpu_count() or 1) + 4)
    return max(1, min(8, concurrency, pool))


@contextmanager
def _timed(trace: ExecutionTrace | None, component_id: str):
    """Accumulate wall time for a stage. No-op when tracing is off."""
    if trace is None:
        yield
        return
    with trace.timing(component_id):
        yield


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
) -> list[ScanResult]:
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
        return []

    if spec.host_level:
        # Cached under port=None: one fact per host, not per port.
        if not cache.should_recheck(host, None, spec.component,
                                    force_recheck_after=force_recheck_after):
            entry = cache.get(host, None, spec.component)
            asset.merge_result(entry.result)
            _record_reused(trace, spec.component, [entry.result])
            return []
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
            return []

    # Resolved from THIS module's namespace at call time, so tests that patch
    # workflow_engine.<Scanner> keep working exactly as they did.
    scanner_cls = globals()[spec.scanner]
    produced: list[ScanResult] = []
    for extra in spec.kwargs(asset, ports):
        scanner = scanner_cls(scope, rate=rate, concurrency=concurrency,
                              timeout=timeout, **extra)
        with _timed(trace, spec.component):
            results = await _scan_one(scanner, host)
        _record(trace, spec.component, target_count=1, results=results)
        _store_results(results, assets=assets, cache=cache, profile=profile)
        produced.extend(results)
    return produced


async def run_engagement(targets: list[str], scope: ScopeGuard, *, profile: str = "it",
                         rate: float = 200.0, concurrency: int = 100, timeout: float = 3.0,
                         disc_timeout: float = 1.5, retries: int = 1,
                         max_host_seconds: float | None = None,
                         tail_deadline: float | None = None,
                         port_override: list[int] | None = None,
                         first_pass_ports: list[int] | None = None,
                         udp_port_set: list[int] | None = None,
                         on_host_complete=None,
                         skip_hosts: set[str] | None = None,
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
                         host_concurrency: int | None = None,
                         trace: ExecutionTrace | None = None) -> dict[str, Asset]:
    """Runs gates 0/2-6 (in order) across `targets`, mutating and returning
    the Asset dict. Pass a pre-loaded `assets`/`cache` (e.g. from a prior
    engagement's JSONL) to get re-scan/delta behavior for free — gates and
    cache.should_recheck() naturally skip work that's still fresh.

    `tail_deadline` (a time.monotonic() value) bounds a phased sweep's port
    tail by the job's time budget: each host's tail budget is capped at the
    time left when that host starts. None bounds it by max_host_seconds alone.
    """
    cache = cache or WorkflowCache()
    # How many hosts run their deep-branch sequence at once. Deliberately far
    # below `concurrency` (which bounds sockets WITHIN one scanner): this
    # multiplies total in-flight work, and a lab that tolerates 100 sockets to
    # one host will not thank us for 100 hosts at once.
    if host_concurrency is None:
        host_concurrency = _default_host_concurrency(concurrency)
    stage_ceiling = resolve_stage_ceiling(
        stage_ceiling,
        stop_after_banner=stop_after_banner,
    )
    # HARD scope allowlist. The per-host gates below call scan_target()
    # directly, which bypasses BaseScanner._guarded() (where the scope check
    # normally lives), so scope MUST be enforced here at the single entry
    # point or out-of-scope hosts would be scanned. Found via testing.
    targets = list(scope.filter(targets))
    # RESUME. Hosts the manager already holds evidence for (see the probe's
    # committed_hosts) are not rescanned: a retry after a crashed attempt should
    # cost only the hosts that were still outstanding. Their facts are not lost —
    # the manager merges what it buffered into this job's final result.
    if skip_hosts:
        already = [t for t in targets if t in skip_hosts]
        if already:
            LOG.info("resume: %d host(s) already committed — not rescanning",
                     len(already))
            targets = [t for t in targets if t not in skip_hosts]
    assets = assets if assets is not None else {t: Asset(host=t, profile=profile) for t in targets}
    for t in targets:
        assets.setdefault(t, Asset(host=t, profile=profile))

    # Does the caller's sink understand partial commits? Inspected once so an
    # older two-argument sink keeps working unchanged.
    _sink_wants_complete = False
    if on_host_complete is not None:
        try:
            _sink_wants_complete = "complete" in inspect.signature(
                on_host_complete).parameters
        except (TypeError, ValueError):
            _sink_wants_complete = False

    # host -> fact count at its last PARTIAL commit, so a stage that added
    # nothing for a host does not re-POST identical evidence. At 1000 hosts x
    # four stage boundaries that is the difference between 4,000 requests and
    # only the ones carrying something new.
    _committed_sig: dict[str, int] = {}

    def _at_ceiling(stage: str) -> bool:
        """Is this stage where THIS job stops? Then its commit is the host's
        final word, and the manager may skip that host on a retry."""
        return stage == stage_ceiling

    async def _commit_host(host: str, *, complete: bool = True) -> None:
        """Hand ONE host's evidence to the caller (the probe commits it to the
        manager) so work already done survives a process that never returns.

        `complete` says whether this is the host's final word. Mid-pipeline
        commits are partial: they protect the evidence but must never let a
        retry skip a host that was only discovered, not scanned.

        Best-effort: the buffer is an optimisation and must never be able to
        fail a scan that is working.
        """
        if on_host_complete is None:
            return
        try:
            # Serialisable fact dicts, the same shape agent/engine.py submits —
            # the caller puts these straight on the wire.
            #
            # Via the cache's host index, NOT a scan of every entry. This runs
            # once per host over a cache that grows with every host, so the
            # inline scan it replaces was O(hosts x entries) across a job —
            # 5.0 ms/host at 1000 hosts, awaited on the event loop, stalling
            # every other host's scan behind it.
            facts = [asdict(entry.result)
                     for entry in cache.all_entries_for_host(host)]
            if not facts:
                return
            # A partial commit that would repeat the last one is pure cost.
            # A COMPLETE one always goes through: it flips the host's state
            # from "evidence held" to "finished", which is what resume reads.
            if not complete and _committed_sig.get(host) == len(facts):
                return
            outcome = (on_host_complete(host, facts, complete=complete)
                       if _sink_wants_complete else on_host_complete(host, facts))
            if inspect.isawaitable(outcome):
                await outcome
            _committed_sig[host] = len(facts)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            LOG.debug("per-host commit for %s failed: %s", host, exc)

    async def _commit_stage(hosts: list[str], *, complete: bool) -> None:
        """Deliver one stage's evidence for many hosts, with bounded fan-out.

        Every stage before the deep branches used to reach the manager ONLY via
        the job's final submission, so a probe killed during the port sweep —
        where a wide scan spends its hours — lost all of it. Worse, a job whose
        ceiling stops before deep_scan returned early and committed nothing at
        all, ever.
        """
        if on_host_complete is None or not hosts:
            return
        slots = asyncio.Semaphore(max(1, _COMMIT_CONCURRENCY))

        async def _one(host: str) -> None:
            async with slots:
                await _commit_host(host, complete=complete)

        await asyncio.gather(*(_one(host) for host in hosts))

    def _port_scanner_for(port_list: list[int], *, method: str):
        """The port scanner for ONE phase.

        Wide sweeps go through the stateless SYN scanner — far cheaper than 65k
        connect() calls per host — and it falls back to a connect scan off
        privileged Linux, so port states and completeness metrics are identical
        everywhere; only the method (syn vs connect_fallback) differs.

        Both paths carry `retries` and the per-host budget: max_host_seconds
        bounds ONE host's sweep, and ports it does not reach are reported
        not_scanned, never "filtered", so a truncated sweep stays honest.
        """
        if method == "syn":
            return SynScanner(scope, ports=port_list, rate=rate,
                              concurrency=concurrency, timeout=timeout,
                              retries=retries, deadline_seconds=max_host_seconds)
        return PortScanner(scope, ports=port_list, rate=rate,
                           concurrency=concurrency, timeout=timeout,
                           retries=retries, deadline_seconds=max_host_seconds)

    def _deliver(results: list[ScanResult]) -> None:
        """Store ONE host's results the moment that host finishes.

        The per-host stages below used to store everything after the whole stage
        returned, so a job cut short mid-stage lost every completed host with it.
        agent/engine.py builds its partial result from this cache, so delivering
        here is what an interrupted scan actually reports.
        """
        _store_results(results, assets=assets, cache=cache, profile=profile)

    # --- Gate 0: OT passive-only hard stop ------------------------------
    if gate_0_is_passive_profile(profile):
        with _timed(trace, "passive_collect"):
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
        with _timed(trace, "ipv6_discovery"):
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
    # TWO-PHASE COVERAGE. The same ports, in an order that pays out early.
    #
    # A deep run asks for all 65,535 ports, and every stage that turns a port
    # into an ASSESSMENT — banner, OS, the deep branches — waited for the whole
    # sweep. At the aggressive envelope that is 109s per host at best (280-2,728s
    # measured), so on a /24 nothing was assessed for hours, and a job cut short
    # had port states with nothing behind them.
    #
    # So sweep the high-signal set first (the caller's fast list UNION the branch
    # catalogs — a fast pass without the branch ports could not assess anything),
    # let the rest of the pipeline run on it, then take the remainder as a
    # budgeted tail. Coverage is unchanged; only the order is.
    #
    # Skipped when nothing runs after the port stage (a full-port audit): there
    # is no assessment to bring forward, so phasing would only add a second
    # scanner setup.
    requested_ports = list(ports)
    tail_ports: list[int] = []
    if first_pass_ports and includes_stage(stage_ceiling, STAGE_DEEP_SCAN):
        fast = set(_port_candidates(profile, service_filter,
                                    port_override=list(first_pass_ports)))
        first = sorted(fast & set(ports))
        if first and len(first) < len(ports):
            tail_ports = sorted(set(ports) - set(first))
            ports = first
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
        LOG.info("stage host_discovery: probing %d target(s)", len(disc_targets))
        discovery_ports = ports if service_filter is not None else None
        disc = HostDiscoveryScanner(
            scope,
            ports=discovery_ports,
            rate=rate,
            concurrency=concurrency,
            timeout=disc_timeout,
        )
        with _timed(trace, "host_discovery"):
            results = await _gather_per_host(
                disc,
                disc_targets,
                max_in_flight=concurrency,
                on_results=_deliver,
            )
        _record(
            trace,
            "host_discovery",
            target_count=len(disc_targets),
            results=results,
        )

    live_hosts = [t for t in targets if assets[t].last_seen_alive is not None]

    # Every target, not just the live ones: "this host did not answer" is
    # evidence the operator needs, and a discovery-only job has nothing else.
    await _commit_stage(targets, complete=_at_ceiling(STAGE_HOST_DISCOVERY))

    if not includes_stage(stage_ceiling, STAGE_PORT_SCAN):
        _finalize_trace(trace)
        return assets

    # --- Gate 3: port scan ------------------------------------------------
    port_targets = [t for t in live_hosts if gate_3_port_scan(assets[t], profile)]
    LOG.info("stage host_discovery: %d of %d target(s) alive", len(live_hosts), len(targets))
    if port_targets and ports:
        LOG.info("stage port_scan: %d host(s) x %d port(s)", len(port_targets), len(ports))
        # A phased run's first pass is the small high-signal set, so it takes the
        # proven connect path; `scan_method` describes the WIDE sweep, which in a
        # phased run is the tail below.
        scanner = _port_scanner_for(
            ports, method="connect" if tail_ports else scan_method)
        with _timed(trace, "port_scan"):
            results = await _gather_per_host(
                scanner,
                port_targets,
                # HOST slots, not the socket budget. `concurrency` bounds sockets
                # WITHIN a scanner; using it here also started that many hosts at
                # once, so on a /24 every live host swept in lockstep and none
                # finished early. The shared semaphore still caps total sockets,
                # so throughput is unchanged — but memory is bounded, hosts
                # complete progressively, and a per-host budget means something.
                max_in_flight=host_concurrency,
                on_results=_deliver,
            )
        _record(
            trace,
            "port_scan",
            target_count=len(port_targets),
            results=results,
        )

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
            with _timed(trace, "os_fingerprint"):
                # HOST slots, not the socket budget — the same correction the
                # port and deep stages already carry. It matters most here:
                # scan_target makes THREE run_in_executor(None, ...) calls per
                # host (SMB2 negotiate, ICMP echo TTL, ICMP timestamp) on the
                # DEFAULT thread pool, which is min(32, cpu+4). At the
                # aggressive envelope `concurrency` is up to 500, so this
                # queued ~1,500 blocking tasks against ~14 workers — the
                # saturation _recheck_alive below documents from the field:
                # the heartbeat it needs cannot get a worker either.
                results = await _gather_per_host(
                    osfp, to_scan, max_in_flight=host_concurrency)
            _record(trace, "os_fingerprint", target_count=len(to_scan), results=results)
            _store_results(results, assets=assets, cache=cache, profile=profile)

    # The port sweep is where a wide scan spends its HOURS. Committing here is
    # the single most valuable point in the pipeline: before this, a probe
    # killed mid-sweep delivered nothing at all.
    await _commit_stage(live_hosts, complete=_at_ceiling(STAGE_PORT_SCAN))

    if not includes_stage(stage_ceiling, STAGE_SERVICE_BANNER):
        _finalize_trace(trace)
        return assets

    # --- Gate 4: service banner ------------------------------------------
    async def _banner_pass(hosts: list[str]) -> None:
        """Fingerprint the OPEN ports of each host.

        Cache-guarded per (host, port), so running it a second time after the
        port tail probes ONLY the ports the tail newly opened — which is what
        stops a tail-discovered service from reaching the manager as a bare port
        number with no product behind it.
        """
        # Hosts run CONCURRENTLY. Every other per-host stage already fans out
        # (host_discovery and os_fingerprint via _gather_per_host, the deep
        # branches via host_slots); this one was a plain loop, so the stage cost
        # the SUM of every host's banner grabs while the other slots sat idle.
        # A banner grab is mostly waiting for a remote service to speak first,
        # which is exactly the shape that overlaps well.
        #
        # Bounded by the same host_concurrency the deep stage uses, for the
        # reason its docstring gives: `concurrency` bounds sockets WITHIN one
        # scanner, so using it here too would multiply total in-flight work —
        # and a banner grab opens a socket per OPEN port, which would make this
        # the widest burst in the pipeline.
        slots = asyncio.Semaphore(max(1, host_concurrency))

        async def _banner_one(host: str) -> None:
            asset = assets[host]
            if not gate_4_service_banner(asset):
                return
            candidate_ports = asset.open_ports_for_deep_scan()
            if service_filter is not None:
                # The REQUESTED coverage, not the current phase's slice.
                candidate_ports &= set(requested_ports)
            candidate_ports = sorted(candidate_ports)
            to_scan, reused = _split_cached(cache, host, candidate_ports, "service_banner", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "service_banner", reused)
            if not to_scan:
                return
            banner = ServiceBannerScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
            async with slots:
                with _timed(trace, "service_banner"):
                    results = await _scan_one(banner, host)
            _record(trace, "service_banner", target_count=1, results=results)
            _store_results(results, assets=assets, cache=cache, profile=profile)

        await asyncio.gather(*(_banner_one(host) for host in hosts))

    LOG.info("stage service_banner: %d host(s)", len(live_hosts))
    await _banner_pass(live_hosts)

    await _commit_stage(live_hosts, complete=_at_ceiling(STAGE_SERVICE_BANNER))

    if not includes_stage(stage_ceiling, STAGE_DEEP_SCAN):
        _finalize_trace(trace)
        return assets

    # --- Gate 5: dynamic routing + deep-scan branches ---------------------
    # Every branch is a row in branches.BRANCHES; _run_branch below is the ONE
    # implementation of the gate -> split-cache -> scan -> record -> store shape
    # they all shared. Adding a service is now a table row, not ten more lines.
    branch_hosts = targets if direct_datagram else live_hosts

    # A host proven alive at Gate 2 can still go away mid-scan — rebooted,
    # unplugged, DHCP-moved. The monitor watches every branch's results and, on
    # sustained silence, spends ONE active liveness re-check to decide between
    # "gone" and "merely filtered". See workflow/host_health.py for why silence
    # alone can never be the verdict.
    async def _recheck_alive(host: str) -> bool:
        """Is this host still answering?

        A plain asyncio connect to a port THIS SCAN already proved open. Two
        reasons it is not HostDiscoveryScanner:

        * Cost of being wrong is low but cost of being slow is high — every
          scanner offloads its blocking socket work to the default thread pool,
          and during the datagram tail that pool is saturated. A heartbeat that
          needs a worker thread just queues behind the very scanners it is
          supposed to be watching, and silently stops heartbeating. That is
          exactly what happened: one beat got through, then nothing.
        * "The port that was open thirty seconds ago no longer accepts a
          connection" is a sharper liveness signal than a fresh discovery sweep,
          and it costs one socket.

        Falls back to discovery only when no open TCP port is known.
        """
        known_open = sorted(assets[host].open_ports_for_deep_scan())[:2]
        for port in known_open:
            try:
                fut = asyncio.open_connection(host, port)
                reader, writer = await asyncio.wait_for(fut, timeout=disc_timeout)
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
                return True
            except (OSError, asyncio.TimeoutError):
                continue
        if known_open:
            return False
        disc = HostDiscoveryScanner(scope, rate=rate, concurrency=1,
                                    timeout=disc_timeout)
        results = await _scan_one(disc, host)
        return any((r.data or {}).get("alive") for r in results)

    health = HostHealthMonitor(_recheck_alive)
    _deep_done = [0]            # list so the closure can mutate it
    _deep_total = [len(branch_hosts)]   # reset for the tail's follow-up pass

    async def _scan_one_host(host: str) -> None:
        asset = assets[host]
        routed = route_branches(asset)
        for spec in BRANCHES:
            if health.is_offline(host):
                health.note_skipped(host, spec.component)
                continue
            results = await _run_branch(
                spec, host, asset, routed,
                scope=scope, assets=assets, cache=cache, trace=trace,
                profile=profile, service_filter=service_filter,
                force_recheck_after=force_recheck_after,
                rate=rate, concurrency=concurrency, timeout=timeout,
            )
            # Datagram branches are excluded on purpose: "no reply" is their
            # normal answer on nearly every host, so they carry no information
            # about whether the target is still there.
            if not spec.datagram:
                health.observe(host, spec.component, results)
                if health.suspect(host):
                    await health.confirm(host)

        if service_filter is None or "udp" in service_filter:
            if health.is_offline(host):
                health.note_skipped(host, "udp_scan")
                return
            # Aggressive intensity widens the UDP set to every catalogued
            # service; standard/stealth keep the common few (the engine default).
            udp_ports = sorted(udp_port_set) if udp_port_set is not None else sorted(UDP_PORTS)
            to_scan, reused = _split_cached(cache, host, udp_ports, "udp_scan", force_recheck_after)
            for r in reused:
                asset.merge_result(r)
            _record_reused(trace, "udp_scan", reused)
            if to_scan:
                udp = UDPScanner(scope, ports=to_scan, rate=rate, concurrency=concurrency, timeout=timeout)
                with _timed(trace, "udp_scan"):
                    results = await _scan_one(udp, host)
                _record(trace, "udp_scan", target_count=1, results=results)
                _store_results(results, assets=assets, cache=cache, profile=profile)

    async def _scan_one_host_logged(host: str) -> None:
        started = time.monotonic()
        # Heartbeat this host for exactly as long as it has work in flight. This
        # is the detector that actually works: the TCP branches finish in
        # milliseconds, so branch-failure evidence covers almost none of a scan,
        # while the datagram tail — where most of the wall time goes — produces no
        # usable signal at all.
        beat = asyncio.create_task(health.watch(host))
        try:
            await _scan_one_host(host)
        finally:
            beat.cancel()
            try:
                await beat
            except asyncio.CancelledError:
                pass
            _deep_done[0] += 1
            await _commit_host(host)
            LOG.info("  deep_scan %d/%d  %s  (%.1fs)%s",
                     _deep_done[0], _deep_total[0], host,
                     time.monotonic() - started,
                     "  OFFLINE" if health.is_offline(host) else "")

    # Hosts run CONCURRENTLY here. Every earlier stage already fans out across
    # hosts (_gather_per_host); this stage did not, so a job spent the sum of
    # every host's every branch end to end — and since most branches are waiting
    # on a UDP timeout that will never be answered, that wait dominated the whole
    # job. Each host keeps its branches in order (later branches read facts the
    # earlier ones stored); it is the hosts that overlap.
    host_slots = asyncio.Semaphore(max(1, host_concurrency))

    async def _guarded(host: str) -> None:
        async with host_slots:
            await _scan_one_host_logged(host)

    if branch_hosts:
        LOG.info("stage deep_scan: %d host(s), %d branch(es) each, %d host(s) in parallel",
                 len(branch_hosts), len(BRANCHES), host_concurrency)
        await asyncio.gather(*(_guarded(h) for h in branch_hosts))
        LOG.info("stage deep_scan: complete (%d/%d host(s))", _deep_done[0], len(branch_hosts))

    # --- Port tail: the rest of the requested range ----------------------
    # Every host now has a real assessment of the high-signal ports. Only now do
    # we spend the hours the wide sweep costs, and only as many as the job has:
    # with a tail_deadline, each host's budget is the smaller of
    # max_host_seconds and the time left when that host starts, so a wide job
    # goes on to the liveness verdicts and credentialed collection below
    # instead of running into its runtime ceiling. Ports a budget does not
    # reach are reported not_scanned.
    #
    # Nothing is cancelled. The SYN sweep runs in a worker thread that
    # cancellation cannot stop — it would keep sending after the job ended —
    # so the budget is cooperative: the scanners stop SENDING when it is spent.
    # Each host's results are still delivered as it finishes (see _deliver).
    if tail_ports and branch_hosts:
        before = {h: set(assets[h].open_ports_for_deep_scan()) for h in branch_hosts}
        LOG.info("stage port_scan: tail of %d port(s) across %d host(s)%s",
                 len(tail_ports), len(branch_hosts),
                 "" if tail_deadline is None else
                 f", {max(0.0, tail_deadline - time.monotonic()):.0f}s of the "
                 f"job's tail budget left")

        def _tail_budget() -> float | None:
            if tail_deadline is None:
                return max_host_seconds
            left = tail_deadline - time.monotonic()
            budget = min(max_host_seconds, left) if max_host_seconds else left
            return max(_MIN_TAIL_BUDGET, budget)

        tail_scanner = _port_scanner_for(tail_ports, method=scan_method)
        with _timed(trace, "port_scan"):
            tail_results = await _gather_per_host(
                _BudgetedScan(tail_scanner, _tail_budget),
                branch_hosts,
                max_in_flight=host_concurrency,
                on_results=_deliver,
            )
        _record(trace, "port_scan", target_count=len(branch_hosts),
                results=tail_results)
        # A port the tail opened has had no banner and no branch. Both passes are
        # cache-guarded, so re-running them touches only what the tail added.
        grew = [h for h in branch_hosts
                if assets[h].open_ports_for_deep_scan() - before[h]]
        if grew:
            LOG.info("stage port_scan: tail opened new port(s) on %d host(s) — "
                     "assessing them", len(grew))
            await _banner_pass(grew)
            _deep_done[0] = 0
            _deep_total[0] = len(grew)
            await asyncio.gather(*(_guarded(h) for h in grew))
        # Refresh the per-host buffer for the hosts the tail did NOT change: they
        # were committed before it ran, so their chunk still says the scan
        # stopped at the fast set. If the job dies now, the manager would promote
        # a result that understates the coverage actually achieved.
        for host in branch_hosts:
            if host not in grew:
                await _commit_host(host)

    # Offline/flaky verdicts are facts like any other: they reach the manager,
    # and they carry scan_complete=false so an incomplete host can never be read
    # as a clean one.
    health_facts = health.finalize()
    if health_facts:
        _record(trace, "host_liveness", target_count=len(health_facts),
                results=health_facts)
        _store_results(health_facts, assets=assets, cache=cache, profile=profile)

    # --- Gate 6: credentialed collection -----------------------------------
    # Hosts run CONCURRENTLY. A credentialed collection is a key
    # exchange, an auth and a series of command round trips (or an SMB session
    # setup plus DCE/RPC binds): almost entirely latency, none of it this host's
    # CPU, so it overlaps nearly perfectly. Serially, 200 Windows hosts at ~4 s
    # was 13 minutes of waiting with every other host slot idle.
    #
    # Bounded by host_concurrency like every other per-host stage, and here the
    # bound earns its keep rather than just matching a convention: these
    # collectors are BLOCKING clients (paramiko, impacket) driven through the
    # default executor of min(32, cpu+4) threads — the same pool os_fingerprint
    # was found saturating, and one collection holds a thread far longer than an
    # ICMP echo does.
    cred_slots = asyncio.Semaphore(max(1, host_concurrency))

    async def _collect_one(host: str) -> None:
        asset = assets[host]
        if not gate_6_credentialed_collection(asset, bool(ssh_creds), bool(win_creds)):
            return
        # SSH and Windows stay sequential WITHIN a host: they are two protocols
        # against the same box, and overlapping them would double the load on
        # one target to save time the fan-out above already recovers.
        for creds, component, factory in (
            (ssh_creds, "ssh_inventory", lambda: SSHCollector(scope, **ssh_creds)),
            (win_creds, "windows_inventory", lambda: WindowsCollector(scope, **win_creds)),
        ):
            if not creds:
                continue
            # Slot acquired OUTSIDE the timer so queueing never reads as
            # collection time — `timing` accumulates, and under fan-out the
            # figure is total work, not wall clock.
            async with cred_slots:
                with _timed(trace, component):
                    results = await _run_inventory(component, host, factory)
            _record(trace, component, target_count=1, results=results)
            _store_results(results, assets=assets, cache=cache, profile=profile)

    # _run_inventory converts a collector failure into a result, so one
    # unreachable host cannot cancel its peers mid-gather.
    await asyncio.gather(*(_collect_one(host) for host in live_hosts))

    _finalize_trace(trace)
    return assets
