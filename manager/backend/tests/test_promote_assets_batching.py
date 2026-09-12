"""
Promoting a scan's hosts must not cost a query per host and per port.

`_promote_assets` ran one SELECT for every host, then one more for every port of
every host, all inside the HTTP request that also holds a FOR UPDATE lock on the
job row. A 1,000-host result with ten open ports each is ~11,000 sequential round
trips before the probe's 30s read timeout — at which point the probe re-uploads
the whole 100 MB payload while the first request is still running.

Two queries answer the same question: which of these IPs already exist, and which
services do they already have.
"""
from __future__ import annotations

import uuid

import pytest

from app.models.asset import Asset
from app.models.service import Service
from app.services.job_result_service import _promote_assets

ENGAGEMENT = uuid.uuid4()
HOSTS = 50
PORTS_PER_HOST = 5


def _result(hosts=HOSTS, ports=PORTS_PER_HOST) -> dict:
    return {
        "hosts": [
            {
                "ip": f"10.0.{i // 256}.{i % 256}",
                "hostname": f"host-{i}",
                "ports": [{"port": 8000 + p, "protocol": "tcp",
                           "service": "http"} for p in range(ports)],
            }
            for i in range(hosts)
        ],
    }


class _Rows:
    """Minimal stand-in for a SQLAlchemy Result."""

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

    def all(self):
        return list(self._rows)


def _bound_values(stmt) -> set:
    """Every value the statement filters on, IN-lists flattened.

    The fake has to honour the filter or a batched IN query and a per-row query
    would look the same to it.
    """
    values: set = set()
    for value in stmt.compile().params.values():
        if isinstance(value, (list, tuple, set)):
            values.update(value)
        else:
            values.add(value)
    return values


def _matches(row, wanted: set) -> bool:
    if isinstance(row, Asset):
        return row.ip_address in wanted
    if isinstance(row, Service):
        return row.asset_id in wanted
    return False


class _FakeSession:
    """Counts queries. The point of the test is how MANY there are."""

    def __init__(self, existing=()):
        self.executed: list = []
        self.added: list = []
        self.flushes = 0
        self._existing = list(existing)

    async def execute(self, stmt):
        self.executed.append(stmt)
        entity = stmt.column_descriptions[0]["entity"]
        wanted = _bound_values(stmt)
        return _Rows([row for row in self._existing
                      if isinstance(row, entity) and _matches(row, wanted)])

    def add(self, obj):
        self.added.append(obj)
        if isinstance(obj, Asset) and obj.id is None:
            obj.id = uuid.uuid4()          # what flush() would assign

    async def flush(self):
        self.flushes += 1


@pytest.mark.asyncio
async def test_promotion_is_a_constant_number_of_queries():
    db = _FakeSession()

    promoted = await _promote_assets(db, ENGAGEMENT, _result())

    assert promoted == HOSTS
    assert len(db.executed) <= 4, (
        f"{len(db.executed)} queries for {HOSTS} hosts x {PORTS_PER_HOST} ports "
        "— promotion is still per-host/per-port")


@pytest.mark.asyncio
async def test_every_host_and_service_is_still_created():
    db = _FakeSession()

    await _promote_assets(db, ENGAGEMENT, _result())

    assets = [o for o in db.added if isinstance(o, Asset)]
    services = [o for o in db.added if isinstance(o, Service)]
    assert len(assets) == HOSTS
    assert len(services) == HOSTS * PORTS_PER_HOST
    assert {a.hostname for a in assets} == {f"host-{i}" for i in range(HOSTS)}


@pytest.mark.asyncio
async def test_an_existing_asset_is_updated_not_duplicated():
    existing = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.0",
                     hostname="old-name")
    existing.id = uuid.uuid4()
    db = _FakeSession(existing=[existing])

    promoted = await _promote_assets(db, ENGAGEMENT, _result(hosts=2, ports=1))

    assert promoted == 1                                  # only the second host
    assert existing.hostname == "host-0"                  # updated in place
    assert [o for o in db.added if isinstance(o, Asset)] != [existing]


@pytest.mark.asyncio
async def test_an_existing_service_is_updated_not_duplicated():
    asset = Asset(engagement_id=ENGAGEMENT, ip_address="10.0.0.0")
    asset.id = uuid.uuid4()
    service = Service(asset_id=asset.id, port=8000, protocol="tcp")
    db = _FakeSession(existing=[asset, service])

    await _promote_assets(db, ENGAGEMENT, _result(hosts=1, ports=1))

    assert [o for o in db.added if isinstance(o, Service)] == []
    assert service.service_name == "http"


@pytest.mark.asyncio
async def test_no_hosts_issues_no_queries():
    db = _FakeSession()

    promoted = await _promote_assets(db, ENGAGEMENT, {"hosts": []})

    assert promoted == 0
    assert db.executed == []
