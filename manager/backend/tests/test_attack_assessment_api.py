"""API/outbox/capture integration against the isolated PostgreSQL database."""

import os
import asyncio
import uuid
from types import SimpleNamespace

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker

from tests.test_attack_assessment_storage import database as storage_database
from app.dependencies import get_current_user
from app.database import get_db
from app.models.attack_assessment import AttackAssessmentSnapshot
from app.models.outbox import OutboxEvent
from app.routers import attack_assessments as api
from app.schemas.auth import CurrentUser
from app.services.attack_assessments import (
    capture_snapshot,
    compute_snapshot,
    TOPIC_ATTACK_ASSESSMENT,
)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.getenv("ATTACK_PATH_TEST_DATABASE_URL"),
        reason="isolated PostgreSQL URL required",
    ),
]

database = storage_database


def _test_app(engine, tenant, engagement, monkeypatch, *, enabled=True):
    monkeypatch.setattr(
        api,
        "get_settings",
        lambda: SimpleNamespace(
            attack_assessments_enabled=enabled,
            attack_assessment_engagement_allowlist={engagement},
        ),
    )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    state = {"role": "analyst", "auth_type": "jwt"}

    def user():
        return CurrentUser(
            user_id=uuid.uuid5(tenant, "test-operator"), tenant_id=tenant, **state
        )

    async def db():
        async with factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app = FastAPI()
    app.include_router(api.router)
    app.dependency_overrides[get_db] = db
    app.dependency_overrides[get_current_user] = user
    return app, state, factory


async def add_finding(engine, engagement):
    asset, service, finding = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    async with engine.begin() as db:
        await db.execute(
            text(
                "INSERT INTO assets (id,engagement_id,hostname) VALUES (:id,:eng,'synthetic-datastore')"
            ),
            {"id": asset, "eng": engagement},
        )
        await db.execute(
            text(
                "INSERT INTO services (id,asset_id,port,protocol,service_name) VALUES (:id,:asset,6379,'tcp','redis')"
            ),
            {"id": service, "asset": asset},
        )
        await db.execute(
            text(
                "INSERT INTO findings (id,engagement_id,asset_id,title,severity,evidence) VALUES (:id,:eng,:asset,'scoped test finding','high',jsonb_build_object('service_id',CAST(:service AS text),'unauthenticated',true))"
            ),
            {"id": finding, "eng": engagement, "asset": asset, "service": str(service)},
        )
    return finding


@pytest.mark.asyncio
async def test_capture_queue_compute_detail_and_read_only_get(database, monkeypatch):
    engine, tenant, engagement = database
    finding = await add_finding(engine, engagement)
    app, _, factory = _test_app(engine, tenant, engagement, monkeypatch)
    base = f"/engagements/{engagement}/attack-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        empty = await client.get(base)
        assert empty.json()["state"] == "not_evaluated"
        created = await client.post(base)
        assert created.status_code == 202, created.text
        assert created.headers["cache-control"] == "no-store"
        snapshot_id = uuid.UUID(created.json()["id"])
        async with factory() as db:
            event = (
                await db.execute(
                    select(OutboxEvent).where(
                        OutboxEvent.topic == TOPIC_ATTACK_ASSESSMENT,
                        OutboxEvent.engagement_id == engagement,
                    )
                )
            ).scalar_one()
            assert event.payload["snapshot_id"] == str(snapshot_id)
            snapshot = await db.get(AttackAssessmentSnapshot, snapshot_id)
            assert (
                snapshot.input_document["capture_protocol"]
                == "materialized_repeatable_read"
            )
            await compute_snapshot(db, snapshot_id, tenant)
            await db.commit()
        response = await client.get(f"{base}/{snapshot_id}")
        assert response.status_code == 200
        assert response.json()["total"] == 1
        item = response.json()["items"][0]
        assert item["goal_state"] == "indeterminate"
        assert item["supported_proofs"] == 0
        assert item["rule_applicability"] == "candidate"
        detail = await client.get(f"{base}/{snapshot_id}/findings/{finding}")
        assert detail.json()["assessment"]["finding_id"] == str(finding)
        current = await client.get(base)
        assert current.json()["last_completed"]["id"] == str(snapshot_id)
        async with factory() as db:
            events = (
                (
                    await db.execute(
                        select(OutboxEvent).where(
                            OutboxEvent.topic == TOPIC_ATTACK_ASSESSMENT,
                            OutboxEvent.engagement_id == engagement,
                        )
                    )
                )
                .scalars()
                .all()
            )
            assert len(events) == 1  # GET never queues or recomputes.


@pytest.mark.asyncio
async def test_scope_role_flag_and_revocation(database, monkeypatch):
    engine, tenant, engagement = database
    app, state, _ = _test_app(engine, tenant, engagement, monkeypatch)
    base = f"/engagements/{engagement}/attack-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        assert (
            await client.get(f"/engagements/{uuid.uuid4()}/attack-assessments")
        ).status_code == 404
        state["role"] = "client"
        assert (await client.get(base)).status_code == 403
        state["role"] = "auditor"
        assert (await client.get(base)).status_code == 200
        assert (await client.post(base)).status_code == 403
        state["role"] = "analyst"
        state["auth_type"] = "pat"
        assert (await client.get(base)).status_code == 403
        monkeypatch.setattr(
            api,
            "get_settings",
            lambda: SimpleNamespace(attack_assessments_enabled=False),
        )
        assert (await client.get(base)).status_code == 404


@pytest.mark.asyncio
async def test_capture_is_frozen_retry_idempotent_and_failure_keeps_last_result(
    database, monkeypatch
):
    engine, tenant, engagement = database
    finding = await add_finding(engine, engagement)
    app, _, factory = _test_app(engine, tenant, engagement, monkeypatch)
    base = f"/engagements/{engagement}/attack-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        first = uuid.UUID((await client.post(base)).json()["id"])
        async with factory() as db:
            await db.execute(
                text("UPDATE findings SET title='changed after capture' WHERE id=:id"),
                {"id": finding},
            )
            await db.commit()
            await compute_snapshot(db, first, tenant)
            await db.commit()
            await compute_snapshot(db, first, tenant)  # duplicate outbox delivery
            await db.commit()
        old = (await client.get(f"{base}/{first}")).json()
        assert old["items"][0]["title"] == "scoped test finding"
        second = uuid.UUID((await client.post(base)).json()["id"])
        async with factory() as db:
            row = await db.get(AttackAssessmentSnapshot, second)
            row.status = "failed"
            row.failure_code = "assessment_compute_failed"
            await db.commit()
        current = (await client.get(base)).json()
        assert current["latest_request"]["status"] == "failed"
        assert current["last_completed"]["id"] == str(first)
        assert (
            await client.get(f"{base}/{second}/findings/{finding}")
        ).status_code == 404


@pytest.mark.asyncio
async def test_capture_does_not_mix_concurrently_changed_source_rows(
    database, monkeypatch
):
    engine, tenant, engagement = database
    finding = await add_finding(engine, engagement)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as db:
        execute = db.stream
        changed = False

        async def interleave(statement, *args, **kwargs):
            nonlocal changed
            result = await execute(statement, *args, **kwargs)
            if not changed and "FROM findings" in str(statement):
                changed = True
                async with engine.begin() as writer:
                    await writer.execute(
                        text("UPDATE findings SET title='new revision' WHERE id=:id"),
                        {"id": finding},
                    )
                    await writer.execute(
                        text(
                            "UPDATE services SET port=6380 WHERE asset_id IN (SELECT id FROM assets WHERE engagement_id=:id)"
                        ),
                        {"id": engagement},
                    )
            return result

        monkeypatch.setattr(db, "stream", interleave)
        snapshot = await capture_snapshot(db, tenant, engagement)
        assert changed
        assert snapshot.input_document["findings"][0]["title"] == "scoped test finding"
        assert snapshot.input_document["services"][0]["port"] == 6379
        await db.rollback()
    async with engine.begin() as current:
        assert (
            await current.execute(
                text("SELECT title FROM findings WHERE id=:id"), {"id": finding}
            )
        ).scalar_one() == "new revision"


@pytest.mark.asyncio
async def test_real_outbox_handler_duplicate_delivery(database, monkeypatch):
    from app.workers import outbox

    engine, tenant, engagement = database
    await add_finding(engine, engagement)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(outbox, "AsyncSessionLocal", factory)
    async with factory() as db:
        snapshot = await capture_snapshot(db, tenant, engagement)
        await db.commit()
    event = outbox.Event(
        id=str(uuid.uuid4()),
        topic=TOPIC_ATTACK_ASSESSMENT,
        engagement_id=str(engagement),
        scan_result_id=None,
        payload={"snapshot_id": str(snapshot.id), "tenant_id": str(tenant)},
        attempts=1,
    )
    await outbox._handle_attack_assessment(event)
    await outbox._handle_attack_assessment(event)
    async with factory() as db:
        completed = await db.get(AttackAssessmentSnapshot, snapshot.id)
        assert completed.status == "completed"
        assert len(completed.result_document["assessments"]) == 1


@pytest.mark.asyncio
async def test_live_demotion_disable_and_tenant_disable_override_old_token(
    database, monkeypatch
):
    engine, tenant, engagement = database
    app, _, _ = _test_app(engine, tenant, engagement, monkeypatch)
    base = f"/engagements/{engagement}/attack-assessments"
    user_id = uuid.uuid5(tenant, "test-operator")
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        assert (await client.get(base)).json()["can_compute"]
        async with engine.begin() as db:
            await db.execute(
                text("UPDATE users SET role='auditor' WHERE id=:id"), {"id": user_id}
            )
        read_only = await client.get(base)
        assert read_only.status_code == 200
        assert read_only.json()["can_compute"] is False
        assert (await client.post(base)).status_code == 403
        async with engine.begin() as db:
            await db.execute(
                text("UPDATE users SET is_active=false WHERE id=:id"), {"id": user_id}
            )
        assert (await client.get(base)).status_code == 403
        async with engine.begin() as db:
            await db.execute(
                text("UPDATE users SET is_active=true,role='analyst' WHERE id=:id"),
                {"id": user_id},
            )
            await db.execute(
                text("UPDATE tenants SET is_active=false WHERE id=:id"), {"id": tenant}
            )
        assert (await client.get(base)).status_code == 403


@pytest.mark.asyncio
async def test_capture_refuses_an_existing_inconsistent_transaction(database):
    engine, tenant, engagement = database
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as db:
        await db.execute(select(AttackAssessmentSnapshot.id).limit(1))
        with pytest.raises(ValueError, match="capture_requires_repeatable_read"):
            await capture_snapshot(db, tenant, engagement)


@pytest.mark.asyncio
async def test_repeated_and_concurrent_request_key_create_one_job(
    database, monkeypatch
):
    engine, tenant, engagement = database
    app, _, factory = _test_app(engine, tenant, engagement, monkeypatch)
    base = f"/engagements/{engagement}/attack-assessments"
    key = str(uuid.uuid4())
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        results = await asyncio.gather(
            *(client.post(base, headers={"Idempotency-Key": key}) for _ in range(2))
        )
        assert all(r.status_code == 202 for r in results), [r.text for r in results]
        assert results[0].json()["id"] == results[1].json()["id"]
        repeated = await client.post(base, headers={"Idempotency-Key": key})
        assert repeated.json()["id"] == results[0].json()["id"]
    async with factory() as db:
        events = (
            (
                await db.execute(
                    select(OutboxEvent).where(
                        OutboxEvent.engagement_id == engagement,
                        OutboxEvent.topic == TOPIC_ATTACK_ASSESSMENT,
                    )
                )
            )
            .scalars()
            .all()
        )
        assert len(events) == 1


@pytest.mark.asyncio
async def test_input_budget_rejection_preserves_previous_result(database, monkeypatch):
    from app.services import attack_assessments as service

    engine, tenant, engagement = database
    await add_finding(engine, engagement)
    app, _, factory = _test_app(engine, tenant, engagement, monkeypatch)
    base = f"/engagements/{engagement}/attack-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        created = uuid.UUID((await client.post(base)).json()["id"])
        async with factory() as db:
            await compute_snapshot(db, created, tenant)
            await db.commit()
        monkeypatch.setattr(service, "MAX_INPUT_BYTES", 16)
        assert (await client.post(base)).status_code == 413
        result = (await client.get(base)).json()
        assert result["last_completed"]["id"] == str(created)
