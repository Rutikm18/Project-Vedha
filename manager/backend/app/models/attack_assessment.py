"""Durable immutable-input jobs and completed finding-centered assessments."""

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Identity,
    Index,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class AttackAssessmentSnapshot(Base, TimestampMixin):
    __tablename__ = "attack_assessment_snapshots"
    __table_args__ = (
        ForeignKeyConstraint(
            ["engagement_id", "tenant_id"],
            ["engagements.id", "engagements.tenant_id"],
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "status IN ('queued','running','completed','failed')",
            name="ck_attack_assessment_status",
        ),
        CheckConstraint(
            "status != 'completed' OR result_document IS NOT NULL",
            name="ck_attack_assessment_completed_result",
        ),
        Index(
            "ix_attack_assessment_scope_sequence",
            "tenant_id",
            "engagement_id",
            "request_sequence",
        ),
        Index(
            "ix_attack_assessment_scope_input",
            "tenant_id",
            "engagement_id",
            "input_hash",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    engagement_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    request_sequence: Mapped[int] = mapped_column(
        BigInteger, Identity(), nullable=False, unique=True
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    effective_as_of: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    known_at_cutoff: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    normalization_version: Mapped[str] = mapped_column(String(64), nullable=False)
    rule_pack_version: Mapped[str] = mapped_column(String(64), nullable=False)
    rule_artifact_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    input_document: Mapped[dict] = mapped_column(JSONB, nullable=False)
    result_document: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    failure_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
