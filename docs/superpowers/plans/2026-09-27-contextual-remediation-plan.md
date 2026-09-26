# Contextual Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace generic keyword remediation with asset-grounded per-finding plans, deterministic fix bundles (by fix / by host), engagement SLA + customer extension workflow, gateway-routed AI refinement, a backend AI report, and an XLSX/CSV tracker.

**Architecture:** A new pure package `app/remediation/` (context → recipes → plan → bundles) computed live from Finding/Asset/Service rows; persisted overlays only (AI refinements, extension requests, approved due dates). All LLM calls go through `ManagerLlmService` (gateway + audit chain). Frontend consumes the new contracts on findings page, a new Remediation page (operator + portal), the report and an export.

**Tech Stack:** FastAPI + SQLAlchemy async + Alembic (Postgres), pytest (handlers called directly with mocked async db — repo convention), Next.js (App Router, React Query), `openpyxl` (new).

**Spec:** `docs/superpowers/specs/2026-09-27-contextual-remediation-design.md`

## Global Constraints

- Every new LLM caller goes through `ManagerLlmService` (`app/services/llm.py`, gateway in `_dispatch`) and persists `svc.audit_records` via `app.ai.audit_chain.persist_ai_calls`.
- Scan-derived text (banners, hostnames, products) reaches a model only inside `AiGenerateRequest.context` (fenced by `_fence_untrusted`), never in the trusted system text.
- Timestamps are timezone-aware; displayed IST via existing `project_time` helpers.
- Missing facts render the literal `not recorded`; never inferred.
- CIS/benchmark references by section name only; no invented control numbers.
- Recipes' commands are hand-authored and non-destructive.
- `app/services/remediation_kb.py` stays (compliance/content use `classify_finding`); routes stop serving it.
- Probe scanner trees (`scanner/`, `main_scripts/`) untouched; `manager/detection_engine` change limited to additive `fixed_version`.
- Shared checkout: stage explicit paths only; never upgrade the shared `.venv` (install `openpyxl` only after confirming with a dry run; if the shared venv would change other packages, stop and use an isolated venv).
- One migration: `0048` (revises `0047`).
- Backend tests: `cd manager/backend && .venv/bin/python -m pytest tests/<file> -q`. Detection engine tests: `cd manager/detection_engine && ../backend/.venv/bin/python -m pytest tests/<file> -q`.

---

## Phase 1 — Asset-grounded plans (pure core)

### Task 1: Structured `fixed_version` from the matcher

**Files:**
- Modify: `manager/detection_engine/matcher.py` (`_version_in_ranges`, `match_candidate`)
- Modify: `manager/detection_engine/models.py` (`Finding.fixed_version: str | None = None`)
- Test: `manager/detection_engine/tests/test_detection_core.py`

**Interfaces:** Produces `_fixed_bound(interval: str | None) -> str | None` and `Finding.fixed_version`. `_version_in_ranges` signature unchanged (keeps 13 existing call sites).

- [ ] Step 1: failing tests

```python
from matcher import _fixed_bound

class TestFixedBound:
    def test_half_open_interval_yields_fixed(self):
        assert _fixed_bound("[1.0, 2.4.50)") == "2.4.50"
    def test_last_affected_has_no_fixed(self):
        assert _fixed_bound("[1.0, 2.4.49]") is None
    def test_unbounded_has_no_fixed(self):
        assert _fixed_bound("[1.0, unbounded)") is None
    def test_none(self):
        assert _fixed_bound(None) is None
```
And in the `match_candidate` test class: a finding matched on `[introduced, fixed)` carries `fixed_version == fixed`.

- [ ] Step 2: run → FAIL (ImportError)
- [ ] Step 3: implement

```python
def _fixed_bound(interval: str | None) -> str | None:
    """The first non-vulnerable version of a matched `[introduced, fixed)` interval.
    `last_affected` (closed `]`) and unbounded intervals have no fixed release."""
    if not interval or not interval.endswith(")"):
        return None
    hi = interval[1:-1].split(",", 1)[-1].strip()
    return None if hi in ("", "unbounded") else hi
```
Pass `fixed_version=_fixed_bound(interval)` in `Finding(...)`; add field `fixed_version: str | None = None` after `matched_version` docs block (dataclass default → append at the end of optional fields).
- [ ] Step 4: run detection_engine tests → PASS
- [ ] Step 5: commit `feat(detection): carry structured fixed_version on CVE matches`

### Task 2: Remediation context (`app/remediation/context.py`)

**Files:** Create `manager/backend/app/remediation/__init__.py`, `context.py`; Test `tests/test_remediation_context.py`

**Interfaces — Produces:**
```python
@dataclass(frozen=True)
class Fact: value: Any; source: str   # "scan" | "asset_record" | "not_recorded"

@dataclass(frozen=True)
class RemediationContext:
    host: Fact; ip: Fact; fqdn: Fact; os: Fact; os_version: Fact
    os_family: str                  # linux|windows|macos|network|unknown
    port: Fact; protocol: Fact; service_name: Fact; product: Fact; version: Fact
    cpe: Fact; banner_excerpt: Fact
    exposure: str                   # internet|internal|unknown
    criticality: Fact; environment: Fact; tags: tuple[str, ...]
    fragile: bool; fragile_reason: str | None
    kev: bool; epss: float | None; exploit_validated: bool
    rule_id: str | None; cve_ids: tuple[str, ...]
    fixed_version: str | None; scanner: str | None; category: str | None
    def text(self, name: str) -> str   # value or "not recorded"
    def facts_used(self) -> list[str]  # names whose source != not_recorded

def build_context(finding, asset=None, service=None) -> RemediationContext
def pick_service(finding, services: list) -> Service | None   # match by port from evidence
def evidence_port(finding) -> int | None
```
Rules: `rule_id` = `evidence["rule_id"]`; port = `evidence["port"]` or `evidence["evidence"]["port"]`; exposure from `service.exposure` (`external`→internet, `internal_only`/`not_exposed`→internal), else `evidence["internet_facing"]` bool, else asset environment keywords, else unknown; `os_family` from asset.os/os_version keywords (windows/linux-distros/mac/darwin; asset_type network/printer/iot → network); fragile via `app.intel.fragile` public helper; `banner_excerpt` truncated to 200 chars; `kev` from `evidence.get("kev")`/`kev_listed`; `fixed_version` from `evidence["fixed_version"]`.

- [ ] Step 1: failing tests (SimpleNamespace finding/asset/service):
  - facts from service marked `scan`, asset fields `asset_record`, absent → `not_recorded` and `ctx.text("version") == "not recorded"`
  - exposure mapping for each `Service.exposure` value + fallback to `internet_facing`
  - os_family for "Windows Server 2012 R2", "Ubuntu 22.04", "Darwin", asset_type "printer"
  - `pick_service` picks the service whose port equals evidence port
  - banner longer than 200 chars truncated
- [ ] Step 2: run → FAIL
- [ ] Step 3: implement
- [ ] Step 4: run → PASS
- [ ] Step 5: commit `feat(remediation): asset-grounded remediation context`

### Task 3: Recipe catalogue (`app/remediation/recipes.py`)

**Files:** Create `app/remediation/recipes.py`; Test `tests/test_remediation_recipes.py`

**Interfaces — Produces:**
```python
REMEDIATION_TYPES = ("vendor_fix","workaround","mitigation","none_available","no_fix_planned")
RISK_RESPONSES = ("mitigate","avoid","transfer","accept")
TIERS = ("containment","fix","hardening")

@dataclass(frozen=True)
class Step:
    tier: str; title: str; description: str          # description may use {host} {ip} {port} {product} {version} {os} {fixed_version} {target}
    commands: dict[str, tuple[str, ...]]            # keys: linux|windows|macos|network|generic
    pre_checks: tuple[str, ...] = (); reboot_required: bool | None = None
    downtime: str = "none expected"; rollback: str = ""; risk: str = "low"

@dataclass(frozen=True)
class Verification:
    scanner: str; check: str; expected: str; manual: dict[str, str]

@dataclass(frozen=True)
class Recipe:
    recipe_id: str; version: int; title: str; remediation_type: str; risk_response: str
    target_state: str                               # template, e.g. "{product} ≥ {fixed_version}"
    steps: tuple[Step, ...]; compensating_controls: str; verification: Verification
    references: tuple[str, ...] = (); effort: str = "medium"; long_term: tuple[str, ...] = ()

RECIPES: dict[str, Recipe]
def resolve_recipe(ctx: RemediationContext, finding) -> Recipe
```
Keys: the 29 posture rule IDs; `POSTURE-EXPOSED-{BACKDOOR,CONTAINER,DATASTORE,DATABASE,CLEARTEXT,REMOTE_ACCESS,ADMIN_UI}`; `CVE-PATCH`; `GENERIC`; legacy keyword categories map (`weak_tls`→`POSTURE-TLS-DEPRECATED-VERSION`, `smb_signing`→`POSTURE-SMB-SIGNING-OFF`, `exposed_rdp`→`POSTURE-RDP-EXPOSED`, `default_credentials`→`POSTURE-DEFAULT-CRED-CANDIDATE`, `missing_patch`→`CVE-PATCH`, `open_mgmt_port`→`POSTURE-EXPOSED-REMOTE_ACCESS`, `anon_ftp`→`POSTURE-FTP-ANONYMOUS-LOGIN`, `outdated_ssh`→`POSTURE-SSH-WEAK-ALGORITHMS`).
Resolution: `ctx.rule_id in RECIPES` → rule; CVE ids present → `CVE-PATCH`; `remediation_kb.classify_finding` legacy map → mapped; else `GENERIC`. Every recipe has ≥1 `fix` step, a verification naming the posture rule's scanner (from `posture_rules.RULES`), and content derived from the rule's own remediation sentence.

- [ ] Step 1: failing tests
```python
from detection_engine.posture_rules import RULES   # via sys.path as other backend tests do
from detection_engine.port_intel import PORT_RISKS  # or the catalogue's category set

def test_every_posture_rule_has_a_recipe():
    missing = [r.rule_id for r in RULES if r.rule_id not in recipes.RECIPES]
    assert missing == []

def test_every_exposed_category_has_a_recipe():
    cats = {risk.category for risk in port_intel_catalogue()}
    missing = [c for c in cats if f"POSTURE-EXPOSED-{c.upper()}" not in recipes.RECIPES]
    assert missing == []

def test_recipes_are_well_formed():
    for rid, r in recipes.RECIPES.items():
        assert r.remediation_type in recipes.REMEDIATION_TYPES, rid
        assert r.risk_response in recipes.RISK_RESPONSES, rid
        assert any(s.tier == "fix" for s in r.steps), rid
        assert all(s.tier in recipes.TIERS for s in r.steps), rid
        assert r.verification.expected, rid

def test_no_destructive_commands():
    guard = HallucinationGuard()
    for r in recipes.RECIPES.values():
        for s in r.steps:
            for cmds in s.commands.values():
                for c in cmds:
                    assert guard.validate_remediation_commands(c)["valid"], (r.recipe_id, c)

def test_scanner_matches_rule():
    by_id = {r.rule_id: r for r in RULES}
    for rid, rule in by_id.items():
        assert recipes.RECIPES[rid].verification.scanner in rule.scanners

def test_resolution_order(): rule_id wins; CVE → CVE-PATCH; keyword legacy map; else GENERIC
```
- [ ] Step 2: run → FAIL
- [ ] Step 3: implement all recipes
- [ ] Step 4: run → PASS
- [ ] Step 5: commit `feat(remediation): rule-keyed recipe catalogue covering every posture rule`

### Task 4: Plan builder (`app/remediation/plan.py`)

**Files:** Create `app/remediation/plan.py`; Test `tests/test_remediation_plan.py`

**Interfaces — Produces:**
```python
def urgency_for(ctx: RemediationContext, severity: str) -> dict   # {"label": act|attend|track_star|track, "drivers": [str]}
def target_state_for(recipe, ctx) -> str
def build_plan(finding, ctx: RemediationContext, *, due: dict | None = None,
               os: str | None = None) -> dict
```
Plan dict keys (superset of old contract): `category` (= recipe_id), `recipe_id`, `recipe_version`, `os` (selected), `os_auto` (ctx.os_family mapped to linux|windows|macos|generic), `source: "kb"`… keep `"deterministic_kb"` for back-compat in `source`; `summary`, `effort`, `remediation_risk`, `remediation_type`, `risk_response`, `target_state`, `urgency`, `due` (`{"at": iso|None, "source": str|None}`), `context` (`{name: {"value", "source"}}`), `steps` (each: `step`, `tier`, `title`, `description`, `commands`, `commands_for_os`, `pre_checks`, `reboot_required`, `downtime`, `rollback`, `risk`, `verification`), `verification` (list[str] for back-compat) + `verification_check` (`{"scanner","check","expected","manual_command"}`), `long_term_recommendations`, `compensating_controls`, `references`, `fragile_guard` (`{"active": bool, "reason": str|None}`), `provenance` (`{"source":"kb","recipe_id","recipe_version","facts_used","generated_at"}`).
Templating: `str.format_map` with a `_SafeDict` returning `not recorded` for missing keys; `{target}` = target state. Fragile: prefix every step description with "Coordinate with the asset owner — no automated change on this fragile asset." and set `fragile_guard.active`. Urgency (SSVC-shaped, informational): exploitation = active if kev, poc if epss≥0.5 or exploit_validated, else none; automatable = exposure internet; impact = total if severity critical else partial; mission = criticality high/critical→high, medium→medium else low; label table: active∧automatable∧(total∨mission high)→act; active→attend; poc∧mission high→attend; poc∧total∧automatable→track_star; else track.

- [ ] Step 1: failing tests: SMBv1 example (context filled, `commands_for_os` windows auto, target "SMBv1 disabled…"), CVE with fixed_version → "`{product} ≥ 9.8p1`", CVE without fixed_version → contains "confirm fixed version", missing facts render "not recorded", fragile prefix, urgency table rows (kev+internet+critical → act; nothing → track), back-compat keys present.
- [ ] Step 2: FAIL → Step 3 implement → Step 4 PASS
- [ ] Step 5: commit `feat(remediation): contextual plan builder with SSVC urgency and fragile guard`

### Task 5: Serve v2 plans on operator + portal GET

**Files:** Create `app/remediation/loader.py`; Modify `app/routers/remediation.py`, `app/routers/portal.py` (`portal_finding_remediation`); Modify `app/schemas/remediation.py` if the response model restricts plan keys; Tests: extend `tests/test_remediation_routes.py`, `tests/test_portal_remediation.py`.

**Interfaces — Produces:**
```python
async def load_finding_context(db, finding) -> tuple[RemediationContext, dict]  # (ctx, due) — loads Asset + its Services (2 queries) and due via deadlines resolver (Task 9; until then due=None)
def kb_plan(finding, ctx, *, due, os) -> dict   # = plan.build_plan
```
GET miss path returns `build_plan(...)` instead of `recipe_for_finding`. Cached AI rows unchanged here (Task 11 adds overlay/stale).
- [ ] Steps: failing route tests (KB miss returns `recipe_id`, `context`, `verification_check`) → implement → pass → commit `feat(remediation): serve asset-grounded plans on operator and portal routes`

---

## Phase 2 — Fix bundles

### Task 6: Bundle engine (`app/remediation/bundles.py`)

**Interfaces — Produces:**
```python
def product_family(ctx) -> str            # normalized product or service or rule family; mirrors group_key_for signature
def fix_key_for(recipe_id: str, family: str, target_state: str) -> str   # sha256(...)[:12]
def fix_ref(fix_key: str) -> str          # "FIX-" + fix_key[:6].upper()
@dataclass
class Member: finding_id: str; title: str; severity: str; status: str; host: str; ip: str; os: str; port: int|None; due_at: datetime|None; due_source: str|None; closed_at: datetime|None; excluded_reason: str|None
def build_bundles(items: list[tuple[finding, RemediationContext, dict]], *, now) -> list[dict]
def by_host(bundles: list[dict]) -> list[dict]
```
Bundle dict: `fix_key, ref, recipe_id, title, remediation_type, target_state, steps_by_os {os_family: steps}, hosts [{host, ip, os, port, finding_ids, status}], resolves [finding ids], open_count, closed_count, excluded [{finding_id, reason}], due_at, due_source, urgency (max), progress {closed,total}, status open|done`. Order: due asc (None last), then len(resolves) desc. Status: open/confirmed → open; remediated → closed; accepted/fp → excluded with reason.
- [ ] Tests: same inputs → same key; banner casing does not split; nginx vs IIS split; earliest due; excluded counted; single-member generic; by_host pivot; done status.
- [ ] Commit `feat(remediation): deterministic fix bundles with by-fix and by-host views`

### Task 7: Engagement loader + bundle routes

**Files:** Modify `app/remediation/loader.py` (`load_engagement_items(db, engagement) -> list[tuple]` — findings, assets, services in 3 queries); Modify `app/routers/remediation.py` (`GET /engagements/{id}/remediation/bundles?view=fix|host`) — new router prefix `/engagements` inside the same module (`bundles_router`) registered in `main.py`; Portal `GET /portal/remediation/bundles?view=`.
- [ ] Tests: tenant scoping 404, view=host pivot, one execute per table (count db.execute calls = 4 incl. engagement).
- [ ] Commit `feat(remediation): engagement bundle endpoints (operator + portal)`

---

## Phase 3 — Deadlines & extensions

### Task 8: Migration 0048 + models

**Files:** Create `alembic/versions/0048_contextual_remediation.py`, `app/models/deadline_extension.py`; Modify `app/models/finding.py` (`due_at`, `due_at_source`), `app/models/remediation_plan.py` (`subject_type`, `fix_key`, `facts_fingerprint`, nullable `finding_id`), `app/models/__init__.py`, `app/models/enums.py` (event types `extension_requested|extension_approved|extension_rejected|extension_withdrawn`), `app/services/finding_events.py` labels.
DDL as spec §5; partial unique index `uq_remediation_bundle_os` on `(engagement_id, fix_key, os) WHERE subject_type='bundle'`; replace `uq_remediation_finding_os` constraint with partial unique index on `(finding_id, os) WHERE subject_type='finding'` — **keep constraint name usable by `on_conflict_do_update`**: use `index_elements=["finding_id","os"], index_where=...` in the upsert instead of `constraint=`.
- [ ] Tests: model columns exist; upsert statement compiles with `index_where` (update `test_remediation_routes` upsert SQL assertions).
- [ ] Commit `feat(db): 0048 due dates, extension requests, bundle-capable remediation plans`

### Task 9: Deadline resolver + engagement SLA policy

**Files:** Create `app/services/deadlines.py`; Modify `app/services/sla.py` (`compute` honours `finding.due_at`; `summarize(..., engagement_windows=None)`), `app/routers/findings.py` sla-summary passes engagement windows; add `GET/PUT /engagements/{id}/sla-policy` in `app/routers/sla_policy.py` (`engagement_router`).

**Interfaces — Produces:**
```python
def engagement_windows(engagement) -> dict[str,int] | None   # rules_of_engagement["sla_policy"] → {critical..info}
async def windows_for(db, tenant_id, engagement) -> tuple[dict[str,int], str]   # (windows, "engagement"|"tenant"|"default")
def due_for(finding, windows, source) -> dict   # {"at": datetime|None, "source": "extension"|source|None}
```
- [ ] Tests: precedence extension > engagement > tenant > default; invalid RoE policy ignored; `sla.compute` uses due_at; PUT validates 0..8760; portal cannot PUT (403 via role).
- [ ] Commit `feat(sla): per-engagement SLA policy and single due-date resolver`

### Task 10: Extension request workflow

**Files:** Create `app/services/extensions.py`, `app/schemas/extension.py`, `app/routers/extensions.py` (operator: `GET /engagements/{id}/extensions`, `POST /extensions/{id}/approve`, `POST /extensions/{id}/reject`); portal routes in `app/routers/portal.py` (`GET /portal/extensions`, `POST /portal/extensions`, `POST /portal/extensions/{id}/withdraw`); register router in `main.py`.

**Interfaces — Produces:**
```python
async def create_request(db, *, engagement, user, subject_type, finding_id, fix_key, requested_due_at, reason, compensating_control) -> DeadlineExtensionRequest
async def decide(db, *, request, operator, approve: bool, decided_due_at: datetime|None, note: str) -> DeadlineExtensionRequest
async def withdraw(db, *, request, user) -> DeadlineExtensionRequest
```
Validation: subject resolves inside engagement (404 otherwise); open members only; `requested_due_at` > current max due of members (422); compensating control required if any member critical/high or KEV (422); one pending per subject (409); note required on decide (422); only pending can be decided/withdrawn (409). Approve sets `due_at`/`due_at_source='extension'` on each open member; events on every member; `record_audit`.
- [ ] Tests for every rule + IDOR (client of another engagement → 404) + events recorded.
- [ ] Commit `feat(remediation): customer deadline extension requests with operator approval`

---

## Phase 4 — AI refinement

### Task 11: Gateway-routed refinement (finding + bundle)

**Files:** Create `app/remediation/ai_refine.py`; Modify `app/schemas/ai.py` (task literal `remediation_refine`, `engagement_report`), `app/services/llm.py` (`_TASK_RULES["remediation_refine"]`, `_TASK_RULES["engagement_report"]`), `app/routers/remediation.py` (`POST /findings/{id}/remediation/refine`, `/generate` alias; `POST /engagements/{id}/remediation/bundles/{fix_key}/refine`; GET returns overlay + `stale`).

**Interfaces — Produces:**
```python
def facts_fingerprint(ctx_or_contexts) -> str
def overlay(kb_plan: dict, ai: dict, *, allowed_cves: set[str], allowed_versions: set[str], guard) -> tuple[dict, list[dict]]   # (merged, ai_changes)
async def refine(db, *, engagement, kb_plan: dict, context_payload: dict, actor_id) -> dict   # uses ManagerLlmService.generate_with_fallback, persists audit
```
AI may set: per-step `description`, `commands` (for the selected OS), `pre_checks`, `rollback`, plus `sequencing_rationale`, `summary`, `target_state` (labelled when not confirmed). Strip unknown CVE/version tokens (`CVE-\d{4}-\d+`, version-looking tokens not in `allowed_versions` inside target_state → label "AI-suggested — verify against the vendor advisory"). Unsafe commands dropped + `unsafe_commands_removed`. Stored `plan` = merged; `plan["ai_changes"]`; `facts_fingerprint` column. GET: if cached row fingerprint != live → `stale: true`.
- [ ] Tests: overlay keeps KB fields the model omitted; unknown CVE stripped; unsafe command dropped; unconfirmed version labelled; stale detection; refine persists audit records (fake svc); AI unavailable → 503 and nothing cached; sovereign w/o model → `AiRuntimeError 503` surfaced.
- [ ] Commit `feat(remediation): gateway-routed AI refinement overlay for findings and bundles`

---

## Phase 5 — Backend AI report

### Task 12: Engagement AI report job on the backend

**Files:** Create `app/ai/engagement_report.py` (scorecard + prompt + validation ported from `frontend/lib/prompts/report.ts`), route `POST /engagements/{id}/ai-report/roadmap` (sync, bounded) in `app/routers/ai_report.py` or a new `app/routers/engagement_report.py`; Modify `frontend/app/api/reports/generate/route.ts` → proxy to backend; remove report-generation use of `callAnthropicWithRetry`/SDK in `frontend/lib/ai-engine.ts`.
Deterministic: scorecard, exposure matrix, `remediation_plan` = bundles (refs `FIX-xxxxxx`, windows from due dates: due ≤ 7d → immediate, ≤ 30d → 30_days, else 90_days). LLM writes: verdict, decisions, executive_summary, attack_narrative, per-finding narrative fields, per-bundle `description`/`verification` narrative, controls_observed, limitations. Validation: every FIX/finding ref in the output exists in the input; otherwise 422 with the failed check.
- [ ] Tests: scorecard parity on a fixture; validation rejects invented refs; audit persisted; response matches the `ReportResult` shape the page renders.
- [ ] Commit `feat(ai): backend engagement report with deterministic roadmap; remove direct Anthropic path`

---

## Phase 6 — Surfaces

### Task 13: Findings page plan view v2 + extension panel
Files: `manager/frontend/app/findings/page.tsx` (RemediationPlanView), `lib/findings-workspace-api.ts` (`refineRemediation`, `publishRemediation`, `extensions`), CSS in `app/globals.css`. Render context card, tiers, verification check, bundle link, Refine with AI (operator), AI diff toggle, stale badge, Approve for customer; operator extension decisions; portal request form.

### Task 14: Remediation page (operator + portal)
Files: `app/remediation/page.tsx` (operator), `app/portal/remediation/page.tsx`, BFF routes `app/api/engagements/[id]/remediation/bundles/route.ts`, `app/api/portal/...` via existing portal proxy; nav entries. By fix / by host toggle; checklist; due + source; extension request (portal).

### Task 15: Report integration
Files: `components/report/FindingReport.tsx` (Remediation section renders plan from bundle data), `app/reports/page.tsx` (roadmap from bundles + backend AI report), `lib/report/finding-model.ts` (stop `SLA_DAYS` dates; use backend due), fix compliance object rendering.

### Task 16: XLSX/CSV tracker export
Files: `app/remediation/export.py`, route `GET /engagements/{id}/remediation/export?format=xlsx|csv` (+ portal), `requirements.txt` (+`openpyxl`), BFF route + buttons. Tests: workbook has 3 sheets, header frozen, dates typed; CSV zip has 3 files.

### Task 17: Verification & wrap-up
Full `pytest tests/` (backend) + detection_engine tests; `npx tsc --noEmit`, `npm run lint`; browser preview of findings page / Remediation page / portal / report; `graphify update .`; memory note.
