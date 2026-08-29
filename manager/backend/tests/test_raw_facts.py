"""Raw scanner facts endpoint — inspect exactly what the vedha-agent collected."""
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


def _sr(facts):
    return SimpleNamespace(
        id=uuid.uuid4(), job_id=uuid.uuid4(), agent_id=uuid.uuid4(),
        scan_type="network_va", fact_count=len(facts), validation_state="accepted",
        created_at=None, facts=facts)


@pytest.mark.asyncio
async def test_raw_facts_grouped_by_scanner():
    facts = [
        {"scanner": "port_scan", "target": "10.0.0.5", "port": 445, "status": "open"},
        {"scanner": "port_scan", "target": "10.0.0.5", "port": 3389, "status": "open"},
        {"scanner": "smb_scan", "target": "10.0.0.5", "port": 445, "status": "open",
         "data": {"smbv1_enabled": True, "negotiated_dialect": "0x0311"}},
        {"scanner": "rdp_scan", "target": "10.0.0.5", "port": 3389, "status": "open",
         "data": {"nla": False, "nla_required": False}},
    ]
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),  # get_or_404
        _scalars([_sr(facts)]),                                                  # scan_results
    ])
    out = await eng.raw_facts(uuid.uuid4(), db, _user())
    assert out["scanners"] == ["port_scan", "rdp_scan", "smb_scan"]
    assert out["by_scanner"] == {"port_scan": 2, "rdp_scan": 1, "smb_scan": 1}
    r = out["scan_results"][0]
    assert r["fact_count"] == 4 and r["scan_type"] == "network_va"
    # the RAW ScanResult dicts are returned verbatim (this is the ground truth)
    smb = next(f for f in r["facts"] if f["scanner"] == "smb_scan")
    assert smb["data"]["smbv1_enabled"] is True and smb["data"]["negotiated_dialect"] == "0x0311"


@pytest.mark.asyncio
async def test_raw_facts_filter_by_scanner():
    facts = [
        {"scanner": "port_scan", "target": "t", "port": 445, "status": "open"},
        {"scanner": "smb_scan", "target": "t", "port": 445, "status": "open", "data": {"x": 1}},
    ]
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([_sr(facts)]),
    ])
    out = await eng.raw_facts(uuid.uuid4(), db, _user(), scanner="smb_scan")
    shown = out["scan_results"][0]["facts"]
    assert len(shown) == 1 and shown[0]["scanner"] == "smb_scan"
    # by_scanner still reflects ALL scanners (the breakdown), only `facts` is filtered
    assert out["by_scanner"] == {"port_scan": 1, "smb_scan": 1}


@pytest.mark.asyncio
async def test_raw_facts_bounds_and_no_results():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([]),
    ])
    out = await eng.raw_facts(uuid.uuid4(), db, _user(), limit=999, max_facts=999999)
    assert out["scan_results"] == [] and out["scanners"] == []
