import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AttackPathSnapshot(Base):
    """One line of an engagement's attack-path history: the headline numbers of ONE computation.

    `attack_path_analyses` keeps only the latest analysis, so nothing could say whether the
    picture was changing. A snapshot is small (counts and a few labels, never the analysis) and is
    written whenever the analysis is, so a trend can be drawn without keeping old analyses.

    Counts are nullable on purpose: an analysis that did not record per-jewel data leaves them
    NULL ("unknown"), which a trend must never draw as zero. `assets_seen` and `coverage` are what
    the computation was given to look at, so a change that comes from seeing more of the network
    can be told apart from one that comes from the network.
    """
    __tablename__ = "attack_path_snapshots"
    __table_args__ = (Index("ix_attack_path_snapshots_engagement_time", "engagement_id", "computed_at"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False
    )
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    # "manual" (someone opened or recomputed it) or "detection" (a detection run changed the findings)
    trigger: Mapped[str] = mapped_column(String(16), nullable=False, server_default="manual")
    state: Mapped[str] = mapped_column(String(16), nullable=False)
    jewels_total: Mapped[int | None] = mapped_column(Integer, nullable=True)
    jewels_reachable: Mapped[int | None] = mapped_column(Integer, nullable=True)
    jewels_exposed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fix_set_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    entry_points: Mapped[int | None] = mapped_column(Integer, nullable=True)
    path_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    assets_seen: Mapped[int | None] = mapped_column(Integer, nullable=True)
    coverage: Mapped[str | None] = mapped_column(String(16), nullable=True)
