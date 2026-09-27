import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { describe, test } from "node:test";

import { mapFindingGroupPage } from "../lib/adapters";
import { backendFindingFilters, backendQueryString } from "../lib/findings-query";

const findingsPage = readFileSync(new URL("../app/findings/page.tsx", import.meta.url), "utf8");

describe("findings filter mapping", () => {
  test("accepts the page's own signal-filter names (they were silently dropped)", () => {
    const f = backendFindingFilters(new URL("http://x/?detection_status=missed&exploit_validated=true"));
    assert.equal(f.detection_status, "missed");
    assert.equal(f.exploit_validated, true);
  });

  test("still accepts the older aliases", () => {
    const f = backendFindingFilters(new URL("http://x/?blind=true&validated=true"));
    assert.equal(f.detection_status, "missed");
    assert.equal(f.exploit_validated, true);
  });

  test("translates UI enums and drops garbage", () => {
    const f = backendFindingFilters(new URL(
      "http://x/?severity=HIGH&status=FALSE_POSITIVE&asset_ip=10.0.%25&verification_state=bogus"));
    assert.equal(f.severity, "high");
    assert.equal(f.status, "fp");
    assert.equal(f.asset_ip, undefined);
    assert.equal(f.verification_state, undefined);
  });

  test("portal query string reaches FastAPI with backend enum values", () => {
    const qs = new URLSearchParams(backendQueryString(
      "paginated=true&page=2&page_size=20&sort=risk&severity=CRITICAL&status=OPEN&scan=SCN-1&sort_bad=1"));
    assert.equal(qs.get("severity"), "critical");
    assert.equal(qs.get("status"), "open");
    assert.equal(qs.get("page"), "2");
    assert.equal(qs.get("sort"), "risk");
    assert.equal(qs.get("scan"), "SCN-1");
    assert.equal(qs.has("paginated"), false);
  });
});

describe("mapFindingGroupPage", () => {
  test("maps the backend payload to the UI shape", () => {
    const page = mapFindingGroupPage({
      items: [{
        engagement_id: "eng-1",
        key: "product:openbsd:openssh:7.4", kind: "product", label: "openssh 7.4 — known vulnerabilities",
        severity: "critical", severity_counts: { critical: 2, medium: 4 }, status_counts: { open: 5, fp: 1 },
        finding_count: 6, open_count: 5, host_count: 2, unassigned_count: 0,
        hosts: [{ ip: "10.0.0.7", hostname: null }], ports: [22], port_count: 1,
        cve_count: 3, cves: ["CVE-2023-38408"], max_risk: 980, max_cvss: 9.8, max_epss: null,
        kev: true, exploit_validated: false, first_seen: null, last_seen: null,
        top_finding_id: "f1",
        members: [{ id: "f1", title: "CVE-2023-38408 — openssh", severity: "critical", status: "open",
          asset_ip: "10.0.0.7", port: 22, cve_ids: ["CVE-2023-38408"], risk: 980, cvss: 9.8 }],
        members_truncated: true,
      }],
      total: 1, page: 1, page_size: 20, pages: 1, finding_total: 6, truncated: false,
    });
    const [g] = page.items;
    assert.equal(g.engagementId, "eng-1");
    assert.equal(g.severity, "CRITICAL");
    assert.deepEqual(g.severityCounts, { CRITICAL: 2, MEDIUM: 4 });
    assert.deepEqual(g.statusCounts, { OPEN: 5, FALSE_POSITIVE: 1 });
    assert.equal(g.members[0].severity, "CRITICAL");
    assert.equal(g.members[0].status, "OPEN");
    assert.equal(g.members[0].assetHostname, null);
    assert.equal(g.membersTruncated, true);
    assert.equal(page.findingTotal, 6);
  });

  test("tolerates an empty page", () => {
    assert.deepEqual(mapFindingGroupPage({}), {
      items: [], total: 0, page: 1, pageSize: 20, pages: 1, findingTotal: 0, truncated: false,
    });
  });
});

describe("grouped view wiring", () => {
  test("the grouped view queries with the same filter query string as the list", () => {
    assert.match(findingsPage, /api\.groups<FindingGroupPage>\(groupQueryString\.toString\(\)\)/);
    assert.match(findingsPage, /const groupQueryString = new URLSearchParams\(queryString\);/);
  });

  test("All findings is the default view and comes first; Grouped is second", () => {
    assert.match(findingsPage, /function getServerQueueView\(\): QueueView \{\s*return "list";/);
    assert.match(findingsPage, /=== "grouped" \? "grouped" : "list";/);
    const all = findingsPage.indexOf("<List size={13} aria-hidden /> All findings");
    const grouped = findingsPage.indexOf("<Layers size={13} aria-hidden /> Grouped");
    assert.ok(all > 0 && grouped > all, "All findings button renders before Grouped");
  });

  test("a group member opens the shared detail panel", () => {
    assert.match(findingsPage, /onSelect=\{toggleFinding\}[\s\S]{0,200}<\/FindingGroupRow>|<FindingGroupRow[\s\S]{0,400}onSelect=\{toggleFinding\}/);
  });
});
