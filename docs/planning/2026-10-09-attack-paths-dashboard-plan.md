# Attack paths on the dashboard: how to represent them (research and plan, 2026-10-09)

**Status:** plan for your review. Nothing in this document is built. It follows the first dashboard
section (shipped on `claude/elegant-noether-ggdafj`, three commits `27b80255`, `3a921fce`, `7df368c6`).

## 0. The decision in eight lines

1. **Do not put a graph on the dashboard.** The products I could find summarise attack paths with
   counts and ranked lists (Microsoft and Tenable add change over time) and keep the graph in a drill-down. Our own research agrees:
   a graph at dashboard size becomes unreadable at 18 hosts (see the mock-up below).
2. **Lead with "crown jewels reachable in the model", not "N routes".** The route count I shipped is
   the length of a *capped* list (at most 5 routes per entry point per crown jewel), so it measures the
   search limit as much as the network. Eight exposed hosts behind one gateway read as "8 routes"
   while the real answer is "fix one host".
3. **Recommended layout (Option C):** three triage tiles, a ranked list of engagements where each row
   shows a one-glance jewel meter, and a "Fix first" card for the top engagement: the highest-risk route
   as a short vertical chain, and the hosts ranked by modelled risk removed.
4. **Zero new libraries.** The chain, the meters and the bars are HTML and CSS. I measured the
   alternatives (section 2.4): 17 KB to 440 KB gzipped for layout and graph engines we do not need.
5. **Honesty rules carry over unchanged** and get stricter: "reachable in the model", "separate ways
   in", "modelled, not a probability", and bars that are never added up.
6. **One existing accessibility defect found:** the engagement route map draws its edges in a colour
   that fails the 3:1 non-text contrast minimum (2.68:1 light, 2.22:1 dark). Fixed in Phase 0.
7. **A trend ("is it getting better?") is the one thing both Microsoft and Tenable show that we cannot,**
   because we keep only the latest analysis. It needs a small history table (Phase 3, migration `0061`).
8. **Six decisions are yours** (section 8). Phases 0 to 2 need none of them.

![Option C beside the baseline and the rejected forms, light theme](assets/2026-10-09-attack-paths-dashboard/options-light-wide.png)

*Mock-up page, not product code. Colours, type and spacing are the app's real tokens copied from
`globals.css`. Host names and counts are illustrative but shaped like the analyzer's real output.
Dark theme and a 420 px screen are in the appendix.*

---

## 1. What the section has to do

The operator on this dashboard runs several engagements. In a few seconds they need to answer:

| # | Question | Where the answer comes from |
| --- | --- | --- |
| 1 | Can an attacker reach a crown jewel? How many of them? | `choke.targets[].best_likelihood > 0` out of all targets |
| 2 | How many separate ways in? (one fix, or several?) | `choke.min_fix_set.independent_routes` (vertex-disjoint, by Menger's theorem) |
| 3 | What do I do first? | `choke.min_fix_set.assets`, `choke.ranked` |
| 4 | Can I trust this? | `coverage.confidence`, `freshness.stale_assets`, `computed_at`, "not computed yet" |
| 5 | Is it getting better? | **not stored today** (Phase 3) |
| 6 | Where do I go next? | link to `/engagements/{id}/attack-paths` |

The layout rule on this dashboard (`DashboardGrid.tsx`) is that nothing below the first tier competes
with it: no display numerals above 26 px, no colour outside severity and state. Stephen Few's
definition fits: a dashboard is read in brief glances and fails if it cannot say what matters in an
instant ([summary](https://www.theinformationlab.co.uk/community/blog/information-dashboard-design-stephen)).

## 2. What I found

### 2.1 In our own data: the headline number I shipped is the weak one

Read from `analyzer.py` and `routers/attack_paths.py`:

| What the dashboard shows now | What it really is | Better number already stored |
| --- | --- | --- |
| "8 routes" (`path_count`) | `len()` of a list capped at `max_paths_per_source=5` per entry point per crown jewel (`find_paths_to_target`). Grows with entry points, not with exposure | `min_fix_set.size`, `independent_routes` |
| "N crown jewels" (`len(choke.targets)`) | Jewels *considered*, reachable or not | `targets[].best_likelihood > 0` = reachable |
| "N entry points" (`choke.entry_points`) | Internet-exposed hosts *considered* | not stored per reachable jewel |

Measured on the repo's own validation fixtures (real analyzer output):

| Fixture | Stored route count | What matters |
| --- | --- | --- |
| `09` eight exposed hosts, one gateway | **8** | one fix (`gw`) cuts everything |
| `08` two independent routes | **4** | only 2 separate ways in; no single host fixes it (`ranked` is empty) |
| `01` flat internal network | **1** | one fix (`entry`) |

The count tracks the number of entry points, not how hard the crown jewel is to protect: `09` reads as
twice `08` although `08` needs more fixes. Sorting engagements by it would mislead. So the plan demotes the route count (it stays on the engagement page, labelled as a capped
list) and leads with reachability, independent routes and the fix set.

Also not stored: any history. `attack_path_analyses` holds one row per engagement, replaced on every
recompute, so no trend or "since last scan" can be shown yet.

### 2.2 How other products summarise attack paths

I could not open vendor pages from this environment (outbound fetches are blocked, only search
summaries came back), so this table is from search-result summaries. Check the linked pages before
quoting any of it.

| Product | What its summary view shows | Graph? | Source |
| --- | --- | --- | --- |
| Microsoft Exposure Management | A chart of attack paths **over time**, top choke points, top attack-path scenarios, top targets, top entry points; choke-point side panel with "View blast radius" | Drill-down | [docs](https://learn.microsoft.com/en-us/security-exposure-management/review-attack-paths) |
| Tenable One, Attack Path Analysis | Counts (vulnerable critical assets, attack paths), open findings by severity, a **matrix** (source-node exposure score × target criticality), a trending list, a "compare to" baseline with direction arrows | Drill-down | [docs](https://docs.tenable.com/tenableone/attack-path-analysis/Content/AttackPath/AttackPathDashboard.htm) |
| XM Cyber | Security score, choke points by severity, critical assets by severity, top compromising exposures (this from a third-party integration listing) | Separate view | [listing](https://cortex.marketplace.pan.dev/marketplace/details/XMCyber), [review](https://www.scworld.com/news/xm-cyber-1-35) |
| Wiz | Issues prioritised by impact; the full path in a graph view | Graph on the issue | [Wiz academy](https://www.wiz.io/academy/attack-path-analysis) |
| Horizon3 NodeZero | Paths ranked by impact, step-by-step summary per path, one-click check that a fix worked | Per path | [Horizon3](https://horizon3.ai/using-nodezero-to-uncover-the-paths-attackers-take-before-they-do) |

Pattern across all five: **summary = counts + ranked lists + change over time; graph = drill-down.**
Two things worth borrowing: a *trend/compare* element (Microsoft, Tenable), and *verification of a fix*
(Horizon3), which our "recompute after detection" already enables once history exists.
XM Cyber and Cyentia's research that only about 2% of exposures sit on choke points
([Cyentia](https://www.cyentia.com/value-of-choke-points/), vendor-sourced) supports giving the "fix first"
element as much visual weight as the exposure number.

### 2.3 What research says about the forms

- **Node-link graphs stop working at modest complexity.** Even the best layouts end as "hairballs";
  the remedy is aggregation or filtering ([Yoghourdjian et al., InfoVis 2020](https://vcg.seas.harvard.edu/publications/20201001-scalability-of-network-visualisation-from-a-cognitive-load-perspective)).
  For *path-finding* tasks, node-link beats matrices in the comparisons I found, though the studies
  disagree about large graphs ([Okoe et al., TVCG 2018](https://smsf.cs.arizona.edu/~kobourov/NL-AM-TVCG18.pdf),
  [layered-graph study, 2025](https://arxiv.org/pdf/2507.10883)). So: node-link is right for *one route*
  on the engagement page, wrong for a dashboard overview.
- **Attack-graph literature's fix is aggregation.** Group hosts into protection domains and show the
  domains ([Noel & Jajodia, ACSAC 2005](https://acsac.org/2005/abstracts/87.html),
  [aggregation framework](https://patents.google.com/patent/US7627900),
  [Homer et al., VizSEC 2008](https://www.cs.ksu.edu/~xou/publications/vizsec08.pdf)). Vedha already has
  subnet "hub" nodes, so a zone-level view is feasible later (Phase 5, optional).
- **Sankey diagrams promise a conserved quantity** (flow in equals flow out) and are hard to read for
  exact values ([guide](https://www.storytellingwithdata.com/blog/what-is-a-sankey-diagram)). Attack
  routes are not a conserved flow: eight routes through one gateway are one way in. A Sankey would
  overstate exposure. Rejected.
- **Risk matrices** can rank a smaller risk above a larger one and, with negatively correlated axes,
  do worse than random (Cox 2008, as summarised in a [2021 follow-up](https://arxiv.org/pdf/2103.05440)). Tenable's matrix
  also needs two per-path scores Vedha does not compute. Rejected.
- **Gauges use a lot of space to show only "now"**; Few designed the bullet graph to replace them
  ([summary](https://www.theinformationlab.co.uk/community/blog/information-dashboard-design-stephen)).
  The reachable-jewel meter below is a small count meter in that spirit, not a dial.

### 2.4 Technology, measured here

Bundle cost of each candidate, measured in this environment (esbuild, minified, `gzip -9`, React external).
The figures in web summaries disagreed with each other (for example 25 KB versus 113 KB for sigma), so
these are measured, not quoted.

| Candidate | gzip | Verdict |
| --- | --- | --- |
| d3-sankey | 2.8 KB | cheap, but wrong form (2.3) |
| dagre (`@dagrejs/dagre`) | 16.8 KB | a layered layout we do not need: roles give the columns |
| `@xyflow/react` (React Flow) | 59.3 KB | built for editable node editors; no layout engine included |
| Recharts `Sankey` | 74.6 KB | recharts is already loaded on the dashboard (`DashboardCharts`); wrong form |
| sigma + graphology | 112.8 KB | WebGL, for very large graphs; opaque to screen readers |
| cytoscape | 141.5 KB | analysis toolkit; heavy |
| elkjs (bundled) | 440.1 KB | nested/orthogonal routing; far beyond need |

**Conclusion: hand-rolled HTML/CSS plus a few inline SVG glyphs, 0 KB added.** The existing route map
on the engagement page is already hand-rolled SVG with its own layout function, so this matches the code
base. A sparkline (Phase 3) is one `<polyline>`.

### 2.5 Accessibility, checked against the app's own tokens

Contrast computed for the tokens a redesign would use, on `--bg-panel` and `--bg-surface`, both themes
(the lowest figure is shown):

| Token group | Lowest ratio | Needed | Result |
| --- | --- | --- | --- |
| `--text-primary`, `-secondary`, `-muted`, `-faint` | 4.55 | 4.5 (text) | pass |
| `--accent`, `--sev-critical/high/medium/low`, `--nominal` | 4.59 | 4.5 (text), 3 (graphics) | pass |
| **`--border-default`** | **1.45** | 3 (graphics that carry meaning) | **fail** |
| **`--border-strong`** | **2.07** | 3 | **fail** |

Consequences: marks that carry meaning (connectors, hollow shapes, meter outlines) use `--text-muted`
or stronger, never a border token. **Existing defect:** `.ap-edge { stroke: var(--border-strong) }` in
`app/engagements/[id]/attack-paths/styles.ts` draws the route-map edges at 2.68:1 (light) and 2.22:1
(dark). Role is already stated in words on every node, but which node connects to which is carried by
those edges. Fixed in Phase 0.

Other rules the design follows (from the data-viz guidance the repo's dashboard already uses): colour is
never the only channel (each role has a shape and a word), every chart has a text twin (the list), status
colours are reserved for state, no dual axes, marks are thin with 2 px gaps.

### 2.6 Limits of this research

- Vendor pages could not be opened; section 2.2 rests on search summaries.
- No user test: nobody has looked at this on a real engagement. The mock-up uses invented host names.
- The studies on node-link versus matrix disagree; I rely on them only for the narrow claim "a graph
  stops being readable as it grows", which they all support.
- Phase 0's numbers depend on the model's existing limits: only findings already marked exploitable
  create steps, targets are the assets marked critical, and reachability between subnets is inferred.
  P2, P3 and P4b remain unbuilt, so "0 reachable" never means "safe".

---

## 3. Options considered

| | Form | Answers Q1–Q6 | Honest? | Cost | Verdict |
| --- | --- | --- | --- | --- | --- |
| A | Ranked text rows (shipped) | 1, 3, 4, 6 partly; headline is the weak number | mostly | done | baseline: fix the numbers, add scan-ability |
| B | Tiles + rows with meters | 1–4, 6 | yes | S–M | the base of C |
| **C** | **B + "Fix first" card (route chain + ranked hosts)** | **1–4, 6 (5 in Phase 3)** | **yes** | **M** | **recommended** |
| D | Mini node-link graph | 6 only; unreadable beyond ~12 hosts | yes | M + a layout lib | rejected for the dashboard; keep on engagement page |
| E | Exposure × criticality matrix | needs scores we do not have | ordinal cells mislead | M | rejected |
| F | Sankey | implies conserved flow | **no** | S–M | rejected |
| G | Trend sparkline / change arrow | 5 | yes, with caveats (2.7) | M, needs a table | Phase 3 |
| H | Zone-level aggregated map | 3, 6; the literature's answer to hairballs | yes | L | optional Phase 5, engagement page |
| I | Item in "Needs attention now" | 3 | yes if neutral wording | S | decision D3 |

## 4. Recommended design (Option C)

### 4.1 Anatomy

```
Panel "Attack paths"                         [Beta]  updated 2 min ago
┌ tile ───────────────┬ tile ───────────────────┬ tile ──────────────┐
│ Crown jewels        │ Hosts to fix to cut     │ Not computed yet   │
│ reachable           │ every route             │                    │
│ 4 of 5 in the model │ 3 hosts                 │ 2 of 5 engagements │
└─────────────────────┴─────────────────────────┴────────────────────┘
┌ engagement ladder (top 5) ──────────────────┬ Fix first · <top engagement> ┐
│ Acme prod   ◆◆◇ 2 of 3 reachable · 1 way in │ ① ENTRY POINT  web-dmz-03    │
│   Fixing edge-gw-01 alone cuts every route. │   │ Observed                  │
│   [Coverage partial] [2 hosts not seen]     │ ② FIX HERE     edge-gw-01    │
│ Initech     ◆◆  2 of 2 reachable · 2 ways   │   │ Assumed route (verify)    │
│   No single host fixes this: gw1 and gw2    │ ③ CROWN JEWEL  fin-db-01     │
│ Globex      ◇  No crown jewels marked       │ Hosts ranked by risk removed │
│ Umbrella    ◇  Not computed yet             │ edge-gw-01 ████████░ 78      │
└─────────────────────────────────────────────┴──────────────────────────────┘
 footnote: what "no routes" and "not computed" mean         All engagements →
```

### 4.2 Each element, its data and its rule

| Element | Data | Rule |
| --- | --- | --- |
| Tile 1 "Crown jewels reachable: X of Y" | sum over **computed** engagements of reachable and total targets | caption states how many engagements are included ("from 3 engagements that have been computed"); `0 of 5` carries the "not evidence of safety" caveat |
| Tile 2 "Hosts to fix" | sum of `min_fix_set.size` over computed engagements | caption "smallest set per engagement, added together" (effort adds across separate networks; risk would not) |
| Tile 3 "Not computed yet" | count of engagements with no stored analysis | always shown (reads 0 when everything is computed); a gap in trust is surfaced, never folded into the other tiles |
| Jewel meter | one diamond per crown jewel (max 8, then "+N"): filled = reachable, hollow outline = not reachable, dashed = not computed or no target | the words "2 of 3 crown jewels reachable" sit beside it; the meter is `aria-hidden` |
| "N separate ways in" | max of `independent_routes` over reachable jewels | phrase is "separate ways in", never "routes" |
| Fix sentence | `min_fix_set` | unchanged from today; when `ranked` is empty and size > 1: "No single host fixes this" |
| Coverage / stale chips | `coverage.confidence`, `freshness.stale_assets` | unchanged: "partial", "observed", "not recorded", never "complete" |
| Route chain | top route by `risk_score`, hops with `basis` | roles by shape **and** word (entry, fix here, crown jewel); an assumed hop shows its caveat in words; rendered as an ordered list |
| Risk-removed bars | `choke.ranked[:3]` | one bar per host, **never stacked or summed** (each is an independent "if only this host were fixed"); caption "modelled 0–100 ordering weight, not a probability" |

Order of the ladder: engagements with reachable jewels first (most reachable, then highest modelled
risk, then name), then computed with none, then not computed. The modelled risk is an ordering weight
on one scale, so the ordering is stable; it is not a claim about likelihood.

### 4.3 Where it sits on the dashboard

Keep it in its own band under posture and SLA (as today). The ledger and posture are measured facts; this
section is a Beta model, so it should not outrank them. Optional pointer from the "Needs attention now"
strip is decision D3.

### 4.4 States (each is a different claim, so each looks different)

| State | Shows |
| --- | --- |
| Loading | skeleton with the final shape (tiles, rows, card) to avoid layout shift |
| Load failed | error with Retry; never an empty list |
| No engagements | "No engagements yet" with a hint |
| Engagements, none computed | tiles show dashes, tile 3 shows the count, rows say "Not computed yet", no fix card |
| Computed, zero reachable | tile 1 "0 of Y" with the not-safe caveat; rows keep their `why_empty` reason |
| Computed, no crown jewels marked | row says so ("No crown jewels marked") and the meter is dashed |
| Refetching | keep the previous render, reduced opacity, no skeleton flash |

### 4.5 Responsive, theme, motion, keyboard

- Two columns from 900 px, one column below. **The mock-up shows the row grid must also collapse below
  ~640 px** (name above facts); at 420 px the fixed name column squeezed the facts into a narrow strip.
- Dark theme works with the same tokens (checked in the mock-up and by the contrast table).
- No animation beyond the existing panel transitions; `prefers-reduced-motion` already handled globally.
- Rows are links (keyboard and screen reader reachable), the chain is an `<ol>`, the bars are a list
  with text values. v1 shows the top-ranked engagement in the card; picking another one is a later
  refinement.

## 5. Data and API changes

| Change | Where | Notes |
| --- | --- | --- |
| Overview row v2 | `app/graph/overview.py`, `routers/attack_paths.py` | add `jewels_total`, `jewels_reachable`, `ways_in` (max independent routes over reachable jewels), `fix_has_single` (whether any single host cuts all); keep `path_count` but mark it a capped list; all derived from the stored analysis, no new query |
| Focus card data | frontend only | reuses existing BFF routes: top path (`page_size=1`), its detail (hops and `basis`), and `analysis` (`choke.ranked`). Three cached requests, only for the top engagement. Trade-off: a new `/attack-paths/overview/focus` endpoint would be one request but one more surface; revisit if slow |
| View-model | `lib/attack-paths.ts` | `overviewLine` gains reachable/ways-in wording; new `overviewTiles(o)`, `focusChain(...)`, `riskBars(...)`; every sentence stays in one tested place |
| History | migration `0061`, `attack_path_snapshots` | Phase 3 only (below) |

## 6. Phases

Each phase ships with tests and keeps `tsc`, `eslint`, backend and frontend suites green. None adds a
dependency.

### Phase 0 — correct the numbers and fix the contrast (S)

- Backend: overview row v2 (above). Test from the real fixtures: `09` must produce "1 host to fix", never
  "8" as a headline; `08` must produce "2 separate ways in" and "no single host fixes this".
- Frontend: `overviewLine` leads with reachable jewels; route count moves to a capped-list note.
- Route map edge colour `--border-strong` → `--text-muted`; a unit test asserts every token used for an
  edge or connector reaches 3:1 in both themes (script computes it).
- Type-scale cleanup: the panel uses 10.5 px and 11.5 px where the tokens say 11 and 12.
- **Done when:** the dashboard and `/attack-paths` page show the new wording; tests above pass.

### Phase 1 — tiles and the ladder (M)

- `AttackPathsTiles`, `JewelMeter`, rebuilt `OverviewList` rows (shared by the dashboard and the
  `/attack-paths` page); responsive collapse below 640 px; skeleton parity.
- **Done when:** screenshots (light, dark, 420 px, 1240 px) match the mock-up within layout tolerance,
  the table-equivalent text is present for every glyph, and the honesty tests (never "0 routes" for
  not-computed; "not evidence of safe" on zero) pass.

### Phase 2 — "Fix first" card (M)

- `FixFirstCard` with `RouteChain` and `RiskBars`; three queries enabled only for the top engagement.
- Edge cases to test: no `ranked` (redundant routes), a path with an assumed hop, a stale hop, a
  label-less host (falls back to its address), a long name (truncates, full name in the title attribute),
  top engagement changes between refetches.
- **Done when:** the card never shows a bar sum, never shows a route without its caveats, and degrades to
  the fix sentence if the detail request fails.

### Phase 3 — history and trend (M) — needs decision D4

- Migration `0061_attack_path_snapshots`: `(engagement_id, computed_at, jewels_total, jewels_reachable,
  fix_set_size, entry_points, coverage, trigger)`; written by `_store_analysis`; retention: keep
  everything for 7 days, then one per day, cap 90 rows per engagement.
- Overview returns the last 12 `jewels_reachable` values per engagement; tile 1 gets a "since last scan"
  line and rows get a sparkline (one `<polyline>`, 2 px, current point ringed).
- **Caveat to build in:** a rise can mean better scanning rather than a worse network (more hosts seen).
  The wording is "changed", never "worse/better", and a snapshot notes when coverage changed.
- **Done when:** migration up/down verified on PostgreSQL, retention test, and the sparkline has a text
  twin ("reachable crown jewels: 3, 3, 4, 4").

### Phase 4 — surfacing (S, decisions D3 and D5)

- Optional "Needs attention now" item (neutral tone, "Beta" label, only when a jewel is reachable).
- Optional "Compute" button on not-computed rows (a write; confirm first; operators only).

### Phase 5 — zone view on the engagement page (L, optional)

- Aggregate hosts into their subnets (protection domains) and show the route as a strip of zones
  (internet → DMZ → servers → jewel's zone), the aggregation the literature recommends. Needs the
  path-to-segment mapping that the d3 output already carries as `groups`.

## 7. Verification plan

- **Unit:** view-model sentences, tile aggregation (computed engagements only), ladder ordering, every
  state in 4.4, token contrast, escaping of engagement and host names (they are untrusted text).
- **Backend:** fixture-driven overview tests, tenant scoping, read-only SQL, role gating (unchanged).
- **Browser (Playwright, as before):** dashboard, `/attack-paths`, customer portal does not show it,
  error and empty states, dark theme, 420 px, keyboard path through rows and card, no horizontal scroll.
- **Visual baselines:** the repo already has `npm run test:visual`; add the dashboard section to it.
- **Performance budget:** 0 KB added; overview stays 2 to 3 queries; card requests only for one
  engagement; refetch every 120 s as now.
- **What I will still not be able to claim:** that it reads right on real engagement data. That needs you
  to open it on a real engagement with crown jewels marked.

## 8. Decisions for you

| # | Decision | My recommendation |
| --- | --- | --- |
| D1 | Headline metric: "crown jewels reachable" or keep "N routes"? | reachable jewels; keep routes only as a capped-list note |
| D2 | Should customers see this on the portal dashboard? | no for now (operator-only); revisit after real-data review |
| D3 | Add a neutral item to "Needs attention now"? | yes, with the Beta label, only when a jewel is reachable |
| D4 | Add history (migration `0061`) for the trend? | yes, after Phase 2 |
| D5 | Allow "Compute" from the dashboard (a write)? | not in v1; keep the dashboard read-only |
| D6 | Keep the Beta label until reviewed on real data and P2/P3/P4b are decided? | yes |

## 9. Appendix: mock-up views

Dark theme:

![Dark theme](assets/2026-10-09-attack-paths-dashboard/options-dark-wide.png)

420 px screen (shows the row grid must collapse below ~640 px):

![Narrow screen](assets/2026-10-09-attack-paths-dashboard/options-light-narrow.png)

## 10. Sources

Read as search-result summaries only (pages could not be opened from this environment):
[Microsoft](https://learn.microsoft.com/en-us/security-exposure-management/review-attack-paths) ·
[Tenable](https://docs.tenable.com/tenableone/attack-path-analysis/Content/AttackPath/AttackPathDashboard.htm) ·
[XM Cyber listing](https://cortex.marketplace.pan.dev/marketplace/details/XMCyber) ·
[SC World on XM Cyber](https://www.scworld.com/news/xm-cyber-1-35) ·
[Cyentia on choke points](https://www.cyentia.com/value-of-choke-points/) ·
[Wiz](https://www.wiz.io/academy/attack-path-analysis) ·
[Horizon3](https://horizon3.ai/using-nodezero-to-uncover-the-paths-attackers-take-before-they-do) ·
[Yoghourdjian et al.](https://vcg.seas.harvard.edu/publications/20201001-scalability-of-network-visualisation-from-a-cognitive-load-perspective) ·
[Okoe et al.](https://smsf.cs.arizona.edu/~kobourov/NL-AM-TVCG18.pdf) ·
[layered-graph study](https://arxiv.org/pdf/2507.10883) ·
[Noel & Jajodia](https://acsac.org/2005/abstracts/87.html) ·
[aggregation framework](https://patents.google.com/patent/US7627900) ·
[Homer et al.](https://www.cs.ksu.edu/~xou/publications/vizsec08.pdf) ·
[Cox and later work](https://arxiv.org/pdf/2103.05440) ·
[Few](https://www.theinformationlab.co.uk/community/blog/information-dashboard-design-stephen) ·
[Sankey guidance](https://www.storytellingwithdata.com/blog/what-is-a-sankey-diagram) ·
[accessible graph visualisation](https://cambridge-intelligence.com/build-accessible-data-visualization-apps-with-keylines/) ·
[React Flow layouting](https://reactflow.dev/learn/layouting/layouting) ·
[ELK vs dagre](https://calm.finos.org/calm-studio/adrs/use-elk-for-auto-layout).

Measured here: bundle sizes (esbuild + gzip), token contrast, analyzer output on the nine validation
fixtures (`manager/backend/tests/fixtures/attack_paths`).
