"""Scoped immutable attack-assessment input snapshots and durable results.

Revision ID: 0063
Revises: 0062
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.db_rls import enable_statements

revision = "0063"
down_revision = "0062"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        "uq_engagement_id_tenant", "engagements", ["id", "tenant_id"]
    )
    op.create_table(
        "attack_assessment_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("idempotency_key", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "request_sequence",
            sa.BigInteger(),
            sa.Identity(),
            nullable=False,
            unique=True,
        ),
        sa.Column("status", sa.String(16), nullable=False, server_default="queued"),
        sa.Column("input_hash", sa.String(64), nullable=False),
        sa.Column("effective_as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("known_at_cutoff", sa.DateTime(timezone=True), nullable=False),
        sa.Column("normalization_version", sa.String(64), nullable=False),
        sa.Column("rule_pack_version", sa.String(64), nullable=False),
        sa.Column("rule_artifact_sha256", sa.String(64), nullable=False),
        sa.Column("input_document", postgresql.JSONB(), nullable=False),
        sa.Column("result_document", postgresql.JSONB(), nullable=True),
        sa.Column("failure_code", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["engagement_id", "tenant_id"],
            ["engagements.id", "engagements.tenant_id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "tenant_id",
            "engagement_id",
            "idempotency_key",
            name="uq_attack_assessment_request_key",
        ),
        sa.CheckConstraint(
            "status IN ('queued','running','completed','failed')",
            name="ck_attack_assessment_status",
        ),
        sa.CheckConstraint(
            "status != 'completed' OR result_document IS NOT NULL",
            name="ck_attack_assessment_completed_result",
        ),
    )
    op.create_index(
        "ix_attack_assessment_scope_sequence",
        "attack_assessment_snapshots",
        ["tenant_id", "engagement_id", "request_sequence"],
    )
    op.create_index(
        "ix_attack_assessment_scope_input",
        "attack_assessment_snapshots",
        ["tenant_id", "engagement_id", "input_hash"],
    )
    # Match main's dormant RLS policy. Do not add this table to migration 0062's
    # shared table list: it does not exist when that older migration runs.
    for statement in enable_statements("attack_assessment_snapshots"):
        op.execute(statement)
    op.execute("""
        CREATE FUNCTION protect_attack_assessment_snapshot() RETURNS trigger AS $$
        BEGIN
          IF (NEW.id, NEW.created_at, NEW.tenant_id, NEW.engagement_id, NEW.idempotency_key, NEW.request_sequence, NEW.input_hash,
              NEW.effective_as_of, NEW.known_at_cutoff, NEW.normalization_version,
              NEW.rule_pack_version, NEW.rule_artifact_sha256, NEW.input_document)
             IS DISTINCT FROM
             (OLD.id, OLD.created_at, OLD.tenant_id, OLD.engagement_id, OLD.idempotency_key, OLD.request_sequence, OLD.input_hash,
              OLD.effective_as_of, OLD.known_at_cutoff, OLD.normalization_version,
              OLD.rule_pack_version, OLD.rule_artifact_sha256, OLD.input_document) THEN
            RAISE EXCEPTION 'attack assessment inputs are immutable';
          END IF;
          IF OLD.status = 'completed' AND NEW IS DISTINCT FROM OLD THEN
            RAISE EXCEPTION 'completed attack assessments are immutable';
          END IF;
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER protect_attack_assessment_snapshot
        BEFORE UPDATE ON attack_assessment_snapshots
        FOR EACH ROW EXECUTE FUNCTION protect_attack_assessment_snapshot();
    """)


def downgrade():
    op.drop_table("attack_assessment_snapshots")
    op.execute("DROP FUNCTION protect_attack_assessment_snapshot()")
    op.drop_constraint("uq_engagement_id_tenant", "engagements", type_="unique")
