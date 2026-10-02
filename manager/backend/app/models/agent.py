import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin
import enum


class AgentStatus(str, enum.Enum):
    online = "online"
    offline = "offline"
    busy = "busy"
    #: Connected and healthy, but REFUSING work — its result spool is at the
    #: high-water mark, so taking another job would only produce more
    #: undeliverable results. Deliberately not `online`: both dispatch paths
    #: select on that, so a paused probe stops being offered jobs, and the
    #: fleet view can say "paused" instead of showing a healthy idle probe
    #: that silently declines everything.
    paused = "paused"


class Agent(Base, TimestampMixin):
    __tablename__ = "agents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    capabilities: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    network_segments: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    status: Mapped[AgentStatus] = mapped_column(
        Enum(AgentStatus, name="agentstatus"), nullable=False, server_default="offline"
    )
    last_heartbeat: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    current_job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    # X25519 public key for end-to-end scope encryption (Phase 4).
    # base64-encoded 32-byte raw key. NULL = agent hasn't registered a key yet
    # (scope is sent in the clear inside the TLS tunnel, as it always was).
    public_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    site_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("probe_sites.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    lifecycle_status: Mapped[str] = mapped_column(String(24), nullable=False, server_default="active")
    signing_public_key: Mapped[str | None] = mapped_column(String(64), nullable=True)
    signing_key_fingerprint: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    credential_generation: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    approved_capabilities: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    approved_networks: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    agent_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    installer_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    build_digest: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # Access expiry set from Fleet (migration 0053). NULL = no expiry. Enforced by
    # the manager: past this instant the agent is refused heartbeats, job polls and
    # token refreshes (in-flight result/chunk uploads are still accepted so a scan
    # running at expiry isn't lost). Extending the date restores access with no
    # reinstall — nothing on the agent host enforces it, so a changed clock or a
    # patched binary can't get around it.
    access_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
