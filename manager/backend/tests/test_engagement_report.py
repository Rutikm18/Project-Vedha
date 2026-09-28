"""test_engagement_report.py — backend AI report: deterministic core, validated narrative."""
from __future__ import annotations

import asyncio
import json
import math
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.ai import engagement_report as ER
from app.models.enums import FindingSeverity, FindingStatus
from app.remediation.context import build_context

NOW = datetime(2026, 9, 27, 12, tzinfo=timezone.utc)


def _row(severity, *, kev=False, validated=False, epss=None, status="open", domain="network"):
    return {"severity": severity, "kev": kev, "exploit_validated": validated, "epss": epss,
            "status": status, "domain": domain}


def _js_round(x):
    return math.floor(x + 0.5)


class TestScorecard:
    def test_matches_the_typescript_formula(self):
        rows = [_row("critical", kev=True), _row("high"), _row("medium", status="remediated")]
        sc = ER.build_scorecard(rows)
        assert sc["overall"] == _js_round(100 * (1 - math.exp(-(80 + 20) / 120)))   # 57
        assert sc["overall"] == 57
        assert sc["exploitability"] == {"open": 2, "kev": 1, "validated": 0, "epssHigh": 0}
        assert sc["delta"] == {"overall": None, "direction": "unknown"}

    def test_domains_and_delta(self):
        rows = [_row("high", epss=0.7, domain="authentication"), _row("low", domain="configuration")]
        sc = ER.build_scorecard(rows, previous_overall=60)
        assert sc["domains"]["authentication"] == {"score": _js_round(100 * (1 - math.exp(-40 / 120))),
                                                   "open": 1, "worst": "high"}
        assert sc["domains"]["web_application"] == {"score": 0, "open": 0, "worst": "info"}
        assert sc["delta"]["direction"] == "improved"

    def test_empty(self):
        assert ER.build_scorecard([])["overall"] == 0


def _asset(i):
    return SimpleNamespace(ip_address=f"10.0.0.{i}", hostname=f"h{i}", fqdn=None, os="Windows",
                           os_version="Windows Server 2019", asset_type=SimpleNamespace(value="server"),
                           criticality=SimpleNamespace(value="high"), environment=None, tags=None)


def _finding(title, severity, evidence, status=FindingStatus.open, cvss=None):
    return SimpleNamespace(id=uuid.uuid4(), title=title, description="", remediation="",
                           severity=FindingSeverity(severity), status=status, evidence=evidence,
                           cve_ids=[], cvss_score=cvss, cvss_vector=None, epss_score=None,
                           exploit_validated=False, verification_state=None,
                           first_seen=NOW - timedelta(days=2), created_at=NOW - timedelta(days=2),
                           resolved_at=None, due_at=None)


def _items():
    smb = [(_finding("SMBv1 enabled", "critical", {"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445}), i)
           for i in (1, 2)]
    tls = [(_finding("TLS 1.0 accepted", "high", {"rule_id": "POSTURE-TLS-DEPRECATED-VERSION", "port": 443}), 3)]
    fixed = [(_finding("Old issue", "high", {"rule_id": "POSTURE-SMB-SIGNING-OFF", "port": 445},
                       status=FindingStatus.remediated), 4)]
    out = []
    for f, i in smb + tls + fixed:
        ctx = build_context(f, _asset(i), None)
        days = 3 if "SMB" in f.title else 20
        out.append((f, ctx, {"at": NOW + timedelta(days=days), "source": "tenant"}))
    return out


class TestRegisterAndRoadmap:
    def test_register_open_only_worst_first(self):
        reg = ER.build_register(_items())
        assert [r["ref"] for r in reg] == ["F-01", "F-02", "F-03"]
        assert [r["severity"] for r in reg] == ["critical", "critical", "high"]
        assert reg[0]["domain"] == "authentication" and reg[2]["domain"] == "configuration"

    def test_roadmap_is_the_bundles_with_windows(self):
        from app.remediation.bundles import build_bundles
        items = _items()
        reg = ER.build_register(items)
        road = ER.build_roadmap(build_bundles(items, now=NOW), reg, NOW)
        assert [g["window"] for g in road] == ["immediate", "30_days"]
        assert road[0]["resolves"] == ["F-01", "F-02"] and road[0]["asset_count"] == 2
        assert road[0]["fix_id"].startswith("FIX-")

    @pytest.mark.parametrize("days,window", [(1, "immediate"), (7, "immediate"), (8, "30_days"),
                                             (31, "90_days")])
    def test_window_for(self, days, window):
        assert ER.window_for(NOW + timedelta(days=days), NOW) == window
        assert ER.window_for(None, NOW) == "90_days"


class _FakeSvc:
    """Stands in for ManagerLlmService: answers per section, records audit rows."""

    def __init__(self, answers):
        self.answers = answers
        self.audit_records = []
        self.calls = []

    async def generate_with_fallback(self, request, *, domain_brief=None):
        section = request.context["section"]
        self.calls.append(section)
        self.audit_records.append({"task": request.task})
        body = self.answers(section, request.context)
        return json.dumps(body), SimpleNamespace(provider="fake", model="fake-1"), False


def _run(answers, monkeypatch):
    from app.remediation import service as RS
    from app.services import domain_context

    async def fake_bundles(db, engagement, tenant_id):
        from app.remediation.bundles import build_bundles
        items = _items()
        return {"bundles": build_bundles(items, now=NOW), "items": items, "sla_source": "tenant"}

    async def no_brief(db, engagement, findings=()):
        return None
    persisted = {}

    async def capture(db, records, *, actor_id, engagement_id):
        persisted["n"] = len(records)
    monkeypatch.setattr(RS, "engagement_bundles", fake_bundles)
    monkeypatch.setattr(domain_context, "domain_brief_for", no_brief)
    monkeypatch.setattr("app.ai.audit_chain.persist_ai_calls", capture)
    svc = _FakeSvc(answers)
    eng = SimpleNamespace(id=uuid.uuid4(), name="Bank VA", scope_cidrs=["10.0.0.0/24"], excluded_cidrs=[],
                          start_time=None, end_time=None, rules_of_engagement={})
    report = asyncio.run(ER.generate_engagement_report(None, engagement=eng, tenant_id=uuid.uuid4(),
                                                       actor_id=uuid.uuid4(), svc=svc, now=NOW))
    return report, svc, persisted


def _good(section, ctx):
    if section == "finding_writeup":
        ref = ctx["finding"]["ref"]
        return {"ref": ref, "business_impact": "An attacker on the LAN could take over the file server.",
                "technical_detail": "SMBv1 negotiation succeeded.", "evidence_summary": "Negotiate accepted NT1.",
                "severity_rationale": "Wormable class.", "severity_flag": None,
                "remediation_detail": "Disable SMBv1.", "verification": "Re-scan port 445."}
    if section == "roadmap":
        first = ctx["roadmap"][0]["fix_id"]
        return {"groups": [{"fix_id": first, "description": "Disable SMBv1 by GPO; audit legacy clients first.",
                            "verification": "smb_scan shows no NT1 on both hosts.", "depends_on": []}],
                "immediate_window_empty_reason": None}
    if section == "limitations":
        return {"method": "Network VA of 10.0.0.0/24.", "limitations": ["Only the listed range was tested."]}
    fix = ctx["roadmap"][0]["fix_id"]
    return {"verdict": "Two file servers can be taken over from the LAN; the web tier is contained.",
            "summary": "Two critical findings share one fix.", "decisions": [
                {"horizon": "this_week", "ask": "Approve an out-of-cycle change window.",
                 "rationale": "Requires a brief SMB outage.", "fix_ids": [fix]}]}


class TestGenerate:
    def test_full_report_shape_and_audit(self, monkeypatch):
        report, svc, persisted = _run(_good, monkeypatch)
        assert report["verdict"].startswith("Two file servers")
        assert report["findings"][0]["business_impact"].startswith("An attacker")
        # Each register entry says its lifecycle state — the report shows it per finding.
        assert {f["status"] for f in report["findings"]} <= {"open", "confirmed"}
        assert all("domain" not in f and "remediation_hint" not in f for f in report["findings"])
        assert report["remediation_plan"][0]["description"].startswith("Disable SMBv1 by GPO")
        assert report["remediation_plan"][0]["window"] == "immediate"
        assert report["decisions"][0]["fix_ids"] == [report["remediation_plan"][0]["fix_id"]]
        assert report["attack_narrative"] is None
        assert report["scorecard"]["overall"] > 0
        assert report["generation"]["issues"] == []
        assert persisted["n"] == len(svc.calls)                   # every call audited
        assert set(svc.calls) == {"finding_writeup", "roadmap", "limitations", "verdict_and_summary"}

    def test_invented_fix_ref_is_rejected_not_published(self, monkeypatch):
        def answers(section, ctx):
            out = _good(section, ctx)
            if section == "verdict_and_summary":
                out["summary"] = "Apply FIX-ABCDEF immediately."
            return out
        report, _svc, _ = _run(answers, monkeypatch)
        assert report["executive_summary"] == "" and report["verdict"] == ""
        assert report["generation"]["sections"]["verdict_and_summary"] == "fallback"
        assert any("FIX-ABCDEF" in i for i in report["generation"]["issues"])

    def test_invented_finding_ref_in_writeup_falls_back(self, monkeypatch):
        def answers(section, ctx):
            out = _good(section, ctx)
            if section == "finding_writeup":
                out["technical_detail"] = "Chains with F-99."
            return out
        report, _svc, _ = _run(answers, monkeypatch)
        assert "F-99" not in json.dumps(report["findings"])
        assert report["findings"][0]["severity_rationale"].startswith("Severity")   # deterministic fallback

    def test_unparseable_section_is_fail_soft(self, monkeypatch):
        def answers(section, ctx):
            return "not json" if section == "limitations" else _good(section, ctx)
        report, _svc, _ = _run(answers, monkeypatch)
        assert report["generation"]["sections"]["limitations"] == "fallback"
        assert any("untested" in lim or "not evidence" in lim for lim in report["limitations"])


class TestRoutes:
    def test_unknown_engagement_404(self):
        from app.routers import engagement_report as R
        from app.schemas.auth import CurrentUser

        class _DB:
            async def execute(self, *a, **k):
                return SimpleNamespace(scalar_one_or_none=lambda: None)
        user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")
        with pytest.raises(HTTPException) as e:
            asyncio.run(R.generate_operator_report(uuid.uuid4(), _DB(), user))
        assert e.value.status_code == 404

    def test_no_provider_is_503(self, monkeypatch):
        from app.routers import engagement_report as R
        from app.schemas.auth import CurrentUser
        from app.services.llm import AiRuntimeError

        async def boom(db, **kw):
            raise AiRuntimeError("no AI provider is configured", 503)
        monkeypatch.setattr(R, "generate_engagement_report", boom)
        user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")
        with pytest.raises(HTTPException) as e:
            asyncio.run(R._generate(None, SimpleNamespace(id=uuid.uuid4()), user))
        assert e.value.status_code == 503
