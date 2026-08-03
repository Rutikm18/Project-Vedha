import uuid

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class ProbeSite(Base, TimestampMixin):
    __tablename__ = "probe_sites"
    __table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_probe_site_tenant_name"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default="active")
    authorized_cidrs: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    excluded_cidrs: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    approved_capabilities: Mapped[list[str]] = mapped_column(ARRAY(Text()), nullable=False, server_default="{}")
    max_targets: Mapped[int] = mapped_column(Integer, nullable=False, server_default="4096")
    max_job_seconds: Mapped[int] = mapped_column(Integer, nullable=False, server_default="7200")
    max_rate_pps: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1000")
    policy_version: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default="1")
    update_channel: Mapped[str] = mapped_column(String(32), nullable=False, server_default="stable")
