"""
agent_recommendation.py — decisions/actions proposed by the agentic AI advisor.

The advisor (app/ai/agent.py) runs a Claude tool-use loop over an engagement's
REAL data (read-only tools) and emits structured recommendations across three
use cases — finding triage, next-action orchestration, and attack-path reasoning.

RECOMMEND-ONLY: every row lands with status "pending". The agent never executes
anything itself; a human approves a recommendation, and only then does the
existing gated path (job dispatch / exploit approval) act on it. This mirrors the
llm_outputs review model and keeps a security tool's actions human-gated.
"""
from __future__ import annotations

import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


# category values
CAT_TRIAGE = "triage"            # verdict on an existing finding (validity/severity/priority)
CAT_NEXT_ACTION = "next_action"  # proposed follow-up work (routed through gates on approval)
CAT_ATTACK_PATH = "attack_path"  # attack-path narrative + remediation

# status values (ReviewStatus semantics, kept as plain strings — no new PG enum)
STATUS_PENDING = "pending"


class AgentRecommendation(Base, TimestampMixin):
    __tablename__ = "agent_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    # Groups all recommendations produced by one advisor run.
    run_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)

    category: Mapped[str] = mapped_column(String(32), nullable=False)
    # What the recommendation is about (e.g. "finding" + the finding id).
    target_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    # For next_action rows: the proposed (gated) action, from a fixed allowlist.
    action: Mapped[str | None] = mapped_column(String(64), nullable=True)

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(4, 1), nullable=True)  # 0–100
    priority: Mapped[str | None] = mapped_column(String(16), nullable=True)           # critical/high/...

    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default=STATUS_PENDING)
    evidence: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # raw structured payload
    model: Mapped[str | None] = mapped_column(String(64), nullable=True)
