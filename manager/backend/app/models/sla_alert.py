"""
sla_alert.py — which SLA transitions have already been announced.

One row per (finding, state): the watcher inserts it atomically before it notifies,
so a finding entering "at_risk" or "breached" is announced exactly once even with
several workers, restarts, or a notification rule that was off at the time.
"""
from __future__ import annotations

import uuid

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class SlaAlert(Base):
    __tablename__ = "sla_alerts"
    __table_args__ = (UniqueConstraint("finding_id", "state", name="uq_sla_alert_finding_state"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    finding_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("findings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    state: Mapped[str] = mapped_column(String(16), nullable=False)   # at_risk | breached
    notified_at = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
