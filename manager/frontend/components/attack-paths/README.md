# Vedha business route panel

The actual global route view is `/attack-paths`, behind the existing assessment pilot flag and authorized-engagement allowlist. `/attack-paths/demo` is a separate, visibly labelled made-up example. It never supplies actual environment records.

## Files

| File | Responsibility |
| --- | --- |
| `BusinessRoutePanel.tsx`, `business-routes.css` | React Flow map, accessible route list, finding inspector, in-memory fix preview and captured-view comparison |
| `EnvironmentScopeSelector.tsx`, `EnvironmentSystemChart.tsx`, `FindingChainExplorer.tsx` | Compact searchable scope, captured-finding queue and progressive evidence investigation |
| `lib/business-routes.ts` | Pure bounded `analyse`, `previewFix`, `compare`, identity validation and duplicate handling |
| `lib/business-route-layout.ts` | Memoized dagre ordering within four stable semantic lanes |
| `lib/demo-business-routes.json` | 12 systems, 15 connections and two made-up scans; isolated example/test fixture |
| `lib/environment-assessments.ts`, `EnvironmentAttackWorkspace.tsx` | Existing authorized BFF/API capture, polling, result restoration and two-view history |
| Backend `app/services/environment_route_map.py` | Tenant-scoped, bounded projection of actual inventory, finding remediation and already stored route models |

## Run

Use this project's normal backend, database and outbox-worker setup. Apply migrations through 0064. Enable `ATTACK_ASSESSMENTS_ENABLED` with an explicit `ATTACK_ASSESSMENT_ENGAGEMENT_ALLOWLIST` for the intended engagement IDs. In the frontend, run `npm install`, then `NEXT_PUBLIC_ATTACK_ASSESSMENTS_ENABLED=true npm run dev`. Set `BACKEND_INTERNAL_URL` to the intended backend. Sign in with an existing operator account. Select the actual engagement(s) and rebuild the view; ordinary GET requests do not generate routes or run scans.

`npm test` runs the repository's existing Node/TypeScript test runner, including `tests/business-routes.test.ts`. Keeping that runner avoids an unrelated Jest/Vitest migration. `npm run build` and `npx tsc --noEmit` verify the Next.js integration. The framework stays Next.js/React 19; React Flow and dagre are the graph libraries requested in the brief.

## Investigation layout

The page follows scope → captured result → selected evidence. Scope selection expands inline rather than occupying the whole first viewport. Paths and Findings & evidence have separate keyboard-accessible tabs; recorded connections lead with the map, while a capture without connections leads with its available findings. Both panels remain mounted so switching tabs retains local inspection and fix previews. Selection, capture age, incomplete coverage and source identity remain explicit.

The path view prioritizes four measures: confirmed routes, possible routes, critical assets reached and findings on counted routes. Fix totals remain capture metadata; simulation counts stay in the preview notice. Unavailable grades move into the reading guide. Empty connection data presents the recorded inventory/finding counts and a working evidence-review action instead of a blank graph. The map inspector sits beside the map on wide containers; the finding queue, required-evidence checklist and selected inspector form the evidence workbench. Smaller containers stack those regions with explicit return controls. See `docs/planning/2026-10-13-attack-path-information-layout.md` for placement and responsive decisions.

## Colour roles

The panel reuses Vedha's existing theme tokens from `app/globals.css`; no brand hex values are duplicated in components. Scoped `--route-*` aliases distinguish action, connection evidence, attack risk and simulated remediation. Confidence and severity are independent: a confirmed attack connection uses teal, while confirmed reachability of a critical asset uses red. A preview uses blue until a scan confirms the fix. Zero routes stays neutral rather than implying safety.

| Role | Light HEX | Dark HEX | Non-colour cue |
| --- | --- | --- | --- |
| Actions, selection, focus and fix preview | `#1D4ED8` | `#60A5FA` | Pressed state, focus outline, “Fix preview” label |
| Confirmed connection / scan-confirmed fix | `#0F766E` on `#CCFBF1` | `#5EEAD4` on `#134E4A` | Solid line, confirmation icon and label |
| Possible connection | `#854D0E` on `#FEF3C7` | `#FBBF24` on `#3A2C10` | Dashed line, “Possible” label |
| Confirmed attack risk | `#B91C1C` | `#F87171` | Critical-asset icon and confirmed-route count |
| Critical finding badge (text / background) | `#FFFFFF` / `#B91C1C` | `#450A0A` / `#F87171` | “Critical” label |
| High finding badge (text / background) | `#FFFFFF` / `#C2410C` | `#431407` / `#FB923C` | “High” label |
| Low finding text | `#57534E` | `#A8A29E` | “Low” label |
| Informational finding text | `#64748B` | `#94A3B8` | “Info” label |
| Removed connection | `#607086` | `#7D8CA1` | Faded line and explicit preview / scan-fixed label |

Text and badge pairs must meet 4.5:1 contrast; meaningful graph lines, icons and focus indicators must meet 3:1. Faded removed edges are supplementary to the inspector and comparison labels. Desktop and narrow layouts retain textual status, line patterns and the accessible route list.

## Real-data contract and honesty

`BusinessScan` supports the brief's nodes/edges/findings contract plus scoped source IDs, a captured time, model version and incomplete-coverage metadata. Every edge must reference two captured systems and an actual finding attached to its destination. Duplicate stored hops are collapsed. Engagement-qualified identities never merge by IP/hostname and no cross-engagement hop is invented.

Existing stored-model edges always become **theoretical**, enforced again in the frontend. A confirmed finding, `exploited` flag, an exposure annotation or a CVSS value cannot confirm a whole connection. Each hop must follow consecutive systems in its stored model and match a destination finding in the same engagement. False-positive or contradicted findings cannot enable connections. Older connections remain visible for inspection but are excluded from analysis; conflicting duplicate freshness stays conservative. The future reviewed observation adapter must supply exact directed reachability, entry/actor/permission/service bindings, consequence and current source provenance before producing confirmed edges. Entry locations come from stored route starts and remain modelled; no extra Internet hop is fabricated. Only operator-marked criticality creates critical nodes. Grades absent from the API remain unavailable.

Two completed captures of the same engagement selection and route-map version support before/after comparison. These are captured views, not renamed scan executions. Scan-confirmed remediation requires the existing coverage-gated automatic-resolution method and a reference to a completed detection run in the same engagement. Manual closure or an invalid, failed, running or foreign run stays awaiting scan confirmation. Dismissed findings are separate from unresolved findings and fixes. Accepted risk remains unresolved. Findings missing from a later capture are reported as missing, never fixed. The inspector exposes the recorded finding verdict and last observation time without inventing either. After findings change, operators explicitly analyze the selection again; ordinary reads preserve the captured cut.

The current projection contract is `stored-environment-routes@2`. Older captures require reassessment and their route counts are withheld until refreshed. Reachability requires at least one directed hop from a distinct entry; an entry/critical annotation alone or a cycle returning to its own start is not a route. Enumeration continues through critical systems so downstream critical systems receive their own routes, subject to the existing work/path limits.

“Preview this fix” removes that finding's edges from analysis without changing the source snapshot. The graph fades those edges over 240ms, or immediately under reduced motion. Undo and reset are local to this component; no localStorage, scan request or lifecycle mutation is made. The inspector links to the existing finding workflow to record real remediation; running scans is outside this panel's scope.

## Expected example results

Scan one: **8 routes**, **3 reachable critical systems**, **1 all-confirmed route**. Scan two: **6 routes**, **2 reachable critical systems**, **0 all-confirmed routes**, two explicit example fixes and one new finding. Turning off possible routes in scan one leaves the sole confirmed Customer data route; previewing finding `f3` then removes that route and makes Customer data unreachable in that filtered view. With possible routes shown, its other theoretical connection remains until the separate public-application fix is applied.

Path enumeration is capped at 2,000 and 100,000 work steps, reports lower-bound counts when truncated, and displays pages of at most 20 routes. Separate traversal computes reachable critical systems independently of enumeration limits. Cycles do not bootstrap reachability, and duplicate edges do not inflate path counts. Memoized layout does not move on fix previews. The 300-system/600-connection test measures layout/computation separately; browser smoothness and Lighthouse scores must be measured rather than inferred from this test.

Remaining real-integration questions: which existing customer/engagement is intended for the preview; which source owns confirmed connection observations; and which assets the customer/operator has marked critical. The local task preview contains only synthetic records. The actual view never falls back to the made-up fixture.
