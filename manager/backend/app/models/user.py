import uuid

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import UserRole


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
        UniqueConstraint("tenant_id", "portal_slug", name="uq_user_tenant_portal_slug"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="userrole"), nullable=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    # Added migration 0016: soft-disable without deleting the record.
    # All existing rows get server_default=True — no data loss.
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    # Optional password expiry. NULL = never expires. Set to enforce rotation policy.
    password_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # role == client only: the temp password ENCRYPTED at rest (Fernet, keyed off
    # jwt_secret via credential_crypto) so an operator can re-reveal it. NULL for
    # logins provisioned before this existed → operator resets to populate. Auth
    # still uses hashed_password (bcrypt); this is a separate recoverable copy.
    portal_password_enc: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Set ONLY for role == client — binds this login to exactly one engagement
    # (the customer-portal scoping boundary). SET NULL so deleting an engagement
    # disables the login rather than deleting the user record.
    client_engagement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )

    # Set ONLY for role == client. A URL-safe per-customer handle ("user as
    # domain"): brands the shared portal today, becomes <slug>.portal.<domain>
    # once a wildcard domain is configured. Unique per tenant (see __table_args__).
    portal_slug: Mapped[str | None] = mapped_column(String(63), nullable=True)

    tenant: Mapped["Tenant"] = relationship(back_populates="users", lazy="noload")
