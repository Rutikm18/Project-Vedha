"""Allow the documented 0-1000 finding risk score range.

Revision ID: 0015
Revises: 0014
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0015"
down_revision: Union[str, None] = "0014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "findings",
        "risk_score",
        existing_type=sa.Numeric(5, 2),
        type_=sa.Numeric(6, 2),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "findings",
        "risk_score",
        existing_type=sa.Numeric(6, 2),
        type_=sa.Numeric(5, 2),
        existing_nullable=True,
    )
