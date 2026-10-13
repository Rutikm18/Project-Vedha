"""Real PostgreSQL constraints; opt-in and restricted to the task test DB."""

import os
import uuid

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine

TEST_URL = os.getenv("ATTACK_PATH_TEST_DATABASE_URL")
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not TEST_URL, reason="isolated PostgreSQL URL required"),
]


@pytest_asyncio.fixture
async def database():
    url = make_url(TEST_URL)
    if (
        url.host not in ("localhost", "127.0.0.1")
        or url.port != 25432
        or url.database != "attack_path_test"
    ):
        raise RuntimeError("refusing a database outside the isolated task test scope")
    engine = create_async_engine(TEST_URL)
    tenant, engagement = uuid.uuid4(), uuid.uuid4()
    async with engine.begin() as db:
        await db.execute(
            text("INSERT INTO tenants (id,name) VALUES (:id,'attack-path-test')"),
            {"id": tenant},
        )
        await db.execute(
            text(
                "INSERT INTO engagements (id,tenant_id,name) VALUES (:id,:tenant,'test')"
            ),
            {"id": engagement, "tenant": tenant},
        )
        await db.execute(
            text(
                "INSERT INTO users (id,tenant_id,email,hashed_password,role) VALUES (:id,:tenant,'operator@example.invalid','test-only','analyst')"
            ),
            {"id": uuid.uuid5(tenant, "test-operator"), "tenant": tenant},
        )
    try:
        yield engine, tenant, engagement
    finally:
        async with engine.begin() as db:
            await db.execute(
                text("DELETE FROM outbox_events WHERE engagement_id=:id"),
                {"id": engagement},
            )
            await db.execute(text("DELETE FROM tenants WHERE id=:id"), {"id": tenant})
        await engine.dispose()


async def insert_snapshot(db, tenant, engagement, *, status="queued", result=None):
    snapshot = uuid.uuid4()
    await db.execute(
        text("""
        INSERT INTO attack_assessment_snapshots
        (id,tenant_id,engagement_id,status,input_hash,effective_as_of,known_at_cutoff,
         normalization_version,rule_pack_version,rule_artifact_sha256,input_document,result_document)
        VALUES (:id,:tenant,:eng,:status,:hash,now(),now(),'test@1','binding-contract@1',:hash,'{}',CAST(:result AS jsonb))
    """),
        {
            "id": snapshot,
            "tenant": tenant,
            "eng": engagement,
            "status": status,
            "hash": "a" * 64,
            "result": result,
        },
    )
    return snapshot


@pytest.mark.asyncio
async def test_snapshot_input_and_completed_result_are_immutable(database):
    engine, tenant, engagement = database
    async with engine.begin() as db:
        snapshot = await insert_snapshot(db, tenant, engagement)
    with pytest.raises(DBAPIError, match="inputs are immutable"):
        async with engine.begin() as db:
            await db.execute(
                text(
                    "UPDATE attack_assessment_snapshots SET input_document=CAST(:document AS jsonb) WHERE id=:id"
                ),
                {"id": snapshot, "document": '{"changed":true}'},
            )
    with pytest.raises(DBAPIError, match="inputs are immutable"):
        async with engine.begin() as db:
            await db.execute(
                text(
                    "UPDATE attack_assessment_snapshots SET id=:replacement WHERE id=:id"
                ),
                {"id": snapshot, "replacement": uuid.uuid4()},
            )
    async with engine.begin() as db:
        await db.execute(
            text(
                "UPDATE attack_assessment_snapshots SET status='completed',result_document='{}' WHERE id=:id"
            ),
            {"id": snapshot},
        )
    with pytest.raises(DBAPIError, match="completed attack assessments are immutable"):
        async with engine.begin() as db:
            await db.execute(
                text(
                    "UPDATE attack_assessment_snapshots SET result_document='[]' WHERE id=:id"
                ),
                {"id": snapshot},
            )


@pytest.mark.asyncio
async def test_foreign_tenant_engagement_binding_rejected(database):
    engine, _, engagement = database
    with pytest.raises(DBAPIError):
        async with engine.begin() as db:
            await insert_snapshot(db, uuid.uuid4(), engagement)


@pytest.mark.asyncio
async def test_completion_requires_result_and_failure_rollback_is_atomic(database):
    engine, tenant, engagement = database
    with pytest.raises(DBAPIError):
        async with engine.begin() as db:
            await insert_snapshot(db, tenant, engagement, status="completed")
    async with engine.begin() as db:
        count = (
            await db.execute(
                text(
                    "SELECT count(*) FROM attack_assessment_snapshots WHERE engagement_id=:id"
                ),
                {"id": engagement},
            )
        ).scalar_one()
        assert count == 0


@pytest.mark.asyncio
async def test_late_worker_cannot_replace_newer_completed_snapshot(database):
    engine, tenant, engagement = database
    async with engine.begin() as db:
        older = await insert_snapshot(db, tenant, engagement)
        newer = await insert_snapshot(
            db, tenant, engagement, status="completed", result='{"newer":true}'
        )
    async with engine.begin() as db:
        await db.execute(
            text(
                "UPDATE attack_assessment_snapshots SET status='completed',result_document='{}' WHERE id=:id"
            ),
            {"id": older},
        )
    async with engine.begin() as db:
        current = (
            await db.execute(
                text(
                    "SELECT id FROM attack_assessment_snapshots WHERE tenant_id=:tenant AND engagement_id=:eng AND status='completed' ORDER BY request_sequence DESC LIMIT 1"
                ),
                {"tenant": tenant, "eng": engagement},
            )
        ).scalar_one()
        assert current == newer
