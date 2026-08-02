import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(50), nullable=False, server_default="free")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # Added migration 0016: soft-disable without cascade-deleting users.
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")

    users: Mapped[list["User"]] = relationship(back_populates="tenant", lazy="noload")
    engagements: Mapped[list["Engagement"]] = relationship(back_populates="tenant", lazy="noload")
