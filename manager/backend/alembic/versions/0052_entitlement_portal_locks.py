"""Portal plan locks on customer entitlements

* customer_entitlements.locked_severities — finding severities the customer
  sees only as locked teaser rows (e.g. ["critical", "high"] on a POC).
* customer_entitlements.locked_features — portal features answering
  "available on a licensed plan": ai_assistant, compliance, remediation, reports.

Both default to an empty list, so every existing customer keeps exactly the
access it has today; the operator applies locks per customer at any time.
New POC customers get Critical + High locked by the application, not here.

Revision ID: 0052
Revises: 0051
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0052"
down_revision: Union[str, None] = "0051"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for column in ("locked_severities", "locked_features"):
        op.add_column("customer_entitlements", sa.Column(
            column, postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb")))


def downgrade() -> None:
    for column in ("locked_features", "locked_severities"):
        op.drop_column("customer_entitlements", column)
