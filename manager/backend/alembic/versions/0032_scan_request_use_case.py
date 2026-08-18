"""scan_requests.use_case_id — the capability use-case a customer requested.

The portal now offers the operator use-case catalog (agents._USE_CASES) instead
of a hardcoded, partly-aspirational scan_type list. The chosen use-case id is
stored here so the approved ScanJob runs exactly that use case. Nullable —
existing rows keep NULL (they used the coarse scan_type only).

Revision ID: 0032
Revises: 0031
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0032"
down_revision: Union[str, None] = "0031"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "scan_requests",
        sa.Column("use_case_id", sa.String(length=40), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("scan_requests", "use_case_id")
