# Coverage-Gated Auto-Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** When a later scan *provably re-covers* an asset and a previously-detected finding is gone, auto-mark it `remediated` on the manager — safely, with a confirmation window, a vuln-DB-change guard, and regression reopen.

**Architecture:** Add a small, mostly-pure module `app/detection/resolution.py` (coverage builder + resolution decision core) plus six lifecycle columns on `findings`. Wire it into the existing background detection path (`engine_bridge.create_findings_from_facts`) so every detection run, after producing/​reaffirming findings, evaluates non-reaffirmed findings for auto-resolution. The risky decision logic is pure and fully unit-tested; the DB layer is thin and tested with a mocked session (matching this codebase's test style).

**Tech Stack:** Python 3, SQLAlchemy 2 (async), Alembic, FastAPI (background tasks), Postgres, pytest (`asyncio_mode = strict`).

This plan implements **Phase 0 (coverage ledger)** and **Phase 1 (auto-resolution)** of `plan_after_probe.md`. Phases P2–P4 (LangGraph verification, active validation, risk-rank) are out of scope and get their own plans. A follow-up UI plan adds the reopen button + lifecycle timeline; this plan makes auto-resolution visible through the *existing* findings status column.

## Global Constraints

- **Best-effort, never raises into the probe path.** A resolution failure must never fail probe-result submission (mirror the existing `try/except` posture in `engine_bridge.py`). Copy verbatim: `# noqa: BLE001 — one bad finding must not sink the batch`.
- **Deterministic & offline.** No clock-dependent branching beyond timestamps, no network, same inputs → same decision.
- **Absence ≠ remediation unless coverage is proven.** Only auto-resolve a finding whose asset was re-observed this run by a *completed* scanner.
- **Never auto-resolve across a vuln-DB change.** If the run's `vuln_db_version` differs from the finding's `detected_db_version`, skip (the CVE may have vanished from the DB, not the host).
- **Follow existing patterns.** Async DB tests mock the session (`MagicMock` + `AsyncMock`); pure logic gets plain unit tests. New PG enum values are avoided (no `ALTER TYPE`) — the confirmation window is represented by `resolution_miss_count`, not a new status.
- **Statuses:** `FindingStatus` = `open, confirmed, remediated, accepted, fp` (`app/models/enums.py`). Auto-resolution only ever touches `open`/`confirmed`; never `accepted`/`fp`. Resolved state is `remediated`.
- **Run from `manager/backend/`** for all pytest/alembic commands.

---

### Task 1: Finding resolution-lifecycle schema (model + migration)

**Files:**
- Modify: `manager/backend/app/models/finding.py` (add 6 columns + `Integer` import)
- Create: `manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py`
- Test: `manager/backend/tests/test_finding_resolution_schema.py`

**Interfaces:**
- Produces (used by Tasks 4–6): `Finding.resolution_miss_count: int`, `Finding.resolved_at: datetime | None`, `Finding.resolution_method: str | None`, `Finding.resolution_run_id: uuid.UUID | None`, `Finding.reopened_count: int`, `Finding.detected_db_version: str | None`.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_finding_resolution_schema.py`:

```python
from __future__ import annotations

from app.models.finding import Finding


def test_finding_has_resolution_lifecycle_columns():
    cols = Finding.__table__.columns
    for name in (
        "resolution_miss_count", "resolved_at", "resolution_method",
        "resolution_run_id", "reopened_count", "detected_db_version",
    ):
        assert name in cols, f"missing column {name}"
    assert cols["resolution_miss_count"].nullable is False
    assert cols["reopened_count"].nullable is False
    assert cols["detected_db_version"].nullable is True
    assert cols["resolved_at"].nullable is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && python -m pytest tests/test_finding_resolution_schema.py -v`
Expected: FAIL — `AssertionError: missing column resolution_miss_count`.

- [ ] **Step 3: Add the columns to the model**

In `manager/backend/app/models/finding.py`, add `Integer` to the sqlalchemy import (line 5 currently `from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, Text`):

```python
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
```

Then insert, immediately after the `detection_run_id` column block (after line 60, before the `engagement:` relationship on line 62):

```python
    # ── Resolution lifecycle (coverage-gated auto-resolution) ──────────────────
    # resolution_miss_count: consecutive coverage-proven runs this finding was
    #   ABSENT (reset to 0 the moment it is re-observed). > 0 while status=open
    #   means "pending remediation" — inside the confirmation window.
    # detected_db_version: the vuln-DB snapshot hash that produced this finding.
    #   Used to tell "gone because patched" from "gone because the DB changed"
    #   (never auto-resolve on the latter).
    # resolution_run_id: the run that auto-closed it; resolution_method: auto|manual.
    resolution_miss_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    resolution_run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("detection_runs.id", ondelete="SET NULL"), nullable=True
    )
    reopened_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    detected_db_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && python -m pytest tests/test_finding_resolution_schema.py -v`
Expected: PASS.

- [ ] **Step 5: Create the Alembic migration**

First confirm the current head id:
Run: `grep -h "^revision" manager/backend/alembic/versions/0019_probe_enrollment_tokens.py`
Expected: `revision: str = "0019"` (if different, use that value as `down_revision` below).

Create `manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py`:

```python
"""Finding resolution lifecycle: coverage-gated auto-resolution columns.

Revision ID: 0020
Revises: 0019
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "0020"
down_revision: Union[str, None] = "0019"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("findings", sa.Column("resolution_miss_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("findings", sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("findings", sa.Column("resolution_method", sa.String(length=16), nullable=True))
    op.add_column("findings", sa.Column("resolution_run_id", UUID(as_uuid=True), nullable=True))
    op.add_column("findings", sa.Column("reopened_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("findings", sa.Column("detected_db_version", sa.String(length=128), nullable=True))
    op.create_foreign_key(
        "fk_findings_resolution_run", "findings", "detection_runs",
        ["resolution_run_id"], ["id"], ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_findings_resolution_run", "findings", type_="foreignkey")
    for col in (
        "detected_db_version", "reopened_count", "resolution_run_id",
        "resolution_method", "resolved_at", "resolution_miss_count",
    ):
        op.drop_column("findings", col)
```

- [ ] **Step 6: Verify the migration applies (requires a dev DB)**

Run: `cd manager/backend && alembic upgrade head && alembic downgrade -1 && alembic upgrade head`
Expected: three clean runs, no error. (If no DB is configured locally, skip and note it — CI applies migrations.)

- [ ] **Step 7: Commit**

```bash
git add manager/backend/app/models/finding.py \
        manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py \
        manager/backend/tests/test_finding_resolution_schema.py
git commit -m "feat(resolution): add finding resolution-lifecycle columns + migration"
```

---

### Task 2: Coverage builder (pure)

**Files:**
- Create: `manager/backend/app/detection/resolution.py` (this task adds `host_of` + `build_coverage`)
- Test: `manager/backend/tests/test_resolution_coverage.py`

**Interfaces:**
- Produces: `host_of(target: str) -> str`; `build_coverage(scanner_runs: list[dict] | None, facts: list[dict] | None) -> dict` returning `{"assets": list[str], "scanners_completed": list[str], "scanners_degraded": list[str]}`.
- Consumes: probe result fields `scanner_runs` (each `{"id","status",...}`, status one of `completed|cached|skipped|degraded|failed`) and `facts` (each a ScanResult dict with `scanner` and `target`).

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_resolution_coverage.py`:

```python
from __future__ import annotations

from app.detection.resolution import build_coverage, host_of


def test_host_of_strips_single_port():
    assert host_of("10.0.0.5:443") == "10.0.0.5"
    assert host_of("10.0.0.5") == "10.0.0.5"
    assert host_of("") == ""


def test_coverage_counts_only_completed_scanner_observations():
    scanner_runs = [
        {"id": "tls_scan", "status": "completed"},
        {"id": "smb_scan", "status": "degraded"},
    ]
    facts = [
        {"scanner": "tls_scan", "target": "10.0.0.5:443"},   # completed → covered
        {"scanner": "smb_scan", "target": "10.0.0.6:445"},   # degraded → NOT covered
    ]
    cov = build_coverage(scanner_runs, facts)
    assert cov["assets"] == ["10.0.0.5"]
    assert cov["scanners_completed"] == ["tls_scan"]
    assert cov["scanners_degraded"] == ["smb_scan"]


def test_coverage_empty_when_no_scanner_runs():
    # Older probe with no scanner_runs → nothing counts as covered (fail-closed).
    cov = build_coverage(None, [{"scanner": "tls_scan", "target": "10.0.0.5"}])
    assert cov["assets"] == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && python -m pytest tests/test_resolution_coverage.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'app.detection.resolution'`.

- [ ] **Step 3: Write the module (coverage part)**

Create `manager/backend/app/detection/resolution.py`:

```python
"""
resolution.py — coverage-gated auto-resolution of findings.

Split into a PURE core (host_of / build_coverage / decide_resolution) that is
fully unit-testable without a database, and a thin async applier
(evaluate_resolutions) that walks the engagement's still-open findings and
applies the pure decision. Wired into engine_bridge.create_findings_from_facts.

Safety rule: absence of a finding is only meaningful if we PROVED we looked.
A host counts as covered this run only if a *completed* scanner produced a fact
about it; a degraded/failed/skipped scanner is not proof.
"""
from __future__ import annotations


def host_of(target: str) -> str:
    """IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.
    Mirrors finding_translator._resolve_asset's host extraction."""
    if not target:
        return ""
    return target.split(":", 1)[0] if target.count(":") == 1 else target


def build_coverage(scanner_runs: list[dict] | None, facts: list[dict] | None) -> dict:
    """What this run PROVABLY re-observed. An asset is covered only if a
    completed scanner produced a fact about it. Fail-closed: no scanner_runs
    (older probe) → empty coverage → nothing auto-resolves."""
    scanner_runs = scanner_runs or []
    facts = facts or []
    completed = {sr.get("id") for sr in scanner_runs if sr.get("status") == "completed"}
    degraded = {
        sr.get("id") for sr in scanner_runs
        if sr.get("status") in ("degraded", "failed", "skipped")
    }
    assets = {
        host_of(f.get("target", "")) for f in facts
        if f.get("scanner") in completed and host_of(f.get("target", ""))
    }
    return {
        "assets": sorted(a for a in assets if a),
        "scanners_completed": sorted(c for c in completed if c),
        "scanners_degraded": sorted(d for d in degraded if d),
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && python -m pytest tests/test_resolution_coverage.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/resolution.py manager/backend/tests/test_resolution_coverage.py
git commit -m "feat(resolution): coverage builder from completed-scanner facts"
```

---

### Task 3: Resolution decision core (pure)

**Files:**
- Modify: `manager/backend/app/detection/resolution.py` (add `resolution_threshold`, `ResolutionOutcome`, `decide_resolution`)
- Test: `manager/backend/tests/test_resolution_decision.py`

**Interfaces:**
- Consumes: `FindingSeverity` from `app.models.enums`.
- Produces: `resolution_threshold(severity: FindingSeverity) -> int`; `ResolutionOutcome(action: str, miss_count: int, reason: str)` where `action ∈ {"skip","pending","resolve"}`; `decide_resolution(*, covered: bool, db_changed: bool, miss_count: int, severity: FindingSeverity) -> ResolutionOutcome`.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_resolution_decision.py`:

```python
from __future__ import annotations

from app.detection.resolution import decide_resolution, resolution_threshold
from app.models.enums import FindingSeverity


def test_threshold_is_stricter_for_critical_and_high():
    assert resolution_threshold(FindingSeverity.critical) == 2
    assert resolution_threshold(FindingSeverity.high) == 2
    assert resolution_threshold(FindingSeverity.medium) == 1
    assert resolution_threshold(FindingSeverity.low) == 1
    assert resolution_threshold(FindingSeverity.info) == 1


def test_not_covered_is_skipped_and_counter_untouched():
    out = decide_resolution(covered=False, db_changed=False,
                            miss_count=0, severity=FindingSeverity.medium)
    assert out.action == "skip"
    assert out.miss_count == 0


def test_db_change_blocks_resolution():
    out = decide_resolution(covered=True, db_changed=True,
                            miss_count=0, severity=FindingSeverity.medium)
    assert out.action == "skip"
    assert out.miss_count == 0


def test_medium_resolves_on_first_covered_clean_run():
    out = decide_resolution(covered=True, db_changed=False,
                            miss_count=0, severity=FindingSeverity.medium)
    assert out.action == "resolve"
    assert out.miss_count == 1


def test_high_needs_two_covered_clean_runs():
    first = decide_resolution(covered=True, db_changed=False,
                              miss_count=0, severity=FindingSeverity.high)
    assert first.action == "pending"
    assert first.miss_count == 1
    second = decide_resolution(covered=True, db_changed=False,
                               miss_count=1, severity=FindingSeverity.high)
    assert second.action == "resolve"
    assert second.miss_count == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && python -m pytest tests/test_resolution_decision.py -v`
Expected: FAIL — `ImportError: cannot import name 'decide_resolution'`.

- [ ] **Step 3: Add the decision core to `resolution.py`**

Add these imports at the top of `manager/backend/app/detection/resolution.py` (below the module docstring, replacing the bare `from __future__ import annotations` line with):

```python
from __future__ import annotations

from dataclasses import dataclass

from app.models.enums import FindingSeverity
```

Append to the module (after `build_coverage`):

```python
def resolution_threshold(severity: FindingSeverity) -> int:
    """Consecutive coverage-proven clean runs required before auto-close.
    critical/high demand a SECOND confirmation — a premature 'you're safe' on a
    critical is the costliest false signal in the product."""
    return 2 if severity in (FindingSeverity.critical, FindingSeverity.high) else 1


@dataclass(frozen=True)
class ResolutionOutcome:
    action: str        # "skip" | "pending" | "resolve"
    miss_count: int    # the new resolution_miss_count to persist
    reason: str


def decide_resolution(*, covered: bool, db_changed: bool,
                      miss_count: int, severity: FindingSeverity) -> ResolutionOutcome:
    """Pure heart of auto-resolution. Given whether the finding's asset was
    re-observed this run (covered), whether the vuln-DB basis changed, and the
    current miss streak, decide what to do. Never resolves without coverage."""
    if not covered:
        return ResolutionOutcome("skip", miss_count, "asset not re-observed (out of coverage)")
    if db_changed:
        return ResolutionOutcome("skip", miss_count,
                                 "absent under a changed vuln-DB basis; not a confirmed fix")
    new_count = miss_count + 1
    threshold = resolution_threshold(severity)
    if new_count >= threshold:
        return ResolutionOutcome("resolve", new_count,
                                 f"coverage-proven clean for {new_count} run(s) >= threshold {threshold}")
    return ResolutionOutcome("pending", new_count,
                             f"coverage-proven clean {new_count}/{threshold} runs")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && python -m pytest tests/test_resolution_decision.py -v`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/resolution.py manager/backend/tests/test_resolution_decision.py
git commit -m "feat(resolution): pure decision core (coverage + confirm window + db guard)"
```

---

### Task 4: Async applier `evaluate_resolutions`

**Files:**
- Modify: `manager/backend/app/detection/resolution.py` (add `evaluate_resolutions`)
- Test: `manager/backend/tests/test_resolution_apply.py`

**Interfaces:**
- Consumes: `decide_resolution` (Task 3), `Finding`/`Asset` models, `FindingStatus`.
- Produces: `async def evaluate_resolutions(db: AsyncSession, engagement_id: uuid.UUID, run, coverage: dict, now: datetime) -> int` — returns count auto-resolved. `run` is a `DetectionRun` (reads `run.id`, `run.vuln_db_version`). Mutates `Finding` rows in place (session-tracked).

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_resolution_apply.py`:

```python
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.detection.resolution import evaluate_resolutions
from app.models.enums import FindingSeverity, FindingStatus

_NOW = datetime(2026, 8, 11, tzinfo=timezone.utc)


def _finding(**kw):
    base = dict(
        severity=FindingSeverity.medium, status=FindingStatus.open,
        resolution_miss_count=0, detected_db_version="v1",
        resolved_at=None, resolution_method=None, resolution_run_id=None,
    )
    base.update(kw)
    return SimpleNamespace(**base)


def _db_returning(rows):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(all=lambda: rows))
    db.flush = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_covered_clean_medium_finding_is_auto_resolved():
    run = SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v1")
    f = _finding()
    db = _db_returning([(f, "10.0.0.5")])

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW)

    assert resolved == 1
    assert f.status == FindingStatus.remediated
    assert f.resolution_method == "auto"
    assert f.resolution_run_id == run.id
    assert f.resolved_at == _NOW
    assert f.resolution_miss_count == 1


@pytest.mark.asyncio
async def test_uncovered_finding_is_left_open():
    run = SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v1")
    f = _finding()
    db = _db_returning([(f, "10.0.0.99")])  # host not in coverage

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW)

    assert resolved == 0
    assert f.status == FindingStatus.open
    assert f.resolution_miss_count == 0


@pytest.mark.asyncio
async def test_db_version_change_blocks_resolution():
    run = SimpleNamespace(id=uuid.uuid4(), vuln_db_version="v2")  # DB moved
    f = _finding(detected_db_version="v1")
    db = _db_returning([(f, "10.0.0.5")])

    resolved = await evaluate_resolutions(db, uuid.uuid4(), run, {"assets": ["10.0.0.5"]}, _NOW)

    assert resolved == 0
    assert f.status == FindingStatus.open
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && python -m pytest tests/test_resolution_apply.py -v`
Expected: FAIL — `ImportError: cannot import name 'evaluate_resolutions'`.

- [ ] **Step 3: Implement `evaluate_resolutions`**

Add to the top imports of `manager/backend/app/detection/resolution.py`:

```python
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.finding import Finding
from app.models.enums import FindingStatus
```

(Keep the existing `from app.models.enums import FindingSeverity` — or merge into `from app.models.enums import FindingSeverity, FindingStatus`.)

Append to the module:

```python
async def evaluate_resolutions(
    db: AsyncSession, engagement_id: uuid.UUID, run, coverage: dict, now: datetime,
) -> int:
    """Apply decide_resolution to every engine-managed open/confirmed finding
    NOT touched by `run` (i.e. detection_run_id != run.id). Returns the number
    auto-resolved. Findings with no detection_run_id (probe self-assessed path,
    legacy) are intentionally NOT governed here."""
    covered = set(coverage.get("assets") or [])
    rows = (await db.execute(
        select(Finding, Asset.ip_address)
        .join(Asset, Finding.asset_id == Asset.id)
        .where(
            Finding.engagement_id == engagement_id,
            Finding.status.in_((FindingStatus.open, FindingStatus.confirmed)),
            Finding.detection_run_id.isnot(None),
            Finding.detection_run_id != run.id,
        )
    )).all()

    resolved = 0
    for finding, ip in rows:
        db_changed = (
            run.vuln_db_version is not None
            and finding.detected_db_version is not None
            and finding.detected_db_version != run.vuln_db_version
        )
        outcome = decide_resolution(
            covered=ip in covered, db_changed=db_changed,
            miss_count=finding.resolution_miss_count, severity=finding.severity,
        )
        finding.resolution_miss_count = outcome.miss_count
        if outcome.action == "resolve":
            finding.status = FindingStatus.remediated
            finding.resolved_at = now
            finding.resolution_method = "auto"
            finding.resolution_run_id = run.id
            resolved += 1
    await db.flush()
    return resolved
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && python -m pytest tests/test_resolution_apply.py -v`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add manager/backend/app/detection/resolution.py manager/backend/tests/test_resolution_apply.py
git commit -m "feat(resolution): async applier over engine-managed open findings"
```

---

### Task 5: Wire auto-resolution into the detection run

**Files:**
- Modify: `manager/backend/app/detection/engine_bridge.py` (`create_findings_from_facts`)
- Test: `manager/backend/tests/test_engine_bridge_resolution.py`

**Interfaces:**
- Consumes: `build_coverage`, `evaluate_resolutions` (Tasks 2, 4); existing `db_version` local (`engine_bridge.py:121`), `now` local (`engine_bridge.py:120`), `run` (`engine_bridge.py:125`).
- Produces: after each run, `run.stats == {"coverage": <dict>, "auto_resolved": <int>}`; new findings carry `detected_db_version`; reaffirmed findings have `resolution_miss_count` reset to 0.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_engine_bridge_resolution.py`. This mocks the DB session and patches the deterministic pipeline call, asserting the run gets a coverage ledger and calls the applier:

```python
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge


@pytest.mark.asyncio
async def test_run_records_coverage_and_invokes_resolution():
    engagement_id = uuid.uuid4()
    result = {
        "facts": [{"scanner": "tls_scan", "target": "10.0.0.5:443", "status": "open"}],
        "scanner_runs": [{"id": "tls_scan", "status": "completed"}],
    }

    # A DetectionRun stand-in whose attributes the code sets; db just records adds.
    added = []
    db = MagicMock()
    db.add = MagicMock(side_effect=lambda o: added.append(o))
    db.flush = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))

    with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
         patch.object(engine_bridge, "detect_findings_from_facts", return_value=[]), \
         patch("app.detection.resolution.evaluate_resolutions",
               new=AsyncMock(return_value=2)) as mock_eval:
        await engine_bridge.create_findings_from_facts(db, engagement_id, result)

    # the run row is the first thing added
    run = added[0]
    assert run.stats["coverage"]["assets"] == ["10.0.0.5"]
    assert run.stats["auto_resolved"] == 2
    mock_eval.assert_awaited_once()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && python -m pytest tests/test_engine_bridge_resolution.py -v`
Expected: FAIL — `KeyError: 'coverage'` (run.stats not set) or `AttributeError`.

- [ ] **Step 3: Wire the calls into `create_findings_from_facts`**

In `manager/backend/app/detection/engine_bridge.py`:

**(a)** Add the import near the other detection imports (top of file, after line 36):

```python
from app.detection.resolution import build_coverage, evaluate_resolutions
```

**(b)** Stamp `detected_db_version` on new findings. In the `db.add(Finding(...))` call (around line 158–174), add this line inside the constructor (next to `detection_run_id=run.id,`):

```python
                    detected_db_version=db_version,
```

**(c)** Reset the confirmation window when a finding is re-observed. In the reaffirm branch (around line 150–155), after `dup.detection_run_id = run.id`, add:

```python
                    dup.resolution_miss_count = 0   # re-observed → out of the resolution window
```

**(d)** Run coverage + resolution after the create/reaffirm loop. Replace the block that computes `current` (lines 181–194, from the comment `# Snapshot the live risk set...` through `run.findings_current = int(current or 0)`) with:

```python
        # Coverage ledger + coverage-gated auto-resolution (Phase 0/1). Best-effort:
        # never let resolution failure sink an otherwise-good detection run.
        resolved = 0
        try:
            coverage = build_coverage(result.get("scanner_runs"), facts)
            resolved = await evaluate_resolutions(db, engagement_id, run, coverage, now)
            run.stats = {"coverage": coverage, "auto_resolved": resolved}
        except Exception as exc:  # noqa: BLE001 — resolution must not fail the run
            logger.warning("detection_run.resolution_failed", error=str(exc))
            run.stats = {"coverage": {}, "auto_resolved": 0}

        # Snapshot the live risk set AFTER resolution (auto-resolved findings drop out).
        current = (await db.execute(
            select(func.count()).select_from(Finding).where(
                Finding.engagement_id == engagement_id,
                Finding.status.in_(_CURRENT_STATUSES),
            )
        )).scalar_one()

        run.status = RUN_COMPLETED
        run.finished_at = datetime.now(timezone.utc)
        run.findings_new = created
        run.findings_reaffirmed = reaffirmed
        run.findings_current = int(current or 0)
```

(The `logger.info("detection_run.completed", ...)` line right after stays; optionally add `resolved=resolved` to it.)

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && python -m pytest tests/test_engine_bridge_resolution.py -v`
Expected: PASS.

- [ ] **Step 5: Run the full detection test group to check for regressions**

Run: `cd manager/backend && python -m pytest tests/test_detection_validation.py tests/test_posture.py tests/test_finding_schema.py -v`
Expected: PASS (no regressions from the schema/bridge change).

- [ ] **Step 6: Commit**

```bash
git add manager/backend/app/detection/engine_bridge.py manager/backend/tests/test_engine_bridge_resolution.py
git commit -m "feat(resolution): wire coverage ledger + auto-resolution into detection run"
```

---

### Task 6: Regression reopen (returning finding re-opens the same row)

**Files:**
- Modify: `manager/backend/app/detection/engine_bridge.py` (`create_findings_from_facts` create/reaffirm loop)
- Test: `manager/backend/tests/test_engine_bridge_regression.py`

**Interfaces:**
- Consumes: existing `_find_open_duplicate` (finding_translator) and `Finding`/`FindingStatus`.
- Produces: `_find_remediated_match(db, engagement_id, asset_id, title) -> Finding | None`; behavior — a `remediated` finding whose issue reappears in a covered run is re-opened in place (`status → open`, `reopened_count += 1`, `resolution_miss_count = 0`, `evidence["regression"] = True`) instead of creating a fresh row.

**Rationale:** the probe self-assessed path (`finding_translator`) intentionally lets a returning remediated issue create a *fresh* row. The detection-engine path instead reopens the same finding and flags it, so the dashboard shows a regression on the original finding with its history intact. We keep the two paths separate — this task only changes the engine path.

- [ ] **Step 1: Write the failing test**

Create `manager/backend/tests/test_engine_bridge_regression.py`:

```python
from __future__ import annotations

import uuid
from types import SimpleNamespace

from app.detection.engine_bridge import _apply_regression_reopen
from app.models.enums import FindingStatus


def test_reopen_flips_remediated_to_open_and_flags_regression():
    now = object()
    run_id = uuid.uuid4()
    f = SimpleNamespace(
        status=FindingStatus.remediated, reopened_count=0,
        resolution_miss_count=3, resolved_at="old", resolution_method="auto",
        evidence={"cve_id": "CVE-1"}, last_seen=None, detection_run_id=None,
    )
    _apply_regression_reopen(f, run_id, now)

    assert f.status == FindingStatus.open
    assert f.reopened_count == 1
    assert f.resolution_miss_count == 0
    assert f.resolved_at is None
    assert f.evidence["regression"] is True
    assert f.last_seen is now
    assert f.detection_run_id == run_id
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/backend && python -m pytest tests/test_engine_bridge_regression.py -v`
Expected: FAIL — `ImportError: cannot import name '_apply_regression_reopen'`.

- [ ] **Step 3: Add the reopen helper and use it**

In `manager/backend/app/detection/engine_bridge.py`, add a module-level helper (near the other helpers, above `create_findings_from_facts`):

```python
def _apply_regression_reopen(finding, run_id, now) -> None:
    """A previously-remediated finding whose issue reappeared this run: reopen
    the SAME row and flag it as a regression (history preserved)."""
    finding.status = FindingStatus.open
    finding.reopened_count = (finding.reopened_count or 0) + 1
    finding.resolution_miss_count = 0
    finding.resolved_at = None
    finding.resolution_method = None
    finding.resolution_run_id = None
    finding.last_seen = now
    finding.detection_run_id = run_id
    ev = dict(finding.evidence or {})
    ev["regression"] = True
    finding.evidence = ev
```

Add the query helper (async), next to it:

```python
async def _find_remediated_match(db, engagement_id, asset_id, title):
    """A remediated finding with the same (engagement, asset, title) — the
    regression candidate. Mirrors _find_open_duplicate but for the closed set."""
    from sqlalchemy import select
    q = select(Finding).where(
        Finding.engagement_id == engagement_id,
        Finding.title == title,
        Finding.status == FindingStatus.remediated,
    )
    q = q.where(Finding.asset_id == asset_id) if asset_id else q.where(Finding.asset_id.is_(None))
    return (await db.execute(q.limit(1))).scalar_one_or_none()
```

Then, in the create/reaffirm loop of `create_findings_from_facts`, after the existing `dup = await _find_open_duplicate(...)` block (i.e. when `dup is None`, before `db.add(Finding(...))`), insert:

```python
                regressed = await _find_remediated_match(db, engagement_id, asset_id, title)
                if regressed is not None:
                    _apply_regression_reopen(regressed, run.id, now)
                    regressed.evidence = {**(regressed.evidence or {}), **d, "regression": True}
                    reaffirmed += 1   # counts as a re-touch, not a brand-new finding
                    continue
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/backend && python -m pytest tests/test_engine_bridge_regression.py -v`
Expected: PASS.

- [ ] **Step 5: Run the whole detection-related suite**

Run: `cd manager/backend && python -m pytest tests/test_resolution_coverage.py tests/test_resolution_decision.py tests/test_resolution_apply.py tests/test_engine_bridge_resolution.py tests/test_engine_bridge_regression.py tests/test_finding_resolution_schema.py -v`
Expected: PASS (all).

- [ ] **Step 6: Commit**

```bash
git add manager/backend/app/detection/engine_bridge.py manager/backend/tests/test_engine_bridge_regression.py
git commit -m "feat(resolution): reopen + flag regressions on the original finding row"
```

---

## Self-Review

**1. Spec coverage (against `plan_after_probe.md` §4):**
- Coverage ledger (§4.2) → Task 2 + Task 5(d). ✅
- Coverage-gated auto-resolve + confirmation window (§4.3) → Task 3 + Task 4 + Task 5. ✅
- DB-version guard (§4.1 cause #4, §4.3) → `detected_db_version` (Task 1), stamped (Task 5b), enforced (Task 4). ✅
- Flap reset (§4.3) → `resolution_miss_count = 0` on reaffirm (Task 5c). ✅
- Regression reopen + flag (§4.3) → Task 6. ✅
- Data-model columns (§4.4) → Task 1. ✅ (Deliberately **no** `pending_remediation` enum value — represented by `resolution_miss_count > 0 && status == open`; documented in Global Constraints. `pending_remediation` as an explicit status/label is a dashboard follow-up.)
- Severity-scaled threshold (§4.3) → `resolution_threshold` (Task 3). ✅
- Dashboard visibility (§4.6) → auto-resolution surfaces through the existing `status = remediated` column; the reopen **button** + lifecycle **timeline** are an explicit follow-up UI plan (noted in the header). Partial by design.
- Edge cases (§4.5): host offline / scanner degraded → not covered (Task 2); service moved ports → coverage is asset-keyed (Task 2); DB refreshed → guard (Task 4); accepted/fp untouched → status filter (Task 4); flap → reset (Task 5c); regression → Task 6. ✅

**2. Placeholder scan:** No TBD/TODO; every code step shows complete code and exact commands. ✅

**3. Type consistency:** `build_coverage`/`host_of`/`decide_resolution`/`resolution_threshold`/`ResolutionOutcome`/`evaluate_resolutions` names are identical across Tasks 2–5. `evaluate_resolutions(db, engagement_id, run, coverage, now)` signature matches its call site in Task 5(d). `FindingStatus.remediated` used consistently. `resolution_miss_count`/`detected_db_version`/`reopened_count` column names match model (Task 1), applier (Task 4), and bridge (Tasks 5–6). ✅

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-08-11-coverage-gated-auto-resolution.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints for review.

**Which approach?**
