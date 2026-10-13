import json
import os
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest
from sqlalchemy import text

from app.routers import attack_paths as legacy
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


@pytest.mark.asyncio
async def test_reads_never_refresh_and_target_refresh_preserves_other_goals(
    database, monkeypatch
):
    engine, tenant, engagement = database
    src, target_a, target_b = [uuid.uuid4() for _ in range(3)]
    async with engine.begin() as db:
        for asset in (src, target_a, target_b):
            await db.execute(
                text("INSERT INTO assets (id,engagement_id) VALUES (:id,:eng)"),
                {"id": asset, "eng": engagement},
            )
        for target in (target_a, target_b):
            await db.execute(
                text(
                    "INSERT INTO attack_paths (engagement_id,path_nodes,risk_score) VALUES (:eng,ARRAY[CAST(:src AS uuid),CAST(:target AS uuid)],10)"
                ),
                {"eng": engagement, "src": str(src), "target": str(target)},
            )
    app, _, _ = _test_app(engine, tenant, engagement, monkeypatch)
    app.include_router(legacy.router)
    analyzer = SimpleNamespace(
        find_paths_to_target=lambda _: [],
        identify_chokepoints=lambda _: [],
        choke_analysis=lambda _: {},
        diagnose=lambda _: {"reasons": ["synthetic empty model"]},
    )
    build = AsyncMock(return_value=(analyzer, None))
    monkeypatch.setattr(legacy, "_build_analyzer", build)
    base = f"/engagements/{engagement}/attack-paths"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        read = await client.get(base)
        assert read.status_code == 200
        assert read.json()["total"] == 2
        assert read.json()["coverage"] == "partial"
        assert read.json()["model_status"] == "legacy_heuristic"
        assert build.await_count == 0
        assert (await client.get(base + "?refresh=true")).status_code == 405
        assert build.await_count == 0
        filtered = await client.get(base + f"?target_asset_id={target_a}")
        assert filtered.json()["total"] == 1
        refreshed = await client.post(base + f"/refresh?target_asset_id={target_a}")
        assert refreshed.status_code == 200, refreshed.text
        remaining = (await client.get(base)).json()
        assert remaining["total"] == 1
        assert remaining["items"][0]["target"] == str(target_b)


@pytest.mark.asyncio
async def test_legacy_graph_live_role_and_target_scope(database, monkeypatch):
    engine, tenant, engagement = database
    app, _, _ = _test_app(engine, tenant, engagement, monkeypatch)
    app.include_router(legacy.router)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        assert (
            await client.get(f"/engagements/{engagement}/blast-radius/{uuid.uuid4()}")
        ).status_code == 404
        async with engine.begin() as db:
            await db.execute(
                text("UPDATE users SET role='client' WHERE id=:id"),
                {"id": uuid.uuid5(tenant, "test-operator")},
            )
        for suffix in ("attack-paths", "attack-graph", "chokepoints"):
            assert (
                await client.get(f"/engagements/{engagement}/{suffix}")
            ).status_code == 403


@pytest.mark.asyncio
async def test_enabling_finding_resolution_cannot_disclose_foreign_or_wrong_asset_records(
    database, monkeypatch
):
    engine, tenant, engagement = database
    valid = await add_finding(engine, engagement)
    wrong_asset = await add_finding(engine, engagement)
    other_engagement = uuid.uuid4()
    async with engine.begin() as db:
        await db.execute(
            text(
                "INSERT INTO engagements (id,tenant_id,name) VALUES (:id,:tenant,'other scope')"
            ),
            {"id": other_engagement, "tenant": tenant},
        )
    foreign = await add_finding(engine, other_engagement)
    src, path_id = uuid.uuid4(), uuid.uuid4()
    async with engine.begin() as db:
        target = (
            await db.execute(
                text("SELECT asset_id FROM findings WHERE id=:id"), {"id": valid}
            )
        ).scalar_one()
        await db.execute(
            text("INSERT INTO assets (id,engagement_id) VALUES (:id,:eng)"),
            {"id": src, "eng": engagement},
        )
        await db.execute(
            text("UPDATE findings SET title='PRIVATE foreign title' WHERE id=:id"),
            {"id": foreign},
        )
        await db.execute(
            text("UPDATE findings SET title='PRIVATE wrong-asset title' WHERE id=:id"),
            {"id": wrong_asset},
        )
        edges = [
            {
                "source": str(src),
                "target": str(target),
                "finding": str(fid),
                "technique": "SAME_SUBNET",
                "basis": "assumed",
            }
            for fid in (valid, wrong_asset, foreign)
        ]
        await db.execute(
            text(
                "INSERT INTO attack_paths (id,engagement_id,path_nodes,path_edges,risk_score) VALUES (:id,:eng,ARRAY[CAST(:src AS uuid),CAST(:target AS uuid)],ARRAY(SELECT jsonb_array_elements(CAST(:edges AS jsonb))),10)"
            ),
            {
                "id": path_id,
                "eng": engagement,
                "src": str(src),
                "target": str(target),
                "edges": json.dumps(edges),
            },
        )
    app, _, _ = _test_app(engine, tenant, engagement, monkeypatch)
    app.include_router(legacy.router)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(f"/engagements/{engagement}/attack-paths/{path_id}")
        assert response.status_code == 200
        hops = response.json()["hops"]
        assert hops[0]["finding"]["id"] == str(valid)
        assert (
            hops[0]["finding"]["metadata_basis"]
            == "current_scoped_finding_not_snapshot_proof"
        )
        assert all(h["finding"] is None for h in hops[1:])
        assert "PRIVATE" not in response.text
        assert str(foreign) not in response.text
        assert str(wrong_asset) not in response.text
