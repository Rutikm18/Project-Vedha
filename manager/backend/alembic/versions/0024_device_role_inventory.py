"""Device-role inventory: persist the probe device_classifier's role on assets.

Adds two AssetType enum values (printer, hypervisor) and three asset columns
(device_role, role_detail, role_confidence) so the device_inventory use-case's
evidence-based classification is stored instead of every host defaulting to
'server'. Part of Track A (manager ingests the probe's richer facts).

Revision ID: 0024
Revises: 0023
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0024"
down_revision: Union[str, None] = "0023"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # New device roles the classifier distinguishes. PG 12+ permits ADD VALUE in
    # a migration transaction; IF NOT EXISTS keeps re-runs idempotent.
    op.execute("ALTER TYPE assettype ADD VALUE IF NOT EXISTS 'printer'")
    op.execute("ALTER TYPE assettype ADD VALUE IF NOT EXISTS 'hypervisor'")

    op.add_column("assets", sa.Column("device_role", sa.String(length=40), nullable=True))
    op.add_column("assets", sa.Column("role_detail", sa.String(length=60), nullable=True))
    op.add_column("assets", sa.Column("role_confidence", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("assets", "role_confidence")
    op.drop_column("assets", "role_detail")
    op.drop_column("assets", "device_role")
    # NOTE: Postgres cannot DROP a single enum value; the added 'printer' /
    # 'hypervisor' labels are left in place on downgrade (harmless, unused).
