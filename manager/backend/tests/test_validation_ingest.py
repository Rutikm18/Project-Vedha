"""Unit tests for P3 Task 7: validation-result ingestion → finding verdict.

Pure transition (`apply_validation_outcome`) + mocked-session ingestion
(`ingest_validation_result`). No DB.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.detection.active_validation import interpret_validation
from app.models.enums import FindingStatus
from app.services.validation_ingest import (
    apply_validation_outcome,
    ingest_validation_result,
    looks_like_validation_result,
)


def _finding(**kw):
    base = dict(status=FindingStatus.open, verification_state="inferred",
                exploit_validated=False)
    base.update(kw)
    return SimpleNamespace(**base)


# ── pure transition ───────────────────────────────────────────────────────────

def test_confirmed_raises_certainty():
    f = _finding()
    apply_validation_outcome(f, interpret_validation({"outcome": "confirmed"}))
    assert f.verification_state == "confirmed"
    assert f.exploit_validated is True
    assert f.status == FindingStatus.confirmed


def test_contradicted_marks_false_positive_without_touching_status():
    f = _finding()
    apply_validation_outcome(f, interpret_validation({"outcome": "contradicted"}))
    assert f.verification_state == "contradicted"
    assert f.exploit_validated is False
    assert f.status == FindingStatus.open


def test_inconclusive_leaves_finding_unchanged():
    f = _finding()
    apply_validation_outcome(f, interpret_validation({"outcome": "inconclusive"}))
    assert f.verification_state == "inferred"
    assert f.status == FindingStatus.open


def test_confirmed_never_overrides_human_closed_finding():
    f = _finding(status=FindingStatus.fp)
    apply_validation_outcome(f, interpret_validation({"outcome": "confirmed"}))
    assert f.status == FindingStatus.fp          # not resurrected to confirmed
    assert f.verification_state == "confirmed"   # verdict still recorded


# ── gate ──────────────────────────────────────────────────────────────────────

def test_scan_result_is_not_mistaken_for_validation():
    assert looks_like_validation_result({"outcome": "partial", "facts": []}) is False
    assert looks_like_validation_result({"outcome": "confirmed"}) is True
    assert looks_like_validation_result(None) is False


# ── mocked-session ingestion ──────────────────────────────────────────────────

def _exec(scalar):
    r = MagicMock()
    r.scalar_one_or_none.return_value = scalar
    return r


@pytest.mark.asyncio
async def test_ingest_normal_scan_is_noop():
    db = MagicMock()
    db.execute = AsyncMock()
    handled = await ingest_validation_result(db, uuid.uuid4(), {"outcome": "partial", "facts": []})
    assert handled is False
    db.execute.assert_not_awaited()   # gated before any query


@pytest.mark.asyncio
async def test_ingest_confirmed_updates_request_and_finding():
    job_id, finding_id = uuid.uuid4(), uuid.uuid4()
    vr = SimpleNamespace(id=uuid.uuid4(), job_id=job_id, finding_id=finding_id,
                         result=None, outcome=None)
    finding = _finding()
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[_exec(vr), _exec(finding)])
    db.flush = AsyncMock()

    handled = await ingest_validation_result(db, job_id, {"outcome": "confirmed"})

    assert handled is True
    assert vr.outcome == "confirmed"
    assert vr.result == {"outcome": "confirmed"}
    assert finding.verification_state == "confirmed"
    assert finding.status == FindingStatus.confirmed


@pytest.mark.asyncio
async def test_ingest_unknown_job_is_noop():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[_exec(None)])
    handled = await ingest_validation_result(db, uuid.uuid4(), {"outcome": "confirmed"})
    assert handled is False
