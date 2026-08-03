import uuid
from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ScanJobAttempt(Base, TimestampMixin):
    """One immutable, fenced execution claim for a logical scan job."""

    __tablename__ = "scan_job_attempts"
    __table_args__ = (
        UniqueConstraint("job_id", "attempt_number", name="uq_scan_job_attempt_number"),
        UniqueConstraint("job_id", "fence", name="uq_scan_job_attempt_fence"),
        CheckConstraint("attempt_number > 0", name="ck_scan_job_attempt_number_positive"),
        CheckConstraint("fence > 0", name="ck_scan_job_attempt_fence_positive"),
        CheckConstraint(
            "status IN ('running', 'succeeded', 'failed', 'expired', 'cancelled', 'stale')",
            name="ck_scan_job_attempt_status",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("scan_jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    fence: Mapped[int] = mapped_column(BigInteger, nullable=False)
    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="running")
    claimed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    lease_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    result_checksum: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
