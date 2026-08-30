"""Detection-trace coverage surfaced in the API: complete_with_gaps + explain.

Guards the research's central fix — a completed run with blind rules must NOT read
as clean; the portal must say what happened, and detection-explain must name the
per-rule verdict (the machine answer to "the scripts catch it but the manager doesn't").
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.routers import engagements as eng


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


def _scalars(items):
    return MagicMock(scalars=lambda: MagicMock(all=lambda: items))


def _rows(items):
    return MagicMock(all=lambda: items)


def _job(status="completed"):
    return SimpleNamespace(
        id=uuid.uuid4(), job_type=SimpleNamespace(value="discovery"),
        status=SimpleNamespace(value=status), agent_id=None,
        result={"use_case_id": "uc_network_va"}, created_at=None,
        started_at=None, completed_at=None)


def _run(status="completed", stats=None, scan_result_id=None):
    return SimpleNamespace(
        id=uuid.uuid4(), status=status, facts_count=3, findings_new=0,
        findings_current=0, started_at=None, finished_at=None, error=None,
        stats=stats, scan_result_id=scan_result_id)


# ── complete_with_gaps: blind rules must degrade the verdict ───────────────────
@pytest.mark.asyncio
async def test_completed_with_blind_rules_is_complete_with_gaps():
    stats = {"posture_coverage": {"rules_total": 11, "rules_assessed": 9,
                                  "rules_blind": 2, "rules_unassessed": 0,
                                  "blind_rule_ids": ["POSTURE-SMB-V1-ENABLED",
                                                     "POSTURE-RDP-NO-NLA"]}}
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),  # get_or_404
        _scalars([_job()]),                                                      # jobs
        _scalars([_run(stats=stats)]),                                           # runs (all)
        _scalars([]),                                                            # scan_result ids
        _rows([]),                                                               # queue
        _scalars([]),                                                            # findings
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    # completed, but NOT plain "complete" — and still is_complete (terminal).
    assert out["overall_status"] == "complete_with_gaps"
    assert out["is_complete"] is True
    assert out["coverage"]["rules_blind"] == 2
    assert out["coverage"]["has_gaps"] is True
    assert "POSTURE-SMB-V1-ENABLED" in out["coverage"]["blind_rule_ids"]
    # the reason must tell the operator NOT to read this as clean
    assert any("UNKNOWN" in r or "could not be assessed" in r for r in out["reasons"])


@pytest.mark.asyncio
async def test_completed_no_blind_is_plain_complete():
    stats = {"posture_coverage": {"rules_total": 11, "rules_assessed": 11,
                                  "rules_blind": 0, "blind_rule_ids": []}}
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([_job()]),
        _scalars([_run(stats=stats)]),
        _scalars([]),
        _rows([]),
        _scalars([]),
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["overall_status"] == "complete"
    assert out["coverage"]["has_gaps"] is False
    assert out["reasons"] == []


@pytest.mark.asyncio
async def test_aggregating_reason_names_the_outbox_worker():
    # jobs done, but no detection run yet → the operational gotcha, made visible.
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([_job()]),
        _scalars([]),          # no runs
        _scalars([]),          # scan_result ids
        _rows([]),             # queue
        _scalars([]),
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["overall_status"] == "aggregating"
    assert any("outbox" in r for r in out["reasons"])


# ── detection-explain ─────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_explain_single_rule_reports_schema_drift():
    stats = {"posture_verdicts": {
        "POSTURE-SMB-V1-ENABLED": {"verdict": "schema_drift",
                                   "reasons": ["required fact path absent: data.smbv1_enabled"]}}}
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),  # get_or_404
        MagicMock(scalar_one_or_none=lambda: _run(stats=stats)),                 # run
    ])
    out = await eng.detection_explain(uuid.uuid4(), db, _user(),
                                      rule_id="POSTURE-SMB-V1-ENABLED")
    assert out["verdict"] == "schema_drift"
    assert "smbv1_enabled" in out["reasons"][0]


@pytest.mark.asyncio
async def test_explain_all_rules_sorts_gaps_first():
    stats = {"posture_coverage": {"rules_blind": 1},
             "posture_verdicts": {
                 "A-CLEAN": {"verdict": "evaluated_clean", "reasons": []},
                 "B-DRIFT": {"verdict": "schema_drift", "reasons": ["absent"]},
                 "C-FINDING": {"verdict": "finding_exists", "reasons": []}}}
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        MagicMock(scalar_one_or_none=lambda: _run(stats=stats)),
    ])
    out = await eng.detection_explain(uuid.uuid4(), db, _user())
    order = [r["rule_id"] for r in out["rules"]]
    # drift before finding before clean
    assert order.index("B-DRIFT") < order.index("C-FINDING") < order.index("A-CLEAN")


@pytest.mark.asyncio
async def test_explain_no_run_says_never_ran():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        MagicMock(scalar_one_or_none=lambda: None),
    ])
    out = await eng.detection_explain(uuid.uuid4(), db, _user(), rule_id="X")
    assert out["verdict"] == "detection_never_ran"
