"""Read-only canonical report document for one engagement."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, HTTPException, status

from app.auth.rbac import require_role
from app.dependencies import AuthUser, ReadDB
from app.schemas.report_document import ReportDocument
from app.services.report_document import load_report_document

router = APIRouter(prefix="/engagements", tags=["reports"])
_REPORT_READER = require_role(["admin", "manager", "tester", "analyst", "auditor"])


@router.get(
    "/{engagement_id}/report-document",
    response_model=ReportDocument,
    summary="Canonical engagement report snapshot from recorded data",
)
async def get_report_document(
    engagement_id: uuid.UUID,
    db: ReadDB,
    current_user: Annotated[AuthUser, _REPORT_READER],
):
    generated_at = datetime.now(timezone.utc)
    document = await load_report_document(
        db,
        tenant_id=current_user.tenant_id,
        engagement_id=engagement_id,
        generated_at=generated_at,
    )
    if document is None:
        # The tenant predicate intentionally makes foreign engagements
        # indistinguishable from missing ones.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found",
        )
    return document
