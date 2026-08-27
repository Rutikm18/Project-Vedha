"""
va_campaign.py — the sequential Network Vulnerability-Assessment campaign.

WHY THIS EXISTS
  Every capability the probe has (discovery, inventory, deep service assessment,
  SMB/SNMP/UDP exposure, full-port audit, internet-exposure mapping, CVE
  correlation) already exists as an INDIVIDUAL scanner or use-case. What was
  missing is a single job that runs the RIGHT ones, in the RIGHT order, as one
  coherent background campaign that TELLS YOU WHAT IT IS DOING at every step.

  This module is that orchestrator. It is "phase-major": instead of finishing one
  host completely before starting the next (host-major, what scan_funnel does), it
  advances the WHOLE host set through one capability at a time —

      Discovery → Port/Service map → Deep assessment → SNMP/UDP exposure
      → Internet-exposure mapping → Device inventory → Weakness detection
      → CVE correlation

  so an operator (or the manager UI) sees a live, honest picture: "now mapping
  ports on 14 hosts", "now correlating CVEs", with per-stage counts, a percent,
  and an ETA. Cheap broad stages gate the expensive narrow ones (a dead host is
  never deep-scanned; a host with no open ports is never routed to a deep scanner).

DESIGN (dependency-injected, so the engine is testable with zero network)
  * VACampaign — the generic engine: runs an ordered list of Stage objects,
    mutating a shared CampaignContext and emitting progress after every
    transition. Knows nothing about sockets.
  * Stage — {id, name, detail, enabled?, gate?, run}. `run(ctx)` is async and
    returns a StageOutcome(results, count, note).
  * ProgressReporter — owns the CampaignProgress record, writes it atomically to
    campaign_progress.json, and invokes an optional callback on every update.
    This JSON IS THE CONTRACT the manager frontend renders.
  * default_stages(funnel, options) — the real capability stages, composed from
    the package's proven scanners via scan_funnel's public seams.

COLLECTION ONLY: the campaign composes collection-only scanners, enforces scope
before every stage, and adds no new probes or exploitation. The CVE stage emits
prioritized CANDIDATES (confidence "medium" max) — never a confirmed-vuln claim.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable

from .scanner_base import (
    ScanResult, ScopeGuard, ResultWriter, expand_targets, setup_logging,
    base_argparser, main_entrypoint, LOG,
)
from .scan_funnel import (
    build_default_funnel, route_ports, DEFAULT_PORT_ROUTES,
)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── the operator-facing capability catalog (ORDER IS THE CAMPAIGN) ─────────────
# id must be stable (the manager UI and tests key on it). name/detail are the
# "what we are doing" copy shown live. This list doubles as documentation of the
# campaign's scope.
STAGE_CATALOG: list[dict[str, str]] = [
    {"id": "discovery",  "name": "Host & Network Discovery",
     "detail": "Finding every live device on the network."},
    {"id": "port_map",   "name": "Port & Service Mapping",
     "detail": "Mapping the open TCP ports each live host exposes."},
    {"id": "assessment", "name": "Service & Deep Assessment",
     "detail": "Inspecting TLS, web, SMB/Windows, databases, SSH, LDAP, and more "
               "on the ports proven open."},
    {"id": "udp_snmp",   "name": "SNMP & UDP / Amplification Exposure",
     "detail": "Probing UDP services (SNMP, DNS, NTP, memcached, NetBIOS) for weak "
               "config and amplification exposure."},
    {"id": "full_port",  "name": "Full-Port Audit (all 65,535)",
     "detail": "Scanning every TCP port to surface services hiding on odd ports."},
    {"id": "exposure",   "name": "Internet-Exposure Mapping",
     "detail": "Recording which ports are reachable from this vantage point."},
    {"id": "inventory",  "name": "Device Inventory & Classification",
     "detail": "Inferring each device's role from OS, ports, and banners."},
    {"id": "detect",     "name": "Weakness & Vulnerability Detection",
     "detail": "Applying deterministic detection rules to every collected fact — "
               "weak protocols, insecure config, exposed and unauthenticated services."},
    {"id": "cve",        "name": "CVE Correlation",
     "detail": "Mapping observed service versions to prioritized CVE candidates."},
]


@dataclass
class CampaignOptions:
    """Everything that changes WHAT the campaign does (not HOW it reports)."""
    rate: float = 200.0
    concurrency: int = 100          # per-scanner internal concurrency
    timeout: float = 3.0
    host_concurrency: int = 64      # hosts probed in parallel within a stage
    full_ports: bool = False        # opt-in: the all-65,535 audit stage
    udp: bool = True                # SNMP/UDP exposure stage
    vuln_db: str | None = None      # opt-in: offline CVE mirror → CVE stage
    exposed: bool = False           # operator asserts targets are internet-facing
    force: bool = False             # assess even hosts discovery marks down
    out_dir: str | None = None      # where campaign_progress.json + results land


@dataclass
class StageOutcome:
    """What a stage produced. `count` is stage-specific (live hosts, open ports,
    services, candidates); `note` is the human one-liner shown in progress."""
    results: list[ScanResult] = field(default_factory=list)
    count: int = 0
    note: str = ""


# A stage's run receives the shared context and returns a StageOutcome.
StageRun = Callable[["CampaignContext"], Awaitable[StageOutcome]]


@dataclass
class Stage:
    id: str
    name: str
    detail: str
    run: StageRun
    # enabled(options) — opt-in stages return False to be marked "skipped".
    enabled: Callable[[CampaignOptions], bool] | None = None
    # gate(ctx) — data dependency; e.g. skip deep scan when no ports are open.
    gate: Callable[["CampaignContext"], bool] | None = None


@dataclass
class CampaignContext:
    """Mutable state threaded through the stages."""
    targets: list[str]
    scope: ScopeGuard
    options: CampaignOptions
    reporter: "ProgressReporter"
    live_hosts: list[str] = field(default_factory=list)
    open_ports: dict[str, list[int]] = field(default_factory=dict)  # host → open TCP
    facts: list[ScanResult] = field(default_factory=list)


# ── progress contract ─────────────────────────────────────────────────────────
@dataclass
class StageState:
    id: str
    name: str
    detail: str
    status: str = "pending"     # pending | running | done | skipped | error
    started_at: str | None = None
    ended_at: str | None = None
    count: int = 0
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "name": self.name, "detail": self.detail,
            "status": self.status, "started_at": self.started_at,
            "ended_at": self.ended_at, "count": self.count, "note": self.note,
        }


class ProgressReporter:
    """Owns the live campaign record. Every transition recomputes percent + ETA,
    writes campaign_progress.json atomically, and fires the callback. The emitted
    dict is the exact shape the manager frontend consumes."""

    def __init__(self, campaign_id: str, targets: list[str], stages: list[Stage],
                 options: CampaignOptions, *,
                 out_path: Path | None = None,
                 callback: Callable[[dict], None] | None = None):
        self.campaign_id = campaign_id
        self.targets = targets
        self.options = options
        self.out_path = out_path
        self.callback = callback
        self.started_at = _now()
        self._start_monotonic = _monotonic()
        # Only enabled stages count toward percent; disabled opt-ins are excluded
        # so a campaign without --full-ports still reaches 100 %.
        self._enabled_ids = {
            s.id for s in stages
            if s.enabled is None or s.enabled(options)
        }
        self.stages: dict[str, StageState] = {
            s.id: StageState(s.id, s.name, s.detail,
                             status=("pending" if s.id in self._enabled_ids else "skipped"))
            for s in stages
        }
        self._order = [s.id for s in stages]
        self.status = "running"
        self.totals: dict[str, int] = {}
        self._flush()

    # -- transitions -----------------------------------------------------------
    def mark(self, stage_id: str, status: str, *, count: int = 0, note: str = "") -> None:
        st = self.stages[stage_id]
        if status == "running":
            st.started_at = _now()
        elif status in ("done", "skipped", "error"):
            st.ended_at = _now()
            st.count = count
            st.note = note
        st.status = status
        self._flush()

    def set_totals(self, **totals: int) -> None:
        self.totals.update(totals)
        self._flush()

    def finish(self, status: str = "completed") -> None:
        self.status = status
        self._flush()

    # -- derived fields --------------------------------------------------------
    def _percent(self) -> int:
        active = [i for i in self._order if i in self._enabled_ids]
        if not active:
            return 100
        done = sum(1 for i in active
                   if self.stages[i].status in ("done", "skipped", "error"))
        return round(100 * done / len(active))

    def _current(self) -> str | None:
        for i in self._order:
            if self.stages[i].status == "running":
                return i
        return None

    def _eta_seconds(self) -> float | None:
        active = [i for i in self._order if i in self._enabled_ids]
        done = sum(1 for i in active
                   if self.stages[i].status in ("done", "skipped", "error"))
        if done == 0 or done >= len(active):
            return None
        elapsed = _monotonic() - self._start_monotonic
        per_stage = elapsed / done
        return round(per_stage * (len(active) - done), 1)

    def snapshot(self) -> dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "targets": self.targets,
            "status": self.status,
            "started_at": self.started_at,
            "updated_at": _now(),
            "percent": self._percent(),
            "current_stage": self._current(),
            "eta_seconds": self._eta_seconds(),
            "stages": [self.stages[i].to_dict() for i in self._order],
            "totals": dict(self.totals),
        }

    def _flush(self) -> None:
        snap = self.snapshot()
        if self.out_path is not None:
            _atomic_write_json(self.out_path, snap)
        if self.callback is not None:
            try:
                self.callback(snap)
            except Exception as exc:                 # a bad sink never breaks a scan
                LOG.debug("progress callback error: %s", exc)


def _monotonic() -> float:
    # Isolated so the one time-source the engine needs is easy to fake in tests.
    import time
    return time.monotonic()


def _atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str))
    os.replace(tmp, path)


# ── the engine ────────────────────────────────────────────────────────────────
class VACampaign:
    """Runs the ordered stages sequentially, emitting progress throughout.

    The engine is deliberately dumb: it enforces enable/gate, times each stage,
    funnels results into the shared context, and never lets one stage's failure
    abort the campaign (the stage is marked "error" and the run continues)."""

    def __init__(self, ctx: CampaignContext, stages: list[Stage]):
        self.ctx = ctx
        self.stages = stages

    async def run(self) -> dict[str, Any]:
        rep = self.ctx.reporter
        for stage in self.stages:
            if stage.enabled is not None and not stage.enabled(self.ctx.options):
                continue                              # already "skipped" in the record
            if stage.gate is not None and not stage.gate(self.ctx):
                rep.mark(stage.id, "skipped", note="prerequisite not met")
                continue
            rep.mark(stage.id, "running")
            try:
                outcome = await stage.run(self.ctx)
            except Exception as exc:                  # isolate stage failure
                LOG.warning("campaign stage %s failed: %s", stage.id, exc)
                rep.mark(stage.id, "error", note=f"{type(exc).__name__}: {exc}")
                continue
            self.ctx.facts.extend(outcome.results)
            rep.mark(stage.id, "done", count=outcome.count, note=outcome.note)
            self._refresh_totals()
        rep.finish("completed")
        return rep.snapshot()

    def _refresh_totals(self) -> None:
        open_total = sum(len(v) for v in self.ctx.open_ports.values())
        self.ctx.reporter.set_totals(
            live_hosts=len(self.ctx.live_hosts),
            open_ports=open_total,
            facts=len(self.ctx.facts),
        )


# ── default capability stages (compose the real scanners) ─────────────────────
def _alive(results: list[ScanResult]) -> bool:
    return any((r.data or {}).get("alive") for r in results)


def _candidate_ports(routes: dict[str, list[int]]) -> list[int]:
    ports: set[int] = set()
    for rp in routes.values():
        ports.update(rp)
    return sorted(ports)


async def _bounded_gather(items, coro_factory, limit: int):
    """Run coro_factory(item) over items with bounded concurrency; return the
    list of results in completion order (errors become empty lists)."""
    sem = asyncio.Semaphore(max(1, limit))

    async def _one(it):
        async with sem:
            try:
                return await coro_factory(it)
            except Exception as exc:
                LOG.debug("host task error %s: %s", it, exc)
                return []

    return await asyncio.gather(*[_one(it) for it in items])


def default_stages(funnel) -> list[Stage]:
    """Build the real capability stages from a pre-wired ScanFunnel, reusing its
    proven scanner construction (discovery, port factory, deep routing, UDP)."""

    async def run_discovery(ctx: CampaignContext) -> StageOutcome:
        hosts = [h for h in expand_targets(ctx.targets) if ctx.scope.in_scope(h)]
        per_host = await _bounded_gather(
            hosts, lambda h: funnel.discovery.scan_target(h),
            ctx.options.host_concurrency)
        results: list[ScanResult] = []
        live: list[str] = []
        for h, res in zip(hosts, per_host):
            results.extend(res)
            if _alive(res) or ctx.options.force:
                live.append(h)
        ctx.live_hosts = live
        return StageOutcome(results, count=len(live),
                            note=f"{len(live)} live host(s) of {len(hosts)} probed")

    async def _map_ports(ctx: CampaignContext, ports: list[int], label: str) -> StageOutcome:
        results: list[ScanResult] = []

        async def _one(h):
            scanner = funnel.port_scanner_factory(ports)
            res = await scanner.scan_target(h)
            open_p = sorted({r.port for r in res
                             if r.status == "open" and r.proto == "tcp"
                             and r.port is not None})
            ctx.open_ports[h] = sorted(set(ctx.open_ports.get(h, [])) | set(open_p))
            return res

        per_host = await _bounded_gather(ctx.live_hosts, _one, ctx.options.host_concurrency)
        for res in per_host:
            results.extend(res)
        total_open = sum(len(v) for v in ctx.open_ports.values())
        return StageOutcome(results, count=total_open,
                            note=f"{total_open} open port(s) across "
                                 f"{len(ctx.live_hosts)} host(s) [{label}]")

    async def run_port_map(ctx: CampaignContext) -> StageOutcome:
        return await _map_ports(ctx, _candidate_ports(funnel.routes), "service ports")

    async def run_full_port(ctx: CampaignContext) -> StageOutcome:
        return await _map_ports(ctx, list(range(1, 65536)), "all 65,535")

    async def run_assessment(ctx: CampaignContext) -> StageOutcome:
        results: list[ScanResult] = []
        services = 0

        async def _one(h):
            nonlocal services
            open_ports = ctx.open_ports.get(h, [])
            host_results: list[ScanResult] = []
            for route_name, ports in route_ports(open_ports, funnel.routes).items():
                factory = funnel.deep_scanner_factories.get(route_name)
                if factory is None:
                    continue
                scanner = factory(ports)
                res = await scanner.scan_target(h)
                host_results.extend(res)
                services += 1
            return host_results

        hosts = [h for h in ctx.live_hosts if ctx.open_ports.get(h)]
        per_host = await _bounded_gather(hosts, _one, ctx.options.host_concurrency)
        for res in per_host:
            results.extend(res)
        return StageOutcome(results, count=len(results),
                            note=f"assessed {len(hosts)} host(s), "
                                 f"{services} service scan(s)")

    async def run_udp_snmp(ctx: CampaignContext) -> StageOutcome:
        if funnel.udp_scanner is None:
            return StageOutcome([], 0, "UDP scanning disabled")
        per_host = await _bounded_gather(
            ctx.live_hosts, lambda h: funnel.udp_scanner.scan_target(h),
            ctx.options.host_concurrency)
        results: list[ScanResult] = []
        for res in per_host:
            results.extend(res)
        openish = sum(1 for r in results if r.status in ("open", "open|filtered"))
        return StageOutcome(results, count=openish,
                            note=f"{openish} UDP service(s) responded/exposed")

    async def run_exposure(ctx: CampaignContext) -> StageOutcome:
        # Vantage exposure = which ports are reachable FROM HERE. With one probe we
        # report the reachable set; the manager fuses multiple vantages. This stage
        # summarizes the funnel's own observations rather than re-scanning.
        reachable = {h: ports for h, ports in ctx.open_ports.items() if ports}
        total = sum(len(p) for p in reachable.values())
        marker = ScanResult(
            "exposure_matrix", "campaign", status="observed",
            data={"type": "exposure_matrix",
                  "vantage_reachable": reachable,
                  "exposed_asserted": ctx.options.exposed},
            evidence=f"{total} reachable TCP port(s) across {len(reachable)} host(s) "
                     f"from this vantage")
        return StageOutcome([marker], count=total,
                            note=f"{total} reachable port(s) from this vantage")

    async def run_inventory(ctx: CampaignContext) -> StageOutcome:
        # classify_from_results reads os_guess / open ports / services straight off
        # the ScanResult facts we already collected — no re-scanning.
        from .device_classifier import classify_from_results
        classified = 0
        results: list[ScanResult] = []
        for h in ctx.live_hosts:
            host_facts = [r for r in ctx.facts if r.target == h]
            try:
                verdict = classify_from_results(host_facts)
            except Exception as exc:
                LOG.debug("classify %s failed: %s", h, exc)
                continue
            classified += 1
            results.append(ScanResult(
                "device_classifier", h, status="observed",
                data={"type": "device_classification", **verdict},
                evidence=f"{verdict.get('device_type', 'device')} "
                         f"(confidence {verdict.get('confidence', 'n/a')})"))
        return StageOutcome(results, count=classified,
                            note=f"classified {classified} device(s)")

    async def run_detect(ctx: CampaignContext) -> StageOutcome:
        # The deterministic "condition" layer. Every fact already collected is run
        # through the weakness-detection rule engine (findings.py) — the SAME rules
        # run_all applies locally: weak/legacy TLS, SMBv1 / no-signing / null-session,
        # weak-SSH / Terrapin, anonymous FTP/LDAP, no-auth VNC, IPMI cipher-0, RDP
        # without NLA, missing web-security headers, exposed UDP amplifiers, plus the
        # cross-fact attack-path correlations. Offline, no DB, always on.
        #
        # This turns raw facts into RANKED, actionable weakness findings — it does
        # NOT assert a CVE (that stays the opt-in --vuln-db stage / the manager side),
        # so it holds the "probe never emits a CVE claim" line while still answering
        # "what did we actually detect".
        from .findings import run_findings, summarize
        findings = run_findings(ctx.facts)
        summ = summarize(findings)
        results = [ScanResult("findings", f.target or "campaign",
                              port=f.port, status="observed",
                              data=f.to_dict(), evidence=f.evidence)
                   for f in findings]
        sev = summ["by_severity"]
        return StageOutcome(results, count=summ["total"],
                            note=f"{summ['total']} weakness finding(s), "
                                 f"{summ['actionable']} actionable "
                                 f"({sev.get('critical', 0)} critical, "
                                 f"{sev.get('high', 0)} high)")

    async def run_cve(ctx: CampaignContext) -> StageOutcome:
        from cve.vulndb import VulnDB
        from cve.correlator import correlate, summarize, mirror_age_note
        from cve.weakness_map import correlate_weaknesses
        db_path = Path(ctx.options.vuln_db)
        if not db_path.exists():
            return StageOutcome([], 0, f"vuln-db {db_path} not found — skipped")
        db = VulnDB(str(db_path))
        try:
            age = mirror_age_note(db)
            exposed = set(ctx.live_hosts) if ctx.options.exposed else set()
            # Two complementary routes to a CVE off the same fact stream:
            #  (1) correlate() — version-range CPE matches on service banners;
            #  (2) correlate_weaknesses() — the curated weakness->canonical-CVE map
            #      (SMBv1->EternalBlue, Terrapin, ...) driven by the detect stage's
            #      findings, which already landed in ctx.facts (detect runs first).
            # Both accept objects with .to_json() (ScanResult qualifies).
            cpe = correlate(ctx.facts, db, exposed_targets=exposed)
            weak = correlate_weaknesses(ctx.facts, db, exposed_targets=exposed)
            # Dedup across routes by (cve_id, target, port); pre-sorted, so the
            # higher-risk hit wins the slot.
            seen, findings = set(), []
            for f in sorted(cpe + weak, key=lambda x: x.risk_score, reverse=True):
                key = (f.cve_id, f.target, f.port)
                if key not in seen:
                    seen.add(key)
                    findings.append(f)
        finally:
            db.close()
        summ = summarize(findings)
        results = [ScanResult("cve_correlator", f.target or "campaign",
                              port=f.port, status="observed",
                              data=f.to_dict(), evidence=f.evidence)
                   for f in findings]
        return StageOutcome(results, count=summ["total"],
                            note=f"{summ['total']} CVE candidate(s), "
                                 f"{summ['kev']} KEV ({len(weak)} via weakness map) — {age}")

    return [
        Stage("discovery",  "Host & Network Discovery",
              STAGE_CATALOG[0]["detail"], run_discovery),
        Stage("port_map",   "Port & Service Mapping",
              STAGE_CATALOG[1]["detail"], run_port_map,
              gate=lambda c: bool(c.live_hosts)),
        Stage("assessment", "Service & Deep Assessment",
              STAGE_CATALOG[2]["detail"], run_assessment,
              gate=lambda c: any(c.open_ports.values())),
        Stage("udp_snmp",   "SNMP & UDP / Amplification Exposure",
              STAGE_CATALOG[3]["detail"], run_udp_snmp,
              enabled=lambda o: o.udp,
              gate=lambda c: bool(c.live_hosts)),
        Stage("full_port",  "Full-Port Audit (all 65,535)",
              STAGE_CATALOG[4]["detail"], run_full_port,
              enabled=lambda o: o.full_ports,
              gate=lambda c: bool(c.live_hosts)),
        Stage("exposure",   "Internet-Exposure Mapping",
              STAGE_CATALOG[5]["detail"], run_exposure,
              gate=lambda c: bool(c.live_hosts)),
        Stage("inventory",  "Device Inventory & Classification",
              STAGE_CATALOG[6]["detail"], run_inventory,
              gate=lambda c: bool(c.live_hosts)),
        Stage("detect",     "Weakness & Vulnerability Detection",
              STAGE_CATALOG[7]["detail"], run_detect,
              gate=lambda c: bool(c.facts)),
        Stage("cve",        "CVE Correlation",
              STAGE_CATALOG[8]["detail"], run_cve,
              enabled=lambda o: bool(o.vuln_db)),
    ]


# ── public entrypoint ─────────────────────────────────────────────────────────
def build_campaign(targets: list[str], scope: ScopeGuard, options: CampaignOptions,
                   *, campaign_id: str = "va", stages: list[Stage] | None = None,
                   progress_cb: Callable[[dict], None] | None = None,
                   ) -> tuple[VACampaign, ProgressReporter]:
    """Wire a campaign with the real scanners (or injected stages for tests)."""
    funnel = build_default_funnel(
        scope, rate=options.rate, concurrency=options.concurrency,
        timeout=options.timeout, force=options.force, with_udp=options.udp)
    stages = stages if stages is not None else default_stages(funnel)
    out_path = None
    if options.out_dir:
        out_path = Path(options.out_dir) / "campaign_progress.json"
    reporter = ProgressReporter(campaign_id, targets, stages, options,
                                out_path=out_path, callback=progress_cb)
    ctx = CampaignContext(targets=targets, scope=scope, options=options,
                          reporter=reporter)
    return VACampaign(ctx, stages), reporter


async def run_campaign(targets: list[str], scope: ScopeGuard,
                       options: CampaignOptions, *, campaign_id: str = "va",
                       progress_cb: Callable[[dict], None] | None = None,
                       ) -> dict[str, Any]:
    campaign, _ = build_campaign(targets, scope, options,
                                 campaign_id=campaign_id, progress_cb=progress_cb)
    return await campaign.run()


# ── CLI live progress view ────────────────────────────────────────────────────
class CliProgressView:
    """Renders campaign progress to a stream. On a TTY it re-draws one live block
    in place; when piped it prints a concise line per stage TRANSITION so a log
    file stays readable. Wired as the campaign's progress callback."""

    _ICON = {"pending": "·", "running": "▶", "done": "✓",
             "skipped": "–", "error": "✗"}

    def __init__(self, stream=None):
        self.stream = stream if stream is not None else sys.stderr
        self.tty = hasattr(self.stream, "isatty") and self.stream.isatty()
        self._last_status: dict[str, str] = {}
        self._lines_drawn = 0

    def __call__(self, snap: dict) -> None:
        if self.tty:
            self._redraw(snap)
        else:
            self._transitions(snap)

    def _redraw(self, snap: dict) -> None:
        lines = self._format(snap)
        if self._lines_drawn:
            self.stream.write(f"\x1b[{self._lines_drawn}A")   # cursor up
        for ln in lines:
            self.stream.write("\x1b[2K" + ln + "\n")           # clear + write
        self.stream.flush()
        self._lines_drawn = len(lines)

    def _transitions(self, snap: dict) -> None:
        for st in snap["stages"]:
            prev = self._last_status.get(st["id"])
            if prev != st["status"] and st["status"] in (
                    "running", "done", "skipped", "error"):
                note = f" — {st['note']}" if st["note"] else ""
                self.stream.write(
                    f"[{snap['percent']:3d}%] {self._ICON.get(st['status'], '?')} "
                    f"{st['name']}: {st['status']}{note}\n")
            self._last_status[st["id"]] = st["status"]
        self.stream.flush()

    def _format(self, snap: dict) -> list[str]:
        eta = f"  eta {snap['eta_seconds']}s" if snap.get("eta_seconds") else ""
        head = (f"campaign {snap['campaign_id']}  [{snap['status']}]  "
                f"{snap['percent']}%{eta}")
        lines = [head]
        for st in snap["stages"]:
            icon = self._ICON.get(st["status"], "?")
            note = f"  — {st['note']}" if st["note"] else ""
            lines.append(f"  {icon} {st['name']:<44}{note}")
        t = snap.get("totals") or {}
        if t:
            lines.append(f"  totals: {t.get('live_hosts', 0)} live · "
                         f"{t.get('open_ports', 0)} open ports · "
                         f"{t.get('facts', 0)} facts")
        return lines


# ── standalone CLI (background-runnable: `python -m scanner.va_campaign ...`) ──
def main() -> None:
    parser = base_argparser(
        "Sequential Network Vulnerability-Assessment campaign: discovery → "
        "deep assessment → SNMP/UDP → exposure → inventory → weakness detection "
        "→ CVE, with live progress you can watch or stream to the manager.")
    parser.add_argument("--full-ports", action="store_true",
                        help="opt-in: audit ALL 65,535 TCP ports (slow; default "
                             "scans the curated service-port set)")
    parser.add_argument("--no-udp", action="store_true",
                        help="skip the SNMP / UDP amplification-exposure stage")
    parser.add_argument("--vuln-db",
                        help="offline CVE mirror (SQLite) to correlate facts "
                             "against; enables the CVE-correlation stage")
    parser.add_argument("--exposed", action="store_true",
                        help="assert the targets are internet-facing (raises the "
                             "exposed weighting in CVE risk scoring)")
    parser.add_argument("--force", action="store_true",
                        help="assess hosts even if discovery marks them down")
    parser.add_argument("--out-dir", default=".",
                        help="directory for campaign_progress.json + results.jsonl "
                             "+ findings.jsonl (default: current directory)")
    parser.add_argument("--campaign-id", default="va",
                        help="identifier stamped into the progress output")
    parser.add_argument("--quiet", action="store_true",
                        help="suppress the live progress view (JSON summary still "
                             "prints to stdout)")
    args = parser.parse_args()
    setup_logging(args.verbose)

    async def _run():
        scope = ScopeGuard.from_file(args.scope)
        targets = expand_targets(args.targets)
        options = CampaignOptions(
            rate=args.rate, concurrency=args.concurrency, timeout=args.timeout,
            full_ports=args.full_ports, udp=not args.no_udp,
            vuln_db=args.vuln_db, exposed=args.exposed, force=args.force,
            out_dir=args.out_dir)
        view = None if args.quiet else CliProgressView()
        campaign, _ = build_campaign(targets, scope, options,
                                     campaign_id=args.campaign_id, progress_cb=view)
        snap = await campaign.run()

        # Persist every collected fact next to the progress file, so a background
        # run leaves a durable artifact (progress JSON is state; this is evidence).
        # The detect stage's weakness findings live in ctx.facts too (scanner
        # "findings"); split them into their own file so an operator gets a clean,
        # ranked list of what was DETECTED, separate from the raw evidence — the
        # same separation run_all keeps.
        results_path = Path(args.out_dir) / "results.jsonl"
        findings_path = Path(args.out_dir) / "findings.jsonl"
        writer = ResultWriter(str(results_path), also_stdout=False)
        fwriter = ResultWriter(str(findings_path), also_stdout=False)
        try:
            for r in campaign.ctx.facts:
                writer.write(r)
                if r.scanner == "findings":
                    fwriter.write(r)
        finally:
            writer.close()
            fwriter.close()

        # Clean-stdout contract: the machine-readable summary is the only thing on
        # stdout; the live view and logs go to stderr.
        print(json.dumps(snap, default=str))

    main_entrypoint(_run)


if __name__ == "__main__":
    main()
