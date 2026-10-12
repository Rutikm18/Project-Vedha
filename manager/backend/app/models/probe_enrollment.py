import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
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
    __table_args__ = (
        UniqueConstraint("token_hash", name="uq_probe_enroll_token_hash"),
        CheckConstraint(
            "site_id IS NOT NULL OR engagement_id IS NOT NULL",
            name="ck_probe_enrollment_tokens_target",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Exactly what the token installs an agent for: a pre-built Site (operator
    # API), or an engagement — then the Site is built from the engagement's scope
    # when the agent enrols and the agent is assigned to that engagement.
    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("probe_sites.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    engagement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=True, index=True
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


class AgentInstallCode(Base, TimestampMixin):
    """A one-time *install code* the operator hands a Windows client (``vac_...``).

    Unlike a ProbeEnrollmentToken, this row stores **no enrolment secret**: it is a
    pointer that authorises minting exactly one ``vet_`` token, once, at redeem
    time. The client pastes only this opaque code — never the manager URL, a key,
    or a token. On redeem the manager mints the real ``vet_`` for the bound
    engagement/Site, hands it back over TLS, and burns the code.

    Only the SHA-256 of the raw code is stored; the raw ``vac_...`` is shown once.
    Single-use redeem + the minted token's ``max_uses=1`` together bind the whole
    install to the first machine that redeems — a stolen-but-already-redeemed code
    is dead, and the redeemer's IP is recorded for the operator to sanity-check.
    """

    __tablename__ = "agent_install_codes"
    __table_args__ = (
        UniqueConstraint("code_hash", name="uq_agent_install_code_hash"),
        CheckConstraint(
            "site_id IS NOT NULL OR engagement_id IS NOT NULL",
            name="ck_agent_install_codes_target",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Exactly one target (same rule as ProbeEnrollmentToken): the vet_ minted on
    # redeem installs for this engagement, or into this pre-built Site.
    engagement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=True, index=True
    )
    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("probe_sites.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    code_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    code_prefix: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    redeemed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    redeemed_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    # The vet_ this code minted on redeem — traceability from the pasted code all
    # the way to the enrolled agent. Never the raw token, only its row id.
    minted_token_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("probe_enrollment_tokens.id", ondelete="SET NULL"), nullable=True, index=True
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
