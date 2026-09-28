"""
engagement_report.py — the client-ready AI report, generated on the backend.

Replaces the Next.js path that called Anthropic directly (bypassing the AI
gateway, the audit chain and sovereign mode). Every model call here goes
through ``ManagerLlmService`` → gateway → audit chain.

What is DETERMINISTIC (computed, never generated):
  * the scorecard (port of frontend lib/prompts/report.ts::buildScorecard)
  * the findings register, refs F-01… (worst first), confidence
  * the remediation roadmap: the fix bundles (app/remediation/bundles.py) with
    their FIX refs, due dates, windows (≤7d immediate · ≤30d · later), effort,
    change risk, asset counts and the findings each resolves

What the model WRITES (narrative only, section by section, fail-soft):
  * per-finding write-ups for the worst N (business impact, technical detail …)
  * per-bundle description/verification wording and dependencies
  * limitations/method, then the verdict + executive summary + board decisions

Validation: any finding ref or FIX ref in model output that was not supplied is
a failed check; that section falls back to its deterministic text and the issue
is reported in ``generation.issues`` — never silently published.
"""
from __future__ import annotations

import asyncio
import math
import re
from datetime import datetime, timedelta
from typing import Any

import structlog

from app.remediation.plan import build_plan
from app.remediation.recipes import resolve_recipe
from app.services.finding_ai import _extract_json

logger = structlog.get_logger()

SEVERITY_WEIGHT = {"critical": 40, "high": 20, "medium": 8, "low": 2, "info": 0}
SEV_RANK = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
DOMAINS = ("network", "authentication", "configuration", "patch_management", "web_application")
MAX_FULL_WRITEUPS = 8
_OPEN = {"open", "confirmed"}
_FIX_REF = re.compile(r"\bFIX-[0-9A-F]{6}\b")
_F_REF = re.compile(r"\bF-\d{2,3}\b")
_WEB_PORTS = {80, 443, 8000, 8080, 8443, 8888}
_AUTH_RECIPES = ("SMB", "RDP", "LDAP", "FTP", "VNC", "SNMP", "DEFAULT-CRED", "IPMI", "RSYNC", "NFS",
                 "DB-UNAUTH", "SMTP-USER")


def _enum(v: Any) -> Any:
    return getattr(v, "value", v)


def _sev(f: Any) -> str:
    s = str(_enum(getattr(f, "severity", "info")) or "info").lower()
    return s if s in SEVERITY_WEIGHT else "info"


def _status(f: Any) -> str:
    return str(_enum(getattr(f, "status", "open")) or "open").lower()


def _kev(ctx: Any) -> bool:
    return bool(ctx.kev)


# ── deterministic scorecard ──────────────────────────────────────────────────

def domain_for(finding: Any, ctx: Any) -> str:
    rid = resolve_recipe(ctx, finding).recipe_id
    port = ctx.port.value if ctx.port.recorded else None
    if rid == "POSTURE-EXPOSED-ADMIN_UI" or (isinstance(port, int) and port in _WEB_PORTS
                                             and rid not in ("CVE-PATCH",) and "TLS" not in rid):
        return "web_application"
    if any(k in rid for k in _AUTH_RECIPES):
        return "authentication"
    if "TLS" in rid or "SSH" in rid or "CLEARTEXT" in rid:
        return "configuration"
    if rid in ("CVE-PATCH", "POSTURE-OS-END-OF-LIFE"):
        return "patch_management"
    return "network"


def build_scorecard(rows: list[dict], previous_overall: int | None = None) -> dict:
    """Weighted open risk saturating toward 100; exploitable findings weigh
    double. Identical to the TypeScript implementation it replaces."""
    open_rows = [r for r in rows if r["status"] in _OPEN]

    def weigh(r: dict) -> float:
        base = SEVERITY_WEIGHT.get(r["severity"], 0)
        exploitable = r["kev"] or r["exploit_validated"] or (r["epss"] or 0) >= 0.5
        return base * 2 if exploitable else base

    def saturate(total: float) -> int:
        # JS Math.round rounds .5 up; Python round() is banker's — match JS.
        return int(math.floor(100 * (1 - math.exp(-total / 120)) + 0.5))

    domains = {}
    for d in DOMAINS:
        in_d = [r for r in open_rows if r["domain"] == d]
        worst = max((r["severity"] for r in in_d), key=lambda s: SEV_RANK[s], default="info")
        domains[d] = {"score": saturate(sum(weigh(r) for r in in_d)), "open": len(in_d), "worst": worst}
    overall = saturate(sum(weigh(r) for r in open_rows))
    delta = None if previous_overall is None else overall - previous_overall
    return {
        "overall": overall,
        "domains": domains,
        "exploitability": {
            "open": len(open_rows),
            "kev": sum(1 for r in open_rows if r["kev"]),
            "validated": sum(1 for r in open_rows if r["exploit_validated"]),
            "epssHigh": sum(1 for r in open_rows if (r["epss"] or 0) >= 0.5),
        },
        "delta": {"overall": delta,
                  "direction": "unknown" if delta is None else "improved" if delta < 0
                  else "worsened" if delta > 0 else "unchanged"},
    }


# ── register ─────────────────────────────────────────────────────────────────

def _confidence(finding: Any) -> str:
    vs = str(getattr(finding, "verification_state", "") or "").lower()
    if getattr(finding, "exploit_validated", False) or vs == "confirmed" or _status(finding) == "confirmed":
        return "confirmed"
    if vs == "corroborated" or getattr(finding, "cve_ids", None) or getattr(finding, "cvss_score", None):
        return "likely"
    return "potential"


def _validation_method(finding: Any, ctx: Any) -> str:
    if getattr(finding, "exploit_validated", False):
        return "Safely validated during testing"
    scanner = ctx.scanner or "the Vedha detection engine"
    return f"Observed by {scanner}"


def build_register(items: list[tuple[Any, Any, dict]]) -> list[dict]:
    """Open findings, worst first, with stable F-refs and scanner facts."""
    rows = []
    for f, ctx, due in items:
        if _status(f) not in _OPEN:
            continue
        rows.append({
            "finding_id": str(f.id), "title": f.title, "severity": _sev(f),
            "confidence": _confidence(f), "validation_method": _validation_method(f, ctx),
            "affected_assets": [f"{ctx.text('host')}:{ctx.port.value}" if ctx.port.recorded else ctx.text("host")],
            "cvss": float(f.cvss_score) if getattr(f, "cvss_score", None) is not None else None,
            "cvss_vector": getattr(f, "cvss_vector", None),
            "epss": ctx.epss, "kev": _kev(ctx), "exploit_validated": bool(getattr(f, "exploit_validated", False)),
            "internet_reachable": True if ctx.exposure == "internet" else False if ctx.exposure == "internal" else None,
            "references": list(ctx.cve_ids),
            "first_seen": (getattr(f, "first_seen", None) or getattr(f, "created_at", None)),
            "due_at": due.get("at") if due else None,
            "remediation_hint": build_plan(f, ctx)["summary"],
            "domain": domain_for(f, ctx), "status": _status(f),
            "_finding": f, "_ctx": ctx,
        })
    rows.sort(key=lambda r: (-SEV_RANK[r["severity"]], -(r["cvss"] or 0), r["title"]))
    for i, r in enumerate(rows, start=1):
        r["ref"] = f"F-{i:02d}"
    return rows


def window_for(due_at: datetime | None, now: datetime) -> str:
    if due_at is None:
        return "90_days"
    if due_at - now <= timedelta(days=7):
        return "immediate"
    if due_at - now <= timedelta(days=30):
        return "30_days"
    return "90_days"


def build_roadmap(bundles: list[dict], register: list[dict], now: datetime) -> list[dict]:
    """The remediation plan = the open fix bundles, deterministic."""
    ref_of = {r["finding_id"]: r["ref"] for r in register}
    plan = []
    for b in bundles:
        if b["status"] != "open":
            continue
        resolves = [ref_of[fid] for fid in b["open_finding_ids"] if fid in ref_of]
        if not resolves:
            continue
        plan.append({
            "fix_id": b["ref"], "fix_key": b["fix_key"], "title": b["title"],
            "description": f"{b['title']}. Target: {b['target_state']}.",
            "window": window_for(b["due_at"], now), "due_at": b["due_at"], "due_source": b["due_source"],
            "effort": b["effort"], "change_risk": b["remediation_risk"], "resolves": resolves,
            "asset_count": sum(1 for h in b["hosts"] if h["status"] in ("open", "extension_approved")),
            "verification": f"{b['verification_check']['check']} — expected: {b['verification_check']['expected']}",
            "remediation_type": b["remediation_type"], "urgency": b["urgency"], "depends_on": [],
        })
    order = {"immediate": 0, "30_days": 1, "90_days": 2}
    plan.sort(key=lambda g: (order[g["window"]], -len(g["resolves"]), g["fix_id"]))
    return plan


# ── model sections ───────────────────────────────────────────────────────────

_SHARED = ("Use only the supplied data. Never introduce a CVE, score, version, host, port, date, "
           "control id or reference that is not in the input. Match each finding's confidence: "
           "'confirmed' may be stated as fact; 'likely' needs validation wording; 'potential' is an "
           "untested possibility. Plain English; explain a technical term the first time it appears. "
           "Never give operational attack instructions or destructive commands.")

SECTIONS: dict[str, tuple[str, int]] = {
    "finding_writeup": (
        _SHARED + "\nWrite the report entry for ONE finding. Return JSON: {\"ref\": as supplied, "
        "\"business_impact\": 2-3 sentences for an executive, \"technical_detail\": 3-5 sentences for an "
        "engineer including one limiting factor, \"evidence_summary\": from supplied evidence only, "
        "\"severity_rationale\": 1-2 sentences from the supplied signals, \"severity_flag\": a sentence if "
        "the severity looks inconsistent with the signals else null, \"remediation_detail\": specific and "
        "non-destructive, based on the supplied plan, \"verification\": observable and covering all "
        "assets}.", 1400),
    "roadmap": (
        _SHARED + "\nThe fix bundles, their FIX refs, windows and due dates are already decided — do not "
        "change, merge, split or re-order them. For each bundle write the wording an engineer is assigned. "
        "Return JSON: {\"groups\": [{\"fix_id\": as supplied, \"description\": what to change and what "
        "actually costs time (2-3 sentences), \"verification\": how to confirm across all its assets, "
        "\"depends_on\": [FIX refs that must complete first, only from the supplied list]}], "
        "\"immediate_window_empty_reason\": a sentence if no bundle is in the immediate window, else null}.",
        2000),
    "limitations": (
        _SHARED + "\nWrite the method and limitations for an auditor reading this a year from now. Return "
        "JSON: {\"method\": 2-3 sentences on what was tested, how and when (only supplied facts), "
        "\"limitations\": [3-6 statements of what the reader must NOT conclude; always include the scope "
        "boundary and that absence of a finding on an untested asset is not evidence it is secure]}.", 900),
    "verdict_and_summary": (
        _SHARED + "\nWrite for a board member with sixty seconds. Return JSON: {\"verdict\": one sentence, "
        "at most 15 words, stating the position (what an attacker can do + what they cannot), "
        "\"summary\": 3-5 sentences of prose covering the overall position, what an attacker could achieve, "
        "the change since last time only if a delta is supplied, and what separates urgent from the rest; "
        "name at least one thing that is contained, \"decisions\": [2-4 {\"horizon\": \"this_week\"|"
        "\"this_month\"|\"this_quarter\", \"ask\": the decision (not a task), \"rationale\": why it needs a "
        "decision and what it costs, \"fix_ids\": FIX refs from the supplied roadmap}]}. Every number must "
        "appear in the input.", 1100),
}


def _refs_ok(obj: Any, allowed_fix: set[str], allowed_f: set[str]) -> list[str]:
    text = str(obj)
    bad = sorted({m for m in _FIX_REF.findall(text) if m not in allowed_fix}
                 | {m for m in _F_REF.findall(text) if m not in allowed_f})
    return bad


class _Runner:
    def __init__(self, svc: Any, brief: str | None):
        self.svc = svc
        self.brief = brief
        self.status: dict[str, str] = {}
        self.issues: list[str] = []
        self.runtime: Any = None

    async def run(self, name: str, key: str, payload: dict) -> dict | None:
        from app.schemas.ai import AiGenerateRequest, AiMessage
        from app.services.llm import AiRuntimeError
        instructions, max_tokens = SECTIONS[key]
        req = AiGenerateRequest(task="engagement_report",
                                messages=[AiMessage(role="user", content=instructions)],
                                context={"section": key, **payload}, max_tokens=max_tokens)
        try:
            text, runtime, _fallback = await self.svc.generate_with_fallback(req, domain_brief=self.brief)
        except AiRuntimeError as exc:
            self.status[name] = "fallback"
            self.issues.append(f"{name}: model unavailable ({exc})")
            if getattr(exc, "status_code", None) == 503 and self.runtime is None:
                raise
            return None
        self.runtime = self.runtime or runtime
        parsed = _extract_json(text or "")
        if parsed is None:
            self.status[name] = "fallback"
            self.issues.append(f"{name}: output was not valid JSON")
            return None
        self.status[name] = "ok"
        return parsed


def _writeup_payload(r: dict, compliance: list[dict]) -> dict:
    plan = build_plan(r["_finding"], r["_ctx"])
    ev = r["_finding"].evidence if isinstance(getattr(r["_finding"], "evidence", None), dict) else {}
    return {"finding": {k: r[k] for k in ("ref", "title", "severity", "confidence", "validation_method",
                                          "affected_assets", "cvss", "cvss_vector", "epss", "kev",
                                          "exploit_validated", "internet_reachable", "references")},
            "evidence": {k: ev.get(k) for k in ("scanner", "rule_id", "port", "banner", "evidence",
                                                "matched_version", "fixed_version") if ev.get(k) is not None},
            "plan": {"target_state": plan["target_state"], "steps": [s["title"] for s in plan["steps"]],
                     "verification": plan["verification_check"]},
            "compliance": compliance}


def _fallback_writeup(r: dict) -> dict:
    plan = build_plan(r["_finding"], r["_ctx"])
    return {"business_impact": "", "technical_detail": "", "evidence_summary": "",
            "severity_rationale": f"Severity {r['severity']} as recorded by the scanner.",
            "severity_flag": None, "remediation_detail": plan["summary"],
            "verification": f"{plan['verification_check']['check']} — expected: "
                            f"{plan['verification_check']['expected']}"}


def _public_finding(r: dict, w: dict | None, full: bool) -> dict:
    # "status" is published: the report shows each finding's lifecycle state.
    out = {k: v for k, v in r.items() if not k.startswith("_") and k not in ("domain", "remediation_hint")}
    out["first_seen"] = r["first_seen"].isoformat() if isinstance(r["first_seen"], datetime) else r["first_seen"]
    out["due_at"] = r["due_at"].isoformat() if isinstance(r["due_at"], datetime) else r["due_at"]
    base = _fallback_writeup(r)
    w = w or {}
    for key in ("business_impact", "technical_detail", "evidence_summary", "severity_rationale",
                "remediation_detail", "verification"):
        val = w.get(key)
        out[key] = str(val).strip() if full and isinstance(val, str) and val.strip() else (base[key] if full else "")
    if not full:
        out["remediation_detail"] = r["remediation_hint"]
    out["severity_flag"] = w.get("severity_flag") if full and isinstance(w.get("severity_flag"), str) else None
    out["compliance_refs"] = []
    return out


async def generate_engagement_report(db: Any, *, engagement: Any, tenant_id: Any, actor_id: Any,
                                     svc: Any = None, now: datetime | None = None) -> dict:
    """Build the report. Raises AiRuntimeError(503) when no provider can serve."""
    from app.ai.audit_chain import persist_ai_calls
    from app.remediation import service as remediation_service
    from app.services.domain_context import domain_brief_for
    from app.services.finding_compliance import compliance_for
    from app.services.llm import ManagerLlmService
    from app.services.project_time import project_now

    now = now or project_now()
    data = await remediation_service.engagement_bundles(db, engagement, tenant_id)
    register = build_register(data["items"])
    roadmap = build_roadmap(data["bundles"], register, now)
    scorecard = build_scorecard(register)
    allowed_fix = {g["fix_id"] for g in roadmap}
    allowed_f = {r["ref"] for r in register}

    svc = svc or ManagerLlmService()
    brief = await domain_brief_for(db, engagement, [r["_finding"] for r in register[:10]])
    runner = _Runner(svc, brief.text if brief else None)

    top = register[:MAX_FULL_WRITEUPS]
    # Model calls only — the shared AsyncSession is never touched inside gather.
    writeups = await asyncio.gather(*[
        runner.run(f"finding:{r['ref']}", "finding_writeup",
                   _writeup_payload(r, [{"framework": c["framework"], "controls": c["controls"]}
                                        for c in compliance_for(r["_finding"])]))
        for r in top])
    checked = []
    for r, w in zip(top, writeups):
        bad = _refs_ok(w, allowed_fix, allowed_f) if w else []
        if w and (bad or (w.get("ref") not in (None, r["ref"]))):
            runner.issues.append(f"finding:{r['ref']}: unknown refs {bad or [w.get('ref')]}")
            runner.status[f"finding:{r['ref']}"] = "fallback"
            w = None
        checked.append(w)

    findings = [_public_finding(r, checked[i], True) for i, r in enumerate(top)]
    findings += [_public_finding(r, None, False) for r in register[MAX_FULL_WRITEUPS:]]

    road_payload = {"roadmap": [{k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in g.items()}
                                for g in roadmap],
                    "findings": [{"ref": r["ref"], "title": r["title"], "severity": r["severity"]}
                                 for r in register]}
    road = await runner.run("roadmap", "roadmap", road_payload) if roadmap else None
    empty_reason = None
    if road:
        bad = _refs_ok(road, allowed_fix, allowed_f)
        if bad:
            runner.issues.append(f"roadmap: unknown refs {bad}")
            runner.status["roadmap"] = "fallback"
        else:
            by_id = {g["fix_id"]: g for g in roadmap}
            for item in road.get("groups") or []:
                g = by_id.get(item.get("fix_id")) if isinstance(item, dict) else None
                if g is None:
                    continue
                if isinstance(item.get("description"), str) and item["description"].strip():
                    g["description"] = item["description"].strip()
                if isinstance(item.get("verification"), str) and item["verification"].strip():
                    g["verification"] = item["verification"].strip()
                g["depends_on"] = [d for d in (item.get("depends_on") or [])
                                   if d in allowed_fix and d != g["fix_id"]]
            if isinstance(road.get("immediate_window_empty_reason"), str):
                empty_reason = road["immediate_window_empty_reason"]
    if not any(g["window"] == "immediate" for g in roadmap) and not empty_reason:
        empty_reason = "No fix is due within the next seven days under the configured SLA policy."

    def _when(v: Any) -> str:
        return v.isoformat() if isinstance(v, datetime) else "Not recorded"
    lim = await runner.run("limitations", "limitations", {
        "engagement": {"name": engagement.name,
                       "scope": list(getattr(engagement, "scope_cidrs", None) or []),
                       "excluded": list(getattr(engagement, "excluded_cidrs", None) or []),
                       "start": _when(getattr(engagement, "start_time", None)),
                       "end": _when(getattr(engagement, "end_time", None))},
        "counts": {"open_findings": len(register), "hosts": len({h['ip'] for b in data['bundles'] for h in b['hosts']}),
                   "low_confidence": sum(1 for r in register if r["confidence"] != "confirmed")}})
    method = (lim or {}).get("method") if isinstance((lim or {}).get("method"), str) else ""
    limitations = [str(x) for x in (lim or {}).get("limitations") or [] if str(x).strip()] or [
        "Findings reflect only the assets and services within the authorised scope at the time of testing.",
        "Absence of a finding on an asset that was not tested is not evidence that the asset is secure.",
    ]

    counts = {s: sum(1 for r in register if r["severity"] == s) for s in ("critical", "high", "medium", "low")}
    vs = await runner.run("verdict_and_summary", "verdict_and_summary", {
        "engagement": {"name": engagement.name}, "scorecard": scorecard, "severity_counts": counts,
        "roadmap": [{"fix_id": g["fix_id"], "title": g["title"], "window": g["window"], "effort": g["effort"],
                     "change_risk": g["change_risk"], "asset_count": g["asset_count"],
                     "resolves": g["resolves"]} for g in roadmap]})
    decisions = []
    verdict, summary = "", ""
    if vs:
        bad = _refs_ok(vs, allowed_fix, allowed_f)
        if bad:
            runner.issues.append(f"verdict_and_summary: unknown refs {bad}")
            runner.status["verdict_and_summary"] = "fallback"
        else:
            verdict = str(vs.get("verdict") or "").strip()
            summary = str(vs.get("summary") or "").strip()
            for d in vs.get("decisions") or []:
                if isinstance(d, dict) and d.get("ask"):
                    decisions.append({"horizon": d.get("horizon") if d.get("horizon") in
                                      ("this_week", "this_month", "this_quarter") else "this_quarter",
                                      "ask": str(d["ask"]), "rationale": str(d.get("rationale") or ""),
                                      "fix_ids": [x for x in d.get("fix_ids") or [] if x in allowed_fix]})
            if len(verdict.split()) > 15:
                runner.issues.append("verdict exceeds 15 words")

    await persist_ai_calls(db, list(getattr(svc, "audit_records", None) or []),
                           actor_id=actor_id, engagement_id=engagement.id)

    roadmap_out = [{k: (v.isoformat() if isinstance(v, datetime) else v) for k, v in g.items()}
                   for g in roadmap]
    return {
        "verdict": verdict,
        "executive_summary": summary,
        "decisions": decisions,
        "attack_narrative": None,          # no connected chain is supplied → never invented
        "cheapest_break": None,
        "preconditions": [],
        "findings": findings,
        "findings_detailed": len(top),
        "remediation_plan": roadmap_out,
        "immediate_window_empty_reason": empty_reason,
        "controls": [],
        "controls_observed": ["No controls were specifically evidenced as effective within the tested scope."],
        "limitations": limitations,
        "method": method,
        "scorecard": scorecard,
        "generation": {
            "provider": getattr(runner.runtime, "provider", None), "model": getattr(runner.runtime, "model", None),
            "sections": runner.status, "issues": runner.issues, "sla_source": data["sla_source"],
            "generated_at": now.isoformat(),
        },
    }
