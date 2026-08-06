# Posture & Patch-Comparison Scorecard — Design Spec

**Date:** 2026-08-05
**Status:** Approved (design), pending implementation plan
**Scope:** Part 1 of a 4-part platform effort. This spec covers **only** Part 1.
Parts 2 (customer portal), 3 (Slack/Jira/Email integrations), and 4 (responsive
UI/UX) are separate specs, built in the order **1 → 3 → 2 → 4**.

---

## 1. Problem

Operators can see the current list of findings, but they cannot see **what
changed between scans** — specifically which vulnerabilities were *actually
fixed* since the last detection run, whether overall exposure is improving or
worsening, and a single defensible number for security posture. Today the raw
material exists (per-finding `risk_score`, detection-run deltas, temporal
`first_seen`/`last_seen`) but there is no aggregation or comparison layer, and
nothing surfaces on the dashboard or in reports.

## 2. Goals

1. Show **which findings were patched** (resolved) between the previous and the
   latest detection run, plus new and persisting findings.
2. Provide three bounded, defensible **posture scores** (Risk Index, Exploitable
   Score, Posture Score/grade) derived from finding criticality, exploitability,
   and asset criticality.
3. Surface all of this on the **dashboard first**, then mirror the **same
   computed values** into generated reports so the two never disagree.

## 3. Non-goals (YAGNI)

- Reintroduced/regressed findings (patched then reappeared) — excluded from v1.
- Selectable arbitrary A/B run comparison — v1 is fixed to *previous vs latest*.
- Manual "remediated" workflow changes — resolution is inferred from scans only.
- Historical posture time-series charts beyond the single prev→now delta.

## 4. Definitions (locked)

- **Detection run**: an existing `DetectionRun` row. We consider only
  `status == completed` runs, ordered by `started_at`.
- **Latest run** `L`: newest completed run for the engagement.
- **Previous run** `P`: the completed run immediately preceding `L`. If only one
  completed run exists, the comparison degrades gracefully (see §8).
- A finding is **present in run R** when
  `first_seen <= R.started_at AND last_seen >= R.started_at`
  (timestamps normalized to UTC; a finding touched once has `first_seen == last_seen`).
- **Resolved / "patched"** = present in `P` but **not** present in `L`
  (i.e. `last_seen < L.started_at` while it was live as of `P`). No human action
  required — this reuses the same "resolution candidate" logic already in
  `routers/detection_runs.py::latest_run_delta`.
- **New** = present in `L` but not in `P` (`first_seen >= P.started_at`).
- **Persisting** = present in both `P` and `L`.
- **Open findings** = `status in {open, confirmed}` (matches `sla.py` `_TRACKED_STATUSES`
  and the router's `_OPEN_STATUSES`).

## 5. Scoring model

All three numbers are on **0–100**, bounded and monotonic, computed with a
**noisy-OR aggregate** so each finding contributes *diminishing marginal* risk
and no single finding pegs the score:

```
aggregate(pₖ) = 100 · (1 − ∏ₖ (1 − clamp(pₖ, 0, 1)))
```

Computed over the **currently open findings** (the `L` open set).

### 5.1 Risk Index (higher = worse)
Per open finding: `pₖ = risk_score / 1000` (reusing the existing
`compute_composite_risk` output; findings with null `risk_score` contribute 0).
`RiskIndex = aggregate(pₖ)`.

### 5.2 Exploitable Score (higher = worse)
Per open finding: `pₖ = exploitΞ · asset_critⱼ` where

- `exploitΞ = max(1.0 if exploit_validated, 0.6 if exploitable, epss_n)`
  with `epss_n = clamp(epss_score, 0, 1)` (null → 0).
- `asset_critⱼ` reuses `enrichment._CRIT_WEIGHT` (critical 1.0, high 0.75,
  medium 0.5, low 0.25; findings with no asset → default 0.5).

`ExploitableScore = aggregate(pₖ)`.

### 5.3 Posture Score + grade (higher = better)
`PostureScore = round(100 − blend)`, where
`blend = 0.6 · RiskIndex + 0.4 · ExploitableScore` (risk weighted slightly over
raw exploitability). Mapped to a letter grade by band:

| Posture Score | Grade |
|---|---|
| 90–100 | A |
| 75–89  | B |
| 55–74  | C |
| 35–54  | D |
| 0–34   | F |

### 5.4 Deltas
Each score is also computed over the **`P` open set** (the open findings as of
the previous run) so the UI can show `prev → now` with a delta arrow. Improving
= Posture Score up / Risk & Exploit down.

## 6. Comparison matrix

A severity × state table over the `P`→`L` transition:

| Severity | Prev open | New | Resolved (patched) | Now open | Net Δ |
|---|---|---|---|---|---|
| critical / high / medium / low / info | count | count | count | count | signed |

Plus:
- **`risk_burned_down`** = Σ `risk_score` of resolved findings (value delivered).
- Totals row.

## 7. Architecture

Mirrors the existing pure-service pattern of `services/sla.py` and
`services/analytics.py` (no I/O, fully unit-testable).

### 7.1 New service — `manager/backend/app/services/posture.py`
Pure functions, no DB/network:

```python
@dataclass
class Scores:
    risk_index: float
    exploitable_score: float
    posture_score: int
    grade: str

def compute_scores(open_findings: list[Finding]) -> Scores: ...

def compare(
    findings: list[Finding],       # all engagement findings (with first/last_seen)
    prev_run_started_at: datetime | None,
    latest_run_started_at: datetime,
) -> dict:
    # returns {
    #   "scores": Scores(L open set), "scores_prev": Scores(P open set),
    #   "matrix": [ {severity, prev_open, new, resolved, now_open, net} ... ],
    #   "risk_burned_down": float,
    #   "resolved_count", "new_count", "persisting_count": int,
    # }
```

Bucketing uses the §4 "present in run R" predicate with UTC-normalized
timestamps (same normalization approach as `sla.py`).

### 7.2 New endpoint — `GET /engagements/{id}/posture`
Added to the existing `routers/analytics.py`. Loads the two newest completed
`DetectionRun` rows + the engagement's findings, calls `posture.compare(...)`,
returns:

```json
{
  "has_runs": true,
  "latest_run": { "id": "...", "started_at": "..." },
  "previous_run": { "id": "...", "started_at": "..." },
  "scores": { "risk_index": 42.1, "exploitable_score": 30.4,
              "posture_score": 61, "grade": "C" },
  "scores_prev": { ... },
  "matrix": [ ... ],
  "risk_burned_down": 1830.5,
  "resolved_count": 3, "new_count": 1, "persisting_count": 7
}
```

Tenant-scoped via the existing `get_or_404(..., current_user.tenant_id)` guard.

### 7.3 Dashboard — `manager/frontend/app/page.tsx`
- **`PostureScorecard`** component: three scores as dials/stat cards with
  `prev → now` delta arrows and the letter grade prominent.
- **`PatchComparisonMatrix`** component: the §6 table + `risk_burned_down`
  callout. Both fetch `GET /engagements/{id}/posture`.

### 7.4 Reports mirror — `manager/backend/app/routers/ai_report.py`
A new **deterministic** (non-LLM) report section "Posture & Remediation
Progress" built by calling the *same* `posture.compare(...)` service. Renders the
three scores, grade, the comparison matrix, and `risk_burned_down`. Because both
dashboard and report read one service, they cannot disagree — exactly the SLA
engine's single-source-of-truth pattern.

## 8. Edge cases & error handling

- **Zero completed runs** → endpoint returns `{"has_runs": false}`; UI shows an
  empty state ("Run a scan to see posture"). Report section omitted.
- **Exactly one completed run** → no `P`. Scores computed for `L` only; matrix
  shows New/Now-open with Prev/Resolved = 0; deltas hidden.
- **Empty open set** → `aggregate([]) = 0` ⇒ RiskIndex 0, ExploitableScore 0,
  PostureScore 100, grade A.
- **Null `risk_score` / `epss` / asset** → contribute 0 / default weight, never
  raise (same defensive stance as `sla.py::compute`).
- Timestamps normalized to UTC before comparison; naive datetimes treated as UTC.

## 9. Testing

New `manager/backend/tests/test_posture.py` (style follows `test_manager_ai.py`):

- `aggregate` bounds: always within [0, 100]; empty ⇒ 0.
- Monotonicity: adding a finding never lowers RiskIndex.
- Empty open set ⇒ PostureScore 100 / grade A.
- All-resolved scenario ⇒ correct `risk_burned_down` and resolved counts.
- Bucketing: a fixture with known first/last_seen across two run timestamps
  yields the expected new/resolved/persisting split.
- One API test asserting the endpoint response shape + tenant scoping + the
  `has_runs:false` and single-run degraded paths.

No new external dependencies.

## 10. Out of scope for this spec

Parts 2–4 (customer portal, integrations, responsive UI/UX) — separate specs.
