"""
validation_request.py — an approval-gated request to safely re-check a finding
live on the probe. Mirrors ExploitApprovalRequest, but for NON-destructive
validation only (no module_path/payload_path). status/outcome are plain strings
(no PG enum) per the DetectionRun precedent.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

VR_PENDING = "pending"
VR_APPROVED = "approved"
VR_REJECTED = "rejected"
VR_EXPIRED = "expired"

CHECK_TLS = "tls_handshake"
CHECK_BANNER = "banner_regrab"
CHECK_SAFE_POC = "safe_poc"


class ValidationRequest(Base, TimestampMixin):
    __tablename__ = "validation_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    finding_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("findings.id", ondelete="SET NULL"), nullable=True, index=True,
    )
    target_ip: Mapped[str] = mapped_column(String(45), nullable=False)
    target_port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    check_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default=VR_PENDING, index=True)
    outcome: Mapped[str | None] = mapped_column(String(16), nullable=True)
    job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    requested_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
