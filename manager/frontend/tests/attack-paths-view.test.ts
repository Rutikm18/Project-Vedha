import assert from "node:assert/strict";
import test from "node:test";
import {
  basisInfo, caveatSummary, emptyReasons, fixFirstSummary, fixPointIds, fixSentence, focusBars, focusLead,
  attackPathAttention, canCompute, freshnessInfo, layoutPathMap, layoutZoneMap, MAP, meterCells, overviewLine, overviewState, overviewSummary, overviewTiles,
  percent, riskLabel, riskShare, routeChainView, shortDate, sparkline, targetExposed, techniqueLabel, trendView, truncateLabel, ZONE, zoneRoles, zoneSummary,
  type ChokeAnalysis, type Coverage, type Diagnostics, type Focus, type FocusNode, type FocusRoute,
  type FreshnessReport, type HistoryPoint, type Overview, type Zone, type ZoneLink, type ZoneView, type OverviewRow, type OverviewSummary, type PathSummary,
} from "../lib/attack-paths";

function route(id: string, ...hosts: string[]): PathSummary {
  return {
    id, risk_score: 50, hops: hosts.length - 1,
    source: `asset:${hosts[0]}`, target: `asset:${hosts[hosts.length - 1]}`,
    source_label: hosts[0], target_label: hosts[hosts.length - 1],
    freshness: "fresh", chokepoint_count: 0,
    nodes: hosts.map((h) => ({ asset_id: h, label: h.toUpperCase() })),
  };
}

// ── wording ──────────────────────────────────────────────────────────────────

test("an assumed route says it is assumed, in words, and an observed one does not", () => {
  const assumed = basisInfo("assumed");
  assert.equal(assumed.tone, "weak");
  assert.match(assumed.caveat ?? "", /assumed, not observed/);
  assert.equal(basisInfo("observed").caveat, null);
  assert.equal(basisInfo("observed").tone, "firm");
});

test("cross-site and name-only links are marked weak and explain why", () => {
  assert.match(basisInfo("assumed_cross_site").caveat ?? "", /unlikely by default/);
  assert.equal(basisInfo("assumed_cross_site").tone, "weak");
  assert.match(basisInfo("same_host_name").caveat ?? "", /host name alone/);
  assert.equal(basisInfo("same_host_fqdn").caveat, null);
});

test("an unknown basis still renders a readable label instead of vanishing", () => {
  assert.equal(basisInfo("some_new_basis").label, "Some new basis");
  assert.equal(basisInfo(null).label, "Direct step");
  assert.equal(basisInfo(undefined).tone, "neutral");
});

test("freshness maps to a label and never calls stale data recent", () => {
  assert.deepEqual(freshnessInfo("fresh"), { label: "Recent", tone: "firm" });
  assert.equal(freshnessInfo("partly_stale").label, "Partly stale");
  assert.equal(freshnessInfo("stale").tone, "weak");
});

test("numbers that are missing render a dash, not 0", () => {
  assert.equal(percent(null), "—");
  assert.equal(percent(undefined), "—");
  assert.equal(percent(NaN), "—");
  assert.equal(percent(0.634), "63%");
  assert.equal(percent(1.4), "100%");
  assert.equal(riskLabel(null), "—");
  assert.equal(riskLabel(42.567), "42.6");
});

test("technique codes read as phrases", () => {
  assert.equal(techniqueLabel("CROSS_SUBNET"), "Across subnets");
  assert.equal(techniqueLabel("GATEWAY_ROUTE"), "Through a gateway");
  assert.equal(techniqueLabel("NEW_THING"), "New thing");
  assert.equal(techniqueLabel(null), "Step");
});

// ── empty results ────────────────────────────────────────────────────────────

const diag = (codes: [string, string][]): Diagnostics => ({
  assets: 0, findings: 0, exploitable_findings: 0, entry_points: 0, internet_exposed_assets: 0, targets: 0,
  reachability_edges: 0, control_edges: 0, segments: 0, reachability_posture: null, unplaced_assets: 0,
  reasons: codes.map(([code, detail]) => ({ code, detail })),
});

test("every reason the backend can give has a title and something to do about it", () => {
  const codes = ["no_assets", "no_entry_points", "entry_points_not_compromisable", "no_targets",
    "no_reachability", "no_exploitable_steps", "no_control_edges"];
  const out = emptyReasons(diag(codes.map((c) => [c, `evidence for ${c}`])));
  assert.equal(out.length, codes.length);
  for (const r of out) {
    assert.ok(r.title && !r.title.includes("_"), r.code);
    assert.ok(r.action.length > 10, `${r.code} needs a next step`);
    assert.match(r.evidence, /^evidence for/);
  }
});

test("the crown-jewel reason tells the operator to mark targets, and does not promise auto-selection", () => {
  const [r] = emptyReasons(diag([["no_targets", "x"]]));
  assert.match(r.action, /Mark the systems/);
  assert.doesNotMatch(r.action, /auto/i);
});

test("an unknown reason code is shown, not dropped", () => {
  const [r] = emptyReasons(diag([["brand_new_gap", "something the model lacked"]]));
  assert.equal(r.title, "Brand new gap");
  assert.equal(r.evidence, "something the model lacked");
  assert.equal(r.action, "");
});

test("no diagnostics means no reasons, not an invented one", () => {
  assert.deepEqual(emptyReasons(null), []);
  assert.deepEqual(emptyReasons(undefined), []);
});

// ── fix first ────────────────────────────────────────────────────────────────

const choke = (over: Partial<ChokeAnalysis> = {}): ChokeAnalysis => ({
  ranked: [],
  min_fix_set: { size: 1, assets: [{ asset_id: "g", label: "gateway-1" }], independent_routes: { "db-1": 1 } },
  targets: [{ asset_id: "d", label: "db-1", best_likelihood: 0.5, risk: 40 }],
  ...over,
});

test("a single shared host reads as one decision", () => {
  const s = fixFirstSummary(choke());
  assert.equal(s?.headline, "Fixing gateway-1 alone cuts every modelled route to a crown jewel.");
  assert.match(s?.routes[0] ?? "", /one route reaches it/);
});

test("several independent routes say that one fix is not enough", () => {
  const s = fixFirstSummary(choke({
    min_fix_set: {
      size: 2, assets: [{ asset_id: "a", label: "web-1" }, { asset_id: "b", label: "web-2" }],
      independent_routes: { "db-1": 2 },
    },
  }));
  assert.equal(s?.headline, "Cutting every modelled route takes 2 hosts: web-1, web-2.");
  assert.match(s?.routes[0] ?? "", /2 independent routes reach it, so fixing one host on one route is not enough/);
});

test("no route to any target is stated plainly, and no targets means no summary", () => {
  const none = fixFirstSummary(choke({ min_fix_set: { size: 0, assets: [], independent_routes: {} } }));
  assert.equal(none?.headline, "No modelled route reaches a crown jewel.");
  assert.equal(fixFirstSummary(choke({ targets: [] })), null);
  assert.equal(fixFirstSummary(null), null);
});

test("risk share is the fraction of modelled risk one fix removes, clamped", () => {
  const targets = [{ asset_id: "d", label: "d", best_likelihood: 1, risk: 30 }, { asset_id: "e", label: "e", best_likelihood: 1, risk: 20 }];
  const entry = { asset_id: "g", label: "g", risk_removed: 25, targets_cut_off: [], targets_cut_off_labels: [], remediation_priority: "high" as const };
  assert.equal(riskShare(entry, targets), 0.5);
  assert.equal(riskShare({ ...entry, risk_removed: 500 }, targets), 1);
  assert.equal(riskShare(entry, []), 0);
});

// ── caveats ──────────────────────────────────────────────────────────────────

const coverage = (over: Partial<Coverage> = {}): Coverage => ({
  basis: "hosts observed per subnet", confidence: "observed", segments: [],
  scope_without_observed_hosts: [], observed_outside_scope: [], assets_placed: 5,
  assets_without_a_subnet: 0, inferred_subnets: 0, ...over,
});
const fresh = (over: Partial<FreshnessReport> = {}): FreshnessReport => ({
  window_days: 30, assets: 5, stale_assets: 0, stale_fraction: 0, assets_without_timestamp: 0,
  oldest_seen: null, newest_seen: null, ...over,
});

test("clean reports produce no caveats and report observed, never complete", () => {
  const s = caveatSummary(coverage(), fresh());
  assert.equal(s.confidence, "observed");
  assert.deepEqual(s.items, []);
});

test("unscanned ranges are named and say a route through them cannot appear", () => {
  const s = caveatSummary(coverage({
    confidence: "partial",
    scope_without_observed_hosts: [
      { cidr: "10.9.0.0/24", addresses: 256 }, { cidr: "10.8.0.0/24", addresses: 256 },
      { cidr: "10.7.0.0/24", addresses: 256 }, { cidr: "10.6.0.0/24", addresses: 256 },
    ],
  }), fresh());
  assert.equal(s.confidence, "partial");
  assert.match(s.items[0].text, /4 ranges in scope with no observed host \(10\.9\.0\.0\/24, 10\.8\.0\.0\/24, 10\.7\.0\.0\/24 and 1 more\)/);
  assert.match(s.items[0].text, /cannot appear/);
});

test("stale hosts are counted against the window", () => {
  const s = caveatSummary(coverage(), fresh({ stale_assets: 2, assets: 9, window_days: 30 }));
  assert.match(s.items[0].text, /2 of 9 hosts not seen in the last 30 days/);
});

test("singular and plural agree", () => {
  const s = caveatSummary(coverage({ assets_without_a_subnet: 1, inferred_subnets: 1 }), fresh({ assets_without_timestamp: 1 }));
  const text = s.items.map((i) => i.text).join(" | ");
  assert.match(text, /1 host without an IP address, so it is not placed/);
  assert.match(text, /1 subnet inferred/);
  assert.match(text, /1 host with no last-seen time/);
});

test("missing reports are an unknown, never a clean result", () => {
  const s = caveatSummary(null, null);
  assert.equal(s.confidence, "unknown");
  assert.equal(s.items.length, 2);
  assert.match(s.items[0].text, /No coverage report/);
});

// ── route map ────────────────────────────────────────────────────────────────

test("a single route lays out left to right, entry to target", () => {
  const m = layoutPathMap([route("p1", "web", "app", "db")]);
  const by = Object.fromEntries(m.nodes.map((n) => [n.id, n]));
  assert.deepEqual([by.web.col, by.app.col, by.db.col], [0, 1, 2]);
  assert.ok(by.web.isEntry && !by.web.isTarget);
  assert.ok(by.db.isTarget && !by.db.isEntry);
  assert.equal(m.edges.length, 2);
  assert.ok(m.edges.every((e) => !e.backward && e.paths[0] === "p1"));
  assert.ok(m.edges[0].x2 > m.edges[0].x1);
});

test("routes that converge share a node, mark it as a choke point and record which routes use each step", () => {
  const m = layoutPathMap(
    [route("p1", "web1", "gw", "db"), route("p2", "web2", "gw", "db")],
    new Set(["gw"]),
  );
  assert.equal(m.nodes.filter((n) => n.id === "gw").length, 1);
  assert.equal(m.nodes.find((n) => n.id === "gw")?.isChoke, true);
  assert.equal(m.nodes.find((n) => n.id === "web1")?.isChoke, false);
  const shared = m.edges.find((e) => e.from === "gw" && e.to === "db");
  assert.deepEqual(shared?.paths, ["p1", "p2"]);
  // two entries stack in one column without overlapping
  const entries = m.nodes.filter((n) => n.isEntry);
  assert.equal(new Set(entries.map((n) => n.y)).size, 2);
});

test("a longer route pushes shared hosts right so no step runs backwards", () => {
  const m = layoutPathMap([route("p1", "a", "b", "t"), route("p2", "a", "x", "b", "t")]);
  const by = Object.fromEntries(m.nodes.map((n) => [n.id, n.col]));
  assert.ok(by.b > by.x && by.x > by.a);
  assert.ok(m.edges.every((e) => !e.backward));
});

test("routes that disagree about direction terminate, and the odd edge is flagged", () => {
  const m = layoutPathMap([route("p1", "a", "b", "t"), route("p2", "b", "a", "t")]);
  assert.equal(m.nodes.length, 3);
  assert.ok(m.edges.some((e) => e.backward), "the cycle must be visible, not hidden");
});

test("only the highest-risk routes are drawn, and the map says how many", () => {
  const items = Array.from({ length: 30 }, (_, i) => route(`p${i}`, `s${i}`, "mid", "t"));
  const m = layoutPathMap(items, new Set(), 5);
  assert.equal(m.shown, 5);
  assert.equal(m.nodes.filter((n) => n.isEntry).length, 5);
});

test("layout is deterministic and sized to its content", () => {
  const items = [route("p1", "web1", "gw", "db"), route("p2", "web2", "gw", "db")];
  assert.deepEqual(layoutPathMap(items), layoutPathMap(items));
  const m = layoutPathMap(items);
  assert.equal(m.width, MAP.pad * 2 + 2 * MAP.colWidth + MAP.nodeWidth);
  assert.equal(m.height, MAP.pad * 2 + 1 * MAP.rowHeight + MAP.nodeHeight);
});

test("routes with fewer than two hosts, or none at all, produce an empty map", () => {
  assert.equal(layoutPathMap([]).nodes.length, 0);
  assert.equal(layoutPathMap([route("p", "only")]).nodes.length, 0);
  const empty = layoutPathMap([]);
  assert.ok(empty.width > 0 && empty.height > 0);
});

test("truncation keeps short labels intact and marks cut ones", () => {
  assert.equal(truncateLabel("web-1"), "web-1");
  assert.equal(truncateLabel("a".repeat(40), 10), `${"a".repeat(9)}…`);
  assert.equal(truncateLabel(""), "");
});

test("fix points are the cutting set plus the few biggest single wins, not every ranked host", () => {
  const entry = (id: string, removed: number) => ({
    asset_id: id, label: id, risk_removed: removed, targets_cut_off: [], targets_cut_off_labels: [],
    remediation_priority: "medium" as const,
  });
  const c = choke({
    ranked: [entry("a", 40), entry("b", 30), entry("c", 20), entry("d", 10), entry("e", 0)],
    min_fix_set: { size: 1, assets: [{ asset_id: "gw", label: "gw" }], independent_routes: {} },
  });
  assert.deepEqual([...fixPointIds(c)].sort(), ["a", "b", "c", "gw"]);
  assert.deepEqual([...fixPointIds(c, 5)].sort(), ["a", "b", "c", "d", "gw"], "a host that removes no risk is never a fix point");
  assert.equal(fixPointIds(null).size, 0);
});


// ── an exposed crown jewel on the engagement page ───────────────────────────

test("a crown jewel that is itself exposed is never told 'fix the gateway'", () => {
  const exposed = choke({ targets: [{ asset_id: "d", label: "db-1", best_likelihood: 1, risk: 100, exposed_directly: true }] });
  const s = fixFirstSummary(exposed);
  assert.match(s?.headline ?? "", /db-1 is exposed to the internet and can be exploited directly/);
  assert.match(s?.headline ?? "", /Fixing other hosts does not protect it; remove that exposure first\./);
  assert.doesNotMatch(s?.headline ?? "", /alone cuts every/);
  assert.deepEqual(s?.routes, []);
});

test("analyses stored before the flag existed are read by their likelihood of exactly 1", () => {
  assert.equal(targetExposed({ best_likelihood: 1 }), true);
  assert.equal(targetExposed({ best_likelihood: 0.95 }), false);
  assert.equal(targetExposed({ best_likelihood: 1, exposed_directly: false }), false, "an explicit flag wins");
  assert.equal(targetExposed({ best_likelihood: 0.2, exposed_directly: true }), true);
});

// ── overview rows (dashboard) ────────────────────────────────────────────────

const orow = (over: Partial<OverviewRow> = {}): OverviewRow => ({
  engagement_id: "e1", name: "Acme", status: "active", state: "reachable", computed: true,
  computed_at: "2026-10-09T09:00:00Z", path_count: 8, entry_points: 8, crown_jewels: 3,
  jewels_total: 3, jewels_reachable: 2, jewels_exposed: 0, ways_in: 1, top_risk: 40,
  fix_set_size: 1, fix_assets: ["edge-gw-01"], fix_assets_more: 0, coverage: "partial", stale_assets: 1, why_empty: [], ...over,
});
const never = (): OverviewRow => orow({
  state: "not_computed", computed: false, computed_at: null, path_count: null, entry_points: null, crown_jewels: null,
  jewels_total: null, jewels_reachable: null, jewels_exposed: null, ways_in: null, top_risk: null,
  fix_set_size: null, fix_assets: [], coverage: null, stale_assets: null,
});

test("reachable: the headline counts crown jewels, never routes; the fix and the ways in follow", () => {
  const line = overviewLine(orow());
  assert.equal(line.headline, "2 of 3 crown jewels reachable");
  assert.equal(line.ways, "1 separate way in");
  assert.equal(line.detail, "Fixing edge-gw-01 alone cuts every route.");
  assert.deepEqual(line.coverage, { label: "Coverage partial", tone: "weak" });
  assert.equal(line.stale, "1 host not seen recently");
  assert.doesNotMatch(JSON.stringify(line), /\b8 routes|\broutes\b.*8/, "the capped route count is not shown");
  assert.equal(overviewLine(orow({ jewels_total: 1, jewels_reachable: 1 })).headline, "1 of 1 crown jewel reachable");
});

test("several fixes say 'no single host', a long list counts the rest, none found says so", () => {
  const two = overviewLine(orow({ fix_set_size: 2, fix_assets: ["gw1", "gw2"], ways_in: 2 }));
  assert.equal(two.ways, "2 separate ways in");
  assert.equal(two.detail, "No single host fixes this: cutting every route takes 2 hosts: gw1, gw2.");
  assert.equal(fixSentence({ fix_set_size: 6, fix_assets: ["a", "b", "c"], fix_assets_more: 3 }),
    "No single host fixes this: cutting every route takes 6 hosts: a, b, c, +3 more.");
  assert.equal(fixSentence({ fix_set_size: 0, fix_assets: [], fix_assets_more: 0 }), "The analysis found no host whose fix cuts these routes.");
  assert.equal(fixSentence({ fix_set_size: null, fix_assets: [], fix_assets_more: 0 }), null);
});

test("exposed: the worst case is said outright, with no fix-the-gateway and no 'ways in'", () => {
  const line = overviewLine(orow({ state: "exposed", jewels_exposed: 1, jewels_reachable: 1, jewels_total: 1, ways_in: null }));
  assert.equal(line.headline, "1 crown jewel directly exposed to the internet");
  assert.equal(line.detail, "Fixing hosts on the way in does not protect it. Remove the exposure first.");
  assert.equal(line.ways, null);
  assert.doesNotMatch(JSON.stringify(line), /alone cuts every route/);
  const mixed = overviewLine(orow({ state: "exposed", jewels_exposed: 1, jewels_reachable: 3, jewels_total: 3, ways_in: null }));
  assert.match(mixed.detail ?? "", /2 more crown jewels can be reached by a route\./);
});

test("unreachable keeps its reason and never claims safety", () => {
  const line = overviewLine(orow({ state: "unreachable", jewels_reachable: 0, ways_in: null, fix_set_size: 0, fix_assets: [],
    why_empty: [{ code: "no_entry_points", detail: "no asset is internet-exposed" }] }));
  assert.equal(line.headline, "No modelled route reaches a crown jewel");
  assert.match(line.detail ?? "", /This is not evidence the network is safe\.$/);
  assert.doesNotMatch(JSON.stringify(line), /all clear|you are safe|no risk/i);
  const bare = overviewLine(orow({ state: "unreachable", jewels_reachable: 0, why_empty: [] }));
  assert.match(bare.detail ?? "", /The analysis recorded no reason\. This is not evidence the network is safe\./);
});

test("no crown jewel marked, not recorded and not computed are 'cannot assess', never '0 reachable'", () => {
  const noTargets = overviewLine(orow({ state: "no_targets", jewels_total: 0, jewels_reachable: 0 }));
  assert.equal(noTargets.headline, "No crown jewels marked");
  assert.match(noTargets.detail ?? "", /not evidence the network is safe/);
  assert.doesNotMatch(noTargets.detail ?? "", /^No hosts yet/);
  const empty = overviewLine(orow({ state: "no_targets", jewels_total: 0, jewels_reachable: 0,
    why_empty: [{ code: "no_assets", detail: "the engagement has no assets yet" }, { code: "no_targets", detail: "x" }] }));
  assert.match(empty.detail ?? "", /^No hosts yet\. No asset is marked critical/, "the engagement with no hosts says so first");
  const unknown = overviewLine(orow({ state: "unrecorded", jewels_total: null, jewels_reachable: null }));
  assert.equal(unknown.headline, "Computed; per-jewel detail not recorded");
  assert.doesNotMatch(JSON.stringify(unknown), /\b0 of\b/);
  const nc = overviewLine(never());
  assert.equal(nc.headline, "Not computed yet");
  assert.equal(nc.coverage, null);
  assert.doesNotMatch(JSON.stringify(nc), /0 routes|0 of|Coverage/);
});

test("coverage the analysis did not record is said to be missing, not 'observed'", () => {
  assert.deepEqual(overviewLine(orow({ coverage: null })).coverage, { label: "Coverage not recorded", tone: "neutral" });
  assert.deepEqual(overviewLine(orow({ coverage: "observed" })).coverage, { label: "Coverage observed", tone: "firm" });
});

test("a server that predates `state` is classified only from what the fields prove", () => {
  const old = (over: Partial<OverviewRow>) => ({ ...orow(over), state: undefined });
  assert.equal(overviewState(old({ computed: false })), "not_computed");
  assert.equal(overviewState(old({ jewels_total: null })), "unrecorded");
  assert.equal(overviewState(old({ jewels_total: 0 })), "no_targets");
  assert.equal(overviewState(old({ jewels_exposed: 1 })), "exposed");
  assert.equal(overviewState(old({})), "reachable");
  assert.equal(overviewState(old({ jewels_reachable: 0 })), "unreachable");
});

test("the meter is one diamond per crown jewel, capped at 8, with the rest counted", () => {
  assert.deepEqual(meterCells(orow()), { cells: ["reachable", "reachable", "unreachable"], more: 0 });
  const wide = meterCells(orow({ jewels_total: 12, jewels_reachable: 2 }));
  assert.equal(wide.cells.length, 8);
  assert.equal(wide.more, 4);
  assert.equal(wide.cells.filter((c) => c === "reachable").length, 2);
  assert.deepEqual(meterCells(orow({ jewels_total: 12, jewels_reachable: 11 })).cells.filter((c) => c === "reachable").length, 8);
  for (const r of [never(), orow({ state: "no_targets", jewels_total: 0 }), orow({ state: "unrecorded", jewels_total: null })]) {
    assert.deepEqual(meterCells(r), { cells: ["unknown"], more: 0 });
  }
});

// ── tiles and the footer line ────────────────────────────────────────────────

const summary = (over: Partial<OverviewSummary> = {}): OverviewSummary => ({
  engagements: 5, computed: 4, assessed: 3, with_reachable: 2, exposed: 0, single_fix: 1,
  not_computed: 1, no_targets: 1, unrecorded: 0, jewels_total: 5, jewels_reachable: 4, ...over,
});

test("the tiles count engagements, and say what they are counted out of", () => {
  const [a, b, c] = overviewTiles(summary())!;
  assert.deepEqual([a.value, a.unit, a.tone], ["2", "of 3 assessed", "high"]);
  assert.equal(a.sub, "4 of 5 crown jewels reachable across them.");
  assert.deepEqual([b.value, b.unit], ["1", "of 2"]);
  assert.equal(b.sub, "1 need several fixes.");
  assert.deepEqual([c.value, c.unit], ["2", "engagements"]);
  assert.equal(c.sub, "1 not computed · 1 with no crown jewel marked.");
});

test("an exposed jewel makes tile 1 critical and keeps it out of the one-fix count", () => {
  const [a, b] = overviewTiles(summary({ exposed: 1, with_reachable: 2, single_fix: 1 }))!;
  assert.equal(a.tone, "critical");
  assert.equal(a.sub, "1 with a crown jewel directly exposed to the internet.");
  assert.deepEqual([b.value, b.unit], ["1", "of 1"], "2 reachable minus 1 exposed leaves 1 that a fix on the way in can help");
  assert.equal(b.sub, "One host each cuts every route.");
});

test("nothing assessed shows a dash, never '0 of 0'", () => {
  const none = overviewTiles(summary({ assessed: 0, with_reachable: 0, computed: 0, not_computed: 5, no_targets: 0 }))!;
  assert.deepEqual([none[0].value, none[0].unit, none[0].sub], ["—", "", "Nothing computed yet."]);
  assert.equal(none[1].value, "—");
  const marked = overviewTiles(summary({ assessed: 0, with_reachable: 0, computed: 2, not_computed: 0, no_targets: 2 }))!;
  assert.equal(marked[0].sub, "No computed engagement has a crown jewel marked.");
});

test("zero reachable among the assessed says so without claiming safety; all assessed says that", () => {
  const [a, , c] = overviewTiles(summary({ with_reachable: 0, single_fix: 0, not_computed: 0, no_targets: 0 }))!;
  assert.equal(a.value, "0");
  assert.match(a.sub, /not evidence the network is safe/);
  assert.equal(c.sub, "Every engagement has been assessed.");
  assert.equal(overviewTiles(null), null);
  assert.equal(overviewTiles(undefined), null);
});

test("the footer line counts only what is true", () => {
  const o = (s: OverviewSummary | null): Overview => ({ total: 5, shown: 3, summary: s, engagements: [orow()] });
  assert.equal(overviewSummary(o(summary())), "2 of 3 assessed engagements have a reachable crown jewel · 2 can't be assessed yet");
  assert.equal(overviewSummary(o(summary({ with_reachable: 1, assessed: 1, not_computed: 0, no_targets: 0 }))),
    "1 of 1 assessed engagement has a reachable crown jewel");
  assert.equal(overviewSummary(o(summary({ assessed: 0, with_reachable: 0 }))), "No engagement assessed yet · 2 can't be assessed yet");
  assert.equal(overviewSummary({ total: 0, shown: 0, summary: summary({ engagements: 0 }), engagements: [] }), "No engagements");
  assert.equal(overviewSummary(null), "");
});

// ── the "fix first" card ─────────────────────────────────────────────────────

const node = (label: string, role: FocusNode["role"], on = false): FocusNode => ({ asset_id: label, label, role, on_fix_list: on });
const routeOf = (nodes: FocusNode[], bases: (string | null)[] = []): FocusRoute => ({
  path_id: "p", risk_score: 12, freshness: "fresh", nodes,
  hops: nodes.slice(0, -1).map((_, i) => ({ basis: bases[i] ?? "observed", technique: null, stale: false, exploited: true })),
});
const focusOf = (over: Partial<Focus> = {}): Focus => ({
  engagement_id: "e1", name: "Acme", state: "reachable", computed: true, computed_at: "2026-10-09T09:00:00Z", path_count: 8,
  exposed: [], route: null, ranked: [],
  fix: { size: 1, assets: [{ asset_id: "gw", label: "edge-gw-01" }], independent_routes: {} }, ...over,
});

test("the lead sentence follows the fix set, and an exposed jewel is told to remove its exposure", () => {
  assert.equal(focusLead(focusOf()), "Fixing edge-gw-01 alone cuts every modelled route to a crown jewel.");
  assert.equal(focusLead(focusOf({ fix: { size: 2, assets: [{ asset_id: "a", label: "gw1" }, { asset_id: "b", label: "gw2" }], independent_routes: {} } })),
    "No single host fixes this: cutting every modelled route takes 2 hosts: gw1, gw2.");
  assert.equal(focusLead(focusOf({ fix: { size: 0, assets: [], independent_routes: {} } })), "The analysis found no host whose fix cuts these routes.");
  const exposed = focusLead(focusOf({ state: "exposed", exposed: [{ asset_id: "j", label: "fin-db-01" }] }));
  assert.match(exposed ?? "", /fin-db-01 is exposed to the internet and can be exploited directly\./);
  assert.doesNotMatch(exposed ?? "", /alone cuts/);
  assert.equal(focusLead(focusOf({ state: "unreachable" })), null);
});

test("a short route is drawn whole, with each step described between its two hosts", () => {
  const chain = routeChainView(routeOf([node("web-1", "entry"), node("gw", "via", true), node("db", "jewel")], ["observed", "assumed"]));
  assert.deepEqual(chain.map((c) => (c.kind === "node" ? c.node.label : "gap")), ["web-1", "gw", "db"]);
  const first = chain[0] as Extract<(typeof chain)[number], { kind: "node" }>;
  const second = chain[1] as Extract<(typeof chain)[number], { kind: "node" }>;
  assert.equal(first.hop?.label, "Observed");
  assert.equal(second.hop?.weak, true);
  assert.match(second.hop?.caveat ?? "", /assumed, not observed/i);
  assert.equal((chain[2] as { hop: unknown }).hop, null, "the last host has no step after it");
  assert.deepEqual(routeChainView(null), []);
});

test("a long route keeps its entry, its jewel and every fix-list host, and counts the rest", () => {
  const nodes = [node("e", "entry"), ...["a", "b", "c", "d", "e2", "f"].map((l) => node(l, "via", l === "d")), node("j", "jewel")];
  const chain = routeChainView(routeOf(nodes));
  const labels = chain.map((c) => (c.kind === "node" ? c.node.label : `+${c.hidden}`));
  assert.ok(chain.filter((c) => c.kind === "node").length <= 5);
  assert.ok(labels.includes("e") && labels.includes("j") && labels.includes("d"), "entry, jewel and the fix host stay visible");
  const hidden = chain.filter((c) => c.kind === "gap").reduce((n, c) => n + (c.kind === "gap" ? c.hidden : 0), 0);
  assert.equal(hidden, nodes.length - chain.filter((c) => c.kind === "node").length);
  const before = chain[chain.findIndex((c) => c.kind === "gap") - 1] as { hop: unknown };
  assert.equal(before.hop, null, "a step next to hidden hosts is not described by borrowing a neighbour's wording");
});

test("an assumed link inside the hidden hosts is still said", () => {
  const nodes = [node("e", "entry"), node("a", "via"), node("b", "via"), node("c", "via"), node("d", "via"), node("f", "via"), node("j", "jewel")];
  const bases = ["observed", "observed", "observed", "observed", "assumed", "observed"];   // d -> f: both hidden
  const chain = routeChainView(routeOf(nodes, bases));
  const gap = chain.find((c) => c.kind === "gap");
  assert.ok(gap && gap.kind === "gap" && gap.weakHidden === true);
});

test("bars show a bounded share, one per host, and say what each cuts off on its own", () => {
  const bars = focusBars(focusOf({ ranked: [
    { asset_id: "gw", label: "edge-gw-01", share: 0.824, cuts_off: 2, jewels_reachable: 2 },
    { asset_id: "w", label: "web-1", share: 0.12, cuts_off: 0, jewels_reachable: 2 },
    { asset_id: "x", label: "x", share: null, cuts_off: 1, jewels_reachable: null },
  ] }));
  assert.deepEqual(bars.map((b) => [b.value, b.width]), [["82%", 82], ["12%", 12], ["—", 0]]);
  assert.equal(bars[0].sub, "Cuts off 2 of 2 reachable crown jewels on its own.");
  assert.equal(bars[1].sub, "Cuts off 0 of 2 reachable crown jewels on its own.");
  assert.equal(bars[2].sub, "Cuts off 1 crown jewel on its own.");
  assert.ok(bars.every((b) => b.width >= 0 && b.width <= 100));
});

// ── history and trend ────────────────────────────────────────────────────────

const pt = (day: number, reachable: number | null, over: Partial<HistoryPoint> = {}): HistoryPoint => ({
  at: `2026-10-${String(day).padStart(2, "0")}T09:00:00+00:00`, state: "reachable", reachable, exposed: 0,
  assets_seen: 10, coverage: "observed", ...over,
});
const withHistory = (history: HistoryPoint[], change: OverviewRow["change"]) => orow({ history, change });
const chg = (over: Partial<NonNullable<OverviewRow["change"]>> = {}): NonNullable<OverviewRow["change"]> => ({
  since: "2026-10-08T09:00:00+00:00", reachable_from: 2, reachable_to: 3, exposed_from: 0, exposed_to: 0,
  changed: true, inputs_changed: false, ...over,
});

test("dates are short, in UTC, and an unreadable one is said not to be known", () => {
  assert.equal(shortDate("2026-10-09T23:59:00+00:00"), "Oct 9");
  assert.equal(shortDate("2026-01-01T00:00:00Z"), "Jan 1");
  assert.equal(shortDate("nonsense"), "an earlier computation");
  assert.equal(shortDate(null), "an earlier computation");
});

test("fewer than two computations is no trend at all, not 'unchanged'", () => {
  assert.equal(trendView(orow()), null);
  assert.equal(trendView(withHistory([pt(1, 2)], null)), null);
});

test("a change is a difference, with its date and without a verdict", () => {
  const v = trendView(withHistory([pt(7, 2), pt(8, 2), pt(9, 3)], chg()))!;
  assert.deepEqual(v.values, [2, 2, 3]);
  assert.equal(v.change, "Changed since Oct 8: 2 → 3 reachable");
  assert.equal(v.changed, true);
  assert.equal(v.note, null);
  assert.equal(v.twin, "Crown jewels reachable at the last 3 computations, oldest first: 2, 2, 3.");
  assert.doesNotMatch(JSON.stringify(v), /better|worse|improv|deteriorat|risk (up|down)/i);
});

test("unchanged is said only when two computations really agree", () => {
  const v = trendView(withHistory([pt(8, 3), pt(9, 3)], chg({ reachable_from: 3, reachable_to: 3, changed: false })))!;
  assert.equal(v.change, "Unchanged since Oct 8: 3 reachable");
  assert.equal(v.changed, false);
});

test("a newly exposed jewel is part of the sentence", () => {
  const v = trendView(withHistory([pt(8, 2), pt(9, 2, { exposed: 1 })], chg({ reachable_from: 2, reachable_to: 2, exposed_from: 0, exposed_to: 1 })))!;
  assert.equal(v.change, "Changed since Oct 8: 2 → 2 reachable; directly exposed 0 → 1");
});

test("a change that came with different inputs carries that, in words", () => {
  const v = trendView(withHistory([pt(8, 2, { assets_seen: 10 }), pt(9, 3, { assets_seen: 14 })], chg({ inputs_changed: true })))!;
  assert.match(v.note ?? "", /More or fewer hosts were seen, or the coverage differed, so part of this may be what was looked at, not the network\./);
  assert.equal(trendView(withHistory([pt(8, 2), pt(9, 2)], chg({ changed: false, inputs_changed: true, reachable_from: 2 })))!.note, null,
    "no change, nothing to qualify");
});

test("a computation that recorded no per-jewel data is a gap in the twin, never a zero", () => {
  const v = trendView(withHistory([pt(7, 2), pt(8, null, { state: "unrecorded" }), pt(9, 3)], chg()))!;
  assert.deepEqual(v.values, [2, null, 3]);
  assert.match(v.twin, /2, not recorded, 3\./);
  const noCompare = trendView(withHistory([pt(8, null), pt(9, 3)], null))!;
  assert.equal(noCompare.change, null, "when the last two cannot be compared no change is claimed");
});

test("the sparkline starts at zero, draws the latest value as a dot and breaks at a gap", () => {
  const s = sparkline([0, 2, 4], 64, 20, 5);
  assert.equal(s.segments.length, 1);
  const ys = s.segments[0].split(" ").map((p) => Number(p.split(",")[1]));
  assert.ok(ys[0] > ys[1] && ys[1] > ys[2], "higher values are higher up");
  assert.equal(ys[0], 15, "zero sits on the baseline (height - pad)");
  assert.deepEqual(s.last, { x: 59, y: 5 });
  const gap = sparkline([1, 2, null, 3, 4], 64, 20, 5);
  assert.equal(gap.segments.length, 2, "a gap is not bridged by a line");
  assert.deepEqual(sparkline([3, null]).last, null);
  const flat = sparkline([3, 3, 3]);
  assert.equal(new Set(flat.segments[0].split(" ").map((p) => p.split(",")[1])).size, 1);
  assert.equal(sparkline([]).segments.length, 0);
});

test("the first tile counts how many engagements changed, as a count and nothing more", () => {
  const [a] = overviewTiles(summary({ compared: 3, changed: 2 }))!;
  assert.match(a.sub, /4 of 5 crown jewels reachable across them\. 2 of 3 changed since their previous computation\.$/);
  const [none] = overviewTiles(summary())!;
  assert.doesNotMatch(none.sub, /changed/, "no history yet: nothing is said about change");
  const [zero] = overviewTiles(summary({ compared: 2, changed: 0 }))!;
  assert.match(zero.sub, /0 of 2 changed since their previous computation\./);
});

// ── surfacing ────────────────────────────────────────────────────────────────

test("the attention strip says an exposed jewel first, in engagements, marked Beta, and never 'critical'", () => {
  const item = attackPathAttention(summary({ exposed: 2, with_reachable: 5 }))!;
  assert.equal(item.label, "Crown jewel exposed (Beta)");
  assert.equal(item.detail, "2 engagements · remove the exposure first");
  assert.ok(item.label.length <= 30, "the strip truncates a label at about 30 characters");
  assert.equal(item.tone, "high");
  assert.equal(item.href, "/attack-paths");
  assert.doesNotMatch(JSON.stringify(item), /critical/i);
});

test("a reachable crown jewel is a quieter line, and says it is modelled", () => {
  const item = attackPathAttention(summary({ exposed: 0, with_reachable: 1 }))!;
  assert.equal(item.label, "Crown jewel reachable (Beta)");
  assert.equal(item.detail, "1 engagement · modelled, not measured");
  assert.ok(item.label.length <= 30);
  assert.equal(item.tone, "medium");
});

test("when the model has nothing reachable the strip says nothing about it, and nothing is invented without a summary", () => {
  assert.equal(attackPathAttention(summary({ exposed: 0, with_reachable: 0 })), null);
  assert.equal(attackPathAttention(null), null);
  assert.equal(attackPathAttention(undefined), null);
});

test("only rows nobody computed, or whose analysis recorded no per-jewel data, can be computed from a list", () => {
  assert.equal(canCompute(never()), true);
  assert.equal(canCompute(orow({ state: "unrecorded", jewels_total: null })), true);
  for (const state of ["exposed", "reachable", "unreachable", "no_targets"] as const) {
    assert.equal(canCompute(orow({ state })), false, state);
  }
  assert.equal(canCompute({ state: undefined, computed: false, jewels_total: null }), true, "a server that predates `state`");
});

// ── zones ────────────────────────────────────────────────────────────────────

const zone = (key: string, over: Partial<Zone> = {}): Zone => ({
  key, label: key, hosts: 3, stale_hosts: 0, inferred: false, in_scope: true, entry: false, jewel: false, fix: false, routes: 4, ...over,
});
const link = (from: string, to: string, over: Partial<ZoneLink> = {}): ZoneLink => ({ from, to, routes: 2, basis: "assumed", weak: true, ...over });
const view = (zones: Zone[], links: ZoneLink[], over: Partial<ZoneView> = {}): ZoneView => ({
  engagement_id: "e1", computed: true, computed_at: "2026-10-09T09:00:00Z", routes_considered: 6, zones, links, other_zones: 0,
  unplaced_assets: 0, zones_hidden: 0, links_hidden: 0, routes_unplaced: 0, entry_unplaced: 0, jewel_unplaced: 0, ...over,
});

test("roles are words, in reading order, and an inferred subnet says so", () => {
  assert.deepEqual(zoneRoles({ entry: true, jewel: true, fix: true, inferred: true }), ["Entry", "Crown jewel", "Fix here", "Inferred subnet"]);
  assert.deepEqual(zoneRoles({ entry: false, jewel: false, fix: false, inferred: false }), []);
});

test("subnets sit one column after the nearest subnet that leads to them, entries on the left", () => {
  const l = layoutZoneMap(
    [zone("dmz", { entry: true }), zone("app"), zone("db", { jewel: true })],
    [link("dmz", "app"), link("app", "db")],
  );
  const col = Object.fromEntries(l.nodes.map((n) => [n.key, n.col]));
  assert.deepEqual(col, { dmz: 0, app: 1, db: 2 });
  assert.equal(l.width, ZONE.pad * 2 + 2 * (ZONE.boxWidth + ZONE.colGap) + ZONE.boxWidth);
  assert.equal(l.edges.length, 2);
  assert.ok(l.edges.every((e) => !e.backward && e.x2 > e.x1));
});

test("two entries and two jewels fit in two columns without boxes overlapping", () => {
  const l = layoutZoneMap(
    [zone("a", { entry: true }), zone("b", { entry: true }), zone("c", { jewel: true }), zone("d", { jewel: true })],
    [link("a", "c"), link("a", "d"), link("b", "c"), link("b", "d")],
  );
  assert.deepEqual(l.nodes.map((n) => n.col).sort(), [0, 0, 1, 1]);
  const spots = new Set(l.nodes.map((n) => `${n.x},${n.y}`));
  assert.equal(spots.size, 4, "no two boxes share a position");
  for (const a of l.nodes) for (const b of l.nodes) {
    if (a !== b && a.col === b.col) assert.ok(Math.abs(a.y - b.y) >= ZONE.boxHeight, "boxes in one column do not overlap");
  }
});

test("the layout is the same for the same input, whatever the order it arrives in", () => {
  const zs = [zone("x", { entry: true }), zone("y"), zone("z", { jewel: true })];
  const ls = [link("x", "y"), link("y", "z")];
  const a = layoutZoneMap(zs, ls);
  const b = layoutZoneMap([...zs].reverse(), [...ls].reverse());
  const pos = (m: typeof a) => Object.fromEntries(m.nodes.map((n) => [n.key, [n.x, n.y]]));
  assert.deepEqual(pos(a), pos(b));
});

test("a step against the flow, a cycle and a subnet no step leads to are all drawn", () => {
  const l = layoutZoneMap([zone("a", { entry: true }), zone("b"), zone("lonely", { entry: true, jewel: true })], [link("a", "b"), link("b", "a")]);
  assert.equal(l.nodes.length, 3, "nothing disappears");
  assert.equal(l.edges.find((e) => e.key === "b>a")?.backward, true);
  assert.equal(l.nodes.find((n) => n.key === "lonely")?.col, 0);
  assert.equal(layoutZoneMap([zone("only", { entry: true, jewel: true })], []).edges.length, 0);
});

test("links to a subnet that is not drawn, or back to the same one, are dropped rather than crashing the map", () => {
  const l = layoutZoneMap([zone("a", { entry: true })], [link("a", "ghost"), link("a", "a")]);
  assert.equal(l.edges.length, 0);
  assert.deepEqual(layoutZoneMap([], []), { nodes: [], edges: [], width: 0, height: 0 });
});

test("an edge carries its basis in words", () => {
  const l = layoutZoneMap([zone("a", { entry: true }), zone("b", { jewel: true })], [link("a", "b", { basis: "assumed" })]);
  assert.equal(l.edges[0].basisLabel, "Assumed route");
  assert.equal(l.edges[0].weak, true);
});

test("the sentence over the map counts steps and says how many rest on an assumed link", () => {
  const zs = [zone("a", { entry: true }), zone("b", { jewel: true }), zone("c", { jewel: true })];
  assert.equal(zoneSummary(view(zs, [link("a", "b"), link("a", "c")])).lead,
    "The listed routes start in 1 subnet and end in 2 subnets; 2 steps cross between subnets, and all of them rest on assumed links.");
  assert.equal(zoneSummary(view(zs, [link("a", "b", { basis: "observed", weak: false }), link("a", "c")])).lead,
    "The listed routes start in 1 subnet and end in 2 subnets; 2 steps cross between subnets, and 1 of them rests on an assumed link.");
  assert.match(zoneSummary(view(zs, [link("a", "b", { basis: "same_subnet", weak: false })])).lead ?? "", /1 step crosses between subnets, and none of them rests on an assumed link\.$/);
  assert.match(zoneSummary(view([zone("a", { entry: true, jewel: true })], [])).lead ?? "", /no step crosses from one subnet to another\.$/);
  assert.match(zoneSummary(view(zs, [link("a", "b")])).lead ?? "", /1 step crosses between subnets, and it rests on an assumed link\.$/);
});

test("what the map leaves out is said, each in its own sentence", () => {
  const s = zoneSummary(view([zone("a", { entry: true })], [], {
    other_zones: 2, unplaced_assets: 3, zones_hidden: 1, entry_unplaced: 1, jewel_unplaced: 2, routes_truncated: true,
  }));
  assert.equal(s.notes.length, 6);
  assert.match(s.notes.join(" "), /1 listed route starts at a host the analysis did not place in a subnet, so no entry subnet is claimed for it\./);
  assert.match(s.notes.join(" "), /2 listed routes end at a crown jewel the analysis did not place in a subnet\./);
  assert.match(s.notes.join(" "), /2 other subnets have hosts but no listed route touches them\./);
  assert.match(s.notes.join(" "), /3 hosts could not be placed in any subnet and are not drawn\./);
  assert.match(s.notes.join(" "), /1 more subnet is not drawn/);
  assert.match(s.notes.join(" "), /Only the first 500 stored routes were aggregated\./);
});

test("nothing is said for a never-computed engagement, and routes that place no host say that and nothing safer", () => {
  assert.deepEqual(zoneSummary(null), { lead: null, notes: [] });
  assert.deepEqual(zoneSummary(view([], [], { computed: false })), { lead: null, notes: [] });
  const none = zoneSummary(view([], [], { routes_unplaced: 2 }));
  assert.equal(none.lead, null);
  assert.deepEqual(none.notes, ["2 listed routes could not be placed in any subnet, so none is drawn."]);
  assert.deepEqual(zoneSummary(view([], [], { routes_considered: 0 })), { lead: null, notes: [] });
});

// ── P2/P3/P4b/D8 view-model additions ────────────────────────────────────────
import {
  capabilityLabel, suggestedTargetsNote, type TargetSelection,
} from "../lib/attack-paths";

test("techniqueLabel names an NTLM relay", () => {
  assert.equal(techniqueLabel("RELAY"), "NTLM relay");
});

test("capabilityLabel maps control capabilities and ignores unknowns", () => {
  assert.equal(capabilityLabel("foothold"), "Foothold");
  assert.equal(capabilityLabel("lateral"), "Lateral move");
  assert.equal(capabilityLabel("priv_esc"), "Privilege escalation");
  assert.equal(capabilityLabel("recon"), "Reconnaissance");
  assert.equal(capabilityLabel(null), null);
  assert.equal(capabilityLabel("nonsense"), null);
});

test("routeChainView labels a step by its capability, and a relay by its technique", () => {
  const r: FocusRoute = {
    path_id: "p", risk_score: 40, freshness: "fresh",
    nodes: [
      { asset_id: "a", label: "A", role: "entry", on_fix_list: false },
      { asset_id: "b", label: "B", role: "jewel", on_fix_list: false },
    ],
    hops: [{ basis: "assumed", technique: "RELAY", stale: false, exploited: true, capability: null }],
  };
  const chain = routeChainView(r);
  const node = chain.find((c) => c.kind === "node" && c.hop) as Extract<typeof chain[number], { kind: "node" }>;
  assert.equal(node.hop?.step, "NTLM relay");
});

test("suggestedTargetsNote speaks only when targets were suggested", () => {
  const operator: TargetSelection = { basis: "operator", suggested: [] };
  assert.equal(suggestedTargetsNote(operator), null);
  const suggested: TargetSelection = {
    basis: "suggested",
    suggested: [{ asset_id: "dc", label: "DC01", reason: "domain controller" }],
  };
  const note = suggestedTargetsNote(suggested);
  assert.ok(note && note.includes("DC01 (domain controller)"));
  assert.ok(note && note.toLowerCase().includes("no asset was marked critical"));
});
