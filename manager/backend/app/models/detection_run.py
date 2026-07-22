"""
detection_run.py — one execution of the deterministic detection engine over a
facts payload. Turns findings from a snapshot into a TIME SERIES.

WHY: previously a Finding row had no provenance and no notion of time beyond
created_at/updated_at. You could not answer "what changed since yesterday", nor
"which vuln-DB snapshot produced this", nor re-run detection with a newer DB and
diff the result. A DetectionRun records:

  * WHICH facts it ran on        (scan_result_id — the append-only raw facts)
  * WHICH vuln-DB it ran against (vuln_db_version = snapshot content hash)
  * WHAT changed                 (findings_new / findings_reaffirmed / current)

Each Finding is stamped with first_seen, last_seen, and the detection_run_id
that last touched it — so a run's delta is a query, and a finding open across
many runs shows a stable first_seen with an advancing last_seen.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


# Status values (plain strings — no PG enum type).
RUN_RUNNING = "running"
RUN_COMPLETED = "completed"
RUN_FAILED = "failed"

# Trigger values (why the run happened).
TRIGGER_FACTS_READY = "facts_ready"   # a probe submitted new facts
TRIGGER_MANUAL = "manual"             # operator re-ran detection (e.g. newer DB)


class DetectionRun(Base, TimestampMixin):
    __tablename__ = "detection_runs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    # Provenance: the raw facts this run consumed (append-only scan_results row).
    scan_result_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    trigger: Mapped[str] = mapped_column(String(32), nullable=False, server_default=TRIGGER_FACTS_READY)
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default=RUN_RUNNING)

    # The exact vuln-DB basis, so two runs are provably comparable (same hash) or
    # visibly NOT the same basis (different hash after a snapshot refresh).
    vuln_db_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    vuln_db_fetched_at: Mapped[str | None] = mapped_column(String(64), nullable=True)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    facts_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    findings_new: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    findings_reaffirmed: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    # Total still-open findings for the engagement after this run (the "current" set).
    findings_current: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    stats: Mapped[dict | None] = mapped_column(JSONB, nullable=True)   # room for per-severity, etc.
