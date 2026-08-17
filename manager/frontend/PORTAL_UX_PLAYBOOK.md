# Spawning a Customer Dashboard *from* an Operator Dashboard

The recipe used to derive the Vedha **customer portal** from the existing
**manager (operator) dashboard**: one product, two audiences. The customer
dashboard is visually the *same product*, but exposes only a **scoped,
read-only slice** of the data — achieved by **reusing** the design system,
**forking** the shell + auth, and **projecting** scoped data.

Use this to spin a customer/partner/client dashboard off any internal admin app.

---

## The mental model

```
                 operator dashboard (full trust, full data, all actions)
                         │
        ┌────────────────┼─────────────────────────────┐
   REUSE (verbatim)   FORK (thin copies)          PROJECT (scoped subset)
   design system      shell + auth + transport    read-only Client* data
        │                     │                          │
        └──────────────► customer dashboard ◄────────────┘
              (looks identical · limited nav · client-scoped · read-only)
```

**Four moves:**
1. **REUSE** the design-system layer verbatim → instant visual parity.
2. **FORK** the shell (mirror the operator chrome; limited nav; client identity).
3. **FORK** the auth + transport (separate login, cookie, BFF proxy, client-role backend router).
4. **PROJECT** scoped, read-only data (`Client*Out` subsets via a scoping query); downgrade capabilities.

---

## 1. REUSE — the shared design-system layer (don't rebuild)

The customer dashboard imports the **same** `globals.css` — same tokens, same
primitives (`.btn*`, `.input-base`, `.panel`, `.chip`), same `DataState`
orchestrator, same `report-*` / `settings-*` component classes.

> This is *why* the portal "looks like the same product." **Do not re-theme, do
> not re-implement primitives.** Visual parity is free because both audiences
> render off one token + primitive layer.

(The full design-system layer — tokens, primitives, motion, `DataState`, a11y —
is the foundation; it is deliberately audience-agnostic so both dashboards share it.)

---

## 2. FORK the shell — mirror the chrome, swap the map

Create a `PortalShell` that is a **structural copy** of the operator `PageShell`
(same header / sidebar / footer built from the same tokens), differing only in:

| Aspect | Operator `PageShell` | Customer `PortalShell` |
|---|---|---|
| Nav items | full (Engagements, Fleet, Scan, Customers, Settings…) | **limited** (Dashboard, Findings, Scans, Reports, Settings) |
| Identity | operator user | "Customer" + engagement name |
| Sign-out | operator logout | portal logout (`/api/portal/logout`) |
| Live/status chrome | operator status | same widgets, customer data |

Everything else (theme toggle, session timer, footer, spacing) is **identical**
by reusing the same tokens. Keep the chrome the same on purpose — parity is the
point.

---

## 3. FORK the auth + transport — the trust boundary

This is the part that makes it a *separate product surface*, not just a filtered view.

- **Separate login + cookie.** A dedicated portal login route issues a **distinct
  session cookie** (`vedha_portal_token`) — a different principal than the operator
  JWT.
- **BFF catch-all proxy.** One route, `app/api/portal/[...path]/route.ts`, forwards
  `/api/portal/<path>` → backend `/portal/<path>`, attaching the portal token.
  **The proxy carries the token only; it never enforces scoping** — that is the
  backend's job.
- **Dedicated backend router.** `app/routers/portal.py` — every endpoint is gated
  by a **client-role dependency** (`ClientUser`). The operator routers are a
  different trust context entirely; the portal router is the *only* surface a
  customer principal can reach.
- **Thin typed client.** `portalApi<T>(path)` → `/api/portal<path>`; on `401`,
  a single silent **refresh-and-retry**, then redirect to `/portal/login`.
  React-Query keys are namespaced (`["portal", resource, …]`).

```
Customer browser ──(vedha_portal_token cookie)──▶ /api/portal/[...path]   (Next BFF: carries token)
                                                        │
                                                        ▼
                                            backend /portal/*  (ClientUser gate + scoping)
```

---

## 4. PROJECT — scoped, read-only data (the core "customer-only" logic)

For every operator resource you want to expose, define a **`Client<Resource>Out`
schema = a *subset* of the operator schema** (drop internal / operator-only
fields), and produce it with a **scoping query**:

```python
# every portal query is pinned to the caller's engagement/tenant
rows = client_scoped(select(Model), user, Model.engagement_id) ...
```

- `client_scoped(...)` guarantees a customer can only ever address rows inside
  **their** engagement/tenant. An out-of-scope id returns **404** — the customer
  can't even learn it exists (no existence disclosure).
- Encode "what a customer may see" as **extra server-side filters**, e.g. reports
  are returned **only when `approved`**; scans exclude already-dispatched duplicate
  requests; drafts are invisible.
- **Read-only by default.** In the portal the *only* write is
  `create_scan_request` (`ScanRequestCreate`) — and even that is **approval-gated**:
  it creates a *request* that an operator must approve before anything runs.

So "customer dashboard that only [shows its own, read-only, approved slice]" is
enforced at the schema + query layer, not the UI.

---

## 5. DOWNGRADE — capability matrix (operator → customer)

| Operator capability | Customer equivalent |
|---|---|
| **Launch scan** (pick probe / engagement / fleet, runs immediately) | **Request scan** (type · intensity · targets · note) → operator approves. **Probe fleet, probe selection, engagement selection all removed.** |
| Findings (full, editable, reopen/triage) | Findings (**read-only**, sort + severity filter) |
| Reports (engagement-grounded, operator endpoints) | Reports **document rebuilt from scoped `/portal/summary + /findings + /trends`** + an approved-downloads tab |
| Settings (AI runtime, Email/Slack/Jira secrets, **Access & Security**, SLA, Notifications) | Settings (**Engagement, Appearance, SLA, Notifications**) — all operator config + Access/Security **removed** |
| Live jobs / activity | Status **accordion** (collapsed by default, phase ticker, polls while active) |

Rule of thumb: **remove any action that changes infrastructure or crosses
tenants; keep read + one approval-gated request.**

---

## 6. Page mirror map (what each customer page is derived from)

| Customer page (`/portal/*`) | Derived from operator | How |
|---|---|---|
| `page.tsx` (dashboard) | operator dashboard | KPIs/posture from `/portal/summary` + `/trends` |
| `findings/page.tsx` | `/findings` | read-only projection, client-scoped |
| `scans/page.tsx` | `/scan` (launch) | launch → **request**; jobs → accordion |
| `reports/page.tsx` | `/reports` | tabbed live document from scoped endpoints + approved docs |
| `settings/page.tsx` | `/settings` | same `settings-*` shell, customer-relevant sections only |
| `login/page.tsx` | operator login | separate cookie + portal auth |

---

## 7. Recipe — spawn a customer dashboard for a NEW product

1. **Confirm the shared layer exists** (tokens + primitives + `DataState`). If the
   operator app inlines styles, extract them into primitives first — otherwise the
   portal can't inherit parity.
2. **Add a client principal.** New login + cookie + a role/claim that identifies a
   client and pins it to a tenant/engagement.
3. **Add a BFF catch-all** `/api/<portal>/[...path]` that forwards the client token
   to a **new backend router** gated by the client role.
4. **Define `Client*Out` schemas** = subsets of operator schemas; implement every
   query through a `client_scoped()` helper. Add per-resource visibility filters
   (approved-only, etc.). Keep it read-only + at most one approval-gated write.
5. **Fork the shell** (`PortalShell`) from the operator shell: same chrome, limited
   nav, client identity, portal logout.
6. **Compose the pages** by mirroring operator pages against the scoped endpoints;
   **apply the downgrade matrix** (strip infra/cross-tenant actions).
7. **Verify the boundary:** an authenticated client principal can reach *only* the
   portal router; every portal query is scoped; out-of-scope ids 404; the only
   mutation is the approval-gated request.

---

## 8. Security invariants (must hold)

- **Backend owns scoping; the BFF only carries the token.** Never scope in the proxy.
- **Client principal ≠ operator principal.** Different cookie, different router,
  different role gate.
- **Every portal query is `client_scoped`** — no unscoped `select` in the portal router.
- **Out-of-scope = 404**, not 403 (no existence disclosure).
- **Read-only by default;** the sole write is approval-gated and creates a
  *request*, never a live action.
- **Approved-only projections** for anything reviewable (reports, etc.).

---

## 9. Reference file map (mirror these)

| Concern | Artifact |
|---|---|
| Shared design system (reused) | `app/globals.css`, `components/states/DataState.tsx` |
| Forked shell | `components/portal/PortalShell.tsx` (mirrors `components/PageShell.tsx`) |
| BFF proxy | `app/api/portal/[...path]/route.ts` |
| Client transport + 401 refresh | `lib/portal-client.ts` |
| Client-role backend router + `Client*Out` + `client_scoped` | `backend/app/routers/portal.py`, `backend/app/schemas/portal.py` |
| Customer pages | `app/portal/{page,findings,scans,reports,settings,login}` |

---

**One-line summary:** reuse the design system verbatim (parity for free), fork a
thin shell + a separate client auth/BFF/router, and expose the domain only through
**client-scoped, read-only `Client*Out` projections** with one approval-gated
write. The look is inherited; the *boundary* — a distinct principal reaching a
scoped, read-only router — is what makes it a customer dashboard.
