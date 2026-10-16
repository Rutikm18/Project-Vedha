import { test } from "node:test";
import assert from "node:assert/strict";
import {
  EMPTY_FILTERS, RECORDED_FIELDS, actorName, auditQuery, changeLines, exportHref, filterCount,
  formatUtc, hasFilters, integritySentence, mapAuditEntry, mapAuditPage, mapCustomerPage,
  mapIntegrity, periodRange,
} from "../lib/audit-log";

test("an empty filter asks for everything, and dates are read as UTC days", () => {
  assert.equal(auditQuery(EMPTY_FILTERS), "");
  const q = new URLSearchParams(auditQuery({ ...EMPTY_FILTERS, from: "2026-10-01", to: "2026-10-16" }));
  assert.equal(q.get("from"), "2026-10-01T00:00:00Z");
  assert.equal(q.get("to"), "2026-10-16T23:59:59.999Z");
});

test("a malformed date is dropped rather than sent", () => {
  assert.equal(auditQuery({ ...EMPTY_FILTERS, from: "yesterday" }), "");
});

test("filters are trimmed, and extras such as the cursor are appended", () => {
  const q = new URLSearchParams(auditQuery(
    { ...EMPTY_FILTERS, q: "  login ", category: "authentication", outcome: "failure", ip: " 203.0.113.7 " },
    { limit: 50, cursor: "abc", skipped: undefined, empty: "" }));
  assert.equal(q.get("q"), "login");
  assert.equal(q.get("ip"), "203.0.113.7");
  assert.equal(q.get("category"), "authentication");
  assert.equal(q.get("outcome"), "failure");
  assert.equal(q.get("limit"), "50");
  assert.equal(q.get("cursor"), "abc");
  assert.equal(q.has("skipped") || q.has("empty"), false);
});

test("filters in force are counted and detected", () => {
  assert.equal(hasFilters(EMPTY_FILTERS), false);
  assert.equal(filterCount({ ...EMPTY_FILTERS, q: "x", outcome: "denied" }), 2);
});

test("quick periods end open and start on a UTC day", () => {
  const now = new Date("2026-10-16T08:30:00Z");
  assert.deepEqual(periodRange("24h", now), { from: "2026-10-15", to: "" });
  assert.deepEqual(periodRange("7d", now), { from: "2026-10-09", to: "" });
  assert.deepEqual(periodRange("all", now), { from: "", to: "" });
});

test("the export link carries the filters in force", () => {
  const href = exportHref({ ...EMPTY_FILTERS, outcome: "failure" }, "json");
  assert.match(href, /^\/api\/audit-logs\/export\?/);
  assert.match(href, /outcome=failure/);
  assert.match(href, /format=json/);
});

test("times are shown in UTC", () => {
  assert.equal(formatUtc("2026-10-16T08:21:04.123Z"), "2026-10-16 08:21:04 UTC");
  assert.equal(formatUtc("not a date"), "not a date");
});

test("the actor is named by label, then by kind, then by a short id", () => {
  const a = (actor: { id: string; type: string | null; label: string | null }) => actorName({ actor });
  assert.equal(a({ id: "u1", type: "user", label: "ops@vedha.io" }), "ops@vedha.io");
  assert.equal(a({ id: "anonymous", type: "anonymous", label: null }), "Not signed in");
  assert.equal(a({ id: "system", type: "system", label: null }), "System");
  assert.equal(a({ id: "11111111-2222-3333-4444-555555555555", type: "user", label: null }), "11111111…");
});

test("changes read as field, before and after, with blanks shown as a dash", () => {
  assert.deepEqual(
    changeLines({ status: { before: "open", after: "confirmed" }, owner: { before: null, after: { id: 1 } } }),
    [{ field: "status", before: "open", after: "confirmed" }, { field: "owner", before: "—", after: '{"id":1}' }]);
  assert.deepEqual(changeLines(null), []);
});

test("the integrity sentence is honest about each state", () => {
  const base = mapIntegrity({ ok: true, entries_checked: 1284, retention_days: 365, minimum_retention_days: 180 });
  assert.equal(integritySentence(base), "Tamper check passed: 1,284 entries verified in order.");
  assert.match(integritySentence({ ...base, entriesChecked: 0 }), /No entries yet/);
  const bad = mapIntegrity({
    ok: false, entries_checked: 10, first_problem: { position: 4, entry_id: "x", reason: "an entry was changed" },
  });
  assert.match(integritySentence(bad), /failed at entry 4: an entry was changed.*untrusted/);
});

test("the server's snake_case entry maps to the UI shape", () => {
  const e = mapAuditEntry({
    id: "i", timestamp: "t", action: "a", label: "L", category: "c", category_label: "C", outcome: "denied",
    actor: { id: "u", type: "user", label: "x@y" }, ip_address: "1.2.3.4", chain_position: 7, entry_hash: "ff",
    changes: { f: { before: 1, after: 2 } },
  });
  assert.equal(e.categoryLabel, "C");
  assert.equal(e.ipAddress, "1.2.3.4");
  assert.equal(e.chainPosition, 7);
  assert.equal(e.resourceType, null);
  assert.equal(mapAuditPage({ items: [{ id: "i", actor: {} }], next_cursor: "c" }).nextCursor, "c");
});

test("the customer view maps who and whether the actor is Vedha staff", () => {
  const page = mapCustomerPage({
    items: [{ id: "i", timestamp: "t", label: "Finding changed", category: "findings", category_label: "Findings",
      outcome: "success", who: "Vedha analyst", who_is_vedha: true, ip_address: null }],
    next_cursor: null,
  });
  assert.equal(page.items[0].whoIsVedha, true);
  assert.equal(page.items[0].ipAddress, null);
});

test("every recorded field names the controls it supports", () => {
  for (const r of RECORDED_FIELDS) assert.ok(r.field && r.answers && r.controls, r.field);
});
