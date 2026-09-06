# Report Section — Phase 1 (Foundation + Admin Reports) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the admin report's Technical-Findings and Evidence-Vault tabs with the vendored `reportsection/` module (assessment-grade finding cards + secret-redacting evidence), fed by a tested `FindingOut → RawFinding` adapter.

**Architecture:** Copy the three module files into the manager frontend verbatim (they were written against this repo's `lib/severity.ts` and CSS tokens). Add a pure, unit-tested adapter (`lib/report/adapt.ts`) that turns the existing UI `Finding` shape into the module's `RawFinding`, deriving `detectionMethod`, `assets[]`, `epss`, and `internetReachable` from fields the backend already sends. Wire both tabs; delete the superseded local components. The module's own print CSS neutralises the aggressive `globals.css` print rule by specificity, so no shared CSS is edited.

**Tech Stack:** Next.js (App Router, React 18), TypeScript, `node:test` via `tsx`, `@tanstack/react-query`, lucide-react.

## Global Constraints

- Repo root: `/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha`. All paths below are relative to `manager/frontend/` unless prefixed with `reportsection/` (repo root) or `docs/`.
- Work on the current branch `manager_pipeline_enhancement` (already checked out; not `main`).
- Test runner: `npm test` = `tsx --test tests/*.test.ts`. Test files live in `manager/frontend/tests/` and use `node:test` + `node:assert/strict`. Run one file with `npx tsx --test tests/<file>.test.ts`.
- Type gate: `npx tsc --noEmit` (there is no `typecheck` npm script). `tsconfig.json` has `strict: false`, `noUnusedLocals: false` — dangling unused helpers are NOT build errors, so deletions never cascade.
- Integration gate (end of plan): `npm run build` (`next build`, which also type-checks).
- **KEEP `parseCvss`** in `app/reports/page.tsx` (used by ExecTab line ~948 and CveTab line ~1071). Only `parseCvssVector`/`VM_LABEL`/`VM_NAME`/`CvssVector` are safe to delete.
- **Security-mandatory:** the Technical tab AND the Evidence Vault tab must both use the redacting `EvidenceArtifact`. Never leave one on the old raw renderer (secrets masked in one tab would still leak from the other, and into the same PDF).
- CSS import order: `import "../../styles/report-finding.css"` must appear after the app already imports `globals.css` (globals is imported in `app/layout.tsx`; a page-level import naturally follows). The critical print overrides win by selector specificity regardless, so this is belt-and-suspenders.
- Commit after every task. Commit trailer (both lines, verbatim):
  ```
  Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK
  ```

---

### Task 1: Vendor `finding-model.ts` + port its 58-assertion spec (the safety net)

**Files:**
- Create: `manager/frontend/lib/report/finding-model.ts` (copy of `reportsection/finding-model.ts`)
- Create: `manager/frontend/tests/report-finding-model.test.ts`

**Interfaces:**
- Produces: everything the rest of the plan imports from `./finding-model` — `assess(f, now?) → AssessedFinding`, `readVector(s) → VectorReading | null`, `redact(s) → Redaction`, `priorityOf(f) → Priority`, `slaOf(f, code, now?) → Sla`, `confidenceOf(f) → Confidence`, `readinessOf(f)`, and the types `RawFinding`, `RawEvidence`, `RawAsset`, `DetectionMethod`, `RemediationTier`, `AssessedFinding`. Its only import is `../severity`, which resolves to the existing `lib/severity.ts`.

- [ ] **Step 1: Copy the model verbatim**

Run:
```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
mkdir -p manager/frontend/lib/report
cp reportsection/finding-model.ts manager/frontend/lib/report/finding-model.ts
```
The file's `import { ... } from "../severity"` now resolves to `manager/frontend/lib/severity.ts` (verified: it exports `SEVERITY` with `.rank/.label/.sigil`, `SEVERITY_ORDER`, `toSeverity`, `type Severity`). Do not edit the copied file.

- [ ] **Step 2: Write the ported test file**

The source `reportsection/spec.ts` is already a complete 58-assertion suite using a local `ok(name, cond, got?)` / `group(name)` harness. Port it by re-pointing those two helpers at `node:test`, then pasting the assertion body unchanged.

Create `manager/frontend/tests/report-finding-model.test.ts`:

```ts
import { test } from "node:test";
import assert from "node:assert/strict";

import {
  assess, readVector, redact, priorityOf, slaOf, confidenceOf, readinessOf,
  type RawFinding,
} from "../lib/report/finding-model";

// Re-point spec.ts's harness at node:test. `ok(name, cond, got?)` registers one
// test; the optional third diagnostic arg is accepted and ignored.
function ok(name: string, cond: boolean, _got?: unknown) {
  test(name, () => assert.ok(cond));
}
function group(_n: string) { /* section marker only */ }

// ↓↓↓ Paste the body of reportsection/spec.ts from the `const base: RawFinding`
//     declaration down to (but NOT including) the final two lines:
//       console.log(`\n${pass} passed, ${fail} failed`);
//       if (fail) throw new Error(`${fail} check(s) failed`);
//     Everything between (the `const base`, `const NOW`, `const F`, every
//     group(...) and ok(...) call) is copied unchanged.
```

Copy the region now:
```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
# Preview the region to paste (from `const base` to the last ok(...) before the summary):
sed -n '/^const base/,/readiness reports every blocker/p; /cvss .9.8 (High)./p; /cvss out of range rejected/p' reportsection/spec.ts
```
Paste that region beneath the harness in the new test file. Remove the two trailing summary lines. Do not change any `ok(...)`/`group(...)` call.

- [ ] **Step 3: Run the test to verify it passes**

Run:
```bash
cd manager/frontend && npx tsx --test tests/report-finding-model.test.ts
```
Expected: all subtests pass (`# pass 58`, `# fail 0`). If any fail, the paste is incomplete — re-check the region boundaries; do not edit `finding-model.ts`.

- [ ] **Step 4: Commit**

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
git add manager/frontend/lib/report/finding-model.ts manager/frontend/tests/report-finding-model.test.ts
git commit -m "$(printf 'Vendor finding-model + port its spec into admin frontend\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 2: Vendor `FindingReport.tsx` + `report-finding.css`

**Files:**
- Create: `manager/frontend/components/report/FindingReport.tsx` (copy of `reportsection/FindingReport.tsx`)
- Create: `manager/frontend/styles/report-finding.css` (copy of `reportsection/report-finding.css`)

**Interfaces:**
- Consumes: `../../lib/severity` and `../../lib/report/finding-model` (both resolve from `components/report/`).
- Produces: `FindingsSection({ findings: RawFinding[]; total: number })` and `EvidenceArtifact({ item: RawEvidence; refId: string })`, both exported.

- [ ] **Step 1: Copy the component and stylesheet verbatim**

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
mkdir -p manager/frontend/components/report manager/frontend/styles
cp reportsection/FindingReport.tsx manager/frontend/components/report/FindingReport.tsx
cp reportsection/report-finding.css manager/frontend/styles/report-finding.css
```
No edits. `FindingReport.tsx` already starts with `"use client";` and imports `flushSync` from `react-dom` (React 18 — present).

- [ ] **Step 2: Type-check that the component compiles against the project**

Run:
```bash
cd manager/frontend && npx tsc --noEmit
```
Expected: no errors referencing `components/report/FindingReport.tsx` or `lib/report/finding-model.ts`. (Pre-existing errors elsewhere, if any, are out of scope — confirm none are new by comparing against a clean `npx tsc --noEmit` on `HEAD~1` if unsure.)

- [ ] **Step 3: Commit**

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
git add manager/frontend/components/report/FindingReport.tsx manager/frontend/styles/report-finding.css
git commit -m "$(printf 'Vendor FindingReport component + report-finding.css\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 3: Adapter `lib/report/adapt.ts` (UI `Finding` → `RawFinding`) + tests

**Files:**
- Create: `manager/frontend/lib/report/adapt.ts`
- Create: `manager/frontend/tests/report-adapt.test.ts`
- Modify: `manager/frontend/lib/adapters.ts` (add one field to `toUiFinding`)

**Interfaces:**
- Consumes: `RawFinding`, `RawAsset`, `DetectionMethod` from `./finding-model`.
- Produces: `toRawFinding(f: any): RawFinding`, `deriveDetectionMethod(f: any): DetectionMethod | undefined`, `toReportAssets(f: any): RawAsset[]`. Consumed by Task 4.

- [ ] **Step 1: Expose `exploit_validated` on the UI finding**

The module derives CONFIRMED confidence from `exploitValidated`, but `toUiFinding` currently folds it only into `activelyExploited`. Add it back as its own field.

In `manager/frontend/lib/adapters.ts`, inside `toUiFinding`'s returned object, immediately after the line:
```ts
    activelyExploited: api.actively_exploited ?? api.exploit_validated ?? api.kev_listed ?? false,
```
add:
```ts
    exploitValidated: api.exploit_validated ?? false,
```
This is additive; no existing consumer breaks.

- [ ] **Step 2: Write the failing adapter tests**

Create `manager/frontend/tests/report-adapt.test.ts`:

```ts
import { test } from "node:test";
import assert from "node:assert/strict";

import { toRawFinding, deriveDetectionMethod, toReportAssets } from "../lib/report/adapt";

// A minimal UI-Finding-shaped object (as toUiFinding would produce).
const uiBase = {
  id: "VDH-1", title: "t", severity: "CRITICAL", status: "OPEN",
  affectedHost: "web-01", discoveredAt: "2026-08-20T09:00:00Z",
  description: "d", technicalDetails: "td", impact: "i",
  evidence: [{ label: "l", content: "c" }], remediation: ["fix it"],
  mitre: [], riskScore: 900, cvss: "9.8", cvssVector: "",
  activelyExploited: false, detectionCoverage: "BLIND",
  epssScore: 0, epssPercentile: 0, epssRecorded: false,
  exploitValidated: false, verificationState: null,
  assetContext: null,
};
const U = (o: Record<string, unknown>) => ({ ...uiBase, ...o });

test("detectionMethod: validated exploit ⇒ exploit", () => {
  assert.equal(deriveDetectionMethod(U({ exploitValidated: true })), "exploit");
});
test("detectionMethod: confirmed verification ⇒ behavioural", () => {
  assert.equal(deriveDetectionMethod(U({ verificationState: "confirmed" })), "behavioural");
});
test("detectionMethod: covered detection ⇒ version", () => {
  assert.equal(deriveDetectionMethod(U({ detectionCoverage: "COVERED" })), "version");
});
test("detectionMethod: nothing recorded ⇒ undefined (honest 'Unverified')", () => {
  assert.equal(deriveDetectionMethod(U({})), undefined);
});

test("assets: empty when no asset context", () => {
  assert.deepEqual(toReportAssets(U({})), []);
});
test("assets: one row derived from asset context", () => {
  const rows = toReportAssets(U({
    assetContext: { hostname: "web-01", ipAddress: "10.0.0.5", environment: "internal", owner: "ops" },
  }));
  assert.equal(rows.length, 1);
  assert.equal(rows[0].host, "web-01");
  assert.equal(rows[0].ip, "10.0.0.5");
  assert.equal(rows[0].internetReachable, false);
});

test("epss: mapped only when recorded", () => {
  assert.equal(toRawFinding(U({ epssScore: 0.7, epssRecorded: true })).epss, 0.7);
  assert.equal(toRawFinding(U({ epssScore: 0, epssRecorded: false })).epss, undefined);
});
test("internetReachable: dmz environment ⇒ true", () => {
  assert.equal(
    toRawFinding(U({ assetContext: { hostname: "h", environment: "DMZ" } })).internetReachable,
    true,
  );
});
test("toRawFinding: preserves required fields for assess()", () => {
  const r = toRawFinding(U({ exploitValidated: true }));
  assert.equal(r.id, "VDH-1");
  assert.equal(r.exploitValidated, true);
  assert.equal(r.detectionMethod, "exploit");
});
```

- [ ] **Step 3: Run the tests to verify they fail**

Run:
```bash
cd manager/frontend && npx tsx --test tests/report-adapt.test.ts
```
Expected: FAIL — `Cannot find module '../lib/report/adapt'`.

- [ ] **Step 4: Implement the adapter**

Create `manager/frontend/lib/report/adapt.ts`:

```ts
/**
 * adapt.ts — maps the admin UI `Finding` shape (produced by lib/adapters.ts::
 * toUiFinding) into the report module's `RawFinding`. Kept pure and unit-tested;
 * the reports page applies it at the call site because its other tabs still
 * consume the UI shape. Backend enrichment (Phase 3) later supplies real values
 * for the fields derived here, at which point the derivations become pass-throughs.
 */
import type { RawFinding, RawAsset, DetectionMethod } from "./finding-model";

/** Best-effort exposure read from the asset's environment label. */
function deriveInternetReachable(f: any): boolean | undefined {
  const env = String(f?.assetContext?.environment ?? "").toLowerCase();
  if (!env) return undefined;
  if (/(internet|dmz|external|public|edge)/.test(env)) return true;
  if (/(internal|corp|private|lan|intranet)/.test(env)) return false;
  return undefined;
}

/** How the finding was established → module confidence input. Undefined ⇒ "Unverified". */
export function deriveDetectionMethod(f: any): DetectionMethod | undefined {
  if (f?.exploitValidated) return "exploit";
  const vs = String(f?.verificationState ?? "").toLowerCase();
  if (vs === "confirmed") return "behavioural";
  if (vs === "corroborated") return "configuration";
  const cov = String(f?.detectionCoverage ?? "").toUpperCase();
  if (cov === "COVERED") return "version";
  if (cov === "PARTIAL" || cov === "BLIND") return "banner";
  return undefined;
}

/** The single-row affected-assets table from asset context; [] when absent. */
export function toReportAssets(f: any): RawAsset[] {
  const ac = f?.assetContext;
  if (!ac) return [];
  return [{
    host: ac.hostname ?? ac.fqdn ?? ac.ipAddress ?? f.affectedHost ?? "—",
    ip: ac.ipAddress ?? undefined,
    version: ac.osVersion ?? undefined,
    environment: ac.environment ?? undefined,
    owner: ac.owner ?? undefined,
    internetReachable: deriveInternetReachable(f),
  }];
}

export function toRawFinding(f: any): RawFinding {
  return {
    ...f,
    epss: f?.epssRecorded && typeof f.epssScore === "number" ? f.epssScore : undefined,
    epssPercentile: f?.epssPercentile || undefined,
    assets: toReportAssets(f),
    detectionMethod: deriveDetectionMethod(f),
    internetReachable: deriveInternetReachable(f),
    exploitValidated: Boolean(f?.exploitValidated),
    activelyExploited: Boolean(f?.activelyExploited),
    detectionCoverage: f?.detectionCoverage ?? "",
  } as RawFinding;
}
```
The `as RawFinding` on the spread is deliberate: the UI `Finding` is a verified superset, and the assertion suppresses the excess-property check on the UI-only fields (`riskBreakdown`, `killChain`, …). The derived fields above the spread are the authoritative values.

- [ ] **Step 5: Run all report tests to verify they pass**

Run:
```bash
cd manager/frontend && npx tsx --test tests/report-adapt.test.ts tests/report-finding-model.test.ts
```
Expected: all pass.

- [ ] **Step 6: Commit**

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
git add manager/frontend/lib/report/adapt.ts manager/frontend/tests/report-adapt.test.ts manager/frontend/lib/adapters.ts
git commit -m "$(printf 'Add UI-Finding to RawFinding adapter with derivations + tests\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 4: Wire the Technical tab → `FindingsSection`; delete `TechTab`/`FindingCard`/`CvssVector` + dead helpers

**Files:**
- Modify: `manager/frontend/app/reports/page.tsx`

**Interfaces:**
- Consumes: `FindingsSection` (Task 2), `toRawFinding` (Task 3).

- [ ] **Step 1: Add imports**

In `app/reports/page.tsx`, after the existing import block (the `import { type ReportResult } from "../../lib/ai-engine";` line, ~line 22), add:
```ts
import { FindingsSection, EvidenceArtifact } from "../../components/report/FindingReport";
import { toRawFinding } from "../../lib/report/adapt";
import "../../styles/report-finding.css"; // after globals.css (imported in app/layout.tsx)
```
(`EvidenceArtifact` is imported now; it is used in Task 5.)

- [ ] **Step 2: Derive report findings in the page component**

In `ReportsPage`, immediately after:
```ts
  const findings = findQ.data?.items ?? [];
```
add:
```ts
  const reportFindings = useMemo(() => findings.map(toRawFinding), [findings]);
```
(`useMemo` is already imported on line 3.)

- [ ] **Step 3: Swap the Technical tab render**

Replace the line:
```ts
              {tab === "technical" && <TechTab findings={findings} total={summary.total} />}
```
with:
```ts
              {tab === "technical" && <FindingsSection findings={reportFindings} total={summary.total} />}
```

- [ ] **Step 4: Delete the superseded components and their private helpers**

Delete these top-level definitions from `app/reports/page.tsx` (delete highest line numbers first so ranges stay valid; `noUnusedLocals` is off so order does not affect compilation):

1. `function TechTab(...) { ... }` — currently ~lines 970–997.
2. `function FindingCard(...) { ... }` — currently ~lines 242–426.
3. `function CvssVector(...) { ... }` — currently ~lines 180–200 (only rendered inside `FindingCard`).
4. `function parseCvssVector(...) { ... }` — ~lines 86–89.
5. `const VM_LABEL = { ... };` — ~lines 90–96.
6. `const VM_NAME = { ... };` — ~lines 97–103.

Do NOT delete `parseCvss` (~76–78) — ExecTab/CveTab still call it. Leave `cvssColor`, `remText`, `SevBadge`, `StatusPill`, `CopyBtn` as-is (still referenced by surviving tabs, or harmlessly unused).

- [ ] **Step 5: Type-check and confirm no dangling references**

Run:
```bash
cd manager/frontend && npx tsc --noEmit
```
Expected: no errors mentioning `TechTab`, `FindingCard`, `CvssVector`, `parseCvssVector`, `VM_LABEL`, or `VM_NAME` (i.e. nothing still references the deleted symbols). Fix any straggler reference the compiler names.

- [ ] **Step 6: Commit**

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
git add manager/frontend/app/reports/page.tsx
git commit -m "$(printf 'Wire admin Technical tab to FindingsSection; drop legacy FindingCard\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 5: Switch the Evidence Vault tab → `EvidenceArtifact`; delete `EvidBlock` (security-mandatory)

**Files:**
- Modify: `manager/frontend/app/reports/page.tsx`

- [ ] **Step 1: Swap the evidence renderer in `EvidTab`**

In `EvidTab`, the evidence list maps items shaped `{ ...evidenceEntry, finding }` (see `const all = findings.flatMap(f => f.evidence.map(e => ({ ...e, finding: f })))`). Replace:
```tsx
              <EvidBlock item={item} />
```
with:
```tsx
              <EvidenceArtifact item={item} refId={`${item.finding.id}/E${String(i + 1).padStart(2, "0")}`} />
```
(`item` carries `label`/`content`/`type`, structurally assignable to `RawEvidence`; `i` is the existing map index.)

- [ ] **Step 2: Delete `EvidBlock`**

Delete `function EvidBlock(...) { ... }` — currently ~lines 201–241. It has no remaining callers after Step 1 (its only other caller, `FindingCard`, was removed in Task 4).

- [ ] **Step 3: Build to verify the whole page compiles and no caller is left**

Run:
```bash
cd manager/frontend && npx tsc --noEmit && npm run build
```
Expected: type-check clean; `next build` completes. No error mentions `EvidBlock`.

- [ ] **Step 4: Commit**

```bash
cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha"
git add manager/frontend/app/reports/page.tsx
git commit -m "$(printf 'Switch Evidence Vault to redacting EvidenceArtifact; remove EvidBlock\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01Ly6sQyweShez371NmUc4jK')"
```

---

### Task 6: Manual verification gate — screen + print/PDF

**Files:** none (verification only).

- [ ] **Step 1: Run the app and open a report**

Run:
```bash
cd manager/frontend && npm run dev
```
Open `http://localhost:3000/reports`, select an engagement with findings, open the **Technical Findings** tab.

- [ ] **Step 2: Confirm on-screen behavior**

Verify: numbered finding cards expand/collapse; severity/priority/CVSS/confidence tags render; the triage summary line shows P0 / overdue counts; severity + "Exploited or proven" + "Missing fields" filters work; the Evidence Vault tab shows artifacts with a "N values masked" note where secrets were present, and a "Reveal N" toggle.

- [ ] **Step 3: Confirm print/PDF (the `globals.css:2534` risk path)**

With the Technical tab open, invoke browser print preview (Cmd-P / Ctrl-P). Verify in the preview: the report cover and finding **headers/titles are visible** (they are `<button>`s — the module's `.vf-head { display: grid !important }` must override `globals.css`'s `button { display:none !important }`); every accordion is expanded; evidence prints the **masked** text (no secrets), with interactive buttons hidden.

- [ ] **Step 4: Record the result**

If all three steps pass, Phase 1 is complete — note it in the PR/commit description. If the print headers are missing, confirm `import "../../styles/report-finding.css"` is present in `app/reports/page.tsx` (Task 4 Step 1) and that the dev server picked it up; the fix is import presence, not order (specificity handles order).

---

## Self-Review

**Spec coverage (against `docs/superpowers/specs/2026-09-06-report-section-integration-design.md`, Phase 1):**
- New files `lib/report/finding-model.ts`, `components/report/FindingReport.tsx`, `styles/report-finding.css` → Tasks 1–2. ✅
- Adapter `lib/report/adapt.ts` with derivations → Task 3. ✅
- Ported `spec.ts` test → Task 1. ✅
- Admin wiring (Technical → FindingsSection; Evidence → EvidenceArtifact both tabs; delete TechTab/FindingCard/EvidBlock/parseCvssVector/VM_*; keep parseCvss) → Tasks 4–5. ✅
- Print handled by module CSS, no globals edit → Task 5 build + Task 6 print gate. ✅
- Risk #3 (both evidence renderers switch) → Task 5 is a dedicated, separately-gated task. ✅
- `mode` prop is **Phase 2** (portal); intentionally not in this plan — the module is copied verbatim here. Noted so a reviewer does not expect it.

**Placeholder scan:** No TBD/TODO. Every code step shows complete code or an exact copy/sed command against an in-repo source. The only "paste this region" step (Task 1 Step 2) targets a concrete, existing file with exact boundary markers and a `sed` preview.

**Type consistency:** `toRawFinding`/`deriveDetectionMethod`/`toReportAssets` names are identical across Task 3's definition, its tests, and Task 4's import. `FindingsSection`/`EvidenceArtifact` names match the module's exports (Task 2) and their imports (Tasks 4–5). `reportFindings` defined once (Task 4 Step 2) and used once (Step 3).

## Build order

Tasks are sequential: 1 (model+test) → 2 (component+css) → 3 (adapter) → 4 (Technical tab + deletions) → 5 (Evidence tab, security) → 6 (manual print gate). Each ends in a green gate and a commit.
