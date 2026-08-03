import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ScanJobStatus, ScanJobType


class ScanJob(Base, TimestampMixin):
    __tablename__ = "scan_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_type: Mapped[ScanJobType] = mapped_column(
        Enum(ScanJobType, name="scanjobtype"), nullable=False
    )
    status: Mapped[ScanJobStatus] = mapped_column(
        Enum(ScanJobStatus, name="scanjobstatus"), nullable=False, server_default="pending", index=True
    )
    agent_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # Lease for a claimed (running) job: set at claim time, renewed on each probe
    # heartbeat. The reaper requeues running jobs whose lease has expired (dead probe).
    lease_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    # The logical job owns a monotonically increasing execution fence. A claim
    # creates a separate ScanJobAttempt and installs it as the only current
    # attempt; heartbeat and completion must present both values.
    current_attempt_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "scan_job_attempts.id",
            ondelete="SET NULL",
            deferrable=True,
            initially="DEFERRED",
            use_alter=True,
            name="fk_scan_jobs_current_attempt_id",
        ),
        nullable=True,
        index=True,
    )
    current_fence: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default="0")
    attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, server_default="3")

    engagement: Mapped["Engagement"] = relationship(back_populates="scan_jobs", lazy="noload")
