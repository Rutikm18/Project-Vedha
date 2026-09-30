# Mobile, Dashboard, and Reporting UI Research

**Date:** 2026-09-30
**Scope:** Workstream 8 — responsive UI, mobile table treatment, touch ergonomics, dashboard triage, state design, report/export usability, and screenshot regression testing.

> Repository note: the requested `docs/planning/2026-09-29-next-8-workstreams-plan.md` was not present in this checkout during research. This brief uses the Workstream 8 excerpt supplied in the request.

## Executive recommendation

Build the UI around three decisions users repeatedly make:

1. **What needs action now?** Put a compact, evidence-backed triage strip first on the dashboard.
2. **What changed, and can I trust the posture number?** Pair every score with trend, scope/coverage, freshness, and the underlying actionable counts.
3. **How do I investigate or share it?** Preserve filters while moving from summary to findings and into a reliable HTML/CSV/XLSX/PDF/DOCX report workflow.

The phone UI should be a genuine task-focused composition, not the desktop grid squeezed narrower. Preserve the same information and actions, but collapse secondary detail, convert suitable text-heavy rows into labeled cards, and keep dense comparison tables in a contained horizontal scroller.

## 1. Responsive behavior

### What authoritative guidance says

- WCAG 2.2 Reflow requires content to work without loss of information or functionality at a width equivalent to **320 CSS pixels**, with exceptions for content whose meaning requires two-dimensional layout. This benefits both mobile users and users zooming a desktop browser. [W3C: Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)
- Content should not be locked to portrait or landscape unless orientation is essential. [W3C: Orientation](https://www.w3.org/WAI/WCAG22/Understanding/orientation.html)
- USWDS recommends choosing a small-screen strategy for every table with more than two columns: use horizontal scrolling for dense numerical comparisons and stacked rows for directory/list-style content. It also recommends minimizing columns. [USWDS: Table](https://designsystem.digital.gov/components/table/)
- Accessible tables retain explicit header/data relationships (`th`, `td`, `scope`, and, where needed, `headers`). [W3C: Tables tutorial](https://www.w3.org/WAI/tutorials/tables/)

### Vedha design rules

- Use mobile-first layouts and verify every authenticated route at four baseline widths:
  - **320 px**: WCAG reflow boundary.
  - **390 px**: representative phone and touch layout.
  - **768 px**: portrait tablet.
  - **1440 px**: desktop workspace.
- Also smoke-test phone and tablet landscape. Do not lock orientation.
- At phone width:
  - Replace the permanent left navigation with a top app bar and drawer.
  - Use one content column; remove fixed card heights and desktop-only empty space.
  - Keep the primary page action visible near the page title; move secondary actions into a labeled overflow menu.
  - Place filters in a full-width sheet/drawer with an applied-filter count and a clear-all action.
  - Make the entire logical row/card the drill-in target when that does not conflict with nested controls.
- Do not blindly turn every table into a card:
  - **Stacked labeled cards:** findings, customers, engagements, agents, reports, scan runs — rows with a clear entity identity and text-heavy attributes.
  - **Contained horizontal table:** dense numeric comparisons, port matrices, time-series grids, and data where scanning down columns is the main task.
  - **Progressive disclosure:** show identity, severity/status, age, owner, and primary action first; expose technical metadata in an expansion/detail page.
- Preserve real table semantics in the DOM when only the visual presentation changes. If a separate mobile card DOM is necessary, do not expose duplicate table and card content to assistive technology.

## 2. Touch and accessible interaction

### What authoritative guidance says

- WCAG 2.2 AA requires pointer targets to be at least **24 by 24 CSS pixels** or to meet the spacing exception; W3C recommends aiming higher for important controls. [W3C: Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- The WCAG enhanced target criterion is **44 by 44 CSS pixels**. [W3C: Target Size (Enhanced)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced)
- Apple likewise recommends a **44 by 44 pt** hit region for buttons and stresses spacing and a visible pressed state. [Apple HIG: Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
- Severity and status cannot be conveyed by color alone. [W3C: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color)

### Vedha design rules

- Use **44 by 44 CSS pixels** as the product default for primary controls, navigation items, row actions, pagination, filter chips, disclosure buttons, and icon-only controls. Treat 24 px as the compliance floor, not the design target.
- Give icon-only controls an accessible name, visible tooltip on hover/focus, strong focus treatment, and pressed/selected state where applicable.
- Do not hide essential actions behind hover. Support keyboard, pointer, and touch paths.
- Pair security colors with explicit text and/or icons: `Critical`, `High`, `Overdue`, `Known exploited`, `Scan failed`.
- Maintain a logical focus order after responsive rearrangement. When a drawer/dialog closes, return focus to its trigger.

## 3. “Needs attention now” and security posture

### What authoritative guidance says

- NIST recommends prioritizing cybersecurity risks in light of their potential impact on enterprise objectives and recording priority and response information, rather than treating a raw score as the whole decision. [NIST IR 8286B](https://www.nist.gov/publications/prioritizing-cybersecurity-risk-enterprise-risk-management)
- CISA SSVC turns vulnerability data into four response decisions — `Track`, `Track*`, `Attend`, and `Act` — based on exploitation and impact context. [CISA SSVC guide](https://www.cisa.gov/sites/default/files/publications/cisa-ssvc-guide%20508c.pdf)
- CISA calls the KEV catalog an authoritative source of vulnerabilities exploited in the wild and recommends using it as an input to vulnerability-management prioritization. [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### Vedha recommendation (an application of those sources)

Use a deterministic priority model rather than ordering solely by CVSS or the 0–100 posture score:

1. **Act now:** confirmed exploitation/attack path, CISA KEV on an in-scope asset, critical internet exposure, or remediation overdue beyond policy.
2. **Attend soon:** high business impact plus credible exploitability, deteriorating control/coverage, or an approaching due date.
3. **Monitor:** accepted/mitigated risk or tracked findings without current action criteria.

The dashboard strip should:

- Sit immediately below the page heading and above summary metrics.
- Show at most three to five reason-based groups, for example `3 known-exploited findings`, `2 overdue critical fixes`, `1 scan failed`, rather than an undifferentiated list of red items.
- Include evidence, affected asset/customer, age or due date, owner/status, and one clear next action.
- Link to a pre-filtered triage view and show a quiet “No urgent actions” success state when empty.
- Avoid turning routine medium/low findings into alerts; WAI warns that frequent interruptions inhibit usability. [WAI: Alert pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alert/)

### Fix for the shown security-posture panel

The screenshot’s posture module devotes most of its height to blank space and presents `C`, `65/100`, `47.5`, and `16.6` without a strong explanatory hierarchy. Redesign it as a compact responsive module:

- **Header:** scope, last successful scan time, data freshness, and coverage/confidence.
- **Primary row:** posture score + text label + trend versus a clearly named comparison period.
- **Drivers:** top three factors changing the score, each linked to filtered findings.
- **Action summary:** critical/high actionable count, known-exploited count, overdue count, and remediation progress.
- **Method link:** short explanation of scale, direction (`lower is better`), inputs, and unavailable/partial-data behavior.

On phones, order those blocks vertically. Do not preserve the desktop panel’s fixed height or place the gauge beside tiny metric cards.

## 4. Loading, empty, error, and partial-data states

### What authoritative guidance says

- WAI-ARIA defines `aria-busy` for a region being updated; assistive technology may defer announcing its changes until the update completes. [WAI-ARIA 1.2: `aria-busy`](https://www.w3.org/TR/wai-aria/#aria-busy)
- WCAG status-message guidance uses `role="status"` for advisory success/progress and `role="alert"` for important errors. [W3C: Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)
- USWDS distinguishes advisory status from an immediate alert and recommends short, clear alert titles. [USWDS: Alert](https://designsystem.digital.gov/components/alert/)

### Required state contract for every data surface

| State | Required behavior |
|---|---|
| Initial loading | Keep the page shell and heading stable; use shape-matched skeletons for content that will appear. Mark the updating region busy and expose a concise status message. |
| Background refresh | Keep usable stale data visible, show `Refreshing…`, and update freshness on completion. Do not blank the page. |
| Empty — first use | Explain what this area will contain, why it is empty, and offer the primary creation/setup action. |
| Empty — filtered | Say that no results match the current filters, show applied filters, and offer `Clear filters`; do not show the first-use message. |
| Error — recoverable | State what failed in plain language, preserve the user’s context, and provide `Retry`. Include a support/reference ID when useful. |
| Partial/stale | Show available data with a persistent, non-blocking warning that names the missing source and the last successful update. Never silently compute a complete-looking posture score from incomplete data. |
| Success | Confirm exports and mutating actions using `role="status"`; reserve assertive alerts for failures needing immediate attention. |

Skeletons must not mimic real severity data, and their motion must respect reduced-motion preferences. All state containers should reserve enough space to avoid large layout shifts.

## 5. Reports and export usability

### What authoritative guidance says

- GOV.UK recommends HTML as the primary reading format; PDFs can be harder to find, maintain, and use with assistive technology, so an accessible alternative should accompany them. [GOV.UK: Publishing accessible documents](https://www.gov.uk/guidance/publishing-accessible-documents)
- For CSV, GOV.UK recommends a header row and consistent values under each column, because this improves import and manipulation. [GOV.UK: Publishing tabular data](https://www.gov.uk/guidance/publishing-your-tabular-data)
- Spreadsheet guidance recommends simple structure, one header row, no merged cells, no blank separator rows, and text in addition to color. It also warns about hidden rows, columns, tabs, and metadata. [GOV.UK: Creating and sharing spreadsheets](https://www.gov.uk/guidance/creating-and-sharing-spreadsheets)
- Accessible PDFs need tags, logical reading order, document language, semantic headings/tables, and verification; auto-tagging alone is not a guarantee. [Adobe: Create and verify PDF accessibility](https://helpx.adobe.com/acrobat/using/create-verify-pdf-accessibility.html)
- CSV exports containing untrusted text can trigger spreadsheet formulas. OWASP identifies leading formula characters and notes that there is no universal sanitization strategy for all spreadsheet applications and downstream consumers. [OWASP: CSV Injection](https://community.owasp.org/attacks/CSV_Injection)

### Reporting information architecture

- Make the Reports landing page a useful workspace, not a grid of generic format cards:
  - `Create report` primary action.
  - Recent reports with scope, period, template, format(s), owner, created time, and state.
  - Saved templates and scheduled reports as secondary sections.
- Use a four-step report builder:
  1. **Scope:** customer/engagement/assets and permission-aware data boundary.
  2. **Period and filters:** severity, status, evidence class, assignee, tags.
  3. **Audience/template:** executive, technical, remediation, compliance.
  4. **Preview and export:** HTML preview first; explicit format choices and included sections.
- Preserve selections after a failure. Show a report-generation job as `Queued`, `Generating`, `Ready`, or `Failed`, with progress/status text, retry, cancel where supported, and expiration information.
- Do not announce success until the artifact is downloadable and passes server-side validation.

### Clear format contract

| Format | User need | Required content behavior |
|---|---|---|
| HTML | Default reading, filtering, and accessible navigation | Semantic headings, tables, links, chart summaries, print stylesheet. |
| CSV | Raw machine-readable finding data | One record per row, one header row, stable schema/version, UTF-8, consistent dates/IDs; neutralize spreadsheet formula injection according to the chosen human-vs-machine consumption contract. |
| XLSX | Analyst workbook | Accessible sheet names, a single header row per table, no merged data cells, text labels beyond color, filters, data dictionary, and no hidden sensitive data/author metadata. |
| PDF | Fixed executive/print artifact | Tagged structure, bookmarks/headings, logical reading order, selectable text, chart text alternatives, repeated table headers, page number, scope, generated time, and confidentiality marking. |
| DOCX | Editable narrative handoff | Semantic heading styles, accessible tables, alt text, page header/footer metadata, and an accessibility-check pass before release. |

### Production acceptance for exports

- A generated artifact must be opened and parsed in automated tests, not merely checked for HTTP 200.
- Verify extension, MIME type, non-zero size, scope/tenant authorization, row/section counts, applied-filter metadata, and generated-at timestamp.
- Re-check authorization at download time; use expiring downloads and audit report generation/download.
- Keep secrets and sensitive filter values out of filenames and URLs.
- Provide a visible failure reason that is safe to expose and an internal correlation ID for operations.

## 6. Automated responsive and visual regression checks

### What Playwright officially supports

- Playwright projects can run the same tests across desktop, phone, tablet, browser, and environment configurations. [Playwright: Projects](https://playwright.dev/docs/test-projects)
- Device emulation includes viewport, screen size, user agent, and touch capability. [Playwright: Emulation](https://playwright.dev/docs/emulation)
- `toHaveScreenshot()` waits for two consecutive stable screenshots before comparison and supports disabling animations, masking known-dynamic regions, and controlled diff thresholds. [Playwright: Screenshot assertions](https://playwright.dev/docs/api/class-pageassertions#page-assertions-to-have-screenshot-1)
- Browser and platform rendering differ, so baselines must be generated and compared in a consistent environment or maintained per project. [Playwright: Visual comparisons](https://playwright.dev/docs/test-snapshots)
- ARIA snapshots can separately protect accessible structure; pixels alone cannot. [Playwright: ARIA snapshots](https://playwright.dev/docs/aria-snapshots)

### Vedha test design

Create a route/state manifest rather than hand-picking a few happy-path pages:

- Every top-level manager and portal route.
- Representative detail pages with long names, large counts, and worst-case badges.
- Loading, first-use empty, filtered empty, recoverable error, stale/partial, and populated states.
- Open navigation drawer, open filters, expanded table/card row, and report export states.

Run screenshot projects at `320`, phone/touch, tablet/touch, and desktop widths. Use deterministic fixtures, a fixed locale/timezone, stable fonts, disabled animation, and frozen timestamps. Mask only truly nondeterministic values; masking a whole content panel would hide regressions.

For every viewport, add structural assertions alongside screenshots:

- No page-level horizontal overflow; designated dense-table scrollers are the only exception.
- Primary heading and action are present and not clipped.
- Touch controls meet the product’s 44 px target policy.
- Keyboard focus remains visible and follows the visual order.
- Stacked rows retain visible field labels and accessible names.
- No overlap at 200% text zoom and no loss of functionality at 320 CSS px.
- ARIA snapshot for critical dashboard, findings, filters, and report-builder structures.

Keep baseline updates reviewable: CI should upload expected, actual, and diff artifacts; accepting new goldens should be an explicit review action, not an automatic CI rewrite.

## 7. Definition of done

- Every route passes the phone/tablet/desktop screenshot matrix and 320 px reflow check.
- Every table has an intentional phone strategy documented as stacked cards or contained horizontal scroll.
- All recurring interactive controls meet the 44 px product target and work by keyboard and touch.
- Dashboard has a reason-based “Needs attention now” strip with deterministic ordering and a pre-filtered drill-in.
- Security posture shows score meaning, trend period, coverage/freshness, major drivers, and incomplete-data behavior.
- Every data surface implements the same loading, refresh, empty, error, partial, and success contracts.
- CSV, XLSX, PDF, and DOCX exports generate in production, preserve scope/filters, pass artifact validation, and expose accessible job states.
- CSV formula-injection handling and export/download authorization have explicit automated tests.
- Visual baselines are deterministic, stored per project/environment, and gated in CI together with semantic assertions.
