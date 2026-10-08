import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AttackPathAnalysis(Base):
    """The engagement-level result of the last attack-path computation (P5).

    Per-path rows (`attack_paths`) describe individual routes. Facts that belong
    to the WHOLE engagement — which hosts are the choke points, the minimum fix
    set, coverage of the scanned space, why a result is empty — were previously
    smeared across every path row (FM-26) or recomputed on every read (FM-22).
    One row per engagement, replaced on each recompute."""
    __tablename__ = "attack_path_analyses"

    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), primary_key=True
    )
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    path_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    analysis: Mapped[dict] = mapped_column(JSONB, nullable=False)
