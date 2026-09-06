import { test } from "node:test";
import assert from "node:assert/strict";

import {
  assess, readVector, redact, priorityOf, slaOf, confidenceOf, readinessOf,
  type RawFinding,
} from "../lib/report/finding-model";

function ok(name: string, cond: boolean, got?: unknown) {
  test(name, () => assert.ok(cond, got === undefined ? name : `${name}: ${JSON.stringify(got)}`));
}
function group(_name: string) {}

const base: RawFinding = {
  id: "VDH-001", title: "t", severity: "critical", status: "OPEN",
  affectedHost: "web-01", discoveredAt: "2026-08-20T09:00:00Z",
  description: "d", technicalDetails: "td", impact: "i",
  evidence: [{ label: "l", content: "c" }],
  remediation: ["fix it"], mitre: [], riskScore: 900,
  cvss: "9.8", activelyExploited: false, detectionCoverage: "BLIND",
  verification: { expected: "returns 403" },
};
const NOW = new Date("2026-09-06T00:00:00Z");
const F = (o: Partial<RawFinding>): RawFinding => ({ ...base, ...o });

/* ── priority ─────────────────────────────────────────────────────────────── */
group("priority");
ok("critical + KEV + internet-facing ⇒ P0",
  priorityOf(F({ activelyExploited: true, internetReachable: true })).code === "P0",
  priorityOf(F({ activelyExploited: true, internetReachable: true })).code);

ok("critical with no exploitation signal ⇒ P1",
  priorityOf(F({})).code === "P1", priorityOf(F({})).code);

ok("high + EPSS 0.7 ⇒ P1",
  priorityOf(F({ severity: "high", epss: 0.7 })).code === "P1",
  priorityOf(F({ severity: "high", epss: 0.7 })).code);

ok("high, quiet ⇒ P2", priorityOf(F({ severity: "high" })).code === "P2");
ok("medium, quiet ⇒ P3", priorityOf(F({ severity: "medium" })).code === "P3");
ok("low, quiet ⇒ P4", priorityOf(F({ severity: "low" })).code === "P4");

// The regression this run fixed.
const lowKev = priorityOf(F({ severity: "low", activelyExploited: true }));
ok("low but on KEV ⇒ floored to P2, not P4", lowKev.code === "P2", lowKev.code);
ok("...and the floor explains itself", lowKev.drivers.some(d => d.startsWith("Raised to P2")));

ok("drivers are listed for the reader",
  priorityOf(F({ activelyExploited: true, epss: 0.9, internetReachable: true })).drivers.length >= 3);
ok("dampeners are listed too",
  priorityOf(F({ severity: "medium", internetReachable: false,
    cvssVector: "CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:U/C:H/I:N/A:N" })).dampeners.length >= 2);

/* ── SLA ──────────────────────────────────────────────────────────────────── */
group("remediation clock");
const p0sla = slaOf(F({}), "P0", NOW);
ok("no backend deadline means no invented target", p0sla.state === "no-target", p0sla.state);
ok("an explicit past deadline is breached",
  slaOf(F({ dueAt: "2026-09-05T12:00:00Z" }), "P0", NOW).state === "breached");
ok("an accepted finding is no longer tracked",
  slaOf(F({ status: "ACCEPTED", dueAt: "2026-09-05T00:00:00Z" }), "P0", NOW).state === "closed");
ok("a future backend deadline is on track",
  slaOf(F({ dueAt: "2026-09-30T00:00:00Z" }), "P0", NOW).state === "on-track");

/* ── CVSS ─────────────────────────────────────────────────────────────────── */
group("CVSS vector reading");
const v31 = readVector("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H")!;
ok("3.1 parses", v31.version === "3.x");
ok("reach is network", v31.reach === "network");
ok("no credentials needed", v31.needsCredentials === false);
ok("prerequisites in plain English", v31.prerequisites[0].startsWith("Network reachability"));
ok("scope change is surfaced as blast radius",
  v31.outcomes.some(o => o.startsWith("Impact beyond")));

const v40 = readVector("CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N")!;
ok("4.0 parses", v40.version === "4.0");
ok("4.0 VC/VI/VA map onto the same outcome table", v40.outcomes.length >= 3, v40.outcomes);
ok("4.0 AT is named", v40.metrics.some(m => m.key === "AT" && m.name === "Attack requirements"));

ok("garbage vector returns null, not a guess", readVector("not-a-vector") === null);
ok("empty vector returns null", readVector(undefined) === null);

const stmt = assess(F({ cvssVector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
  internetReachable: true }), NOW).attackerStatement!;
ok("attacker statement reads as a sentence", /^An unauthenticated attacker reaching this service from the internet can /.test(stmt), stmt);

/* ── confidence ───────────────────────────────────────────────────────────── */
group("confidence");
ok("proven exploit ⇒ CONFIRMED", confidenceOf(F({ exploitValidated: true })).level === "CONFIRMED");
ok("version match ⇒ LIKELY", confidenceOf(F({ detectionMethod: "version" })).level === "LIKELY");
ok("version match carries the backport caveat",
  /backport/i.test(confidenceOf(F({ detectionMethod: "version" })).caveat ?? ""));
ok("banner only ⇒ POTENTIAL", confidenceOf(F({ detectionMethod: "banner" })).level === "POTENTIAL");
ok("nothing recorded ⇒ says so rather than implying proof",
  confidenceOf(F({})).label === "Unverified");

/* ── redaction ────────────────────────────────────────────────────────────── */
group("evidence redaction");
const dirty = [
  "uid=0(root)",
  "aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEX",
  "AKIAIOSFODNN7EXAMPLE",
  'curl https://admin:hunter2@10.0.0.5/api',
  "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIn0.dBjftJeZ4CVP",
  '{"api_key":"sk-live-9f8a7b6c5d4e"}',
  "Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0",
  "-----BEGIN RSA PRIVATE KEY-----\nMIIEow==\n-----END RSA PRIVATE KEY-----",
].join("\n");
const r = redact(dirty);

ok("aws_secret_access_key masked (no \\b — the classic miss)", !r.text.includes("wJalrXUtnFEMI"));
ok("AKIA key masked", !r.text.includes("AKIAIOSFODNN7EXAMPLE"));
ok("URL password masked", !r.text.includes("hunter2"));
ok("bearer token masked", !r.text.includes("eyJhbGciOiJIUzI1NiJ9"));
ok("JSON api_key masked", !r.text.includes("sk-live-9f8a7b6c5d4e"));
ok("NTLM hash masked", !r.text.includes("31d6cfe0d16ae931b73c59d7e0c089c0"));
ok("private key masked", !r.text.includes("MIIEow=="));
ok("non-secret output survives", r.text.includes("uid=0(root)"));
ok("hits are counted for the banner", r.total >= 7, r.total);
// The bug fixed this run: the subject string leaking in as a capture group.
ok("output is not duplicated by the replace callback",
  (r.text.match(/uid=0\(root\)/g) ?? []).length === 1);
ok("clean text passes through untouched", redact("open port 443/tcp").text === "open port 443/tcp");

/* ── readiness ────────────────────────────────────────────────────────────── */
group("delivery readiness");
ok("a complete finding is deliverable", readinessOf(base).ready);
ok("no evidence blocks delivery", !readinessOf(F({ evidence: [] })).ready);
ok("no remediation blocks delivery", !readinessOf(F({ remediation: [] })).ready);
ok("no pass criteria blocks delivery", !readinessOf(F({ verification: undefined })).ready);
ok("missing reproduction warns but does not block",
  readinessOf(F({ reproductionSteps: undefined })).blocking === 0);
ok("gaps name the field and say why",
  readinessOf(F({ evidence: [] })).gaps.every(g => g.field.length > 0 && g.why.length > 10));

/* ── degradation ──────────────────────────────────────────────────────────── */
group("missing data never throws");
const bare = { id: "X", title: "t", severity: "", status: "", affectedHost: "",
  discoveredAt: "", description: "", technicalDetails: "", evidence: [],
  impact: "", remediation: [], mitre: [], riskScore: 0, cvss: "",
  activelyExploited: false, detectionCoverage: "" } as RawFinding;
const a = assess(bare, NOW);
ok("severity falls back to INFO", a.severity === "INFO");
ok("no CVSS ⇒ null, not 0", a.cvssScore === null);
ok("no vector ⇒ null", a.vector === null);
ok("no attacker statement is invented", a.attackerStatement === null);
ok("assets empty rather than a phantom host", a.assets.length === 0);
ok("readiness reports every blocker", a.readiness.blocking >= 4, a.readiness.blocking);
ok("cvss '9.8 (High)' parses to 9.8", assess(F({ cvss: "9.8 (High)" }), NOW).cvssScore === 9.8);
ok("cvss out of range rejected", assess(F({ cvss: "94" }), NOW).cvssScore === null);
