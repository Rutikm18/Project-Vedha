"""Immutable selected-engagement assessment manifests.

Revision ID: 0064
Revises: 0063
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from app.db_rls import enable_statements

revision = "0064"
down_revision = "0063"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "environment_assessments",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "tenant_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("idempotency_key", pg.UUID(as_uuid=True)),
        sa.Column(
            "request_sequence",
            sa.BigInteger(),
            sa.Identity(),
            nullable=False,
            unique=True,
        ),
        sa.Column("engagement_ids", pg.ARRAY(pg.UUID(as_uuid=True)), nullable=False),
        sa.Column("status", sa.String(16), nullable=False, server_default="queued"),
        sa.Column("input_hash", sa.String(64), nullable=False),
        sa.Column("effective_as_of", sa.DateTime(timezone=True), nullable=False),
        sa.Column("input_document", pg.JSONB(), nullable=False),
        sa.Column("result_document", pg.JSONB()),
        sa.Column("failure_code", sa.String(64)),
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
        sa.UniqueConstraint(
            "tenant_id", "idempotency_key", name="uq_environment_assessment_key"
        ),
        sa.CheckConstraint(
            "status IN ('queued','running','completed','failed')",
            name="ck_environment_assessment_status",
        ),
        sa.CheckConstraint(
            "status != 'completed' OR result_document IS NOT NULL",
            name="ck_environment_assessment_result",
        ),
        sa.CheckConstraint(
            "cardinality(engagement_ids) BETWEEN 1 AND 20",
            name="ck_environment_assessment_scope_count",
        ),
    )
    op.create_index(
        "ix_environment_assessments_tenant_id", "environment_assessments", ["tenant_id"]
    )
    for statement in enable_statements("environment_assessments"):
        op.execute(statement)
    op.execute("""
      CREATE FUNCTION protect_environment_assessment() RETURNS trigger AS $$
      BEGIN
        IF (NEW.id,NEW.created_at,NEW.tenant_id,NEW.idempotency_key,NEW.request_sequence,NEW.engagement_ids,NEW.input_hash,NEW.effective_as_of,NEW.input_document)
          IS DISTINCT FROM
          (OLD.id,OLD.created_at,OLD.tenant_id,OLD.idempotency_key,OLD.request_sequence,OLD.engagement_ids,OLD.input_hash,OLD.effective_as_of,OLD.input_document)
        THEN RAISE EXCEPTION 'environment assessment inputs are immutable'; END IF;
        IF OLD.status='completed' AND NEW IS DISTINCT FROM OLD THEN
          RAISE EXCEPTION 'completed environment assessments are immutable'; END IF;
        RETURN NEW;
      END; $$ LANGUAGE plpgsql;
    """)
    op.execute(
        "CREATE TRIGGER protect_environment_assessment BEFORE UPDATE ON environment_assessments FOR EACH ROW EXECUTE FUNCTION protect_environment_assessment()"
    )


def downgrade():
    op.drop_table("environment_assessments")
    op.execute("DROP FUNCTION protect_environment_assessment()")
