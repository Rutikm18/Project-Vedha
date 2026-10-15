"""Read-only canonical report document for one engagement."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.auth.rbac import require_role
from app.dependencies import AuthUser, ReadDB
from app.schemas.report_document import ReportDocument
from app.services.report_document import load_report_document

router = APIRouter(prefix="/engagements", tags=["reports"])
_REPORT_READER = require_role(["admin", "manager", "tester", "analyst", "auditor"])


def _parse_finding_ids(raw: str | None) -> set[uuid.UUID] | None:
    """Comma-separated finding ids → a scope set. Blank/invalid tokens are
    dropped; an all-invalid or empty value falls back to the whole engagement
    rather than silently emptying the report."""
    if not raw:
        return None
    ids: set[uuid.UUID] = set()
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            ids.add(uuid.UUID(token))
        except ValueError:
            continue
    return ids or None


@router.get(
    "/{engagement_id}/report-document",
    response_model=ReportDocument,
    summary="Canonical engagement report snapshot from recorded data",
)
async def get_report_document(
    engagement_id: uuid.UUID,
    db: ReadDB,
    current_user: Annotated[AuthUser, _REPORT_READER],
    finding_ids: Annotated[
        str | None,
        Query(description="Comma-separated finding ids; scopes the report to this subset."),
    ] = None,
):
    generated_at = datetime.now(timezone.utc)
    document = await load_report_document(
        db,
        tenant_id=current_user.tenant_id,
        engagement_id=engagement_id,
        generated_at=generated_at,
        finding_ids=_parse_finding_ids(finding_ids),
    )
    if document is None:
        # The tenant predicate intentionally makes foreign engagements
        # indistinguishable from missing ones.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )
    return document
