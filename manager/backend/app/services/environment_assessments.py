"""Coherent selected-source manifest and conservative environment projection."""

import hashlib
import json
import uuid

from sqlalchemy import select

from app.graph.environment_engine import (
    ENGINE_DIGEST,
    ENGINE_VERSION,
    derive_environment_paths,
)
from app.graph.finding_readiness import NORMALIZATION_VERSION
from app.models.attack_assessment import AttackAssessmentSnapshot
from app.models.engagement import Engagement
from app.models.environment_assessment import EnvironmentAssessment
from app.services.attack_assessments import capture_snapshot, compute_readiness

TOPIC = "environment_assessment.compute"
MAX_SELECTED_INPUT_BYTES = 4 * 1024 * 1024
MAX_ITEMS = 1000


def digest(document):
    return hashlib.sha256(
        json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


async def capture_environment(db, tenant_id, engagement_ids, key):
    ids = sorted(set(engagement_ids), key=str)
    if not 1 <= len(ids) <= 20:
        raise ValueError("selection_limit")
    if key:
        existing = (
            await db.execute(
                select(EnvironmentAssessment).where(
                    EnvironmentAssessment.tenant_id == tenant_id,
                    EnvironmentAssessment.idempotency_key == key,
                )
            )
        ).scalar_one_or_none()
        if existing:
            if existing.engagement_ids != ids:
                raise ValueError("request_key_scope_mismatch")
            return existing
    names = dict(
        (
            await db.execute(
                select(Engagement.id, Engagement.name).where(
                    Engagement.tenant_id == tenant_id, Engagement.id.in_(ids)
                )
            )
        ).all()
    )
    if set(names) != set(ids):
        raise ValueError("selection_not_authorized")
    sources = []
    size = 0
    as_of = None
    for engagement_id in ids:
        source = await capture_snapshot(db, tenant_id, engagement_id)
        size += len(json.dumps(source.input_document).encode())
        if size > MAX_SELECTED_INPUT_BYTES:
            raise ValueError("selection_input_size_limit")
        if as_of is not None and as_of != source.effective_as_of:
            raise ValueError("incoherent_source_cut")
        as_of = source.effective_as_of
        sources.append(
            {
                "engagement_id": str(engagement_id),
                "engagement_name": names[engagement_id],
                "snapshot_id": str(source.id),
                "input_hash": source.input_hash,
            }
        )
    document = {
        "tenant_id": str(tenant_id),
        "engagement_ids": [str(i) for i in ids],
        "sources": sources,
        "effective_as_of": as_of.isoformat(),
        "engine_version": ENGINE_VERSION,
        "engine_digest": ENGINE_DIGEST,
        "normalization_version": NORMALIZATION_VERSION,
        "capture_protocol": "materialized_repeatable_read",
    }
    row = EnvironmentAssessment(
        tenant_id=tenant_id,
        engagement_ids=ids,
        idempotency_key=key,
        effective_as_of=as_of,
        input_hash=digest(document),
        input_document=document,
    )
    db.add(row)
    await db.flush()
    from app.workers.outbox import enqueue

    enqueue(
        db,
        TOPIC,
        engagement_id=ids[0],
        payload={"assessment_id": str(row.id), "tenant_id": str(tenant_id)},
    )
    return row


async def compute_environment(db, assessment_id, tenant_id):
    row = (
        await db.execute(
            select(EnvironmentAssessment)
            .where(
                EnvironmentAssessment.id == assessment_id,
                EnvironmentAssessment.tenant_id == tenant_id,
            )
            .with_for_update()
        )
    ).scalar_one_or_none()
    if row is None or row.status == "completed":
        return
    manifest = row.input_document
    if (
        digest(manifest) != row.input_hash
        or manifest["engine_digest"] != ENGINE_DIGEST
        or manifest.get("normalization_version") != NORMALIZATION_VERSION
    ):
        raise ValueError("environment_input_or_model_mismatch")
    items, systems, total = [], [], 0
    truncated = False
    for ref in manifest["sources"]:
        source = (
            await db.execute(
                select(AttackAssessmentSnapshot).where(
                    AttackAssessmentSnapshot.id == uuid.UUID(ref["snapshot_id"]),
                    AttackAssessmentSnapshot.tenant_id == tenant_id,
                    AttackAssessmentSnapshot.engagement_id
                    == uuid.UUID(ref["engagement_id"]),
                )
            )
        ).scalar_one_or_none()
        if (
            source is None
            or source.input_hash != ref["input_hash"]
            or digest(source.input_document) != source.input_hash
            or source.effective_as_of != row.effective_as_of
        ):
            raise ValueError("environment_source_integrity_mismatch")
        readiness = compute_readiness(source.input_document)
        total += readiness["total_findings"]
        truncated |= readiness["compute"] == "truncated"
        for item in readiness["assessments"]:
            if len(items) == MAX_ITEMS:
                truncated = True
                break
            items.append(
                {
                    **item,
                    "engagement_id": ref["engagement_id"],
                    "engagement_name": ref["engagement_name"],
                }
            )
        for asset in source.input_document["assets"]:
            if len(systems) < 2000:
                systems.append(
                    {
                        "id": f"{ref['engagement_id']}:{asset['id']}",
                        "asset_id": asset["id"],
                        "engagement_id": ref["engagement_id"],
                        "label": asset.get("hostname")
                        or asset.get("ip_address")
                        or asset["id"],
                    }
                )
            else:
                truncated = True
    # The repository does not yet contain a reviewed observation-rich adapter.
    # Empty normalized transitions remain empty, regardless of neighboring CVEs.
    engine = derive_environment_paths(
        (),
        tenant_id=tenant_id,
        environment_id=row.id,
        engagement_ids=frozenset(row.engagement_ids),
        as_of=row.effective_as_of,
        known_at=row.effective_as_of,
    )
    row.result_document = {
        "items": items,
        "systems": systems,
        "total_findings": total,
        "engine": engine,
        "compute": "truncated" if truncated else "complete_for_readiness",
        "coverage": "partial",
        "bridges": [],
        "bridge_state": "not_normalized",
        "identity_policy": "engagement_qualified_no_automatic_merge",
        "sources": manifest["sources"],
        "missing_relationships": [
            "directed_reachability",
            "service_instance_identity",
            "credential_or_permission_transfer",
            "valid_observation_lineage",
            "explicit_environment_membership",
        ],
    }
    row.status = "completed"
    row.failure_code = None
    await db.flush()
