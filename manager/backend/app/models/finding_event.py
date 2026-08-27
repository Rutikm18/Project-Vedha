import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class FindingEvent(Base):
    """
    Append-only lifecycle audit trail for a single finding — one row per
    transition (detected, confirmed, remediated, accepted, reopened, resolved, …)
    with the actor who caused it and the exact timestamp it happened.

    No TimestampMixin: an audit record is immutable, so an `updated_at` would be a
    lie. Deleting the parent finding cascades (the trail has no meaning without it).
    `event_type` is a plain string (values from enums.FindingEventType) so the log
    accepts new event kinds without a schema migration.
    """

    __tablename__ = "finding_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    finding_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("findings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    # Who caused it: a user id (manual action) or a system actor name
    # ("auto-resolution", "detection-engine", "network-VA campaign").
    actor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    actor_type: Mapped[str] = mapped_column(String(16), nullable=False, server_default="system")
    # Lifecycle transitions carry the before/after status (FindingStatus values).
    from_status: Mapped[str | None] = mapped_column(String(16), nullable=True)
    to_status: Mapped[str | None] = mapped_column(String(16), nullable=True)
    # Free-form context: run id, cvss before/after, rule id, note text, reason…
    detail: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )
