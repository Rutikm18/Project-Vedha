import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, test } from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { PathMap } from "../app/engagements/[id]/attack-paths/PathMap";
import { ZoneMap } from "../app/engagements/[id]/attack-paths/ZoneMap";
import {
  BetaNotice, CoveragePanel, EmptyExplainer, ExposedCallout, FixFirstPanel, PathDetailPanel, PathTable,
} from "../app/engagements/[id]/attack-paths/Panels";
import type {
  Analysis, ChokeAnalysis, Diagnostics, PathDetail, PathSummary, ZoneView,
} from "../lib/attack-paths";

const html = (el: Parameters<typeof renderToStaticMarkup>[0]) => renderToStaticMarkup(el);

const diagnostics = (reasons: Diagnostics["reasons"]): Diagnostics => ({
  assets: 3, findings: 1, exploitable_findings: 0, entry_points: 0, internet_exposed_assets: 0, targets: 0,
  reachability_edges: 0, control_edges: 0, segments: 1, reachability_posture: "flat", unplaced_assets: 0, reasons,
});

const summary = (id: string, hosts: string[], over: Partial<PathSummary> = {}): PathSummary => ({
  id, risk_score: 61.2, hops: hosts.length - 1,
  source: `asset:${hosts[0]}`, target: `asset:${hosts[hosts.length - 1]}`,
  source_label: hosts[0], target_label: hosts[hosts.length - 1],
  freshness: "fresh", chokepoint_count: 1,
  nodes: hosts.map((h) => ({ asset_id: h, label: h })), ...over,
});

describe("an empty result never reads as safe", () => {
  test("says so, and lists each reason with what to do", () => {
    const out = html(createElement(EmptyExplainer, {
      diagnostics: diagnostics([
        { code: "no_targets", detail: "no crown-jewel target: no asset is marked critical." },
        { code: "no_entry_points", detail: "no asset is internet-exposed" },
      ]),
    }));
    assert.match(out, /No attack paths were modelled/);
    assert.match(out, /not evidence that the network is safe/);
    assert.match(out, /No crown jewels marked/);
    assert.match(out, /Mark the systems that matter most as critical/);
    assert.match(out, /No internet-exposed entry point/);
    assert.doesNotMatch(out, /all clear|no risk|secure/i);
  });

  test("with no reasons it still does not claim safety", () => {
    const out = html(createElement(EmptyExplainer, { diagnostics: null }));
    assert.match(out, /not evidence that the network is safe/);
    assert.match(out, /did not say why/);
  });
});

describe("coverage and freshness", () => {
  const analysis = (over: Record<string, unknown>): Analysis => ({
    computed: true, computed_at: "2026-10-08T10:00:00Z", path_count: 3,
    choke: { ranked: [], min_fix_set: { size: 0, assets: [], independent_routes: {} }, targets: [] },
    coverage: {
      basis: "x", confidence: "partial", segments: [],
      scope_without_observed_hosts: [{ cidr: "10.9.0.0/24", addresses: 256 }],
      observed_outside_scope: [], assets_placed: 4, assets_without_a_subnet: 0, inferred_subnets: 0,
    },
    freshness: {
      window_days: 30, assets: 4, stale_assets: 1, stale_fraction: 0.25, assets_without_timestamp: 0,
      oldest_seen: null, newest_seen: null,
    },
    diagnostics: null, ...over,
  } as Analysis);

  test("partial coverage names the unscanned range and the stale hosts", () => {
    const out = html(createElement(CoveragePanel, { analysis: analysis({}) }));
    assert.match(out, /Coverage: <strong>partial<\/strong>/);
    assert.match(out, /10\.9\.0\.0\/24/);
    assert.match(out, /1 of 4 hosts not seen in the last 30 days/);
  });

  test("observed coverage still says it is not proof of a complete scan", () => {
    const out = html(createElement(CoveragePanel, {
      analysis: analysis({
        coverage: {
          basis: "x", confidence: "observed", segments: [], scope_without_observed_hosts: [],
          observed_outside_scope: [], assets_placed: 4, assets_without_a_subnet: 0, inferred_subnets: 0,
        },
        freshness: {
          window_days: 30, assets: 4, stale_assets: 0, stale_fraction: 0, assets_without_timestamp: 0,
          oldest_seen: null, newest_seen: null,
        },
      }),
    }));
    assert.match(out, /observed/);
    assert.match(out, /not proof the scan was complete/);
    assert.doesNotMatch(out, /\bcomplete coverage\b|fully scanned/i);
  });

  test("an analysis that was never recorded asks for a recompute instead of showing a clean bill", () => {
    const out = html(createElement(CoveragePanel, { analysis: { computed: false } }));
    assert.match(out, /have not been recorded/);
    assert.doesNotMatch(out, /Coverage: /);
  });

  test("while loading it shows a placeholder, not a verdict", () => {
    const out = html(createElement(CoveragePanel, { analysis: undefined }));
    assert.match(out, /aria-busy="true"/);
    assert.doesNotMatch(out, /Coverage: /);
  });
});

describe("fix first", () => {
  const choke: ChokeAnalysis = {
    ranked: [
      { asset_id: "gw", label: "gateway-1", risk_removed: 45, targets_cut_off: ["db"], targets_cut_off_labels: ["db-1"], remediation_priority: "critical" },
      { asset_id: "w", label: "web-1", risk_removed: 5, targets_cut_off: [], targets_cut_off_labels: [], remediation_priority: "medium" },
    ],
    min_fix_set: { size: 1, assets: [{ asset_id: "gw", label: "gateway-1" }], independent_routes: { "db-1": 1 } },
    targets: [{ asset_id: "db", label: "db-1", best_likelihood: 0.5, risk: 50 }],
  };

  test("leads with the decision, then the ranking with words beside every colour", () => {
    const out = html(createElement(FixFirstPanel, { choke }));
    assert.match(out, /Fixing gateway-1 alone cuts every modelled route/);
    assert.match(out, /90%/);                       // 45 of 50 modelled risk
    assert.match(out, /Cuts off db-1/);
    assert.match(out, /Lowers the risk but does not cut a route off/);
    assert.match(out, />critical</);
    assert.match(out, /not a prediction/);
  });

  test("no targets renders nothing rather than a headline about nothing", () => {
    assert.equal(html(createElement(FixFirstPanel, { choke: { ...choke, targets: [] } })), "");
  });
});

describe("routes and steps", () => {
  test("the table is a keyboard-operable list that says which row is selected", () => {
    const out = html(createElement(PathTable, {
      items: [summary("p1", ["web", "db"]), summary("p2", ["vpn", "db"], { freshness: "partly_stale" })],
      selectedId: "p2", onSelect: () => {},
    }));
    assert.equal((out.match(/<button/g) ?? []).length, 2);
    assert.match(out, /aria-pressed="true"/);
    assert.match(out, /aria-label="Show route from vpn to db"/);
    assert.match(out, /Partly stale/);
    assert.match(out, /<caption/);
  });

  const detail: PathDetail = {
    id: "p1", risk_score: 61.2, freshness: "partly_stale", node_count: 3, nodes: ["web-1", "app-1", "db-1"],
    chokepoints: ["app-1"],
    hops: [
      { from: "web-1", to: "app-1", technique: "CROSS_SUBNET", weight: 1, exploited: true, cvss: 9.8, via: ["10.0.1.0/24", "10.0.2.0/24"],
        basis: "assumed", likelihood: 0.5, stale: false, explanation: "From web-1, the attacker crosses to app-1. Reachability is assumed." },
      { from: "app-1", to: "db-1", technique: "SAME_SUBNET", weight: 1, exploited: false, cvss: null, via: [],
        basis: "same_subnet", likelihood: null, stale: true, explanation: "From app-1, the attacker moves within the subnet to db-1." },
    ],
  };

  test("each step states how it is known, how likely, and what it relies on", () => {
    const out = html(createElement(PathDetailPanel, { detail }));
    assert.match(out, /Assumed route/);
    assert.match(out, /Across subnets/);
    assert.match(out, /Likelihood 50%/);
    assert.match(out, /Likelihood —/);               // no estimate renders a dash, never 0%
    assert.match(out, /Exploits a finding · CVSS 9\.8/);
    assert.match(out, /Not seen recently/);
    assert.match(out, /Reachability is assumed/);
    assert.match(out, /10\.0\.1\.0\/24 → 10\.0\.2\.0\/24/);
    assert.match(out, /On this route and in the fix-first list/);
    assert.match(out, /data-step="1"/);
  });

  test("the map names every role in text and exposes an accessible summary", () => {
    const out = html(createElement(PathMap, {
      items: [summary("p1", ["web", "gw", "db"]), summary("p2", ["vpn", "gw", "db"])],
      chokeIds: new Set(["gw"]), selectedId: "p1",
    }));
    assert.match(out, /role="img"/);
    assert.match(out, /Route map: 2 routes across 4 hosts/);
    assert.match(out, />ENTRY</);
    assert.match(out, />CROWN JEWEL</);
    assert.match(out, />FIX HERE</);
    assert.match(out, /data-dim="true"/);            // the route not selected recedes
  });

  test("an empty list draws no map at all", () => {
    assert.equal(html(createElement(PathMap, { items: [], chokeIds: new Set<string>(), selectedId: null })), "");
  });
});

describe("the page is wired to the backend, not to demo data", () => {
  const read = (p: string) => readFileSync(join(process.cwd(), p), "utf8");

  test("the demo graph store is gone and nothing imports it", () => {
    assert.equal(existsSync(join(process.cwd(), "lib/graph-store.ts")), false);
    for (const f of [
      "app/api/engagements/[id]/attack-paths/route.ts",
      "app/api/engagements/[id]/attack-paths/[pathId]/route.ts",
      "app/api/engagements/[id]/chokepoints/route.ts",
      "app/api/engagements/[id]/attack-graph/route.ts",
      "app/api/engagements/[id]/blast-radius/[assetId]/route.ts",
      "app/api/engagements/[id]/attack-path-analysis/route.ts",
    ]) {
      const src = read(f);
      assert.doesNotMatch(src, /graph-store|graphStore/, f);
      assert.match(src, /engagementGet/, f);
    }
  });

  test("the workspace reads stored data and offers an explicit recompute", () => {
    const src = read("app/engagements/[id]/attack-paths/AttackPathsWorkspace.tsx");
    assert.match(src, /attackPathsApi\.list/);
    assert.match(src, /attackPathsApi\.analysis/);
    assert.match(src, /attackPathsApi\.detail/);
    assert.match(src, /refresh: true/);
    assert.match(src, /Recompute paths/);
  });

  test("a failed analysis is shown as a failure, never as an empty caveat list", () => {
    const src = read("app/engagements/[id]/attack-paths/AttackPathsWorkspace.tsx");
    assert.match(src, /analysis\.isError/);
    assert.match(src, /Couldn't load coverage/);
  });

  test("the engagement page links to it for operators only", () => {
    const src = read("app/engagements/[id]/workspace.tsx");
    assert.match(src, /surface === "manager" && \(\s*<Link href=\{`\/engagements\/\$\{encodeURIComponent\(id\)\}\/attack-paths`\}/);
  });
});

describe("attack paths is labelled Beta", () => {
  const read = (p: string) => readFileSync(join(process.cwd(), p), "utf8");

  test("the notice says it is beta and what that means, not a generic disclaimer", () => {
    const out = html(createElement(BetaNotice));
    assert.match(out, />Beta</);
    assert.match(out, /Attack paths is in beta/);
    assert.match(out, /already marked exploitable/);
    assert.match(out, /without being safe/);
    assert.match(out, /assets you mark critical/);
  });

  test("the page header and the engagement toolbar link both carry the Beta badge", () => {
    const page = read("app/engagements/[id]/attack-paths/AttackPathsWorkspace.tsx");
    assert.match(page, /headerActions=\{<span className="badge badge-info"[^>]*>Beta<\/span>\}/);
    assert.match(page, /<BetaNotice \/>/);
    const toolbar = read("app/engagements/[id]/workspace.tsx");
    assert.match(toolbar, /Attack paths <span className="badge badge-info">Beta<\/span>/);
  });
});

describe("a crown jewel exposed outright is not an empty result", () => {
  test("the callout says it is exposed, that no route is needed, and that this is not 'safe'", () => {
    const out = html(createElement(ExposedCallout, { targets: [{ asset_id: "j", label: "fin-db-01" }] }));
    assert.match(out, /data-tone="critical"/);
    assert.match(out, /fin-db-01 is exposed to the internet/);
    assert.match(out, /No route is needed/);
    assert.match(out, /Fixing other hosts does not protect it; remove that exposure first\./);
    assert.match(out, /That is why there are no routes to list\. It is not evidence that the network is safe\./);
    assert.doesNotMatch(out, /did not have what it needs/);
  });

  test("several exposed jewels are counted and the sentence agrees in number", () => {
    const out = html(createElement(ExposedCallout, { targets: [{ asset_id: "a", label: "a" }, { asset_id: "b", label: "b" }] }));
    assert.match(out, /2 crown jewels are exposed to the internet/);
    assert.match(out, /does not protect them/);
  });

  test("the page shows it instead of the 'nothing modelled' explainer, and does not call the count exposure", () => {
    const src = readFileSync(join(process.cwd(), "app/engagements/[id]/attack-paths/AttackPathsWorkspace.tsx"), "utf8");
    assert.match(src, /exposed\.length > 0 \? <ExposedCallout targets=\{exposed\} \/> : <EmptyExplainer/);
    assert.match(src, /crown jewel\$\{exposed\.length === 1 \? "" : "s"\} directly exposed/);
    assert.match(src, /At most 5 routes are listed per entry point per\s+crown jewel/);
  });
});

describe("the subnet map", () => {
  const view = (over: Partial<ZoneView> = {}): ZoneView => ({
    engagement_id: "e", computed: true, computed_at: "2026-10-09T09:00:00Z", routes_considered: 6, other_zones: 1, unplaced_assets: 0,
    zones_hidden: 0, links_hidden: 0, routes_unplaced: 0, entry_unplaced: 0, jewel_unplaced: 0,
    zones: [
      { key: "10.1.0.0/24", label: "10.1.0.0/24", hosts: 2, stale_hosts: 1, inferred: false, in_scope: true, entry: true, jewel: false, fix: true, routes: 4 },
      { key: "10.3.0.0/24", label: "10.3.0.0/24 @ HQ", hosts: 1, stale_hosts: 0, inferred: false, in_scope: true, entry: false, jewel: true, fix: false, routes: 3 },
    ],
    links: [{ from: "10.1.0.0/24", to: "10.3.0.0/24", routes: 4, basis: "assumed", weak: true }], ...over,
  });

  test("a subnet is a box with its range, hosts and roles in words; an assumed step is dashed and says so", () => {
    const out = html(createElement(ZoneMap, { view: view() }));
    assert.match(out, /role="img" aria-label="Subnet map: 2 subnets and 1 step between them\./);
    assert.match(out, />10\.1\.0\.0\/24</);
    assert.match(out, />2 hosts · 1 not seen recently</);
    assert.match(out, />ENTRY · FIX HERE</);
    assert.match(out, />CROWN JEWEL</);
    assert.match(out, /data-weak="true"/);
    assert.doesNotMatch(out, /ap-zone-pill/, "no labels on the arrows: crossing steps share a midpoint and would sit on each other");
    assert.match(out, /Step on an assumed link/);
    assert.match(out, /Thicker line = more listed routes/);
    assert.match(out, /10\.3\.0\.0\/24 @ HQ/);
  });

  test("the same information is in two tables a keyboard and a screen reader can read", () => {
    const out = html(createElement(ZoneMap, { view: view() }));
    assert.match(out, /aria-label="Subnets \(table\)" tabindex="0"/);
    assert.match(out, /aria-label="Steps between subnets \(table\)" tabindex="0"/);
    assert.match(out, /<th scope="col">Hosts seen<\/th>/);
    assert.match(out, /Entry, Fix here/);
    assert.match(out, /<span class="ap-chip" data-tone="weak">Assumed route<\/span>/);
  });

  test("hosts not recorded are said to be, never shown as 0; a subnet with no role is 'on a route'", () => {
    const out = html(createElement(ZoneMap, { view: view({ zones: [
      { key: "x", label: "x", hosts: null, stale_hosts: null, inferred: false, in_scope: true, entry: false, jewel: false, fix: false, routes: 1 },
    ], links: [] }) }));
    assert.match(out, />hosts not recorded</);
    assert.match(out, />ON A ROUTE</);
    assert.doesNotMatch(out, />0 hosts</);
  });

  test("names are escaped, and nothing is drawn when there are no subnets", () => {
    const out = html(createElement(ZoneMap, { view: view({ zones: [
      { key: "k", label: "<script>alert(1)</script>", hosts: 1, stale_hosts: 0, inferred: true, in_scope: true, entry: true, jewel: true, fix: false, routes: 1 },
    ], links: [] }) }));
    assert.doesNotMatch(out, /<script>alert/);
    assert.match(out, /&lt;script&gt;/);
    assert.match(out, /INFERRED SUBNET/);
    assert.equal(html(createElement(ZoneMap, { view: view({ zones: [], links: [] }) })), "");
  });

  test("the page reads it after the list, never before it, and a failure does not touch the routes", () => {
    const src = readFileSync(join(process.cwd(), "app/engagements/[id]/attack-paths/AttackPathsWorkspace.tsx"), "utf8");
    assert.match(src, /queryKey: \["attack-path-zones", engagementId\],\s*queryFn: \(\) => attackPathsApi\.zones\(engagementId\),\s*enabled: list\.isSuccess,/);
    assert.match(src, /The subnet map could not be loaded\. The routes below are unaffected\./);
    assert.match(src, /A step marked assumed has not been observed\./);
  });
});
