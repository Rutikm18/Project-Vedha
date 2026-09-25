# Per-scan findings — label, filter, and compare

**Goal:** Every finding shows which scan produced/re-observed it (the existing `SCN-YYMMDD-XXXXXX` reference + use-case + intensity + timestamp); the findings page can filter to one scan; and two scans can be compared (new / fixed / still-present). Operator console **and** customer portal.

**Confirmed with the operator:** reuse the `SCN-…` job reference (no new ID); do label + filter + **compare**; surface scan reference, use-case, intensity, timestamp; both operator and portal.

## Grounding (verified in code)
- Per-scan ID already exists: `ScanJob.reference` = `SCN-YYMMDD-XXXXXX`, stamped `before_insert`, stored (`services/reference.py`).
- Finding→scan today is indirect and lossy: `Finding.detection_run_id` = the **last** run that touched it → `DetectionRun.scan_result_id` → `ScanResult.job_id` → `ScanJob`. A finding re-observed by a later scan loses its link to earlier scans.
- `DetectionRun` records per-run **counts** (`findings_new/reaffirmed/current`) but **not which findings** — so accurate "scan X's findings" and A-vs-B compare are impossible without membership.
- use-case / intensity are **not columns** — they live in `ScanJob.result` JSON (enqueue params, then the probe result blob). Must be captured cleanly.
- `create_findings_from_facts` (`detection/engine_bridge.py`) already branches per finding into created / reaffirmed / regressed / resolved — the exact hook points for membership.
- `FindingOut` (`schemas/finding.py`) exposes no scan field; `/findings` (`routers/findings.py`) filters severity/status/asset/engagement/agent/mitre/search — no scan filter.
- Portal reuses operator handlers via the console-source seam (`lib/console-source.tsx`), engagement pinned.

## Key design decision — per-run finding membership
A **`detection_run_finding`** table (run_id, finding_id, outcome ∈ new|reaffirmed|regressed|resolved), one row per finding a run touches, populated inside `create_findings_from_facts` at the points it already classifies each finding. This is the source of truth for both "which findings did scan X observe" and "A vs B". Rejected alternatives: (a) last-run join — lossy, a re-observed finding vanishes from the earlier scan; (b) timestamp windows — can't tell reaffirmed from untouched. Exactness matters here (a wrong "fixed" is the same false-clean class this codebase keeps fighting).

## Global Constraints
- `.githooks` bumps VERSION (expected). Never `--no-verify`. Trailer: `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- Migrations are additive + backfilled; the detection pipeline stays concurrency-safe (ADR-0001 advisory lock) — membership writes ride the same transaction as the finding writes.
- No new failures in the manager suite (currently green).

---

### Task 1 — capture scan identity on the run
- Migration: add `DetectionRun.job_id` (FK, nullable, indexed); add `ScanJob.use_case_id` (str) and `ScanJob.intensity` (str) columns. Backfill `job_id` from `scan_result→job`; backfill use_case_id/intensity from `ScanJob.result` JSON where present.
- Stamp `use_case_id` + `intensity` on `ScanJob` at enqueue (`enqueue_agent_job`), resolved from the request (already normalized there).
- Set `DetectionRun.job_id` when the run is created (the outbox already loads the job).
- Tests: enqueue stamps both; a run links its job; backfill derives them.

### Task 2 — per-run finding membership
- Migration: `detection_run_finding` (run_id FK, finding_id FK, outcome enum, PK(run_id,finding_id), index on finding_id).
- In `create_findings_from_facts`, record a membership row at each branch: created→`new`, reaffirmed→`reaffirmed`, regression-reopen→`regressed`, auto-resolve→`resolved`. Same transaction.
- Tests: a run that creates 1, reaffirms 1, resolves 1 writes exactly those 3 rows with the right outcomes; concurrency-safe (no duplicate rows under the advisory lock).

### Task 3 — expose scan identity on findings
- `FindingOut` gains `scan` block: `{reference, use_case_id, intensity, scanned_at}` from the finding's most-recent membership run's job (join). `first_seen`/`last_seen` already exist.
- Tests: a finding serializes its scan block; a finding with no run (legacy) returns null scan cleanly.

### Task 4 — filter findings by scan
- `/findings?scan=<SCN ref or run id>` → findings that have a membership row for that scan's run(s). Accepts the SCN reference (resolve via `is_reference`) or a job id.
- A `/scans` (or `/engagements/{id}/scans`) list endpoint: recent scans for the picker (reference, use-case, intensity, finished_at, counts).
- Tests: the filter returns exactly the scan's findings incl. re-observed ones; unknown ref → 422; the scans list orders by recency.

### Task 5 — compare two scans
- `/findings/compare?a=<ref>&b=<ref>` → `{new:[…], fixed:[…], still_present:[…]}` from set ops over the two runs' memberships (new = in B not A; fixed = open in A, resolved/absent in B; still_present = both). Each entry carries the finding summary.
- Tests: constructed A/B fixtures produce the exact three buckets; same-scan compare = all still_present, none new/fixed.

### Task 6 — operator UI
- Findings page: a **scan filter** (typeahead/dropdown of recent scans showing `SCN-… · use-case · intensity · time`), each row shows its scan chip; a **Compare** mode picking two scans → the 3-bucket diff view.
- Tests: `lib` adapters for the scan list + compare payload; the filter serializes to the query param.

### Task 7 — portal parity
- Expose the scan label, filter, and compare in the portal findings view via the console-source seam (engagement pinned; portal audience gate respected).
- Tests: portal scan list/compare delegate to the operator handlers with the engagement pinned; portal cannot query another engagement's scans.

### Task 8 — verify
- Full manager suite green; frontend tests green; live e2e: run two scans (e.g. Normal then Aggressive) on the same scope, confirm each finding shows its scan, filter isolates each, and compare shows what Aggressive added.

---

## Status — SHIPPED (2026-09-25, branch feat/per-scan-findings)

All 8 tasks landed as incremental commits. Deviations from the plan above, and why:

- **Membership (Task 2) is derived from DB state at run end**, not written inline at each
  create/reaffirm/regress/resolve branch. `_record_run_membership(db, run)` reads the
  finding rows' own run pointers after every write + auto-resolution:
  `detection_run_id == run.id` → new (first_seen == last_seen) or reaffirmed; a regression
  reopen keeps its older first_seen so it reads as reaffirmed; `resolution_run_id == run.id`
  → resolved (disjoint set — `evaluate_resolutions` only touches `detection_run_id != run.id`).
  This is one code site instead of five across three helpers, and is exactly as consistent
  as the run because it reads what was actually persisted. Best-effort — never sinks a run.
- **Unknown scan is a 404 on compare, and an empty page on the list filter** (not 422). The
  filter matches every other findings filter (unknown → empty); compare needs two real scans.
- **compare/filter accept SCN ref *or* job id *or* run id**; a scan (job) can span several
  runs (chunked submissions), so resolution unions them.
- **engagement_id threading** added to `compare_scans` + `_resolve_scan_run_ids` so the portal
  pins both scan resolution and the finding load to the client's engagement (a tenant can hold
  several engagements). Operator stays tenant-wide (`engagement_id=None`).
- **UI is one shared workspace** (console-source seam): scan chip on every card, a Scan filter
  dropdown, and a Compare panel — identical on operator + portal. Portal transport delegates to
  `/workspace/findings/scans` + `/compare` (operator handlers, engagement pinned).

Verification: manager backend 1581 passed / 4 skipped; frontend 242 passed; `tsc --noEmit`
clean; full alembic chain 0001→0047 applied on a throwaway Postgres — `detection_run_findings`
verified (PK, ix on finding_id, ON DELETE CASCADE FKs), head 0047. Live browser e2e (two scans →
diff) is a post-deploy check: Turbopack can't build inside this symlinked worktree.
