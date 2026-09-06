# Report-section integration — design

**Date:** 2026-09-06
**Branch:** `manager_pipeline_enhancement`
**Status:** Approved design — ready for implementation planning

## Problem

`reportsection/` (repo root) is a self-contained, unit-tested "technical findings"
report module — a professional-grade replacement for the current `FindingCard`.
It separates severity from priority (and shows its working), states confidence
honestly from the detection method, redacts secrets out of evidence before they
reach a PDF, groups remediation into contain/fix/harden, and flags findings that
are not yet delivery-ready.

We want this UI/UX in **both** the internal assessor report
(`manager/frontend/app/reports/page.tsx`) and the **customer portal** report
(`manager/frontend/app/portal/reports/page.tsx`), and we want the backend to
progressively emit the data the module reads.

## Goals

- Land the module in the admin reports page as a true drop-in (Technical +
  Evidence tabs), deleting the superseded local components.
- Reuse the **same visual component** in the customer portal without breaching
  the existing confidentiality boundary (the portal deliberately withholds
  internal red/blue-team judgment).
- Progressively enrich the backend so fewer "not recorded" gaps appear over time,
  with no further UI change required.

## Non-goals

- No redesign of the Executive / CVE / MITRE-coverage tabs.
- No change to the AI-report generation flow.
- No new evidence-capture pipeline in the scanner (P3 populates from what already
  exists; net-new capture is out of scope).

## Source module (what we are integrating)

Three files + a test spec + an integration guide, under `reportsection/`:

| File | Role |
|---|---|
| `finding-model.ts` | All judgement: CVSS 3.1/4.0 reading, severity→priority (shown), SLA clock, confidence-from-detection-method, evidence redaction, delivery-readiness. No JSX. |
| `FindingReport.tsx` | Layout only: numbered 9-section finding card, filterable `FindingsSection`, exported `EvidenceArtifact`. Decides nothing. |
| `report-finding.css` | Theme-aware styling via existing SIGNAL tokens. |
| `spec.ts` | 58 behavioural assertions (priority, SLA, CVSS, confidence, redaction, readiness, degradation). |
| `INTEGRATION.md` | Wiring guide — **partially stale**, see Risk #1 and #2. |

### Verified compatibility

- `manager/frontend/lib/severity.ts` exports exactly what the model needs
  (`SEVERITY` with `.rank/.label/.sigil`, `SEVERITY_ORDER`, `toSeverity`,
  `type Severity`). The module was written against this file.
- All ~35 CSS custom properties referenced by `report-finding.css` are already
  defined in `app/globals.css`.
- The admin page's local `Finding` interface is structurally assignable to
  `RawFinding` (every enrichment field is optional).
- Single git repo rooted at repo root; specs live in `docs/superpowers/specs/`.

## Backend reality (drives the adapter + P3)

`manager/backend/app/schemas/finding.py :: FindingOut` already emits ~80% of
`RawFinding`:

| Module `RawFinding` field | Backend `FindingOut` | Action |
|---|---|---|
| id, title, severity, status, description, impact, remediation, mitre | present | pass-through |
| cvss, cvssVector, epss, riskScore, activelyExploited | `cvss_score`, `cvss_vector`, `epss_score`, `risk_score`/`risk_rank`, `actively_exploited` | pass-through |
| exploitValidated, technicalDetails, businessImpact, evidence, compliance | `exploit_validated`, `technical_details`, `business_impact`, `evidence`/`evidence_summary`, `compliance` | pass-through / reshape |
| detectionCoverage | `detection_status` (COVERED/PARTIAL/BLIND) | pass-through |
| assets[] | single `asset_context` (ip/host/os/env/owner) | adapter → one row |
| **detectionMethod** | — | **derive** in adapter (P1), first-class column (P3) |
| **verification{expected,command,…}** | only `verification_state/confidence/rationale` | **P3** adds retest block |
| internetReachable, epssPercentile, kevAddedAt, rootCause, prerequisites, attackPath, advisories | — | derive where possible (P1), first-class (P3) |

## Decision record

Locked with the user during brainstorming:

1. **Surfaces:** both admin + portal get the same report UI/UX.
2. **Portal data:** *same look, curated data* — identical component, fed a
   client-safe `RawFinding`; confidentiality boundary preserved.
3. **Print rule:** rely on the module's own higher-specificity print CSS; **do
   not** edit the shared `globals.css` print rule.
4. **Adapter home:** frontend BFF (TypeScript, Next.js `/api` routes + a shared
   `lib/report/adapt.ts`). Backend adds real columns later.
5. **Depth:** UI now + progressive backend enrichment (P3).

## Architecture — three independently shippable phases

```
Phase 1  Foundation + Admin reports      (frontend only)
   ├─ Phase 2  Portal parity, curated     (frontend only; depends on P1)
   └─ Phase 3  Backend enrichment         (Python; independent; auto-lights-up P1+P2)
```

### Phase 1 — Foundation + Admin reports

**New files**

- `manager/frontend/lib/report/finding-model.ts` — verbatim from source
  (its `import "../severity"` resolves to `lib/severity.ts`).
- `manager/frontend/components/report/FindingReport.tsx` — from source, plus a
  new `mode?: "assessor" | "client"` prop (default `"assessor"` = unchanged
  behavior). Threaded from `FindingsSection` → `FindingReport`. Used by P2.
- `manager/frontend/styles/report-finding.css` — verbatim.
- `manager/frontend/lib/report/adapt.ts` — **new.** `toRawFinding(api): RawFinding`
  plus `curateForClient(raw): RawFinding` (used by P2). Holds all derivations so
  neither the component nor the pages know about the API shape.
- `manager/frontend/lib/report/__tests__/finding-model.test.ts` — the 58
  assertions from `spec.ts`, ported to the project test runner.

**Adapter derivations (`adapt.ts`)**

- `detectionMethod` ← `exploit_validated` → `exploit`; else
  `verification_state === "active"/"confirmed"` → `behavioural`; else map
  `detection_status` + `exploit_maturity` heuristically; else leave undefined
  (→ honest "Unverified").
- `assets[]` ← `asset_context` single row (host/ip/service/version/env/owner).
- `evidence[]` ← reshape `evidence` dict / `evidence_summary[]` into `RawEvidence`.
- `internetReachable` ← `asset_context.environment` heuristic until P3.
- Everything else: direct pass-through with name mapping.

**Admin wiring — `app/reports/page.tsx`**

```diff
+ import { FindingsSection, EvidenceArtifact } from "../../components/report/FindingReport";
+ import "../../styles/report-finding.css";   // after globals.css

- {tab === "technical" && <TechTab findings={findings} total={summary.total} />}
+ {tab === "technical" && <FindingsSection findings={findings} total={summary.total} />}
```

- Evidence Vault tab: replace `<EvidBlock item={item} />` with
  `<EvidenceArtifact item={item} refId={`${item.finding.id}/E${i+1}`} />`
  (**both** the Technical tab and the Evidence Vault tab — Risk #3).
- **Delete:** `TechTab`, `FindingCard`, `EvidBlock`, `parseCvssVector`,
  `VM_LABEL`, `VM_NAME`.
- **KEEP:** `parseCvss` — still used by `ExecTab` and `CveTab`
  (`page.tsx:948`, `page.tsx:1071`). INTEGRATION.md is wrong to say drop it.
- `findings` are mapped through `toRawFinding` **in the admin BFF route**
  (`app/api/findings/route.ts` + the `[id]` detail route), consistent with the
  "adapter home = BFF" decision, so the page receives report-ready data and the
  local `Finding` interface converges on `RawFinding`.

### Phase 2 — Portal parity (same look, curated data)

Confidentiality is preserved by two mechanisms together:

1. **Curated data** — `curateForClient()` strips raw evidence content,
   `exploitValidated`, internal confidence *basis/caveat*, and reproduction
   steps; keeps title/severity/CVSS/impact/remediation/references.
2. **`mode="client"`** — the component suppresses assessor-only sections:
   Evidence artifacts, Reproduction, the "reproduced here" signal, the
   "Not ready for delivery" blocker panel, and internal gap-nag copy. Client
   mode renders a clean, gap-free professional report.

`app/portal/reports/page.tsx` swaps its `FindingCard`/`FindingsTable` for
`<FindingsSection mode="client" findings={curated} total={…} />`, fed via the
portal BFF (`/api/portal/...` + `lib/portal-client.ts`). The portal backend
schema (`schemas/portal.py`) is **not** widened — curation happens in the BFF
from whatever the portal endpoint already returns.

Result: pixel-identical component, customer-safe data.

### Phase 3 — Backend enrichment (progressive, by value)

Own detailed plan after a focused backend-exploration pass. Order by value
(INTEGRATION.md ranking):

1. `detection_method` enum (highest value — turns "Unverified" into real confidence).
2. `verification` retest block `{method, command, expected, retain}` (delivery blocker).
3. `internet_reachable` boolean (exposure → priority).
4. Incremental: `epss_percentile`, `kev_added_at`, `advisories`, `root_cause`,
   `prerequisites`, `attack_path`.

Each = one column + populate-from-scanner/enrichment + expose in `FindingOut`.
When a real value arrives, the adapter drops its derivation and passes it
through — no UI change; both surfaces light up.

## Points-of-failure register

| # | Risk | Fix |
|---|---|---|
| 1 | Deleting `parseCvss` breaks ExecTab/CveTab | Keep it; only delete `parseCvssVector`/`VM_LABEL`/`VM_NAME`. |
| 2 | `globals.css:2534` print rule (`button {display:none!important}`) hides finding headers (they are `<button>`) | Module's higher-specificity `.vf-head`/`.vf-card` print rules override it; import module CSS after globals. No globals edit. |
| 3 | Secrets leak if only one evidence renderer switches to redaction | Switch **both** Technical + Evidence Vault to `EvidenceArtifact` in the same change. |
| 4 | Portal exposes internal judgment | `mode="client"` + `curateForClient()` — dual guard. |
| 5 | `Finding[]`→`RawFinding[]` assignability | Verified structurally assignable; `toRawFinding` makes it explicit + centralises it. |
| 6 | Next.js CSS import-order flakiness | Critical print overrides win by *specificity*, not source order — order-independent. |
| 7 | Empty "not recorded" gaps day 1 | Honest/expected in assessor mode; suppressed in client mode; P3 fills them. |
| 8 | TS strict build breakage | Port `spec.ts` first; typecheck + build in each phase's verification gate. |

## Testing

- **Port `spec.ts`** (58 assertions) to `lib/report/__tests__/` — the safety net;
  run it first and keep it green through all phases.
- Add adapter tests for `toRawFinding` (derivations) and `curateForClient`
  (that internal fields are actually stripped — this is a security assertion).
- Per phase: `tsc` typecheck + production build.
- Manual: print/PDF the admin report (Risk #2 path — the fiddliest bit) and
  confirm cover, finding headers, and redacted-but-not-secret evidence all render.

## Build order

P1 → P2 (both frontend, deliver the full UI) → P3 (backend, progressive).
Each phase gets its own implementation plan; P1 is planned first.
