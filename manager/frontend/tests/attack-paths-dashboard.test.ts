import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, test } from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { NextRequest } from "next/server";

import { GET as focusGet } from "../app/api/attack-paths/focus/[id]/route";
import { GET as overviewGet } from "../app/api/attack-paths/overview/route";
import { AttackPathsTiles } from "../components/attack-paths/AttackPathsTiles";
import { FixFirstCard } from "../components/attack-paths/FixFirstCard";
import { OverviewFootnote, OverviewList } from "../components/attack-paths/OverviewList";
import { OVERVIEW_STYLES } from "../components/attack-paths/overview-styles";
import {
  OperatorConsoleProvider, PortalConsoleProvider, useConsoleCapability, useConsoleSource,
} from "../lib/console-source";
import type { Focus, OverviewRow, OverviewSummary } from "../lib/attack-paths";

const read = (p: string) => readFileSync(join(process.cwd(), p), "utf8");
const html = (el: Parameters<typeof renderToStaticMarkup>[0]) => renderToStaticMarkup(el);

const ID = "11111111-1111-4111-8111-111111111111";

const row = (over: Partial<OverviewRow> = {}): OverviewRow => ({
  engagement_id: ID, name: "Acme network assessment", status: "active", state: "reachable",
  computed: true, computed_at: "2026-10-09T09:00:00Z", path_count: 8, entry_points: 8, crown_jewels: 3,
  jewels_total: 3, jewels_reachable: 2, jewels_exposed: 0, ways_in: 1, top_risk: 40,
  fix_set_size: 1, fix_assets: ["edge-gw-01"], fix_assets_more: 0, coverage: "partial", stale_assets: 1,
  why_empty: [], ...over,
});

describe("overview rows", () => {
  test("each row links to that engagement's Attack paths page and says what it found, in words", () => {
    const out = html(createElement(OverviewList, { rows: [row()] }));
    assert.match(out, /href="\/engagements\/11111111-1111-4111-8111-111111111111\/attack-paths"/);
    assert.match(out, /Acme network assessment/);
    assert.match(out, />2 of 3 crown jewels reachable</);
    assert.match(out, /<span class="apo-ways">1 separate way in<\/span>/);
    assert.match(out, /Fixing edge-gw-01 alone cuts every route\./);
    assert.match(out, /Coverage partial/);
    assert.match(out, /1 host not seen recently/);
    assert.match(out, /aria-label="Acme network assessment: 2 of 3 crown jewels reachable, 1 separate way in\. Fixing edge-gw-01 alone cuts every route\."/);
    assert.doesNotMatch(out, /8 routes/, "the capped route count is not a headline");
  });

  test("the meter has a diamond per crown jewel and is hidden from assistive technology", () => {
    const out = html(createElement(OverviewList, { rows: [row()] }));
    assert.match(out, /<span class="apx-meter" aria-hidden="true">/);
    assert.equal((out.match(/<svg width="14"/g) ?? []).length, 3);
  });

  test("a crown jewel exposed outright is its own state, in the critical rail, with no fix-the-gateway", () => {
    const out = html(createElement(OverviewList, { rows: [row({
      state: "exposed", jewels_total: 1, jewels_reachable: 1, jewels_exposed: 1, ways_in: null, path_count: 0,
    })] }));
    assert.match(out, />1 crown jewel directly exposed to the internet</);
    assert.match(out, /Remove the exposure first\./);
    assert.match(out, /--rail:var\(--sev-critical-color\)/);
    assert.doesNotMatch(out, /alone cuts every route|No routes modelled|separate way/);
  });

  test("an engagement nobody computed reads 'not computed yet', never '0 routes' or '0 of'", () => {
    const out = html(createElement(OverviewList, {
      rows: [row({ state: "not_computed", computed: false, path_count: null, fix_set_size: null, fix_assets: [],
        coverage: null, stale_assets: null, computed_at: null, jewels_total: null, jewels_reachable: null, jewels_exposed: null, ways_in: null })],
    }));
    assert.match(out, /Not computed yet/);
    assert.doesNotMatch(out, /0 routes|0 of|No routes modelled|Coverage/);
  });

  test("nothing reachable carries its reason and never claims safety; no crown jewel marked says so", () => {
    const none = html(createElement(OverviewList, {
      rows: [row({ state: "unreachable", jewels_reachable: 0, ways_in: null, fix_set_size: 0, fix_assets: [], path_count: 0,
        coverage: "observed", stale_assets: 0, why_empty: [{ code: "no_entry_points", detail: "x" }] })],
    }));
    assert.match(none, /No modelled route reaches a crown jewel/);
    assert.match(none, /This is not evidence the network is safe\./);
    const unmarked = html(createElement(OverviewList, {
      rows: [row({ state: "no_targets", jewels_total: 0, jewels_reachable: 0, ways_in: null, path_count: 0 })],
    }));
    assert.match(unmarked, />No crown jewels marked</);
    assert.doesNotMatch(none + unmarked, /all clear|you are safe|no risk/i);
  });

  test("a row with history draws a sparkline whose name is the numbers, and states the change", () => {
    const pt = (day: number, reachable: number) => ({ at: `2026-10-0${day}T09:00:00+00:00`, state: "reachable" as const, reachable,
      exposed: 0, assets_seen: 10, coverage: "observed" as const });
    const out = html(createElement(OverviewList, { rows: [row({
      history: [pt(7, 2), pt(8, 2), pt(9, 3)],
      change: { since: "2026-10-08T09:00:00+00:00", reachable_from: 2, reachable_to: 3, exposed_from: 0, exposed_to: 0, changed: true, inputs_changed: true },
    })] }));
    assert.match(out, /<svg class="apx-spark"[^>]*role="img" aria-label="Crown jewels reachable at the last 3 computations, oldest first: 2, 2, 3\."/);
    assert.match(out, /Changed since Oct 8: 2 → 3 reachable/);
    assert.match(out, /Inputs changed too/);
    assert.doesNotMatch(out, /better|worse|improved|deteriorated/i);
  });

  test("a row with one computation (or none) has no sparkline and does not claim 'no change'", () => {
    const one = html(createElement(OverviewList, { rows: [row({ history: [{ at: "2026-10-09T09:00:00+00:00", state: "reachable", reachable: 2,
      exposed: 0, assets_seen: 10, coverage: "observed" }], change: null })] }));
    const none = html(createElement(OverviewList, { rows: [row()] }));
    for (const out of [one, none]) {
      assert.doesNotMatch(out, /apx-spark|Unchanged|Changed since|no change/i);
    }
  });

  test("the footnote says what each kind of 'nothing' means", () => {
    const out = html(createElement(OverviewFootnote));
    assert.match(out, /is not evidence the network is safe/);
    assert.match(out, /can&#x27;t be assessed|can&apos;t be assessed/);
    assert.match(out, /no asset is marked critical/);
    assert.match(out, /A change between two computations is a difference, not a\s+verdict/);
  });

  test("special characters in an engagement name are escaped, not rendered as markup", () => {
    const out = html(createElement(OverviewList, { rows: [row({ name: "<img src=x onerror=alert(1)>" })] }));
    assert.doesNotMatch(out, /<img src=x/);
    assert.match(out, /&lt;img src=x onerror=alert\(1\)&gt;/);
  });
});

const summary = (over: Partial<OverviewSummary> = {}): OverviewSummary => ({
  engagements: 5, computed: 4, assessed: 3, with_reachable: 2, exposed: 0, single_fix: 1,
  not_computed: 1, no_targets: 1, unrecorded: 0, jewels_total: 5, jewels_reachable: 4, ...over,
});

describe("Compute from a list", () => {
  const uncomputed = () => row({
    engagement_id: "22222222-2222-4222-8222-222222222222", name: "Umbrella lab", state: "not_computed", computed: false,
    computed_at: null, path_count: null, fix_set_size: null, fix_assets: [], coverage: null, stale_assets: null,
    jewels_total: null, jewels_reachable: null, jewels_exposed: null, ways_in: null,
  });
  const noop = { run: () => undefined, pendingId: null };

  test("an uncomputed row gets a Compute button beside its link, never inside it", () => {
    const out = html(createElement(OverviewList, { rows: [uncomputed()], compute: noop }));
    assert.match(out, /<\/a><button type="button" class="btn btn-secondary apo-compute focusable"/);
    assert.match(out, /aria-label="Compute attack paths for Umbrella lab"/);
    assert.match(out, /Compute<\/button>/);
    const link = out.slice(out.indexOf("<a "), out.indexOf("</a>"));
    assert.doesNotMatch(link, /<button/, "an interactive control inside a link is invalid and unreachable by keyboard");
  });

  test("rows that already have a reading, and lists with no compute handler, get no button", () => {
    const computed = html(createElement(OverviewList, { rows: [row(), row({ state: "unreachable", jewels_reachable: 0 }), row({ state: "no_targets", jewels_total: 0 })], compute: noop }));
    assert.doesNotMatch(computed, /apo-compute/);
    assert.doesNotMatch(html(createElement(OverviewList, { rows: [uncomputed()] })), /apo-compute/);
  });

  test("while one engagement computes, its button says so and every button is disabled", () => {
    const out = html(createElement(OverviewList, { rows: [uncomputed()], compute: { run: () => undefined, pendingId: "22222222-2222-4222-8222-222222222222" } }));
    assert.match(out, /aria-label="Computing attack paths for Umbrella lab"/);
    assert.match(out, /disabled=""/);
    assert.match(out, /Computing…/);
  });

  test("the action is the existing explicit recompute, run on a click and nowhere else", () => {
    const hook = read("components/attack-paths/useComputeAttackPaths.ts").replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "");
    assert.match(hook, /attackPathsApi\.list\(row\.engagement_id, \{ refresh: true, pageSize: 1 \}\)/);
    assert.match(hook, /useMutation/);
    assert.doesNotMatch(hook, /useQuery\(|useEffect|setInterval/, "nothing computes on load or on a timer");
    assert.match(hook, /onError: \(e, row\) => toast\.error/);
    for (const key of ['q.queryKey[2] === "attackPaths"', '"attack-paths-overview"', '"attack-paths-focus"']) {
      assert.ok(hook.includes(key), `refreshes ${key}`);
    }
  });

  test("both lists pass the handler in", () => {
    assert.match(read("components/dashboard/AttackPathsPanel.tsx"), /<OverviewList rows=\{shown\} compute=\{compute\} \/>/);
    assert.match(read("app/attack-paths/page.tsx"), /<OverviewList rows=\{rows\} compute=\{compute\} \/>/);
  });
});

describe("the Needs attention strip", () => {
  const grid = read("components/dashboard/DashboardGrid.tsx");

  test("reads the attack-paths dataset only where the capability exists, and adds no request of its own", () => {
    assert.match(grid, /const canSeeAttackPaths = useConsoleCapability\("viewAttackPaths"\)/);
    assert.match(grid, /useConsoleQuery<Overview>\("attackPaths", \{ refetchInterval: 120_000, enabled: canSeeAttackPaths \}\)/);
    assert.match(grid, /canSeeAttackPaths \? attackPathAttention\(attackPaths\.data\?\.summary\) : null/);
  });

  test("its item comes last, and an outage of it is not counted as an unavailable urgent signal", () => {
    const items = grid.slice(grid.indexOf("const items = ["), grid.indexOf("if (loading && items.length === 0)"));
    assert.ok(items.indexOf("critical > 0") < items.indexOf("breached > 0") && items.indexOf("offline > 0") < items.indexOf("attackPathItem ?"));
    assert.match(grid, /const failed = \[findings\.error, sla\.error, agents\.error\]\.filter\(Boolean\)\.length;/);
    assert.match(grid, /Items marked Beta are modelled, not measured\./);
  });
});

describe("the triage tiles", () => {
  test("three tiles of engagement counts, each with what it is counted out of", () => {
    const out = html(createElement(AttackPathsTiles, { summary: summary() }));
    assert.match(out, /role="group" aria-label="Attack paths summary"/);
    assert.match(out, /Engagements with a reachable crown jewel/);
    assert.match(out, /<span>2<\/span><small>of 3 assessed<\/small>/);
    assert.match(out, /4 of 5 crown jewels reachable across them\./);
    assert.match(out, /<span>1<\/span><small>of 2<\/small>/);
    assert.match(out, /Can&#x27;t be assessed yet|Can&apos;t be assessed yet/);
    assert.match(out, /1 not computed · 1 with no crown jewel marked\./);
  });

  test("an exposed jewel is a critical tile, in words", () => {
    const out = html(createElement(AttackPathsTiles, { summary: summary({ exposed: 1 }) }));
    assert.match(out, /data-tone="critical"/);
    assert.match(out, /1 with a crown jewel directly exposed to the internet\./);
  });

  test("no summary renders nothing rather than zeros", () => {
    assert.equal(html(createElement(AttackPathsTiles, { summary: null })), "");
  });
});

describe("the fix-first card", () => {
  const focus = (over: Partial<Focus> = {}): Focus => ({
    engagement_id: ID, name: "Acme network assessment", state: "reachable", computed: true,
    computed_at: "2026-10-09T09:00:00Z", path_count: 8, exposed: [],
    fix: { size: 1, assets: [{ asset_id: "gw", label: "edge-gw-01" }], independent_routes: { "fin-db-01": 1 } },
    route: {
      path_id: "p1", risk_score: 12.15, freshness: "fresh",
      nodes: [
        { asset_id: "w", label: "web-dmz-03", role: "entry", on_fix_list: false },
        { asset_id: "gw", label: "edge-gw-01", role: "via", on_fix_list: true },
        { asset_id: "db", label: "fin-db-01", role: "jewel", on_fix_list: false },
      ],
      hops: [
        { basis: "observed", technique: null, stale: false, exploited: true },
        { basis: "assumed", technique: null, stale: false, exploited: null },
      ],
    },
    ranked: [{ asset_id: "gw", label: "edge-gw-01", share: 0.824, cuts_off: 2, jewels_reachable: 2 }], ...over,
  });

  const card = (f: Focus | undefined, r: OverviewRow = row()) => {
    const client = new QueryClient();
    if (f) client.setQueryData(["attack-paths-focus", r.engagement_id, r.computed_at], f);
    return html(createElement(QueryClientProvider, { client }, createElement(FixFirstCard, { row: r })));
  };

  test("the route is an ordered list with a word and a shape for every role, and the caveat in words", () => {
    const out = card(focus());
    assert.match(out, /<ol class="apx-chain" aria-label="Highest-risk route">/);
    assert.match(out, />Entry point</);
    assert.match(out, />Host on the route · on the fix list</);
    assert.match(out, />Crown jewel</);
    assert.match(out, /web-dmz-03[\s\S]*Observed[\s\S]*edge-gw-01[\s\S]*Assumed route — Reachability between these subnets is assumed, not observed/);
    assert.match(out, /Fixing edge-gw-01 alone cuts every modelled route to a crown jewel\./);
  });

  test("bars are a share of modelled risk, never added up, and say so", () => {
    const out = card(focus());
    assert.match(out, /Share of modelled risk removed/);
    assert.match(out, />82%</);
    assert.match(out, /width:82%/);
    assert.match(out, /Cuts off 2 of 2 reachable crown jewels on its own\./);
    assert.match(out, /so the bars do not add up/);
    assert.match(out, /not a probability/);
  });

  test("when no host of the route is on the fix list it says so instead of tagging one", () => {
    const f = focus();
    f.route!.nodes.forEach((n) => { n.on_fix_list = false; });
    assert.match(card(f), /None of this route&#x27;s hosts is on the fix list|None of this route&apos;s hosts is on the fix list/);
  });

  test("an exposed jewel is named and told to remove its exposure; no route is invented", () => {
    const f = focus({ state: "exposed", route: null, ranked: [], exposed: [{ asset_id: "j", label: "fin-db-01" }],
      fix: { size: 0, assets: [], independent_routes: {} }, path_count: 0 });
    const out = card(f, row({ state: "exposed" }));
    assert.match(out, /fin-db-01 is exposed to the internet and can be exploited directly/);
    assert.match(out, /Crown jewel · directly exposed/);
    assert.doesNotMatch(out, /Highest-risk route|alone cuts|Share of modelled risk/);
  });

  test("with no host that fixes it alone the card says the fixes go together", () => {
    const out = card(focus({ ranked: [], fix: { size: 2, assets: [{ asset_id: "a", label: "gw1" }, { asset_id: "b", label: "gw2" }], independent_routes: {} } }));
    assert.match(out, /No single host removes any modelled risk on its own/);
  });

  test("until the data arrives it is a busy placeholder, and it always links to the engagement", () => {
    const out = card(undefined);
    assert.match(out, /aria-busy="true"/);
    assert.match(out, /href="\/engagements\/11111111-1111-4111-8111-111111111111\/attack-paths"/);
  });

  test("it asks only for stored results: one GET to the read-only focus route, nothing else", () => {
    const src = read("components/attack-paths/FixFirstCard.tsx").replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "");
    assert.match(src, /\/api\/attack-paths\/focus\//);
    assert.doesNotMatch(src, /method:\s*["'](POST|PUT|PATCH|DELETE)|refresh=true|recompute/i);
  });
});

describe("the dashboard section is operator-only", () => {
  function Probe() {
    const source = useConsoleSource();
    const can = useConsoleCapability("viewAttackPaths");
    return createElement("p", null, `mode=${source.mode};can=${can};endpoint=${source.endpoints.attackPaths}`);
  }

  test("the operator console has the dataset and the capability", () => {
    const out = html(createElement(OperatorConsoleProvider, null, createElement(Probe)));
    assert.match(out, /mode=operator;can=true;endpoint=\/api\/attack-paths\/overview\?limit=5/);
  });

  test("the customer console has neither, so nothing is fetched and no section renders", () => {
    const out = html(createElement(PortalConsoleProvider, null, createElement(Probe)));
    assert.match(out, /mode=portal;can=false;endpoint=null/);
  });

  test("the dashboard only renders the panel behind that capability", () => {
    const grid = read("components/dashboard/DashboardGrid.tsx");
    assert.match(grid, /useConsoleCapability\("viewAttackPaths"\)/);
    assert.match(grid, /showAttackPaths && \(\s*<div className="console-band band-4">/);
    assert.match(grid, /title="Attack paths"/);
    assert.match(grid, /className="badge badge-info"[^>]*>Beta<\/span>/);
  });

  test("the card is drawn only for an exposed or reachable top row; the ladder never waits for it", () => {
    const panel = read("components/dashboard/AttackPathsPanel.tsx");
    assert.match(panel, /\["exposed", "reachable"\]\.includes\(overviewState\(top\)\)/);
    assert.match(panel, /<OverviewList rows=\{shown\} compute=\{compute\} \/>\s*\{focusRow && <FixFirstCard row=\{focusRow\} \/>\}/);
  });
});

describe("layout and type", () => {
  test("layout follows the panel's own width (container queries), not the viewport", () => {
    assert.match(OVERVIEW_STYLES, /@container apxp \(min-width: 760px\)/);
    assert.match(OVERVIEW_STYLES, /@container apx \(max-width: 560px\)/);
    assert.doesNotMatch(OVERVIEW_STYLES, /@media[^{]*(min|max)-width/, "no viewport breakpoints; only the motion preference may use @media");
  });

  test("sizes come from the type scale and meaning-carrying marks are not drawn with border tokens", () => {
    assert.doesNotMatch(OVERVIEW_STYLES, /font-size:\s*\d+(\.\d+)?px/);
    assert.match(OVERVIEW_STYLES, /\.apx-chain > li::before \{[^}]*background: var\(--text-muted\)/);
    assert.doesNotMatch(OVERVIEW_STYLES, /(stroke|background): var\(--border/);
  });
});

describe("navigation", () => {
  test("operators get an Attack paths entry marked BETA; the customer menu does not", () => {
    const sidebar = read("components/Sidebar.tsx");
    const operator = sidebar.slice(sidebar.indexOf("const NAV_SECTIONS"), sidebar.indexOf("const PORTAL_NAV_SECTIONS"));
    const portal = sidebar.slice(sidebar.indexOf("const PORTAL_NAV_SECTIONS"));
    assert.match(operator, /label: "Attack paths", href: "\/attack-paths", badge: "BETA"/);
    assert.doesNotMatch(portal.slice(0, portal.indexOf("];") + 2), /attack-paths|Attack paths/);
  });

  test("the /attack-paths page reads the overview, shows the tiles and says it is beta", () => {
    const page = read("app/attack-paths/page.tsx");
    assert.match(page, /\/api\/attack-paths\/overview\?limit=200/);
    assert.match(page, /<AttackPathsTiles summary=\{query\.data\?\.summary\} \/>/);
    assert.match(page, /<AttackPathStyles \/>/);
    assert.match(page, /badge badge-info/);
    assert.match(page, /<BetaNotice \/>/);
  });
});

describe("BFF /api/attack-paths/overview", () => {
  const original = globalThis.fetch;
  afterEach(() => { globalThis.fetch = original; });
  const req = (qs = "", token: string | null = "operator-token") =>
    new NextRequest(`http://localhost/api/attack-paths/overview${qs}`, token ? { headers: { authorization: `Bearer ${token}` } } : {});

  test("forwards to the stored-results endpoint with the operator token and only a valid limit", async () => {
    let url = "", auth = "";
    globalThis.fetch = async (input, init) => {
      url = String(input); auth = new Headers(init?.headers).get("authorization") ?? "";
      return new Response(JSON.stringify({ total: 0, shown: 0, engagements: [] }), { status: 200, headers: { "content-type": "application/json" } });
    };
    const res = await overviewGet(req("?limit=50&evil=1"));
    assert.equal(res.status, 200);
    assert.deepEqual(await res.json(), { total: 0, shown: 0, engagements: [] });
    const u = new URL(url);
    assert.equal(u.pathname, "/attack-paths/overview");
    assert.equal(u.searchParams.get("limit"), "50");
    assert.equal(u.searchParams.get("evil"), null);
    assert.equal(auth, "Bearer operator-token");
  });

  test("a bad limit is refused before any backend call; no token means no call", async () => {
    let calls = 0;
    globalThis.fetch = async () => { calls += 1; return new Response("{}", { status: 200 }); };
    for (const q of ["?limit=0", "?limit=201", "?limit=abc", "?limit=-1"]) {
      assert.equal((await overviewGet(req(q))).status, 400, q);
    }
    assert.equal((await overviewGet(req("", null))).status, 401);
    assert.equal(calls, 0);
  });

  test("a backend refusal and an outage stay errors, never an empty overview", async () => {
    globalThis.fetch = async () => new Response(JSON.stringify({ detail: "Role 'client' is not permitted." }), { status: 403 });
    const denied = await overviewGet(req());
    assert.equal(denied.status, 403);
    assert.match((await denied.json()).error, /not permitted/);
    globalThis.fetch = async () => { throw new TypeError("fetch failed"); };
    assert.ok((await overviewGet(req())).status >= 500);
  });
});

describe("BFF /api/attack-paths/focus/{id}", () => {
  const original = globalThis.fetch;
  afterEach(() => { globalThis.fetch = original; });
  const call = (id: string, token: string | null = "operator-token", qs = "") =>
    focusGet(new NextRequest(`http://localhost/api/attack-paths/focus/${id}${qs}`, token ? { headers: { authorization: `Bearer ${token}` } } : {}),
      { params: Promise.resolve({ id }) });

  test("forwards a valid engagement id to the read-only focus endpoint and nothing the browser added", async () => {
    let url = "", auth = "";
    globalThis.fetch = async (input, init) => {
      url = String(input); auth = new Headers(init?.headers).get("authorization") ?? "";
      return new Response(JSON.stringify({ state: "reachable" }), { status: 200, headers: { "content-type": "application/json" } });
    };
    const res = await call(ID, "operator-token", "?refresh=true&evil=1");
    assert.equal(res.status, 200);
    const u = new URL(url);
    assert.equal(u.pathname, `/attack-paths/focus/${ID}`);
    assert.equal(u.search, "", "no query key is forwarded: a refresh flag can never reach the backend");
    assert.equal(auth, "Bearer operator-token");
  });

  test("a path that is not a UUID is refused before any backend call; no token means no call", async () => {
    let calls = 0;
    globalThis.fetch = async () => { calls += 1; return new Response("{}", { status: 200 }); };
    for (const id of ["..%2F..%2Fadmin", "not-a-uuid", "1", `${ID}x`]) {
      assert.equal((await call(id)).status, 400, id);
    }
    assert.equal((await call(ID, null)).status, 401);
    assert.equal(calls, 0);
  });

  test("a refusal and an outage stay errors", async () => {
    globalThis.fetch = async () => new Response(JSON.stringify({ detail: "Engagement not found" }), { status: 404 });
    assert.equal((await call(ID)).status, 404);
    globalThis.fetch = async () => { throw new TypeError("fetch failed"); };
    assert.ok((await call(ID)).status >= 500);
  });
});
