"""Selected-engagement manifest; source snapshots remain individually scoped."""

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class EnvironmentAssessment(Base, TimestampMixin):
    __tablename__ = "environment_assessments"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id", "idempotency_key", name="uq_environment_assessment_key"
        ),
        CheckConstraint(
            "status IN ('queued','running','completed','failed')",
            name="ck_environment_assessment_status",
        ),
        CheckConstraint(
            "status != 'completed' OR result_document IS NOT NULL",
            name="ck_environment_assessment_result",
        ),
        CheckConstraint(
            "cardinality(engagement_ids) BETWEEN 1 AND 20",
            name="ck_environment_assessment_scope_count",
        ),
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    idempotency_key: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    request_sequence: Mapped[int] = mapped_column(
        BigInteger, Identity(), unique=True, nullable=False
    )
    engagement_ids: Mapped[list[uuid.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True)), nullable=False
    )
    status: Mapped[str] = mapped_column(String(16), default="queued", nullable=False)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    effective_as_of: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    input_document: Mapped[dict] = mapped_column(JSONB, nullable=False)
    result_document: Mapped[dict | None] = mapped_column(JSONB)
    failure_code: Mapped[str | None] = mapped_column(String(64))
