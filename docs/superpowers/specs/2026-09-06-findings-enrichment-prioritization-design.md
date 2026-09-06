# Findings Enrichment & Prioritization — Design

**Date:** 2026-09-06
**Scope:** Manager only (`backend/` + `frontend/`). Findings first; Reports maturity is a
separate follow-up spec.

## Problem

The frontend findings detail panel already renders explanation, business impact, technical
detail, compliance, exploit maturity, an evidence gallery, and a fix-plan view — but the
backend `FindingOut` schema emits **none** of that content. The adapter
(`frontend/lib/adapters.ts`) reads `technical_details`, `business_impact`, `impact`,
`compliance[]`, `exploit_maturity`, `actively_exploited`, `attack_path`, … which the API never
sends, so those sections render empty. This is a *fill-the-contract + polish* effort, not a
rebuild. Additionally, the list default sort (`effective_risk` desc) can place a KEV'd **high**
above a **critical**, so criticals are not guaranteed on top.

## Decisions (agreed)

- **Content engine:** deterministic curated KB as the always-available spine (works offline,
  no AI key, reproducible), mirroring `backend/app/services/remediation_kb.py`. Optional AI
  layer enriches on top and **fails closed** to the KB.
- **Compliance frameworks:** PCI DSS 4.0, ISO 27001:2022 (Annex A), NIST CSF / 800-53,
  SOC 2 (TSC), HIPAA Security Rule.
- **Storage:** hybrid. Deterministic content computes on read (like `risk_rank`); AI/analyst
  overrides persist in one new nullable `findings.content_overrides` JSONB column.
- **List vs detail:** heavy prose only on the detail endpoint; list carries cheap derived
  fields (`exploit_maturity`, compliance count). Preserves the bounded-read / no-N+1 rule.

## Architecture

New pure/offline services (no DB, no network in the deterministic path):

- `services/finding_priority.py` — `SEVERITY_RANK`, a SQLAlchemy `severity_order_case()` for
  tier-first ordering, and a pure `priority_key()` tuple used by tests / any in-memory sort.
- `services/finding_content.py` — `finding_content(finding, asset_ctx, signals)` →
  `technical_explanation`, `business_impact` (scaled by asset criticality + severity),
  `exploitation` (validated vs **"Not validated. Absence of proof is not proof of absence."**
  + KEV/EPSS/PoC), `exploit_maturity` (WEAPONIZED/POC/THEORETICAL). Reuses
  `remediation_kb.classify_finding` as the single category source of truth.
- `services/finding_compliance.py` — curated category→control map across the five frameworks;
  returns `[{framework, controls[], rationale}]`.
- `services/evidence_summary.py` — arbitrary `evidence` JSONB → flat `[{label, value}]` facts.

`FindingOut` gains the derived content on the detail path; `content_overrides` (AI/analyst)
takes precedence over the deterministic value field-by-field.

## Prioritization ("critical always top")

Default `sort="risk"` becomes: severity tier (critical>high>medium>low>info) DESC, then
`risk_rank`/effective_risk DESC, then `created_at` DESC, then `id`. `cvss`/`epss`/`date`
remain pure axes (explicit operator override). Detail path wires real asset
criticality/exposure into `compute_risk_rank` (the override hook already exists). The client
"urgent findings" summary widget (`page.tsx:1883`) is a separate urgency lens and is left as-is.

## Frontend

Ordered explanation stack in the detail panel: What it is → Why it matters (business) →
Exploitation (honest) → Evidence (fact table, raw JSON behind a disclosure) → Compliance
(framework chips → controls) → Fix plan (color-coded step risk/effort chips, copy buttons,
visually distinct verification / long-term / compensating-control blocks, using existing design
tokens). Extract the detail panel out of the 3,499-line `findings/page.tsx` into its own
component (targeted de-bloat, no unrelated refactor).

## Phases (small, independently shippable, test-backed)

1. **P1** Prioritization — tier-first sort + asset-context risk_rank.
2. **P2** `finding_content.py` (technical/business/exploitation/maturity) + tests.
3. **P3** `finding_compliance.py` (5 frameworks) + tests.
4. **P4** `evidence_summary.py` + tests.
5. **P5** Expose via `FindingOut` (detail-heavy / list-light) + `content_overrides` migration.
6. **P6** Frontend detail panel polish + component extraction.
7. **P7** Optional AI enrichment seam (fails closed) via `services/llm.py`.
8. **P8** Verify — backend pytest, frontend typecheck/build, smoke.

## Edge cases

Generic/no-CVE finding still gets content; missing evidence → graceful empty; posture and CVE
findings both classify; `exploit_validated` true → validated framing; `verification_state ==
contradicted` → do not overstate impact; null asset context → severity-only business framing;
list stays light for performance; deterministic content is customer-safe (portal can reuse).
