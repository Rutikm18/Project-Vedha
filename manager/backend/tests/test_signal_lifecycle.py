"""M1 hardening — merged-signal lifecycle across detection runs.

Two producers describing one condition collapse into ONE finding. The signals that explain the
merge must follow the evidence: stamped by the run that saw them, dropped when a producer stops
matching, and never counted as a merge once only one remains."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from app.detection import engine_bridge as EB
from app.discovery.finding_translator import prune_stale_signals
from app.models.asset import Asset
from app.models.enums import FindingSeverity
from app.models.finding import Finding

ENG = uuid.uuid4()


class _Db:
    def __init__(self):
        self.added = []

    def add(self, o):
        self.added.append(o)
        o.id = getattr(o, "id", None) or uuid.uuid4()

    async def flush(self):
        pass


def _posture(rule, title, sev, port=2049):
    return {"rule_id": rule, "title": title, "asset_ip": "10.0.0.9", "severity": sev,
            "state": "confirmed", "category": "misconfiguration", "port": port, "remediation": "x",
            "evidence": {"dedup_key": f"exposed:{port}"}}


NFS = _posture("POSTURE-NFS-WORLD-READABLE-EXPORT", "NFS export world-readable", "high")
INTEL = _posture("POSTURE-EXPOSED-CLEARTEXT", "Cleartext protocol exposed on 2049 (NFS)", "medium")


async def _run(db, rows, run_id, index, asset):
    touched: list = []
    await EB._persist_posture_findings(
        db, ENG, run_id, datetime.now(timezone.utc), [dict(r) for r in rows], touched, "db-1",
        cache={"10.0.0.9": asset}, open_index=index, remediated_index={})
    EB.prune_stale_signals(touched, run_id)
    return touched


@pytest.fixture
def world():
    asset = Asset(engagement_id=ENG, ip_address="10.0.0.9")
    asset.id = uuid.uuid4()
    return _Db(), {}, asset


@pytest.mark.asyncio
async def test_two_producers_in_one_run_merge_and_keep_both_signals(world):
    db, index, asset = world
    await _run(db, [INTEL, NFS], uuid.uuid4(), index, asset)
    rows = [o for o in db.added if isinstance(o, Finding)]
    assert len(rows) == 1                                                  # one finding, not two
    sigs = rows[0].evidence["signals"]
    assert {s["rule_id"] for s in sigs} == {"POSTURE-EXPOSED-CLEARTEXT", "POSTURE-NFS-WORLD-READABLE-EXPORT"}
    assert rows[0].severity == FindingSeverity.high                        # strongest signal wins


@pytest.mark.asyncio
async def test_a_producer_that_stops_matching_drops_out_of_the_signals(world):
    db, index, asset = world
    await _run(db, [INTEL, NFS], uuid.uuid4(), index, asset)
    finding = next(o for o in db.added if isinstance(o, Finding))
    # Next run: only the dedicated NFS scanner still matches.
    await _run(db, [NFS], uuid.uuid4(), index, asset)
    assert "signals" not in finding.evidence                               # no longer a merge


@pytest.mark.asyncio
async def test_signals_survive_while_both_producers_keep_matching(world):
    db, index, asset = world
    await _run(db, [INTEL, NFS], uuid.uuid4(), index, asset)
    finding = next(o for o in db.added if isinstance(o, Finding))
    r2 = uuid.uuid4()
    await _run(db, [NFS, INTEL], r2, index, asset)
    assert len(finding.evidence["signals"]) == 2
    assert all(s["run_id"] == str(r2) for s in finding.evidence["signals"])


def test_prune_is_a_noop_for_findings_without_signals():
    f = Finding(engagement_id=ENG, title="t", evidence={"a": 1})
    prune_stale_signals([f], uuid.uuid4())
    assert f.evidence == {"a": 1}


def test_signals_are_not_part_of_the_integrity_digest():
    from app.services.evidence_integrity import content_for_integrity
    assert content_for_integrity({"x": 1, "signals": [{"rule_id": "A"}]}) == {"x": 1}
