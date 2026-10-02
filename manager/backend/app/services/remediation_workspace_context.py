"""Tenant-scoped context adapter for the deterministic remediation workspace.

The artifact compiler intentionally knows nothing about SQLAlchemy or request
authorization.  This adapter is the only place that turns persisted findings
and assets into its narrow, trusted ``FindingContext`` contract.
"""
from __future__ import annotations

import hashlib
import json
import uuid
from collections.abc import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.remediation_workspace import FindingContext, MAX_FINDINGS, OsFamily
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.services.finding_scan_provenance import SCAN_PROVENANCE_KEY


class RemediationContextNotFound(LookupError):
    """At least one requested ID is absent or outside the caller's tenant."""


class RemediationContextConflict(ValueError):
    """The authorized selection cannot form one workspace."""


def os_family(value: object) -> OsFamily:
    normalized = str(value or "").strip().lower()
    if any(marker in normalized for marker in ("windows", "win32", "win64")):
        return OsFamily.windows
    if any(marker in normalized for marker in (
        "linux", "ubuntu", "debian", "rhel", "red hat", "centos", "rocky",
        "alma", "fedora", "suse", "amazon linux",
    )):
        return OsFamily.linux
    if any(marker in normalized for marker in ("macos", "mac os", "os x", "darwin")):
        return OsFamily.macos
    return OsFamily.generic


def remediation_selector(
    evidence: object,
    family: OsFamily,
    *,
    trusted_detection: bool = False,
) -> tuple[str, dict[str, str | int | bool]]:
    """Map machine-readable evidence to an allowlisted catalog selector.

    Never infer an executable change from title/remediation prose.  The exact
    SMB rule is emitted by Manager's deterministic posture engine.  Package
    automation requires an explicit structured descriptor; arbitrary command
    strings are ignored even when present in evidence.
    """
    record = evidence if isinstance(evidence, dict) else {}
    engine_owned = trusted_detection and SCAN_PROVENANCE_KEY not in record
    if (
        engine_owned
        and family is OsFamily.windows
        and record.get("rule_id") == "POSTURE-SMB-SIGNING-OFF"
        and record.get("scanner") == "smb_scan"
        and record.get("state") == "confirmed"
    ):
        return "windows.smb_signing.require", {}

    automation = record.get("remediation_automation")
    if (
        engine_owned
        and family is OsFamily.linux
        and record.get("source_confidence") == "authoritative"
        and record.get("ai_assisted") is False
        and isinstance(automation, dict)
        and automation.get("template") == "linux.apt.package_exact"
    ):
        parameters = automation.get("parameters")
        if isinstance(parameters, dict):
            package = parameters.get("package")
            version = parameters.get("version")
            if isinstance(package, str) and isinstance(version, str):
                return "linux.apt.package_exact", {
                    "package": package,
                    "version": version,
                }

    # A stable unsupported key deliberately compiles to a manual Markdown
    # runbook.  It does not pass finding prose into the executable catalog.
    return "manual.review", {}


def _source_version(finding: Finding, asset: Asset | None) -> str:
    material = {
        "finding_id": str(finding.id),
        "finding_updated_at": getattr(finding, "updated_at", None),
        "finding_status": getattr(finding.status, "value", finding.status),
        "evidence": finding.evidence,
        "remediation": finding.remediation,
        "asset_id": str(asset.id) if asset else None,
        "asset_updated_at": getattr(asset, "updated_at", None) if asset else None,
        "asset_os": asset.os if asset else None,
        "asset_os_version": asset.os_version if asset else None,
    }
    encoded = json.dumps(material, default=str, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def to_workspace_context(
    finding: Finding,
    asset: Asset | None,
    *,
    tenant_id: uuid.UUID,
) -> FindingContext:
    family = os_family(asset.os if asset else None)
    key, parameters = remediation_selector(
        finding.evidence,
        family,
        trusted_detection=isinstance(
            getattr(finding, "detection_run_id", None), uuid.UUID
        ),
    )
    return FindingContext(
        tenant_id=tenant_id,
        engagement_id=finding.engagement_id,
        finding_id=finding.id,
        asset_id=asset.id if asset else None,
        os_family=family,
        os_version=asset.os_version if asset else None,
        title=finding.title,
        remediation_key=key,
        parameters=parameters,
        source_version=_source_version(finding, asset),
    )


async def load_workspace_contexts(
    db: AsyncSession,
    *,
    tenant_id: uuid.UUID,
    finding_ids: Sequence[uuid.UUID],
) -> list[FindingContext]:
    """Resolve the exact authorized selection while hiding cross-tenant IDs."""
    requested = list(finding_ids)
    if not requested or len(requested) > MAX_FINDINGS or len(set(requested)) != len(requested):
        raise RemediationContextConflict(
            f"finding_ids must contain 1-{MAX_FINDINGS} unique identifiers"
        )

    rows = (await db.execute(
        select(Finding, Asset)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .outerjoin(
            Asset,
            and_(
                Finding.asset_id == Asset.id,
                Asset.engagement_id == Finding.engagement_id,
            ),
        )
        .where(
            Finding.id.in_(requested),
            Engagement.tenant_id == tenant_id,
        )
    )).all()
    by_id = {finding.id: (finding, asset) for finding, asset in rows}
    if set(by_id) != set(requested):
        # Deliberately indistinguishable: never disclose whether another tenant
        # owns an identifier.
        raise RemediationContextNotFound("One or more findings were not found")

    engagement_ids = {finding.engagement_id for finding, _asset in by_id.values()}
    if len(engagement_ids) != 1:
        raise RemediationContextConflict(
            "All selected findings must belong to one engagement"
        )
    if any(
        finding.asset_id is not None
        and (
            asset is None
            or getattr(asset, "engagement_id", None) != finding.engagement_id
        )
        for finding, asset in by_id.values()
    ):
        raise RemediationContextConflict(
            "One or more findings have invalid asset context"
        )

    return [
        to_workspace_context(by_id[finding_id][0], by_id[finding_id][1], tenant_id=tenant_id)
        for finding_id in requested
    ]


__all__ = [
    "RemediationContextConflict",
    "RemediationContextNotFound",
    "load_workspace_contexts",
    "os_family",
    "remediation_selector",
    "to_workspace_context",
]
