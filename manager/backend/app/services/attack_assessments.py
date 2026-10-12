"""Scoped frozen-input snapshots; ordinary reads never trigger computation."""

import hashlib
import json
import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy import String, case, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.graph.finding_readiness import NORMALIZATION_VERSION, finding_readiness
from app.models.asset import Asset
from app.models.attack_assessment import AttackAssessmentSnapshot
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.service import Service
from app.utils.db import get_or_404

MAX_FINDINGS = 1000
MAX_ASSETS = 2000
MAX_SERVICES = 5000
MAX_INPUT_BYTES = 2 * 1024 * 1024
TOPIC_ATTACK_ASSESSMENT = "attack_assessment.compute"


def _record(row) -> dict:
    return {
        key: value.isoformat()
        if isinstance(value, datetime)
        else str(value)
        if isinstance(value, uuid.UUID)
        else value.value
        if hasattr(value, "value")
        else value
        for key, value in row._mapping.items()
    }


async def capture_snapshot(
    db: AsyncSession, tenant_id: uuid.UUID, engagement_id: uuid.UUID
) -> AttackAssessmentSnapshot:
    """Call before any other DB statement on this fresh request session."""
    await db.connection(execution_options={"isolation_level": "REPEATABLE READ"})
    await get_or_404(db, Engagement, engagement_id, tenant_id)
    as_of = (await db.execute(select(func.now()))).scalar_one()
    evidence_length = func.octet_length(cast(Finding.evidence, String))
    fq = (
        select(
            Finding.id,
            Finding.asset_id,
            Finding.title,
            Finding.severity,
            Finding.status,
            Finding.updated_at,
            case((evidence_length <= 65536, Finding.evidence), else_=None).label(
                "evidence"
            ),
            (evidence_length > 65536).label("evidence_limited"),
        )
        .where(Finding.engagement_id == engagement_id)
        .order_by(Finding.id)
        .limit(MAX_FINDINGS + 1)
    )
    aq = (
        select(
            Asset.id, Asset.hostname, Asset.ip_address, Asset.owner, Asset.updated_at
        )
        .where(Asset.engagement_id == engagement_id)
        .order_by(Asset.id)
        .limit(MAX_ASSETS + 1)
    )
    sq = (
        select(
            Service.id,
            Service.asset_id,
            Service.port,
            Service.protocol,
            Service.service_name,
            Service.product,
            Service.updated_at,
        )
        .join(Asset, Service.asset_id == Asset.id)
        .where(Asset.engagement_id == engagement_id)
        .order_by(Service.id)
        .limit(MAX_SERVICES + 1)
    )
    findings = [_record(r) for r in (await db.execute(fq)).all()]
    assets = [_record(r) for r in (await db.execute(aq)).all()]
    services = [_record(r) for r in (await db.execute(sq)).all()]
    total = (
        await db.execute(
            select(func.count())
            .select_from(Finding)
            .where(Finding.engagement_id == engagement_id)
        )
    ).scalar_one()
    truncated = (
        len(findings) > MAX_FINDINGS
        or len(assets) > MAX_ASSETS
        or len(services) > MAX_SERVICES
    )
    document = {
        "tenant_id": str(tenant_id),
        "engagement_id": str(engagement_id),
        "capture_protocol": "materialized_repeatable_read",
        "effective_as_of": as_of.isoformat(),
        "known_at_cutoff": as_of.isoformat(),
        "findings": findings[:MAX_FINDINGS],
        "assets": assets[:MAX_ASSETS],
        "services": services[:MAX_SERVICES],
        "total_findings": total,
        "input_truncated": truncated,
        "inventory_coverage": "partial",
        "reachability_coverage": "not_normalized",
        "read_evidence_coverage": "not_normalized",
        "normalization_version": NORMALIZATION_VERSION,
        "rule_pack_version": "binding-contract@1",
        "rule_artifact_sha256": hashlib.sha256(
            Path(__file__)
            .resolve()
            .parents[1]
            .joinpath("graph/local_rule.py")
            .read_bytes()
        ).hexdigest(),
    }
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":"))
    if len(encoded.encode()) > MAX_INPUT_BYTES:
        raise ValueError("snapshot_input_size_limit")
    snapshot = AttackAssessmentSnapshot(
        tenant_id=tenant_id,
        engagement_id=engagement_id,
        input_hash=hashlib.sha256(encoded.encode()).hexdigest(),
        effective_as_of=as_of,
        known_at_cutoff=as_of,
        normalization_version=NORMALIZATION_VERSION,
        rule_pack_version=document["rule_pack_version"],
        rule_artifact_sha256=document["rule_artifact_sha256"],
        input_document=document,
    )
    db.add(snapshot)
    await db.flush()
    # Import after creation: producer/outbox share the request transaction.
    from app.workers.outbox import enqueue

    enqueue(
        db,
        TOPIC_ATTACK_ASSESSMENT,
        engagement_id=engagement_id,
        payload={"snapshot_id": str(snapshot.id), "tenant_id": str(tenant_id)},
    )
    return snapshot


def compute_readiness(document: dict) -> dict:
    if document.get("normalization_version") != NORMALIZATION_VERSION:
        raise ValueError("unsupported_normalization_version")
    assets = {a["id"]: a for a in document["assets"]}
    services = {s["id"]: s for s in document["services"]}
    return {
        "assessments": [
            finding_readiness(f, assets, services) for f in document["findings"]
        ],
        "total_findings": document["total_findings"],
        "assessed_findings": len(document["findings"]),
        "compute": "truncated"
        if document["input_truncated"]
        else "complete_for_readiness",
        "coverage": "partial",
        "rule_activation": "experimental_not_activated",
        "unsupported_families": ["multi_host_transfer", "ad_identity", "cloud_iam"],
    }


async def compute_snapshot(
    db: AsyncSession, snapshot_id: uuid.UUID, tenant_id: uuid.UUID
) -> None:
    snapshot = (
        await db.execute(
            select(AttackAssessmentSnapshot)
            .where(
                AttackAssessmentSnapshot.id == snapshot_id,
                AttackAssessmentSnapshot.tenant_id == tenant_id,
            )
            .with_for_update()
        )
    ).scalar_one_or_none()
    if snapshot is None or snapshot.status == "completed":
        return
    encoded = json.dumps(snapshot.input_document, sort_keys=True, separators=(",", ":"))
    if hashlib.sha256(encoded.encode()).hexdigest() != snapshot.input_hash:
        raise ValueError("snapshot_input_integrity_mismatch")
    snapshot.result_document = compute_readiness(snapshot.input_document)
    snapshot.status = "completed"
    snapshot.failure_code = None
    await db.flush()
