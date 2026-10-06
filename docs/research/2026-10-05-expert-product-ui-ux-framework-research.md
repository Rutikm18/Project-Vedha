# Vedha · Expert product and interface checkpoints

> Primary-source research, 2026-10-05. This is a review framework, not a claim that Vedha currently passes or fails every checkpoint. Preserve Vedha's branding, theme, logo, type family, and palette. The application audit should attach code or browser evidence to each proposed change.

## Evidence and how to apply it

| Source | What the source supports | Application to Vedha — proposed interpretation |
|---|---|---|
| [Nielsen Norman Group: 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | Visible system status, familiar language, consistency, error prevention and recovery, recognition instead of recall, and progressive complexity. These are evaluation principles, not numerical acceptance standards. | Keep engagement context visible; explain scan states; make severity, verification, and remediation labels predictable; retain filters when returning from a finding. |
| [Apple HIG: Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback?changes=latest_5_9) | Place status feedback near the affected object; match interruption to importance; make feedback accessible; explain why commands cannot run. | Show a report's generation status on its row. Use a persistent actionable error for failed scans; reserve interruptive dialogs for consequences that need attention. Provide text alongside status colors. |
| [IBM Carbon: Data table guidelines](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines) | Give tables sufficient width; use coherent row/header sizing; place global actions in a toolbar, pagination below, and selection actions in batch mode. Expand supplemental detail, using a side panel or page when it becomes cramped. | Findings and assets should favor scanning, comparing, and acting. Put search and filters in a predictable toolbar; use explicit checkboxes for selection; show selected count and scope; preserve list position after inspecting evidence. Adopt the interaction principles within Vedha's existing visual system. |
| [Linear: A calmer interface for a product in motion](https://linear.app/now/behind-the-latest-design-refresh) — Charlie Aufmann and Maxime Heckel, March 12, 2026 | Task content should receive more attention than navigation; inconsistent action placement and unnecessary separators accumulate as products grow. The team used comparisons behind feature flags and iterative review of small details. | Audit header/action placement across routes. Remove redundant visual containers where spacing already expresses grouping. Compare changes in the running product with identical data. Preserve Vedha's palette rather than copying Linear's color refresh. |

These sources offer relevant expertise; they do not establish an objective ranking of the world's designers or a universal “Silicon Valley” style. For a security platform, expert craft means faster accurate decisions, reliable feedback, and clear evidence.

## Accessibility standards versus optional targets

[WCAG 2.2](https://www.w3.org/TR/WCAG22/) is the normative reference. The following is a focused checklist, not a full conformance audit:

- **A/AA requirements:** keyboard operation and no keyboard traps (2.1.1–2.1.2); visible focus (2.4.7); focus not entirely obscured by authored content (2.4.11).
- **AA contrast:** ordinary text at least 4.5:1, large text 3:1 (1.4.3); applicable UI boundaries/state indicators 3:1 (1.4.11), subject to the criteria's exceptions.
- **AA pointer targets:** at least 24 × 24 CSS pixels, or satisfy the stated spacing/other exceptions (2.5.8). This does not mean every visual icon must itself be 24 pixels.
- **A/AA semantics:** labels, accessible names/roles/values, text error identification, and programmatically determinable status messages where applicable (3.3.1–3.3.2, 4.1.2–4.1.3).
- **AA reflow:** verify 320 CSS pixel equivalent widths; genuinely two-dimensional data tables have an exception (1.4.10). Surrounding controls still need usable layout.
- **Optional stronger targets:** 44-pixel targets and disabling nonessential interaction animation correspond to AAA criteria (2.5.5, 2.3.3), not AA requirements.

## Review checkpoints — proposed Vedha framework

### Modal interaction checkpoint

The [WAI-ARIA APG modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) is implementation guidance rather than a separate WCAG conformance level. On opening, move focus to an appropriate element inside the dialog; contain Tab and Shift+Tab inside it; make background content inert; provide a visible close control; and restore focus to the invoker when closing, or a logical successor if the invoker no longer exists. Supply dialog semantics and an accessible title. Choose initial focus for the content and consequence, rather than always focusing the first control.

The application audit reports that `AssistantProvider` already handles Escape. Treat that as existing behavior to preserve and verify, not a missing feature. The remaining review must check focus entry, containment, return, and background interaction in the rendered product. An Escape handler alone does not establish an accessible modal.

These are product-specific recommendations inferred from the sources, not source-mandated metrics.

| Gate | Checkpoint | Evidence required before marking complete |
|---|---|---|
| 1 · Establish baseline | Record brand tokens and screenshots of dashboard, engagements, scans, findings, assets, reports, and settings using representative data. | Route/state inventory; unchanged branding checklist; same-data before/after comparison. |
| 2 · Clarify the task | Each page explains its purpose, active engagement/scope, and most useful next action. A finding answers what is affected, why it matters, what supports it, and what action is available. | Analyst walkthrough: identify the next task without coaching; inspect ambiguous labels and unsupported certainty. |
| 3 · Make dense work efficient | Search, filter, sort, pagination, row action, and batch selection follow consistent conventions. Evidence opens without losing the analyst's place. | Complete filter → inspect → return; test no results, many rows, long hostnames, narrow widths, and selection across pages. |
| 4 · Make every state trustworthy | Distinguish initial loading, refreshing existing data, empty inventory, no matching results, denied access, failed request, and stale data. | State matrix with recovery action, retained context, freshness indication, and screen-reader feedback. |
| 5 · Prevent consequential errors | Scans expose intended scope before execution; destructive/batch actions identify affected objects and consequences. Reversible actions use recovery when feasible. | Run the task with realistic scope changes, API failure, repeated clicks, and partial batch failure. |
| 6 · Polish without rebranding | Reuse existing tokens; normalize alignment, spacing, text hierarchy, density, and control heights. Motion explains a change and remains interruptible. | Review actual laptop view and zoom; verify focus, contrast, reduced motion, and long-content behavior. |
| 7 · Verify with users | Test first scan setup, high-risk triage, evidence inspection, remediation/status update, and report handoff. | Record task completion, errors, assistance, time, and confusion before/after. Set improvement goals after measuring the baseline; do not invent benchmark scores. |

## Prioritization and release discipline

Create one review item per issue: **user task → observed evidence → consequence → proposed change → acceptance check → owner**. Prioritize blocked tasks, misleading security state, inaccessible controls, and unrecoverable errors first; then repeated workflow friction; then visual polish.

Ship in small coherent slices: shared interaction primitives, table conventions, state handling, then route-specific refinement. Review each slice in context with populated data and adverse states. A prettier screenshot alone is insufficient proof of improvement.
