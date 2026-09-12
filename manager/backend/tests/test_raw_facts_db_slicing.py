"""
The raw-facts view must not pull whole fact blobs into the API worker.

It loaded up to 25 ScanResult rows through the ORM and then sliced in Python —
but the slicing is the cheap part. A deep scan stores ~107 KB of facts per host,
so a 1,000-host submission is a ~107 MB jsonb column; the default of 5
submissions is over half a gigabyte of transfer, and several times that once
Python has objects for it. Opening the page could take the worker down.

Postgres can slice the array and count the scanners without shipping either:
measured on a real row, 2,257 bytes instead of 107,039 — 47x less, for identical
output. The response shape does not change; the frontend is untouched.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.routers import engagements as eng


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(),
                           role="admin")


def _row(facts, *, by_scanner, matched=None, fact_count=None):
    """One row as the sliced query returns it: metadata + a SLICE + DB-side census."""
    return {
        "id": uuid.uuid4(),
        "job_id": uuid.uuid4(),
        "agent_id": uuid.uuid4(),
        "scan_type": "network_va",
        "fact_count": fact_count if fact_count is not None else len(facts),
        "validation_state": "accepted",
        "created_at": datetime.now(timezone.utc),
        "facts": facts,
        "by_scanner": by_scanner,
        "matched": len(facts) if matched is None else matched,
    }


def _db(rows):
    db = MagicMock()
    executed: list = []

    async def _execute(stmt, params=None):
        executed.append((stmt, params))
        if len(executed) == 1:                       # get_or_404
            return MagicMock(
                scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4()))
        return MagicMock(mappings=lambda: MagicMock(all=lambda: rows))

    db.execute = AsyncMock(side_effect=_execute)
    db.executed = executed
    return db


@pytest.mark.asyncio
async def test_slicing_and_counting_happen_in_the_database():
    db = _db([_row([{"scanner": "syn_scan", "target": "10.0.0.5", "port": 445}],
                   by_scanner={"syn_scan": 23, "service_banner": 22},
                   fact_count=63)])

    await eng.raw_facts(uuid.uuid4(), db, _user())

    sql = str(db.executed[1][0]).lower()
    assert ("jsonb_array_elements" in sql or "jsonb_path_query_array" in sql), (
        "the fact array is still being loaded whole and sliced in Python")
    assert "jsonb_object_agg" in sql, (
        "the per-scanner census is still counted in Python over every fact")


@pytest.mark.asyncio
async def test_response_shape_is_unchanged():
    facts = [{"scanner": "smb_scan", "target": "10.0.0.5", "port": 445,
              "status": "open", "data": {"smbv1_enabled": True}}]
    db = _db([_row(facts, by_scanner={"smb_scan": 1, "syn_scan": 23},
                   fact_count=24)])

    out = await eng.raw_facts(uuid.uuid4(), db, _user())

    assert out["scanners"] == ["smb_scan", "syn_scan"]
    assert out["by_scanner"] == {"smb_scan": 1, "syn_scan": 23}
    row = out["scan_results"][0]
    assert row["fact_count"] == 24
    assert row["scan_type"] == "network_va"
    # The raw fact dicts still come back verbatim — this view is the ground truth.
    assert row["facts"][0]["data"]["smbv1_enabled"] is True
    assert row["truncated"] is False


@pytest.mark.asyncio
async def test_truncation_is_reported_from_the_database_count():
    db = _db([_row([{"scanner": "syn_scan"}] * 2,
                   by_scanner={"syn_scan": 500}, matched=500, fact_count=500)])

    out = await eng.raw_facts(uuid.uuid4(), db, _user(), max_facts=2)

    assert out["scan_results"][0]["truncated"] is True


@pytest.mark.asyncio
async def test_scanner_filter_is_applied_in_the_query_not_in_python():
    db = _db([_row([{"scanner": "smb_scan"}],
                   by_scanner={"smb_scan": 1, "syn_scan": 23}, fact_count=24)])

    out = await eng.raw_facts(uuid.uuid4(), db, _user(), scanner="smb_scan")

    params = db.executed[1][1] or {}
    assert "smb_scan" in params.values(), (
        "the scanner filter must be a query parameter, not a Python filter")
    # The breakdown still describes EVERY scanner; only `facts` is filtered.
    assert out["by_scanner"] == {"smb_scan": 1, "syn_scan": 23}
    assert [f["scanner"] for f in out["scan_results"][0]["facts"]] == ["smb_scan"]


@pytest.mark.asyncio
async def test_no_submissions_returns_empty():
    db = _db([])

    out = await eng.raw_facts(uuid.uuid4(), db, _user())

    assert out["scan_results"] == [] and out["scanners"] == []
