# Vedha product and UI/UX enhancement framework

**Date:** 2026-10-05
**Brief:** Identify expert-level enhancements to the existing platform while preserving branding and theme.
**Deliverable:** Evidence-backed audit, prioritized backlog, and review checkpoints. Implementation is recorded in the [delivery report](./2026-10-05-ui-ux-enhancement-implementation.md).

## Recommendation

Improve the accuracy and continuity of the analyst's work before adding visual effects. The largest opportunities are trustworthy status indicators, dashboard-to-findings handoffs, persistent investigation context, accessible overlays, and consistent handling of unavailable data. Then refine density, hierarchy, and action placement within the existing interface system.

This is an operational security product. Premium quality means an analyst can understand the risk, inspect the evidence, take the right action, and trust the result with less effort.

## Audit baseline and delivery status

The findings below record the initial local checkout (`0edde1d`) and its saved fixture screenshots. Implementation was subsequently ported to current main (`64051cd`) in an isolated branch, preserving its newer logo, shared customer workspaces, plan locks, deep scanning, and motion refinements. Some audit findings had already been addressed upstream; the delivery report distinguishes those inherited improvements from this PR's changes. Source paths and line numbers below identify the audit baseline, not the final module layout.

## Evidence boundary

- Reviewed current source for the shared operator shell, navigation, dashboard composition, findings, scan setup, assistant drawer/provider, reporting/export, selected portal components, tokens, and responsive tests.
- Visually inspected seven saved Playwright baselines: desktop dashboard, findings, scan, reports, settings, portal findings, and phone findings. These are historical fixture screenshots, not newly captured current-product evidence. Fixture time is fixed to September 30, 2026; screenshots can diverge from current code.
- Ran the Impeccable deterministic detector against `manager/frontend/app` and `manager/frontend/components`: **15 warnings**, comprising six layout-property transitions and nine accent-border flags. These are leads, not verified performance defects or reasons to erase existing branding.
- No server answered on localhost:3000. No authenticated live walkthrough, real-user study, contrast measurement, performance benchmark, or WCAG conformance test was performed. No numeric product-quality score is assigned without that evidence.
- Unrelated application changes in the original working tree were left untouched. Implementation and verification use an isolated checkout.

Primary-source research and attribution: [Expert product and interface checkpoints](../research/2026-10-05-expert-product-ui-ux-framework-research.md). This builds on the [existing mobile/dashboard/reporting research](../research/2026-09-30-mobile-dashboard-reporting-ui-research.md), checking where the current implementation still differs from its intent.

## Preserve the existing identity

The incumbent authority is [DESIGN_SYSTEM.md](../../manager/frontend/DESIGN_SYSTEM.md), [globals.css](../../manager/frontend/app/globals.css), and [console-tokens.css](../../manager/frontend/styles/console-tokens.css).

- Keep the Vedha name, shield, system sans and evidence monospace stacks, light/dark themes, semantic palette, and existing surface hierarchy.
- Preserve blue for operator intent, red/orange/amber for urgency, stone/slate for low/informational severity, teal for verified health, and violet for machine-generated content. Color remains accompanied by text or an icon.
- Preserve severity, priority, evidence verdict, exploit confirmation, risk score, and lifecycle as distinct concepts. Do not change scoring contracts through visual refinement.
- Improve alignment, spacing, density, hierarchy, grouping, labels, focus, and feedback using existing tokens. Do not introduce a new font, decorative palette, generic gradients, replacement navigation style, or novelty animation.
- A semantic accent border is not automatically a defect. Retain it when it helps operators identify urgency and matches the incumbent design rules.

## Strengths to retain

1. The design system explicitly separates technical severity from response priority and documents the Manager risk scale.
2. The dashboard already begins with an attention strip rather than only charts; findings already support search, sorting, keyboard shortcuts, evidence views, and reasoned lifecycle actions.
3. Shared `DataState` distinguishes loading, empty, error, and expired-session states. Dashboard `Freshness` and semantic table captions/header relationships provide a useful foundation.
4. Reports identify live drafts and missing evidence; assistant copy distinguishes public CVE information from verified client exposure.
5. Responsive regression coverage already spans 19 routes at 320, 390, 768, and 1440 pixels. Enhance this investment rather than replacing it.

## Prioritized enhancement backlog

Priorities here mean **P1: major trust/task/accessibility issue**, **P2: repeated workflow friction**, and **P3: bounded polish**. No P0 outage was established. Effort is relative: S = localized frontend change; M = shared state/interaction work; L = cross-layer product work. Each estimate requires implementation review.

### E01 · P1 · Make attention shortcuts apply their promised filters · M

**Verified source:** `components/dashboard/DashboardGrid.tsx:79–88` sends `/findings?severity=CRITICAL&status=open` and `/findings?sla=breached`. `app/findings/page.tsx:3021–3043` consumes only `finding` and `engagement`; severity/status/SLA start at their default local states.

**Consequence:** A click on urgent work opens the general queue, making the user search again and weakening trust in the summary-to-detail relationship.

**Enhancement:** Define one validated URL/filter contract. Hydrate supported filters, normalize status casing, reflect active filters visibly, and preserve them through reload/back/forward. Unknown parameters must degrade safely.

**Acceptance:** Clicking Critical applies Critical + Open; clicking SLA breach applies the breach filter; counts reflect the same scope; returning from a finding retains filters, page, and list position. Add behavioral regression coverage for both shortcuts.

### E02 · P1 · Connect status language to observed state · M/L

**Verified source:** `PageShell.tsx:163–178` unconditionally presents “Live — console connected”; its footer uses fixed ENGINE/API/DB indicators around line 360. `Sidebar.tsx:295` always renders “System Nominal”. Dashboard header queries in `app/page.tsx` fall back to zero/“NONE TRACKED” after a request fails because only initial loading is considered.

**Consequence:** A failed request or unknown service state can be presented as a reassuring result. This is especially damaging in security operations.

**Enhancement:** Derive query freshness/connectivity from actual observations. Label unknown, stale, updating, and failed states explicitly. Only expose backend component health if a supported authorized health contract exists; otherwise remove the unsupported claim. Keep health colors within existing semantic roles.

**Acceptance:** An API failure never produces “System Nominal”, “Live”, or a zero interpreted as absence of exposure. Cached data stays visible with an age and stale/error notice. Zero tracked findings says “No SLA-tracked findings”; unavailable tracking says “SLA status unavailable”.

### E03 · P1 · Complete modal and mobile-navigation keyboard behavior · M

**Verified source:** `AssistantDrawer.tsx:161` declares `role="dialog" aria-modal="true"`, but does not set initial focus, contain focus, make the background inert, or restore focus. `AssistantProvider.tsx:85` already closes on Escape; retain that behavior. The shell/sidebar mobile drawer similarly lacks focus management.

**Consequence:** Keyboard and screen-reader users can remain on or move into obscured page controls while a modal is open.

**Enhancement:** Use a shared accessible overlay primitive consistent with [WAI APG's modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). Define the mobile drawer as modal only at the relevant breakpoint; desktop navigation remains ordinary navigation.

**Acceptance:** Open by keyboard; focus enters a useful control; Tab/Shift+Tab stay inside a modal; Escape closes; focus returns to the invoking control; background cannot be operated. Verify nested-overlay behavior and responsive breakpoint transitions.

### E04 · P1 · Distinguish scan dependency failures from empty setup · M

**Verified source:** `app/scan/page.tsx:710–738` loads use cases, probes, and engagements in one `Promise.all`; failure produces a toast while default arrays remain. Job polling around line 743 swallows request failures. The saved scan screenshot also shows an empty configuration state, but current code has a Network VA fallback, so that screenshot is not proof of today's same defect.

**Consequence:** “No probes” may mean a load failed; a job can appear to continue normally after polling loses contact.

**Enhancement:** Track loading/error/empty state for each dependency, keep successful data, give persistent contextual retry, and show the last successful job update when polling fails. Ensure any catalog fallback is identified and valid for the Manager contract.

**Acceptance:** Fail each dependency independently. Users can tell unavailable data from no registered probes and recover without re-entering valid scope. A polling failure shows stale status; it does not imply completion or restart execution.

### E05 · P2 · Preserve work during refresh and navigation · M

**Verified source:** `RefreshButton.tsx:56` reloads the entire page after a delay. Most Findings filters are local state; scan configuration is also local state. The dedicated Findings agent refresh already provides a more targeted precedent.

**Consequence:** Routine refresh can discard filters, selections, or typed configuration. A generic delay also makes data refresh feel slower than necessary.

**Enhancement:** Use targeted query refetch/invalidation for ordinary refresh. Represent shareable queue state in the URL; preserve appropriate non-secret draft inputs during short navigation. Keep enrollment settling tied to the actual enrollment state rather than every refresh action.

**Acceptance:** Refresh updates data without resetting query, page, selection, or an unsent scan configuration. Recovery never automatically launches a scan. Do not persist tokens, credentials, or sensitive evidence in browser storage.

### E06 · P2 · Bring Findings back to its documented decision hierarchy · M

**Verified source + historical visual evidence:** `DESIGN_SYSTEM.md` calls for search, engagement, agent, and sort to stay visible while secondary filters use “More filters”. `app/findings/page.tsx:3481–3540` instead displays severity, lifecycle, evidence, and sort together; signal filters follow. In the phone baseline, summary and urgent-detail content consume nearly the first viewport before the queue search appears.

**Enhancement:** Keep search/scope/sort directly accessible. Place secondary filters in one disclosure with applied count and chips; provide useful task presets once E01 is fixed. Condense the phone summary so investigation begins sooner. Preserve access to every existing filter and the underlying information.

**Acceptance:** Compare identical-data before/after views at phone and 1366×768 laptop size. Analysts can find search and see applied filters without exploring multiple panels. Validate faster triage in a task study; do not enforce an arbitrary maximum option count.

### E07 · P2 · Make navigation reflect the current work context · S/M

**Verified source:** `Sidebar.tsx:195` checks exact pathname equality, so engagement and campaign detail routes lose their parent active state. Operator links lack `aria-current`; the nav landmark has no distinguishing label.

**Enhancement:** Use segment-aware parent matching, current-page semantics where appropriate, a named landmark, and consistent context/breadcrumbs for detail routes. Keep the current section names and brand presentation unless user research demonstrates a terminology issue.

**Acceptance:** Engagement and campaign details identify their parent location; sibling routes never match accidentally; screen readers can determine navigation context; small-screen menu trigger exposes expanded state and its controlled region.

### E08 · P2 · Make the regression suite prove interaction quality · M

**Verified source:** `playwright.config.ts` fixes light mode and reduced motion. `e2e/responsive.spec.ts:243` checks only visible buttons below 40×40, whereas the design system specifies at least 44 pixels on coarse pointers. Tests assert document overflow, not all clipping inside nested containers, and do not complete analyst workflows.

**Enhancement:** Retain current screenshots; add representative dark-mode, keyboard, overlay, failure-state, nested-scroll, and workflow cases. Check links, inputs, chips, and pagination targets as well as buttons. Use actual coarse-pointer emulation for the product's 44-pixel touch goal.

**Acceptance:** Tests cover E01–E05; target dimensions meet the product rule on touch; meaningful content cannot disappear inside clipped containers; no screenshot is treated as evidence of task completion. WCAG AA's 24-pixel/exception rule and the product's stronger 44-pixel goal must remain distinct.

### E09 · P2 · Clarify report handoff and draft readiness · M/L

**Observed opportunity:** `app/reports/page.tsx` honestly labels the current report as a live non-persisted draft and exposes printing/export. It also presents AI-assisted draft review. The saved report baseline gives substantial prominence to technical metadata such as schema and snapshot information.

**Enhancement:** Establish a concise operational hierarchy: selected engagement → draft/approval state → missing evidence → preview/export. Group implementation metadata in a disclosure in the operator UI while preserving canonical report completeness. Consider persisted delivery snapshots only after confirming the backend and product scope.

**Acceptance:** An assessor can explain which artifact is live, which content was approved, and which export is appropriate for customer delivery. Missing evidence stays visible. A visual label never implies immutable or approved status without backend support.

### E10 · P2 · Validate score comprehension across operator and customer surfaces · M

**Observed opportunity:** The dashboard shows posture, risk index, exploitable share, protocol risk, and zone health; Findings documents Manager risk `/1000`; the saved portal baseline displays a risk value without an explicit denominator. These can be legitimate distinct measures, but their meanings must be legible.

**Enhancement:** Show score name, scale, direction, scope, and source near decision-making values. Offer a concise explanation of contributing factors. Verify portal/API adapters before proposing any normalization; never silently change the risk contract.

**Acceptance:** Operators and customers can distinguish “higher is worse” risk from “higher is better” health and can describe what a number summarizes. Unknown measurements render unknown, not zero. Validate with real report consumers.

### E11 · P3 · Refine typography and component rhythm within existing tokens · M

**Verified source + historical visual evidence:** `DataState.tsx` uses monospace for empty/error narratives despite the design system reserving it for machine data. Several reviewed screens use very small supporting labels; the historical Findings desktop header overlaps its title with header actions.

**Enhancement:** Use the existing body stack for narrative text, reserve monospace for IDs/evidence, normalize label/body/control tiers, and make header layout priorities explicit. Review small text at real laptop resolution and zoom; no new typography identity is required.

**Acceptance:** Current screenshots at 1366×768 and 1440×900 show no title/action collision. Long names and translated-length labels wrap or truncate with accessible full text. Measure token contrast in both themes; small type alone is not claimed as a WCAG failure.

### E12 · P3 · Use restrained, state-driven motion · S/M

**Verified source:** Six detector warnings identify width transitions in campaign/progress and related components. `globals.css:395` uses a blanket 0.01ms reduced-motion override. Nine accent-border warnings align with existing semantic styling and are not actionable without further context.

**Enhancement:** Profile busy progress views before optimizing. Where useful, animate a transformed fill rather than layout width. Stop decorative pulses when state no longer warrants them. Define static or low-motion alternatives while keeping explicit state feedback.

**Acceptance:** Reduced-motion users still receive loading, completion, and failure feedback. Animation never blocks an action, implies live connectivity without evidence, or continues after the operation ends. No performance claim is made without measurement.

## Expert review checkpoints

These are proposed Vedha gates, informed by [NN/g's heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [Apple feedback guidance](https://developer.apple.com/design/human-interface-guidelines/feedback), [Carbon data-table guidance](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines), and [Linear's design-team account](https://linear.app/now/behind-the-latest-design-refresh). They are not a claim that one company has a universal process or that a named designer is objectively “the best”.

| Gate | Review question | Required evidence | Pass condition |
| --- | --- | --- | --- |
| G0 · Identity and baseline | What must remain recognizable, and what is observed today? | Token inventory, route/state matrix, current same-data screenshots | Brand constraints recorded; historical evidence clearly labeled |
| G1 · Product task | What does the analyst need to decide on this surface? | One task statement per surface; operator/customer walkthrough | Purpose, scope, and next action are clear without coaching |
| G2 · Information hierarchy | Does attention go to the decision before secondary metadata? | Laptop and phone comparisons; label/score comprehension study | Essential evidence and actions are discoverable; no lost information |
| G3 · Interaction continuity | Can the user investigate, act, and return without starting over? | Dashboard → filtered queue → evidence → lifecycle → return recording | Filters, scope, position, and state survive; results match intent |
| G4 · Trust and adverse states | What does the interface claim when data is missing or stale? | Initial load, refresh, empty, filtered-empty, stale, denied, failed and partial states | No unsupported reassuring state; actionable recovery retains work |
| G5 · Accessibility and resilience | Can users operate it with keyboard, touch, zoom, and assistive technology? | Keyboard/screen-reader checks, measured contrast, dark/light, 320px reflow and 200% text | Applicable WCAG 2.2 AA checks pass; stronger product touch rule verified |
| G6 · Craft and performance | Are details coherent and interactions responsive? | Token/component comparison; representative browser performance traces | No drift or collisions; justified motion; performance assessed with data |
| G7 · Outcome and release | Did the change improve the real task? | Task study, regression results, reviewer sign-off and remaining limitations | No critical task/accessibility regression; improvement supported by observations |

Mark each gate **Not assessed / Evidence gathered / Needs changes / Verified**. Never mark Verified from a screenshot alone. Averages must not hide a broken scan launch, inaccessible modal, or misleading health claim.

## Five tasks for validation

Use representative operators and customer report consumers with realistic data. A small initial study (for example, five participants across relevant roles) is a discovery round, not statistically representative proof.

| Task | Scenario | Record |
| --- | --- | --- |
| First scan | Engagement exists; one compatible probe, one unavailable probe; scope excludes a sensitive host | Setup completion, scope errors, assistance, time, disabled-action comprehension |
| Urgent triage | Critical exposure and overdue remediation exist among routine findings | Correct shortcut/filter, first finding inspected, confidence in counts |
| Evidence to action | Inspect evidence, choose a lifecycle action, explain the reason | Confusion between confirmed evidence and exploitation; incorrect action; recovery |
| Interrupted investigation | Filter queue, open finding/assistant, refresh, return | Lost filters/input/position; keyboard focus; recovery effort |
| Customer handoff | Draft contains missing evidence and an AI section awaiting review | Can the assessor identify draft readiness and produce the intended artifact? |

Capture baseline task success, assistance, errors, time, and short confidence/comprehension answers. Set improvement targets after baseline measurement. Do not invent a conversion uplift or “world-class” score.

## Implementation sequence and definition of done

1. **Trust and continuity:** E01, E02, E03, E04. Owners: frontend plus API owner where telemetry/state contracts are needed.
2. **Daily analyst efficiency:** E05, E06, E07, E08. Owners: frontend and product designer; validate with assessors.
3. **Decision comprehension and delivery:** E09, E10. Owners: product, reporting/API, frontend; validate with customers.
4. **Visual craft:** E11, E12. Owners: design/frontend after behavior and hierarchy stabilize.

For each slice: record the task and defect → implement the smallest coherent change → inspect desktop/phone and both themes in one batched pass → fix observed defects → confirm once → capture task/regression evidence. Run normal frontend checks when source changes are implemented; documentation-only work does not require rebuilding the application.

**Definition of done:** existing identity retained; issue-specific acceptance passed; honest loading/error/stale behavior; keyboard and touch paths verified; same-data current screenshots reviewed; appropriate behavior tests pass; measured outcomes and remaining limitations recorded. New backend capabilities and delivery-state changes require explicit product definitions before they are represented in UI.

## Backlog item template

Use this format for future implementation tickets:

```text
ID / priority / accountable owner:
User and task:
Observed evidence (current source or reproduced behavior):
Consequence:
Proposed enhancement:
Brand/theme constraints:
API or state dependencies:
Acceptance scenarios (normal + failure + keyboard/touch):
Before/after evidence and measured outcome:
Remaining limitations:
```

The immediate next implementation slice is **E01–E04**. It improves the platform's credibility and task completion while using its existing visual identity.
