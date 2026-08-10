import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
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
    # Composite risk is scored on 0–1000. Numeric(6, 2) is required to persist
    # the valid maximum 1000.00; Numeric(5, 2) overflowed at 999.99.
    risk_score: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
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

    # ── Resolution lifecycle (coverage-gated auto-resolution) ──────────────────
    # resolution_miss_count: consecutive coverage-proven runs this finding was
    #   ABSENT (reset to 0 the moment it is re-observed). > 0 while status=open
    #   means "pending remediation" — inside the confirmation window.
    # detected_db_version: the vuln-DB snapshot hash that produced this finding.
    #   Used to tell "gone because patched" from "gone because the DB changed"
    #   (never auto-resolve on the latter).
    # resolution_run_id: the run that auto-closed it; resolution_method: auto|manual.
    resolution_miss_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    resolution_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("detection_runs.id", ondelete="SET NULL"), nullable=True
    )
    reopened_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    detected_db_version: Mapped[str | None] = mapped_column(String(128), nullable=True)

    # ── Verification (P2 passive; P3 adds active) ──────────────────────────────
    # verification_state: normalized dashboard verdict — confirmed | corroborated
    #   | inferred | contradicted. Distinct from `status` (lifecycle) and from the
    #   internal 0-100 confidence: it's the human-facing "how sure are we this is
    #   real". needs_review flags a high-stakes uncertain finding for an analyst.
    verification_state: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    verification_confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)
    verification_rationale: Mapped[str | None] = mapped_column(Text(), nullable=True)
    needs_review: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", index=True)
    verification_method: Mapped[str | None] = mapped_column(String(16), nullable=True)

    engagement: Mapped["Engagement"] = relationship(back_populates="findings", lazy="noload")
    asset: Mapped["Asset | None"] = relationship(back_populates="findings", lazy="noload")
    detection_results: Mapped[list["DetectionResult"]] = relationship(
        back_populates="finding", lazy="noload"
    )
