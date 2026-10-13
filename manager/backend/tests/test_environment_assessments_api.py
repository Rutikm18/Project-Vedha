import os
import uuid

import httpx
import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError

from app.models.environment_assessment import EnvironmentAssessment
from app.models.outbox import OutboxEvent
from app.routers import environment_assessments as api
from app.services.environment_assessments import compute_environment
from tests.test_attack_assessment_api import _test_app, add_finding
from tests.test_attack_assessment_storage import database as storage_database

database = storage_database
pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not os.getenv("ATTACK_PATH_TEST_DATABASE_URL"),
        reason="isolated PostgreSQL URL required",
    ),
]


async def app_for(database, monkeypatch):
    engine, tenant, first = database
    second = uuid.uuid4()
    async with engine.begin() as db:
        await db.execute(
            text(
                "INSERT INTO engagements (id,tenant_id,name) VALUES (:id,:tenant,'second assessment')"
            ),
            {"id": second, "tenant": tenant},
        )
    await add_finding(engine, first)
    await add_finding(engine, second)
    app, state, factory = _test_app(engine, tenant, first, monkeypatch)
    from types import SimpleNamespace

    monkeypatch.setattr(
        api,
        "get_settings",
        lambda: SimpleNamespace(
            attack_assessments_enabled=True,
            attack_assessment_engagement_allowlist={first, second},
        ),
    )
    app.include_router(api.router)
    return app, state, factory, second


@pytest.mark.asyncio
async def test_combined_cut_worker_retry_and_current_selection(database, monkeypatch):
    _engine, tenant, first = database
    app, state, factory, second = await app_for(database, monkeypatch)
    base = "/attack-paths/environment-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        assert len((await client.get(base + "/options")).json()["items"]) == 2
        key = str(uuid.uuid4())
        body = {"engagement_ids": [str(first), str(second)]}
        created = await client.post(base, json=body, headers={"Idempotency-Key": key})
        assert created.status_code == 202, created.text
        assessment = uuid.UUID(created.json()["id"])
        repeated = await client.post(
            base,
            json={"engagement_ids": [str(second), str(first)]},
            headers={"Idempotency-Key": key},
        )
        assert repeated.json()["id"] == str(assessment)
        assert (
            await client.post(
                base,
                json={"engagement_ids": [str(first)]},
                headers={"Idempotency-Key": key},
            )
        ).status_code == 409
        async with factory() as db:
            await compute_environment(db, assessment, tenant)
            await db.commit()
            await compute_environment(db, assessment, tenant)
            await db.commit()
            row = await db.get(EnvironmentAssessment, assessment)
            sources = row.input_document["sources"]
            assert len(sources) == 2
            assert row.status == "completed"
        detail = await client.get(base + f"/{assessment}")
        result = detail.json()
        assert result["total"] == 2
        assert (
            len({s["id"] for s in result["systems"]}) == 2
        )  # same host label cannot merge distinct systems
        assert {i["engagement_id"] for i in result["items"]} == {
            str(first),
            str(second),
        }
        assert result["engine"]["supported_proofs"] == []
        assert result["bridge_state"] == "not_normalized"
        assert detail.headers["cache-control"] == "no-store"
        saved = await client.get(base, params={"engagement_ids": f"{second},{first}"})
        assert saved.status_code == 200
        assert saved.json()["latest_request"]["id"] == str(assessment)
        assert saved.json()["last_completed"]["id"] == str(assessment)
        assert (
            await client.get(base, params={"engagement_ids": str(first)})
        ).json() == {
            "latest_request": None,
            "last_completed": None,
            "completed_history": [],
        }
        assert (
            await client.get(base, params={"engagement_ids": f"{first},{first}"})
        ).status_code == 422
        assert (
            await client.get(base, params={"engagement_ids": str(uuid.uuid4())})
        ).status_code == 404
        async with factory() as db:
            # Sorted scope can queue on either member; inspect the tenant through group payload below.
            all_events = (
                (
                    await db.execute(
                        select(OutboxEvent).where(
                            OutboxEvent.topic == "environment_assessment.compute",
                            OutboxEvent.engagement_id.in_([first, second]),
                        )
                    )
                )
                .scalars()
                .all()
            )
            assert len(all_events) == 1
            assert all_events[0].payload["assessment_id"] == str(assessment)
        state["role"] = "auditor"
        assert (await client.get(base + f"/{assessment}")).status_code == 200
        assert (await client.post(base, json=body)).status_code == 403


@pytest.mark.asyncio
async def test_latest_failed_selection_retains_completed_result(database, monkeypatch):
    _engine, tenant, first = database
    app, _state, factory, second = await app_for(database, monkeypatch)
    base = "/attack-paths/environment-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        body = {"engagement_ids": [str(first), str(second)]}
        completed = uuid.UUID((await client.post(base, json=body)).json()["id"])
        async with factory() as db:
            await compute_environment(db, completed, tenant)
            await db.commit()
        failed = uuid.UUID((await client.post(base, json=body)).json()["id"])
        async with factory() as db:
            row = await db.get(EnvironmentAssessment, failed)
            row.status = "failed"
            row.failure_code = "compute_failed"
            await db.commit()
        result = (
            await client.get(base, params={"engagement_ids": f"{first},{second}"})
        ).json()
        assert result["latest_request"]["id"] == str(failed)
        assert result["latest_request"]["status"] == "failed"
        assert result["last_completed"]["id"] == str(completed)


@pytest.mark.asyncio
async def test_actual_stored_route_projection_is_sealed_scoped_and_always_possible(
    database, monkeypatch
):
    from app.models.finding import Finding
    from app.models.asset import Asset
    from app.models.attack_path import AttackPath

    engine, tenant, first = database
    app, _state, factory, second = await app_for(database, monkeypatch)
    entry = uuid.uuid4()
    async with factory() as db:
        target = (
            await db.execute(select(Finding).where(Finding.engagement_id == first))
        ).scalar_one()
        foreign = (
            await db.execute(select(Finding).where(Finding.engagement_id == second))
        ).scalar_one()
        asset = await db.get(Asset, target.asset_id)
        asset.criticality = "critical"
        target.verification_state = "confirmed"
        target.remediation = (
            "Restrict access to approved services.\nRecheck the same listener."
        )
        db.add(Asset(id=entry, engagement_id=first, hostname="entry-location"))
        edge = {
            "source": str(entry),
            "target": str(target.asset_id),
            "finding": str(target.id),
            "basis": "observed",
            "exploited": True,
        }
        db.add(
            AttackPath(
                engagement_id=first,
                path_nodes=[str(entry), str(target.asset_id)],
                path_edges=[edge, edge, {**edge, "finding": str(foreign.id)}],
            )
        )
        target_id = target.id
        await db.commit()
    base = "/attack-paths/environment-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        created = uuid.UUID(
            (
                await client.post(
                    base, json={"engagement_ids": [str(first), str(second)]}
                )
            ).json()["id"]
        )
        async with factory() as db:
            target = await db.get(Finding, target_id)
            target.remediation = "Changed after the cut"
            await db.commit()
            await compute_environment(db, created, tenant)
            await db.commit()
        result = (await client.get(base + f"/{created}")).json()
        graph = result["route_graph"]
        assert len(graph["edges"]) == 1
        assert graph["edges"][0]["status"] == "theoretical"
        assert graph["omittedConnections"] == 1
        finding = graph["findings"][f"{first}:{target_id}"]
        assert finding["findingConfirmed"] is True
        assert finding["fixSteps"][0] == "Restrict access to approved services."
        assert result["snapshot"]["requires_reassessment"] is False
        repeated = uuid.UUID(
            (
                await client.post(
                    base, json={"engagement_ids": [str(second), str(first)]}
                )
            ).json()["id"]
        )
        async with factory() as db:
            await compute_environment(db, repeated, tenant)
            await db.commit()
        history = (
            await client.get(base, params={"engagement_ids": f"{second},{first}"})
        ).json()
        assert [r["id"] for r in history["completed_history"]] == [
            str(repeated),
            str(created),
        ]


@pytest.mark.asyncio
async def test_different_worker_assembly_cannot_publish_a_mixed_model_result(
    database, monkeypatch
):
    from app.services import environment_assessments as service

    _engine, tenant, first = database
    app, _state, factory, second = await app_for(database, monkeypatch)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        created = uuid.UUID(
            (
                await client.post(
                    "/attack-paths/environment-assessments",
                    json={"engagement_ids": [str(first), str(second)]},
                )
            ).json()["id"]
        )
        monkeypatch.setattr(service, "ASSEMBLY_DIGEST", "0" * 64)
        async with factory() as db:
            with pytest.raises(ValueError, match="model_mismatch"):
                await service.compute_environment(db, created, tenant)
            await db.rollback()
            row = await db.get(EnvironmentAssessment, created)
            assert row.status == "queued" and row.result_document is None


@pytest.mark.asyncio
async def test_scope_membership_role_revocation_and_untrusted_body(
    database, monkeypatch
):
    engine, tenant, first = database
    app, _state, _factory, second = await app_for(database, monkeypatch)
    base = "/attack-paths/environment-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        assert (
            await client.post(
                base, json={"engagement_ids": [str(first), str(uuid.uuid4())]}
            )
        ).status_code == 404
        assert (
            await client.post(base, json={"engagement_ids": [str(first), str(first)]})
        ).status_code == 422
        assert (
            await client.post(
                base, json={"engagement_ids": [str(first)], "evidence": ["invented"]}
            )
        ).status_code == 422
        created = (
            await client.post(base, json={"engagement_ids": [str(first), str(second)]})
        ).json()
        async with engine.begin() as db:
            await db.execute(
                text("UPDATE users SET is_active=false WHERE id=:id"),
                {"id": uuid.uuid5(tenant, "test-operator")},
            )
        assert (await client.get(base + f"/{created['id']}")).status_code == 403


@pytest.mark.asyncio
async def test_combined_budget_rolls_back_sources_and_completed_manifest_is_immutable(
    database, monkeypatch
):
    from app.services import environment_assessments as service

    engine, tenant, first = database
    app, _state, factory, second = await app_for(database, monkeypatch)
    base = "/attack-paths/environment-assessments"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        created = uuid.UUID(
            (
                await client.post(
                    base, json={"engagement_ids": [str(first), str(second)]}
                )
            ).json()["id"]
        )
        async with factory() as db:
            await compute_environment(db, created, tenant)
            await db.commit()
        monkeypatch.setattr(service, "MAX_SELECTED_INPUT_BYTES", 16)
        assert (
            await client.post(base, json={"engagement_ids": [str(first), str(second)]})
        ).status_code == 413
        assert (await client.get(base + f"/{created}")).json()["snapshot"][
            "status"
        ] == "completed"
        async with engine.begin() as db:
            with pytest.raises(DBAPIError, match="immutable"):
                await db.execute(
                    text(
                        "UPDATE environment_assessments SET engagement_ids=ARRAY[CAST(:id AS uuid)] WHERE id=:snapshot"
                    ),
                    {"id": first, "snapshot": created},
                )
