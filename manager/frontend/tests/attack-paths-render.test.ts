import assert from "node:assert/strict";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, test } from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { PathMap } from "../app/engagements/[id]/attack-paths/PathMap";
import {
  CoveragePanel, EmptyExplainer, FixFirstPanel, PathDetailPanel, PathTable,
} from "../app/engagements/[id]/attack-paths/Panels";
import type {
  Analysis, ChokeAnalysis, Diagnostics, PathDetail, PathSummary,
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
    const src = read("app/engagements/[id]/workspace.tsx");       // page.tsx re-exports it
    assert.match(src, /surface === "manager" && \(\s*<Link href=\{`\/engagements\/\$\{encodeURIComponent\(id\)\}\/attack-paths`\}/);
  });
});
