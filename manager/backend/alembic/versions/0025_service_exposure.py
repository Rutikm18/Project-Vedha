"""Service exposure: persist the exposure_matrix reachability verdict.

Adds services.exposure (external | internal_only | ambiguous | not_exposed) so a
finding on an internet-reachable service can be escalated. Part of Track A
(manager ingests the probe's richer facts).

Revision ID: 0025
Revises: 0024
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0025"
down_revision: Union[str, None] = "0024"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("services", sa.Column("exposure", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("services", "exposure")
