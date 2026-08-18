"""
scan_request.py — a customer-initiated, operator-approved request to run a scan
on an engagement's assigned agent.

The customer creates it (status=pending); an operator approves or rejects it. On
approval a ScanJob is dispatched and linked via scan_job_id. The customer can
never run a scan directly — this request/review split is the control. Mirrors
ValidationRequest (plain-string status, no PG enum, per the DetectionRun precedent).
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

SR_PENDING = "pending"
SR_APPROVED = "approved"
SR_REJECTED = "rejected"


class ScanRequest(Base, TimestampMixin):
    __tablename__ = "scan_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    # The client user (User.id) who raised the request.
    requested_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    # A ScanJobType value (e.g. "discovery", "vuln_scan"); plain string like status.
    scan_type: Mapped[str] = mapped_column(String(32), nullable=False, server_default="vuln_scan")
    # The capability use-case the customer picked (operator _USE_CASES catalog id,
    # e.g. "uc_device_inventory"). NULL for legacy scan_type-only requests. Threaded
    # into the approved ScanJob so the probe runs exactly this use case.
    use_case_id: Mapped[str | None] = mapped_column(String(40), nullable=True)
    # Specific in-scope targets the customer asked to scan (IP/CIDR/range strings),
    # each proven subset of the engagement scope at request time. NULL = whole scope.
    targets: Mapped[list[str] | None] = mapped_column(JSONB, nullable=True)
    # Scan hardness: "light" | "standard" | "deep". NULL = use the use-case default.
    intensity: Mapped[str | None] = mapped_column(String(16), nullable=True)
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default=SR_PENDING, index=True
    )
    note: Mapped[str | None] = mapped_column(Text(), nullable=True)
    # Set when an operator approves and dispatches the scan.
    scan_job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_jobs.id", ondelete="SET NULL"), nullable=True,
    )
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    review_reason: Mapped[str | None] = mapped_column(Text(), nullable=True)
