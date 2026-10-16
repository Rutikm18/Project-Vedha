"""
Response priority (P0-P5) is a rule set over real signals, not a relabelled severity.

The rules are data (PRIORITY_RULES), evaluated top to bottom, first match wins, and the
explanation lists every rule with whether it matched and which one decided.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import FindingSeverity, FindingStatus
from app.routers import findings as findings_router
from app.services.finding_priority import PRIORITY_LABELS, PRIORITY_RULES, explain_priority


def P(severity, *, kev=False, validated=False, epss=None, sla=None, status=FindingStatus.open):
    return explain_priority(severity=severity, kev=kev, exploit_validated=validated,
                            epss_score=epss, sla_state=sla, status=status)


@pytest.mark.parametrize("kwargs,expected,rule", [
    (dict(severity="critical", kev=True), "P0", "exploited_high_impact"),
    (dict(severity="high", validated=True), "P0", "exploited_high_impact"),
    (dict(severity="critical", sla="breached"), "P0", "critical_past_sla"),
    (dict(severity="critical", sla="on_track"), "P1", "critical"),
    (dict(severity="medium", kev=True), "P1", "exploited"),
    (dict(severity="low", validated=True), "P1", "exploited"),
    (dict(severity="high", epss=0.5), "P1", "high_strong_epss"),
    (dict(severity="high", epss=0.49), "P2", "high"),
    (dict(severity="medium", epss=0.8), "P2", "medium_strong_epss"),
    (dict(severity="medium", epss=0.1), "P3", "medium"),
    (dict(severity="low", epss=0.99), "P4", "low"),
    (dict(severity="info"), "P5", "info"),
    (dict(severity="nonsense"), "P5", "info"),
    (dict(severity=FindingSeverity.critical, sla="breached"), "P0", "critical_past_sla"),
])
def test_rules_decide_the_label(kwargs, expected, rule):
    out = P(**kwargs)
    assert (out["priority"], out["rule"]) == (expected, rule)
    assert out["label"] == PRIORITY_LABELS[expected]


def test_exactly_one_rule_is_decisive_and_it_is_the_first_match():
    out = P("critical", kev=True, sla="breached", epss=0.9)
    decisive = [r for r in out["rules"] if r["decisive"]]
    assert len(decisive) == 1 and decisive[0]["id"] == out["rule"]
    first_match = next(r for r in out["rules"] if r["matched"])
    assert first_match["id"] == decisive[0]["id"]
    # later rules can still match (the explanation says so) but never decide
    assert any(r["matched"] and not r["decisive"] for r in out["rules"])
    assert [r["id"] for r in out["rules"]] == [r[0] for r in PRIORITY_RULES]


def test_severity_and_priority_are_not_the_same_thing():
    assert P("critical")["priority"] != P("critical", kev=True)["priority"]      # P1 vs P0
    assert P("medium", kev=True)["priority"] != P("medium")["priority"]          # P1 vs P3
    assert P("high")["priority"] == "P2" and P("critical")["priority"] == "P1"   # not Critical=P0


@pytest.mark.parametrize("status", [FindingStatus.remediated, FindingStatus.accepted,
                                    FindingStatus.fp, "remediated"])
def test_closed_findings_have_no_response_priority(status):
    out = P("critical", kev=True, status=status)
    assert out["priority"] is None and out["rule"] == "closed"


@pytest.mark.parametrize("status", [FindingStatus.open, FindingStatus.confirmed, "open", None])
def test_open_and_confirmed_findings_are_prioritised(status):
    assert P("high", status=status)["priority"] is not None


def test_every_priority_is_reachable():
    reached = {rule[1] for rule in PRIORITY_RULES}
    assert reached == set(PRIORITY_LABELS)


# ── SLA state per finding: engagement policy, then tenant, then defaults ─────

def _finding(severity="critical", *, eng, age_hours):
    started = datetime.now(timezone.utc) - timedelta(hours=age_hours)
    return SimpleNamespace(
        id=uuid.uuid4(), engagement_id=eng, severity=FindingSeverity(severity), status=FindingStatus.open,
        first_seen=started, created_at=started, due_at=None, due_at_source=None, title="t")


def _db(engagements, tenant_row=None):
    eng_res = MagicMock()
    eng_res.scalars.return_value.all.return_value = engagements
    tenant_res = MagicMock()
    tenant_res.scalar_one_or_none.return_value = tenant_row
    results = iter([eng_res, tenant_res])
    db = MagicMock()
    db.execute = AsyncMock(side_effect=lambda *_a, **_k: next(results))
    return db


@pytest.mark.asyncio
async def test_sla_state_uses_the_engagement_policy_before_the_tenant_and_defaults():
    tenant = uuid.uuid4()
    strict, plain = uuid.uuid4(), uuid.uuid4()
    roe = {"sla_policy": {f"{s}_hours": h for s, h in
                          (("critical", 2), ("high", 2), ("medium", 2), ("low", 2), ("info", 0))}}
    engs = [SimpleNamespace(id=strict, tenant_id=tenant, rules_of_engagement=roe),
            SimpleNamespace(id=plain, tenant_id=tenant, rules_of_engagement={})]
    a = _finding(eng=strict, age_hours=5)      # past a 2h engagement window
    b = _finding(eng=plain, age_hours=5)       # well inside the 24h default
    states = await findings_router._sla_states(_db(engs), [a, b])
    assert states[a.id] == "breached" and states[b.id] != "breached"


@pytest.mark.asyncio
async def test_sla_lookup_is_two_bulk_queries_however_many_findings():
    tenant, eng = uuid.uuid4(), uuid.uuid4()
    engs = [SimpleNamespace(id=eng, tenant_id=tenant, rules_of_engagement={})]
    db = _db(engs)
    await findings_router._sla_states(db, [_finding(eng=eng, age_hours=i) for i in range(50)])
    assert db.execute.await_count == 2
