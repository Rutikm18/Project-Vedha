# Unified Risk-Rank + Lifecycle UI (P4) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give operators a single, explainable **risk rank** that floats verified + exploitable + exposed findings on critical assets to the top (and sinks contradicted/low-confidence ones), plus a **manual reopen** for auto-resolved findings and the dashboard surfacing of the P1–P3 lifecycle/verification state.

**Architecture:** A PURE `compute_risk_rank(...)` (0–1000) blends severity/CVSS, exploit likelihood (EPSS/KEV), verification state, confidence, asset criticality, and exposure. A PURE `apply_manual_reopen(...)` mirrors the P1 regression-reopen for a human action. Both are unit-tested here; risk rank is exposed on the findings API. The Next.js badge/timeline/reopen-button UI is specified (needs `npm`/browser to verify).

**Tech Stack:** Python 3, SQLAlchemy 2 (async), pytest (backend); Next.js/React (frontend, spec).

Implements **Phase 4** of `plan_after_probe.md` (§4.6, §7). Builds on P1–P3 (branch `feat/coverage-gated-auto-resolution`).

## Global Constraints

- **Explainable.** `compute_risk_rank` is pure and deterministic; every factor is a named multiplier a reviewer can reconstruct (consistent with the verifier's `checks{}` philosophy).
- **Bounded 0–1000** to match the existing `Finding.risk_score` scale (migration `0015`).
- **Contradicted/low-confidence sink; confirmed/exploitable/exposed float.** Verification state and confidence are first-class de-rankers.
- **Manual actions are audited and reversible.** `apply_manual_reopen` records who/when and preserves history (`reopened_count`).
- **Run from `manager/backend/`.** Use `./.venv/bin/python -m pytest ...`.

## Environment note

- **Verifiable here (Tasks 1–3):** `compute_risk_rank`, `apply_manual_reopen`, and exposing `risk_rank` on the findings API.
- **Requires your infra (Tasks 4–5, spec):** the reopen endpoint wiring (mockable, but needs the router stack) and the Next.js UI (badges, lifecycle timeline, reopen button, needs-review filter) — needs `npm`/a browser.

---

### Task 1: Pure risk-rank

**Files:**
- Create: `manager/backend/app/services/risk_rank.py`
- Test: `manager/backend/tests/test_risk_rank.py`

**Interfaces:**
- Produces: `compute_risk_rank(*, severity: str, cvss_score: float | None, epss_score: float | None, kev: bool, exploit_validated: bool, verification_state: str | None, confidence: int | None, asset_criticality: str | None, internet_facing: bool | None, auth_enforced: bool | None) -> int` (0–1000).

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_risk_rank.py`:

```python
from __future__ import annotations

from app.services.risk_rank import compute_risk_rank


def _rank(**kw):
    base = dict(severity="high", cvss_score=7.5, epss_score=0.1, kev=False,
                exploit_validated=False, verification_state="inferred",
                confidence=60, asset_criticality="medium",
                internet_facing=False, auth_enforced=False)
    base.update(kw)
    return compute_risk_rank(**base)


def test_bounds():
    assert 0 <= _rank() <= 1000
    assert _rank(severity="critical", cvss_score=10.0, epss_score=0.99, kev=True,
                 exploit_validated=True, verification_state="confirmed",
                 confidence=100, asset_criticality="critical",
                 internet_facing=True, auth_enforced=False) <= 1000


def test_confirmed_exploitable_outranks_contradicted():
    hot = _rank(verification_state="confirmed", exploit_validated=True)
    cold = _rank(verification_state="contradicted")
    assert hot > cold


def test_contradicted_sinks_below_inferred():
    assert _rank(verification_state="contradicted") < _rank(verification_state="inferred")


def test_kev_raises_rank():
    assert _rank(kev=True) > _rank(kev=False)


def test_internet_facing_raises_and_auth_lowers():
    assert _rank(internet_facing=True) > _rank(internet_facing=False)
    assert _rank(auth_enforced=True) < _rank(auth_enforced=False)


def test_low_confidence_lowers_rank():
    assert _rank(confidence=20) < _rank(confidence=95)


def test_missing_optionals_do_not_crash():
    r = compute_risk_rank(severity="low", cvss_score=None, epss_score=None, kev=False,
                          exploit_validated=False, verification_state=None,
                          confidence=None, asset_criticality=None,
                          internet_facing=None, auth_enforced=None)
    assert 0 <= r <= 1000
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_risk_rank.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.services.risk_rank'`.

- [ ] **Step 3: Write the pure function**

Create `manager/backend/app/services/risk_rank.py`:

```python
"""
risk_rank.py — one explainable 0-1000 priority for a finding.

Blends impact (severity/CVSS), exploit likelihood (EPSS/KEV), how sure we are
it's real (verification_state/confidence/exploit_validated), and where it lives
(asset criticality, exposure). Pure + deterministic: every factor is a named
multiplier a reviewer can reconstruct.
"""
from __future__ import annotations

_SEVERITY_BASE = {"critical": 900.0, "high": 700.0, "medium": 450.0, "low": 200.0, "info": 50.0}
_CRIT_MULT = {"critical": 1.2, "high": 1.1, "medium": 1.0, "low": 0.9}
_VERIFICATION_MULT = {"confirmed": 1.25, "corroborated": 1.0, "inferred": 0.8, "contradicted": 0.2}


def compute_risk_rank(*, severity: str, cvss_score: float | None, epss_score: float | None,
                      kev: bool, exploit_validated: bool, verification_state: str | None,
                      confidence: int | None, asset_criticality: str | None,
                      internet_facing: bool | None, auth_enforced: bool | None) -> int:
    # Impact: prefer CVSS when present, else the severity band.
    if cvss_score is not None:
        base = float(cvss_score) / 10.0 * 900.0
    else:
        base = _SEVERITY_BASE.get((severity or "info").lower(), 50.0)

    score = base

    # Exploit likelihood.
    if epss_score is not None:
        score *= 1.0 + 0.5 * max(0.0, min(1.0, float(epss_score)))
    if kev:
        score *= 1.3
    if exploit_validated:
        score *= 1.2

    # How sure we are it's real.
    score *= _VERIFICATION_MULT.get((verification_state or "corroborated").lower(), 1.0)
    if confidence is not None:
        score *= 0.4 + 0.6 * (max(0, min(100, int(confidence))) / 100.0)

    # Where it lives.
    score *= _CRIT_MULT.get((asset_criticality or "medium").lower(), 1.0)
    if internet_facing:
        score *= 1.15
    if auth_enforced:
        score *= 0.9

    return int(max(0.0, min(1000.0, round(score))))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_risk_rank.py -q`
Expected: PASS (7 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/services/risk_rank.py manager/backend/tests/test_risk_rank.py
git commit -m "feat(risk-rank): explainable 0-1000 finding priority"
```

---

### Task 2: Pure manual-reopen helper

**Files:**
- Modify: `manager/backend/app/detection/resolution.py`
- Test: `manager/backend/tests/test_manual_reopen.py`

**Interfaces:**
- Produces: `apply_manual_reopen(finding, *, by: str, now) -> None` — flips a `remediated` finding back to `open`, records `reopened_count += 1`, clears resolution fields, and tags `evidence["reopened_by"] = by`.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_manual_reopen.py`:

```python
from __future__ import annotations

from types import SimpleNamespace

from app.detection.resolution import apply_manual_reopen
from app.models.enums import FindingStatus


def test_manual_reopen_restores_open_and_audits():
    now = object()
    f = SimpleNamespace(status=FindingStatus.remediated, reopened_count=1,
                        resolution_miss_count=2, resolved_at="t", resolution_method="auto",
                        resolution_run_id="r", evidence={"cve_id": "CVE-9"})
    apply_manual_reopen(f, by="alice", now=now)

    assert f.status == FindingStatus.open
    assert f.reopened_count == 2
    assert f.resolution_miss_count == 0
    assert f.resolved_at is None
    assert f.resolution_method is None
    assert f.evidence["reopened_by"] == "alice"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_manual_reopen.py -q`
Expected: FAIL — `ImportError: cannot import name 'apply_manual_reopen'`.

- [ ] **Step 3: Add the helper to `resolution.py`**

Append to `manager/backend/app/detection/resolution.py`:

```python
def apply_manual_reopen(finding, *, by: str, now) -> None:
    """Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's
    regression reopen but records the human who did it. History preserved."""
    finding.status = FindingStatus.open
    finding.reopened_count = (finding.reopened_count or 0) + 1
    finding.resolution_miss_count = 0
    finding.resolved_at = None
    finding.resolution_method = None
    finding.resolution_run_id = None
    ev = dict(finding.evidence or {})
    ev["reopened_by"] = by
    finding.evidence = ev
```

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_manual_reopen.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/resolution.py manager/backend/tests/test_manual_reopen.py
git commit -m "feat(lifecycle): pure manual-reopen helper"
```

---

### Task 3: Expose risk_rank on the findings API

**Files:**
- Modify: `manager/backend/app/schemas/finding.py`
- Test: `manager/backend/tests/test_finding_risk_rank_api.py`

**Interfaces:**
- Produces: `FindingOut.risk_rank: int | None` field.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_finding_risk_rank_api.py`:

```python
from __future__ import annotations

from app.schemas.finding import FindingOut


def test_finding_schema_exposes_risk_rank():
    assert "risk_rank" in FindingOut.model_fields
```

- [ ] **Step 2: Run test to verify it fails**

Run: `./.venv/bin/python -m pytest tests/test_finding_risk_rank_api.py -q`
Expected: FAIL.

- [ ] **Step 3: Add the field**

In `manager/backend/app/schemas/finding.py`, add to `FindingOut` (after the verification fields from P2):

```python
    risk_rank: int | None = None
```

(Populate it in the findings router where the response is built, via `compute_risk_rank(...)` from a finding + its asset — a one-line mapping the router already does for other derived fields. If responses are serialized directly from the ORM, add a small mapping in the list handler.)

- [ ] **Step 4: Run test to verify it passes**

Run: `./.venv/bin/python -m pytest tests/test_finding_risk_rank_api.py -q`
Expected: PASS.

- [ ] **Step 5: Full suite + commit**

Run: `./.venv/bin/python -m pytest -q -m "not integration"` → PASS.

```bash
git add manager/backend/app/schemas/finding.py manager/backend/tests/test_finding_risk_rank_api.py
git commit -m "feat(risk-rank): expose risk_rank on findings API"
```

---

### Task 4 (SPEC — requires router stack): reopen endpoint

**Design:** `POST /engagements/{id}/findings/{finding_id}/reopen` (auth: tester/manager) → load the finding (tenant-scoped), call `apply_manual_reopen(finding, by=current_user.email, now=utcnow())`, commit, return the updated `FindingOut`. Reject if the finding isn't `remediated` (409). **Test (when infra available):** mocked-session unit test asserting the status transition and 409 on a non-remediated finding, following `tests/test_job_result_service.py` mocking.

---

### Task 5 (SPEC — requires npm/browser): dashboard surfacing

**Files:** `manager/frontend/components/` (+ the findings table/detail views).

**Design:**
- **Verification badge** on each finding row: `Confirmed-Active` (green), `Corroborated` (blue), `Inferred` (grey), `Contradicted` (struck-through/muted) from `verification_state`; a `Needs review` chip when `needs_review`.
- **Lifecycle timeline** in the finding detail: `first_seen → last_seen → (pending remediation: miss N/threshold) → remediated (auto, run #, coverage proof) / reopened (regression)`.
- **Reopen button** on auto-resolved findings → `POST …/reopen`.
- **Sort by `risk_rank`** as the default order; **filter** by `needs_review` and `verification_state`.
- **Regression badge** when `evidence.regression` is set; **auto-resolved** badge when `resolution_method == "auto"`.

**Why not executed here:** needs `npm run dev`/a browser to verify rendering (use gstack `/browse` or `/qa` per the repo's CLAUDE.md). All data it needs is already exposed by P1–P4 backend fields.

---

## Self-Review

**1. Spec coverage (against `plan_after_probe.md §4.6, §7`):**
- Unified risk rank (severity×CVSS×EPSS×KEV×exploit_validated×verification×confidence×criticality×exposure) → Task 1. ✅
- Contradicted/low-confidence sink; confirmed/exploitable/exposed float → Task 1 tests. ✅
- One-click reopen → Task 2 (helper) + Task 4 (endpoint spec) + Task 5 (button spec). ✅
- Lifecycle timeline + badges + needs-review filter → Task 5 (spec; backend fields exist). ✅
- Explainable rank → Task 1 (named multipliers). ✅

**2. Placeholder scan:** Tasks 1–3 have complete code. Tasks 4–5 are labeled SPEC with concrete designs + when-infra tests.

**3. Type consistency:** `compute_risk_rank(**kwargs) -> int` signature matches its API/Task-3 use. `apply_manual_reopen(finding, *, by, now)` matches Task-4 endpoint spec. `risk_rank`, `verification_state`, `needs_review` field names match P2/P4 schema. ✅

---

## Execution Handoff

Executing Tasks 1–3 inline (pure logic + schema — verifiable here). Tasks 4–5 are spec-complete and flagged for the router stack / frontend environment.

## Execution status (updated 2026-08-12)

- **Task 1 — pure risk-rank** ✅ committed (`0d6be85`).
- **Task 2 — pure manual-reopen helper** ✅ committed (`3c7740e`).
- **Task 3 — expose `risk_rank` on findings API** ✅ committed (`85e4537`).
- **Task 4 — reopen endpoint** ✅ committed (`3c277ba`) as `POST /findings/{finding_id}/reopen`
  (`app/routers/findings.py`; 409 unless `remediated`; audits `reopened_by`).
- **Task 5 — dashboard surfacing** ✅ **implemented** (2026-08-12). Backend gaps it depended on were
  also closed: `FindingOut` now **computes `risk_rank`** (model validator) and exposes
  `resolution_method`/`reopened_count`/`resolved_at`; the findings list gained
  `verification_state` + `needs_review` filters (`app/schemas/finding.py`, `app/routers/findings.py`;
  +4 tests, backend suite 493). Frontend (`lib/adapters.ts`, `app/api/findings/route.ts`, new
  `app/api/findings/[id]/reopen/route.ts`, `app/findings/page.tsx`): verification badge
  (confirmed/corroborated/inferred/contradicted, contradicted struck-through), needs-review chip,
  regression + auto-resolved badges on list rows **and** detail header; a compact lifecycle timeline
  (first-seen → last-seen → resolved/regressed/reopened); a Reopen button on remediated findings
  wired to `POST /findings/{id}/reopen`; and `needs_review` + `verification_state` filter controls.
  Verified: `tsc --noEmit` clean, `next build` success, 82 frontend tests pass.
  **Not covered:** true server-side *sort by `risk_rank`* still uses the existing risk-first
  (`risk_score`) SQL order as a proxy — a materialized `risk_rank` column is the follow-up; and live
  visual/browser QA (`/browse`) was not run in this environment.
