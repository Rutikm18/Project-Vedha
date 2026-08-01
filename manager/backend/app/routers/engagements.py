import json
import os
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import func, select

from app.auth.rbac import require_role
from app.dependencies import DB, ReadDB, AuthUser
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import AssetType, EngagementStatus, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.models.scan_job import ScanJob
from app.models.scan_result import ScanResult
from app.models.service import Service
from app.schemas.common import PaginatedResponse, paginate
from app.schemas.asset import AssetIn, AssetOut, BulkAssetImportResult
from app.schemas.engagement import (
    EngagementCreate, EngagementDetail, EngagementOut, FindingSummary,
    validate_engagement_dates, validate_scope_entries,
)
from app.utils.csv_parser import parse_csv_assets
from app.utils.db import get_or_404
from app.utils.pagination import paginate_query

router = APIRouter(prefix="/engagements", tags=["engagements"])
logger = structlog.get_logger()


def _overview_cache_key(tenant_id) -> str:
    # Must match the key read by GET /engagements/overview.
    return f"cache:eng_overview:{tenant_id}"


async def _compute_overview(db, tenant_id) -> list:
    """Shared aggregation — used by both the cached read path (ReadDB) and the
    write-through refresh after a mutation (primary DB, same txn as the write).

    A session always sees its own uncommitted writes, so computing on the primary
    after a mutation eliminates the replica-lag race entirely.  The old approach
    (cache DELETE + force next request to re-query ReadDB) was actively harmful:
    the replica might not have caught up yet, and the stale result would then be
    re-cached for a fresh 15s TTL.
    """
    engs = (await db.execute(
        select(Engagement).where(Engagement.tenant_id == tenant_id)
        .order_by(Engagement.created_at.desc())
    )).scalars().all()
    if not engs:
        return []

    asset_rows = (await db.execute(
        select(Asset.engagement_id, func.count(Asset.id))
        .where(Asset.engagement_id.in_([e.id for e in engs]))
        .group_by(Asset.engagement_id)
    )).all()
    asset_by_eng = {eid: n for eid, n in asset_rows}

    frows = (await db.execute(
        select(Finding.engagement_id, Finding.severity, Finding.status, func.count(Finding.id))
        .where(Finding.engagement_id.in_([e.id for e in engs]))
        .group_by(Finding.engagement_id, Finding.severity, Finding.status)
    )).all()

    agg: dict = {}
    for eid, sev, st, cnt in frows:
        a = agg.setdefault(eid, {"sev": {s.value: 0 for s in FindingSeverity},
                                 "total": 0, "open": 0, "remediated": 0})
        a["sev"][sev.value] += cnt
        a["total"] += cnt
        if st in (FindingStatus.open, FindingStatus.confirmed):
            a["open"] += cnt
        elif st == FindingStatus.remediated:
            a["remediated"] += cnt

    out = []
    for e in engs:
        a = agg.get(e.id)
        sev = a["sev"] if a else {s.value: 0 for s in FindingSeverity}
        detail = EngagementDetail.model_validate(e)
        detail.asset_count = asset_by_eng.get(e.id, 0)
        detail.finding_summary = FindingSummary(
            total=a["total"] if a else 0,
            critical=sev["critical"], high=sev["high"], medium=sev["medium"],
            low=sev["low"], info=sev["info"],
            open=a["open"] if a else 0, remediated=a["remediated"] if a else 0,
        )
        out.append(detail)
    return out


async def _refresh_overview_cache(db, tenant_id) -> None:
    """Write-through cache refresh on the WRITE session, right after flush.

    Replaces _bust_overview_cache.  Computing here, on the primary, inside the
    same transaction as the write, sidesteps replica lag entirely.  A session
    always sees its own writes — committed or not.

    Best-effort: a cache write failure must never fail the mutation.
    """
    try:
        rows = await _compute_overview(db, tenant_id)
        from app.dependencies import get_redis
        redis = await get_redis()
        await redis.set(
            _overview_cache_key(tenant_id),
            json.dumps([r.model_dump(mode="json") for r in rows]),
            ex=15,
        )
    except Exception:  # noqa: BLE001 — must never fail the mutation
        logger.warning("overview_cache_refresh_failed", tenant_id=str(tenant_id), exc_info=True)


# ── POST /engagements ─────────────────────────────────────────────────────────

@router.post("/{engagement_id}/re-detect", status_code=status.HTTP_202_ACCEPTED,
             summary="Re-run detection on stored facts (no re-scan) — P3-#10")
async def re_detect(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
    background_tasks: BackgroundTasks,
):
    """Re-runs the detection pipeline against the CURRENT pinned vuln DB using
    the raw facts already stored in scan_results — without touching the network.
    Use after a vuln-DB snapshot update to surface newly-known CVEs on hosts
    that were scanned days ago. Detection runs as a background job."""
    from app.models.scan_result import ScanResult as _SR
    from app.detection.engine_bridge import run_detection_job

    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    rows = (await db.execute(
        select(_SR.facts).where(_SR.engagement_id == engagement_id)
    )).scalars().all()
    facts: list = [f for batch in rows if batch for f in batch]
    if not facts:
        return {"requeued": False, "fact_count": 0,
                "detail": "No stored facts for this engagement — run a scan first."}

    background_tasks.add_task(
        run_detection_job, engagement_id,
        {"facts": facts, "scan_type": "re-detect", "engine": "scanner_module"})
    return {"requeued": True, "fact_count": len(facts),
            "detail": "Re-detection queued against the current vuln DB."}


# ── Import a probe scan file → detection + attack graph ───────────────────────

# Upper bound on an uploaded scan file. Generous (a 2000-fact bundle is well
# under 1 MB) but caps a malicious/accidental multi-GB upload that would
# otherwise be buffered into memory by file.read(). Tune via env if huge scans
# ever need more headroom.
_MAX_IMPORT_BYTES = int(os.environ.get("IMPORT_MAX_BYTES", str(50 * 1024 * 1024)))


async def _read_capped(file: UploadFile, limit: int) -> bytes:
    """Read an UploadFile in chunks, aborting with 413 once `limit` is exceeded
    — so an oversized upload is rejected without buffering the whole payload."""
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = await file.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > limit:
            raise HTTPException(
                status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                f"Scan file exceeds the {limit // (1024 * 1024)} MB import limit.")
        chunks.append(chunk)
    return b"".join(chunks)


def _parse_probe_file(raw: str) -> tuple[list[dict], str | None]:
    """Parse a probe export into (facts, scan_type).

    Accepts two shapes the probe can emit:
      • .json bundle  — `{"facts": [...], "scan_type": ..., "engine": ...}`
        (exactly what `agent.engine.run_scan` returns).
      • .jsonl stream — one ScanResult fact per line (the probe's native
        streaming format for very large scans).
    Classification: if the whole body parses as ONE JSON value it's classified
    definitively — a `facts` array → bundle, a bare list → array of facts, a
    single fact-shaped object (has `scanner`/`target`) → one fact. Any OTHER
    single JSON object (e.g. the wrong file) yields no facts → caller returns
    400 rather than silently storing a junk "fact". Only content that ISN'T a
    single JSON value falls through to per-line JSONL parsing.
    """
    raw = raw.lstrip("﻿").strip()  # tolerate a UTF-8 BOM (Windows editors)
    if not raw:
        return [], None
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        obj = None
    if obj is not None:
        if isinstance(obj, dict):
            if isinstance(obj.get("facts"), list):
                return obj["facts"], obj.get("scan_type")
            if obj.get("scanner") or obj.get("target"):  # a single fact object
                return [obj], obj.get("scan_type")
            return [], None  # valid JSON, but neither a bundle nor a fact → reject
        if isinstance(obj, list):  # a bare JSON array of facts
            return [f for f in obj if isinstance(f, dict)], None
        return [], None  # scalar JSON (number/string/bool) → reject

    facts: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            fact = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(fact, dict):
            facts.append(fact)
    return facts, None


async def _promote_from_facts(db, engagement_id: uuid.UUID, facts: list[dict]) -> int:
    """Upsert assets (and their services) from raw ScanResult facts.

    Mirrors `agents._promote_assets` but reads the ScanResult shape
    (`{target, port, proto, data, ...}`) instead of the host/ports shape, so the
    attack graph has asset/service nodes even for targets that produced no
    finding. Keyed by (engagement, ip) and (asset, port, protocol) — idempotent
    across repeated imports. Returns the number of newly-created assets.
    """
    promoted = 0
    assets: dict[str, Asset] = {}
    # In-batch service cache keyed (asset_id, port, proto). A single import can
    # carry MULTIPLE facts for the same host:port (e.g. ssh_inventory + a banner
    # on :22, or repeated lines) — the DB SELECT below can't see pending,
    # unflushed inserts, so without this cache the second such fact would add a
    # duplicate Service and blow the uq_service_asset_port_proto constraint.
    services: dict[tuple, Service] = {}
    for f in facts:
        target = f.get("target")
        if not target:
            continue
        host = target.split(":", 1)[0] if target.count(":") == 1 else target
        asset = assets.get(host)
        if asset is None:
            asset = (await db.execute(
                select(Asset).where(Asset.engagement_id == engagement_id,
                                    Asset.ip_address == host)
            )).scalar_one_or_none()
            if asset:
                asset.last_seen = datetime.now(timezone.utc)
            else:
                asset = Asset(engagement_id=engagement_id, ip_address=host,
                              asset_type=AssetType.server,
                              last_seen=datetime.now(timezone.utc))
                db.add(asset)
                await db.flush()
                promoted += 1
            assets[host] = asset

        port_no = f.get("port")
        if port_no is None:
            continue
        proto = f.get("proto") or "tcp"
        data = f.get("data") or {}
        key = (asset.id, port_no, proto)
        svc = services.get(key)
        if svc is None:
            svc = (await db.execute(
                select(Service).where(Service.asset_id == asset.id,
                                      Service.port == port_no, Service.protocol == proto)
            )).scalar_one_or_none()
            if svc is None:
                svc = Service(asset_id=asset.id, port=port_no, protocol=proto)
                db.add(svc)
            services[key] = svc
        # later facts for the same port refine fields without inserting again
        svc.service_name = data.get("service") or svc.service_name
        svc.product = data.get("product") or svc.product
        svc.version = data.get("version") or svc.version
    await db.flush()
    return promoted


@router.post(
    "/{engagement_id}/scans/import-facts",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Import a probe scan file (.json bundle or .jsonl) → detection + graph",
)
async def import_facts(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """Offline ingest path: upload a probe's scan export and run it through the
    SAME pipeline the live probe-result path uses — facts are stored durably in
    `scan_results` (so detection can be re-run later), hosts are promoted to
    assets/services, and detection runs as a background job. Once findings and
    assets exist, `GET /engagements/{id}/attack-graph` builds the graph with no
    extra work. Accepts a `.json` bundle or a `.jsonl` fact stream.
    """
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    raw = (await _read_capped(file, _MAX_IMPORT_BYTES)).decode("utf-8", "replace")
    facts, scan_type = _parse_probe_file(raw)
    if not facts:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "No facts found in file — expected a .json bundle with a 'facts' "
            "array or a .jsonl stream of facts.")
    scan_type = scan_type or "import"

    # Durable copy (P3-#10) — keyed by engagement, ready to re-detect later.
    db.add(ScanResult(engagement_id=engagement_id, job_id=None,
                      scan_type=scan_type, fact_count=len(facts), facts=facts))
    await db.flush()

    # Promote hosts → assets/services so the attack graph has nodes, then detect
    # facts → findings off the request path (its own DB session), mirroring the
    # live probe path in routers/agents.submit_job_result.
    promoted = await _promote_from_facts(db, engagement_id, facts)
    await _refresh_overview_cache(db, current_user.tenant_id)  # asset/finding counts changed

    from app.detection.engine_bridge import run_detection_job
    background_tasks.add_task(
        run_detection_job, engagement_id,
        {"facts": facts, "scan_type": scan_type, "engine": "scanner_module"})

    logger.info("engagement.import_facts", engagement_id=str(engagement_id),
                fact_count=len(facts), assets_promoted=promoted)
    return {
        "imported": True,
        "fact_count": len(facts),
        "assets_promoted": promoted,
        "next": f"/engagements/{engagement_id}/attack-graph",
    }


@router.post(
    "",
    response_model=EngagementOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new engagement",
)
async def create_engagement(
    body: EngagementCreate,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    eng = Engagement(
        tenant_id=current_user.tenant_id,
        **body.model_dump(),
    )
    db.add(eng)
    await db.flush()
    await db.refresh(eng)
    await _refresh_overview_cache(db, current_user.tenant_id)
    logger.info("engagement.created", id=str(eng.id), tenant=str(current_user.tenant_id))
    return eng


# ── GET /engagements ──────────────────────────────────────────────────────────

@router.get("", response_model=PaginatedResponse[EngagementOut], summary="List engagements")
async def list_engagements(
    db: DB,
    current_user: AuthUser,
    status_filter: EngagementStatus | None = Query(default=None, alias="status"),
    start_after: str | None = Query(default=None),
    start_before: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    q = select(Engagement).where(Engagement.tenant_id == current_user.tenant_id)

    if status_filter:
        q = q.where(Engagement.status == status_filter)
    if start_after:
        q = q.where(Engagement.start_time >= start_after)
    if start_before:
        q = q.where(Engagement.start_time <= start_before)

    q = q.order_by(Engagement.created_at.desc())
    items, total = await paginate_query(db, q, page, page_size)
    return paginate(items, total, page, page_size)


# ── GET /engagements/{id} ─────────────────────────────────────────────────────

@router.get("/overview", response_model=list[EngagementDetail],
            summary="All engagements WITH counts — one aggregate, no N+1")
async def engagements_overview(db: ReadDB, current_user: AuthUser):
    """P1: kills the BFF N+1 (was list + one detail call per engagement).
    Computes asset + finding-severity counts for ALL engagements in a FIXED
    number of queries (3) regardless of engagement count, by pre-aggregating
    and joining in Python rather than round-tripping per id.
    """
    tid = current_user.tenant_id

    # P2: short-TTL Redis cache on this hot dashboard read. A 15s TTL bounds
    # staleness without fragile write-time invalidation — after a scan,
    # counts refresh within 15s, which is imperceptible for an overview and
    # removes the per-poll DB aggregate load. Per-tenant key.
    from app.dependencies import get_redis
    redis = await get_redis()
    cache_key = _overview_cache_key(tid)
    try:
        hit = await redis.get(cache_key)
        if hit is not None:
            return json.loads(hit)  # list[dict] — FastAPI validates to the response_model
    except Exception:  # noqa: BLE001 — cache must never break the endpoint
        pass

    rows = await _compute_overview(db, tid)
    if not rows:
        return []

    try:  # cache the JSON-serialized models (best-effort)
        await redis.set(cache_key, json.dumps([o.model_dump(mode="json") for o in rows]), ex=15)
    except Exception:  # noqa: BLE001
        pass
    return rows


@router.get("/{engagement_id}", response_model=EngagementDetail, summary="Engagement detail")
async def get_engagement(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    asset_count: int = (
        await db.execute(
            select(func.count(Asset.id)).where(Asset.engagement_id == engagement_id)
        )
    ).scalar_one()

    rows = (
        await db.execute(
            select(Finding.severity, Finding.status, func.count(Finding.id))
            .where(Finding.engagement_id == engagement_id)
            .group_by(Finding.severity, Finding.status)
        )
    ).all()

    sev_counts = {s.value: 0 for s in FindingSeverity}
    open_count = remediated_count = total = 0

    for sev, st, cnt in rows:
        sev_counts[sev.value] = sev_counts.get(sev.value, 0) + cnt
        total += cnt
        if st in (FindingStatus.open, FindingStatus.confirmed):
            open_count += cnt
        elif st == FindingStatus.remediated:
            remediated_count += cnt

    summary = FindingSummary(
        total=total,
        critical=sev_counts["critical"],
        high=sev_counts["high"],
        medium=sev_counts["medium"],
        low=sev_counts["low"],
        info=sev_counts["info"],
        open=open_count,
        remediated=remediated_count,
    )

    detail = EngagementDetail.model_validate(eng)
    detail.asset_count = asset_count
    detail.finding_summary = summary
    return detail


# ── PATCH /engagements/{id} — update fields ───────────────────────────────────

class EngagementUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    status: EngagementStatus | None = None
    scope_cidrs: list[str] | None = None
    excluded_cidrs: list[str] | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    # Partial patch: the provided keys are merged into the existing ROE (see below),
    # so editing e.g. `client` never drops stored `credentials`.
    rules_of_engagement: dict | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("name cannot be blank")
        return value

    @field_validator("scope_cidrs", "excluded_cidrs")
    @classmethod
    def validate_scopes(cls, values: list[str] | None) -> list[str] | None:
        if values is None:
            return None
        return validate_scope_entries(values)

    @model_validator(mode="after")
    def validate_dates(self):
        validate_engagement_dates(self.start_time, self.end_time)
        return self


@router.patch("/{engagement_id}", response_model=EngagementOut, summary="Update engagement fields")
async def update_engagement(
    engagement_id: uuid.UUID,
    body: EngagementUpdate,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    updates = body.model_dump(exclude_unset=True)
    roe_patch = updates.pop("rules_of_engagement", None)
    for field, value in updates.items():
        setattr(eng, field, value)

    # ROE is a JSONB bag of UI-parked fields (client / assessor / description / tags /
    # credentials). A naive assignment would replace the whole bag and lose keys the
    # caller didn't send (notably credentials). Shallow-merge the patch instead.
    if roe_patch is not None:
        eng.rules_of_engagement = {**(eng.rules_of_engagement or {}), **roe_patch}

    await db.flush()
    await db.refresh(eng)
    await _refresh_overview_cache(db, current_user.tenant_id)
    logger.info("engagement.patched", id=str(engagement_id), fields=sorted(updates) + (["roe"] if roe_patch else []))
    return eng


# ── POST /engagements/{id}/assets ─────────────────────────────────────────────

@router.post(
    "/{engagement_id}/assets",
    response_model=BulkAssetImportResult,
    status_code=status.HTTP_201_CREATED,
    summary="Bulk import assets (JSON array or CSV upload)",
)
async def bulk_import_assets(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
    file: UploadFile | None = File(default=None),
    body: list[AssetIn] | None = None,
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    assets_in: list[AssetIn] = []
    parse_errors: list[str] = []

    if file is not None:
        content = (await file.read()).decode("utf-8")
        if file.content_type in ("text/csv", "application/csv") or file.filename.endswith(".csv"):
            assets_in, parse_errors = parse_csv_assets(content)
        else:
            try:
                raw = json.loads(content)
                assets_in = [AssetIn(**r) for r in raw]
            except Exception as exc:
                raise HTTPException(status_code=400, detail=f"Cannot parse file: {exc}")
    elif body:
        assets_in = body
    else:
        raise HTTPException(status_code=400, detail="Provide either a file upload or JSON body")

    created = 0
    for asset_in in assets_in:
        try:
            asset = Asset(engagement_id=engagement_id, **asset_in.model_dump())
            db.add(asset)
            created += 1
        except Exception as exc:
            parse_errors.append(str(exc))

    await db.flush()
    if created:
        await _refresh_overview_cache(db, current_user.tenant_id)  # asset_count changed
    logger.info("assets.bulk_import", engagement=str(engagement_id), created=created, failed=len(parse_errors))
    return BulkAssetImportResult(created=created, failed=len(parse_errors), errors=parse_errors)


# ── GET /{engagement_id}/jobs — list scan jobs + results ──────────────────────

@router.get("/{engagement_id}/jobs", summary="List scan jobs (and results) for an engagement")
async def list_engagement_jobs(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    rows = (await db.execute(
        select(ScanJob).where(ScanJob.engagement_id == engagement_id)
        .order_by(ScanJob.created_at.desc())
    )).scalars().all()
    return [
        {
            "id": str(j.id),
            "job_type": j.job_type.value if hasattr(j.job_type, "value") else str(j.job_type),
            "status": j.status.value if hasattr(j.status, "value") else str(j.status),
            "agent_id": j.agent_id,
            "result": j.result,
            "created_at": j.created_at.isoformat() if j.created_at else None,
            "started_at": j.started_at.isoformat() if j.started_at else None,
            "completed_at": j.completed_at.isoformat() if j.completed_at else None,
        }
        for j in rows
    ]


# ── GET /{engagement_id}/assets — attack surface (hosts + services) ───────────

@router.get("/{engagement_id}/assets", summary="List assets (hosts) and their services")
async def list_engagement_assets(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    assets = (await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id).order_by(Asset.ip_address)
    )).scalars().all()
    asset_ids = [a.id for a in assets]

    svc_by_asset: dict = {}
    if asset_ids:
        services = (await db.execute(
            select(Service).where(Service.asset_id.in_(asset_ids))
        )).scalars().all()
        for s in services:
            svc_by_asset.setdefault(s.asset_id, []).append({
                "port": s.port, "protocol": s.protocol, "service": s.service_name,
                "product": s.product, "version": s.version,
            })

    return [
        {
            "id": str(a.id),
            "ip_address": a.ip_address,
            "hostname": a.hostname,
            "os": a.os,
            "asset_type": a.asset_type.value if hasattr(a.asset_type, "value") else str(a.asset_type),
            "criticality": a.criticality.value if hasattr(a.criticality, "value") else str(a.criticality),
            "services": sorted(svc_by_asset.get(a.id, []), key=lambda x: x["port"] or 0),
        }
        for a in assets
    ]


@router.get("/{engagement_id}/scope", summary="Return the engagement's authoritative scope (for probe re-validation)")
async def get_engagement_scope(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    """Probe-facing: the probe calls this independently before scanning a job to
    re-validate that job targets fall within the engagement's signed scope. This
    is the 'defense in depth' layer from the architecture — even if a manager
    job payload were tampered with, the probe enforces the engagement boundary."""
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    return {
        "engagement_id": str(engagement_id),
        "scope_cidrs": eng.scope_cidrs or [],
        "excluded_cidrs": eng.excluded_cidrs or [],
    }


# ── helpers ───────────────────────────────────────────────────────────────────
# `get_or_404` lives in app/utils/db.py — imported at top of file.
# Keeping this section as a placeholder for engagement-specific helpers.
