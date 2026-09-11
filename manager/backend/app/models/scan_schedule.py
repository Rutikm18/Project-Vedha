import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ScanSchedule(Base, TimestampMixin):
    """A recurring scan.

    Vedha could only ever be told "scan now". Every run therefore started from
    scratch and nothing re-checked an estate on its own, which is the difference
    between an assessment TOOL and a monitoring PRODUCT: exposure that appears on
    a Tuesday is invisible until someone remembers to look.

    The schedule is deliberately dumb — an interval and a next-due timestamp, not
    a cron expression. Cron buys calendar precision nobody has asked for and
    costs a parser, a timezone story, and a class of "why did it not fire"
    support questions. `next_run_at` as a plain column also means "what is due"
    is one indexed query rather than evaluating every schedule on every tick.
    """

    __tablename__ = "scan_schedules"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    # What to run: the same use-case id and intensity an operator picks by hand,
    # so a scheduled run and a manual one are the same job through the same
    # enqueue path — scope, capability and queue-cap checks all still apply.
    use_case_id: Mapped[str] = mapped_column(String(64), nullable=False)
    intensity: Mapped[int] = mapped_column(Integer, nullable=False, server_default="2")

    interval_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    # Disabled rather than deleted: pausing a schedule during a change freeze is
    # routine, and deleting loses the configuration and its history.
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    last_run_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True,
    )
    # Indexed: the worker's only question is "what is due now", and that must not
    # table-scan every schedule in the system on every tick.
    next_run_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True,
    )
    # Who set it up. SET NULL on user deletion — the schedule must keep running
    # when someone leaves the company.
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
    )
