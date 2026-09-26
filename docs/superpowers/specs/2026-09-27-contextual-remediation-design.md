# Contextual Remediation Plans, Fix Bundles & Backend AI Report — Design

- **Date:** 2026-09-27
- **Status:** Approved in brainstorming; awaiting written-spec review
- **Branch:** `feat/contextual-remediation`
- **Related memories/docs:** vedha-ai-pipeline, vedha-tags-domain-ai-bfsi (gateway + audit chain rules),
  vedha-console-parity-seam, vedha-reports-settings-v2, vedha-per-scan-findings

## 1. Problem

Remediation guidance today is generic and not grounded in what the scan saw.

| # | Defect (verified in code) | Location |
|---|---|---|
| D1 | KB has 8 categories + `generic`, chosen by keyword match; most of the 29 posture rules and every exposed-service detection fall to "restrict and harden the service". | `manager/backend/app/services/remediation_kb.py` |
| D2 | KB ignores asset/service facts (product, version, port, banner, detected OS, exposure, criticality, fragile flag). OS is a UI dropdown, not the detected OS. | same |
| D3 | No fixed-version target, advisory link, benchmark reference, remediation type, change-management data (reboot, rollback, pre-checks). | same |
| D4 | Verification is generic ("a follow-up scan no longer reports the finding"), not the scanner check that proves closure. | same |
| D5 | AI plan prompt carries only title/severity/CVSS/EPSS/CVE/description. | `manager/backend/app/ai/llm_report.py:375` |
| D6 | The whole AI report (incl. fix-grouped roadmap) calls Anthropic directly from Next.js — bypasses the AI gateway (hybrid pseudonymisation / sovereign), the AI audit chain and the domain brief; model hard-coded `claude-sonnet-4-20250514`. The LLM also invents the FIX grouping and time windows. | `manager/frontend/lib/ai-engine.ts:171`, `app/api/reports/generate/route.ts` |
| D7 | Per-finding plans never reach the report (report prints only the `remediation` text column). | `manager/frontend/app/reports/page.tsx`, `components/report/FindingReport.tsx` |
| D8 | Three disagreeing deadline sources: backend tenant SLA by severity (24h/72h/7d/30d), frontend report `SLA_DAYS` by priority (P0 3d … P3 90d), LLM roadmap windows (immediate/30/90). No per-finding due date column exists. | `app/services/sla.py`, `lib/report/finding-model.ts:442`, `lib/prompts/report.ts` |

## 2. Standards the design follows

| Source | Used for |
|---|---|
| NIST SP 800-40 Rev.4 — Guide to Enterprise Patch Management Planning | Risk response per plan: mitigate / avoid / transfer / accept; unpatchable-asset handling |
| OASIS CSAF 2.0 §3.2.3.12 remediation category | Remediation type enum: `vendor_fix`, `workaround`, `mitigation`, `none_available`, `no_fix_planned` |
| CISA SSVC (Track / Track\* / Attend / Act) | Informational urgency note derived from exploitation, automatable, impact, mission |
| SEBI CSCRF FAQ (Jun 2025), PR.MA.S3 | High-severity patch findings 1 week; other VAPT observations 3 months graded; "reason for non-closure" and "planned closure date" fields |
| CISA BOD 19-02, PCI DSS 4.0 Req 6.3.3 | Reference deadlines (informational; the configured SLA is authoritative) |

## 3. Decisions (from brainstorming)

1. Context = **asset facts** + **cross-finding bundling**. (Regulatory wording and customer tooling/change windows are out of scope.)
2. **KB is the floor, AI refines on top**, always grounded on the KB plan, behind the existing review gate.
3. **Whole AI report generation moves to the backend**; the Next.js direct-Anthropic path is deleted.
4. Deadlines: **per-engagement SLA policy** + **customer-requested extensions approved by an operator**. Tenant policy remains the fallback. Operators cannot set a date directly except by approving (optionally with a different date).
5. Bundles by fix, with **both by-fix and by-host views**.
6. AI runs **on demand** (operator click) and **at report-generation time** only.
7. Surfaces: **findings page, report, customer portal, XLSX + CSV tracker**.
8. Storage: **derive plans/bundles live; persist only overlays** (AI refinements, reviews, extension requests, approved due dates).

## 4. Architecture

```
Finding + Asset + Service ──► remediation/context.py   (fact extraction, "not recorded" when absent)
                                 │
                                 ▼
                         remediation/recipes/          (one recipe per rule_id / CVE class / port category)
                                 │
                                 ▼
                         remediation/plan.py           build_plan(finding, ctx) → Plan   (pure)
                                 │
                 ┌───────────────┼─────────────────────┐
                 ▼               ▼                     ▼
      remediation/bundles.py   services/deadlines.py   remediation/ai_refine.py
      fix_key, by-fix/by-host  due-date resolution      gateway + audit chain + overlay
                 │               │                     │
                 └──────► routers/remediation.py (+ portal delegation) ◄───────┘
                                 │
                 findings page · Remediation page · report · portal · XLSX/CSV export
```

New backend package `manager/backend/app/remediation/` holds the pure parts (context, recipes, plan, bundles). IO stays in routers/services. `services/remediation_kb.py` becomes a thin compatibility shim over the new package and is deleted once no caller remains.

### 4.1 Context extraction (`remediation/context.py`)

`build_context(finding, asset, services) -> RemediationContext` — pure. Fields: host, ip, fqdn, os, os_version, os_family (`linux|windows|macos|network|unknown`), port, protocol, service_name, product, version, cpe, banner_excerpt (truncated, 200 chars), exposure (`internet|internal|unknown`; from `Service.exposure`: `external`→internet, `internal_only`/`not_exposed`→internal, `ambiguous`/null→ fall back to asset environment, else unknown), criticality, environment, tags, fragile (from `app/intel/fragile.py`), kev, epss, exploit_validated, rule_id (from `finding.evidence["rule_id"]`), cve_ids. Each fact carries provenance `scan|asset_record|not_recorded`. Nothing is inferred beyond existing helpers.

The finding's service is matched by (asset_id, port from evidence). Bulk callers (bundles, export, report) load assets and services for the engagement in **one query each** — no N+1 (see vedha-backend-perf-async).

### 4.2 Recipes (`remediation/recipes/`)

A recipe is keyed by one of:

- **posture `rule_id`** — all 29 rules in `manager/detection_engine/posture_rules.py` (`POSTURE-SMB-V1-ENABLED`, `POSTURE-SMB-SIGNING-OFF`, `POSTURE-RDP-NO-NLA`, `POSTURE-TLS-DEPRECATED-VERSION`, `POSTURE-SSH-TERRAPIN`, `POSTURE-FTP-ANONYMOUS-LOGIN`, `POSTURE-DNS-ZONE-TRANSFER`, `POSTURE-NFS-WORLD-READABLE-EXPORT`, …);
- **exposed-service category** from `detection_engine/port_intel.py` (`backdoor`, `container`, `datastore`, `database`, `cleartext`, admin);
- **CVE / missing patch** (product-level recipe; target version from the vuln DB, §4.3);
- **end-of-life OS/product**, **default credentials**;
- **generic** — last resort only.

Resolution order: `rule_id` → port-intel category → CVE present → keyword classifier (legacy, for findings with no structured key) → generic.

Recipe fields: `recipe_id`, `version`, `title_template`, `remediation_type` (CSAF), `risk_response` (NIST), `target_state_template`, `steps` (tiers `containment | fix | hardening`; each with description template, commands per `os_family`, `pre_checks`, `reboot_required`, `downtime`, `rollback`, `risk`), `compensating_controls`, `verification` (`scanner`, `check` = rule/scanner that proves closure, `manual_command` per os_family, `expected`), `references` (CWE, MITRE, CIS benchmark **by section name only** — never an invented control number, vendor advisory URL when static).

Templates substitute only context facts; a missing fact renders the literal `not recorded` and the step stays valid. All commands are hand-authored and non-destructive (existing KB invariant).

### 4.3 Plan (`remediation/plan.py`)

`build_plan(finding, ctx, *, due) -> Plan` — pure. Output:

| Block | Content |
|---|---|
| `context` | §4.1 facts with provenance |
| `remediation_type`, `risk_response` | from recipe |
| `target_state` | e.g. "OpenSSH ≥ 9.8p1" / "SMBv1 disabled". For CVE recipes the fixed version comes from the matched affected range's `fixed` bound. Today `detection_engine/matcher.py` knows it (`ev["fixed"]`) but only emits it inside the free-text `evidence_reason`; sub-project 1 adds a structured `fixed_version` to the match result and carries it into `finding.evidence["fixed_version"]` via `engine_bridge`. When absent (older findings, `last_affected`-only ranges): "confirm fixed version in the vendor advisory" |
| `urgency` | SSVC-style label (`act|attend|track_star|track`) + drivers list. **Informational only; never sets the due date** |
| `due` | `{at, source}` from §4.5 |
| `steps` | tiered, templated, commands for the auto-selected `os_family` plus the full per-OS map (UI may switch OS) |
| `compensating_controls` | text |
| `verification` | scanner check + manual command + expected result |
| `references` | CVE/NVD, advisory, CWE, MITRE, benchmark section names |
| `fragile_guard` | when the asset is fragile: every step flagged "coordinate with owner; no automated change" |
| `provenance` | `source: kb`, `recipe_id`, `recipe_version`, `facts_used`, `generated_at` (IST, aware) |

Plan shape is a superset of today's `RemediationPlanOut.plan`; `steps[].commands_for_os`, `summary`, `effort`, `remediation_risk`, `verification`, `long_term_recommendations`, `compensating_controls` are kept so existing clients do not break.

### 4.4 Bundles (`remediation/bundles.py`)

- `fix_key = sha256(recipe_id | product_family | normalized_target_state)[:12]`; `product_family` reuses the signature logic of `group_key_for` (`posture_rules.py:394`). Display ref `FIX-<first 6 hex>`; stable across scans. Reports may add ordinals (1, 2, 3) for readability only.
- A bundle holds: title, remediation type, target state, shared steps grouped per `os_family` when hosts differ, **per-host checklist** rows `{host, ip, os, port, finding_ids, status}` where status ∈ `open | closed | extension_approved | excluded`, `resolves` (all finding refs), `due` = earliest due of open members, `urgency` = max, `progress` = closed/total.
- Views: **by fix** (order by due, then by findings resolved desc) and **by host** (host → bundles sorted by due). Same data, pivoted.
- Accepted-risk and false-positive findings are excluded from open counts and listed with the reason. A finding with no specific recipe becomes a single-member generic bundle — never dropped. A bundle with every host closed is `done` and remains in the report with closure dates.

### 4.5 Deadlines (`services/deadlines.py`)

Resolution order (first match wins):

1. Approved extension → `findings.due_at` with `due_at_source = 'extension'`
2. Engagement policy → `engagements.rules_of_engagement["sla_policy"]` (`{critical_hours, high_hours, medium_hours, low_hours, info_hours}`, same validation as the tenant policy; no schema change)
3. Tenant policy → existing `sla_policies` row
4. Environment defaults (`settings.sla_hours_*`)

`services/sla.py` delegates to this resolver so dashboards, breach counts, plans, bundles and the report agree. The frontend `SLA_DAYS` table in `finding-model.ts` stops producing dates: the report uses the backend `due`; a finding with no backend due shows "No target".

**Extension requests**

- Table `deadline_extension_requests`: `id, tenant_id, engagement_id, subject_type (finding|bundle), finding_id NULL, fix_key NULL, member_finding_ids UUID[] (snapshot at request time), requested_due_at, reason, compensating_control NULL, status (pending|approved|rejected|withdrawn), requested_by, requested_at, decided_by NULL, decided_at NULL, decided_due_at NULL, decision_note NULL`.
- Rules: portal `client` users request within their own engagement; **compensating control is mandatory when any member finding is critical/high or KEV-listed**; one pending request per subject; `requested_due_at` must be after the current due date.
- Operators (`admin|manager`) approve (optionally with a different date → `decided_due_at`), or reject; `decision_note` required. On approval every still-open member finding gets `due_at` / `due_at_source='extension'`.
- Every transition writes a finding event (`extension_requested`, `extension_approved`, `extension_rejected`, `extension_withdrawn`) with actor, old/new date, reason, and an `audit_logs` row.
- Report shows "Extended from A → B, approved by X on D, reason R, compensating control C". Reason and planned date feed the SEBI summary fields "reason for non-closure" and "planned closure date".

### 4.6 AI refinement (`remediation/ai_refine.py`)

- Endpoints: `POST /findings/{id}/remediation/refine`, `POST /engagements/{id}/remediation/bundles/{fix_key}/refine` (admin|manager). `POST /findings/{id}/remediation/generate` remains as an alias of refine for one release.
- Input: the KB plan (grounding), the context facts, evidence summary, bundle member hosts, and the domain brief. All scan-derived text (banners, hostnames, product strings) is placed in a fenced untrusted-data block — never instructions.
- Transport: `ManagerLlmService` → `app/ai/gateway.py` (cloud / hybrid pseudonymised / sovereign local); every call persists `audit_records` to the AI audit chain.
- Output is an **overlay** on the KB plan: fields the model omits keep KB values. Allowed changes: product-specific steps/commands, sharper pre-checks/rollback, sequencing rationale. Guards: existing `HallucinationGuard.validate_remediation_commands` for commands; CVE IDs and versions not present in the input are stripped; a fixed version not confirmed by the vuln DB is labelled "AI-suggested — verify against the vendor advisory". The response includes a field-level diff (`ai_changes`).
- Persistence: `remediation_plans` gains `subject_type (finding|bundle)`, `fix_key NULL`, `facts_fingerprint` (sha256 of the facts used). Unique keys: `(finding_id, os)` for findings, `(engagement_id, fix_key, os)` for bundles. A refinement whose fingerprint no longer matches the live facts is returned with `stale: true`.
- Review gate unchanged: portal shows the KB plan until an operator publishes (`reviewed=true`); regeneration resets review (existing upsert semantics).

### 4.7 Backend AI report (replaces Next.js direct path)

- New module `app/ai/engagement_report.py`, ported from `lib/prompts/report.ts` + `lib/ai-engine.ts` (sectioned generation, deterministic scorecard, `validateReport` checks).
- **Deterministic inputs:** scorecard, exposure matrix counts, bundles (§4.4) and due dates (§4.5). The LLM no longer creates FIX groups or time windows; it writes narrative only: verdict, board decisions (referencing existing `FIX-` refs), executive summary, attack narrative, per-bundle rationale and sequencing, controls observed, limitations. Validation rejects any FIX ref or finding ref not in the input.
- Runs as a backend job reusing the `ai_report` router flow (generate → status → draft → approve/reject). All LLM calls go through the gateway and persist audit records.
- Next.js `app/api/reports/generate/route.ts` becomes a BFF proxy to the backend job endpoints; the Anthropic client, `callAnthropicWithRetry`, the hard-coded model and the `SIMULATED` outputs are removed from `lib/ai-engine.ts` for report generation. The report page polls the job and renders the approved/draft sections.

### 4.8 Surfaces

- **Findings page (operator):** rebuilt plan view — context card, OS auto-selected from the scan, tiers, verification, "Part of FIX-xxxxxx (n hosts)" link, Refine with AI, AI-diff toggle, stale badge, Approve for customer; extension-request panel (approve / approve with date / reject).
- **Remediation page (new):** operator + portal via the console-source seam (`lib/console-source.tsx`); toggle by fix / by host; checklists, progress, due + source.
- **Customer portal:** KB plan always; AI plan only when reviewed; "Request extension" on a finding or bundle; request status list. Portal routes delegate to operator handlers with the engagement pinned.
- **Report:** per-finding Remediation section renders the plan; roadmap section renders bundles (by fix, by-host appendix), extension history, approved AI narrative.
- **Tracker export:** `GET /engagements/{id}/remediation/export?format=xlsx|csv`. XLSX via `openpyxl` (new backend dependency) with sheets *By fix*, *By host checklist*, *Findings*, frozen header, autofilter, real date cells in IST; CSV returns a zip of the three sheets. Columns: FIX ref, finding ref, title, severity, host, IP, port, remediation type, target state, due, due source, status, extension reason, planned date, verification check.

## 5. Migrations

One Alembic revision `0048_contextual_remediation`:

- `findings.due_at TIMESTAMPTZ NULL`, `findings.due_at_source VARCHAR(16) NULL`
- `deadline_extension_requests` table (§4.5) with indexes on `(engagement_id, status)` and `finding_id`
- `remediation_plans`: `subject_type VARCHAR(8) NOT NULL DEFAULT 'finding'`, `fix_key VARCHAR(12) NULL`, `facts_fingerprint VARCHAR(64) NULL`; `finding_id` becomes nullable; add partial unique index for bundle rows; add CHECK (finding rows have finding_id, bundle rows have fix_key)

Engagement SLA policy uses the existing `rules_of_engagement` JSONB (no column).

## 6. Error handling

| Situation | Behaviour |
|---|---|
| AI provider unavailable / refused | KB plan stays; refine returns 503 with the reason; nothing cached |
| Sovereign profile with no local model | Refine disabled in UI with the reason; endpoint 409 |
| Missing asset/service facts | Rendered `not recorded`; plan still valid |
| Stale AI refinement | Returned with `stale: true`; UI badge + regenerate |
| Extension for another engagement / tenant | 404 (no existence leak) |
| Extension date not later than current due | 422 |
| Critical/high/KEV request without compensating control | 422 |
| Second pending request on same subject | 409 |
| AI report validation fails (unknown FIX/finding ref) | Section rejected, job reports which check failed; no partial publish |

## 7. Testing

- **Recipe coverage guard:** test fails if any `RULES` entry in `posture_rules.py` or any port-intel category lacks a recipe.
- Pure unit tests: context extraction (each provenance path), template substitution with missing facts, target-version derivation, SSVC label, bundle key stability (same inputs → same key; banner casing does not split), by-fix/by-host pivots, deadline resolution order.
- API tests (real `User` model, per vedha-job-control memory): extension request/approve/reject/withdraw, compensating-control rule, portal IDOR, timeline events written, audit rows written.
- AI tests: refine overlay/diff, guard stripping (unknown CVE, destructive command, unconfirmed version label), **wire-byte inspection** of the gateway transport in hybrid mode (hostnames/IPs pseudonymised), audit chain rows persisted, stale fingerprint.
- Backend AI report: deterministic scorecard parity with the TS implementation on a fixture; validation rejects invented refs.
- Migration upgrade/downgrade test.
- Export: XLSX opens with openpyxl, three sheets, date cells typed; CSV zip content.
- Frontend: model tests for plan rendering and bundle views; browser preview check of findings page, Remediation page, portal request flow and report.
- Full `pytest tests/` must stay green.

## 8. Build order (sub-projects, each independently shippable)

1. Context + recipes v2 + plan (pure) + coverage guard + structured `fixed_version` from the matcher; `GET /findings/{id}/remediation` serves v2.
2. Bundles + `GET /engagements/{id}/remediation/bundles?view=fix|host`.
3. Deadlines resolver + engagement SLA policy + migration 0048 + extension workflow (API + events).
4. AI refinement through gateway (finding + bundle) + stale detection.
5. Backend AI report job; delete Next.js direct path.
6. Surfaces: findings page, Remediation page (operator + portal), portal extension UI, report sections, XLSX/CSV export.

## 9. Out of scope

- Regulator-specific wording/deadlines per jurisdiction, customer tooling / change-window integration (not selected).
- Closure-evidence capture and report document control (separate report-structure project noted on 2026-09-26).
- Operator direct deadline edits without a request.
- Ticketing integrations (Jira) for bundles.

## 10. Constraints

- Shared checkout: stage explicit paths; never upgrade the shared `.venv` — `openpyxl` is added to backend requirements and installed in an isolated venv for verification.
- Any new LLM caller goes through `app/ai/gateway.py` and persists `audit_records`.
- Timestamps are timezone-aware IST via `project_time` helpers.
- Probe scanner trees are untouched (no `scanner/` or `main_scripts/` changes). The only `manager/detection_engine/` change is the additive `fixed_version` field on the match result.

## 11. Implementation notes & deviations (2026-09-27)

Shipped on `feat/contextual-remediation`; verified against a live stack (Postgres 16 + Redis + API + Next.js dev) with a seeded banking engagement.

| Spec | As built | Why |
|---|---|---|
| §4.4 `fix_key = recipe | family | target` for every recipe | CVE-PATCH keys on the product only; the bundle target is the highest `fixed_version` among members. GENERIC keys on the finding id | One upgrade closes every CVE on that product; unrelated generic findings must never merge |
| §4.4 shared bundle steps | Multi-host bundles render steps/closure check with "each host in the checklist"; the report rewrites them to the finding's own host | Live check showed single-host wording on a 2-host bundle |
| §5 replace finding uniqueness | Kept `UNIQUE(finding_id, os)`; bundle rows (NULL finding_id) use a partial unique index | NULLs never conflict in Postgres; no change to the existing upsert |
| §4.5 engagement SLA "edited in engagement settings" | Editor lives on the operator Remediation page | Next to the due dates it drives |
| §4.7 AI report as a job (generate → status → draft → approve) | Synchronous backend endpoint `POST /engagements/{id}/ai-report/engagement` (+ portal), same UX as before | Keeps the existing Reports UX; sections run in parallel and are bounded; the existing job pipeline is unchanged |
| §4.3 plan commands | CVE-PATCH commands name the real package (openssh → openssh-server …); unknown products keep an explicit placeholder | Live check showed `<package>` |
| §4.2 legacy `remediation_kb` | Kept (compliance/content still classify with it); routes no longer serve it | Avoids touching compliance mapping in this project |
| — | Bundles carry `max_severity` + `kev` of open members | The portal form shows the compensating-control rule accurately |

Out of scope, flagged as a follow-up task: `triageFindings` and `chat` in `manager/frontend/lib/ai-engine.ts` still call Anthropic directly from Next.js.

Environment note (not a product bug): several local Vedha instances on `localhost` share the host-scoped `vedha_token` cookie, so a token signed by another instance's secret logs the session out. Use one instance per hostname when testing side by side.
