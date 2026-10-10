import assert from "node:assert/strict";
import { createServer, type Server } from "node:http";
import { createServer as createTcpServer, type AddressInfo } from "node:net";
import { after, afterEach, beforeEach, describe, test } from "node:test";
import { NextRequest } from "next/server";

import { backend, BackendError, backendResponse } from "../lib/backend";
import { GET as probesGet } from "../app/api/scan/probes/route";

// "Probe inventory: fetch failed" — the Next.js server could not get an answer
// from FastAPI and the reason was thrown away. Each case below is a real socket
// failure, not a mock, so the codes are the ones Node's fetch really produces.

const servers: { close: (cb?: () => void) => unknown }[] = [];
const origEnv = { url: process.env.BACKEND_INTERNAL_URL, t: process.env.BACKEND_READ_TIMEOUT_MS };
const origError = console.error;
let logged: string[] = [];

beforeEach(() => { logged = []; console.error = (line: string) => { logged.push(String(line)); }; });
afterEach(async () => {
  console.error = origError;
  await Promise.all(servers.splice(0).map((s) => new Promise<void>((r) => s.close(() => r()))));
  process.env.BACKEND_INTERNAL_URL = origEnv.url;
  if (origEnv.t === undefined) delete process.env.BACKEND_READ_TIMEOUT_MS;
  else process.env.BACKEND_READ_TIMEOUT_MS = origEnv.t;
});
after(() => { console.error = origError; });

async function listen(server: Server | ReturnType<typeof createTcpServer>): Promise<number> {
  servers.push(server);
  await new Promise<void>((r) => server.listen(0, "127.0.0.1", () => r()));
  return (server.address() as AddressInfo).port;
}

async function closedPort(): Promise<number> {
  const s = createTcpServer();
  await new Promise<void>((r) => s.listen(0, "127.0.0.1", () => r()));
  const port = (s.address() as AddressInfo).port;
  await new Promise<void>((r) => s.close(() => r()));
  return port;
}

const useBackend = (port: number) => { process.env.BACKEND_INTERNAL_URL = `http://127.0.0.1:${port}`; };

async function rejection(p: Promise<unknown>): Promise<BackendError> {
  try { await p; } catch (e) { assert.ok(e instanceof BackendError, `not a BackendError: ${e}`); return e; }
  assert.fail("expected the call to fail");
}

describe("an unreachable Manager API is named, not 'fetch failed'", () => {
  test("API down → 503 ECONNREFUSED, retry hint, one log line", async () => {
    useBackend(await closedPort());
    const e = await rejection(backend("/agents", { token: "t" }));
    assert.equal(e.status, 503);
    assert.match(e.message, /ECONNREFUSED/);
    assert.doesNotMatch(e.message, /fetch failed|127\.0\.0\.1/);
    assert.equal(e.retryAfter, 5);
    const entry = JSON.parse(logged[0]);
    assert.equal(entry.event, "backend.unreachable");
    assert.equal(entry.code, "ECONNREFUSED");
    assert.equal(entry.path, "/agents");
  });

  test("the scan page's probe route answers 503 with the reason (was 500 'fetch failed')", async () => {
    useBackend(await closedPort());
    const res = await probesGet(new NextRequest("http://localhost/api/scan/probes", {
      headers: { cookie: "vedha_token=t" },
    }));
    assert.equal(res.status, 503);
    assert.equal(res.headers.get("retry-after"), "5");
    const body = await res.json();
    assert.match(body.error, /Manager API refused the connection/);
  });

  test("a dropped read is retried once and then succeeds", async () => {
    let hits = 0;
    const port = await listen(createServer((req, res) => {
      hits += 1;
      if (hits === 1) { req.socket.destroy(); return; }
      res.setHeader("content-type", "application/json");
      res.end(JSON.stringify([{ id: "probe-1" }]));
    }));
    useBackend(port);
    assert.deepEqual(await backend("/agents", { token: "t" }), [{ id: "probe-1" }]);
    assert.equal(hits, 2);
  });

  test("a read dropped twice → 502 naming the reset", async () => {
    let hits = 0;
    const port = await listen(createServer((req) => { hits += 1; req.socket.destroy(); }));
    useBackend(port);
    const e = await rejection(backend("/engagements/overview", { token: "t" }));
    assert.equal(e.status, 502);
    assert.match(e.message, /dropped the connection/);
    assert.equal(hits, 2);
  });

  test("a write is never repeated", async () => {
    let hits = 0;
    const port = await listen(createServer((req) => { hits += 1; req.socket.destroy(); }));
    useBackend(port);
    const e = await rejection(backend("/scan", { token: "t", method: "POST", body: { a: 1 } }));
    assert.equal(e.status, 502);
    assert.equal(hits, 1);
  });

  test("a read that never answers → 504 after the read timeout, not 300 s", async () => {
    const port = await listen(createServer(() => { /* never answers */ }));
    useBackend(port);
    process.env.BACKEND_READ_TIMEOUT_MS = "200";
    const started = Date.now();
    const e = await rejection(backend("/agents", { token: "t" }));
    assert.equal(e.status, 504);
    assert.match(e.message, /did not answer within 200 ms/);
    assert.ok(Date.now() - started < 5_000);
  });

  test("the timeout bounds the wait for headers only, never a slow body", async () => {
    const port = await listen(createServer((_req, res) => {
      res.writeHead(200, { "content-type": "text/csv" });
      res.write("a,b\n");
      setTimeout(() => res.end("1,2\n"), 500);
    }));
    useBackend(port);
    process.env.BACKEND_READ_TIMEOUT_MS = "200";
    const res = await backendResponse("/export", { token: "t" });
    assert.equal(await res.text(), "a,b\n1,2\n");
  });

  test("a body cut off after the headers → 502", async () => {
    const port = await listen(createServer((_req, res) => {
      res.writeHead(200, { "content-type": "application/json", "content-length": "100" });
      res.write("[{\"id\":");
      setTimeout(() => res.socket?.destroy(), 20);
    }));
    useBackend(port);
    const e = await rejection(backend("/agents", { token: "t" }));
    assert.equal(e.status, 502);
  });

  test("an unresolvable API host → 503 pointing at BACKEND_INTERNAL_URL", async () => {
    process.env.BACKEND_INTERNAL_URL = "http://vedha-api.invalid:8000";
    const e = await rejection(backend("/agents", { token: "t" }));
    assert.equal(e.status, 503);
    assert.match(e.message, /BACKEND_INTERNAL_URL/);
  });

  test("an HTTP error from the API is still passed through unchanged", async () => {
    const port = await listen(createServer((_req, res) => {
      res.writeHead(404, { "content-type": "application/json" });
      res.end(JSON.stringify({ detail: "Engagement not found" }));
    }));
    useBackend(port);
    const e = await rejection(backend("/engagements/x", { token: "t" }));
    assert.equal(e.status, 404);
    assert.equal(e.message, "Engagement not found");
  });
});
