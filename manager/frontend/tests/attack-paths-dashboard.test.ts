import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { afterEach, describe, test } from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { NextRequest } from "next/server";

import { GET as overviewGet } from "../app/api/attack-paths/overview/route";
import { OverviewFootnote, OverviewList } from "../components/attack-paths/OverviewList";
import {
  OperatorConsoleProvider, PortalConsoleProvider, useConsoleCapability, useConsoleSource,
} from "../lib/console-source";
import type { OverviewRow } from "../lib/attack-paths";

const read = (p: string) => readFileSync(join(process.cwd(), p), "utf8");
const html = (el: Parameters<typeof renderToStaticMarkup>[0]) => renderToStaticMarkup(el);

const row = (over: Partial<OverviewRow> = {}): OverviewRow => ({
  engagement_id: "11111111-1111-4111-8111-111111111111", name: "Acme network assessment", status: "active",
  computed: true, computed_at: "2026-10-09T09:00:00Z", path_count: 6, entry_points: 2, crown_jewels: 2,
  fix_set_size: 2, fix_assets: ["vpn-gw", "web-1"], fix_assets_more: 0, coverage: "partial", stale_assets: 1,
  why_empty: [], ...over,
});

describe("overview rows", () => {
  test("each row links to that engagement's Attack paths page and says what it found, in words", () => {
    const out = html(createElement(OverviewList, { rows: [row()] }));
    assert.match(out, /href="\/engagements\/11111111-1111-4111-8111-111111111111\/attack-paths"/);
    assert.match(out, /Acme network assessment/);
    assert.match(out, />6 routes</);
    assert.match(out, /Cutting every route takes 2 hosts: vpn-gw, web-1\./);
    assert.match(out, /Coverage partial/);
    assert.match(out, /1 host not seen recently/);
    assert.match(out, /aria-label="Acme network assessment: 6 routes\./);
  });

  test("an engagement nobody computed reads 'not computed yet', never '0 routes'", () => {
    const out = html(createElement(OverviewList, {
      rows: [row({ computed: false, path_count: null, fix_set_size: null, fix_assets: [], coverage: null, stale_assets: null, computed_at: null })],
    }));
    assert.match(out, /Not computed yet/);
    assert.doesNotMatch(out, /0 routes|No routes modelled|Coverage/);
  });

  test("zero routes carries its reason and never claims safety", () => {
    const out = html(createElement(OverviewList, {
      rows: [row({ path_count: 0, fix_set_size: 0, fix_assets: [], coverage: "observed", stale_assets: 0,
        why_empty: [{ code: "no_targets", detail: "x" }] })],
    }));
    assert.match(out, /No routes modelled/);
    assert.match(out, /No crown jewels marked\. This is not evidence the network is safe\./);
    assert.doesNotMatch(out, /all clear|you are safe|no risk/i);
  });

  test("the footnote says what zero routes and 'not computed' mean", () => {
    const out = html(createElement(OverviewFootnote));
    assert.match(out, /not that the network is safe/);
    assert.match(out, /nobody has opened that engagement/);
  });

  test("special characters in an engagement name are escaped, not rendered as markup", () => {
    const out = html(createElement(OverviewList, { rows: [row({ name: "<img src=x onerror=alert(1)>" })] }));
    assert.doesNotMatch(out, /<img src=x/);
    assert.match(out, /&lt;img src=x onerror=alert\(1\)&gt;/);
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
    assert.match(out, /mode=operator;can=true;endpoint=\/api\/attack-paths\/overview\?limit=50/);
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
});

describe("navigation", () => {
  test("operators get an Attack paths entry marked BETA; the customer menu does not", () => {
    const sidebar = read("components/Sidebar.tsx");
    const operator = sidebar.slice(sidebar.indexOf("const NAV_SECTIONS"), sidebar.indexOf("const PORTAL_NAV_SECTIONS"));
    const portal = sidebar.slice(sidebar.indexOf("const PORTAL_NAV_SECTIONS"));
    assert.match(operator, /label: "Attack paths", href: "\/attack-paths", badge: "BETA"/);
    assert.doesNotMatch(portal.slice(0, portal.indexOf("];") + 2), /attack-paths|Attack paths/);
  });

  test("the /attack-paths page reads the overview and says it is beta", () => {
    const page = read("app/attack-paths/page.tsx");
    assert.match(page, /\/api\/attack-paths\/overview\?limit=200/);
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
