"""Regression tests for AgentDecisionEngine._list_assets service batching.

The read tool used to issue one service query per asset (an N+1 that grew with
the asset count). It now issues a single batched query and groups in Python.
These tests pin that contract: correct grouping, the 30-services-per-asset cap,
and a bounded query count (2, never 1 + N) so the N+1 cannot silently return.

The engine's read tools only touch ``self._db``, so a tiny fake session that
returns queued results in call order is enough — no real DB, Redis, or LLM.
"""
import uuid
from types import SimpleNamespace

import pytest

from app.ai.agent import AgentDecisionEngine


class _Result:
    """Mimics the subset of a SQLAlchemy Result the read tools use."""

    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        return self

    def all(self):
        return list(self._rows)


class _FakeSession:
    """Returns queued results in call order and counts execute() calls."""

    def __init__(self, results):
        self._queue = list(results)
        self.execute_calls = 0

    async def execute(self, *args, **kwargs):
        self.execute_calls += 1
        return self._queue.pop(0)


def _asset(**kw):
    kw.setdefault("id", uuid.uuid4())
    kw.setdefault("ip_address", "10.0.0.1")
    kw.setdefault("hostname", "host")
    kw.setdefault("os", "linux")
    return SimpleNamespace(**kw)


def _svc(asset_id, port):
    return SimpleNamespace(
        asset_id=asset_id, port=port, protocol="tcp", product="nginx", version="1.0"
    )


@pytest.mark.asyncio
async def test_list_assets_batches_services_no_n_plus_one():
    a1, a2 = _asset(), _asset()
    services = [_svc(a1.id, p) for p in range(3)] + [_svc(a2.id, p) for p in range(2)]
    session = _FakeSession([_Result([a1, a2]), _Result(services)])
    engine = AgentDecisionEngine(db=session, client=object())

    out = await engine._list_assets(uuid.uuid4(), limit=50)

    # Exactly two queries (assets + one batched services query) regardless of how
    # many assets came back — this is the guard against the N+1 returning.
    assert session.execute_calls == 2
    assert out["count"] == 2
    by_id = {a["id"]: a for a in out["assets"]}
    assert len(by_id[str(a1.id)]["services"]) == 3
    assert len(by_id[str(a2.id)]["services"]) == 2
    # Grouping is correct: each service lands under its own asset.
    assert {s["port"] for s in by_id[str(a1.id)]["services"]} == {0, 1, 2}


@pytest.mark.asyncio
async def test_list_assets_caps_services_at_30():
    a1 = _asset()
    services = [_svc(a1.id, p) for p in range(50)]
    session = _FakeSession([_Result([a1]), _Result(services)])
    engine = AgentDecisionEngine(db=session, client=object())

    out = await engine._list_assets(uuid.uuid4(), limit=10)

    assert session.execute_calls == 2
    assert len(out["assets"][0]["services"]) == 30


@pytest.mark.asyncio
async def test_list_assets_empty_skips_service_query():
    session = _FakeSession([_Result([])])
    engine = AgentDecisionEngine(db=session, client=object())

    out = await engine._list_assets(uuid.uuid4(), limit=10)

    # No assets → no batched service query at all (only the assets query ran).
    assert session.execute_calls == 1
    assert out == {"count": 0, "assets": []}
