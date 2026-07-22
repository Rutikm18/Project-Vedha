import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus


class Finding(Base, TimestampMixin):
    __tablename__ = "findings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True
    )
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="SET NULL"), nullable=True, index=True
    )
    cve_ids: Mapped[list[str] | None] = mapped_column(ARRAY(Text()), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    cvss_score: Mapped[Decimal | None] = mapped_column(Numeric(4, 1), nullable=True)
    cvss_vector: Mapped[str | None] = mapped_column(String(200), nullable=True)
    epss_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 4), nullable=True)
    risk_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    severity: Mapped[FindingSeverity] = mapped_column(
        Enum(FindingSeverity, name="findingseverity"), nullable=False, index=True
    )
    status: Mapped[FindingStatus] = mapped_column(
        Enum(FindingStatus, name="findingstatus"), nullable=False, server_default="open", index=True
    )
    exploitable: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    exploit_validated: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    mitre_techniques: Mapped[list[str] | None] = mapped_column(ARRAY(Text()), nullable=True)
    detection_status: Mapped[DetectionStatus] = mapped_column(
        Enum(DetectionStatus, name="detectionstatus"), nullable=False, server_default="unknown"
    )
    evidence: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    remediation: Mapped[str | None] = mapped_column(Text(), nullable=True)

    # ── Temporal / provenance (detection-run time series) ──────────────────────
    # first_seen: when detection FIRST produced this finding (stable across runs).
    # last_seen:  the most recent run that reaffirmed it (advances each run).
    # A finding whose last_seen lags the engagement's latest run was NOT observed
    # in that run — i.e. a resolution candidate (surfaced, never auto-closed).
    # detection_run_id: the run that last touched it (null for non-engine sources).
    first_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    detection_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("detection_runs.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )

    engagement: Mapped["Engagement"] = relationship(back_populates="findings", lazy="noload")
    asset: Mapped["Asset | None"] = relationship(back_populates="findings", lazy="noload")
    detection_results: Mapped[list["DetectionResult"]] = relationship(
        back_populates="finding", lazy="noload"
    )
