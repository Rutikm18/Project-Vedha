"""Record who last changed finding remediation text and when.

Revision ID: 0051
Revises: 0050
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0051"
down_revision: Union[str, None] = "0050"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "findings",
        sa.Column("remediation_updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "findings",
        sa.Column("remediation_updated_by", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("findings", "remediation_updated_by")
    op.drop_column("findings", "remediation_updated_at")
