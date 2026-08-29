"""
test_va_campaign.py — the VA-campaign orchestrator (scanner/va_campaign.py).

These tests exercise the ENGINE and the PROGRESS CONTRACT with dependency-injected
fake stages, so they run with zero network and are fully deterministic. The real
stage runners just compose the package's already-tested scanners; what is unique
to this module — sequencing, gating, opt-in skipping, percent/ETA math, and the
JSON progress shape the manager frontend consumes — is what we pin here.
"""
import asyncio
import ipaddress
import json

from scanner import va_campaign as vc
from scanner.va_campaign import (
    CampaignOptions, CampaignContext, Stage, StageOutcome, VACampaign,
    ProgressReporter, CliProgressView, STAGE_CATALOG, build_campaign,
)
from scanner.scanner_base import ScopeGuard, ScanResult


def _scope():
    return ScopeGuard([ipaddress.ip_network("10.0.0.0/24")], set())


def _reporter(stages, options, **kw):
    return ProgressReporter("t", ["10.0.0.5"], stages, options, **kw)


def _run(stages, options=None, targets=None):
    # Existing async scanners are tested with asyncio.run() inside sync tests
    # (see test_scan_funnel.py) — mirror that convention, no marker needed.
    options = options or CampaignOptions()
    targets = targets or ["10.0.0.5", "10.0.0.6"]
    camp, rep = build_campaign(targets, _scope(), options, stages=stages)
    return asyncio.run(camp.run())


# ── stage sequencing / gating / opt-in ────────────────────────────────────────
def test_stages_run_in_order_and_thread_context():
    order = []

    async def disc(ctx):
        order.append("d")
        ctx.live_hosts = ["10.0.0.5"]
        return StageOutcome([], 1, "1 live")

    async def ports(ctx):
        order.append("p")
        assert ctx.live_hosts == ["10.0.0.5"]      # discovery ran first
        ctx.open_ports = {"10.0.0.5": [22]}
        return StageOutcome([], 1, "1 open")

    stages = [
        Stage("discovery", "D", "d", disc),
        Stage("port_map", "P", "p", ports, gate=lambda c: bool(c.live_hosts)),
    ]
    snap = _run(stages)
    assert order == ["d", "p"]
    assert snap["status"] == "completed"
    assert [s["status"] for s in snap["stages"]] == ["done", "done"]


def test_gate_not_met_skips_stage():
    async def disc(ctx):
        return StageOutcome([], 0, "0 live")        # no live hosts

    async def ports(ctx):
        raise AssertionError("must not run — gate is unmet")

    stages = [
        Stage("discovery", "D", "d", disc),
        Stage("port_map", "P", "p", ports, gate=lambda c: bool(c.live_hosts)),
    ]
    snap = _run(stages)
    assert snap["stages"][1]["status"] == "skipped"
    assert "prerequisite" in snap["stages"][1]["note"]


def test_disabled_opt_in_stage_is_skipped_and_excluded_from_percent():
    async def disc(ctx):
        ctx.live_hosts = ["10.0.0.5"]
        return StageOutcome([], 1, "")

    async def full(ctx):
        raise AssertionError("opt-in disabled — must not run")

    stages = [
        Stage("discovery", "D", "d", disc),
        Stage("full_port", "F", "f", full, enabled=lambda o: o.full_ports),
    ]
    # full_ports defaults False → full_port disabled → 1 active stage → 100%.
    snap = _run(stages, CampaignOptions(full_ports=False))
    fp = next(s for s in snap["stages"] if s["id"] == "full_port")
    assert fp["status"] == "skipped"
    assert snap["percent"] == 100


def test_enabled_opt_in_stage_runs():
    ran = []

    async def disc(ctx):
        ctx.live_hosts = ["10.0.0.5"]
        return StageOutcome([], 1, "")

    async def full(ctx):
        ran.append(True)
        return StageOutcome([], 65535, "full")

    stages = [
        Stage("discovery", "D", "d", disc),
        Stage("full_port", "F", "f", full, enabled=lambda o: o.full_ports),
    ]
    snap = _run(stages, CampaignOptions(full_ports=True))
    assert ran == [True]
    assert next(s for s in snap["stages"] if s["id"] == "full_port")["status"] == "done"


def test_stage_error_is_isolated_not_fatal():
    async def boom(ctx):
        raise RuntimeError("scanner blew up")

    async def after(ctx):
        return StageOutcome([], 1, "still ran")

    stages = [
        Stage("discovery", "D", "d", boom),
        Stage("inventory", "I", "i", after),
    ]
    snap = _run(stages)
    assert snap["stages"][0]["status"] == "error"
    assert "RuntimeError" in snap["stages"][0]["note"]
    assert snap["stages"][1]["status"] == "done"    # campaign continued
    assert snap["status"] == "completed"


def test_facts_accumulate_into_totals():
    async def disc(ctx):
        ctx.live_hosts = ["10.0.0.5", "10.0.0.6"]
        return StageOutcome([ScanResult("host_discovery", "10.0.0.5",
                                        data={"alive": True})], 2, "")

    async def ports(ctx):
        ctx.open_ports = {"10.0.0.5": [22, 443], "10.0.0.6": []}
        return StageOutcome([ScanResult("syn_scanner", "10.0.0.5", port=22,
                                        status="open", proto="tcp")], 2, "")

    stages = [
        Stage("discovery", "D", "d", disc),
        Stage("port_map", "P", "p", ports, gate=lambda c: bool(c.live_hosts)),
    ]
    snap = _run(stages)
    assert snap["totals"]["live_hosts"] == 2
    assert snap["totals"]["open_ports"] == 2
    assert snap["totals"]["facts"] == 2


# ── progress contract shape ───────────────────────────────────────────────────
def test_progress_snapshot_shape():
    opts = CampaignOptions()
    stages = [Stage("discovery", "Discovery", "d", None)]
    rep = _reporter(stages, opts)
    snap = rep.snapshot()
    for key in ("campaign_id", "targets", "status", "started_at", "updated_at",
                "percent", "current_stage", "eta_seconds", "stages", "totals"):
        assert key in snap, key
    st = snap["stages"][0]
    for key in ("id", "name", "detail", "status", "started_at", "ended_at",
                "count", "note"):
        assert key in st, key
    # JSON-serializable (this is what gets written / streamed).
    json.dumps(snap)


def test_percent_and_current_stage_transitions():
    opts = CampaignOptions()
    stages = [Stage(i, i.upper(), "", None) for i in ("a", "b", "c", "d")]
    rep = _reporter(stages, opts)
    assert rep.snapshot()["percent"] == 0
    rep.mark("a", "running")
    assert rep.snapshot()["current_stage"] == "a"
    rep.mark("a", "done", count=3, note="ok")
    assert rep.snapshot()["percent"] == 25       # 1 of 4 terminal
    rep.mark("b", "done")
    rep.mark("c", "skipped")
    assert rep.snapshot()["percent"] == 75       # 3 of 4 terminal (skipped counts)
    rep.mark("d", "done")
    rep.finish()
    final = rep.snapshot()
    assert final["percent"] == 100
    assert final["status"] == "completed"
    assert final["current_stage"] is None


def test_progress_file_written_atomically(tmp_path):
    opts = CampaignOptions(out_dir=str(tmp_path))
    stages = [Stage("discovery", "Discovery", "d", None)]
    out = tmp_path / "campaign_progress.json"
    rep = ProgressReporter("t", ["10.0.0.5"], stages, opts,
                           out_path=out)
    assert out.exists()                          # written on construction
    rep.mark("discovery", "done", count=1, note="1 live")
    data = json.loads(out.read_text())
    assert data["stages"][0]["status"] == "done"
    assert data["stages"][0]["count"] == 1
    # no leftover temp file
    assert not (tmp_path / "campaign_progress.json.tmp").exists()


def test_callback_error_never_breaks_reporting():
    def bad_cb(_snap):
        raise ValueError("sink is down")

    opts = CampaignOptions()
    stages = [Stage("discovery", "Discovery", "d", None)]
    # Must not raise despite the callback throwing on every flush.
    rep = ProgressReporter("t", ["10.0.0.5"], stages, opts, callback=bad_cb)
    rep.mark("discovery", "done")


# ── stage catalog integrity ───────────────────────────────────────────────────
def test_catalog_ids_are_unique_and_match_default_stages():
    ids = [s["id"] for s in STAGE_CATALOG]
    assert len(ids) == len(set(ids)), "duplicate stage id in STAGE_CATALOG"

    # default_stages must cover exactly the catalog, in the same order.
    from scanner.scan_funnel import build_default_funnel
    funnel = build_default_funnel(_scope())
    stage_ids = [s.id for s in vc.default_stages(funnel)]
    assert stage_ids == ids


def test_capability_list_covers_the_user_requested_set():
    ids = {s["id"] for s in STAGE_CATALOG}
    # The capabilities the campaign was asked to deliver.
    for required in ("discovery", "assessment", "udp_snmp", "full_port",
                     "exposure", "inventory", "detect", "cve"):
        assert required in ids, required


# ── the real detect stage: facts → deterministic weakness findings ────────────
def _detect_stage():
    # Grab the REAL detect Stage out of default_stages (not a fake) so the wiring —
    # gate, run_detect, findings.py integration — is what gets exercised.
    from scanner.scan_funnel import build_default_funnel
    funnel = build_default_funnel(_scope())
    return next(s for s in vc.default_stages(funnel) if s.id == "detect")


def test_detect_stage_turns_facts_into_weakness_findings():
    # A single collected fact that a findings.py rule fires on (SMBv1 enabled).
    smb = ScanResult("smb_scan", "10.0.0.5", port=445, proto="tcp",
                     status="open", data={"smbv1_enabled": True})

    async def disc(ctx):
        ctx.live_hosts = ["10.0.0.5"]
        return StageOutcome([smb], 1, "1 live")     # fact lands in ctx.facts

    camp, _rep = build_campaign(
        ["10.0.0.5"], _scope(), CampaignOptions(),
        stages=[Stage("discovery", "D", "d", disc), _detect_stage()])
    snap = asyncio.run(camp.run())

    d = next(s for s in snap["stages"] if s["id"] == "detect")
    assert d["status"] == "done"
    assert d["count"] >= 1                            # at least the SMBv1 finding
    # the finding is emitted as a first-class fact (scanner "findings") …
    findings = [r for r in camp.ctx.facts if r.scanner == "findings"]
    assert findings, "detect stage emitted no finding facts"
    # … and it is the deterministic weakness we planted, NOT a CVE claim.
    assert "SMB-V1-ENABLED" in {r.data.get("rule_id") for r in findings}


def test_detect_stage_skipped_when_nothing_was_collected():
    async def disc(ctx):
        return StageOutcome([], 0, "0 live")         # no facts at all

    snap = _run([Stage("discovery", "D", "d", disc), _detect_stage()])
    d = next(s for s in snap["stages"] if s["id"] == "detect")
    assert d["status"] == "skipped"                  # gate=bool(ctx.facts) unmet


# ── CLI live view ─────────────────────────────────────────────────────────────
class _Buf:
    def __init__(self):
        self.text = ""

    def write(self, s):
        self.text += s

    def flush(self):
        pass

    def isatty(self):
        return False        # exercise the piped (transitions) path


def test_cli_view_emits_one_line_per_transition():
    buf = _Buf()
    view = CliProgressView(stream=buf)
    view({"campaign_id": "t", "percent": 0, "stages": [
        {"id": "a", "name": "Discovery", "status": "running", "note": ""}]})
    view({"campaign_id": "t", "percent": 100, "stages": [
        {"id": "a", "name": "Discovery", "status": "done", "note": "1 live"}]})
    lines = [ln for ln in buf.text.splitlines() if ln.strip()]
    assert len(lines) == 2
    assert "Discovery: running" in lines[0]
    assert "Discovery: done" in lines[1] and "1 live" in lines[1]


def test_cli_view_deduplicates_unchanged_status():
    buf = _Buf()
    view = CliProgressView(stream=buf)
    snap = {"campaign_id": "t", "percent": 50, "stages": [
        {"id": "a", "name": "D", "status": "running", "note": ""}]}
    view(snap)
    view(snap)          # same status again (e.g. a totals-only flush)
    lines = [ln for ln in buf.text.splitlines() if ln.strip()]
    assert len(lines) == 1      # printed once, not twice


# ── IPv6 discovery wiring (opt-in, scope-gated) ───────────────────────────────
def test_ipv6_discovery_reports_all_scans_only_in_scope(monkeypatch):
    from scanner import ipv6_discovery as d6
    # link-local in scope, global out of scope
    monkeypatch.setattr(d6, "discover_ipv6_hosts",
                        lambda *a, **k: ["fe80::1%en0", "2001:db8::5"])
    scope = ScopeGuard.from_list(["fe80::/10"])
    res = asyncio.run(vc._discover_ipv6(scope))
    assert len(res["facts"]) == 2                       # both REPORTED
    assert {f.target: f.data["in_scope"] for f in res["facts"]} == {
        "fe80::1%en0": True, "2001:db8::5": False}
    assert res["in_scope"] == ["fe80::1%en0"]           # only authorized one SCANNED
    assert all(f.family == "ipv6" and f.scanner == "ipv6_discovery"
               for f in res["facts"])


def test_ipv6_discovery_never_raises(monkeypatch):
    from scanner import ipv6_discovery as d6
    monkeypatch.setattr(d6, "discover_ipv6_hosts",
                        lambda *a, **k: (_ for _ in ()).throw(OSError("no iface")))
    res = asyncio.run(vc._discover_ipv6(ScopeGuard.from_list(["fe80::/10"])))
    assert res == {"facts": [], "in_scope": []}


def test_ipv6_option_default_off():
    from scanner.va_campaign import CampaignOptions
    assert CampaignOptions().ipv6 is False              # opt-in only
