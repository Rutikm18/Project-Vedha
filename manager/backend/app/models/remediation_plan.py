"""
remediation_plan.py — a generated, OS-specific remediation plan for a finding.

Cached per (finding_id, os) so the AI is billed once per finding/OS. `source` is
"ai" (LLM-generated, command-safety-validated) or "deterministic_kb" (the pure
knowledge-base fallback). `reviewed` gates whether an AI plan may be shown to the
customer portal — unreviewed AI stays operator-only, mirroring the report-approval
gate. The plan JSON is the structured schema the API and UI render.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, DateTime, ForeignKey, Index, String,
    UniqueConstraint, func, text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class RemediationPlan(Base, TimestampMixin):
    __tablename__ = "remediation_plans"
    __table_args__ = (
        UniqueConstraint("finding_id", "os", name="uq_remediation_finding_os"),
        CheckConstraint(
            "(subject_type = 'finding' AND finding_id IS NOT NULL) OR "
            "(subject_type = 'bundle' AND fix_key IS NOT NULL)",
            name="ck_remediation_subject",
        ),
        Index("uq_remediation_bundle_os", "engagement_id", "fix_key", "os", unique=True,
              postgresql_where=text("subject_type = 'bundle'")),
    )

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
    # Null for bundle rows (subject_type="bundle", keyed by fix_key instead).
    finding_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("findings.id", ondelete="CASCADE"),
        nullable=True, index=True,
    )
    # "finding" | "bundle" — a bundle refinement covers every finding a fix closes.
    subject_type: Mapped[str] = mapped_column(String(8), nullable=False, server_default="finding")
    fix_key: Mapped[str | None] = mapped_column(String(12), nullable=True)
    # sha256 of the asset/service facts the refinement was generated from; a
    # mismatch with the live facts marks the cached plan stale.
    facts_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # "linux" | "windows" | "macos" | "generic"
    os: Mapped[str] = mapped_column(String(16), nullable=False)
    plan: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # "ai" | "deterministic_kb"
    source: Mapped[str] = mapped_column(String(16), nullable=False)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # An AI plan is operator-only until reviewed; the portal shows KB otherwise.
    reviewed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
