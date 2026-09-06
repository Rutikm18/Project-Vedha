# Technical findings — integration

Three files. Drop-in against the current `/api/findings` payload: every new field
is optional, so nothing breaks and the extra sections light up as the scanner
starts recording more.

```
lib/report/finding-model.ts        judgement + derivation (no JSX, unit-testable)
components/report/FindingReport.tsx layout only (no decisions)
styles/report-finding.css          SIGNAL tokens throughout, themes for free
```

## Wiring

In `app/.../reports/page.tsx`:

```diff
+ import { FindingsSection, EvidenceArtifact } from "../../components/report/FindingReport";
+ import "../../styles/report-finding.css";   // must come after globals.css

- {tab === "technical" && <TechTab findings={findings} total={summary.total} />}
+ {tab === "technical" && <FindingsSection findings={findings} total={summary.total} />}
```

Then delete `TechTab` and `FindingCard`. Keep `EvidBlock` only until the Evidence
Vault is switched over — **do switch it**:

```diff
- <EvidBlock item={item} />
+ <EvidenceArtifact item={item} refId={`${item.finding.id}/E${i + 1}`} />
```

Until you do, the vault renders raw `content` while the findings tab masks it.
Anything redacted in one tab is still sitting in the other, and in the same PDF.

The page's `Finding` interface is structurally assignable to `RawFinding`, so no
cast is needed. You can drop the local `parseCvss`, `parseCvssVector`, `VM_LABEL`
and `VM_NAME` helpers — the model supersedes them and also handles CVSS 4.0.

## Two upstream bugs this surfaced

**1. `globals.css` breaks PDF export.** The last rule in the file is:

```css
@media print { .no-print, nav, aside, header, footer, button { display: none !important; } }
```

Those bare element selectors hide the report cover (`<header class="report-cover">`),
the report footer, and every finding title — the card header is a `<button>`.
The "Export PDF" button currently produces a document with no cover and no
finding headings. `report-finding.css` puts them back with `display: revert`,
which is why it must be imported after globals. The real fix is to scope those
selectors to the app chrome (`.vedha-page-main > header`, etc.).

**2. A collapsed accordion prints as a list of headings.** `FindingsSection`
listens for `beforeprint`, expands everything with `flushSync` so the commit
lands before the browser paginates, and restores the assessor's state on
`afterprint`.

## API contract

Everything below is optional. Recommended order of work — each row is roughly
what it buys.

| Field | Type | What it unlocks |
|---|---|---|
| `detectionMethod` | `"exploit" \| "behavioural" \| "configuration" \| "credentialed" \| "version" \| "banner" \| "inference"` | Confidence. Without it every finding reads "Unverified". **Highest value per unit of work.** |
| `epss`, `epssPercentile` | `number` 0–1 | Probability signal; feeds priority |
| `exploitValidated` | `boolean` | "Reproduced during this assessment" — the strongest claim in the report |
| `internetReachable` | `boolean` | Exposure; feeds priority. `false` is meaningful, don't send `null` for it |
| `verification` | `{ method?, command?, expected, retain? }` | The retest block. `expected` is the delivery blocker |
| `assets[]` | `{ host, ip?, port?, service?, version?, environment?, owner?, internetReachable? }` | The affected-assets table. Falls back to `affectedHost` as a single row |
| `evidence[].tool/command/capturedAt/capturedBy/sourceHost/sha256` | `string` | Chain of custody. Incomplete custody is called out on the artifact |
| `remediation[].tier` | `"containment" \| "fix" \| "hardening"` | Groups the fix into contain-now / fix-properly / stop-it-recurring. Untiered steps default to `fix` |
| `rootCause`, `prerequisites[]`, `attackPath[]` | `string`, `string[]` | Technical detail subsections |
| `kevAddedAt`, `exploitPublic`, `severityRationale`, `severityAdjustedFrom`, `advisories[]`, `compliance[]`, `dueAt`, `retestedAt`, `assignedTo` | | Incremental |

## Policy you will want to change

`SLA_DAYS` in the model is the remediation clock: P0 3 days, P1 7, P2 30, P3 90,
P4 none. It is stated in the UI as engagement policy, not as a regulatory
requirement, because that is what it is. A per-finding `dueAt` always overrides it.

## Tests

`_check/spec.ts` covers priority, the SLA clock, CVSS 3.1 and 4.0 reading,
confidence, redaction and the missing-data paths — 58 assertions. Two of them are
regressions for bugs found writing it:

- `String.replace` passes `(match, ...groups, offset, subject)`; filtering the
  callback args on `typeof === "string"` kept the whole subject as a trailing
  group, which corrupted redacted output.
- `Math.ceil` on a negative rounds toward zero, so a finding twelve hours past
  its target computed `-0`, and `-0 < 0` is false — it rendered as on-track.
