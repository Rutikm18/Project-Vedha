"""Result ingestion must cost a constant number of queries, however many hosts.

_promote_assets runs inside the probe's submit request under a row lock; a query
per host once cost ~11,000 round trips for a 1,000-host result and blew the probe's
30s read timeout. This harness pins the batched behaviour: it counts every
database call and fails if the count grows with the number of hosts.
"""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.models.asset import Asset
from app.services import job_result_service as svc


class CountingDB:
    """Counts execute()/flush() and answers each query with preset rows."""

    def __init__(self, assets=(), services=()):
        self.assets, self.services = list(assets), list(services)
        self.executes = 0
        self.flushes = 0
        self.added: list = []

    async def execute(self, stmt):
        self.executes += 1
        entity = stmt.column_descriptions[0]["entity"].__name__
        rows = {"Asset": self.assets, "Service": self.services}.get(entity, [])
        res = MagicMock()
        res.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=list(rows))))
        return res

    def add(self, obj):
        self.added.append(obj)
        if isinstance(obj, Asset) and obj.id is None:
            obj.id = uuid.uuid4()

    async def flush(self):
        self.flushes += 1
        for obj in self.added:
            if getattr(obj, "id", "x") is None:
                obj.id = uuid.uuid4()


def _result(n_hosts: int, ports: int = 3) -> dict:
    return {"hosts": [
        {"ip": f"10.1.{i // 250}.{i % 250 + 1}", "hostname": f"h{i}",
         "ports": [{"port": 1000 + p, "protocol": "tcp", "service": "svc", "product": "p", "version": "1"}
                   for p in range(ports)]}
        for i in range(n_hosts)]}


def _run(db, result):
    return asyncio.run(svc._promote_assets(db, uuid.uuid4(), result))


@pytest.mark.parametrize("hosts", [1, 50, 1000])
def test_new_hosts_cost_a_constant_number_of_queries(hosts):
    db = CountingDB()
    promoted = _run(db, _result(hosts))
    assert promoted == hosts
    assert db.executes <= 2, f"{db.executes} queries for {hosts} hosts"
    assert db.flushes <= 2
    assert len([o for o in db.added if not isinstance(o, Asset)]) == hosts * 3     # every port got a Service row


def test_known_hosts_are_updated_without_per_host_lookups():
    known = [SimpleNamespace(id=uuid.uuid4(), ip_address=f"10.1.0.{i + 1}", hostname=None, os=None,
                             last_seen=None, asset_type=None, device_role=None, role_detail=None,
                             role_confidence=None, tags=None, site_id=None) for i in range(200)]
    db = CountingDB(assets=known)
    promoted = _run(db, _result(200))
    assert promoted == 0 and db.executes <= 2
    assert all(a.hostname for a in known)           # updated in place


def test_a_host_listed_twice_creates_one_asset():
    result = _result(1)
    result["hosts"] = result["hosts"] * 2
    db = CountingDB()
    assert _run(db, result) == 1
    assert len([o for o in db.added if isinstance(o, Asset)]) == 1


# ── detection path: resolving the assets for a run ───────────────────────────

class AssetDB(CountingDB):
    def __init__(self, existing=()):
        super().__init__(assets=existing)

    async def execute(self, stmt):
        self.executes += 1
        res = MagicMock()
        # scalars().all() for the IN() prime query, scalar_one_or_none() for a single lookup
        rows = list(self.assets)
        res.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=rows)))
        res.scalar_one_or_none = MagicMock(return_value=None)
        return res


def _existing(n):
    return [SimpleNamespace(id=uuid.uuid4(), ip_address=f"10.5.0.{i}", site_id=None) for i in range(1, n + 1)]


def test_priming_resolves_a_whole_run_in_one_query_per_thousand_hosts():
    from app.discovery.finding_translator import AssetCache, _resolve_asset, prime_asset_cache

    hosts = [f"10.5.{i // 250}.{i % 250 + 1}" for i in range(2500)]
    db = AssetDB(existing=[])
    cache = AssetCache()
    asyncio.run(prime_asset_cache(db, uuid.uuid4(), hosts, cache))
    assert db.executes == 3                              # ceil(2500 / 1000)
    before = db.executes

    async def resolve_all():
        return [await _resolve_asset(db, uuid.uuid4(), h, cache=cache) for h in hosts]
    assets = asyncio.run(resolve_all())
    assert db.executes == before, "a primed host must not be looked up again"
    assert len({a.ip_address for a in assets}) == 2500
    assert all(a.id is not None for a in assets)          # ids come from the client: no flush needed
    assert db.flushes == 0


def test_hosts_that_already_exist_are_found_by_the_prime_query():
    from app.discovery.finding_translator import AssetCache, _resolve_asset, prime_asset_cache

    existing = _existing(3)
    db = AssetDB(existing=existing)
    cache = AssetCache()
    found = asyncio.run(prime_asset_cache(db, uuid.uuid4(), ["10.5.0.1", "10.5.0.2:443", "10.5.0.3"], cache))
    assert found == 3 and db.executes == 1

    async def resolve():
        return await _resolve_asset(db, uuid.uuid4(), "10.5.0.2:443", cache=cache)
    assert asyncio.run(resolve()) is existing[1] and db.executes == 1


def test_a_host_that_was_not_primed_is_still_looked_up_not_assumed_new():
    """Safety: only hosts the prime step actually checked may skip the lookup, so a
    host it never saw (e.g. one an attack-path rule introduces) cannot be duplicated."""
    from app.discovery.finding_translator import AssetCache, _resolve_asset

    db = AssetDB()
    cache = AssetCache()
    cache.known_absent.add("10.9.9.9")

    async def resolve():
        await _resolve_asset(db, uuid.uuid4(), "10.9.9.9", cache=cache)      # checked: no query
        await _resolve_asset(db, uuid.uuid4(), "10.8.8.8", cache=cache)      # never checked: one query
    asyncio.run(resolve())
    assert db.executes == 1


def test_ipv6_literals_keep_their_colons_and_host_port_is_split():
    from app.discovery.finding_translator import _host_of
    assert _host_of("10.0.0.1:443") == "10.0.0.1"
    assert _host_of("fe80::1") == "fe80::1"
    assert _host_of("") is None and _host_of(None) is None
