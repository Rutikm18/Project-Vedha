import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ProbeEnrollmentRequest(Base, TimestampMixin):
    __tablename__ = "probe_enrollment_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    state: Mapped[str] = mapped_column(String(24), nullable=False, server_default="awaiting_approval", index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    device_secret_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    user_code_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    signing_public_key: Mapped[str] = mapped_column(String(64), nullable=False)
    encryption_public_key: Mapped[str] = mapped_column(String(64), nullable=False)
    signing_key_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    nonce: Mapped[str] = mapped_column(String(64), nullable=False)
    activation_challenge: Mapped[str | None] = mapped_column(String(128), nullable=True)
    hostname_hint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    platform: Mapped[str] = mapped_column(String(64), nullable=False)
    architecture: Mapped[str] = mapped_column(String(64), nullable=False)
    agent_version: Mapped[str] = mapped_column(String(64), nullable=False)
    installer_version: Mapped[str] = mapped_column(String(64), nullable=False)
    build_digest: Mapped[str] = mapped_column(String(128), nullable=False)
    reported_capabilities: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    source_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    poll_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    denied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    tenant_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True, index=True
    )
    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("probe_sites.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    assigned_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    approved_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    denied_reason: Mapped[str | None] = mapped_column(Text, nullable=True)


class AgentCredential(Base, TimestampMixin):
    __tablename__ = "agent_credentials"
    __table_args__ = (
        UniqueConstraint("agent_id", "generation", name="uq_agent_credential_generation"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    generation: Mapped[int] = mapped_column(Integer, nullable=False)
    refresh_secret_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    signing_public_key: Mapped[str] = mapped_column(String(64), nullable=False)
    signing_key_fingerprint: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_nonce: Mapped[str | None] = mapped_column(String(128), nullable=True)


class ProbeEnrollmentToken(Base, TimestampMixin):
    """Pre-authorized, Site-bound enrollment token.

    Lets a probe auto-enroll (no operator user_code step) while still inheriting
    a bounded Site policy. Mirrors the PersonalAccessToken security shape: only
    the SHA-256 hash is stored, the raw ``vet_...`` token is shown once.
    """

    __tablename__ = "probe_enrollment_tokens"
    __table_args__ = (UniqueConstraint("token_hash", name="uq_probe_enroll_token_hash"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    site_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("probe_sites.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    token_prefix: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    max_uses: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1")
    uses: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
