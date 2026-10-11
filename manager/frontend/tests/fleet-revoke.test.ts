import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createServer, type Server } from "node:http";
import { join } from "node:path";
import type { AddressInfo } from "node:net";
import { afterEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { POST as revokePost } from "../app/api/fleet/agents/[id]/revoke/route";
import { createFleetWorkspaceApi } from "../lib/fleet-workspace-api";

// Revoking an agent: the console sends one POST to the manager and nothing else. The agent's history is not
// touched here (the manager keeps it); the button only exists for operators.

const read = (p: string) => readFileSync(join(process.cwd(), p), "utf8");
const servers: Server[] = [];
const origUrl = process.env.BACKEND_INTERNAL_URL;

afterEach(async () => {
  await Promise.all(servers.splice(0).map((s) => new Promise<void>((r) => s.close(() => r()))));
  process.env.BACKEND_INTERNAL_URL = origUrl;
});

async function fakeManager(reply: (req: { method?: string; url?: string; auth?: string; body: string }) => [number, unknown]) {
  const seen: { method?: string; url?: string; auth?: string; body: string }[] = [];
  const server = createServer((req, res) => {
    let body = "";
    req.on("data", (c) => { body += c; });
    req.on("end", () => {
      const call = { method: req.method, url: req.url, auth: req.headers.authorization, body };
      seen.push(call);
      const [status, payload] = reply(call);
      res.writeHead(status, { "content-type": "application/json" });
      res.end(JSON.stringify(payload));
    });
  });
  servers.push(server);
  await new Promise<void>((r) => server.listen(0, "127.0.0.1", () => r()));
  process.env.BACKEND_INTERNAL_URL = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
  return seen;
}

const ID = "11111111-1111-4111-8111-111111111111";
const call = (body: unknown, headers: Record<string, string> = { cookie: "vedha_token=op.jwt" }) =>
  revokePost(new NextRequest(`http://localhost/api/fleet/agents/${ID}/revoke`, {
    method: "POST", headers: { "content-type": "application/json", ...headers }, body: JSON.stringify(body),
  }), { params: Promise.resolve({ id: ID }) });

describe("revoke route", () => {
  test("forwards one POST to the manager with the operator's token and the reason", async () => {
    const seen = await fakeManager(() => [200, { id: ID, lifecycle_status: "revoked", already_revoked: false, disconnected: true, released_engagements: [] }]);
    const res = await call({ reason: "laptop lost" });
    assert.equal(res.status, 200);
    assert.equal(seen.length, 1);
    assert.equal(seen[0].method, "POST");
    assert.equal(seen[0].url, `/agents/${ID}/revoke`);
    assert.equal(seen[0].auth, "Bearer op.jwt");
    assert.deepEqual(JSON.parse(seen[0].body), { reason: "laptop lost" });
    assert.equal((await res.json()).lifecycle_status, "revoked");
  });

  test("works without a reason, and trims an oversized one to the manager's limit", async () => {
    const seen = await fakeManager(() => [200, { lifecycle_status: "revoked" }]);
    await call({});
    assert.equal(JSON.parse(seen[0].body).reason, null);
    await call({ reason: "x".repeat(900) });
    assert.equal(JSON.parse(seen[1].body).reason.length, 500);
  });

  test("a caller who is not signed in never reaches the manager", async () => {
    const seen = await fakeManager(() => [200, {}]);
    const res = await call({}, {});
    assert.equal(res.status, 401);
    assert.equal(seen.length, 0);
  });

  test("the manager's refusal (a viewer, another tenant's agent) reaches the operator unchanged", async () => {
    await fakeManager(() => [403, { detail: "Role 'viewer' is not permitted. Required: ['admin', 'manager']" }]);
    const res = await call({});
    assert.equal(res.status, 403);
    assert.match((await res.json()).error, /not permitted/);
    await fakeManager(() => [404, { detail: "Agent not found" }]);
    assert.equal((await call({})).status, 404);
  });
});

describe("Fleet client and screen", () => {
  test("operators get a revoke call; customers do not", async () => {
    const operator = createFleetWorkspaceApi("manager");
    const portal = createFleetWorkspaceApi("portal");
    assert.equal(operator.canRevokeAgent, true);
    assert.equal(portal.canRevokeAgent, false);
    await assert.rejects(portal.revokeAgent(ID), /managed|revoked by your Vedha operator/);
  });

  test("the operator client posts to the revoke route", async () => {
    const calls: { url: string; init?: RequestInit }[] = [];
    const realFetch = globalThis.fetch;
    globalThis.fetch = (async (url: string, init?: RequestInit) => {
      calls.push({ url: String(url), init });
      return new Response(JSON.stringify({ id: ID, lifecycle_status: "revoked", already_revoked: false, disconnected: false, released_engagements: [] }),
        { status: 200, headers: { "content-type": "application/json" } });
    }) as typeof fetch;
    try {
      await createFleetWorkspaceApi("manager").revokeAgent(ID, "retired");
    } finally { globalThis.fetch = realFetch; }
    assert.equal(calls[0].url, `/api/fleet/agents/${ID}/revoke`);
    assert.equal(calls[0].init?.method, "POST");
    assert.deepEqual(JSON.parse(String(calls[0].init?.body)), { reason: "retired" });
  });

  test("the screen asks first, says nothing is deleted, shows revoked agents as revoked and hides expiry for them", () => {
    const screen = read("app/fleet/FleetWorkspace.tsx");
    assert.match(screen, /window\.confirm\(/);
    assert.match(screen, /Its jobs, results and findings are kept/);
    assert.match(screen, /label: "revoked"/);
    assert.match(screen, /lifecycle_status !== "revoked"/);
    assert.match(screen, /api\.canRevokeAgent/);
  });
});
