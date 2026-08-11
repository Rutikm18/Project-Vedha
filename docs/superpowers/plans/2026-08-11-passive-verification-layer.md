# Passive Verification Layer (P2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every finding a normalized, dashboard-facing verification verdict (`confirmed | corroborated | inferred | contradicted`) plus an FP-triage flag and a human-readable rationale — computed deterministically, optionally explained by an LLM, and (optionally) orchestrated by a LangGraph subgraph that becomes load-bearing in P3.

**Architecture:** A PURE deterministic core (`app/detection/verification.py`) maps the detection engine's existing per-finding evidence (`state`, `source_confidence`, `confidence`, `checks`, `kev`) to a `VerificationVerdict`. An async entrypoint optionally enriches the verdict with an LLM rationale via the existing `ManagerLlmService` — the LLM can only add a rationale, lower confidence, or set `needs_review`; it can never raise certainty or invent data. An optional LangGraph skin (`app/ai/verification_graph.py`) orchestrates the same steps; when LangGraph or an LLM key is absent, everything degrades to the deterministic core (fail-closed). Verdicts persist on `findings` and surface as a dashboard badge.

**Tech Stack:** Python 3, SQLAlchemy 2 (async), Alembic, `ManagerLlmService` (existing), LangGraph (new, optional), pytest.

This plan implements **Phase 2** of `plan_after_probe.md` (§5.1, §6). P3 (active validation) and P4 (risk-rank/UI) are separate plans. It builds directly on the P1 detection/resolution work already merged onto `feat/coverage-gated-auto-resolution`.

## Global Constraints

- **Deterministic core is the source of truth.** `compute_verdict` is pure (no LLM, no DB, no network, no LangGraph) and fully unit-tested offline. The verdict STATE is set deterministically.
- **The LLM can only lower or flag.** It may write a rationale, set `needs_review=True`, or (when confidence is already low) mark `contradicted`. It may NEVER raise confidence, change `confirmed`, or invent a CVE/asset/score. Reuse `ManagerLlmService`'s grounding rules (`_BASE_RULES`).
- **Best-effort, fail-closed, optional.** Behind settings flag `verification_enabled` (default `False`). LangGraph and the LLM are optional dependencies (like `anthropic` today): absent either, the deterministic verdict stands and nothing errors. Verification failure must NEVER fail the detection run or probe submission.
- **No new PG enum types.** `verification_state` is a plain `String` (values validated in Python), matching the DetectionRun-status precedent (`detection_run.py` uses plain strings).
- **Verdict vocabulary (exact):** `confirmed`, `corroborated`, `inferred`, `contradicted`. `verification_method`: `passive` (P3 adds `active`).
- **Run from `manager/backend/`** for all pytest/alembic commands. Use `./.venv/bin/python -m pytest ...`.
- **Follow existing patterns:** pure logic → plain unit tests; async/LLM glue → mock with `MagicMock`/`AsyncMock` (see `tests/test_job_result_service.py`).

---

### Task 1: Verification-verdict schema (model + migration)

**Files:**
- Modify: `manager/backend/app/models/finding.py`
- Create: `manager/backend/alembic/versions/0021_finding_verification.py`
- Test: `manager/backend/tests/test_finding_verification_schema.py`

**Interfaces:**
- Produces: `Finding.verification_state: str | None`, `Finding.verification_confidence: int | None`, `Finding.verification_rationale: str | None`, `Finding.needs_review: bool`, `Finding.verification_method: str | None`.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_finding_verification_schema.py`:

```python
from __future__ import annotations

from app.models.finding import Finding


def test_finding_has_verification_columns():
    cols = Finding.__table__.columns
    for name in (
        "verification_state", "verification_confidence",
        "verification_rationale", "needs_review", "verification_method",
    ):
        assert name in cols, f"missing column {name}"
    assert cols["needs_review"].nullable is False
    assert cols["verification_state"].nullable is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_finding_verification_schema.py -q`
Expected: FAIL — `missing column verification_state`.

- [ ] **Step 3: Add the columns to the model**

In `manager/backend/app/models/finding.py`, insert after the resolution-lifecycle block (after the `detected_db_version` column, before the `engagement:` relationship):

```python
    # ── Verification (P2 passive; P3 adds active) ──────────────────────────────
    # verification_state: normalized dashboard verdict — confirmed | corroborated
    #   | inferred | contradicted. Distinct from `status` (lifecycle) and from the
    #   internal 0-100 confidence: it's the human-facing "how sure are we this is
    #   real". needs_review flags a high-stakes uncertain finding for an analyst.
    verification_state: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    verification_confidence: Mapped[int | None] = mapped_column(Integer, nullable=True)
    verification_rationale: Mapped[str | None] = mapped_column(Text(), nullable=True)
    needs_review: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false", index=True)
    verification_method: Mapped[str | None] = mapped_column(String(16), nullable=True)
```

(`Integer`, `Boolean`, `String`, `Text` are already imported from Task-1 of P1 / the existing model.)

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_finding_verification_schema.py -q`
Expected: PASS.

- [ ] **Step 5: Create the migration**

Confirm head: `./.venv/bin/python -m alembic heads` → expect `0020 (head)`.

Create `manager/backend/alembic/versions/0021_finding_verification.py`:

```python
"""Finding verification verdict columns (P2 passive verification).

Revision ID: 0021
Revises: 0020
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0021"
down_revision: Union[str, None] = "0020"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("findings", sa.Column("verification_state", sa.String(length=16), nullable=True))
    op.add_column("findings", sa.Column("verification_confidence", sa.Integer(), nullable=True))
    op.add_column("findings", sa.Column("verification_rationale", sa.Text(), nullable=True))
    op.add_column("findings", sa.Column("needs_review", sa.Boolean(), nullable=False, server_default="false"))
    op.add_column("findings", sa.Column("verification_method", sa.String(length=16), nullable=True))
    op.create_index("ix_findings_verification_state", "findings", ["verification_state"])
    op.create_index("ix_findings_needs_review", "findings", ["needs_review"])


def downgrade() -> None:
    op.drop_index("ix_findings_needs_review", table_name="findings")
    op.drop_index("ix_findings_verification_state", table_name="findings")
    for col in ("verification_method", "needs_review", "verification_rationale",
                "verification_confidence", "verification_state"):
        op.drop_column("findings", col)
```

- [ ] **Step 6: Validate the chain**

Run: `./.venv/bin/python -m alembic history | head -3` and `./.venv/bin/python -m alembic heads`
Expected: `0020 -> 0021 (head)` and a single head `0021`.

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/models/finding.py \
        manager/backend/alembic/versions/0021_finding_verification.py \
        manager/backend/tests/test_finding_verification_schema.py
git commit -m "feat(verification): add finding verification verdict columns + migration"
```

---

### Task 2: Deterministic verdict core (pure)

**Files:**
- Create: `manager/backend/app/detection/verification.py`
- Test: `manager/backend/tests/test_verification_core.py`

**Interfaces:**
- Produces: `VerificationVerdict(state: str, confidence: int, needs_review: bool, rationale: str, method: str = "passive")`; `VERIFICATION_STATES: frozenset[str]`; `compute_verdict(evidence: dict) -> VerificationVerdict`.
- Consumes: the detection finding dict stored in `Finding.evidence` — keys `state` (`confirmed|suspected|potential`), `source_confidence` (`authoritative|inferred`), `confidence` (`int|None`), `checks` (`dict`), `kev` (`bool|None`), `priority` (`str|None`).

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_verification_core.py`:

```python
from __future__ import annotations

from app.detection.verification import VERIFICATION_STATES, compute_verdict


def test_authoritative_is_confirmed():
    v = compute_verdict({"source_confidence": "authoritative", "state": "confirmed",
                         "confidence": 95})
    assert v.state == "confirmed"
    assert v.confidence == 95
    assert v.needs_review is False


def test_high_confidence_inferred_is_corroborated():
    v = compute_verdict({"source_confidence": "inferred", "state": "suspected",
                         "confidence": 80, "checks": {}})
    assert v.state == "corroborated"


def test_low_confidence_inferred_is_inferred():
    v = compute_verdict({"source_confidence": "inferred", "state": "potential",
                         "confidence": 35, "checks": {}})
    assert v.state == "inferred"


def test_kev_suspected_finding_needs_review():
    v = compute_verdict({"source_confidence": "inferred", "state": "suspected",
                         "confidence": 55, "kev": True, "priority": "high"})
    assert v.needs_review is True
    assert v.state in VERIFICATION_STATES


def test_missing_confidence_defaults_to_inferred_not_crash():
    v = compute_verdict({"source_confidence": "inferred", "state": "suspected"})
    assert v.state in VERIFICATION_STATES
    assert isinstance(v.confidence, int)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_verification_core.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.detection.verification'`.

- [ ] **Step 3: Write the pure core**

Create `manager/backend/app/detection/verification.py`:

```python
"""
verification.py — normalized, dashboard-facing verification verdict.

The deterministic detection engine already calibrates a 0-100 `confidence` and
an evidence tier per finding (see detection_engine/verifier.py). This module
maps that into a small, human-facing vocabulary and an FP-triage flag:

    confirmed    authoritative/credentialed truth
    corroborated strong network evidence (protocol/multi-signal, high confidence)
    inferred     weak/single-signal, uncorroborated
    contradicted evidence actively refutes (set by the LLM/active tiers, not here)

PURE: no DB, no network, no LLM, no LangGraph. compute_verdict() is the whole
substance of passive verification and is fully unit-tested offline. The optional
LLM rationale (verify_finding, Task 3) and LangGraph skin (Task 4) wrap this;
they can only lower confidence or flag review — never raise it.
"""
from __future__ import annotations

from dataclasses import dataclass

VERIFICATION_STATES = frozenset({"confirmed", "corroborated", "inferred", "contradicted"})

# Confidence at/above this (for non-authoritative findings) reads as corroborated.
_CORROBORATED_FLOOR = 70


@dataclass
class VerificationVerdict:
    state: str
    confidence: int
    needs_review: bool
    rationale: str
    method: str = "passive"


def _int_confidence(evidence: dict) -> int:
    c = evidence.get("confidence")
    if isinstance(c, (int, float)):
        return max(0, min(100, int(c)))
    # No calibrated confidence recorded → treat as weak evidence.
    return 40


def compute_verdict(evidence: dict) -> VerificationVerdict:
    """Deterministic passive verdict from a detection finding's evidence dict."""
    source = evidence.get("source_confidence")
    state = evidence.get("state")
    conf = _int_confidence(evidence)

    if source == "authoritative" or state == "confirmed":
        vstate, reason = "confirmed", "authoritative/credentialed evidence"
    elif conf >= _CORROBORATED_FLOOR:
        vstate, reason = "corroborated", f"network evidence, confidence {conf}"
    else:
        vstate, reason = "inferred", f"weak/single-signal evidence, confidence {conf}"

    # High-stakes uncertainty → surface for analyst review.
    kev = bool(evidence.get("kev"))
    priority = (evidence.get("priority") or "").lower()
    uncertain = state in ("suspected", "potential") and vstate != "confirmed"
    needs_review = uncertain and (kev or priority in ("critical", "high"))
    if needs_review:
        reason += "; flagged for review (high-stakes + uncertain)"

    return VerificationVerdict(state=vstate, confidence=conf,
                               needs_review=needs_review, rationale=reason)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_verification_core.py -q`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/verification.py manager/backend/tests/test_verification_core.py
git commit -m "feat(verification): deterministic passive verdict core"
```

---

### Task 3: Optional LLM rationale entrypoint (fail-closed)

**Files:**
- Modify: `manager/backend/app/detection/verification.py`
- Test: `manager/backend/tests/test_verification_llm.py`

**Interfaces:**
- Consumes: `compute_verdict` (Task 2); `ManagerLlmService` (duck-typed — any object with `async generate(request) -> (text, runtime)`); `AiGenerateRequest`/message schema is NOT required (we pass a minimal object), so the LLM arg is duck-typed for testability.
- Produces: `async def verify_finding(evidence: dict, llm=None, *, min_review_priority=("critical", "high")) -> VerificationVerdict`. With `llm=None` → identical to `compute_verdict`. With an `llm` and a qualifying finding → attaches an LLM rationale and may set `needs_review`/lower to `contradicted`. Any LLM error → deterministic verdict stands.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_verification_llm.py`:

```python
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.detection.verification import verify_finding


@pytest.mark.asyncio
async def test_no_llm_matches_deterministic():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 80}
    v = await verify_finding(ev, llm=None)
    assert v.state == "corroborated"
    assert v.rationale  # deterministic reason present


@pytest.mark.asyncio
async def test_llm_error_falls_back_to_deterministic():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 55,
          "kev": True, "priority": "high"}
    llm = AsyncMock()
    llm.verify_rationale = AsyncMock(side_effect=RuntimeError("provider down"))
    v = await verify_finding(ev, llm=llm)
    assert v.state in ("corroborated", "inferred")  # deterministic stands
    assert v.needs_review is True                    # from deterministic rule


@pytest.mark.asyncio
async def test_llm_can_flag_false_positive_and_lower():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 35,
          "kev": True, "priority": "high"}
    llm = AsyncMock()
    llm.verify_rationale = AsyncMock(return_value={
        "rationale": "Version string matches but the service banner suggests a backported build.",
        "suspected_false_positive": True,
    })
    v = await verify_finding(ev, llm=llm)
    assert v.needs_review is True
    assert v.state == "contradicted"          # low conf + FP flag → contradicted
    assert "backported" in v.rationale
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_verification_llm.py -q`
Expected: FAIL — `ImportError: cannot import name 'verify_finding'`.

- [ ] **Step 3: Add `verify_finding` to `verification.py`**

Append to `manager/backend/app/detection/verification.py`:

```python
import structlog  # noqa: E402  (grouped with the LLM entrypoint below)

logger = structlog.get_logger()

# Only spend an LLM call on findings where a human-readable rationale / FP-triage
# is worth it: uncertain AND high-stakes. Everything else keeps the cheap verdict.
def _qualifies_for_llm(verdict: VerificationVerdict, evidence: dict) -> bool:
    priority = (evidence.get("priority") or "").lower()
    return verdict.needs_review or priority in ("critical", "high")


async def verify_finding(evidence: dict, llm=None) -> VerificationVerdict:
    """Deterministic verdict, optionally enriched by an LLM rationale. The LLM
    (duck-typed: must expose `async verify_rationale(evidence) -> dict`) can only
    add a rationale, flag needs_review, and — when confidence is already low —
    mark the verdict contradicted. It can NEVER raise confidence or override a
    confirmed verdict. Any LLM failure yields the pure deterministic verdict."""
    verdict = compute_verdict(evidence)
    if llm is None or verdict.state == "confirmed" or not _qualifies_for_llm(verdict, evidence):
        return verdict
    try:
        out = await llm.verify_rationale(evidence)
    except Exception as exc:  # noqa: BLE001 — LLM must never break verification
        logger.warning("verification.llm_failed", error=str(exc))
        return verdict
    if not isinstance(out, dict):
        return verdict
    rationale = str(out.get("rationale") or "").strip()
    fp = bool(out.get("suspected_false_positive"))
    new_reason = rationale or verdict.rationale
    needs_review = verdict.needs_review or fp
    # LLM may only DOWNGRADE: an FP flag on an already-weak finding → contradicted.
    new_state = verdict.state
    if fp and verdict.confidence < _CORROBORATED_FLOOR:
        new_state = "contradicted"
    return VerificationVerdict(state=new_state, confidence=verdict.confidence,
                               needs_review=needs_review, rationale=new_reason,
                               method="passive")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_verification_llm.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/verification.py manager/backend/tests/test_verification_llm.py
git commit -m "feat(verification): optional fail-closed LLM rationale + FP-triage"
```

---

### Task 4: LangGraph orchestration skin (optional dependency)

**Files:**
- Create: `manager/backend/app/ai/verification_graph.py`
- Modify: `manager/backend/requirements-extras.txt`
- Test: `manager/backend/tests/test_verification_graph.py`

**Interfaces:**
- Consumes: `verify_finding`, `VerificationVerdict` (Tasks 2–3).
- Produces: `graph_available() -> bool`; `async def run_verification(evidence: dict, llm=None) -> VerificationVerdict` — uses the LangGraph StateGraph when `langgraph` is importable, else calls `verify_finding` directly. Identical result either way (the graph is orchestration, not logic).

**Note:** For P2 the graph is a linear `intake → corroborate → finalize`; its real value (checkpoint/pause/interrupt) arrives in P3's active-validation node. Introducing the skin now keeps the wiring stable across P2→P3.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_verification_graph.py`:

```python
from __future__ import annotations

import pytest

from app.ai.verification_graph import graph_available, run_verification


@pytest.mark.asyncio
async def test_run_verification_matches_core_without_llm():
    ev = {"source_confidence": "inferred", "state": "suspected", "confidence": 80}
    v = await run_verification(ev, llm=None)
    assert v.state == "corroborated"


def test_graph_available_is_boolean():
    assert isinstance(graph_available(), bool)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_verification_graph.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.ai.verification_graph'`.

- [ ] **Step 3: Write the optional skin**

Create `manager/backend/app/ai/verification_graph.py`:

```python
"""
verification_graph.py — optional LangGraph orchestration for passive verification.

The substance lives in app/detection/verification.py (pure core + optional LLM
rationale). This module wraps it in a LangGraph StateGraph so the SAME wiring
carries forward to P3, where active validation adds a checkpointed, human-in-the-
loop node. LangGraph is an OPTIONAL dependency: if it's not installed,
run_verification() calls the core directly and results are identical.
"""
from __future__ import annotations

from app.detection.verification import VerificationVerdict, verify_finding

try:
    from langgraph.graph import END, START, StateGraph  # type: ignore

    _HAS_LANGGRAPH = True
except ImportError:  # pragma: no cover - exercised only where langgraph is absent
    StateGraph = None  # type: ignore
    START = END = None  # type: ignore
    _HAS_LANGGRAPH = False


def graph_available() -> bool:
    return _HAS_LANGGRAPH


async def run_verification(evidence: dict, llm=None) -> VerificationVerdict:
    """Run passive verification. Uses the LangGraph StateGraph when available;
    otherwise the deterministic/LLM core directly (identical result)."""
    if not _HAS_LANGGRAPH:
        return await verify_finding(evidence, llm=llm)

    async def _corroborate(state: dict) -> dict:
        verdict = await verify_finding(state["evidence"], llm=state.get("llm"))
        return {"verdict": verdict}

    graph = StateGraph(dict)
    graph.add_node("corroborate", _corroborate)
    graph.add_edge(START, "corroborate")
    graph.add_edge("corroborate", END)
    compiled = graph.compile()
    result = await compiled.ainvoke({"evidence": evidence, "llm": llm})
    return result["verdict"]
```

- [ ] **Step 4: Add the optional dependency**

Append to `manager/backend/requirements-extras.txt` (the optional/heavy-integrations file referenced by `requirements.txt`):

```
# P2 verification orchestration (optional; falls back to the deterministic core)
langgraph==0.2.60
```

- [ ] **Step 5: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_verification_graph.py -q`
Expected: PASS (2 tests) — with `langgraph` absent, `run_verification` uses the core and `graph_available()` returns `False`. (If `langgraph` is installed, the graph path runs; result is identical.)

- [ ] **Step 6: Commit**

```bash
git add manager/backend/app/ai/verification_graph.py \
        manager/backend/requirements-extras.txt \
        manager/backend/tests/test_verification_graph.py
git commit -m "feat(verification): optional LangGraph orchestration skin"
```

---

### Task 5: Wire verification into the detection run

**Files:**
- Modify: `manager/backend/app/config.py` (add `verification_enabled` setting)
- Modify: `manager/backend/app/detection/engine_bridge.py`
- Test: `manager/backend/tests/test_engine_bridge_verification.py`

**Interfaces:**
- Consumes: `run_verification` (Task 4), `settings.verification_enabled`.
- Produces: after a detection run, each newly-created/reaffirmed Finding has `verification_state`, `verification_confidence`, `verification_rationale`, `needs_review`, `verification_method` set (when `verification_enabled`); otherwise untouched.

- [ ] **Step 1: Add the setting**

In `manager/backend/app/config.py`, add to the `Settings` class (near other feature flags — search for an existing `bool` setting to match style):

```python
    verification_enabled: bool = False
```

- [ ] **Step 2: Write the failing test**

Create `manager/backend/tests/test_engine_bridge_verification.py`:

```python
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.detection import engine_bridge
from app.detection.verification import VerificationVerdict


@pytest.mark.asyncio
async def test_stamp_verification_sets_columns_when_enabled():
    f = SimpleNamespace(evidence={"source_confidence": "inferred", "state": "suspected",
                                  "confidence": 80},
                        verification_state=None, verification_confidence=None,
                        verification_rationale=None, needs_review=False,
                        verification_method=None)

    with patch.object(engine_bridge, "run_verification",
                      new=AsyncMock(return_value=VerificationVerdict(
                          state="corroborated", confidence=80, needs_review=False,
                          rationale="ok"))):
        await engine_bridge._stamp_verification([f], llm=None)

    assert f.verification_state == "corroborated"
    assert f.verification_confidence == 80
    assert f.verification_method == "passive"
```

- [ ] **Step 3: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_engine_bridge_verification.py -q`
Expected: FAIL — `AttributeError: module 'app.detection.engine_bridge' has no attribute '_stamp_verification'`.

- [ ] **Step 4: Implement the stamp helper and call it**

In `manager/backend/app/detection/engine_bridge.py`, add the import near the resolution import:

```python
from app.ai.verification_graph import run_verification
```

Add the helper (module level, above `create_findings_from_facts`):

```python
async def _stamp_verification(findings, llm=None) -> None:
    """Best-effort: compute + stamp each finding's verification verdict. A failure
    on one finding must not sink the batch or the detection run."""
    for f in findings:
        try:
            verdict = await run_verification(f.evidence or {}, llm=llm)
            f.verification_state = verdict.state
            f.verification_confidence = verdict.confidence
            f.verification_rationale = verdict.rationale
            f.needs_review = verdict.needs_review
            f.verification_method = verdict.method
        except Exception as exc:  # noqa: BLE001 — verification must never break the run
            logger.warning("verification.stamp_failed", error=str(exc))
```

Then, inside `create_findings_from_facts`, collect the findings touched this run and stamp them after resolution. Track new/reaffirmed findings in a list as they're created. Add near the top of the try block:

```python
        touched: list = []
```

In the reaffirm branch, after `dup.resolution_miss_count = 0`, add `touched.append(dup)`. In the regression branch, after `_apply_regression_reopen(...)`, add `touched.append(regressed)`. When creating a new Finding, capture it: change `db.add(Finding(...))` to

```python
                    new_finding = Finding(
                        ...  # unchanged kwargs
                    )
                    db.add(new_finding)
                    touched.append(new_finding)
```

After the coverage/resolution block and before the `current` snapshot, add:

```python
        from app.config import get_settings
        if get_settings().verification_enabled:
            await _stamp_verification(touched)
            await db.flush()
```

- [ ] **Step 5: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_engine_bridge_verification.py -q`
Expected: PASS.

- [ ] **Step 6: Run the detection suite for regressions**

Run: `./.venv/bin/python -m pytest tests/test_detection_validation.py tests/test_engine_bridge_resolution.py tests/test_engine_bridge_regression.py tests/test_posture.py -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/config.py manager/backend/app/detection/engine_bridge.py \
        manager/backend/tests/test_engine_bridge_verification.py
git commit -m "feat(verification): stamp verdicts on detection-run findings (flagged)"
```

---

### Task 6: Surface verification on the findings API

**Files:**
- Modify: the findings response schema + router (locate via `grep -rn "verification\|class Finding.*Response\|risk_score" manager/backend/app/schemas manager/backend/app/routers`)
- Test: `manager/backend/tests/test_finding_verification_api.py`

**Interfaces:**
- Produces: findings API responses include `verification_state`, `needs_review` (and, where full detail is returned, `verification_rationale`, `verification_confidence`).

- [ ] **Step 1: Locate the schema**

Run: `grep -rn "risk_score\|severity" manager/backend/app/schemas/*.py | grep -i finding`
Identify the Pydantic response model for a finding (e.g. `FindingRead`/`FindingResponse`).

- [ ] **Step 2: Write the failing test**

Create `manager/backend/tests/test_finding_verification_api.py` (adjust the import to the schema found in Step 1):

```python
from __future__ import annotations

from app.schemas.finding import FindingRead  # adjust to the real module/class


def test_finding_schema_exposes_verification_fields():
    fields = FindingRead.model_fields
    assert "verification_state" in fields
    assert "needs_review" in fields
```

- [ ] **Step 3: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_finding_verification_api.py -q`
Expected: FAIL — `KeyError`/`AssertionError` (fields absent).

- [ ] **Step 4: Add the fields to the response model**

In the finding response model found in Step 1, add:

```python
    verification_state: str | None = None
    verification_confidence: int | None = None
    verification_rationale: str | None = None
    needs_review: bool = False
```

(If the model uses `from_attributes = True`/ORM mode, no mapping code is needed — the new ORM columns flow through automatically.)

- [ ] **Step 5: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_finding_verification_api.py -q`
Expected: PASS.

- [ ] **Step 6: Full suite check + commit**

Run: `./.venv/bin/python -m pytest -q -m "not integration"`
Expected: PASS (no regressions).

```bash
git add manager/backend/app/schemas manager/backend/app/routers \
        manager/backend/tests/test_finding_verification_api.py
git commit -m "feat(verification): expose verification verdict + needs_review on findings API"
```

---

## Self-Review

**1. Spec coverage (against `plan_after_probe.md §5.1, §6`):**
- Passive verdict `{confirmed, corroborated, inferred, contradicted}` → Task 2. ✅
- LLM only lowers/flags/explains, never fabricates/raises → Task 3 (`verify_finding` invariants) + Global Constraints. ✅
- LangGraph subgraph, optional/fail-closed, forward-compatible with P3 → Task 4. ✅
- Persist + surface verification (badge, needs_review) → Tasks 1, 5, 6. ✅
- Behind a flag, best-effort, never breaks the run → Task 5 + Global Constraints. ✅
- Deterministic core is source of truth; LLM boxed → Tasks 2–3. ✅
- Active validation (Tier A) → **out of scope, P3** (documented). Confidence-raising only via active positive control → enforced here by never letting passive raise. ✅

**2. Placeholder scan:** Task 6 intentionally has a `grep`-locate step because the exact finding response schema name isn't known without inspection; the test/edit show concrete code once located. All other steps have complete code. No TBD/TODO.

**3. Type consistency:** `VerificationVerdict(state, confidence, needs_review, rationale, method)` identical across Tasks 2–5. `compute_verdict`/`verify_finding`/`run_verification` signatures consistent. Column names (`verification_state`, `verification_confidence`, `verification_rationale`, `needs_review`, `verification_method`) match across model (Task 1), stamp (Task 5), and API (Task 6). ✅

---

## Execution Handoff

Executing inline in this session (continuing the `feat/coverage-gated-auto-resolution` branch), TDD task-by-task, per the user's "do all plans one by one" directive.
