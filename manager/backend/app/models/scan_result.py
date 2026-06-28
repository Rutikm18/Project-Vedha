import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ScanResult(Base, TimestampMixin):
    """Append-only raw probe facts (P3-#10).

    Decoupled from scan_jobs so:
      (a) scan_jobs stays LEAN — the (potentially large) facts array no longer
          bloats every job row's JSONB; and
      (b) detection can be RE-RUN against an updated vuln-DB snapshot WITHOUT
          re-scanning the network — the facts are durable here, keyed by
          engagement, ready to re-feed the detection pipeline any time.

    Never updated in place — one row per submitted facts payload.
    """
    __tablename__ = "scan_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    scan_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    fact_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    facts: Mapped[list] = mapped_column(JSONB, nullable=False)
