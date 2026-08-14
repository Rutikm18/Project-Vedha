import uuid

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Service(Base, TimestampMixin):
    __tablename__ = "services"
    __table_args__ = (
        UniqueConstraint("asset_id", "port", "protocol", name="uq_service_asset_port_proto"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    protocol: Mapped[str] = mapped_column(String(10), nullable=False, server_default="tcp")
    service_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    product: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cpe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    banner: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Path-dependent reachability verdict from the probe's exposure_matrix
    # use-case: external | internal_only | ambiguous | not_exposed. Drives
    # severity escalation — an externally reachable service is higher risk.
    exposure: Mapped[str | None] = mapped_column(String(20), nullable=True)
    extra_info: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    asset: Mapped["Asset"] = relationship(lazy="noload")
