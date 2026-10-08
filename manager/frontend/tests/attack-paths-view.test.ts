import assert from "node:assert/strict";
import test from "node:test";
import {
  basisInfo, caveatSummary, emptyReasons, fixFirstSummary, fixPointIds, freshnessInfo, layoutPathMap, MAP,
  percent, riskLabel, riskShare, techniqueLabel, truncateLabel,
  type ChokeAnalysis, type Coverage, type Diagnostics, type FreshnessReport, type PathSummary,
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
