"""Contextual remediation — due dates, extension requests, bundle-capable plans

* findings.due_at / due_at_source — an approved extension's due date. Absent,
  the due date is computed from the SLA policy (engagement → tenant → env).
* deadline_extension_requests — customer requests for a later due date on a
  finding or a fix bundle; an operator approves (optionally with another date)
  or rejects. Member finding ids are snapshotted at request time.
* remediation_plans — AI refinements may now target a fix BUNDLE:
  subject_type ('finding' | 'bundle'), fix_key, facts_fingerprint (staleness).
  finding_id becomes nullable for bundle rows; the existing
  UNIQUE(finding_id, os) still governs finding rows (NULLs never conflict) and a
  partial unique index governs bundle rows.

Revision ID: 0048
Revises: 0047
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0048"
down_revision: Union[str, None] = "0047"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("findings", sa.Column("due_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("findings", sa.Column("due_at_source", sa.String(16), nullable=True))

    op.create_table(
        "deadline_extension_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject_type", sa.String(8), nullable=False),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("findings.id", ondelete="CASCADE"), nullable=True),
        sa.Column("fix_key", sa.String(12), nullable=True),
        sa.Column("member_finding_ids", postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False),
        sa.Column("current_due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("requested_due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("compensating_control", sa.Text(), nullable=True),
        sa.Column("status", sa.String(10), nullable=False, server_default="pending"),
        sa.Column("requested_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("decided_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("decided_due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("decision_note", sa.Text(), nullable=True),
        sa.CheckConstraint("subject_type IN ('finding', 'bundle')", name="ck_extension_subject_type"),
        sa.CheckConstraint(
            "(subject_type = 'finding' AND finding_id IS NOT NULL) OR "
            "(subject_type = 'bundle' AND fix_key IS NOT NULL)", name="ck_extension_subject_ref"),
        sa.CheckConstraint("status IN ('pending', 'approved', 'rejected', 'withdrawn')",
                           name="ck_extension_status"),
    )
    op.create_index("ix_extension_engagement_status", "deadline_extension_requests",
                    ["engagement_id", "status"])
    op.create_index("ix_extension_finding", "deadline_extension_requests", ["finding_id"])

    op.add_column("remediation_plans", sa.Column("subject_type", sa.String(8), nullable=False,
                                                 server_default="finding"))
    op.add_column("remediation_plans", sa.Column("fix_key", sa.String(12), nullable=True))
    op.add_column("remediation_plans", sa.Column("facts_fingerprint", sa.String(64), nullable=True))
    op.alter_column("remediation_plans", "finding_id", nullable=True)
    op.create_check_constraint(
        "ck_remediation_subject", "remediation_plans",
        "(subject_type = 'finding' AND finding_id IS NOT NULL) OR "
        "(subject_type = 'bundle' AND fix_key IS NOT NULL)")
    op.create_index("uq_remediation_bundle_os", "remediation_plans", ["engagement_id", "fix_key", "os"],
                    unique=True, postgresql_where=sa.text("subject_type = 'bundle'"))


def downgrade() -> None:
    op.drop_index("uq_remediation_bundle_os", table_name="remediation_plans")
    op.drop_constraint("ck_remediation_subject", "remediation_plans", type_="check")
    op.execute("DELETE FROM remediation_plans WHERE subject_type = 'bundle'")
    op.alter_column("remediation_plans", "finding_id", nullable=False)
    op.drop_column("remediation_plans", "facts_fingerprint")
    op.drop_column("remediation_plans", "fix_key")
    op.drop_column("remediation_plans", "subject_type")

    op.drop_index("ix_extension_finding", table_name="deadline_extension_requests")
    op.drop_index("ix_extension_engagement_status", table_name="deadline_extension_requests")
    op.drop_table("deadline_extension_requests")

    op.drop_column("findings", "due_at_source")
    op.drop_column("findings", "due_at")
