"""Agent access expiry, set from Fleet and enforced by the manager.

Past agents.access_expires_at the manager refuses the agent's heartbeats, job
polls and token refreshes (in-flight result uploads still land). NULL = no
expiry. Server-side only, so a changed host clock can't bypass it.

Revision ID: 0053
Revises: 0052
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0053"
down_revision: Union[str, None] = "0052"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "agents",
        sa.Column("access_expires_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("agents", "access_expires_at")
