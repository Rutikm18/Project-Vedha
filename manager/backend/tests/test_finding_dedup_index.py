"""
Finding persistence must not cost one or two queries per FINDING.

Every posture/CVE finding did a dedup lookup, and on a miss a second lookup for a
remediated row to reopen. Detection produces ~12 posture findings per host, so a
500-host run is ~6,000 findings and 6,000-12,000 sequential queries inside the
outbox handler — whose reclaim lease is 5 minutes, after which the event is
requeued and the whole run happens again.

The asset lookups in this same loop were already solved with a caller-owned cache
for one run (`_resolve_asset(..., cache=...)`). This applies the identical idiom
to the dedup lookups: load the engagement's existing findings ONCE, keyed by
(asset_id, title), then look up in the dict.

The lifecycle must not change: an unchanged issue reaffirms, a remediated one
reopens as a regression, and two findings with the same identity inside ONE run
must still collapse onto one row.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from app.detection import engine_bridge
from app.models.asset import Asset
from app.models.enums import FindingStatus
from app.models.finding import Finding

ENGAGEMENT = uuid.uuid4()
RUN = uuid.uuid4()
HOSTS = 20
RULES_PER_HOST = 10


def _posture(host_index: int, rule_index: int) -> dict:
    return {
        "rule_id": f"POSTURE-{rule_index:03d}",
        "title": f"Weak configuration {rule_index}",
        "asset_ip": f"10.0.0.{host_index}",
        "severity": "medium",
        "state": "confirmed",
        "remediation": "fix it",
        "risk_score": 5.0,
    }


class _Rows:
    def __init__(self, rows):
        self._rows = list(rows)

    def scalars(self):
        rows = self._rows

        class _Scalars:
            def all(self):
                return list(rows)
        return _Scalars()

    def scalar_one_or_none(self):
        return self._rows[0] if self._rows else None


class _FakeSession:
    def __init__(self):
        self.executed: list = []
        self.added: list = []

    async def execute(self, stmt):
        self.executed.append(stmt)
        return _Rows([])

    def add(self, obj):
        self.added.append(obj)
        if getattr(obj, "id", None) is None:
            obj.id = uuid.uuid4()

    async def flush(self):
        pass


async def _persist(db, posture, *, open_index=None, remediated_index=None,
                   cache=None):
    touched: list = []
    return await engine_bridge._persist_posture_findings(
        db, ENGAGEMENT, RUN, datetime.now(timezone.utc), posture, touched,
        "vulndb-1", cache={} if cache is None else cache,
        open_index={} if open_index is None else open_index,
        remediated_index={} if remediated_index is None else remediated_index,
    )


@pytest.mark.asyncio
async def test_persistence_does_not_query_per_finding():
    db = _FakeSession()
    posture = [_posture(h, r) for h in range(HOSTS) for r in range(RULES_PER_HOST)]

    created, _reaffirmed = await _persist(db, posture)

    assert created == HOSTS * RULES_PER_HOST
    # One asset lookup per distinct host (already cached per run) and nothing else.
    assert len(db.executed) <= HOSTS + 2, (
        f"{len(db.executed)} queries for {len(posture)} findings — dedup is "
        "still per-finding")


@pytest.mark.asyncio
async def test_a_known_open_finding_is_reaffirmed_not_duplicated():
    db = _FakeSession()
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.0")
    asset.id = uuid.uuid4()
    existing = Finding(engagement_id=ENGAGEMENT, asset_id=asset.id,
                       title="Weak configuration 0", status=FindingStatus.open)
    index = {(asset.id, "Weak configuration 0"): existing}

    created, reaffirmed = await _persist(
        db, [_posture(0, 0)], open_index=index, cache={"10.0.0.0": asset})

    assert (created, reaffirmed) == (0, 1)
    assert existing.detection_run_id == RUN
    assert [o for o in db.added if isinstance(o, Finding)] == []


@pytest.mark.asyncio
async def test_a_remediated_finding_reopens_as_a_regression():
    db = _FakeSession()
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.0")
    asset.id = uuid.uuid4()
    closed = Finding(engagement_id=ENGAGEMENT, asset_id=asset.id,
                     title="Weak configuration 0",
                     status=FindingStatus.remediated)
    index = {(asset.id, "Weak configuration 0"): closed}

    created, reaffirmed = await _persist(
        db, [_posture(0, 0)], remediated_index=index,
        cache={"10.0.0.0": asset})

    assert (created, reaffirmed) == (0, 1)
    assert closed.evidence["regression"] is True
    assert [o for o in db.added if isinstance(o, Finding)] == []


@pytest.mark.asyncio
async def test_two_identical_findings_in_one_run_collapse_to_one_row():
    """Autoflush used to make the second lookup find the first row. With an
    index, a newly created finding has to be indexed as it is created."""
    db = _FakeSession()

    created, reaffirmed = await _persist(db, [_posture(0, 0), _posture(0, 0)])

    assert created == 1
    assert reaffirmed == 1
    assert len([o for o in db.added if isinstance(o, Finding)]) == 1
