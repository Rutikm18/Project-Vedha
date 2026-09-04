import json
import os
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field, field_validator, model_validator
from sqlalchemy import func, select

from app.auth.rbac import require_role
from app.dependencies import DB, ReadDB, AuthUser
from app.models.agent import Agent
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import AssetType, EngagementStatus, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.models.detection_run import DetectionRun, RUN_COMPLETED, RUN_FAILED, RUN_RUNNING
from app.models.outbox import (
    OutboxEvent, OUTBOX_PENDING, OUTBOX_PROCESSING, OUTBOX_FAILED, TOPIC_FACTS_READY,
)
from app.models.scan_job import ScanJob
from app.models.scan_result import ScanResult
from app.models.worker_heartbeat import WorkerHeartbeat

# A queued facts_ready event whose available_at is older than this, still undrained,
# means the detection queue is not moving — the worker is down or wedged. Surfaced as
# the `stalled` phase so a dead worker announces itself instead of a permanent spinner.
_QUEUE_STALL_SEC = 120
# A worker heartbeat older than this = the detection worker is down (it beats ~30s).
_WORKER_STALE_SEC = 90
# When to call a still-RUNNING DetectionRun wedged rather than busy. A bare
# duration cannot decide this: a legitimate run over a large scope can take a long
# time, and calling that "stalled" cries wolf on exactly the customers with the
# most to scan. So the call is CORROBORATED, the same discipline the liveness and
# confidence models use — duration is only half the evidence, worker liveness is
# the other half:
#   * worker heartbeat demonstrably STALE  → the thing that would finish this run
#     is not running; a short floor is enough to be sure it is not a blip.
#   * worker liveness UNKNOWN (no heartbeat table / not yet migrated) → fall back
#     to duration alone, but a patient threshold.
#   * worker heartbeat FRESH → never called stalled on duration alone. It is
#     working; a big scope is not a defect.
_RUN_STALL_DEAD_WORKER_SEC = 120
_RUN_STALL_UNKNOWN_WORKER_SEC = 1800
from app.models.service import Service
from app.schemas.common import PaginatedResponse, paginate
from app.schemas.asset import AssetIn, BulkAssetImportResult
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

    # Batch-resolve probe names so restored jobs render with their probe label
    # (one query for the whole set — no N+1 per job). Tolerate a non-UUID/legacy
    # agent_id: skip it for name resolution rather than 500-ing the whole listing.
    def _as_uuid(value) -> uuid.UUID | None:
        try:
            return uuid.UUID(str(value))
        except (ValueError, TypeError, AttributeError):
            return None

    agent_ids = {u for j in rows if j.agent_id for u in (_as_uuid(j.agent_id),) if u}
    names: dict[str, str] = {}
    if agent_ids:
        agents = (await db.execute(
            select(Agent).where(Agent.id.in_(agent_ids))
        )).scalars().all()
        names = {str(a.id): a.name for a in agents}

    # Never leak the raw facts blob or credential params to the client — mirror
    # the redaction the single-job status endpoint applies.
    _REDACT = {"facts", "ssh_creds", "win_creds"}
    return [
        {
            "id": str(j.id),
        # The label a customer quotes; the UUID stays for machines. getattr keeps
        # this readable for a row loaded before migration 0036 stamped one (and
        # matches how the rest of this handler reads optional fields).
        "reference": getattr(j, "reference", None),
            "job_type": j.job_type.value if hasattr(j.job_type, "value") else str(j.job_type),
            "status": j.status.value if hasattr(j.status, "value") else str(j.status),
            "agent_id": str(j.agent_id) if j.agent_id else None,
            "agent_name": names.get(str(j.agent_id)) if j.agent_id else None,
            "use_case_id": (j.result or {}).get("use_case_id"),
            "result": {k: v for k, v in j.result.items() if k not in _REDACT} if j.result else None,
            "created_at": j.created_at.isoformat() if j.created_at else None,
            "started_at": j.started_at.isoformat() if j.started_at else None,
            "completed_at": j.completed_at.isoformat() if j.completed_at else None,
        }
        for j in rows
    ]


# ── GET /{engagement_id}/campaign-progress — the VA Campaigns live view ───────
_OPEN_FINDING_STATES = (FindingStatus.open, FindingStatus.confirmed)


def _job_phase(status: str) -> str:
    """Map a ScanJob status to the operator-facing scan phase shown on the card."""
    return {
        "pending": "queued", "queued": "queued", "dispatched": "dispatched",
        "assigned": "dispatched", "running": "scanning", "in_progress": "scanning",
        "completed": "complete", "succeeded": "complete",
        "failed": "failed", "error": "failed", "cancelled": "cancelled",
    }.get(status, status)


def _reconcile_status(*, jobs_exist: bool, any_running: bool, scanning_done: bool,
                      run_exists: bool, latest_failed: bool, detection_done: bool,
                      evidence_covered: bool, has_gaps: bool,
                      queue_pending: bool, queue_overdue: bool,
                      queue_dead: bool,
                      worker_alive: bool | None = None,
                      any_complete: bool = True,
                      all_cancelled: bool = False) -> tuple[str, bool]:
    """Derive ONE authoritative campaign phase from reconciled evidence, not from a
    single nullable run row. Precedence is load-bearing (it is what makes multi-agent
    campaigns correct and a dead worker visible):

      pending → scanning → error(dead-letter) → stalled(queue not draining) →
      aggregating(queued/no-run-yet) → error(run failed) → detecting →
      complete_with_gaps / complete

    `evidence_covered` (every scan submission consumed by a COMPLETED run) is what
    stops a campaign showing 'complete' the moment its LAST job's run finishes while
    an earlier agent's submission still has no run (F11/F12). Returns
    (overall_status, is_complete)."""
    if not jobs_exist:
        return "pending", False
    if any_running:
        return "scanning", False
    if queue_dead:                                  # a facts_ready event dead-lettered
        return "error", False
    # Queue not draining: either an event went overdue, OR the worker's heartbeat is
    # stale (worker_alive is False) — the latter catches a dead worker BEFORE events
    # age out. worker_alive None (heartbeat unknown/unavailable) → fall back to overdue.
    if queue_pending and (queue_overdue or worker_alive is False):
        return "stalled", False
    if queue_pending:                               # queued, a worker is draining it
        return "aggregating", False
    # NOTHING was ever submitted. "aggregating" infers "facts are in, the run is
    # coming", which is only true when some job actually completed. If every job
    # was cancelled or failed there is no submission, hence no facts.ready event
    # and no DetectionRun — ever. Without this branch the campaign waits on
    # `run_exists` forever: a bar frozen at 1-of-6 phases (~17%), a spinner that
    # never stops, and a frontend polling every 4s for a state that cannot change.
    # A cancel is a legitimate operator action, so this is now reachable on purpose.
    if not any_complete:
        return ("cancelled" if all_cancelled else "error"), True
    if not run_exists:                              # facts done, run not created yet
        return "aggregating", False
    if latest_failed:
        return "error", False
    if not (detection_done and evidence_covered):   # a submission still uncovered
        return "detecting", False
    if has_gaps:
        return "complete_with_gaps", True
    return "complete", True


def _result_summary(result: dict | None) -> dict:
    """A SAFE, bounded view of a job's raw result — the counts an operator needs to
    see 'what the probe found' WITHOUT leaking the full facts blob or credentials."""
    if not result:
        return {}
    runs = result.get("scanner_runs") or result.get("run_stats") or []
    scanners = sorted({(r.get("id") or r.get("scanner")) for r in runs
                       if isinstance(r, dict) and (r.get("id") or r.get("scanner"))}) \
        if isinstance(runs, list) else []
    return {
        "scanners": scanners,
        "scanner_count": len(scanners),
        "fact_count": result.get("facts_count")
        or (len(result["facts"]) if isinstance(result.get("facts"), list) else None),
        "open_ports": result.get("open_tcp") or result.get("open_ports"),
        "profile": result.get("profile"),
        "ok": result.get("ok"),
    }


@router.get("/{engagement_id}/campaign-progress",
            summary="VA campaign live view: per-probe jobs + detection pipeline + findings")
async def campaign_progress(engagement_id: uuid.UUID, db: DB, current_user: AuthUser):
    """One call powers the VA Campaigns page: every probe's job (status + a safe raw
    result summary), the full pipeline progress (Scanning → Aggregating → Detection
    → Correlation → Prioritization → Remediation), and the findings with remediation
    guidance. Read-only aggregation over jobs + the latest detection run + findings."""
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    # ── jobs (per probe) ──────────────────────────────────────────────────────
    job_rows = (await db.execute(
        select(ScanJob).where(ScanJob.engagement_id == engagement_id)
        .order_by(ScanJob.created_at.desc())
    )).scalars().all()
    agent_ids = {j.agent_id for j in job_rows if j.agent_id}
    names: dict = {}
    if agent_ids:
        agents = (await db.execute(select(Agent).where(Agent.id.in_(agent_ids)))).scalars().all()
        names = {str(a.id): a.name for a in agents}

    def _val(x):
        return x.value if hasattr(x, "value") else str(x)

    jobs = [{
        "id": str(j.id),
        # The label a customer quotes; the UUID stays for machines. getattr keeps
        # this readable for a row loaded before migration 0036 stamped one (and
        # matches how the rest of this handler reads optional fields).
        "reference": getattr(j, "reference", None),
        "use_case_id": (j.result or {}).get("use_case_id"),
        "job_type": _val(j.job_type),
        "status": _val(j.status),
        "phase": _job_phase(_val(j.status)),
        "agent_id": str(j.agent_id) if j.agent_id else None,
        "agent_name": names.get(str(j.agent_id)) if j.agent_id else None,
        "result_summary": _result_summary(j.result),
        "created_at": j.created_at.isoformat() if j.created_at else None,
        "started_at": j.started_at.isoformat() if j.started_at else None,
        "completed_at": j.completed_at.isoformat() if j.completed_at else None,
    } for j in job_rows]

    any_running = any(x["phase"] in ("scanning", "dispatched", "queued") for x in jobs)
    any_complete = any(x["phase"] == "complete" for x in jobs)
    # Every job stopped, and an operator stopped them: report that plainly rather
    # than as an error, so housekeeping never looks like a system fault.
    all_cancelled = bool(jobs) and all(x["phase"] == "cancelled" for x in jobs)

    # ── detection runs (ALL of them — completion is proven by coverage) ─────────
    # A multi-agent campaign has one run per fact submission. Reading only the latest
    # run makes the campaign look 'complete' the moment the LAST job's run finishes,
    # even if an EARLIER agent's submission was never detected. So fetch every run and
    # prove coverage against the scan submissions.
    runs = (await db.execute(
        select(DetectionRun).where(DetectionRun.engagement_id == engagement_id)
        .order_by(DetectionRun.started_at.desc())
    )).scalars().all()
    run = runs[0] if runs else None          # latest, for the stats/display below
    # The DetectionRun completes as RUN_COMPLETED ("completed") — NOT "done".
    detection_done = bool(run and run.status == RUN_COMPLETED)
    detection_failed = bool(run and run.status == RUN_FAILED)

    # Coverage: every scan submission (scan_results row) must have a COMPLETED run.
    sr_ids = set((await db.execute(
        select(ScanResult.id).where(ScanResult.engagement_id == engagement_id)
    )).scalars().all())
    covered = {r.scan_result_id for r in runs
               if r.status == RUN_COMPLETED and r.scan_result_id is not None}
    # If submissions aren't linkable to runs (older data / no scan_result_id), fall
    # back to the single-run signal so behaviour is unchanged for that case.
    evidence_covered = (sr_ids <= covered) if (sr_ids and covered) else detection_done

    # Queue state: undrained facts_ready events are the 'is the worker even alive?'
    # signal. An overdue pending event means the queue is not draining → stalled.
    now = datetime.now(timezone.utc)
    q_rows = (await db.execute(
        select(OutboxEvent.status, OutboxEvent.available_at).where(
            OutboxEvent.engagement_id == engagement_id,
            OutboxEvent.topic == TOPIC_FACTS_READY,
        )
    )).all()
    queue_pending = any(s in (OUTBOX_PENDING, OUTBOX_PROCESSING) for s, _ in q_rows)
    queue_dead = any(s == OUTBOX_FAILED for s, _ in q_rows)
    queue_overdue = any(
        s in (OUTBOX_PENDING, OUTBOX_PROCESSING) and av is not None
        and (now - av).total_seconds() > _QUEUE_STALL_SEC
        for s, av in q_rows)

    # ── detection-trace coverage: which RULES were assessed vs BLIND ────────────
    # From run.stats["posture_coverage"] (written by engine_bridge). rules_blind > 0
    # means the scanner submitted facts but some rules could NOT be assessed (agent
    # drift / unparseable / error) — a completed run that is NOT the same as clean.
    # This is the number that lets "no findings" stop masquerading as "checked".
    _stats = (getattr(run, "stats", None) if run else None) or {}
    _stats = _stats if isinstance(_stats, dict) else {}
    _pcov = _stats.get("posture_coverage") or {}
    _pverdicts = _stats.get("posture_verdicts") or {}
    rules_blind = int(_pcov.get("rules_blind") or 0)
    rules_total = int(_pcov.get("rules_total") or 0)
    rules_assessed = int(_pcov.get("rules_assessed") or 0)
    rules_unassessed = int(_pcov.get("rules_unassessed") or 0)
    blind_rule_ids = _pcov.get("blind_rule_ids") or []
    has_gaps = detection_done and rules_blind > 0

    # ── findings (open set), with the counts each pipeline phase reports ──────
    findings = (await db.execute(
        select(Finding).where(
            Finding.engagement_id == engagement_id,
            Finding.status.in_(_OPEN_FINDING_STATES),
        ).order_by(Finding.risk_score.desc().nullslast())
    )).scalars().all()

    def _sev(f):
        return f.severity.value if hasattr(f.severity, "value") else str(f.severity)

    by_severity: dict = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        by_severity[_sev(f)] = by_severity.get(_sev(f), 0) + 1
    correlated = sum(1 for f in findings
                     if isinstance(f.evidence, dict)
                     and ("correlated_findings" in f.evidence or f.evidence.get("correlation")))
    prioritized = sum(1 for f in findings if f.risk_score is not None)
    remediable = sum(1 for f in findings if f.remediation)

    def _phase(name, done, active, count=None):
        return {"name": name, "status": ("done" if done else "active" if active else "pending"),
                "count": count}

    scanning_done = bool(jobs) and not any_running

    # The detection-dependent phases key off the SAME reconciled evidence that
    # decides is_complete — `detection_done AND evidence_covered` — not off the
    # latest run alone.
    #
    # THE BUG THIS FIXES: `percent` counted phases using detection_done (the LATEST
    # run completed) while is_complete additionally required evidence_covered
    # (every scan submission consumed by a completed run). In a multi-agent
    # campaign where the newest submission was detected but an earlier one was not,
    # the two disagreed: the bar read 100% while the campaign stayed "detecting"
    # and never announced completion. Reproduced directly against this handler.
    pipeline_done = detection_done and evidence_covered
    detecting_now = run is not None and not pipeline_done
    phases = [
        _phase("scanning", scanning_done, any_running),
        _phase("aggregating", run is not None, scanning_done and run is None),
        _phase("detection", pipeline_done, detecting_now, len(findings)),
        # correlation/prioritization/remediation run synchronously inside the same
        # detection pass, so they complete together — but each keeps its own count.
        _phase("correlation", pipeline_done, detecting_now, correlated),
        _phase("prioritization", pipeline_done, detecting_now, prioritized),
        _phase("remediation", pipeline_done, detecting_now, remediable),
    ]
    percent = round(100 * sum(1 for p in phases if p["status"] == "done") / len(phases))

    # ── ONE authoritative pipeline status ─────────────────────────────────────
    # The scan job going "complete" is NOT the campaign being complete — detection,
    # correlation, prioritization and remediation-mapping all follow. is_complete is
    # true ONLY when the whole pipeline has finished, so the UI never shows a green
    # "completed" while the manager is still analysing.
    # Worker liveness (best-effort, LAST query): a stale/absent heartbeat means the
    # detection worker is down. Wrapped so a missing worker_heartbeats table (migration
    # not yet run) degrades to the queue-lag signal instead of erroring the whole page.
    # How long has the latest run been RUNNING? A run that never finishes is the
    # other way a campaign never reaches 100%, and it is invisible in the queue
    # signals because the outbox event was already consumed. Duration alone is NOT
    # the verdict — see the thresholds above; it is corroborated below.
    run_running_for: float | None = None
    if run is not None and run.status == RUN_RUNNING and run.started_at is not None:
        started = run.started_at
        if started.tzinfo is None:
            started = started.replace(tzinfo=timezone.utc)
        run_running_for = (now - started).total_seconds()

    worker_alive: bool | None = None
    try:
        last_beat = (await db.execute(
            select(func.max(WorkerHeartbeat.last_beat_at))
        )).scalar_one_or_none()
        if last_beat is not None:
            worker_alive = (now - last_beat).total_seconds() <= _WORKER_STALE_SEC
    except Exception:  # noqa: BLE001 — liveness is a nice-to-have, never fail the page
        worker_alive = None

    # Corroborated stall verdict: duration + worker liveness together.
    if run_running_for is None or worker_alive is True:
        run_stalled = False                       # not running, or demonstrably working
    elif worker_alive is False:
        run_stalled = run_running_for > _RUN_STALL_DEAD_WORKER_SEC
    else:                                          # liveness unknown — be patient
        run_stalled = run_running_for > _RUN_STALL_UNKNOWN_WORKER_SEC

    overall_status, is_complete = _reconcile_status(
        jobs_exist=bool(jobs), any_running=any_running, scanning_done=scanning_done,
        any_complete=any_complete, all_cancelled=all_cancelled,
        run_exists=run is not None, latest_failed=detection_failed,
        detection_done=detection_done, evidence_covered=evidence_covered,
        has_gaps=has_gaps, queue_pending=queue_pending, queue_overdue=queue_overdue,
        queue_dead=queue_dead, worker_alive=worker_alive)

    # A human-readable reason for any non-clean terminal/blocked state — so the UI
    # states what happened instead of showing a spinner or a misleading "clean".
    reasons: list[str] = []
    if overall_status == "error" and queue_dead:
        reasons.append("a facts_ready event was dead-lettered after exhausting retries "
                       "— detection could not run on that submission.")
    elif overall_status == "error":
        reasons.append(getattr(run, "error", None) or "detection failed")
    elif overall_status == "stalled":
        reasons.append("detection queue is not draining — the outbox worker "
                       "(python -m app.workers.outbox) appears to be down or wedged.")
    elif overall_status == "aggregating":
        reasons.append("facts submitted; detection is queued — the outbox worker "
                       "(python -m app.workers.outbox) should pick it up shortly.")
    elif overall_status == "detecting" and detection_done and not evidence_covered:
        pend = len(sr_ids - covered)
        reasons.append(f"{pend} scan submission(s) still awaiting detection — the "
                       f"campaign is not complete until every submission is covered.")
    elif overall_status == "detecting" and run_stalled:
        # A run that started and never finished leaves the campaign stuck on
        # "detecting" with nothing to look at. Name it.
        mins = int(run_running_for // 60) if run_running_for else 0
        if worker_alive is False:
            reasons.append(
                f"the detection run has been in progress for {mins} minute(s) and the "
                f"detection worker has stopped heartbeating — it appears to have died "
                f"mid-run. Restart `python -m app.workers.outbox` and check the run's "
                f"error field.")
        else:
            reasons.append(
                f"the detection run has been in progress for {mins} minute(s) without "
                f"finishing and worker liveness is unknown. If this scope is large the "
                f"run may still be legitimate; otherwise check "
                f"`python -m app.workers.outbox` and the run's error field.")
    elif has_gaps:
        reasons.append(
            f"{rules_blind} of {rules_total} checks could not be assessed against the "
            f"data the scanner returned — treat these as UNKNOWN, not clean.")

    # ── findings with remediation (top 100, worst first) ─────────────────────
    def _conf(f):
        """Calibrated confidence + corroboration, read from the posture finding's
        evidence (posture_confidence stamps confidence + precision_factors there).
        CVE findings won't carry these — return None/[] then."""
        ev = f.evidence if isinstance(f.evidence, dict) else {}
        pf = ev.get("precision_factors") if isinstance(ev.get("precision_factors"), dict) else {}
        chain = pf.get("chain_corroboration") if isinstance(pf.get("chain_corroboration"), dict) else None
        return ev.get("confidence"), (chain.get("chains") if chain else [])

    top = []
    for f in findings[:100]:
        conf, chains = _conf(f)
        top.append({
            "id": str(f.id),
            "title": f.title,
            "severity": _sev(f),
            "risk_score": float(f.risk_score) if f.risk_score is not None else None,
            "confidence": conf,                 # calibrated TP-likelihood (posture)
            "corroborated_by": chains,          # attack chains that raised its confidence
            "priority": f.priority if hasattr(f, "priority") else None,
            "cve_ids": f.cve_ids,
            "mitre_techniques": f.mitre_techniques,
            "state": _val(f.status),
            "remediation": f.remediation,
            "asset_id": str(f.asset_id) if f.asset_id else None,
        })

    # ── high-level summary (the exec view above the detailed/core findings) ───
    exploitable = sum(1 for f in findings if getattr(f, "exploit_validated", False))
    max_risk = max((float(f.risk_score) for f in findings if f.risk_score is not None),
                   default=0.0)
    technique_counts: dict = {}
    for f in findings:
        for t in (f.mitre_techniques or []):
            technique_counts[t] = technique_counts.get(t, 0) + 1
    top_techniques = sorted(technique_counts.items(), key=lambda kv: -kv[1])[:6]

    return {
        "engagement_id": str(engagement_id),
        "engagement": {
            "name": getattr(eng, "name", None),
            "status": _val(getattr(eng, "status", "")),
        },
        # ONE authoritative campaign status — the UI must key its "complete" badge
        # off is_complete, NEVER off a single scan job finishing.
        "overall_status": overall_status,
        "is_complete": is_complete,
        "percent": percent,
        "reasons": reasons,
        "phases": phases,
        # ── coverage: what did detection actually CHECK? (the honest-coverage view)
        "coverage": {
            "rules_total": rules_total,
            "rules_assessed": rules_assessed,
            "rules_blind": rules_blind,
            "rules_unassessed": rules_unassessed,
            "blind_rule_ids": blind_rule_ids,
            "has_gaps": has_gaps,
        },
        # ── evidence coverage: completion PROVEN by every submission being detected
        "evidence": {
            "submissions": len(sr_ids),
            "covered": len(sr_ids & covered) if sr_ids else len(covered),
            "fully_covered": evidence_covered,
        },
        # ── queue health: is the detection worker actually draining events?
        "queue": {
            "pending": queue_pending,
            "overdue": queue_overdue,
            "dead": queue_dead,
            "worker_alive": worker_alive,   # None = heartbeat unknown (pre-migration)
        },
        "jobs": jobs,
        "job_stats": {
            "total": len(jobs),
            "running": sum(1 for x in jobs if x["phase"] in ("scanning", "dispatched", "queued")),
            "complete": sum(1 for x in jobs if x["phase"] == "complete"),
            "failed": sum(1 for x in jobs if x["phase"] == "failed"),
            "probes": sorted({x["agent_name"] for x in jobs if x["agent_name"]}),
        },
        "detection": {
            "status": (run.status if run else "pending"),
            "done": detection_done,
            "failed": detection_failed,
            "facts_count": run.facts_count if run else 0,
            "findings_new": run.findings_new if run else 0,
            "findings_current": (run.findings_current if run else len(findings)),
            "started_at": run.started_at.isoformat() if run and run.started_at else None,
            "finished_at": run.finished_at.isoformat() if run and run.finished_at else None,
            "by_severity": by_severity,
        },
        # high-level rollup for the exec band
        "summary": {
            "total_findings": len(findings),
            "by_severity": by_severity,
            "max_risk_score": round(max_risk, 1),
            "exploitable": exploitable,
            "actionable": by_severity["critical"] + by_severity["high"] + by_severity["medium"],
            "top_techniques": [{"technique": t, "count": c} for t, c in top_techniques],
        },
        "findings": top,
    }


# ── GET /{engagement_id}/detection-explain — why did (or didn't) a rule fire? ──
@router.get("/{engagement_id}/detection-explain",
            summary="Per-rule detection verdicts: why a check did/didn't produce a finding")
async def detection_explain(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
    rule_id: str | None = None,
):
    """The machine-readable answer to "the scripts catch it but the manager doesn't".
    For the latest detection run, returns each posture rule's verdict:
      finding_exists | evaluated_clean | schema_drift | no_evidence_collected | rule_error
    with the reason strings. `schema_drift` means the scanner submitted facts but the
    field the rule reads was absent (agent drift) — the silent false-negative, now
    named. Operator-gated (reasons quote fact paths / errors)."""
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    run = (await db.execute(
        select(DetectionRun).where(DetectionRun.engagement_id == engagement_id)
        .order_by(DetectionRun.started_at.desc()).limit(1)
    )).scalar_one_or_none()

    stats = (getattr(run, "stats", None) if run else None) or {}
    stats = stats if isinstance(stats, dict) else {}
    verdicts = stats.get("posture_verdicts") or {}
    coverage = stats.get("posture_coverage") or {}

    if rule_id:
        v = verdicts.get(rule_id)
        return {
            "engagement_id": str(engagement_id),
            "run_id": str(run.id) if run else None,
            "run_status": run.status if run else "none",
            "rule_id": rule_id,
            "verdict": (v or {}).get("verdict", "detection_never_ran" if run is None else "no_evidence_collected"),
            "reasons": (v or {}).get("reasons", []),
        }

    return {
        "engagement_id": str(engagement_id),
        "run_id": str(run.id) if run else None,
        "run_status": run.status if run else "none",
        "coverage": coverage,
        # sorted worst-first: drift/error before clean, so gaps surface at the top
        "rules": sorted(
            [{"rule_id": rid, **v} for rid, v in verdicts.items()],
            key=lambda r: (
                {"rule_error": 0, "schema_drift": 1, "finding_exists": 2,
                 "no_evidence_collected": 3, "evaluated_clean": 4}.get(r.get("verdict"), 5),
                r["rule_id"]),
        ),
    }


# ── GET /{engagement_id}/raw-facts — inspect exactly what the scanners collected ─
@router.get("/{engagement_id}/raw-facts",
            summary="Raw scanner facts (exactly what the vedha-agent/main_scripts collected)")
async def raw_facts(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
    job_id: uuid.UUID | None = None,
    scanner: str | None = None,
    limit: int = 5,
    max_facts: int = 2000,
):
    """The raw ScanResult facts as the probe submitted them, straight from the
    append-only scan_results table — the ground truth that feeds detection. This is
    the "what did the scanner actually see" view: grouped by scanner name, filterable
    to one submission (job_id) or one scanner. Operator-gated (not exposed to clients)
    because facts can carry banners/hostnames. `limit` bounds scan submissions,
    `max_facts` bounds facts per submission so a huge scan can't blow up the payload."""
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    limit = max(1, min(int(limit), 25))
    max_facts = max(1, min(int(max_facts), 20000))

    q = select(ScanResult).where(ScanResult.engagement_id == engagement_id)
    if job_id is not None:
        q = q.where(ScanResult.job_id == job_id)
    rows = (await db.execute(
        q.order_by(ScanResult.created_at.desc()).limit(limit))).scalars().all()

    total_by_scanner: dict = {}
    results = []
    for r in rows:
        facts = r.facts if isinstance(r.facts, list) else []
        by_scanner: dict = {}
        for f in facts:
            s = (f.get("scanner") if isinstance(f, dict) else None) or "?"
            by_scanner[s] = by_scanner.get(s, 0) + 1
            total_by_scanner[s] = total_by_scanner.get(s, 0) + 1
        shown = [f for f in facts if isinstance(f, dict) and f.get("scanner") == scanner] \
            if scanner else facts
        results.append({
            "id": str(r.id),
            "job_id": str(r.job_id) if r.job_id else None,
            "agent_id": str(r.agent_id) if r.agent_id else None,
            "scan_type": r.scan_type,
            "fact_count": r.fact_count,
            "validation_state": r.validation_state,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "by_scanner": dict(sorted(by_scanner.items())),
            "facts": shown[:max_facts],           # the raw ScanResult dicts, verbatim
            "truncated": len(shown) > max_facts,
        })

    return {
        "engagement_id": str(engagement_id),
        "scanners": sorted(total_by_scanner),     # every scanner that produced facts
        "by_scanner": dict(sorted(total_by_scanner.items())),
        "scan_results": results,
    }


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
