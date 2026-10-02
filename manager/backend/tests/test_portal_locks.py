"""The portal lock guard: while a customer request is served, every ORM query
that touches findings excludes the locked severities — whole rows, single
columns, counts, subqueries and joins alike. Operator requests are untouched."""
from __future__ import annotations

import asyncio

import pytest
from sqlalchemy import event, func, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.finding import Finding
from app.services import portal_locks


def _sql(stmt) -> str:
    return str(portal_locks.guarded(stmt).compile(dialect=postgresql.dialect()))


@pytest.fixture(autouse=True)
def _clean():
    token = portal_locks._LOCKED.set(None)
    yield
    portal_locks._LOCKED.reset(token)


def test_inactive_guard_changes_nothing():
    assert "NOT IN" not in _sql(select(Finding))


@pytest.mark.parametrize("label,stmt", [
    ("rows", select(Finding)),
    ("one column", select(Finding.title)),
    ("count", select(func.count()).select_from(Finding)),
    ("count by severity", select(Finding.severity, func.count()).group_by(Finding.severity)),
    ("subquery", select(select(Finding.title).subquery().c.title)),
    ("join", select(Asset).join(Finding, Finding.asset_id == Asset.id)),
])
def test_active_guard_filters_every_shape(label, stmt):
    portal_locks.activate(["critical", "high"])
    sql = _sql(stmt)
    assert "NOT IN" in sql, label
    assert "severity" in sql


def test_empty_lock_list_is_inactive():
    portal_locks.activate([])
    assert portal_locks.current() == frozenset()
    assert "NOT IN" not in _sql(select(Finding))


def test_lifted_reads_everything_then_restores():
    portal_locks.activate(["critical"])
    with portal_locks.lifted():
        assert "NOT IN" not in _sql(select(Finding))
    assert "NOT IN" in _sql(select(Finding))


def test_the_guard_is_wired_into_every_session():
    assert event.contains(Session, "do_orm_execute", portal_locks._on_execute)


@pytest.mark.asyncio
async def test_locks_do_not_leak_between_concurrent_requests():
    seen: dict[str, frozenset] = {}

    async def customer():
        portal_locks.activate(["critical", "high"])
        await asyncio.sleep(0.01)
        seen["customer"] = portal_locks.current()

    async def operator():
        await asyncio.sleep(0.005)
        seen["operator"] = portal_locks.current()

    await asyncio.gather(asyncio.create_task(customer()), asyncio.create_task(operator()))
    assert seen["customer"] == frozenset({"critical", "high"})
    assert seen["operator"] == frozenset()
