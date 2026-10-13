"""Reproducible synthetic budgets; optional DB is restricted to the task test DB.

Run from backend: python scripts/benchmark_attack_readiness.py
Set ATTACK_PATH_TEST_DATABASE_URL to include isolated capture measurements.
Outputs JSON; creates and deletes only its own synthetic tenant in that DB.
"""

import asyncio
import json
import os
import platform
import statistics
import time
import tracemalloc
import uuid
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.graph.local_assessment import evaluate_local_alternatives
from app.graph.local_rule import LocalRuleInput
from app.services.attack_assessments import capture_snapshot, compute_readiness


def measure(function):
    samples = []
    peak = 0
    for _ in range(3):
        tracemalloc.start()
        started = time.perf_counter()
        result = function()
        samples.append(time.perf_counter() - started)
        peak = max(peak, tracemalloc.get_traced_memory()[1])
        tracemalloc.stop()
    return result, {
        "median_seconds": round(statistics.median(samples), 4),
        "peak_python_bytes": peak,
    }


async def capture_budget(url):
    parsed = make_url(url)
    if (
        parsed.host not in {"127.0.0.1", "localhost"}
        or parsed.port != 25432
        or parsed.database != "attack_path_test"
    ):
        raise RuntimeError("refusing database outside isolated task test scope")
    engine = create_async_engine(url)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    tenant, engagement, asset, service = [uuid.uuid4() for _ in range(4)]
    try:
        async with engine.begin() as db:
            await db.execute(
                text("INSERT INTO tenants (id,name) VALUES (:id,'synthetic-budget')"),
                {"id": tenant},
            )
            await db.execute(
                text(
                    "INSERT INTO engagements (id,tenant_id,name) VALUES (:id,:tenant,'synthetic-budget')"
                ),
                {"id": engagement, "tenant": tenant},
            )
            await db.execute(
                text(
                    "INSERT INTO assets (id,engagement_id,hostname) VALUES (:id,:eng,'synthetic-budget')"
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
                    "INSERT INTO findings (id,engagement_id,asset_id,title,severity,evidence) SELECT gen_random_uuid(),:eng,:asset,'synthetic budget finding','high',jsonb_build_object('service_id',CAST(:service AS text)) FROM generate_series(1,1000)"
                ),
                {"eng": engagement, "asset": asset, "service": str(service)},
            )
        samples = []
        peak = 0
        for _ in range(3):
            async with factory() as db:
                tracemalloc.start()
                started = time.perf_counter()
                row = await capture_snapshot(db, tenant, engagement)
                samples.append(time.perf_counter() - started)
                peak = max(peak, tracemalloc.get_traced_memory()[1])
                tracemalloc.stop()
                document = row.input_document
                await db.rollback()
        result, compute = measure(lambda: compute_readiness(document))
        return {
            "findings": 1000,
            "capture_median_seconds": round(statistics.median(samples), 4),
            "capture_peak_python_bytes": peak,
            "readiness": compute,
            "supported_proofs": sum(
                r["supported_proofs"] for r in result["assessments"]
            ),
        }
    finally:
        async with engine.begin() as db:
            await db.execute(
                text("DELETE FROM outbox_events WHERE engagement_id=:id"),
                {"id": engagement},
            )
            await db.execute(text("DELETE FROM tenants WHERE id=:id"), {"id": tenant})
        await engine.dispose()


def main():
    example = (
        Path(__file__).resolve().parents[3]
        / "docs/planning/2026-10-13-attack-path-local-rule.example.json"
    )
    value = LocalRuleInput.model_validate_json(example.read_text())
    report = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "samples": 3,
        "allocation_measurement": "tracemalloc; excludes prebuilt input objects, not process RSS",
        "local": [],
    }
    for count in (10, 100, 1000, 10000):
        values = tuple(
            value.model_copy(
                update={
                    "finding": value.finding.model_copy(
                        update={"id": uuid.uuid5(value.finding.id, str(i))}
                    )
                }
            )
            for i in range(count)
        )
        result, metrics = measure(lambda values=values: evaluate_local_alternatives(values))
        report["local"].append(
            {
                "input_bundles": count,
                **metrics,
                "compute": result.goal.compute,
                "supported_proofs": result.goal.supported_proofs,
                "displayed": len(result.routes),
            }
        )
    result, metrics = measure(lambda: evaluate_local_alternatives((value,) * 10000))
    report["duplicates"] = {
        **metrics,
        "input_bundles": 10000,
        "supported_proofs": result.goal.supported_proofs,
        "compute": result.goal.compute,
    }
    if url := os.getenv("ATTACK_PATH_TEST_DATABASE_URL"):
        report["database"] = asyncio.run(capture_budget(url))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
