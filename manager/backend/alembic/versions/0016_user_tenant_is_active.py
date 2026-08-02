"""Add is_active to users and tenants; add password_expires_at to users.

All existing rows default to is_active=TRUE and password_expires_at=NULL,
so this migration has zero data impact and is safe to run on live production.

Revision ID: 0016
Revises: 0015
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0016"
down_revision: Union[str, None] = "0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users: soft-disable flag + optional password expiry
    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "password_expires_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # tenants: soft-disable flag
    op.add_column(
        "tenants",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )


def downgrade() -> None:
    op.drop_column("tenants", "is_active")
    op.drop_column("users", "password_expires_at")
    op.drop_column("users", "is_active")
