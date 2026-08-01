# Global AI Assistant + Findings Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a global, bottom-right "Ask Vedha" assistant that explains a *real* finding in plain English (grounded, non-hallucinating), plus friction/polish on the Findings page — frontend-only.

**Architecture:** New BFF routes under `app/api/assistant/` fetch the real finding via the existing backend proxy, build a deterministic fact card from `FindingOut`, and have the LLM narrate (grounded). A global `AssistantProvider` (FAB + drawer) mounts in `app/layout.tsx`. Findings gets an "Explain" deep-link, a Priority Queue band, chip filters, calmer rows, and design-token cleanup.

**Tech Stack:** Next.js (customized — see constraint), React, TypeScript, `@anthropic-ai/sdk`, `@tanstack/react-query`, `node:test` for pure-logic tests, ARCTIC design tokens (`app/globals.css`), `lib/severity`, `lib/adapters.toUiFinding`.

## Global Constraints
- **Frontend only.** No backend change: `GET /findings/{finding_id}` and `app/api/findings/[id]/route.ts` already exist.
- **Customized Next.js:** per `manager/frontend/AGENTS.md`, before writing any `route.ts`/`layout.tsx`, read the relevant guide under `manager/frontend/node_modules/next/dist/docs/`.
- **Finding IDs are UUIDs** (`FindingOut.id: uuid`). Primary explain flow = deep-link from a row / recent-finding chip; paste supports UUID and CVE-ID.
- **Grounded, server-authoritative AI:** system prompt + finding context are built server-side (mirror `app/api/brain/route.ts`). The client never supplies the system prompt or the "finding" text.
- **Graceful degrade:** if `ANTHROPIC_API_KEY` is unset or the LLM errors, return the fact card with `narration: null`; the UI still renders the fact card.
- **Design tokens:** on every touched file, use ARCTIC vars (`var(--accent)`, `var(--font-mono)`, `lib/severity`) — never `--adv-*`, `#2563EB`, or `'JetBrains Mono'`.
- **Test command:** `npx tsx --test tests/<file>.test.ts` (run from `manager/frontend/`).
- **Typecheck/lint gate for UI (no component-test harness exists):** `npm run build` and `npm run lint` from `manager/frontend/`.
- Work from `manager/frontend/` for all commands below.

## File Structure
| File | Responsibility |
|---|---|
| `lib/assistant.ts` | Pure logic: `detectFindingId`, `toFactCard(uiFinding)`, `FactCardVM` type. Testable. |
| `tests/assistant.test.ts` | `node:test` unit tests for `lib/assistant.ts`. |
| `app/api/assistant/explain/route.ts` | BFF: fetch finding → fact card + grounded narration. |
| `app/api/assistant/chat/route.ts` | BFF: follow-up chat, finding re-injected server-side. |
| `components/assistant/AssistantProvider.tsx` | Context/state + `useAssistant()`; renders FAB + Drawer. |
| `components/assistant/AssistantFab.tsx` | Bottom-right FAB, ⌘/Ctrl-K toggle. |
| `components/assistant/AssistantDrawer.tsx` | 420px drawer: input, FactCard, narration, follow-up thread. |
| `components/assistant/FactCard.tsx` | Deterministic finding summary (from `FactCardVM`). |
| `app/layout.tsx` | Mount `<AssistantProvider>` inside `ToastProvider`. |
| `app/findings/page.tsx` | Explain deep-link, Priority Queue band, chip filters, calmer rows, token cleanup. |

---

### Task 1: `lib/assistant.ts` — finding-ID detection + fact-card mapping (TDD)

**Files:**
- Create: `lib/assistant.ts`
- Test: `tests/assistant.test.ts`

**Interfaces:**
- Consumes: the UI finding shape produced by `lib/adapters.toUiFinding` (fields used: `id, title, severity, cvss, cvssVector, category, status, affectedHost, riskScore, epssScore, kevListed, activelyExploited, remediation[]`).
- Produces:
  - `type FactCardVM = { id: string; title: string; severity: string; whatItIs: string; whyItMatters: string; whatToDo: string; cvss: string; epssPct: number; risk: number; kev: boolean; exploited: boolean; status: string; host: string }`
  - `detectFindingId(text: string): string | null`
  - `toFactCard(f: any): FactCardVM`

- [ ] **Step 1: Write the failing test**

```ts
// tests/assistant.test.ts
import assert from "node:assert/strict";
import { describe, test } from "node:test";
import { detectFindingId, toFactCard } from "../lib/assistant";

describe("detectFindingId", () => {
  test("finds a UUID anywhere in pasted text", () => {
    const id = "3f9a1c2e-1b2c-4d5e-8f90-abcdef012345";
    assert.equal(detectFindingId(`please explain ${id} thanks`), id);
  });
  test("finds a CVE id", () => {
    assert.equal(detectFindingId("what about CVE-2024-3094?"), "CVE-2024-3094");
  });
  test("returns null when nothing looks like an id", () => {
    assert.equal(detectFindingId("explain the kerberoast finding"), null);
  });
});

describe("toFactCard", () => {
  const ui = {
    id: "3f9a1c2e-1b2c-4d5e-8f90-abcdef012345",
    title: "Unconstrained Delegation on DC01",
    severity: "CRITICAL", cvss: "9.8", cvssVector: "AV:N", category: "AD",
    status: "OPEN", affectedHost: "10.10.10.5", riskScore: 940,
    epssScore: 0.72, kevListed: true, activelyExploited: true,
    remediation: ["Remove unconstrained delegation from DC01"],
  };
  test("maps real fields into the fact card (no invented numbers)", () => {
    const fc = toFactCard(ui);
    assert.equal(fc.risk, 940);
    assert.equal(fc.kev, true);
    assert.equal(fc.epssPct, 72);
    assert.equal(fc.whatToDo, "Remove unconstrained delegation from DC01");
    assert.equal(fc.host, "10.10.10.5");
  });
  test("degrades gracefully when remediation is empty", () => {
    const fc = toFactCard({ ...ui, remediation: [] });
    assert.equal(fc.whatToDo, "No remediation recorded yet — see the finding's Remediation tab.");
  });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx tsx --test tests/assistant.test.ts`
Expected: FAIL — `Cannot find module '../lib/assistant'`.

- [ ] **Step 3: Write minimal implementation**

```ts
// lib/assistant.ts
export type FactCardVM = {
  id: string; title: string; severity: string;
  whatItIs: string; whyItMatters: string; whatToDo: string;
  cvss: string; epssPct: number; risk: number;
  kev: boolean; exploited: boolean; status: string; host: string;
};

const UUID_RE = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;
const CVE_RE = /CVE-\d{4}-\d{4,7}/i;

export function detectFindingId(text: string): string | null {
  const uuid = text.match(UUID_RE);
  if (uuid) return uuid[0].toLowerCase();
  const cve = text.match(CVE_RE);
  if (cve) return cve[0].toUpperCase();
  return null;
}

function plainWhyItMatters(f: any): string {
  const bits: string[] = [];
  if (f.activelyExploited) bits.push("attackers are actively exploiting this in the wild");
  if (f.kevListed) bits.push("it is on CISA's Known Exploited Vulnerabilities list");
  const epssPct = Math.round((f.epssScore ?? 0) * 100);
  if (epssPct >= 10) bits.push(`there is a ${epssPct}% modelled chance of exploitation (EPSS)`);
  if (bits.length === 0) bits.push(`it carries a ${String(f.severity).toLowerCase()} severity rating`);
  return `This matters because ${bits.join(", and ")}.`;
}

export function toFactCard(f: any): FactCardVM {
  const rem = Array.isArray(f.remediation) ? f.remediation : [];
  const first = rem.find((s: unknown) => typeof s === "string") as string | undefined;
  return {
    id: String(f.id),
    title: f.title ?? "Untitled finding",
    severity: String(f.severity ?? "INFO"),
    whatItIs: `${f.title ?? "This finding"}${f.category ? ` — a ${f.category} issue` : ""} on ${f.affectedHost ?? "an in-scope host"}.`,
    whyItMatters: plainWhyItMatters(f),
    whatToDo: first ?? "No remediation recorded yet — see the finding's Remediation tab.",
    cvss: f.cvss != null ? String(f.cvss) : "—",
    epssPct: Math.round((f.epssScore ?? 0) * 100),
    risk: Math.round(f.riskScore ?? 0),
    kev: Boolean(f.kevListed),
    exploited: Boolean(f.activelyExploited),
    status: String(f.status ?? "OPEN"),
    host: f.affectedHost ?? "—",
  };
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npx tsx --test tests/assistant.test.ts`
Expected: PASS — 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add lib/assistant.ts tests/assistant.test.ts
git commit -m "feat(assistant): finding-id detection + grounded fact-card mapping"
```

---

### Task 2: `app/api/assistant/explain/route.ts` — grounded explain BFF

**Files:**
- Create: `app/api/assistant/explain/route.ts`

**Interfaces:**
- Consumes: `toFactCard` (Task 1); the existing backend proxy convention in `app/api/brain/route.ts` and `app/api/findings/[id]/route.ts` (cookie-forwarded JWT; `BACKEND_INTERNAL_URL`).
- Produces: `POST /api/assistant/explain` body `{ findingId: string, mode?: "simple"|"technical" }` → `{ factCard: FactCardVM, narration: string | null, findingId: string }`.

- [ ] **Step 1: Read the Next route guide** (customized Next.js)

Run: `ls manager/frontend/node_modules/next/dist/docs/ && sed -n '1,60p' app/api/findings/[id]/route.ts`
Expected: understand how the existing finding-by-id proxy forwards auth (reuse the exact same fetch/cookie pattern).

- [ ] **Step 2: Write the route** (mirror `app/api/brain/route.ts` for the LLM half)

```ts
// app/api/assistant/explain/route.ts
import { NextRequest, NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";
import { toFactCard } from "../../../../lib/assistant";
import { toUiFinding } from "../../../../lib/adapters";

const BACKEND = process.env.BACKEND_INTERNAL_URL ?? "http://api:8000";

const SYSTEM = `You are a security analyst explaining ONE finding to a colleague.
You are given the finding's real, structured data. Explain it in plain English.
Rules: never invent a CVE, CVSS, host, or number that is not in the data provided.
If a fact is absent, say it is not recorded. Be concise, calm, and practical.`;

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => null) as { findingId?: string; mode?: string } | null;
  if (!body?.findingId) {
    return NextResponse.json({ error: "findingId is required" }, { status: 400 });
  }

  // 1) fetch the REAL finding server-side, forwarding the operator's session cookie
  const res = await fetch(`${BACKEND}/findings/${encodeURIComponent(body.findingId)}`, {
    headers: { cookie: req.headers.get("cookie") ?? "",
               authorization: req.headers.get("authorization") ?? "" },
    cache: "no-store",
  });
  if (!res.ok) {
    return NextResponse.json({ error: `finding not found (${res.status})` }, { status: res.status });
  }
  const raw = await res.json();
  const factCard = toFactCard(toUiFinding(raw));

  // 2) narrate — grounded; degrade to fact-card-only if the LLM is unavailable
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return NextResponse.json({ factCard, narration: null, findingId: body.findingId });
  }
  try {
    const client = new Anthropic({ apiKey });
    const technical = body.mode === "technical";
    const msg = await client.messages.create({
      model: process.env.LLM_MODEL ?? "claude-sonnet-4-6",
      max_tokens: technical ? 700 : 350,
      system: SYSTEM,
      messages: [{
        role: "user",
        content: `Finding data (JSON):\n${JSON.stringify(raw)}\n\n` +
          (technical
            ? "Explain to a security engineer: what it is, the exploitation path, and the fix."
            : "Explain to a non-expert stakeholder in 4-5 short sentences: what it is, why it matters, and what to do."),
      }],
    });
    const narration = msg.content.filter((c) => c.type === "text").map((c: any) => c.text).join("\n").trim();
    return NextResponse.json({ factCard, narration, findingId: body.findingId });
  } catch {
    return NextResponse.json({ factCard, narration: null, findingId: body.findingId });
  }
}
```

- [ ] **Step 3: Typecheck**

Run: `npm run build`
Expected: build succeeds (route compiles).

- [ ] **Step 4: Manual smoke (dev server + a real finding UUID)**

Run: start dev (`npm run dev`), then with a valid session cookie:
`curl -s -X POST localhost:3000/api/assistant/explain -H 'Content-Type: application/json' -d '{"findingId":"<real-uuid>"}' | python3 -m json.tool`
Expected: JSON with `factCard` (real values matching that finding) and `narration` (string, or `null` if no API key). A bad id returns a 4xx.

- [ ] **Step 5: Commit**

```bash
git add app/api/assistant/explain/route.ts
git commit -m "feat(assistant): grounded explain BFF route (real finding + LLM narration)"
```

---

### Task 3: `app/api/assistant/chat/route.ts` — follow-up chat

**Files:**
- Create: `app/api/assistant/chat/route.ts`

**Interfaces:**
- Produces: `POST /api/assistant/chat` body `{ findingId: string, messages: {role,content}[] }` → `{ content: string }` (503 if no key).

- [ ] **Step 1: Write the route**

```ts
// app/api/assistant/chat/route.ts
import { NextRequest, NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";

const BACKEND = process.env.BACKEND_INTERNAL_URL ?? "http://api:8000";
const SYSTEM = `You are a security analyst answering follow-up questions about ONE finding.
The finding's real JSON data is provided. Never invent facts not present in it.
Be concise and practical; stay in scope of authorized testing.`;

export async function POST(req: NextRequest) {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return NextResponse.json({ error: "ANTHROPIC_API_KEY not configured" }, { status: 503 });
  const body = await req.json().catch(() => null) as
    { findingId?: string; messages?: { role: string; content: string }[] } | null;
  if (!body?.findingId || !Array.isArray(body.messages) || body.messages.length === 0) {
    return NextResponse.json({ error: "findingId and messages[] required" }, { status: 400 });
  }
  const res = await fetch(`${BACKEND}/findings/${encodeURIComponent(body.findingId)}`, {
    headers: { cookie: req.headers.get("cookie") ?? "", authorization: req.headers.get("authorization") ?? "" },
    cache: "no-store",
  });
  const findingJson = res.ok ? JSON.stringify(await res.json()) : "{}";
  try {
    const client = new Anthropic({ apiKey });
    const msg = await client.messages.create({
      model: process.env.LLM_MODEL ?? "claude-sonnet-4-6",
      max_tokens: 600,
      system: `${SYSTEM}\n\nFinding JSON:\n${findingJson}`,
      messages: body.messages.map((m) => ({ role: m.role === "user" ? "user" : "assistant", content: m.content })) as any,
    });
    const content = msg.content.filter((c) => c.type === "text").map((c: any) => c.text).join("\n").trim();
    return NextResponse.json({ content });
  } catch (e) {
    return NextResponse.json({ error: e instanceof Error ? e.message : "LLM error" }, { status: 502 });
  }
}
```

- [ ] **Step 2: Typecheck** — Run: `npm run build` — Expected: succeeds.
- [ ] **Step 3: Commit**

```bash
git add app/api/assistant/chat/route.ts
git commit -m "feat(assistant): grounded follow-up chat route"
```

---

### Task 4: `AssistantProvider` + `useAssistant()` hook

**Files:**
- Create: `components/assistant/AssistantProvider.tsx`

**Interfaces:**
- Produces: `useAssistant()` → `{ open: boolean; findingId: string | null; explain(id: string): void; openBlank(): void; close(): void }`. Renders `<AssistantFab/>` + `<AssistantDrawer/>` (Tasks 5–6).

- [ ] **Step 1: Write the provider** (state + keyboard shortcut; the drawer does the fetching)

```tsx
// components/assistant/AssistantProvider.tsx
"use client";
import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { AssistantFab } from "./AssistantFab";
import { AssistantDrawer } from "./AssistantDrawer";

type Ctx = { open: boolean; findingId: string | null;
  explain: (id: string) => void; openBlank: () => void; close: () => void };
const AssistantCtx = createContext<Ctx | null>(null);
export function useAssistant() {
  const c = useContext(AssistantCtx);
  if (!c) throw new Error("useAssistant must be used within AssistantProvider");
  return c;
}

export function AssistantProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const [findingId, setFindingId] = useState<string | null>(null);
  const explain = useCallback((id: string) => { setFindingId(id); setOpen(true); }, []);
  const openBlank = useCallback(() => { setOpen(true); }, []);
  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); setOpen((o) => !o); }
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <AssistantCtx.Provider value={{ open, findingId, explain, openBlank, close }}>
      {children}
      <AssistantFab />
      <AssistantDrawer />
    </AssistantCtx.Provider>
  );
}
```

- [ ] **Step 2: Typecheck** — Run: `npm run build` — Expected: fails only on missing `./AssistantFab`/`./AssistantDrawer` (created next). Proceed to Task 5–6, then re-run.
- [ ] **Step 3: Commit** (after Tasks 5–6 compile together)

```bash
git add components/assistant/AssistantProvider.tsx
git commit -m "feat(assistant): provider + useAssistant hook"
```

---

### Task 5: `FactCard` component

**Files:**
- Create: `components/assistant/FactCard.tsx`

**Interfaces:**
- Consumes: `FactCardVM` (Task 1), `SEV_COLOR` from `lib/severity`.
- Produces: `<FactCard vm={FactCardVM} />`.

- [ ] **Step 1: Write the component** (ARCTIC tokens only)

```tsx
// components/assistant/FactCard.tsx
"use client";
import React from "react";
import type { FactCardVM } from "../../lib/assistant";
import { SEV_COLOR } from "../../lib/severity";

function Pip({ label, on, color }: { label: string; on: boolean; color: string }) {
  if (!on) return null;
  return <span className="badge" style={{ color, background: `${color}15`, border: `0.5px solid ${color}30` }}>{label}</span>;
}

export function FactCard({ vm }: { vm: FactCardVM }) {
  const sev = (SEV_COLOR as any)[vm.severity] ?? "var(--text-muted)";
  return (
    <div className="card" style={{ padding: 14, display: "flex", flexDirection: "column", gap: 10 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <span className="badge" style={{ color: sev, background: `${sev}15`, border: `0.5px solid ${sev}30` }}>{vm.severity}</span>
        <Pip label="KEV" on={vm.kev} color="var(--sev-critical-color)" />
        <Pip label="ACTIVELY EXPLOITED" on={vm.exploited} color="var(--sev-critical-color)" />
        <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-muted)" }}>RISK {vm.risk}</span>
      </div>
      <div style={{ fontSize: 14, fontWeight: 600, color: "var(--text-primary)" }}>{vm.title}</div>
      <div style={{ fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.5 }}>{vm.whatItIs}</div>
      <div style={{ fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.5 }}>{vm.whyItMatters}</div>
      <div style={{ display: "flex", gap: 14, fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--text-muted)" }}>
        <span>CVSS {vm.cvss}</span><span>EPSS {vm.epssPct}%</span><span>{vm.status}</span><span>{vm.host}</span>
      </div>
      <div style={{ fontSize: 13, color: "var(--text-primary)", borderTop: "0.5px solid var(--border-subtle)", paddingTop: 8 }}>
        <span style={{ fontWeight: 600 }}>Do first: </span>{vm.whatToDo}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Commit** (with Task 6)

---

### Task 6: `AssistantDrawer` + `AssistantFab`

**Files:**
- Create: `components/assistant/AssistantFab.tsx`
- Create: `components/assistant/AssistantDrawer.tsx`

**Interfaces:**
- Consumes: `useAssistant()`, `FactCard`, `detectFindingId`, `FactCardVM`.
- Produces: `<AssistantFab/>`, `<AssistantDrawer/>` (self-contained; fetch `/api/assistant/explain` + `/api/assistant/chat`).

- [ ] **Step 1: Write the FAB**

```tsx
// components/assistant/AssistantFab.tsx
"use client";
import React from "react";
import { Sparkles } from "lucide-react";
import { useAssistant } from "./AssistantProvider";

export function AssistantFab() {
  const { open, openBlank } = useAssistant();
  if (open) return null;
  return (
    <button aria-label="Open Ask Vedha assistant (Cmd/Ctrl-K)" onClick={openBlank}
      className="btn btn-primary"
      style={{ position: "fixed", right: 20, bottom: 20, zIndex: 50, height: 48, width: 48, borderRadius: 999, padding: 0, boxShadow: "var(--shadow-accent)" }}>
      <Sparkles size={20} />
    </button>
  );
}
```

- [ ] **Step 2: Write the Drawer** (input → explain → fact card + narration → follow-up chat)

```tsx
// components/assistant/AssistantDrawer.tsx
"use client";
import React, { useState, useEffect, useCallback } from "react";
import { X, Send } from "lucide-react";
import { useAssistant } from "./AssistantProvider";
import { FactCard } from "./FactCard";
import { detectFindingId, type FactCardVM } from "../../lib/assistant";

type Msg = { role: "user" | "assistant"; content: string };

export function AssistantDrawer() {
  const { open, findingId, close } = useAssistant();
  const [input, setInput] = useState("");
  const [activeId, setActiveId] = useState<string | null>(null);
  const [card, setCard] = useState<FactCardVM | null>(null);
  const [narration, setNarration] = useState<string | null>(null);
  const [thread, setThread] = useState<Msg[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const explainId = useCallback(async (id: string) => {
    setLoading(true); setError(null); setActiveId(id); setThread([]);
    try {
      const r = await fetch("/api/assistant/explain", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ findingId: id }),
      });
      if (!r.ok) { setError(`Couldn't load finding ${id.slice(0, 8)}… (${r.status})`); setCard(null); setNarration(null); return; }
      const d = await r.json() as { factCard: FactCardVM; narration: string | null };
      setCard(d.factCard); setNarration(d.narration);
    } catch { setError("Network error reaching the assistant."); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { if (open && findingId && findingId !== activeId) explainId(findingId); }, [open, findingId, activeId, explainId]);

  const submit = () => {
    const id = detectFindingId(input);
    if (id) { explainId(id); setInput(""); return; }
    if (activeId && input.trim()) sendFollowup(input.trim());
  };

  const sendFollowup = async (text: string) => {
    if (!activeId) return;
    const next = [...thread, { role: "user" as const, content: text }];
    setThread(next); setInput(""); setLoading(true);
    try {
      const r = await fetch("/api/assistant/chat", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ findingId: activeId, messages: next }),
      });
      const d = await r.json() as { content?: string; error?: string };
      setThread([...next, { role: "assistant", content: d.content ?? `[${d.error ?? "no reply"}]` }]);
    } finally { setLoading(false); }
  };

  if (!open) return null;
  return (
    <>
      <div onClick={close} style={{ position: "fixed", inset: 0, background: "var(--modal-backdrop)", zIndex: 50 }} />
      <aside role="dialog" aria-label="Ask Vedha assistant"
        style={{ position: "fixed", top: 0, right: 0, bottom: 0, width: 420, maxWidth: "100vw", zIndex: 51,
          background: "var(--bg-panel)", borderLeft: "0.5px solid var(--border-subtle)", boxShadow: "var(--shadow-lg)",
          display: "flex", flexDirection: "column" }}>
        <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "12px 16px", borderBottom: "0.5px solid var(--border-subtle)" }}>
          <span style={{ fontWeight: 700, color: "var(--text-primary)" }}>Ask Vedha</span>
          <button aria-label="Close assistant" onClick={close} className="btn btn-ghost" style={{ height: 30, width: 30, padding: 0 }}><X size={16} /></button>
        </header>

        <div style={{ flex: 1, overflowY: "auto", padding: 16, display: "flex", flexDirection: "column", gap: 12 }}>
          {!card && !loading && !error && (
            <div style={{ color: "var(--text-secondary)", fontSize: 13, lineHeight: 1.6 }}>
              Paste a finding ID (a UUID or a CVE), or click <b>Explain</b> on any finding.
              I’ll explain it in plain English — grounded in the real finding, never invented.
            </div>
          )}
          {error && <div className="settings-note" style={{ color: "var(--sev-critical-color)" }}>{error}</div>}
          {card && <FactCard vm={card} />}
          {card && (
            <div style={{ fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.6, whiteSpace: "pre-wrap" }}>
              {narration ?? "AI narration is unavailable (no API key or the model is offline) — the facts above are exact."}
            </div>
          )}
          {thread.map((m, i) => (
            <div key={i} style={{ alignSelf: m.role === "user" ? "flex-end" : "flex-start", maxWidth: "85%",
              background: m.role === "user" ? "var(--accent-ghost)" : "var(--bg-surface)",
              border: "0.5px solid var(--border-subtle)", borderRadius: 8, padding: "8px 12px", fontSize: 13, whiteSpace: "pre-wrap" }}>
              {m.content}
            </div>
          ))}
          {loading && <div style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--accent)" }}>thinking…</div>}
        </div>

        <div style={{ padding: 12, borderTop: "0.5px solid var(--border-subtle)", display: "flex", gap: 8 }}>
          <input className="input-base" value={input} onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter") submit(); }}
            placeholder={activeId ? "Ask a follow-up…" : "Paste a finding ID (UUID or CVE)…"} aria-label="Assistant input" />
          <button className="btn btn-primary" onClick={submit} disabled={loading} aria-label="Send"><Send size={14} /></button>
        </div>
      </aside>
    </>
  );
}
```

- [ ] **Step 3: Typecheck the whole assistant** — Run: `npm run build` — Expected: succeeds (Tasks 4–6 compile).
- [ ] **Step 4: Commit**

```bash
git add components/assistant/
git commit -m "feat(assistant): FAB + drawer (explain, grounded narration, follow-up chat)"
```

---

### Task 7: Mount the assistant globally in `app/layout.tsx`

**Files:**
- Modify: `app/layout.tsx` (wrap `children` inside `ToastProvider`).

- [ ] **Step 1: Edit** — replace `<ToastProvider>{children}</ToastProvider>` with:

```tsx
<ToastProvider>
  <AssistantProvider>{children}</AssistantProvider>
</ToastProvider>
```
…and add at the top with the other imports:
```tsx
import { AssistantProvider } from "../components/assistant/AssistantProvider";
```

- [ ] **Step 2: Verify on the running app** — Run: `npm run dev`, open any page.
Expected: the indigo FAB shows bottom-right on every page; `⌘/Ctrl-K` toggles the drawer; `Esc`/backdrop closes it.

- [ ] **Step 3: Commit**

```bash
git add app/layout.tsx
git commit -m "feat(assistant): mount Ask Vedha globally in root layout"
```

---

### Task 8: Findings — "Explain" deep-link + design-token cleanup

**Files:**
- Modify: `app/findings/page.tsx`

- [ ] **Step 1: Add the Explain hook + button.** Near the other imports add `import { useAssistant } from "../../components/assistant/AssistantProvider";`. In the detail view header (the component rendering a selected finding `f`), add a button:

```tsx
// inside the detail header actions, alongside existing buttons:
<button className="btn btn-secondary" onClick={() => explain(f.id)} aria-label="Explain this finding">
  <Brain size={14} /> Explain
</button>
```
…and in that component read the hook: `const { explain } = useAssistant();` (`Brain` is already imported in this file).

- [ ] **Step 2: Token cleanup (scoped to this file).** Replace in `app/findings/page.tsx`:
  - `'JetBrains Mono', monospace` → `var(--font-mono)`
  - literal `#2563EB` → `var(--accent)`
  - `var(--adv-text-muted)` → `var(--text-muted)`, `var(--adv-text)` → `var(--text-primary)`, `var(--adv-border)` → `var(--border-subtle)` (and other `--adv-*` → nearest ARCTIC token per `globals.css` alias table).

- [ ] **Step 3: Verify** — Run: `npm run build && npm run lint` — Expected: both pass.
- [ ] **Step 4: Verify visually** — dev server → Findings → open a finding → click **Explain** → drawer opens pre-loaded with that finding's fact card (values match the row).
- [ ] **Step 5: Commit**

```bash
git add app/findings/page.tsx
git commit -m "feat(findings): Explain deep-link to assistant + ARCTIC token cleanup"
```

---

### Task 9: Findings — Priority Queue band + chip filters + calmer rows

**Files:**
- Modify: `app/findings/page.tsx`

**Interfaces:**
- Consumes: the already-fetched findings list (TanStack Query) + `getSlaColor` (in-file). No new data.

- [ ] **Step 1: Add derived counts** near the list render (after the findings array is available as `rows`):

```tsx
const pq = useMemo(() => ({
  exploited: rows.filter((f) => f.activelyExploited).length,
  kev: rows.filter((f) => f.kevListed).length,
  slaBreached: rows.filter((f) => getSlaColor(f.discoveredAt, f.severity).label === "BREACHED").length,
}), [rows]);
const [quick, setQuick] = useState<null | "exploited" | "kev" | "sla">(null);
```

- [ ] **Step 2: Render the Priority Queue band** above the table; each cell toggles `quick`:

```tsx
<div style={{ display: "flex", gap: 10, marginBottom: 12 }}>
  {[
    { k: "exploited", n: pq.exploited, label: "Actively exploited", c: "var(--sev-critical-color)" },
    { k: "kev", n: pq.kev, label: "KEV-listed", c: "var(--sev-high-color)" },
    { k: "sla", n: pq.slaBreached, label: "SLA breached", c: "var(--sev-critical-color)" },
  ].map((x) => (
    <button key={x.k} onClick={() => setQuick(quick === x.k ? null : (x.k as any))}
      className="stat-card" aria-pressed={quick === x.k}
      style={{ flex: 1, textAlign: "left", cursor: "pointer",
        borderColor: quick === x.k ? x.c : "var(--border-subtle)" }}>
      <div style={{ fontFamily: "var(--font-mono)", fontSize: 22, color: x.c, fontWeight: 700 }}>{x.n}</div>
      <div style={{ fontSize: 12, color: "var(--text-secondary)" }}>{x.label}</div>
    </button>
  ))}
</div>
```

- [ ] **Step 3: Apply the quick filter** where the visible list is computed (fold into the existing filter/`useMemo`):

```tsx
const visible = useMemo(() => rows.filter((f) =>
  (quick === null) ||
  (quick === "exploited" && f.activelyExploited) ||
  (quick === "kev" && f.kevListed) ||
  (quick === "sla" && getSlaColor(f.discoveredAt, f.severity).label === "BREACHED")
), [rows, quick]);
```
Then render `visible` instead of `rows` in the list, preserving any existing search/severity filters (chain them).

- [ ] **Step 4: Verify** — Run: `npm run build && npm run lint` — Expected: pass.
- [ ] **Step 5: Verify visually** — dev server → Findings: band shows counts; clicking a cell filters the list to that set; counts match the filtered rows.
- [ ] **Step 6: Commit**

```bash
git add app/findings/page.tsx
git commit -m "feat(findings): priority-queue band with one-click exploited/KEV/SLA filters"
```

---

## Self-Review

**Spec coverage:** assistant (Tasks 1–7), Findings Explain hook (8), Findings friction/priority queue (9), token cleanup (8), graceful degrade (2/6), grounded/server-authoritative (2/3). ✔ Reports/Settings/AI-Brain-page correctly deferred (out of scope).
**Placeholder scan:** every code step has real code; commands are the verified `npx tsx --test …` / `npm run build|lint`. ✔
**Type consistency:** `FactCardVM` defined in Task 1 is the exact type consumed by Tasks 2, 5, 6. `useAssistant()` signature in Task 4 matches calls in Tasks 6–8. `explain(id)` used consistently. ✔
**Known deviation from strict TDD:** only `lib/assistant.ts` is unit-testable (no component-test harness exists); components/routes are gated by `build` + `lint` + manual dev-server checks, per Global Constraints.
```
