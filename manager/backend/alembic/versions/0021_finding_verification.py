"""Finding verification verdict columns (P2 passive verification).

Revision ID: 0021
Revises: 0020
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0021"
down_revision: Union[str, None] = "0020"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("findings", sa.Column("verification_state", sa.String(length=16), nullable=True))
    op.add_column("findings", sa.Column("verification_confidence", sa.Integer(), nullable=True))
    op.add_column("findings", sa.Column("verification_rationale", sa.Text(), nullable=True))
    op.add_column("findings", sa.Column("needs_review", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("findings", sa.Column("verification_method", sa.String(length=16), nullable=True))
    op.create_index("ix_findings_verification_state", "findings", ["verification_state"])
    op.create_index("ix_findings_needs_review", "findings", ["needs_review"])


def downgrade() -> None:
    op.drop_index("ix_findings_needs_review", table_name="findings")
    op.drop_index("ix_findings_verification_state", table_name="findings")
    for col in ("verification_method", "needs_review", "verification_rationale",
                "verification_confidence", "verification_state"):
        op.drop_column("findings", col)
