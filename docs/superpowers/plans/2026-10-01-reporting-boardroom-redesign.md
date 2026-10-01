# Reporting "Boardroom Deliverable" Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Elevate Vedha's report into a premium, print-ready client deliverable (cover + risk grade, data-viz band, real typography, elevated cards/tables) and fix the Remediation page export — without changing the data model or adding backend endpoints.

**Architecture:** All work is in `manager/frontend`. The report is one shared React component rendered for both the operator console and the customer portal (`surface` prop); the portal page delegates to it. The testable core is **pure data-transform + grade functions** (unit-tested with node:test); the visuals are thin recharts/CSS components that consume those functions and are verified by typecheck/build/lint + a manual pass (this repo has no DOM test harness, by design).

**Tech Stack:** Next.js 16.3.6 (customized), React 19.3.0, recharts ^3.8.1, lucide-react ^1, @tanstack/react-query, Tailwind v4, TypeScript 5, tests via `tsx --test` (node:test + node:assert/strict).

## Global Constraints

- **Branch:** `feat/reporting-boardroom-redesign` (already checked out; the design spec is already committed there).
- **Custom Next.js:** per `manager/frontend/AGENTS.md`, before using `next/font` or any Next API, read the matching guide under `node_modules/next/dist/docs/`. Do not assume stock Next behavior.
- **VERSION auto-bumps every commit** via `.githooks/pre-commit` — `VERSION` WILL appear in every commit; that is correct, do not try to remove it.
- **Shared checkout:** stage explicit paths only (`git add <path>`), never `git add -A`/`git add .`; another session shares this working tree.
- **Tests:** `npm test` runs `tsx --test tests/*.test.ts`. Use `import { describe, test } from "node:test"` + `import assert from "node:assert/strict"`. Run one file with `npx tsx --test tests/<file>.test.ts`. There is **no** @testing-library/jsdom — do not write `render(<Component/>)` tests; test pure functions, and verify components with `npm run build` + `npm run lint` + manual review.
- **Severity is UPPERCASE:** `"CRITICAL"|"HIGH"|"MEDIUM"|"LOW"|"INFO"`. Always normalize with `toSeverity()` and read colors from `SEVERITY[sev]` / `SEVERITY_ORDER` in `lib/severity.ts`. Never hardcode hex.
- **Charts:** mirror `components/DashboardCharts.tsx` — `"use client"`, import from `recharts`, wrap in `ResponsiveContainer` with an explicit pixel height so print works.
- **No new backend endpoints.** Reuse the data from `createReportsWorkspaceApi(surface)`.
- **Commit after every task.** Before each commit run `npm run lint` and `npm test` and confirm both pass.

## File Structure

**Create:**
- `lib/report/risk-grade.ts` — pure: scorecard score → A–F grade + grade color. (Task 1)
- `lib/report/chart-data.ts` — pure: findings/matrix → chart-ready data. (Task 3)
- `components/report/charts/RiskGauge.tsx` — radial gauge of the 0–100 score. (Task 5)
- `components/report/charts/SeverityDonut.tsx` — severity distribution donut. (Task 5)
- `components/report/charts/ExploitScatter.tsx` — EPSS×risk "fix-first" scatter. (Task 6)
- `components/report/charts/SlaAgingBar.tsx` — SLA bucket bar. (Task 6)
- `components/report/charts/MitreHeatmap.tsx` — technique-frequency grid (CSS). (Task 7)
- `components/report/charts/ExposureHeatmap.tsx` — severity×exploitability grid (CSS). (Task 7)
- `components/report/ReportCover.tsx` — title page. (Task 8)
- `components/report/ExecutiveBand.tsx` — composes the six charts. (Task 9)
- `styles/report-cover.css`, `styles/report-charts.css` — token-driven styles. (Tasks 8–9)
- `app/fonts/` — self-hosted font files + loader. (Task 10)
- `tests/report-risk-grade.test.ts`, `tests/report-chart-data.test.ts` — unit tests. (Tasks 1, 3)

**Modify:**
- `components/remediation/RemediationWorkspace.tsx:188-189` — bare `<a download>` → `downloadFile()`. (Task 2)
- `app/layout.tsx` — wire self-hosted fonts. (Task 10)
- `app/globals.css` — point `--font-display`/`--font-body` at the new faces; add a real type scale. (Task 10)
- `app/reports/page.tsx` — insert `<ReportCover>`/`<ExecutiveBand>`; replace inline styles with classes. (Tasks 9, 11)
- `app/reports/layout.tsx`, `app/portal/reports/layout.tsx` — import the new CSS. (Task 9)

---

### Task 1: Risk grade (pure function)

**Files:**
- Create: `manager/frontend/lib/report/risk-grade.ts`
- Test: `manager/frontend/tests/report-risk-grade.test.ts`

**Interfaces:**
- Produces: `type Grade = "A"|"B"|"C"|"D"|"F"`; `scoreToGrade(score: number): Grade`; `gradeColor(grade: Grade): string` (returns a `var(--…)` string).

- [ ] **Step 1: Write the failing test**

```ts
// tests/report-risk-grade.test.ts
import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { scoreToGrade, gradeColor } from "../lib/report/risk-grade";

describe("scoreToGrade (0 = no open risk, 100 = worst)", () => {
  test("boundaries map to A..F", () => {
    assert.equal(scoreToGrade(0), "A");
    assert.equal(scoreToGrade(9), "A");
    assert.equal(scoreToGrade(10), "B");
    assert.equal(scoreToGrade(24), "B");
    assert.equal(scoreToGrade(25), "C");
    assert.equal(scoreToGrade(44), "C");
    assert.equal(scoreToGrade(45), "D");
    assert.equal(scoreToGrade(69), "D");
    assert.equal(scoreToGrade(70), "F");
    assert.equal(scoreToGrade(100), "F");
  });
  test("clamps and rounds out-of-range / fractional input", () => {
    assert.equal(scoreToGrade(-5), "A");
    assert.equal(scoreToGrade(130), "F");
    assert.equal(scoreToGrade(9.4), "A");
    assert.equal(scoreToGrade(9.6), "B");
  });
  test("gradeColor returns a CSS var for every grade", () => {
    for (const g of ["A", "B", "C", "D", "F"] as const) {
      assert.match(gradeColor(g), /^var\(--/);
    }
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/frontend && npx tsx --test tests/report-risk-grade.test.ts`
Expected: FAIL — cannot find module `../lib/report/risk-grade`.

- [ ] **Step 3: Write minimal implementation**

```ts
// lib/report/risk-grade.ts
/**
 * Map the scorecard's open-risk score (0 = clean … 100 = worst) to a letter
 * grade for the cover page. Thresholds are calibratable; keep them in sync with
 * the cover legend. CONFIRM the score polarity against the scorecard source
 * before trusting the grade (higher === more open risk is assumed here).
 */
export type Grade = "A" | "B" | "C" | "D" | "F";

export function scoreToGrade(score: number): Grade {
  const s = Math.max(0, Math.min(100, Math.round(score)));
  if (s <= 9) return "A";
  if (s <= 24) return "B";
  if (s <= 44) return "C";
  if (s <= 69) return "D";
  return "F";
}

export function gradeColor(grade: Grade): string {
  switch (grade) {
    case "A": return "var(--nominal-color)";
    case "B": return "var(--sev-low-color)";
    case "C": return "var(--sev-medium-color)";
    case "D": return "var(--sev-high-color)";
    case "F": return "var(--sev-critical-color)";
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/frontend && npx tsx --test tests/report-risk-grade.test.ts`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/lib/report/risk-grade.ts manager/frontend/tests/report-risk-grade.test.ts
git commit -m "feat(report): score->A-F risk grade helper"
```

---

### Task 2: Fix Remediation export (bare anchor → downloadFile)

**Files:**
- Modify: `manager/frontend/components/remediation/RemediationWorkspace.tsx` (~L188–189, plus add state + handler near the component top)

**Interfaces:**
- Consumes: `downloadFile(url: string, surface: "manager"|"portal", fallbackName: string): Promise<void>` from `lib/report/download`; `api.exportUrl(engId, format, sheet?, filters?)` from the remediation api already in this component.

**Context:** The current code (verbatim, `RemediationWorkspace.tsx:188-189`):
```tsx
<a className="btn btn-secondary" href={api.exportUrl(engId, "xlsx")} download><Download size={13} aria-hidden /> Excel tracker</a>
<a className="btn btn-secondary" href={api.exportUrl(engId, "csv")} download><Download size={13} aria-hidden /> CSV</a>
```
A bare `<a download>` saves a 401/500 error body *as* the file. Use the same `downloadFile` helper the report page uses (fetch + one refresh + readable error).

- [ ] **Step 1: Determine the surface this component runs as**

Run: `cd manager/frontend && grep -nE "surface|createRemediationApi|export function RemediationWorkspace" components/remediation/RemediationWorkspace.tsx | head`
Expected: shows how `api` is created and whether a `surface: "manager"|"portal"` prop/const exists. Note the variable (call it `surface` below; if the component is operator-only, use the literal `"manager"`).

- [ ] **Step 2: Add import + download state near the other hooks at the top of the component**

```tsx
import { downloadFile } from "../../lib/report/download";
// ...inside the component, with the other useState hooks:
const [exporting, setExporting] = useState<string | null>(null);
const [exportError, setExportError] = useState<string | null>(null);

async function runExport(format: "xlsx" | "csv") {
  setExportError(null);
  setExporting(format);
  try {
    await downloadFile(api.exportUrl(engId, format), surface, `remediation.${format}`);
  } catch (e) {
    setExportError(e instanceof Error ? e.message : "Export failed.");
  } finally {
    setExporting(null);
  }
}
```

- [ ] **Step 3: Replace the two bare anchors (L188–189) with buttons**

```tsx
<button type="button" className="btn btn-secondary" disabled={exporting !== null}
  onClick={() => runExport("xlsx")}>
  <Download size={13} aria-hidden /> {exporting === "xlsx" ? "Exporting…" : "Excel tracker"}
</button>
<button type="button" className="btn btn-secondary" disabled={exporting !== null}
  onClick={() => runExport("csv")}>
  <Download size={13} aria-hidden /> {exporting === "csv" ? "Exporting…" : "CSV"}
</button>
{exportError && <span role="alert" className="report-export-error">{exportError}</span>}
```

- [ ] **Step 4: Typecheck + lint + build**

Run: `cd manager/frontend && npm run lint && npm run build`
Expected: no type errors; build succeeds. (No unit test — there is no DOM harness; this is a wiring change verified by typecheck/build and the manual check in Step 5.)

- [ ] **Step 5: Manual verify**

With a dev stack signed in, click Excel/CSV on the Remediation page → a real file downloads; sign out and retry → a readable "session expired" message instead of a saved error page.

- [ ] **Step 6: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/components/remediation/RemediationWorkspace.tsx
git commit -m "fix(remediation): route exports through downloadFile (no error-body files)"
```

> Deploy note (not code): the live "can't export" is a stale deploy over plain HTTP — redeploy current `main` and/or serve HTTPS via `./setup-https.sh`. Track this in `docs/STATUS.md`, not here.

---

### Task 3: Chart data transforms (pure functions)

**Files:**
- Create: `manager/frontend/lib/report/chart-data.ts`
- Test: `manager/frontend/tests/report-chart-data.test.ts`

**Interfaces:**
- Consumes: `Severity`, `SEVERITY`, `SEVERITY_ORDER`, `toSeverity` from `lib/severity`.
- Produces (the component maps the real report finding onto `ChartFinding`, keeping these functions pure/testable):
```ts
export interface ChartFinding {
  severity: Severity;            // normalized via toSeverity()
  epss: number | null;           // 0..1
  riskScore: number | null;      // 0..1000
  kev: boolean;
  mitre: string[];               // technique ids, may be empty
  sla: "ok" | "due_soon" | "overdue" | null;
}
export interface DonutDatum { severity: Severity; label: string; count: number; color: string; }
export interface ScatterDatum { epss: number; risk: number; severity: Severity; color: string; kev: boolean; }
export interface SlaDatum { bucket: "ok" | "due_soon" | "overdue"; label: string; count: number; }
export interface MitreCell { technique: string; count: number; }
export function severityDonutData(fs: ChartFinding[]): DonutDatum[];
export function exploitScatterData(fs: ChartFinding[]): ScatterDatum[];
export function slaAgingData(fs: ChartFinding[]): SlaDatum[];
export function mitreHeatmapData(fs: ChartFinding[], top?: number): MitreCell[];
```

- [ ] **Step 1: Write the failing test**

```ts
// tests/report-chart-data.test.ts
import assert from "node:assert/strict";
import { describe, test } from "node:test";
import {
  severityDonutData, exploitScatterData, slaAgingData, mitreHeatmapData,
  type ChartFinding,
} from "../lib/report/chart-data";

const F = (p: Partial<ChartFinding>): ChartFinding => ({
  severity: "LOW", epss: null, riskScore: null, kev: false, mitre: [], sla: null, ...p,
});

describe("severityDonutData", () => {
  test("counts by severity in CRITICAL..INFO order, zeros omitted", () => {
    const d = severityDonutData([F({ severity: "CRITICAL" }), F({ severity: "CRITICAL" }), F({ severity: "LOW" })]);
    assert.deepEqual(d.map((x) => [x.severity, x.count]), [["CRITICAL", 2], ["LOW", 1]]);
    assert.match(d[0].color, /^var\(--/);
  });
  test("empty input -> empty array", () => {
    assert.deepEqual(severityDonutData([]), []);
  });
});

describe("exploitScatterData", () => {
  test("only findings with both epss and riskScore; carries kev + color", () => {
    const d = exploitScatterData([
      F({ severity: "HIGH", epss: 0.8, riskScore: 700, kev: true }),
      F({ epss: null, riskScore: 500 }),
      F({ epss: 0.2, riskScore: null }),
    ]);
    assert.equal(d.length, 1);
    assert.deepEqual([d[0].epss, d[0].risk, d[0].kev], [0.8, 700, true]);
  });
});

describe("slaAgingData", () => {
  test("buckets ok/due_soon/overdue, nulls ignored, fixed order", () => {
    const d = slaAgingData([F({ sla: "overdue" }), F({ sla: "overdue" }), F({ sla: "ok" }), F({ sla: null })]);
    assert.deepEqual(d.map((x) => [x.bucket, x.count]), [["ok", 1], ["due_soon", 0], ["overdue", 2]]);
  });
});

describe("mitreHeatmapData", () => {
  test("technique frequency, descending, top-N", () => {
    const d = mitreHeatmapData([F({ mitre: ["T1"] }), F({ mitre: ["T1", "T2"] }), F({ mitre: ["T3"] })], 2);
    assert.deepEqual(d, [{ technique: "T1", count: 2 }, { technique: "T2", count: 1 }]);
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd manager/frontend && npx tsx --test tests/report-chart-data.test.ts`
Expected: FAIL — module not found.

- [ ] **Step 3: Write minimal implementation**

```ts
// lib/report/chart-data.ts
import { SEVERITY, SEVERITY_ORDER, type Severity } from "../severity";

export interface ChartFinding {
  severity: Severity;
  epss: number | null;
  riskScore: number | null;
  kev: boolean;
  mitre: string[];
  sla: "ok" | "due_soon" | "overdue" | null;
}
export interface DonutDatum { severity: Severity; label: string; count: number; color: string; }
export interface ScatterDatum { epss: number; risk: number; severity: Severity; color: string; kev: boolean; }
export interface SlaDatum { bucket: "ok" | "due_soon" | "overdue"; label: string; count: number; }
export interface MitreCell { technique: string; count: number; }

export function severityDonutData(fs: ChartFinding[]): DonutDatum[] {
  const counts = new Map<Severity, number>();
  for (const f of fs) counts.set(f.severity, (counts.get(f.severity) ?? 0) + 1);
  return SEVERITY_ORDER.flatMap((s) => {
    const count = counts.get(s) ?? 0;
    return count === 0 ? [] : [{ severity: s, label: SEVERITY[s].label, count, color: SEVERITY[s].color }];
  });
}

export function exploitScatterData(fs: ChartFinding[]): ScatterDatum[] {
  return fs.flatMap((f) =>
    f.epss != null && f.riskScore != null
      ? [{ epss: f.epss, risk: f.riskScore, severity: f.severity, color: SEVERITY[f.severity].color, kev: f.kev }]
      : []);
}

const SLA_ORDER: SlaDatum["bucket"][] = ["ok", "due_soon", "overdue"];
const SLA_LABEL: Record<SlaDatum["bucket"], string> = { ok: "On track", due_soon: "Due soon", overdue: "Overdue" };
export function slaAgingData(fs: ChartFinding[]): SlaDatum[] {
  const counts = new Map<SlaDatum["bucket"], number>();
  for (const f of fs) if (f.sla) counts.set(f.sla, (counts.get(f.sla) ?? 0) + 1);
  return SLA_ORDER.map((b) => ({ bucket: b, label: SLA_LABEL[b], count: counts.get(b) ?? 0 }));
}

export function mitreHeatmapData(fs: ChartFinding[], top = 20): MitreCell[] {
  const counts = new Map<string, number>();
  for (const f of fs) for (const t of f.mitre) counts.set(t, (counts.get(t) ?? 0) + 1);
  return [...counts.entries()]
    .map(([technique, count]) => ({ technique, count }))
    .sort((a, b) => b.count - a.count || a.technique.localeCompare(b.technique))
    .slice(0, top);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd manager/frontend && npx tsx --test tests/report-chart-data.test.ts`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/lib/report/chart-data.ts manager/frontend/tests/report-chart-data.test.ts
git commit -m "feat(report): pure chart-data transforms (donut/scatter/sla/mitre)"
```

---

### Task 4: Find the real finding + scorecard fields and write the ChartFinding adapter

**Files:**
- Modify: `manager/frontend/lib/report/chart-data.ts` (add one adapter at the bottom)
- Test: `manager/frontend/tests/report-chart-data.test.ts` (add one case)

**Interfaces:**
- Produces: `toChartFinding(f: <ReportFinding>): ChartFinding` — maps the report page's finding object onto `ChartFinding`.

- [ ] **Step 1: Identify the real field names**

Run:
```bash
cd manager/frontend
sed -n '79,200p' lib/report/finding-model.ts   # the RawFinding + assessed type (epss/cvss/kev/mitre/dueAt)
grep -nE 'epss|kev|activelyExploited|mitre|dueAt|riskScore|openRisk|score' lib/report/finding-model.ts lib/reports-workspace-api.ts | head -30
```
Record the exact property names for: severity, epss (0–1), risk score (0–1000), KEV/actively-exploited boolean, MITRE technique list, and the SLA/due state. Record the scorecard's 0–100 open-risk field name.

- [ ] **Step 2: Write the failing test for the adapter** (fill in the real field names found)

```ts
import { toChartFinding } from "../lib/report/chart-data";
test("toChartFinding maps a report finding onto ChartFinding", () => {
  const cf = toChartFinding({ /* minimal real finding shape from Step 1 */ } as any);
  assert.equal(cf.severity, "HIGH");       // normalized uppercase
  assert.equal(typeof cf.kev, "boolean");
  assert.ok(Array.isArray(cf.mitre));
});
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd manager/frontend && npx tsx --test tests/report-chart-data.test.ts`
Expected: FAIL — `toChartFinding` not exported.

- [ ] **Step 4: Implement the adapter using the real field names**

```ts
import { toSeverity } from "../severity";
// Replace the bracketed accessors with the real property names from Step 1.
export function toChartFinding(f: {
  severity: string; epss?: number | null; epssPercentile?: number | null;
  riskScore?: number | null; kev?: boolean; activelyExploited?: boolean;
  mitre?: string[]; sla?: "ok" | "due_soon" | "overdue" | null;
}): ChartFinding {
  return {
    severity: toSeverity(f.severity),
    epss: f.epss ?? null,
    riskScore: f.riskScore ?? null,
    kev: Boolean(f.kev || f.activelyExploited),
    mitre: Array.isArray(f.mitre) ? f.mitre : [],
    sla: f.sla ?? null,
  };
}
```

- [ ] **Step 5: Run tests** — `cd manager/frontend && npx tsx --test tests/report-chart-data.test.ts` → PASS.

- [ ] **Step 6: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/lib/report/chart-data.ts manager/frontend/tests/report-chart-data.test.ts
git commit -m "feat(report): map report finding -> ChartFinding"
```

---

### Task 5: RiskGauge + SeverityDonut components

**Files:**
- Create: `components/report/charts/RiskGauge.tsx`, `components/report/charts/SeverityDonut.tsx`
- Create: `styles/report-charts.css`

**Interfaces:**
- Consumes: `severityDonutData`, `DonutDatum` (Task 3); `scoreToGrade`, `gradeColor` (Task 1).
- Produces: `<RiskGauge score={number} />`, `<SeverityDonut findings={ChartFinding[]} />`.

- [ ] **Step 1: RiskGauge** (recharts `RadialBarChart`, mirrors DashboardCharts' client+ResponsiveContainer pattern)

```tsx
"use client";
import { RadialBarChart, RadialBar, PolarAngleAxis, ResponsiveContainer } from "recharts";
import { scoreToGrade, gradeColor } from "../../../lib/report/risk-grade";

export function RiskGauge({ score }: { score: number }) {
  const s = Math.max(0, Math.min(100, Math.round(score)));
  const grade = scoreToGrade(s);
  const color = gradeColor(grade);
  return (
    <div className="rpt-chart rpt-gauge">
      <div className="rpt-gauge-wrap" style={{ width: 160, height: 160 }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart innerRadius="78%" outerRadius="100%" data={[{ v: s, fill: color }]}
            startAngle={225} endAngle={-45}>
            <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
            <RadialBar background dataKey="v" cornerRadius={8} />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="rpt-gauge-center">
          <div className="rpt-gauge-grade" style={{ color }}>{grade}</div>
          <div className="rpt-gauge-score">{s}<span>/100</span></div>
        </div>
      </div>
      <div className="rpt-chart-title">Open risk</div>
    </div>
  );
}
```

- [ ] **Step 2: SeverityDonut** (recharts `PieChart`)

```tsx
"use client";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { severityDonutData } from "../../../lib/report/chart-data";
import type { ChartFinding } from "../../../lib/report/chart-data";

export function SeverityDonut({ findings }: { findings: ChartFinding[] }) {
  const data = severityDonutData(findings);
  if (data.length === 0) return <div className="rpt-chart rpt-empty">No findings</div>;
  return (
    <div className="rpt-chart">
      <div style={{ width: "100%", height: 180 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie data={data} dataKey="count" nameKey="label" innerRadius="60%" outerRadius="100%" paddingAngle={2}>
              {data.map((d) => <Cell key={d.severity} fill={d.color} />)}
            </Pie>
            <Tooltip formatter={(v: number, _n, p) => [`${v}`, (p?.payload as { label?: string })?.label ?? ""]} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="rpt-chart-title">Severity</div>
    </div>
  );
}
```

- [ ] **Step 3: Seed `styles/report-charts.css`** (token-driven; print-safe)

```css
.rpt-chart { display: flex; flex-direction: column; align-items: center; gap: var(--space-2); }
.rpt-chart-title { font: 600 var(--fs-label)/1 var(--font-body); text-transform: uppercase; letter-spacing: .06em; color: var(--text-muted); }
.rpt-empty { color: var(--text-muted); font-size: var(--fs-body-s); padding: var(--space-6); }
.rpt-gauge-wrap { position: relative; }
.rpt-gauge-center { position: absolute; inset: 0; display: grid; place-content: center; text-align: center; }
.rpt-gauge-grade { font: 700 var(--fs-display-l)/1 var(--font-display); }
.rpt-gauge-score { font-size: var(--fs-body-s); color: var(--text-muted); }
.rpt-gauge-score span { opacity: .6; }
@media print { .rpt-chart { break-inside: avoid; } }
```

- [ ] **Step 4: Typecheck + build**

Run: `cd manager/frontend && npm run lint && npm run build`
Expected: compiles; no type errors.

- [ ] **Step 5: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/components/report/charts/RiskGauge.tsx manager/frontend/components/report/charts/SeverityDonut.tsx manager/frontend/styles/report-charts.css
git commit -m "feat(report): RiskGauge + SeverityDonut charts"
```

---

### Task 6: ExploitScatter + SlaAgingBar components

**Files:**
- Create: `components/report/charts/ExploitScatter.tsx`, `components/report/charts/SlaAgingBar.tsx`

**Interfaces:**
- Consumes: `exploitScatterData`, `slaAgingData` (Task 3), `SEVERITY` for SLA bar colors.
- Produces: `<ExploitScatter findings={ChartFinding[]} />`, `<SlaAgingBar findings={ChartFinding[]} />`.

- [ ] **Step 1: ExploitScatter** (recharts `ScatterChart`; x=EPSS, y=risk; "fix-first" = top-right)

```tsx
"use client";
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, Cell, ResponsiveContainer } from "recharts";
import { exploitScatterData } from "../../../lib/report/chart-data";
import type { ChartFinding } from "../../../lib/report/chart-data";

export function ExploitScatter({ findings }: { findings: ChartFinding[] }) {
  const data = exploitScatterData(findings);
  if (data.length === 0) return <div className="rpt-chart rpt-empty">No EPSS-scored findings</div>;
  return (
    <div className="rpt-chart">
      <div style={{ width: "100%", height: 200 }}>
        <ResponsiveContainer>
          <ScatterChart margin={{ top: 8, right: 12, bottom: 20, left: 0 }}>
            <XAxis type="number" dataKey="epss" domain={[0, 1]} name="EPSS"
              tick={{ fontSize: 10 }} label={{ value: "Exploit likelihood (EPSS)", position: "bottom", fontSize: 10 }} />
            <YAxis type="number" dataKey="risk" domain={[0, 1000]} name="Risk" tick={{ fontSize: 10 }} />
            <ZAxis range={[40, 160]} />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter data={data}>
              {data.map((d, i) => <Cell key={i} fill={d.color} stroke={d.kev ? "var(--text)" : "none"} strokeWidth={d.kev ? 1.5 : 0} />)}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>
      <div className="rpt-chart-title">Fix-first (EPSS × risk · ring = KEV)</div>
    </div>
  );
}
```

- [ ] **Step 2: SlaAgingBar** (recharts `BarChart`)

```tsx
"use client";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ResponsiveContainer } from "recharts";
import { slaAgingData } from "../../../lib/report/chart-data";
import type { ChartFinding } from "../../../lib/report/chart-data";

const SLA_FILL = { ok: "var(--nominal-color)", due_soon: "var(--sev-medium-color)", overdue: "var(--sev-critical-color)" } as const;

export function SlaAgingBar({ findings }: { findings: ChartFinding[] }) {
  const data = slaAgingData(findings);
  if (data.every((d) => d.count === 0)) return <div className="rpt-chart rpt-empty">No SLA data</div>;
  return (
    <div className="rpt-chart">
      <div style={{ width: "100%", height: 180 }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
            <XAxis dataKey="label" tick={{ fontSize: 10 }} />
            <YAxis allowDecimals={false} tick={{ fontSize: 10 }} />
            <Tooltip />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {data.map((d) => <Cell key={d.bucket} fill={SLA_FILL[d.bucket]} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="rpt-chart-title">SLA status</div>
    </div>
  );
}
```

- [ ] **Step 3: Typecheck + build** — `cd manager/frontend && npm run lint && npm run build` → passes.

- [ ] **Step 4: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/components/report/charts/ExploitScatter.tsx manager/frontend/components/report/charts/SlaAgingBar.tsx
git commit -m "feat(report): ExploitScatter + SlaAgingBar charts"
```

---

### Task 7: MitreHeatmap + ExposureHeatmap (CSS grids)

**Files:**
- Create: `components/report/charts/MitreHeatmap.tsx`, `components/report/charts/ExposureHeatmap.tsx`
- Modify: `styles/report-charts.css` (grid cell styles)

**Interfaces:**
- Consumes: `mitreHeatmapData` (Task 3). For exposure, consume the existing exposure-matrix object from the report data (confirm its shape in Step 1) — render as a severity×exploitability grid of colored cells (replaces today's plain HTML table).
- Produces: `<MitreHeatmap findings={ChartFinding[]} />`, `<ExposureHeatmap matrix={<ExposureMatrix>} />`.

- [ ] **Step 1: Confirm the exposure-matrix shape**

Run: `cd manager/frontend && grep -nE 'exposure|Exposure|exploitability' lib/reports-workspace-api.ts lib/report/*.ts | head`
Record the exact object shape (rows = severity, cols = exploitability, cell = count).

- [ ] **Step 2: MitreHeatmap** (frequency grid; intensity by count)

```tsx
"use client";
import { mitreHeatmapData } from "../../../lib/report/chart-data";
import type { ChartFinding } from "../../../lib/report/chart-data";

export function MitreHeatmap({ findings }: { findings: ChartFinding[] }) {
  const cells = mitreHeatmapData(findings, 24);
  if (cells.length === 0) return <div className="rpt-chart rpt-empty">No MITRE mappings</div>;
  const max = Math.max(...cells.map((c) => c.count));
  return (
    <div className="rpt-chart">
      <div className="rpt-heatgrid">
        {cells.map((c) => (
          <a key={c.technique} className="rpt-heatcell"
            href={`https://attack.mitre.org/techniques/${c.technique.replace(".", "/")}/`}
            target="_blank" rel="noreferrer"
            style={{ ["--i" as string]: String(c.count / max) }}>
            <span className="rpt-heat-t">{c.technique}</span><span className="rpt-heat-n">{c.count}</span>
          </a>
        ))}
      </div>
      <div className="rpt-chart-title">MITRE ATT&CK coverage</div>
    </div>
  );
}
```

- [ ] **Step 3: ExposureHeatmap** — build a grid from the confirmed matrix shape (fill each cell `background: color-mix(in srgb, var(--sev-…-color) calc(var(--i)*100%), transparent)`), using the real row/col keys from Step 1.

- [ ] **Step 4: Heatmap CSS** (append to `styles/report-charts.css`)

```css
.rpt-heatgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(84px, 1fr)); gap: var(--space-1); width: 100%; }
.rpt-heatcell { display: flex; justify-content: space-between; gap: 6px; padding: 6px 8px; border-radius: var(--radius-sm);
  font: 600 var(--fs-label)/1 var(--font-mono); text-decoration: none; color: var(--text);
  background: color-mix(in srgb, var(--accent) calc(var(--i) * 72%), var(--bg-surface)); }
.rpt-heat-n { color: var(--text-muted); }
@media print { .rpt-heatcell { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
```

- [ ] **Step 5: Typecheck + build** — passes.

- [ ] **Step 6: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/components/report/charts/MitreHeatmap.tsx manager/frontend/components/report/charts/ExposureHeatmap.tsx manager/frontend/styles/report-charts.css
git commit -m "feat(report): MITRE + exposure heatmaps"
```

---

### Task 8: ReportCover (title page)

**Files:**
- Create: `components/report/ReportCover.tsx`, `styles/report-cover.css`

**Interfaces:**
- Consumes: `scoreToGrade`, `gradeColor` (Task 1); `SEVERITY`, `SEVERITY_ORDER` for the count strip.
- Produces: `<ReportCover meta={{ engagement: string; client: string; window: string; assessor: string; scope: string }} score={number} counts={Record<Severity, number>} />`.

- [ ] **Step 1: Component**

```tsx
"use client";
import { scoreToGrade, gradeColor } from "../../lib/report/risk-grade";
import { SEVERITY, SEVERITY_ORDER, type Severity } from "../../lib/severity";

export function ReportCover({ meta, score, counts }: {
  meta: { engagement: string; client: string; window: string; assessor: string; scope: string };
  score: number; counts: Record<Severity, number>;
}) {
  const grade = scoreToGrade(score);
  return (
    <section className="rpt-cover">
      <div className="rpt-cover-band">CONFIDENTIAL — PREPARED FOR {meta.client.toUpperCase()}</div>
      <h1 className="rpt-cover-title">Security Assessment</h1>
      <p className="rpt-cover-sub">{meta.engagement}</p>
      <div className="rpt-cover-grade">
        <div className="rpt-cover-letter" style={{ color: gradeColor(grade) }}>{grade}</div>
        <div className="rpt-cover-score">Open-risk score {Math.round(score)}/100</div>
      </div>
      <ul className="rpt-cover-counts">
        {SEVERITY_ORDER.map((s) => (
          <li key={s}><b style={{ color: SEVERITY[s].color }}>{counts[s] ?? 0}</b> {SEVERITY[s].label}</li>
        ))}
      </ul>
      <dl className="rpt-cover-meta">
        <div><dt>Client</dt><dd>{meta.client}</dd></div>
        <div><dt>Window</dt><dd>{meta.window}</dd></div>
        <div><dt>Assessor</dt><dd>{meta.assessor}</dd></div>
        <div><dt>Scope</dt><dd>{meta.scope}</dd></div>
      </dl>
    </section>
  );
}
```

- [ ] **Step 2: `styles/report-cover.css`** (serif display, owns page 1 in print)

```css
.rpt-cover { display: flex; flex-direction: column; gap: var(--space-5); padding: var(--space-8) var(--space-6); }
.rpt-cover-band { font: 600 var(--fs-label)/1 var(--font-body); letter-spacing: .12em; color: var(--sev-critical-color); }
.rpt-cover-title { font: 700 var(--fs-display-xl)/1.05 var(--font-display); margin: 0; }
.rpt-cover-sub { font-size: var(--fs-display-s); color: var(--text-muted); margin: 0; }
.rpt-cover-letter { font: 800 clamp(64px, 16vw, 128px)/1 var(--font-display); }
.rpt-cover-score { font-size: var(--fs-body); color: var(--text-muted); }
.rpt-cover-counts { display: flex; gap: var(--space-5); list-style: none; padding: 0; margin: 0; font-size: var(--fs-body); }
.rpt-cover-counts b { font: 700 var(--fs-display-s)/1 var(--font-display); margin-right: 6px; }
.rpt-cover-meta { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-3) var(--space-6); margin: 0; }
.rpt-cover-meta dt { font-size: var(--fs-label); text-transform: uppercase; letter-spacing: .06em; color: var(--text-muted); }
.rpt-cover-meta dd { margin: 0; font-size: var(--fs-body); }
@media print { .rpt-cover { break-after: page; min-height: 92vh; justify-content: center; } }
```

- [ ] **Step 3: Typecheck + build** — passes.

- [ ] **Step 4: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/components/report/ReportCover.tsx manager/frontend/styles/report-cover.css
git commit -m "feat(report): boardroom cover page with risk grade"
```

---

### Task 9: ExecutiveBand + wire cover/band into the report page

**Files:**
- Create: `components/report/ExecutiveBand.tsx`
- Modify: `app/reports/page.tsx` (insert `<ReportCover>` + `<ExecutiveBand>` where today's cover header + ExecTab render; map findings via `toChartFinding`)
- Modify: `app/reports/layout.tsx`, `app/portal/reports/layout.tsx` (add CSS imports)

**Interfaces:**
- Consumes: all chart components (Tasks 5–7), `ReportCover` (Task 8), `toChartFinding` (Task 4).
- Produces: `<ExecutiveBand findings={ChartFinding[]} score={number} />`.

- [ ] **Step 1: ExecutiveBand**

```tsx
"use client";
import { RiskGauge } from "./charts/RiskGauge";
import { SeverityDonut } from "./charts/SeverityDonut";
import { ExploitScatter } from "./charts/ExploitScatter";
import { SlaAgingBar } from "./charts/SlaAgingBar";
import { MitreHeatmap } from "./charts/MitreHeatmap";
import type { ChartFinding } from "../../lib/report/chart-data";

export function ExecutiveBand({ findings, score }: { findings: ChartFinding[]; score: number }) {
  return (
    <section className="rpt-exec-band">
      <RiskGauge score={score} />
      <SeverityDonut findings={findings} />
      <ExploitScatter findings={findings} />
      <SlaAgingBar findings={findings} />
      <MitreHeatmap findings={findings} />
    </section>
  );
}
```
Add to `styles/report-charts.css`:
```css
.rpt-exec-band { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: var(--space-5);
  padding: var(--space-6); border: 1px solid var(--border); border-radius: var(--radius-lg); background: var(--bg-panel); }
@media print { .rpt-exec-band { break-inside: avoid; } }
```

- [ ] **Step 2: Add CSS imports to both report layouts**

In `app/reports/layout.tsx` and `app/portal/reports/layout.tsx`, next to the existing report CSS import add:
```tsx
import "../../styles/report-cover.css";
import "../../styles/report-charts.css";
```
(Adjust the relative depth to match each file.)

- [ ] **Step 3: Wire into `app/reports/page.tsx`**

Run first: `cd manager/frontend && grep -nE 'report-cover|ExecTab|FindingsSection|<main' app/reports/page.tsx | head` to find the exact insertion point. Then: build the `ChartFinding[]` once from the page's findings (`const chartFindings = findings.map(toChartFinding)`), read the scorecard's 0–100 score, replace the old `<dl>`-grid cover header with `<ReportCover …/>`, and render `<ExecutiveBand findings={chartFindings} score={score} />` immediately below it (above the old metric tiles). Keep the existing FindingsSection/CVE/coverage sections.

- [ ] **Step 4: Typecheck + build + manual** — `npm run lint && npm run build`; then load `/reports` (operator) and `/portal/reports`, confirm cover + charts render in light and dark, and print preview breaks the cover onto page 1 with charts intact.

- [ ] **Step 5: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/components/report/ExecutiveBand.tsx manager/frontend/app/reports/page.tsx manager/frontend/app/reports/layout.tsx manager/frontend/app/portal/reports/layout.tsx manager/frontend/styles/report-charts.css
git commit -m "feat(report): executive viz band + cover wired into both surfaces"
```

---

### Task 10: Typography (self-hosted display + body)

**Files:**
- Create: `app/fonts/` (font files + `app/fonts.ts` loader)
- Modify: `app/layout.tsx`, `app/globals.css`

- [ ] **Step 1: Read the custom-Next font guide FIRST**

Run: `ls manager/frontend/node_modules/next/dist/docs/ 2>/dev/null; grep -rl "next/font" manager/frontend/node_modules/next/dist/docs/ 2>/dev/null | head`
Read the relevant guide to confirm `next/font/local` usage in THIS Next build (AGENTS.md requirement). If `next/font/local` is unsupported, fall back to `@font-face` in `globals.css` with WOFF2 files under `public/fonts/` — the rest of this task is identical except the var wiring.

- [ ] **Step 2: Add OFL font files** (display: Source Serif 4; body: Inter) as WOFF2 under `app/fonts/`, and a loader `app/fonts.ts` exporting two `next/font/local` instances with `variable: "--font-display"` and `variable: "--font-body"`, `display: "swap"`.

- [ ] **Step 3: Apply the font variables on `<body>`** in `app/layout.tsx`:
```tsx
import { display, body } from "./fonts";
// <body className={`antialiased ${display.variable} ${body.variable}`} …>
```

- [ ] **Step 4: Point the tokens at the faces** — in `app/globals.css` `:root`, change `--font-display` and `--font-body` to begin with the loaded variables, keeping the system stack as fallback:
```css
--font-display: var(--font-display-face, "Source Serif 4"), Georgia, "Times New Roman", serif;
--font-body:    var(--font-body-face, "Inter"), -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```
(Map the `next/font` `variable` names to `--font-display-face`/`--font-body-face`, or set `--font-display`/`--font-body` directly to the font `.variable` if that is what the loader exposes — confirm against Step 1.)

- [ ] **Step 5: Build + manual** — `npm run build`; confirm the cover title and section heads render in the serif, body in Inter, no FOIT, and no network calls to an external font host (self-hosted).

- [ ] **Step 6: Commit**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/app/fonts manager/frontend/app/fonts.ts manager/frontend/app/layout.tsx manager/frontend/app/globals.css
git commit -m "feat(report): self-hosted serif display + sans body typography"
```

---

### Task 11: Token/inline-style cleanup + table elevation in page.tsx

**Files:**
- Modify: `app/reports/page.tsx` (replace inline `style={{}}` with classes)
- Modify: `styles/report-charts.css` or a new `styles/report-layout.css` (the extracted classes), `app/globals.css` (table styles)

- [ ] **Step 1: Inventory the inline styles**

Run: `cd manager/frontend && grep -nE 'style=\{\{' app/reports/page.tsx | wc -l; grep -nE 'style=\{\{' app/reports/page.tsx | head -40`
Work in batches of ~15–20. For each, add a token-driven class to the CSS file and swap the inline object for `className`. Use existing tokens (`--space-*`, `--fs-*`, `--radius-*`); never reintroduce hardcoded px where a token exists.

- [ ] **Step 2: Elevate tables** — add to `app/globals.css` (scoped to the report):
```css
.report-document .report-table tbody tr:nth-child(odd) { background: var(--bg-surface); }
.report-document .report-table thead th { position: sticky; top: 0; background: var(--bg-panel); z-index: 1; }
.report-document .report-table td, .report-document .report-table th { font-size: var(--fs-body-s); }
@media print { .report-document .report-table thead th { position: static; } }
```

- [ ] **Step 3: After each batch** — `npm run lint && npm run build`, visually diff `/reports` before/after (screenshot), confirm no layout regression.

- [ ] **Step 4: Commit per batch**

```bash
cd "$(git rev-parse --show-toplevel)"
git add manager/frontend/app/reports/page.tsx manager/frontend/styles/report-layout.css manager/frontend/app/globals.css
git commit -m "refactor(report): inline styles -> tokens; elevate tables (batch N)"
```

---

### Task 12: Final verification pass

- [ ] **Step 1:** `cd manager/frontend && npm test` — all node tests pass (incl. the new risk-grade + chart-data suites).
- [ ] **Step 2:** `npm run lint && npm run build` — clean.
- [ ] **Step 3:** Manual: `/reports` and `/portal/reports` in light + dark; client/PDF print preview (cover on its own page, charts render, internal-only sections omitted in client mode); Remediation Excel/CSV export downloads a real file and shows a readable error when signed out.
- [ ] **Step 4:** Update `docs/STATUS.md` (done/pending/needs-you/change log) — note the redesign landed and the export deploy fix (redeploy `main` / HTTPS) under needs-you. Commit:

```bash
cd "$(git rev-parse --show-toplevel)"
git add docs/STATUS.md
git commit -m "docs(status): reporting boardroom redesign landed; export = redeploy main"
```

---

## Self-Review

**Spec coverage:** cover/grade → Tasks 1,8; viz band (6 charts) → Tasks 3,5,6,7,9; finding cards note → tables in Task 11 (card spine/chips fold into the existing `FindingReport.tsx`; add as a follow-up batch in Task 11 if desired); typography → Task 10; inline-style cleanup → Task 11; export fix → Task 2; both surfaces/print → Task 9; testing → Tasks 1,3,4,12. **Gap noted:** finding-card chip/spine polish is lighter than the spec's §5.3 — the exposure-matrix cell colors and the card header chips depend on real field names confirmed in Tasks 4/7 Step 1; treat those confirmations as blocking sub-steps.

**Placeholders:** pure-function tasks (1,3,4) carry complete runnable code + tests. Component tasks carry complete real recharts/JSX. The two "confirm the real field name" steps (Tasks 4,7) are explicit lookup steps with exact commands, not vague TODOs — they exist because the report finding/exposure types were not read verbatim here.

**Type consistency:** `ChartFinding`, `DonutDatum`, `ScatterDatum`, `SlaDatum`, `MitreCell`, `Grade`, `scoreToGrade`, `gradeColor`, `toChartFinding` are used consistently across tasks; severity is the uppercase `Severity` union throughout; `downloadFile(url, surface, fallbackName)` matches `lib/report/download.ts`.
