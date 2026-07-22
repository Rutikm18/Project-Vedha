"""
outbox.py — transactional outbox for durable, exactly-once background work.

THE PROBLEM THIS SOLVES
-----------------------
Heavy post-scan work (detection, AD, attack-graph, AI report) used to be fired
with `asyncio.create_task(...)` straight off the request handler. That is not a
background job — it is a coroutine on the same event loop, in the same process,
with no durability: a pod restart / deploy / OOM between the DB commit and the
task running silently drops the work. No retry, no trace, no finding.

THE PATTERN
-----------
In the SAME database transaction that persists the durable input (the raw facts
in `scan_results`), we insert an `OutboxEvent` row. Because it commits atomically
with the data, there is no dual-write race: either both land or neither does.

A separate worker process then polls this table with `FOR UPDATE SKIP LOCKED`,
processes each event in its own session, and marks it done — giving at-least-once
delivery, retry with backoff, a dead-letter state (`failed`), and backpressure,
all on Postgres we already run (no Redis Streams / broker required for this
throughput; that remains an option if event volume ever outgrows DB polling).
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func, Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


# Status values (plain strings — no PG enum type, keeps migrations trivial).
OUTBOX_PENDING = "pending"
OUTBOX_PROCESSING = "processing"
OUTBOX_DONE = "done"
OUTBOX_FAILED = "failed"          # dead-letter: exhausted max_attempts

# Topics (event names). Handlers are registered per-topic in app.workers.outbox.
TOPIC_FACTS_READY = "facts.ready"


class OutboxEvent(Base, TimestampMixin):
    __tablename__ = "outbox_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    topic: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default=OUTBOX_PENDING)

    # Optional references to the durable data the event is about. The worker
    # re-reads facts from scan_results by id, so the (potentially large) facts
    # array is never duplicated into the event payload.
    engagement_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    scan_result_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Delivery bookkeeping.
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, server_default="5")
    available_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    locked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        # The worker's claim query filters on (status, available_at); this index
        # keeps that scan cheap as the table grows and old 'done' rows accumulate.
        Index("ix_outbox_claim", "status", "available_at"),
    )
