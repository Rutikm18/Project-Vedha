# Windows agent — zero-knowledge one-command install (plan)

Date: 2026-10-13 · Status: **BUILT on branch `feat/windows-zero-knowledge-install` (not pushed).**
Supersedes the "VIP token" sketch (see §2, why it was wrong).

> **As-built note (13 Oct).** Two refinements emerged during implementation and are the shipped
> design: (a) **mint-on-redeem** — the install code is its own `agent_install_codes` table (migration
> 0063) that stores *no* secret and authorises minting one `vet_` at redeem time, rather than a column
> on the token row; the manager only stores hashes, so a stored-and-returned raw token was never an
> option. (b) **S3 (device-fingerprint binding) was dropped** — the device key does not exist until
> enrolment (after redeem), and single-use redeem + `max_uses=1` already give "bind to first redeemer";
> theft of a code becomes *visible* via the recorded redeemer IP. §5 below describes the original
> device-pubkey idea; the shipped redeem takes just `{code}`. Tests: 19 backend + 4 PowerShell, full
> backend suite 3,282 passed.
Builds on: [ADR-0005](../adr/0005-windows-agent-delivery.md) · [secure-delivery design](../design/windows-agent-secure-delivery-design.md) ·
[Windows pipeline](2026-10-07-windows-agent-pipeline.md) · [probe_enrollment.py] · [agent_distribution.py].

Owner's requirement (13 Oct 2026):
> Make the Windows install dead simple. The token is **issued and authenticated automatically by the
> manager**. One command installs the required dependencies. Share **only the minimum code** the client
> needs to run the agent. The client must **not log in to the server**, and must **not be given the IP,
> any key, or the manager name**.

## 1. What already exists (read from the code, do not rebuild)

* **`vet_` enrollment tokens** — single-use, engagement-bound, short-TTL, stored only as a hash
  (`ProbeEnrollmentToken`, `probe_enrollment.py`). The manager mints them; the raw is shown once.
* **Enrolment protocol** — device-code / token flow: the agent generates its own Ed25519 device key,
  requests enrolment, signs a challenge, activates, then refreshes 10-minute access tokens. No human
  credential ever lands on the machine. Pairing-code fallback already exists.
* **`manager_public_url`** — config: "what a customer's host dials; used to build the install command."
* **Agent distribution** — the manager already serves `GET /agent/install.ps1`, `install.cmd`,
  `manifest.json` (+ signatures), and a **token-gated** `GET /agent/package/windows`.
* **Compiled build** — Nuitka `--standalone` folder build (ADR-0005 D2): every dependency bundled, and
  **no source, no bytecode, no docstrings** ship (CI fails if any appear).
* **Tokenless + pairing install** — `agent_allow_tokenless_install`; the philosophical sibling of this plan.

The machinery is all here. This plan changes **what the client is handed** and **how the manager fronts
itself**, not the enrolment protocol.

## 2. Why the "VIP token" sketch was wrong (recorded so we don't repeat it)

The earlier idea embedded the manager URL and the `vet_` token inside a signed, base64-encoded code:
`vip_<base64url({"u":"https://mgr…","t":"vet_…"})><sig>`.

| # | Failure | Consequence |
|---|---|---|
| F1 | **base64 is reversible.** A client decodes the code and reads the manager URL + `vet_` in cleartext. | Breaks "don't share IP/key/manager name" outright. The signature authenticates; it does not conceal. |
| F2 | The bootstrap then dialled `irm $mgr_url/agent/install.ps1` with the decoded URL. | Real manager hostname hits the client's DNS/TLS — a second leak. |
| F3 | An HMAC key baked into the **public** `get.ps1` can be read by any client. | Anyone could forge codes. Self-defeating secret placement. |
| F4 | Operator mints a `vet_`, then separately mints the code. | Owner asked for "automatically issued by the manager" — one action, not two. |
| F5 | A stateless wrapper over `vet_` adds no revocation or "redeemed from IP x" audit. | No kill switch, no forensics at the install-code layer. |

**Root cause:** a *self-describing* token. If the secret is inside the thing you hand the client, no
signature saves you. The fix is an **opaque pointer** whose meaning lives only on the manager.

## 3. Honest scope boundary (stated, not promised away)

You **cannot hide the endpoint from someone who owns the machine** — a client admin can `netstat`/sniff
and see the agent's outbound connection. That is physics. What this plan *does* guarantee:

* the **shared command** carries no manager IP, no key, no internal manager name, no readable token;
* the client types **one opaque code** and nothing else, and never logs in anywhere;
* the only name the client can observe is a **generic public façade** (e.g. `get.vedhasec.com`), never
  the manager's real hostname/IP, release key, or enrolment secret.

## 4. The design (owner-approved choices, 13 Oct)

Three changes. Everything else is reuse.

### 4.1 Opaque claim code (replaces the self-describing token)
A random, single-use, short-TTL handle — e.g. `VDHA-7K2M-9QXP`. It contains **nothing**; decoding it
reveals nothing. Stored as `claim_code_hash` on the existing `ProbeEnrollmentToken` row. The raw `vet_`
token stays on the manager and is never displayed.

### 4.2 One public façade: vanity domain → manager  *(chosen: "Vanity domain → manager")*
The Vedha façade `get.vedhasec.com` (domain `vedhasec.com`, owner-confirmed 13 Oct; subdomain label
still their pick) CNAMEs / reverse-proxies to the manager (Caddy). Set
`MANAGER_PUBLIC_URL=https://get.vedhasec.com`. The
manager already serves the installer and enrolment API; the vanity host simply fronts them. The client
only ever sees the vanity name.

```
Client runs ONE line (only the façade + the opaque code are visible):

  & ([scriptblock]::Create((irm https://get.vedhasec.com/agent/install.ps1))) -Code VDHA-7K2M-9QXP
        │
        │  1. POST https://get.vedhasec.com/agent/redeem  { code, device_pub, nonce }   (public, hardened)
        │        └─ atomic single-use: marks code used, pins device_pub, audits redeemer IP,
        │           returns the real vet_ token in the HTTPS body — in memory, never printed
        │
        │  2. installs the COMPILED agent folder against the SAME origin it came from
        │        → there is no separate "manager URL" to reveal; -Manager = the façade
        │
        └─ 3. agent enrols with the vet_ (its device key must match the pinned device_pub),
              then dials https://get.vedhasec.com for everything after.
```

### 4.3 One-click Fleet automation
"Add Windows Agent" → a single backend call mints the `vet_` token **and** the opaque claim code **and**
returns the final one-liner. The operator copies one string; the token is "issued and authenticated
automatically by the manager" with zero token handling.

### 4.4 Compiled Nuitka standalone  *(chosen)*
The single command drops a self-contained folder: all dependencies bundled (satisfies "install required
dependencies"), no source / bytecode / docstrings (satisfies "only limited required code shared"). Wire
this flow to the **compiled** path, never the source `setup.ps1` path.

## 5. Redeem protocol — bind to first redeemer  *(chosen)*

`POST /agent/redeem` (public, unauthenticated by design — the client holds no credentials):

Request `{ code, device_signing_pubkey, nonce }` →
1. **Rate-limit** by source IP (reuse the `probe_enrollment` limiter pattern).
2. Look up the token by `claim_code_hash = sha256(code)` **`WITH FOR UPDATE`**.
3. If missing / expired / already redeemed / revoked → **opaque 404** (no oracle: every bad input looks
   identical, so the endpoint cannot be used to probe which codes exist).
4. Atomically: mark redeemed, set `bound_fingerprint = sha256(device_signing_pubkey)`, record
   `redeemed_ip` + `redeemed_at`, write an audit row.
5. Return `{ manager_url: <façade>, token: <raw vet_> }` — body only, TLS only.

Enforcement at enrolment: `/probe-enrollment/requests` already takes the `vet_` and the device key. Add a
check — if the token carries `bound_fingerprint`, the enrolling key's fingerprint must equal it, else
reject. Baseline guarantee is still `max_uses=1` (exactly one agent enrols); the fingerprint pin closes
the "code stolen in transit before the real client redeems" window and makes any theft **visible in
Fleet** (unexpected `redeemed_ip`).

## 6. Threats → controls

| Threat | Control | Residual |
|---|---|---|
| Client decodes the code to read manager/token | Code is an opaque pointer; nothing embedded | Façade name observable in traffic (§3) |
| Code stolen from a ticket / shoulder-surf | Single-use + short TTL + bound to first device key; Fleet shows redeemer IP | A thief redeeming *before* the client gets a bound agent, visibly, from a wrong IP |
| Redeem endpoint used as a code oracle | Opaque 404 on every invalid/used/expired code; rate-limited | — |
| Forged codes | No secret in `get.ps1`; codes are server-side random, verified by DB lookup | — |
| Manager real identity leak | Vanity façade fronts bootstrap + enrol + agent channel; real hostname/IP/keys never in the command | Machine owner can sniff outbound (§3) |
| Replay of redeem | Atomic `FOR UPDATE` single-use; `nonce` recorded | — |
| Client ships your source | Compiled standalone — no source/bytecode/docstrings (CI-enforced) | — |

## 7. What is reused vs. built new

* **Reuse:** `ProbeEnrollmentToken`, the full enrolment + refresh protocol, pairing fallback,
  `manager_public_url`, the compiled build, `install.ps1`, the rate-limiter and audit helpers.
* **Build new:**
  * DB: `claim_code_hash`, `bound_fingerprint`, `redeemed_ip`, `redeemed_at` columns on
    `probe_enrollment_token` (one Alembic migration, nullable → backward-compatible).
  * `POST /agent/redeem` (public, hardened) in `agent_distribution.py`.
  * `POST /agent/install-codes` (operator one-click) — mints `vet_` + claim code + returns the one-liner.
  * `bound_fingerprint` check in `/probe-enrollment/requests`.
  * `-Code` branch in the bootstrap (`get.ps1` / `install.ps1`): redeem, keep the token in memory, run
    the compiled install against the façade origin.
  * Fleet: an "Add Windows Agent" button that shows the one-liner with a copy control, and lists / revokes
    outstanding codes.

## 8. Build order

| Step | What | Size | Needs owner |
|---|---|---|---|
| S1 | Migration + model fields (`claim_code_hash`, `bound_fingerprint`, `redeemed_ip`, `redeemed_at`) + unit tests | S | no |
| S2 | `POST /agent/install-codes` (one-click mint) + `POST /agent/redeem` (public, hardened) + tests (opaque-404, single-use race, binding) | M | no |
| S3 | `bound_fingerprint` enforcement in `/probe-enrollment/requests` + test | S | no |
| S4 | Bootstrap `-Code`: redeem → in-memory token → compiled install against façade; token never printed; pester tests | M | no |
| S5 | Vanity domain: Caddy host + `MANAGER_PUBLIC_URL`; verify agent WS/poll works through it | S | **Yes: DNS record + domain** |
| S6 | Fleet "Add Windows Agent" button + code list/revoke | S | no |
| S7 | End-to-end on the Windows CI runner: mint code → paste → agent online; token appears in no log / process list / console | M | no |

Each step that changes shipped agent code bumps `AGENT_VERSION` (CI gate enforces it).

## 9. Open decisions still needed from the owner

1. ~~**The vanity domain**~~ **Resolved (13 Oct): `vedhasec.com`.** Façade `get.vedhasec.com`; remaining is only the subdomain label (`get.` vs `agent.` vs `install.`) and the DNS/Caddy route (S5).
2. **Claim-code lifetime** — mirror the `vet_` TTL (1 h / 24 h / 7 d), or cap shorter since re-minting is one click? Recommend: offer the same three, default 24 h.
3. **Claim-code shape** — human-groupable `VDHA-7K2M-9QXP` (easy to read over a call) vs. opaque `vip_<random>`. Recommend the grouped form; it carries no data either way.

## 10. Test plan (write alongside each step)

* A redeemed code cannot be redeemed again (concurrent `FOR UPDATE` race test).
* An invalid, expired, revoked and never-issued code all return the **same** opaque 404.
* An agent whose device key ≠ `bound_fingerprint` is refused at enrolment.
* The raw `vet_` token appears in **no** console output, log line, scheduled-task definition, or process
  argument list (grep assertion in the E2E).
* The install command string contains no manager IP, no key, and no name other than the façade.
* Full compiled install on the Windows runner reaches `online` in Fleet from the one-liner alone.
