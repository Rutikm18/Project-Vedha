"""Site-scoped asset identity (attack-path plan P1b)

* assets.site_id — nullable FK to probe_sites. NULL keeps today's identity (the
  IP alone). Set only for private IPs on engagements that opt into per-site
  identity (rules_of_engagement.asset_identity = 'per_site'), so two sites using
  the same private range no longer merge into one asset.
* ix_assets_engagement_ip_site — the (engagement, ip, site) identity lookup.

Every existing row keeps site_id NULL, so behaviour is unchanged until an
engagement opts in. ON DELETE SET NULL: retiring a site must not delete assets.

Revision ID: 0055
Revises: 0054
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0055"
down_revision: Union[str, None] = "0054"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("assets", sa.Column(
        "site_id", postgresql.UUID(as_uuid=True),
        sa.ForeignKey("probe_sites.id", ondelete="SET NULL", name="fk_assets_site_id"),
        nullable=True))
    op.create_index("ix_assets_engagement_ip_site", "assets",
                    ["engagement_id", "ip_address", "site_id"])


def downgrade() -> None:
    op.drop_index("ix_assets_engagement_ip_site", table_name="assets")
    op.drop_constraint("fk_assets_site_id", "assets", type_="foreignkey")
    op.drop_column("assets", "site_id")
