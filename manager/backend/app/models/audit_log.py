import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, LargeBinary, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AuditLog(Base):
    """
    Immutable, append-only audit trail.
    No TimestampMixin — updated_at would imply mutability.
    Foreign keys use RESTRICT so records survive engagement/finding deletion.

    Append-only is enforced by the database (migration 0066): a trigger refuses
    UPDATE/DELETE/TRUNCATE, and another chains each row to the previous one in its
    tenant (chain_key/chain_pos/prev_hash/row_hash, set by the trigger, never by
    callers). Write through app.services.audit.record_audit.
    """
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    engagement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("engagements.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    detail: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )

    # Who and how. `actor_id` stays a string (a user id, an agent id, or "anonymous");
    # `actor_label` freezes the human-readable identity (an email) at the time, so the
    # entry still reads correctly after the account is renamed or removed.
    tenant_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False, default="success",
                                         server_default="success")   # success | failure | denied
    actor_type: Mapped[str | None] = mapped_column(String(16), nullable=True)  # user|client|agent|system|anonymous
    actor_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    changes: Mapped[dict | None] = mapped_column(JSONB, nullable=True)   # {field: {"before": x, "after": y}}

    # Tamper evidence — assigned by the audit_logs_chain trigger.
    chain_key: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    chain_pos: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    prev_hash: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    row_hash: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
