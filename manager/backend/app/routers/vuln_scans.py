"""
Vuln scan API — Nessus + Nuclei launch, status polling, and enrichment.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import FindingStatus, ScanJobStatus, ScanJobType
from app.models.finding import Finding
from app.models.scan_job import ScanJob
from app.utils.db import get_or_404
from app.vuln.enrichment import VulnEnrichmentService
from app.vuln.nessus import NessusScanner
from app.vuln.nuclei import NucleiRunReport, NucleiScanError, NucleiScanner
from app.vuln.tasks import run_post_scan_enrichment

router = APIRouter(prefix="/engagements/{engagement_id}/scans", tags=["vuln-scans"])
logger = structlog.get_logger()


# ── Schemas ───────────────────────────────────────────────────────────────────

class NessusScanRequest(BaseModel):
    nessus_url: str = Field(..., description="https://nessus-host:8834")
    access_key: str
    secret_key: str
    policy_id: int = 1
    credentials: dict | None = None


class NucleiScanRequest(BaseModel):
    rate_limit: int = Field(default=150, ge=1, le=500)
    templates: list[str] = Field(default_factory=list)
    timeout_sec: int = Field(default=300, ge=30, le=3600)


class FindingImport(BaseModel):
    title: str
    severity: str
    description: str | None = None
    cve_ids: list[str] = []
    cvss_score: float | None = None
    evidence: dict | None = None
    asset_id: str | None = None


# ── POST /nessus — create + launch Nessus scan ────────────────────────────────

@router.post(
    "/nessus",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Launch a Nessus scan against all assets in this engagement",
)
async def launch_nessus_scan(
    engagement_id: uuid.UUID,
    body: NessusScanRequest,
    db: DB,
    background_tasks: BackgroundTasks,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    # Collect target IPs from assets
    assets_result = await db.execute(
        select(Asset.ip_address).where(
            Asset.engagement_id == engagement_id,
            Asset.ip_address.is_not(None),
        )
    )
    target_ips = [row[0] for row in assets_result.all()]
    if not target_ips:
        # Fall back to scope CIDRs
        target_ips = eng.scope_cidrs or []
    if not target_ips:
        raise HTTPException(400, "No targets found — import assets or set scope_cidrs first")

    scanner = NessusScanner()
    await scanner.authenticate(body.nessus_url, body.access_key, body.secret_key)
    scan_id = await scanner.create_scan(
        str(engagement_id), target_ips, body.policy_id, body.credentials
    )
    await scanner.launch_scan(scan_id)
    await scanner.close()

    # Create a ScanJob record
    job = ScanJob(
        engagement_id=engagement_id,
        job_type=ScanJobType.vuln_scan,
        status=ScanJobStatus.running,
        result={"nessus_scan_id": scan_id, "target_count": len(target_ips)},
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)

    logger.info("nessus.scan.launched_via_api", scan_id=scan_id, job_id=str(job.id))
    return {"job_id": str(job.id), "nessus_scan_id": scan_id, "targets": len(target_ips)}


# ── POST /nuclei — run Nuclei scan ────────────────────────────────────────────

@router.post(
    "/nuclei",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Launch a Nuclei template scan against engagement assets",
)
async def launch_nuclei_scan(
    engagement_id: uuid.UUID,
    body: NucleiScanRequest,
    db: DB,
    background_tasks: BackgroundTasks,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    # Collect targets with services for smart template selection
    assets_result = await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id)
    )
    assets = list(assets_result.scalars().all())
    targets = [a.ip_address for a in assets if a.ip_address]
    if not targets:
        raise HTTPException(
            400,
            "No concrete asset targets found - import or discover assets before running Nuclei",
        )

    # Auto-select templates if none provided
    templates = body.templates or ["cves", "misconfigs"]

    # Create scan job and run in background
    job = ScanJob(
        engagement_id=engagement_id,
        job_type=ScanJobType.vuln_scan,
        status=ScanJobStatus.pending,
        result={"scanner": "nuclei", "templates": templates, "targets": len(targets)},
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)

    background_tasks.add_task(
        _run_nuclei_and_save,
        str(engagement_id), str(job.id), targets, templates, body.rate_limit, body.timeout_sec,
    )

    return {"job_id": str(job.id), "targets": len(targets), "templates": templates}


# ── GET /{job_id}/status ──────────────────────────────────────────────────────

@router.get("/{job_id}/status", summary="Poll scan job status")
async def scan_status(
    engagement_id: uuid.UUID,
    job_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
):
    result = await db.execute(
        select(ScanJob).where(
            ScanJob.id == job_id,
            ScanJob.engagement_id == engagement_id,
        )
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(404, "Job not found")

    return {
        "job_id": str(job.id),
        "status": job.status.value,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "result": job.result,
    }


# ── POST /{job_id}/enrich — manual enrichment trigger ────────────────────────

@router.post("/{job_id}/enrich", status_code=status.HTTP_202_ACCEPTED,
             summary="Trigger post-scan CVE enrichment")
async def trigger_enrichment(
    engagement_id: uuid.UUID,
    job_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "analyst"])],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    background_tasks.add_task(
        run_post_scan_enrichment, str(engagement_id), str(job_id)
    )
    return {"queued": True, "job_id": str(job_id)}


# ── POST /import — bulk import findings from external scanner ─────────────────

@router.post(
    "/import",
    status_code=status.HTTP_201_CREATED,
    summary="Bulk import raw findings from any scanner",
)
async def import_findings(
    engagement_id: uuid.UUID,
    body: list[FindingImport],
    db: DB,
    background_tasks: BackgroundTasks,
    current_user: Annotated[AuthUser, require_role(["admin", "manager", "tester"])],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    from app.models.enums import FindingSeverity
    from decimal import Decimal

    created = 0
    for item in body:
        try:
            sev = FindingSeverity(item.severity.lower())
        except ValueError:
            sev = FindingSeverity.info

        finding = Finding(
            engagement_id=engagement_id,
            asset_id=uuid.UUID(item.asset_id) if item.asset_id else None,
            title=item.title,
            description=item.description,
            severity=sev,
            status=FindingStatus.open,
            cve_ids=item.cve_ids or None,
            cvss_score=Decimal(str(item.cvss_score)) if item.cvss_score else None,
            evidence=item.evidence,
        )
        db.add(finding)
        created += 1

    await db.flush()

    # Auto-trigger enrichment
    job = ScanJob(
        engagement_id=engagement_id,
        job_type=ScanJobType.vuln_scan,
        status=ScanJobStatus.completed,
        result={"scanner": "import", "count": created},
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)

    background_tasks.add_task(
        run_post_scan_enrichment, str(engagement_id), str(job.id)
    )

    return {"created": created, "enrichment_job_id": str(job.id)}


# ── helpers ───────────────────────────────────────────────────────────────────

async def _run_nuclei_and_save(
    engagement_id: str,
    job_id: str,
    targets: list[str],
    templates: list[str],
    rate_limit: int,
    timeout_sec: int,
) -> None:
    """Run Nuclei and always leave its job in a truthful terminal state."""
    from app.database import AsyncSessionLocal

    engagement_uuid = uuid.UUID(engagement_id)
    job_uuid = uuid.UUID(job_id)
    logger.info("nuclei.background.start", engagement=engagement_id, targets=len(targets))

    try:
        async with AsyncSessionLocal() as db:
            if not await _set_nuclei_job_state(db, job_uuid, ScanJobStatus.running):
                logger.warning("nuclei.background.job_missing", job_id=job_id)
                return
            await db.commit()
    except Exception as exc:
        logger.error(
            "nuclei.background.start_failed",
            job_id=job_id,
            error=str(exc),
            exc_info=exc,
        )
        return

    scanner = NucleiScanner()
    scan_error: NucleiScanError | None = None
    try:
        raw_findings = await scanner.run_scan(
            targets,
            templates,
            rate_limit,
            timeout_sec,
        )
    except asyncio.CancelledError:
        await _finish_cancelled_nuclei_job(AsyncSessionLocal, job_uuid)
        raise
    except NucleiScanError as exc:
        scan_error = exc
        raw_findings = exc.partial_findings
    except Exception as exc:
        logger.error(
            "nuclei.background.unexpected_scanner_failure",
            job_id=job_id,
            error=str(exc),
            exc_info=exc,
        )
        scan_error = NucleiScanError("scanner_exception", str(exc))
        raw_findings = []

    created = 0
    rejected = 0
    report = scanner.last_run_report
    try:
        async with AsyncSessionLocal() as db:
            for item in raw_findings:
                try:
                    async with db.begin_nested():
                        db.add(_nuclei_finding(engagement_uuid, item))
                        await db.flush()
                    created += 1
                except Exception as exc:
                    rejected += 1
                    logger.warning(
                        "nuclei.finding.save_failed",
                        job_id=job_id,
                        error=str(exc),
                    )

            status_value, result_patch = _nuclei_terminal_result(
                report=report,
                scan_error=scan_error,
                received=len(raw_findings),
                created=created,
                rejected=rejected,
            )
            if not await _set_nuclei_job_state(
                db,
                job_uuid,
                status_value,
                result_patch=result_patch,
            ):
                logger.warning("nuclei.background.job_missing", job_id=job_id)
                await db.rollback()
                return
            await db.commit()
    except Exception as exc:
        logger.error(
            "nuclei.background.persist_failed",
            job_id=job_id,
            error=str(exc),
            exc_info=exc,
        )
        await _finish_failed_nuclei_job(
            AsyncSessionLocal,
            job_uuid,
            code="persistence_failed",
            message="Nuclei finished, but its results could not be persisted",
        )
        return

    logger.info(
        "nuclei.background.done",
        job_id=job_id,
        outcome=result_patch["outcome"],
        created=created,
        rejected=rejected,
    )
    if created:
        try:
            await run_post_scan_enrichment(engagement_id, job_id)
        except Exception as exc:
            logger.warning(
                "nuclei.background.enrichment_failed",
                job_id=job_id,
                error=str(exc),
            )


_NUCLEI_REMEDIATION = {
    "not_installed": "Install Nuclei on the manager and ensure the binary is on PATH.",
    "spawn_failed": "Verify the Nuclei binary is executable by the manager service account.",
    "timeout": "Reduce the target set or rate, or increase the scan wall-clock timeout.",
    "nonzero_exit": "Review the Nuclei stderr tail and validate templates and CLI compatibility.",
    "templates_missing": "Install or update nuclei-templates and verify the configured template tags.",
    "parse_error": "Upgrade Nuclei and verify that JSONL output is not being mixed with other output.",
    "scanner_exception": "Review manager logs and retry after correcting the scanner runtime error.",
    "persistence_failed": "Check database health and constraints before retrying the scan.",
    "cancelled": "The manager stopped the background task; retry after the service is stable.",
}


def _nuclei_finding(engagement_id: uuid.UUID, item: dict) -> Finding:
    from app.models.enums import FindingSeverity

    severity_value = item.get("severity") or FindingSeverity.info
    severity = (
        severity_value
        if isinstance(severity_value, FindingSeverity)
        else FindingSeverity(str(severity_value).lower())
    )
    return Finding(
        engagement_id=engagement_id,
        severity=severity,
        status=FindingStatus.open,
        title=item.get("title", "Unknown"),
        description=item.get("description"),
        cve_ids=item.get("cve_ids") or None,
        cvss_score=item.get("cvss_score"),
        mitre_techniques=item.get("mitre_techniques"),
        exploitable=item.get("exploitable", False),
        evidence=item.get("evidence"),
    )


def _nuclei_terminal_result(
    *,
    report: NucleiRunReport | None,
    scan_error: NucleiScanError | None,
    received: int,
    created: int,
    rejected: int,
) -> tuple[ScanJobStatus, dict]:
    error_code = scan_error.reason if scan_error else (report.reason if report else None)
    persistence_failure = received > 0 and created == 0 and rejected > 0
    fatal = (
        (scan_error is not None and received == 0)
        or (report is not None and report.status == "failed" and received == 0)
        or persistence_failure
    )
    degraded = (
        not fatal
        and (
            rejected > 0
            or (report is not None and report.status == "partial")
            or (scan_error is not None and received > 0)
        )
    )
    outcome = "failed" if fatal else ("partial" if degraded else "success")
    status_value = ScanJobStatus.failed if fatal else ScanJobStatus.completed

    if persistence_failure:
        error_code = "persistence_failed"
    if error_code is None and fatal:
        error_code = "scanner_exception"

    scanner_run = {
        "component": "nuclei",
        "status": "failed" if fatal else ("degraded" if degraded else "completed"),
        "finding_count": received,
        "error_code": error_code,
        "returncode": report.returncode if report else getattr(scan_error, "returncode", None),
        "malformed_lines": report.malformed_lines if report else 0,
    }
    result: dict = {
        "outcome": outcome,
        "degraded": degraded,
        "findings_received": received,
        "findings_created": created,
        "findings_rejected": rejected,
        "scanner_run": scanner_run,
    }
    if error_code:
        detail = str(scan_error) if scan_error else (report.stderr if report else "")
        result["issues"] = [
            {
                "component": "nuclei",
                "code": error_code,
                "message": detail[:1000] or f"Nuclei reported {error_code}",
                "remediation": _NUCLEI_REMEDIATION.get(
                    error_code,
                    "Review the manager scanner logs before retrying.",
                ),
            }
        ]
    return status_value, result


async def _set_nuclei_job_state(
    db: AsyncSession,
    job_id: uuid.UUID,
    status_value: ScanJobStatus,
    *,
    result_patch: dict | None = None,
) -> bool:
    job = (
        await db.execute(select(ScanJob).where(ScanJob.id == job_id))
    ).scalar_one_or_none()
    if job is None:
        return False
    job.status = status_value
    now = datetime.now(timezone.utc)
    if status_value == ScanJobStatus.running and job.started_at is None:
        job.started_at = now
    if status_value in (ScanJobStatus.completed, ScanJobStatus.failed):
        job.completed_at = now
    if result_patch:
        job.result = {**(job.result or {}), **result_patch}
    return True


async def _finish_cancelled_nuclei_job(session_factory, job_id: uuid.UUID) -> None:
    await _finish_failed_nuclei_job(
        session_factory,
        job_id,
        code="cancelled",
        message="Nuclei background task was cancelled",
    )


async def _finish_failed_nuclei_job(
    session_factory,
    job_id: uuid.UUID,
    *,
    code: str,
    message: str,
) -> None:
    try:
        async with session_factory() as db:
            await _set_nuclei_job_state(
                db,
                job_id,
                ScanJobStatus.failed,
                result_patch={
                    "outcome": "failed",
                    "degraded": False,
                    "issues": [
                        {
                            "component": "nuclei",
                            "code": code,
                            "message": message,
                            "remediation": _NUCLEI_REMEDIATION.get(
                                code,
                                "Review the manager scanner logs before retrying.",
                            ),
                        }
                    ],
                },
            )
            await db.commit()
    except Exception as exc:
        logger.error(
            "nuclei.background.terminal_update_failed",
            job_id=str(job_id),
            error=str(exc),
        )
