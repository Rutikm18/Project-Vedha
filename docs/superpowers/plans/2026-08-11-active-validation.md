# Approval-Gated Safe Active Validation (P3) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** For high-severity/KEV findings that are still only *inferred/corroborated* (not authoritatively confirmed), let an operator run a **safe, non-destructive** live re-check via the probe, gated by an approval, whose result either **confirms** the finding (→ `verification_state=confirmed`, `exploit_validated=True`) or **contradicts** it (→ `contradicted`, a strong false-positive signal).

**Architecture:** A PURE manager-side core (`app/detection/active_validation.py`) decides *when* a finding qualifies to escalate and *how* to interpret a returned validation result. A `ValidationRequest` row is the approval-gated record (mirrors `ExploitApprovalRequest`); on approval a `vuln_scan` job with `params.mode="validate"` is enqueued to the probe, scoped to exactly one `asset+port+check`. The probe runs a safe validator and returns a result; the manager interprets it and updates the finding's verdict. This slots into P2's LangGraph graph as the `active_validation` node (checkpoint/pause until the result returns).

**Tech Stack:** Python 3, SQLAlchemy 2 (async), Alembic, existing ScanJob dispatch, pytest.

Implements **Phase 3** of `plan_after_probe.md` (§5.2). Builds on P1/P2 (branch `feat/coverage-gated-auto-resolution`).

## Global Constraints

- **Non-destructive only.** Validation checks are read-only: TLS/protocol handshake, banner re-grab, a pinned safe PoC with an allowlist that EXCLUDES any `destructive|dos|intrusive|write` template. No exploitation, brute force, writes, or DoS. Enforced probe-side by ScopeGuard + an allowlist, and manager-side by only ever emitting the safe check kinds.
- **Approval-gated + RoE-bounded.** No validation job is enqueued without an approved `ValidationRequest`. Escalation only fires when the engagement RoE allows (`active_validation_allowed`) and the profile is not `ot` (structurally passive).
- **Confirmation is the ONLY path to raise certainty.** A network-observed finding may become `verification_state=confirmed` only via a positive active result — never by passive/LLM means (carried from P2).
- **Inconclusive never downgrades to resolved.** A timed-out/unreachable validation keeps the finding as-is.
- **No new PG enum types.** Job routing uses `params.mode="validate"` on `vuln_scan`; `ValidationRequest.status`/`outcome` are plain strings.
- **Best-effort, reversible.** Escalation/interpretation failures never break detection or probe submission.

## Environment note (what this plan can verify vs. not)

- **Verifiable in the manager backend sandbox (Tasks 1–3):** pure escalation decision, pure result interpretation, the `ValidationRequest` model + migration + schema. These are unit-tested here.
- **Requires your infra (Tasks 4–7, spec-complete but NOT executed in-sandbox):** the probe-side safe validator (needs a probe + a target host), the approve→enqueue endpoint round-trip (needs the dispatch stack + a live probe), and the LangGraph `active_validation` node (needs `langgraph` installed). Each is fully specified; run them against a real probe/target and an LLM/langgraph install.

---

### Task 1: Pure escalation decision

**Files:**
- Create: `manager/backend/app/detection/active_validation.py`
- Test: `manager/backend/tests/test_active_validation_escalation.py`

**Interfaces:**
- Produces: `should_escalate(evidence: dict, *, roe_allows: bool, profile: str | None) -> bool`. `evidence` is the detection finding dict (keys `state`, `source_confidence`, `priority`, `kev`).

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_active_validation_escalation.py`:

```python
from __future__ import annotations

from app.detection.active_validation import should_escalate


def _ev(**kw):
    base = {"state": "suspected", "source_confidence": "inferred",
            "priority": "high", "kev": False}
    base.update(kw)
    return base


def test_high_severity_suspected_escalates_when_roe_allows():
    assert should_escalate(_ev(), roe_allows=True, profile="it") is True


def test_kev_escalates_even_if_medium():
    assert should_escalate(_ev(priority="medium", kev=True), roe_allows=True, profile="it") is True


def test_confirmed_authoritative_does_not_escalate():
    assert should_escalate(_ev(state="confirmed", source_confidence="authoritative"),
                           roe_allows=True, profile="it") is False


def test_roe_forbids_blocks_escalation():
    assert should_escalate(_ev(), roe_allows=False, profile="it") is False


def test_ot_profile_never_escalates():
    assert should_escalate(_ev(), roe_allows=True, profile="ot") is False


def test_low_severity_non_kev_does_not_escalate():
    assert should_escalate(_ev(priority="low", kev=False), roe_allows=True, profile="it") is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_active_validation_escalation.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.detection.active_validation'`.

- [ ] **Step 3: Write the escalation core**

Create `manager/backend/app/detection/active_validation.py`:

```python
"""
active_validation.py — manager-side decision core for safe active validation.

PURE: no DB, no network, no probe. should_escalate() decides whether a finding
warrants a live re-check; interpret_validation() maps a probe's safe-check result
back to a verdict transition. The approval gate, job dispatch, and probe-side
validator are wired around this core (see the P3 plan) — this module holds the
logic so it is unit-testable offline.
"""
from __future__ import annotations

from dataclasses import dataclass

_HIGH_STAKES = ("critical", "high")


def should_escalate(evidence: dict, *, roe_allows: bool, profile: str | None) -> bool:
    """True iff this finding warrants an approval-gated active re-check.
    Escalate only uncertain + high-stakes findings, and only when RoE allows and
    the profile isn't OT (structurally passive)."""
    if not roe_allows:
        return False
    if (profile or "").lower() == "ot":
        return False
    state = evidence.get("state")
    source = evidence.get("source_confidence")
    if state == "confirmed" or source == "authoritative":
        return False  # already authoritative — nothing to validate
    high_stakes = (evidence.get("priority") or "").lower() in _HIGH_STAKES or bool(evidence.get("kev"))
    return high_stakes
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_active_validation_escalation.py -q`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/active_validation.py \
        manager/backend/tests/test_active_validation_escalation.py
git commit -m "feat(active-validation): pure escalation decision core"
```

---

### Task 2: Pure result interpretation

**Files:**
- Modify: `manager/backend/app/detection/active_validation.py`
- Test: `manager/backend/tests/test_active_validation_interpret.py`

**Interfaces:**
- Produces: `ValidationOutcome(outcome: str, verification_state: str | None, exploit_validated: bool)`; `interpret_validation(result: dict) -> ValidationOutcome`. `result` is the probe's safe-check payload: `{"outcome": "confirmed"|"contradicted"|"inconclusive", ...}` (also accepts booleans `confirmed`/`contradicted`).

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_active_validation_interpret.py`:

```python
from __future__ import annotations

from app.detection.active_validation import interpret_validation


def test_confirmed_upgrades_and_sets_exploit_validated():
    out = interpret_validation({"outcome": "confirmed"})
    assert out.outcome == "confirmed"
    assert out.verification_state == "confirmed"
    assert out.exploit_validated is True


def test_contradicted_marks_false_positive():
    out = interpret_validation({"outcome": "contradicted"})
    assert out.outcome == "contradicted"
    assert out.verification_state == "contradicted"
    assert out.exploit_validated is False


def test_inconclusive_keeps_state_unchanged():
    out = interpret_validation({"outcome": "inconclusive"})
    assert out.outcome == "inconclusive"
    assert out.verification_state is None   # no change
    assert out.exploit_validated is False


def test_missing_or_garbage_result_is_inconclusive():
    assert interpret_validation({}).outcome == "inconclusive"
    assert interpret_validation({"outcome": "weird"}).outcome == "inconclusive"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_active_validation_interpret.py -q`
Expected: FAIL — `ImportError: cannot import name 'interpret_validation'`.

- [ ] **Step 3: Add interpretation to the module**

Append to `manager/backend/app/detection/active_validation.py`:

```python
@dataclass
class ValidationOutcome:
    outcome: str                     # confirmed | contradicted | inconclusive
    verification_state: str | None   # new verification_state, or None to leave unchanged
    exploit_validated: bool


def interpret_validation(result: dict) -> ValidationOutcome:
    """Map a probe safe-check result to a verdict transition. Anything that isn't
    an explicit confirm/contradict is inconclusive — which NEVER downgrades a
    finding to resolved and NEVER lowers below its current state."""
    outcome = (result or {}).get("outcome")
    if outcome not in ("confirmed", "contradicted", "inconclusive"):
        if result.get("confirmed") is True:
            outcome = "confirmed"
        elif result.get("contradicted") is True:
            outcome = "contradicted"
        else:
            outcome = "inconclusive"
    if outcome == "confirmed":
        return ValidationOutcome("confirmed", "confirmed", True)
    if outcome == "contradicted":
        return ValidationOutcome("contradicted", "contradicted", False)
    return ValidationOutcome("inconclusive", None, False)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_active_validation_interpret.py -q`
Expected: PASS (4 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/active_validation.py \
        manager/backend/tests/test_active_validation_interpret.py
git commit -m "feat(active-validation): pure result interpretation"
```

---

### Task 3: ValidationRequest model + migration + schema

**Files:**
- Create: `manager/backend/app/models/validation_request.py`
- Modify: `manager/backend/app/models/__init__.py` (register the model)
- Create: `manager/backend/alembic/versions/0022_validation_requests.py`
- Test: `manager/backend/tests/test_validation_request_schema.py`

**Interfaces:**
- Produces: `ValidationRequest` ORM model (`validation_requests` table) with `status`/`outcome` plain strings; string constants `VR_PENDING/APPROVED/REJECTED/EXPIRED`, `CHECK_TLS/BANNER/SAFE_POC`.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_validation_request_schema.py`:

```python
from __future__ import annotations

from app.models.validation_request import (
    ValidationRequest, VR_PENDING, CHECK_TLS,
)


def test_validation_request_columns_and_defaults():
    cols = ValidationRequest.__table__.columns
    for name in ("engagement_id", "finding_id", "target_ip", "target_port",
                 "check_kind", "status", "outcome", "job_id", "result",
                 "requested_by", "requested_at"):
        assert name in cols, f"missing column {name}"
    assert VR_PENDING == "pending"
    assert CHECK_TLS == "tls_handshake"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_validation_request_schema.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.models.validation_request'`.

- [ ] **Step 3: Create the model**

Create `manager/backend/app/models/validation_request.py`:

```python
"""
validation_request.py — an approval-gated request to safely re-check a finding
live on the probe. Mirrors ExploitApprovalRequest, but for NON-destructive
validation only (no module_path/payload_path). status/outcome are plain strings
(no PG enum) per the DetectionRun precedent.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

VR_PENDING = "pending"
VR_APPROVED = "approved"
VR_REJECTED = "rejected"
VR_EXPIRED = "expired"

CHECK_TLS = "tls_handshake"
CHECK_BANNER = "banner_regrab"
CHECK_SAFE_POC = "safe_poc"


class ValidationRequest(Base, TimestampMixin):
    __tablename__ = "validation_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    finding_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("findings.id", ondelete="SET NULL"), nullable=True, index=True,
    )
    target_ip: Mapped[str] = mapped_column(String(45), nullable=False)
    target_port: Mapped[int | None] = mapped_column(Integer, nullable=True)
    check_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default=VR_PENDING, index=True)
    outcome: Mapped[str | None] = mapped_column(String(16), nullable=True)
    job_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    requested_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
```

- [ ] **Step 4: Register the model**

In `manager/backend/app/models/__init__.py`, add an import so metadata/Alembic sees it (match the existing import style there):

```python
from app.models.validation_request import ValidationRequest  # noqa: F401
```

- [ ] **Step 5: Create the migration**

Confirm head: `./.venv/bin/python -m alembic heads` → `0021 (head)`.

Create `manager/backend/alembic/versions/0022_validation_requests.py`:

```python
"""Approval-gated safe active-validation requests (P3).

Revision ID: 0022
Revises: 0021
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: str = "0022"
down_revision: Union[str, None] = "0021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "validation_requests",
        sa.Column("id", UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("engagement_id", UUID(as_uuid=True), sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("finding_id", UUID(as_uuid=True), sa.ForeignKey("findings.id", ondelete="SET NULL"), nullable=True),
        sa.Column("target_ip", sa.String(length=45), nullable=False),
        sa.Column("target_port", sa.Integer(), nullable=True),
        sa.Column("check_kind", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=16), server_default="pending", nullable=False),
        sa.Column("outcome", sa.String(length=16), nullable=True),
        sa.Column("job_id", UUID(as_uuid=True), nullable=True),
        sa.Column("result", JSONB(), nullable=True),
        sa.Column("requested_by", sa.String(length=255), nullable=True),
        sa.Column("requested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("reviewed_by", sa.String(length=255), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_validation_requests_engagement_id", "validation_requests", ["engagement_id"])
    op.create_index("ix_validation_requests_finding_id", "validation_requests", ["finding_id"])
    op.create_index("ix_validation_requests_status", "validation_requests", ["status"])


def downgrade() -> None:
    op.drop_index("ix_validation_requests_status", table_name="validation_requests")
    op.drop_index("ix_validation_requests_finding_id", table_name="validation_requests")
    op.drop_index("ix_validation_requests_engagement_id", table_name="validation_requests")
    op.drop_table("validation_requests")
```

(Confirm the `created_at`/`updated_at` columns match `TimestampMixin`'s definition in `app/models/base.py`; adjust server defaults if the mixin differs.)

- [ ] **Step 6: Verify + validate chain**

Run: `./.venv/bin/python -m pytest tests/test_validation_request_schema.py -q` → PASS.
Run: `./.venv/bin/python -m alembic heads` → single head `0022`.

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/models/validation_request.py \
        manager/backend/app/models/__init__.py \
        manager/backend/alembic/versions/0022_validation_requests.py \
        manager/backend/tests/test_validation_request_schema.py
git commit -m "feat(active-validation): ValidationRequest model + migration"
```

---

### Task 4 (SPEC — requires infra): approve → enqueue endpoint

**Files:** `manager/backend/app/routers/validation.py` (new), registered in the app router.

**Design:**
- `POST /engagements/{id}/findings/{finding_id}/validate` → creates a `ValidationRequest` (status `pending`) with the finding's `target_ip`, `target_port`, and a `check_kind` chosen from the finding's evidence (default `CHECK_TLS` for TLS findings, else `CHECK_BANNER`; `CHECK_SAFE_POC` only when a pinned safe template exists). If the engagement RoE has a pre-authorized window, status may start `approved`.
- `GET /engagements/{id}/validation-requests?status=pending` → list.
- `POST /validation-requests/{id}/approve` → set `status=approved`, `reviewed_by/at`, then enqueue a `ScanJob(job_type=vuln_scan, params={"mode":"validate","finding_id":..., "target":ip, "port":port, "check_kind":..., "scope_cidrs":[...], "allowlist":"safe"})` scoped to the single target; store `job.id` on the request. Reuse the scope-enforcement in `routers/agents.py`/`job_result_service.validate_result_scope`.
- `POST /validation-requests/{id}/reject` → `status=rejected`.

**Why not executed here:** enqueuing a job that drives a live probe against a client host requires the dispatch stack + a real probe; verifying it in the sandbox would be a fake. The pure logic it depends on (Tasks 1–2) is tested.

**Test (when infra available):** mocked-session unit tests for the create/approve handlers (assert a `ValidationRequest` is added and, on approve, a `ScanJob` with `params.mode=="validate"` is enqueued) following `tests/test_job_result_service.py` mocking style; then a live round-trip against a lab target.

---

### Task 5 (SPEC — requires infra): probe-side safe validator

**Files:** `probe/workflow/` + `probe/agent/task_runner.py` (dispatch `params.mode=="validate"` to a bounded validator).

**Design:** a new bounded validator that, for a single `target+port+check_kind`, runs ONLY:
- `tls_handshake`: a TLS handshake + exact version/cipher read (no exploit).
- `banner_regrab`: reconnect + re-read the service banner.
- `safe_poc`: a pinned Nuclei template for the finding's CVE, run with an allowlist that rejects any template tagged `destructive|dos|intrusive|network-write`. Enforce ScopeGuard before any packet. Emit `{"outcome": "confirmed"|"contradicted"|"inconclusive", "evidence": {...}}`.

**Why not executed here:** needs a probe runtime + a target host. **Invariant to preserve:** OT profile must reject validation jobs structurally (as it does other active work today).

---

### Task 6 (SPEC — requires langgraph): active_validation graph node

**Files:** `manager/backend/app/ai/verification_graph.py`.

**Design:** extend the P2 StateGraph with a conditional edge after `corroborate`: when `should_escalate(...)` (Task 1) is true, route to an `active_validation` node that creates a pending `ValidationRequest` and **checkpoints/pauses** (LangGraph interrupt) until the probe result arrives; then an `interpret` node applies `interpret_validation(...)` (Task 2) and finalizes. Requires a LangGraph checkpointer (e.g. `AsyncPostgresSaver`) — hence a real `langgraph` install.

---

### Task 7 (SPEC — requires infra): result ingestion → verdict update

**Design:** when a `validate` job result arrives (via the existing `submit_job_result` path in `routers/agents.py`), route `params.mode=="validate"` to a handler that loads the `ValidationRequest` by `job_id`, stores `result`, sets `outcome = interpret_validation(result).outcome`, and applies the transition to the finding: `confirmed` → `verification_state="confirmed"`, `status=FindingStatus.confirmed`, `exploit_validated=True`; `contradicted` → `verification_state="contradicted"`; `inconclusive` → unchanged. Best-effort; scope-checked.

**Test (when infra available):** mocked-session unit test asserting the finding transition for each outcome, plus a live round-trip.

---

## Self-Review

**1. Spec coverage (against `plan_after_probe.md §5.2`):**
- Escalation trigger (high-sev/KEV + uncertain + RoE + not OT) → Task 1. ✅
- Safe non-destructive checks only → Task 5 (spec) + Global Constraints. ✅
- Approval gate → Task 3 (model) + Task 4 (endpoints, spec). ✅
- Confirm → `confirmed`/`exploit_validated`; contradict → `contradicted`; inconclusive → unchanged → Task 2 + Task 7 (spec). ✅
- LangGraph checkpoint/pause active node → Task 6 (spec). ✅
- Confirmation is the only path to raise certainty → enforced by Task 2 semantics + P2 invariants. ✅

**2. Placeholder scan:** Tasks 1–3 have complete code. Tasks 4–7 are explicitly SPEC tasks (design + when-infra tests), clearly labeled — not hidden placeholders.

**3. Type consistency:** `should_escalate(evidence, *, roe_allows, profile)` and `interpret_validation(result) -> ValidationOutcome(outcome, verification_state, exploit_validated)` are consistent between Tasks 1–2 and their consumers in Tasks 4/6/7. `ValidationRequest` field names match across model (Task 3) and endpoint/ingestion specs. Verdict strings (`confirmed`/`contradicted`/`inconclusive`) and `verification_state` values match P2. ✅

---

## Execution Handoff

Executing Tasks 1–3 inline (pure logic + model — verifiable here). Tasks 4–7 are spec-complete and flagged for your probe/langgraph environment.
