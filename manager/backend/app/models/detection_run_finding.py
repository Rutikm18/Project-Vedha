import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# The three outcomes a run can have for a finding. `new` — created this run;
# `reaffirmed` — re-observed as still present (includes a regression reopen);
# `resolved` — this run's coverage proved it gone. Enough to answer "what did
# scan X find" and to diff two scans (new / fixed / still-present).
RUN_FINDING_NEW = "new"
RUN_FINDING_REAFFIRMED = "reaffirmed"
RUN_FINDING_RESOLVED = "resolved"


class DetectionRunFinding(Base):
    """Which findings a detection run touched, and how — the per-scan membership
    that run-level counts can't give. Written in the same transaction as the
    finding writes, so it is exactly as consistent as the run itself."""

    __tablename__ = "detection_run_findings"

    run_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("detection_runs.id", ondelete="CASCADE"),
        primary_key=True)
    finding_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("findings.id", ondelete="CASCADE"),
        primary_key=True, index=True)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)

    # The finding as THIS scan saw it. A finding is one mutable row, so without these a
    # later severity/score/status change would rewrite what an earlier scan "found" and
    # a scan-to-scan diff could not say what changed. NULL for resolved rows and for
    # scans recorded before the snapshot existed (compare then shows presence only).
    severity: Mapped[str | None] = mapped_column(String(16), nullable=True)
    risk_score: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    status: Mapped[str | None] = mapped_column(String(16), nullable=True)
