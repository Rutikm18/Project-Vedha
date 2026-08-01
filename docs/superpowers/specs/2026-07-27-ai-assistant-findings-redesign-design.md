# Design — Global AI Assistant + Findings Redesign (Slice 1)

Date: 2026-07-27
Status: Approved (design); pending implementation plan
Scope: `manager/frontend` only — **no backend changes required**

## 1. Overview

First slice of a larger dashboard redesign. Two coupled surfaces:

1. **"Ask Vedha"** — a global, bottom-right floating AI assistant that explains a finding in
   plain English when the operator pastes its **finding ID**. Grounded in the *real* finding;
   the AI narrates but never invents facts.
2. **Findings** — friction reduction + polish on the existing (already data-rich) page, plus an
   **"Explain"** hook that deep-links the assistant, and cleanup of design-system drift.

Aesthetic: **refine & sharpen ARCTIC v9** (indigo accent, light-default). No new visual language.

### Non-goals (later slices)
Reports, Settings, the standalone AI Brain *page* restyle, and app-wide token migration are
explicitly out. The AI Brain page stays as-is (kept for deep offensive analysis).

## 2. Design principles
1. **Grounded over generative** — every fact the assistant states (severity, CVSS, KEV, EPSS,
   SLA, remediation) comes from the real `FindingOut`, not the model. The LLM only narrates.
2. **Sharpen, don't churn** — evolve ARCTIC; remove drift (`--adv-*` legacy tokens, unloaded
   `JetBrains Mono`, off-palette `#2563EB`). Route all severity colour through `lib/severity`.
3. **Fewer decisions per glance** — Findings answers "what do I fix first?" before anything else.

## 3. Architecture — the assistant

### 3.1 Data flow (grounded, server-authoritative)
```
FAB / ⌘K  ─▶  AssistantDrawer
   paste "F-1024"  ─▶  POST /api/assistant/explain { findingId, mode: "simple"|"technical" }
        │  (Next BFF route; forwards the JWT httpOnly cookie)
        ▼
   1. fetch the REAL finding  ── GET {BACKEND}/findings/{findingId}  → FindingOut
   2. build FACT CARD deterministically from FindingOut (no LLM)
   3. build server-owned "explain" prompt (system prompt NOT client-supplied)
   4. LLM narrates in plain English, grounded in the fetched finding
   ◀──  { factCard, narration, findingId }
Follow-ups ─▶ POST /api/assistant/chat { findingId, messages }
        the finding is re-fetched server-side and injected as context each call
```

**Why this shape:** mirrors the existing `app/api/brain/route.ts` (server owns the system prompt
+ context; client cannot inject either — a prompt-injection guard the codebase already values).
The single-finding fetch already exists end-to-end (`app/api/findings/[id]/route.ts` →
backend `GET /findings/{finding_id}`), so **no backend change**.

### 3.2 Graceful degradation
If `ANTHROPIC_API_KEY` is unset or the LLM call fails, the route returns the **fact card only**
with `narration: null`. The drawer renders the fact card (real data) + a quiet "AI narration
unavailable" note. **The assistant is useful with AI fully disabled** — the factual core is
deterministic.

### 3.3 Fact card (deterministic, from `FindingOut`)
- One-line "what it is" (title + category)
- Severity + risk chip, KEV / actively-exploited pips, EPSS %, CVSS, SLA state — real values
- "What to do first" = top remediation step
- `Simple ⇄ Technical` toggle changes narration verbosity + whether raw CVSS vector / MITRE show

### 3.4 UX / components
- `components/assistant/AssistantProvider.tsx` — context + state (open, activeFindingId, thread);
  mounted in `app/layout.tsx` **inside** `ToastProvider` so every route gets it.
- `AssistantFab.tsx` — bottom-right FAB (indigo, `Sparkles`), `⌘/Ctrl-K` toggle, respects
  `prefers-reduced-motion`.
- `AssistantDrawer.tsx` — 420px right drawer. Empty state: "Paste a finding ID (e.g. `F-1024`)…"
  + up to 3 recent-finding chips (from the findings query cache). ID auto-detect via regex
  (`F-?\d+`, `VAPT-[A-Z]+-\d+`). Then FactCard + narration + follow-up chat thread.
- Deep-link API: `useAssistant().explain(findingId)` — called by Findings "Explain" buttons.

### 3.5 New/changed files (assistant)
| File | Change |
|---|---|
| `app/api/assistant/explain/route.ts` | NEW — fetch finding, fact card + grounded narration |
| `app/api/assistant/chat/route.ts` | NEW — follow-up chat, finding re-injected server-side |
| `components/assistant/AssistantProvider.tsx` | NEW — provider + `useAssistant()` hook |
| `components/assistant/AssistantFab.tsx` | NEW |
| `components/assistant/AssistantDrawer.tsx` | NEW |
| `components/assistant/FactCard.tsx` | NEW — deterministic finding summary |
| `app/layout.tsx` | mount `<AssistantProvider>` (+ FAB/drawer) inside ToastProvider |
| `lib/assistant.ts` | NEW — finding-ID regex, FindingOut→FactCard mapping, fetch helpers |

## 4. Findings redesign (friction ↓, polish ↑)
Existing page: `app/findings/page.tsx` (1059 lines, TanStack Query, master list + 5-tab detail).
Changes are surgical — no data-model rebuild.

1. **Priority Queue band** (top strip): `N actively-exploited · N KEV · N SLA-breached`, each a
   one-click filter. Derived from the already-fetched list.
2. **Sticky filter/search bar**: text search + severity/status/KEV/exploited as **chip toggles**
   (not dropdowns); visible current sort.
3. **Calmer rows**: title + host + one risk chip + severity + SLA countdown + KEV/exploited pips.
   Move MITRE/tags/EPSS% into the detail view. Improves scan-ability.
4. **Detail view**: keep 5 tabs; tighten hierarchy/spacing; add **Explain** button in the header
   → `useAssistant().explain(finding.id)`.
5. **Design-system cleanup (scoped to this page + assistant):** `--adv-*` → ARCTIC tokens,
   `#2563EB` → `var(--accent)`, `'JetBrains Mono'` → `var(--font-mono)`, severity via
   `lib/severity`.

## 5. Shared design-system sharpening (minimal)
Only what this slice needs: (a) `--font-mono` is the single mono source (drop JetBrains refs on
touched files); (b) `AssistantProvider` mounted globally; (c) severity colour routes through
`lib/severity`. No global re-theme.

> Note: the frontend is a customized Next.js ("This is NOT the Next.js you know" —
> `manager/frontend/AGENTS.md`). Before writing route/layout code, read the relevant guide in
> `node_modules/next/dist/docs/`.

## 6. Success criteria (verifiable)
- Paste a real finding ID → fact card values **match that finding's row** on the Findings page.
- First paint of the fact card in < 2s; narration streams/loads after.
- With `ANTHROPIC_API_KEY` unset → fact card still renders; no crash; clear "AI unavailable" note.
- Findings shows a working Priority Queue whose counts match the filtered list; chip filters work.
- No `--adv-*`, `#2563EB`, or `JetBrains Mono` references remain in the touched files.
- `⌘/Ctrl-K` toggles the assistant from any page; drawer is keyboard-navigable; FAB has an
  `aria-label`; reduced-motion honored.

## 7. Risks / open questions
- **Finding-ID format**: confirm the real `FindingOut.id` shape (UUID vs `F-###` vs
  `VAPT-CRIT-###`). The regex + "recent chips" must match reality; verify against a live finding
  during implementation.
- **Streaming**: narration may stream (like `/api/brain`) or return whole. Default: return whole
  for v1 (simpler), stream as a follow-up if latency warrants.
- **Rate/cost**: explain calls hit the LLM per finding; cache last N explanations client-side by
  findingId to avoid re-billing on re-open.

## 8. Out of scope (explicit)
Reports redesign, Settings redesign/PAT UI, AI Brain page restyle, wiring real data into the AI
Brain side panels or Reports, app-wide token migration, and any backend change.
