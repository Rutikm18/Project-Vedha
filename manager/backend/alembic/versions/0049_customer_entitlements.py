"""Customer entitlements — POC / licensed plans with a portal scan quota

* customer_entitlements — one row per engagement: plan_type (poc | licensed),
  starts_at / expires_at, an optional overall scan_quota, per-type quotas
  (stealth / normal / aggressive / deep: NULL = unlimited, 0 = not included),
  usage ledgers changed under a row lock, the deep-scan repeat policy and the
  assets already deep-scanned, license_key.
* scan_requests.quota_consumed / quota_mode — whether (and from which
  allowance) a request took a scan, so a rejection refunds exactly once.
* Backfill: every engagement that already has a customer login gets an
  unlimited, non-expiring "licensed" row, so deploying this never locks an
  existing customer out of scanning. New customers start unconfigured.

Revision ID: 0049
Revises: 0048
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0049"
down_revision: Union[str, None] = "0048"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "customer_entitlements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("plan_type", sa.String(16), nullable=False, server_default="poc"),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scan_quota", sa.Integer(), nullable=True),
        sa.Column("scans_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("stealth_quota", sa.Integer(), nullable=True),
        sa.Column("normal_quota", sa.Integer(), nullable=True),
        sa.Column("aggressive_quota", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("deep_quota", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("stealth_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("normal_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("aggressive_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("deep_used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("deep_repeat_policy", sa.String(16), nullable=False, server_default="distinct"),
        sa.Column("deep_scanned_targets", postgresql.JSONB(), nullable=False,
                  server_default=sa.text("'[]'::jsonb")),
        sa.Column("license_key", sa.String(32), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("plan_type IN ('poc', 'licensed')", name="ck_entitlement_plan_type"),
        sa.CheckConstraint("scan_quota IS NULL OR scan_quota >= 0", name="ck_entitlement_quota"),
        sa.CheckConstraint("scans_used >= 0", name="ck_entitlement_used"),
        sa.CheckConstraint(
            "stealth_quota >= 0 AND normal_quota >= 0 AND aggressive_quota >= 0 AND deep_quota >= 0",
            name="ck_entitlement_mode_quotas"),
        sa.CheckConstraint("deep_repeat_policy IN ('distinct', 'repeat')",
                           name="ck_entitlement_deep_policy"),
        sa.UniqueConstraint("engagement_id", name="uq_customer_entitlements_engagement_id"),
        sa.UniqueConstraint("license_key", name="uq_customer_entitlements_license_key"),
    )
    op.create_index("ix_customer_entitlements_tenant_id", "customer_entitlements", ["tenant_id"])
    op.add_column("scan_requests", sa.Column("quota_consumed", sa.Boolean(), nullable=False,
                                             server_default=sa.false()))
    op.add_column("scan_requests", sa.Column("quota_mode", sa.String(12), nullable=True))
    op.execute("""
        INSERT INTO customer_entitlements (tenant_id, engagement_id, plan_type, notes)
        SELECT DISTINCT e.tenant_id, e.id, 'licensed',
               'Created by migration 0049: unlimited, no expiry (pre-existing customer)'
        FROM engagements e
        JOIN users u ON u.client_engagement_id = e.id
        -- ::text, not the enum literal: on a fresh install every migration runs
        -- in one transaction, and 'client' was added to userrole earlier in it —
        -- Postgres refuses an uncommitted enum value as a literal.
        WHERE u.role::text = 'client'
    """)


def downgrade() -> None:
    op.drop_column("scan_requests", "quota_mode")
    op.drop_column("scan_requests", "quota_consumed")
    op.drop_index("ix_customer_entitlements_tenant_id", table_name="customer_entitlements")
    op.drop_table("customer_entitlements")
