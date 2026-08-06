# Posture & Patch-Comparison Scorecard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Show which vulnerabilities were patched between the previous and latest detection run, plus three bounded posture scores, on the dashboard and mirrored into reports.

**Architecture:** A new pure, DB-free service `services/posture.py` (duck-typed over `FindingView` rows, following the `services/sla.py` / `services/analytics.py` pattern) computes the scores, the comparison matrix, and the full response dict. A thin endpoint on the existing `routers/analytics.py` loads two detection runs + findings and delegates to it. Two dashboard React components and one deterministic report section read the same service output, so they can never disagree.

**Tech Stack:** Python 3.13, FastAPI, SQLAlchemy async, pytest (asyncio); Next.js (modified fork) + React + @tanstack/react-query.

## Global Constraints

- **No new dependencies** (backend or frontend).
- **Backend pure-service pattern:** scoring/comparison logic lives in `services/posture.py` as pure functions over duck-typed `FindingView` dataclasses — no DB or network calls inside the service. Routers stay thin (mirror `routers/analytics.py`).
- **Tenant scoping:** every DB query joins to `Engagement` and filters `Engagement.tenant_id == current_user.tenant_id`; engagement lookups use `app.utils.db.get_or_404(db, Engagement, id, tenant_id)`.
- **Open findings** = `status in (FindingStatus.open, FindingStatus.confirmed)`.
- **Scores are 0–100, bounded, monotonic**, via noisy-OR `aggregate(pₖ) = 100·(1 − ∏(1 − clamp(pₖ,0,1)))`.
- **Grade bands (verbatim):** A ≥ 90, B ≥ 75, C ≥ 55, D ≥ 35, F < 35.
- **Posture blend (verbatim):** `blend = 0.6·RiskIndex + 0.4·ExploitableScore`; `PostureScore = round(100 − blend)`.
- **Asset-criticality weights (verbatim, reuse `enrichment._CRIT_WEIGHT`):** critical 1.0, high 0.75, medium 0.5, low 0.25; missing → 0.5.
- **Exploit likelihood (verbatim):** `exploitΞ = max(epss_n, 0.6 if exploitable, 1.0 if exploit_validated)`; `pₖ = exploitΞ · asset_crit`.
- **Timestamps:** normalize all datetimes to UTC before comparison; treat naive as UTC (same stance as `sla.py`).
- **Frontend is a modified Next.js:** before writing any frontend code, read the relevant guide under `manager/frontend/node_modules/next/dist/docs/` (per `manager/frontend/AGENTS.md`). Follow existing widget conventions: `fetchJson` from `lib/fetcher`, `useQuery`, and `SkeletonRows`/`ErrorState`/`EmptyState` from `components/states/DataState`. Colors via CSS vars (`var(--sev-critical-color)`, etc.).
- **Run all backend commands from `manager/backend/`.** Test runner: `python -m pytest`.

---

### Task 1: Posture scoring core (`aggregate`, `compute_scores`, grade)

**Files:**
- Create: `manager/backend/app/services/posture.py`
- Test: `manager/backend/tests/test_posture.py`

**Interfaces:**
- Consumes: `enrichment._CRIT_WEIGHT` (asset-criticality → weight).
- Produces:
  - `FindingView` dataclass with fields: `id: str`, `severity: str`, `risk_score: float | None`, `epss_score: float | None`, `exploitable: bool`, `exploit_validated: bool`, `asset_criticality: str | None`, `first_seen: datetime | None`, `last_seen: datetime | None`.
  - `Scores` dataclass: `risk_index: float`, `exploitable_score: float`, `posture_score: int`, `grade: str`.
  - `aggregate(probs: list[float]) -> float`
  - `compute_scores(open_findings: list[FindingView]) -> Scores`
  - `grade_for(posture_score: int) -> str`

- [ ] **Step 1: Write the failing tests**

```python
# manager/backend/tests/test_posture.py
from __future__ import annotations

from datetime import datetime, timezone

from app.services.posture import (
    FindingView, Scores, aggregate, compute_scores, grade_for,
)


def _fv(**kw) -> FindingView:
    base = dict(
        id="f", severity="high", risk_score=None, epss_score=None,
        exploitable=False, exploit_validated=False, asset_criticality=None,
        first_seen=None, last_seen=None,
    )
    base.update(kw)
    return FindingView(**base)


def test_aggregate_is_bounded_and_empty_is_zero():
    assert aggregate([]) == 0.0
    assert 0.0 <= aggregate([0.5, 0.5, 0.9]) <= 100.0
    # noisy-OR: two independent 0.5 → 1-(0.5*0.5)=0.75 → 75.0
    assert aggregate([0.5, 0.5]) == 75.0
    # values clamp to [0,1]
    assert aggregate([5.0]) == 100.0


def test_aggregate_is_monotonic():
    before = aggregate([0.4, 0.4])
    after = aggregate([0.4, 0.4, 0.3])
    assert after >= before


def test_grade_bands():
    assert grade_for(95) == "A"
    assert grade_for(90) == "A"
    assert grade_for(80) == "B"
    assert grade_for(60) == "C"
    assert grade_for(40) == "D"
    assert grade_for(10) == "F"


def test_compute_scores_empty_is_perfect():
    s = compute_scores([])
    assert s == Scores(risk_index=0.0, exploitable_score=0.0, posture_score=100, grade="A")


def test_compute_scores_uses_risk_epss_exploit_and_asset_criticality():
    findings = [
        _fv(risk_score=800, epss_score=0.9, exploit_validated=True, asset_criticality="critical"),
        _fv(risk_score=200, epss_score=0.1, exploitable=True, asset_criticality="low"),
    ]
    s = compute_scores(findings)
    # risk_index = 100*(1-(1-0.8)(1-0.2)) = 100*(1-0.16) = 84.0
    assert s.risk_index == 84.0
    # finding 1 exploit prob = max(0.9,0.6? no,1.0)*1.0 = 1.0 → aggregate saturates to 100
    assert s.exploitable_score == 100.0
    # blend = 0.6*84 + 0.4*100 = 90.4 → posture = round(100-90.4)=10 → grade F
    assert s.posture_score == 10
    assert s.grade == "F"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd manager/backend && python -m pytest tests/test_posture.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'app.services.posture'`

- [ ] **Step 3: Write minimal implementation**

```python
# manager/backend/app/services/posture.py
"""
Posture scoring & patch-comparison — the single source of truth behind the
dashboard scorecard and the report's "Posture & Remediation Progress" section.

Pure and DB-free (mirrors services/sla.py and services/analytics.py): callers
build lightweight FindingView rows and pass them in. Scores use a noisy-OR
aggregate so each open finding adds diminishing marginal risk, every score is
bounded to 0-100, and adding a finding can never lower risk.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from app.vuln.enrichment import _CRIT_WEIGHT  # asset-criticality → 0-1 weight (DRY)

# Posture Score → letter grade. Ordered high-to-low; first threshold met wins.
_GRADE_BANDS = ((90, "A"), (75, "B"), (55, "C"), (35, "D"), (0, "F"))


@dataclass
class FindingView:
    """Duck-typed projection of a Finding + its asset's criticality."""
    id: str
    severity: str
    risk_score: float | None
    epss_score: float | None
    exploitable: bool
    exploit_validated: bool
    asset_criticality: str | None
    first_seen: datetime | None
    last_seen: datetime | None


@dataclass
class Scores:
    risk_index: float
    exploitable_score: float
    posture_score: int
    grade: str


def _clamp01(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def aggregate(probs: list[float]) -> float:
    """Noisy-OR: 100·(1 − ∏(1 − clamp(p))). Empty → 0.0. Always in [0, 100]."""
    prod = 1.0
    for p in probs:
        prod *= (1.0 - _clamp01(float(p)))
    return round(100.0 * (1.0 - prod), 2)


def grade_for(posture_score: int) -> str:
    for threshold, letter in _GRADE_BANDS:
        if posture_score >= threshold:
            return letter
    return "F"


def _risk_prob(f: FindingView) -> float:
    rs = float(f.risk_score) if f.risk_score is not None else 0.0
    return rs / 1000.0


def _exploit_prob(f: FindingView) -> float:
    epss_n = _clamp01(float(f.epss_score) if f.epss_score is not None else 0.0)
    candidates = [epss_n]
    if f.exploitable:
        candidates.append(0.6)
    if f.exploit_validated:
        candidates.append(1.0)
    exploit_xi = max(candidates)
    crit = _CRIT_WEIGHT.get(f.asset_criticality or "", 0.5)
    return exploit_xi * crit


def compute_scores(open_findings: list[FindingView]) -> Scores:
    risk_index = aggregate([_risk_prob(f) for f in open_findings])
    exploitable_score = aggregate([_exploit_prob(f) for f in open_findings])
    blend = 0.6 * risk_index + 0.4 * exploitable_score
    posture_score = round(100 - blend)
    return Scores(
        risk_index=risk_index,
        exploitable_score=exploitable_score,
        posture_score=posture_score,
        grade=grade_for(posture_score),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd manager/backend && python -m pytest tests/test_posture.py -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/services/posture.py manager/backend/tests/test_posture.py
git commit -m "feat(posture): add pure scoring core (noisy-OR risk/exploit/posture)"
```

---

### Task 2: Run-comparison + response builder (`compare`, `build_posture`)

**Files:**
- Modify: `manager/backend/app/services/posture.py`
- Test: `manager/backend/tests/test_posture.py`

**Interfaces:**
- Consumes: `FindingView`, `Scores`, `compute_scores` (Task 1).
- Produces:
  - `build_posture(views: list[FindingView], prev_run: dict | None, latest_run: dict | None) -> dict`
    where each `run` dict is `{"id": str, "started_at": datetime}` (or `None`).
    Returns `{"has_runs": False}` when `latest_run is None`; otherwise a dict with
    keys: `has_runs`(True), `latest_run`, `previous_run`, `scores`, `scores_prev`,
    `matrix` (list of `{severity, prev_open, new, resolved, now_open, net}`),
    `risk_burned_down` (float), `resolved_count`, `new_count`, `persisting_count`.

- [ ] **Step 1: Write the failing tests**

```python
# append to manager/backend/tests/test_posture.py
from app.services.posture import build_posture

_T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)   # previous run
_T1 = datetime(2026, 2, 1, tzinfo=timezone.utc)   # latest run


def test_build_posture_no_runs():
    assert build_posture([], None, None) == {"has_runs": False}


def test_build_posture_single_run_has_no_prev():
    # one finding seen only at latest run
    fv = _fv(id="a", severity="high", risk_score=500, first_seen=_T1, last_seen=_T1)
    out = build_posture([fv], None, {"id": "L", "started_at": _T1})
    assert out["has_runs"] is True
    assert out["previous_run"] is None
    assert out["new_count"] == 1
    assert out["resolved_count"] == 0
    # matrix: high row shows new=1, prev_open=0
    high = next(r for r in out["matrix"] if r["severity"] == "high")
    assert high["new"] == 1 and high["prev_open"] == 0 and high["now_open"] == 1


def test_build_posture_buckets_resolved_new_persisting():
    resolved = _fv(id="r", severity="critical", risk_score=900,
                   first_seen=_T0, last_seen=_T0)                 # in P, gone from L
    persisting = _fv(id="p", severity="high", risk_score=400,
                     first_seen=_T0, last_seen=_T1)               # in both
    new = _fv(id="n", severity="medium", risk_score=300,
              first_seen=_T1, last_seen=_T1)                      # only in L
    out = build_posture(
        [resolved, persisting, new],
        {"id": "P", "started_at": _T0},
        {"id": "L", "started_at": _T1},
    )
    assert out["resolved_count"] == 1
    assert out["new_count"] == 1
    assert out["persisting_count"] == 1
    assert out["risk_burned_down"] == 900.0
    crit = next(r for r in out["matrix"] if r["severity"] == "critical")
    assert crit["resolved"] == 1 and crit["now_open"] == 0 and crit["net"] == -1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd manager/backend && python -m pytest tests/test_posture.py -k build_posture -v`
Expected: FAIL with `ImportError: cannot import name 'build_posture'`

- [ ] **Step 3: Write minimal implementation**

Append to `manager/backend/app/services/posture.py`:

```python
# Severity display order for the comparison matrix.
_SEVERITY_ORDER = ("critical", "high", "medium", "low", "info")


def _to_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def _present_in_run(f: FindingView, run_at: datetime | None) -> bool:
    """True when the finding was live as of run_at (first_seen ≤ run_at ≤ last_seen)."""
    if run_at is None:
        return False
    fs = _to_utc(f.first_seen)
    if fs is None:
        return False
    ls = _to_utc(f.last_seen) or fs
    return fs <= run_at and ls >= run_at


def _severity(f: FindingView) -> str:
    return f.severity if f.severity in _SEVERITY_ORDER else "info"


def compare(views: list[FindingView], prev_at: datetime | None, latest_at: datetime) -> dict:
    """Bucket findings across the previous→latest run transition."""
    latest_open = [f for f in views if _present_in_run(f, latest_at)]
    prev_open = [f for f in views if _present_in_run(f, prev_at)]

    latest_ids = {f.id for f in latest_open}
    prev_ids = {f.id for f in prev_open}

    resolved = [f for f in prev_open if f.id not in latest_ids]
    new = [f for f in latest_open if f.id not in prev_ids]
    persisting = [f for f in latest_open if f.id in prev_ids]

    # Per-severity matrix.
    matrix = []
    for sev in _SEVERITY_ORDER:
        p = sum(1 for f in prev_open if _severity(f) == sev)
        nw = sum(1 for f in new if _severity(f) == sev)
        rs = sum(1 for f in resolved if _severity(f) == sev)
        no = sum(1 for f in latest_open if _severity(f) == sev)
        matrix.append({
            "severity": sev, "prev_open": p, "new": nw,
            "resolved": rs, "now_open": no, "net": no - p,
        })

    risk_burned_down = round(
        sum(float(f.risk_score) for f in resolved if f.risk_score is not None), 2
    )

    return {
        "latest_open": latest_open,
        "prev_open": prev_open,
        "matrix": matrix,
        "risk_burned_down": risk_burned_down,
        "resolved_count": len(resolved),
        "new_count": len(new),
        "persisting_count": len(persisting),
    }


def build_posture(
    views: list[FindingView],
    prev_run: dict | None,
    latest_run: dict | None,
) -> dict:
    """Full dashboard/report payload. Degrades gracefully with 0 or 1 run."""
    if latest_run is None:
        return {"has_runs": False}

    prev_at = _to_utc(prev_run["started_at"]) if prev_run else None
    latest_at = _to_utc(latest_run["started_at"])

    cmp = compare(views, prev_at, latest_at)
    scores = compute_scores(cmp["latest_open"])
    scores_prev = compute_scores(cmp["prev_open"]) if prev_run else compute_scores([])

    return {
        "has_runs": True,
        "latest_run": {"id": latest_run["id"], "started_at": latest_at.isoformat()},
        "previous_run": (
            {"id": prev_run["id"], "started_at": prev_at.isoformat()} if prev_run else None
        ),
        "scores": scores.__dict__,
        "scores_prev": scores_prev.__dict__ if prev_run else None,
        "matrix": cmp["matrix"],
        "risk_burned_down": cmp["risk_burned_down"],
        "resolved_count": cmp["resolved_count"],
        "new_count": cmp["new_count"],
        "persisting_count": cmp["persisting_count"],
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd manager/backend && python -m pytest tests/test_posture.py -v`
Expected: PASS (all 9 tests)

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/services/posture.py manager/backend/tests/test_posture.py
git commit -m "feat(posture): add run comparison, matrix, and response builder"
```

---

### Task 3: Posture endpoint (`GET /analytics/posture`)

**Files:**
- Modify: `manager/backend/app/routers/analytics.py`
- Test: `manager/backend/tests/test_posture.py`

**Interfaces:**
- Consumes: `build_posture`, `FindingView` (Tasks 1–2); `DetectionRun`, `RUN_COMPLETED`; `Finding`; `Asset`; `Engagement`.
- Produces: `GET /analytics/posture?engagement_id=<uuid?>` → the `build_posture` dict.
  When `engagement_id` is omitted, resolves to the engagement owning the newest
  completed detection run for the tenant. Also produces a pure helper
  `_finding_views(rows) -> list[FindingView]` unit-tested here.

- [ ] **Step 1: Write the failing test** (for the pure row→view mapper only; the endpoint is verified manually per repo convention)

```python
# append to manager/backend/tests/test_posture.py
from app.routers.analytics import _finding_views


class _Row:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def test_finding_views_maps_columns_and_asset_criticality():
    rows = [
        _Row(id="1", severity=type("S", (), {"value": "high"})(),
             risk_score=400, epss_score=0.2, exploitable=True,
             exploit_validated=False, asset_criticality="critical",
             first_seen=_T0, last_seen=_T1),
    ]
    views = _finding_views(rows)
    assert views[0].id == "1"
    assert views[0].severity == "high"
    assert views[0].asset_criticality == "critical"
    assert views[0].exploitable is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && python -m pytest tests/test_posture.py::test_finding_views_maps_columns_and_asset_criticality -v`
Expected: FAIL with `ImportError: cannot import name '_finding_views'`

- [ ] **Step 3: Write minimal implementation**

Add to the imports at the top of `manager/backend/app/routers/analytics.py`:

```python
from app.models.detection_run import DetectionRun, RUN_COMPLETED
from app.services import posture as posture_service
```

Append to `manager/backend/app/routers/analytics.py`:

```python
def _sev_str(value) -> str:
    return value.value if hasattr(value, "value") else str(value)


def _finding_views(rows) -> list[posture_service.FindingView]:
    """Map joined (Finding, Asset.criticality) rows to duck-typed views."""
    return [
        posture_service.FindingView(
            id=str(r.id),
            severity=_sev_str(r.severity),
            risk_score=float(r.risk_score) if r.risk_score is not None else None,
            epss_score=float(r.epss_score) if r.epss_score is not None else None,
            exploitable=bool(r.exploitable),
            exploit_validated=bool(r.exploit_validated),
            asset_criticality=(
                _sev_str(r.asset_criticality) if getattr(r, "asset_criticality", None) is not None else None
            ),
            first_seen=r.first_seen,
            last_seen=r.last_seen,
        )
        for r in rows
    ]


async def _two_latest_completed_runs(db, engagement_id):
    rows = (await db.execute(
        select(DetectionRun.id, DetectionRun.started_at)
        .where(DetectionRun.engagement_id == engagement_id, DetectionRun.status == RUN_COMPLETED)
        .order_by(DetectionRun.started_at.desc())
        .limit(2)
    )).all()
    latest = {"id": str(rows[0].id), "started_at": rows[0].started_at} if len(rows) >= 1 else None
    prev = {"id": str(rows[1].id), "started_at": rows[1].started_at} if len(rows) >= 2 else None
    return prev, latest


@router.get("/posture", summary="Posture scores + patch comparison (prev vs latest run)")
async def posture(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    tenant_id = current_user.tenant_id

    # Resolve engagement: explicit, else the one owning the newest completed run.
    if engagement_id is None:
        row = (await db.execute(
            select(DetectionRun.engagement_id)
            .join(Engagement, DetectionRun.engagement_id == Engagement.id)
            .where(Engagement.tenant_id == tenant_id, DetectionRun.status == RUN_COMPLETED)
            .order_by(DetectionRun.started_at.desc())
            .limit(1)
        )).first()
        if row is None:
            return {"has_runs": False}
        engagement_id = row.engagement_id
    else:
        await get_or_404(db, Engagement, engagement_id, tenant_id)

    prev_run, latest_run = await _two_latest_completed_runs(db, engagement_id)

    finding_rows = (await db.execute(
        select(
            Finding.id, Finding.severity, Finding.risk_score, Finding.epss_score,
            Finding.exploitable, Finding.exploit_validated,
            Finding.first_seen, Finding.last_seen,
            Asset.criticality.label("asset_criticality"),
        )
        .outerjoin(Asset, Finding.asset_id == Asset.id)
        .where(Finding.engagement_id == engagement_id)
    )).all()

    views = _finding_views(finding_rows)
    return posture_service.build_posture(views, prev_run, latest_run)
```

Add the needed imports if missing at the top of the file: `get_or_404` from `app.utils.db` (`from app.utils.db import get_or_404`).

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd manager/backend && python -m pytest tests/test_posture.py -v`
Expected: PASS (10 tests)

- [ ] **Step 5: Manually verify the route registers**

Run: `cd manager/backend && python -c "from app.main import app; print([r.path for r in app.routes if 'posture' in r.path])"`
Expected: prints `['/analytics/posture']`

- [ ] **Step 6: Commit**

```bash
git add manager/backend/app/routers/analytics.py manager/backend/tests/test_posture.py
git commit -m "feat(posture): add GET /analytics/posture endpoint"
```

---

### Task 4: Dashboard `PostureScorecard` component

**Files:**
- Create: `manager/frontend/components/dashboard/PostureScorecard.tsx`

**Interfaces:**
- Consumes: `GET /api/analytics/posture` (BFF proxies to backend `/analytics/posture`).
- Produces: `export function PostureScorecard()` and `usePosture()` hook + `Posture` type (imported by Task 5 & 6). `Posture` shape:
  `{ has_runs: boolean; scores?: Scores; scores_prev?: Scores | null; matrix?: MatrixRow[]; risk_burned_down?: number; resolved_count?: number; new_count?: number; persisting_count?: number }`
  with `Scores = { risk_index: number; exploitable_score: number; posture_score: number; grade: string }`
  and `MatrixRow = { severity: string; prev_open: number; new: number; resolved: number; now_open: number; net: number }`.

- [ ] **Step 1: Read the framework docs**

Run: `ls manager/frontend/node_modules/next/dist/docs/` and read the client-component / data-fetching guide before writing. (Per `manager/frontend/AGENTS.md` this is a modified Next.js.)

- [ ] **Step 2: Write the component** (no test — frontend widgets in this repo are verified by build + manual review, matching `Exposure.tsx`)

```tsx
// manager/frontend/components/dashboard/PostureScorecard.tsx
"use client";

/**
 * PostureScorecard — the dashboard headline for security posture.
 *
 * Reads /api/analytics/posture (backend services/posture.py is authoritative;
 * this only formats). Shows Posture Score + grade, plus Risk Index and
 * Exploitable Score, each with a prev→now delta arrow.
 */
import React from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldCheck, TrendingDown, TrendingUp, Minus } from "lucide-react";
import { fetchJson } from "../../lib/fetcher";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";

export interface Scores {
  risk_index: number; exploitable_score: number; posture_score: number; grade: string;
}
export interface MatrixRow {
  severity: string; prev_open: number; new: number; resolved: number; now_open: number; net: number;
}
export interface Posture {
  has_runs: boolean;
  scores?: Scores;
  scores_prev?: Scores | null;
  matrix?: MatrixRow[];
  risk_burned_down?: number;
  resolved_count?: number; new_count?: number; persisting_count?: number;
}

export function usePosture() {
  return useQuery({
    queryKey: ["posture"],
    queryFn: () => fetchJson<Posture>("/api/analytics/posture"),
    refetchInterval: 60_000,
  });
}

const GRADE_COLOR: Record<string, string> = {
  A: "var(--nominal-color)", B: "var(--accent)", C: "var(--sev-medium-color)",
  D: "var(--sev-high-color)", F: "var(--sev-critical-color)",
};

/** Delta arrow. `improvedWhenLower` flips arrow meaning for risk-type metrics. */
function Delta({ now, prev, improvedWhenLower }: { now?: number; prev?: number; improvedWhenLower: boolean }) {
  if (prev == null || now == null) return null;
  const diff = Math.round((now - prev) * 10) / 10;
  if (diff === 0) return <span style={{ color: "var(--text-muted)", display: "inline-flex", alignItems: "center", gap: 2 }}><Minus size={12} /> 0</span>;
  const better = improvedWhenLower ? diff < 0 : diff > 0;
  const color = better ? "var(--nominal-color)" : "var(--sev-high-color)";
  const Icon = diff < 0 ? TrendingDown : TrendingUp;
  return <span style={{ color, display: "inline-flex", alignItems: "center", gap: 2, fontSize: 12 }}><Icon size={12} /> {Math.abs(diff)}</span>;
}

function StatCard({ label, value, delta }: { label: string; value: React.ReactNode; delta?: React.ReactNode }) {
  return (
    <div style={{ flex: 1, minWidth: 120, padding: 14, borderRadius: 10, background: "var(--bg-hover)", display: "flex", flexDirection: "column", gap: 4 }}>
      <span style={{ fontSize: 11, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: 0.5 }}>{label}</span>
      <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <span style={{ fontSize: 22, fontWeight: 700, color: "var(--text-primary)" }}>{value}</span>
        {delta}
      </div>
    </div>
  );
}

export function PostureScorecard() {
  const { data, isLoading, error, refetch } = usePosture();
  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={2} height={64} /></div>;
  if (error) return <ErrorState title="Couldn't load posture." onRetry={() => refetch()} />;
  if (!data?.has_runs || !data.scores) {
    return <div style={{ padding: 24 }}><EmptyState icon={ShieldCheck} title="No scan history yet" hint="Posture and patch comparison appear after your first completed scan." /></div>;
  }
  const s = data.scores;
  const p = data.scores_prev ?? undefined;
  return (
    <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
      <StatCard
        label="Posture Score"
        value={<span style={{ color: GRADE_COLOR[s.grade] ?? "var(--text-primary)" }}>{s.posture_score} · {s.grade}</span>}
        delta={<Delta now={s.posture_score} prev={p?.posture_score} improvedWhenLower={false} />}
      />
      <StatCard label="Risk Index" value={s.risk_index} delta={<Delta now={s.risk_index} prev={p?.risk_index} improvedWhenLower />} />
      <StatCard label="Exploitable" value={s.exploitable_score} delta={<Delta now={s.exploitable_score} prev={p?.exploitable_score} improvedWhenLower />} />
    </div>
  );
}
```

- [ ] **Step 3: Verify the frontend builds**

Run: `cd manager/frontend && npx tsc --noEmit`
Expected: no type errors in `PostureScorecard.tsx`

- [ ] **Step 4: Commit**

```bash
git add manager/frontend/components/dashboard/PostureScorecard.tsx
git commit -m "feat(posture): add dashboard PostureScorecard component"
```

---

### Task 5: Dashboard `PatchComparisonMatrix` component

**Files:**
- Create: `manager/frontend/components/dashboard/PatchComparisonMatrix.tsx`

**Interfaces:**
- Consumes: `usePosture`, `Posture`, `MatrixRow` (Task 4).
- Produces: `export function PatchComparisonMatrix()`.

- [ ] **Step 1: Write the component**

```tsx
// manager/frontend/components/dashboard/PatchComparisonMatrix.tsx
"use client";

/**
 * PatchComparisonMatrix — what changed between the previous and latest scan.
 * Reads the shared /api/analytics/posture payload (same React Query key as the
 * scorecard, so one request feeds both). "Resolved" = present last scan, gone now.
 */
import React from "react";
import { GitCompareArrows } from "lucide-react";
import { SkeletonRows, ErrorState, EmptyState } from "../states/DataState";
import { usePosture, MatrixRow } from "./PostureScorecard";

const SEV_COLOR: Record<string, string> = {
  critical: "var(--sev-critical-color)", high: "var(--sev-high-color)",
  medium: "var(--sev-medium-color)", low: "var(--accent)", info: "var(--text-muted)",
};

function netLabel(net: number): { text: string; color: string } {
  if (net < 0) return { text: `↓${Math.abs(net)}`, color: "var(--nominal-color)" };
  if (net > 0) return { text: `↑${net}`, color: "var(--sev-high-color)" };
  return { text: "0", color: "var(--text-muted)" };
}

export function PatchComparisonMatrix() {
  const { data, isLoading, error, refetch } = usePosture();
  if (isLoading) return <div style={{ padding: 16 }}><SkeletonRows rows={5} height={30} /></div>;
  if (error) return <ErrorState title="Couldn't load patch comparison." onRetry={() => refetch()} />;
  if (!data?.has_runs || !data.matrix) {
    return <div style={{ padding: 24 }}><EmptyState icon={GitCompareArrows} title="Nothing to compare yet" hint="A patch comparison needs at least two completed scans." /></div>;
  }
  const rows = data.matrix.filter((r) => r.prev_open || r.new || r.resolved || r.now_open);
  const cell: React.CSSProperties = { padding: "6px 8px", fontSize: 12, textAlign: "right", color: "var(--text-primary)" };
  const head: React.CSSProperties = { ...cell, color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase", fontSize: 10 };
  return (
    <div style={{ padding: "4px 8px" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ ...head, textAlign: "left" }}>Severity</th>
            <th style={head}>Prev</th><th style={head}>New</th>
            <th style={head}>Patched</th><th style={head}>Now</th><th style={head}>Δ</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r: MatrixRow) => {
            const n = netLabel(r.net);
            return (
              <tr key={r.severity} style={{ borderTop: "1px solid var(--border-subtle, rgba(255,255,255,0.06))" }}>
                <td style={{ ...cell, textAlign: "left", color: SEV_COLOR[r.severity], fontWeight: 600, textTransform: "capitalize" }}>{r.severity}</td>
                <td style={cell}>{r.prev_open}</td>
                <td style={cell}>{r.new}</td>
                <td style={{ ...cell, color: "var(--nominal-color)" }}>{r.resolved}</td>
                <td style={cell}>{r.now_open}</td>
                <td style={{ ...cell, color: n.color }}>{n.text}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
      {typeof data.risk_burned_down === "number" && data.risk_burned_down > 0 && (
        <div style={{ marginTop: 8, fontSize: 12, color: "var(--text-muted)" }}>
          Risk burned down: <span style={{ color: "var(--nominal-color)", fontWeight: 600 }}>{Math.round(data.risk_burned_down)}</span>
          {" "}({data.resolved_count} patched)
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Verify the frontend builds**

Run: `cd manager/frontend && npx tsc --noEmit`
Expected: no type errors

- [ ] **Step 3: Commit**

```bash
git add manager/frontend/components/dashboard/PatchComparisonMatrix.tsx
git commit -m "feat(posture): add dashboard PatchComparisonMatrix component"
```

---

### Task 6: Mount posture widgets on the dashboard

**Files:**
- Modify: `manager/frontend/app/page.tsx`

**Interfaces:**
- Consumes: `PostureScorecard` (Task 4), `PatchComparisonMatrix` (Task 5).

- [ ] **Step 1: Add imports** near the other dashboard-component imports (around `manager/frontend/app/page.tsx:11`)

```tsx
import { PostureScorecard } from "../components/dashboard/PostureScorecard";
import { PatchComparisonMatrix } from "../components/dashboard/PatchComparisonMatrix";
```

- [ ] **Step 2: Render the widgets.** Place a section near the top of the dashboard grid (above or beside the existing Exposure/SLA cards), following the existing `SectionHeader` + card pattern already in the file:

```tsx
<div className="stagger-item">
  <SectionHeader icon={<Shield size={16} />} title="Security posture" />
  <div style={{ background: "var(--bg-card)", borderRadius: 12, padding: 12, marginBottom: 12 }}>
    <PostureScorecard />
  </div>
  <SectionHeader icon={<ScanLine size={16} />} title="Patched since last scan" />
  <div style={{ background: "var(--bg-card)", borderRadius: 12, padding: 4 }}>
    <PatchComparisonMatrix />
  </div>
</div>
```

(Use whatever grid cell/column matches the surrounding JSX; the two `SectionHeader` icons `Shield` and `ScanLine` are already imported in `page.tsx`.)

- [ ] **Step 3: Verify the frontend builds**

Run: `cd manager/frontend && npx tsc --noEmit && npm run build`
Expected: build succeeds

- [ ] **Step 4: Commit**

```bash
git add manager/frontend/app/page.tsx
git commit -m "feat(posture): surface posture scorecard + patch matrix on dashboard"
```

---

### Task 7: Mirror posture into generated reports

**Files:**
- Modify: `manager/backend/app/routers/ai_report.py`
- Test: `manager/backend/tests/test_posture.py`

**Interfaces:**
- Consumes: `posture_service.build_posture`, `_finding_views`, `_two_latest_completed_runs` (Task 3).
- Produces: `build_posture_report_section(posture: dict) -> dict` with keys
  `{"title": "Posture & Remediation Progress", "kind": "posture", "content": <markdown str>}`.
  A pure function, unit-tested; wired into the report's deterministic sections.

- [ ] **Step 1: Write the failing test**

```python
# append to manager/backend/tests/test_posture.py
from app.routers.ai_report import build_posture_report_section


def test_posture_report_section_renders_scores_and_matrix():
    posture = {
        "has_runs": True,
        "scores": {"risk_index": 40.0, "exploitable_score": 20.0, "posture_score": 68, "grade": "C"},
        "scores_prev": {"risk_index": 55.0, "exploitable_score": 30.0, "posture_score": 55, "grade": "C"},
        "matrix": [{"severity": "critical", "prev_open": 2, "new": 0, "resolved": 1, "now_open": 1, "net": -1}],
        "risk_burned_down": 900.0, "resolved_count": 1, "new_count": 0, "persisting_count": 1,
        "previous_run": {"id": "P", "started_at": "2026-01-01T00:00:00+00:00"},
        "latest_run": {"id": "L", "started_at": "2026-02-01T00:00:00+00:00"},
    }
    section = build_posture_report_section(posture)
    assert section["title"] == "Posture & Remediation Progress"
    assert section["kind"] == "posture"
    assert "Posture Score: 68 (C)" in section["content"]
    assert "critical" in section["content"]
    assert "900" in section["content"]


def test_posture_report_section_omitted_without_runs():
    assert build_posture_report_section({"has_runs": False}) is None
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd manager/backend && python -m pytest tests/test_posture.py -k report_section -v`
Expected: FAIL with `ImportError: cannot import name 'build_posture_report_section'`

- [ ] **Step 3: Write minimal implementation**

Add to `manager/backend/app/routers/ai_report.py`:

```python
def build_posture_report_section(posture: dict) -> dict | None:
    """Deterministic report section from the same posture payload the dashboard uses."""
    if not posture.get("has_runs"):
        return None
    s = posture["scores"]
    lines = [
        f"**Posture Score: {s['posture_score']} ({s['grade']})** — "
        f"Risk Index {s['risk_index']}, Exploitable Score {s['exploitable_score']}.",
        "",
        "| Severity | Prev open | New | Patched | Now open | Net |",
        "|---|---|---|---|---|---|",
    ]
    for r in posture.get("matrix", []):
        if not (r["prev_open"] or r["new"] or r["resolved"] or r["now_open"]):
            continue
        lines.append(
            f"| {r['severity']} | {r['prev_open']} | {r['new']} | "
            f"{r['resolved']} | {r['now_open']} | {r['net']:+d} |"
        )
    burned = posture.get("risk_burned_down") or 0
    if burned:
        lines += ["", f"Risk burned down this cycle: **{round(burned)}** across "
                      f"{posture.get('resolved_count', 0)} patched finding(s)."]
    return {"title": "Posture & Remediation Progress", "kind": "posture",
            "content": "\n".join(lines)}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd manager/backend && python -m pytest tests/test_posture.py -v`
Expected: PASS (all tests, incl. 2 new)

- [ ] **Step 5: Wire the section into report generation.** In `ai_report.py`, locate the report-assembly path that builds the engagement summary / sections (near `_build_engagement_summary` / `_run_generation`, around lines 211–310). After the findings are loaded there, compute posture and prepend the deterministic section:

```python
# inside the report-generation flow, where sections are assembled:
from app.routers.analytics import _finding_views, _two_latest_completed_runs
from app.services import posture as posture_service

prev_run, latest_run = await _two_latest_completed_runs(db, engagement_id)
finding_rows = (await db.execute(
    select(
        Finding.id, Finding.severity, Finding.risk_score, Finding.epss_score,
        Finding.exploitable, Finding.exploit_validated,
        Finding.first_seen, Finding.last_seen,
        Asset.criticality.label("asset_criticality"),
    ).outerjoin(Asset, Finding.asset_id == Asset.id)
     .where(Finding.engagement_id == engagement_id)
)).all()
posture_payload = posture_service.build_posture(_finding_views(finding_rows), prev_run, latest_run)
posture_section = build_posture_report_section(posture_payload)
# If posture_section is not None, persist it as a FINAL (non-LLM) llm_outputs row
# alongside the other sections, matching how existing sections are stored.
```

Follow the existing section-persistence code in `_run_generation` for the exact `LLMOutput` row shape/status used by sibling sections (this section is deterministic → store as approved/final, not `pending`). Import `Asset` and `select` if not already imported in the file.

- [ ] **Step 6: Run the full backend suite to confirm no regressions**

Run: `cd manager/backend && python -m pytest tests/test_posture.py tests/test_manager_ai.py -v`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/routers/ai_report.py manager/backend/tests/test_posture.py
git commit -m "feat(posture): mirror posture scorecard into generated reports"
```

---

## Self-Review Notes

- **Spec coverage:** §4 definitions → Task 2 `_present_in_run`/`compare`. §5 scores → Task 1. §6 matrix + risk_burned_down → Task 2. §7.1 service → Tasks 1–2. §7.2 endpoint → Task 3. §7.3 dashboard → Tasks 4–6. §7.4 report mirror → Task 7. §8 edge cases (0/1 run, empty set, nulls) → Task 1 (`test_compute_scores_empty_is_perfect`) + Task 2 (`test_build_posture_no_runs`, `test_build_posture_single_run_has_no_prev`). §9 testing → each task's tests.
- **Deviation from spec §7.2 path:** spec wrote `GET /engagements/{id}/posture`; implemented as `GET /analytics/posture?engagement_id=` to match the existing `analytics.py` router prefix/convention (the `exposure` endpoint uses the identical shape). Functionally equivalent, tenant-scoped identically.
- **Type consistency:** `FindingView`, `Scores`, `MatrixRow`, `Posture` names are used identically across backend (Tasks 1–3, 7) and frontend (Tasks 4–6).
- **No placeholders:** every code step contains complete code; the only prose-guided step is Task 7 Step 5 (persisting the section), which is bounded by "follow the existing sibling-section persistence in `_run_generation`" because that row shape is repo-specific and must not be guessed.
