"""
worker_heartbeat.py — one row per background worker process, refreshed every tick.

The outbox worker's liveness was previously maintained only by human discipline
("the worker MUST be running"). This makes the system OBSERVE it: a heartbeat older
than a threshold means the detection worker is down, which campaign-progress uses to
distinguish "worker is down" from "worker is busy on a backlog" — and which a health
view can surface directly. Keyed by worker_name so N workers each keep their own row.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class WorkerHeartbeat(Base, TimestampMixin):
    __tablename__ = "worker_heartbeats"

    worker_name: Mapped[str] = mapped_column(String(128), primary_key=True)
    last_beat_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    meta: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
