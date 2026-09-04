# Vedha — Pending Work

**Compiled:** 2026-08-17 · **Purpose:** single source of truth for what is planned
but **not yet done**, reconciled against the design docs, the scanner roadmaps
(`probe/main_scripts/plan.md`, `RESEARCH_IMPROVEMENTS.md`), and the work delivered
in recent sessions. This is a **documentation-only** inventory — nothing here is
started.

Legend: ✅ done · ⚠️ partial · ❌ not started · 🔎 verify (docs may be stale).
Priority ★ (low) → ★★★ (high) where a source rated it.

---

## 0. Done recently (context — NOT pending)
So the pending list reads honestly, these landed in recent sessions:
- **Customer portal — 6 items:** password reveal/copy, one-click probe approval,
  editable SLA policy, integrations config + delivery worker + "Send test",
  customer-scans request flow, session-clock removal.
- **Remediation AI subsystem** + hardening (ON-CONFLICT upsert, review-gate reset,
  os_key public, prompt-injection framing). Backend complete.
- **Scanner:** OPSEC de-sign (no brand strings on the wire), `--source-port`
  evasion, `os_fingerprint` wrong-host-TTL bugfix + MSS→MTU/link intel.
- **Installer:** LOCAL preflight + self-healing venv + daemon/lock guards; portability
  (default-route iface, arch warning, `--mac-address` diagnosis), `PROBE_IMAGE_SHA256`,
  startup poll, `--uninstall`.
- **Autonomous agent:** Phase-0 **policy engine** (`services/agent_policy.py`) only.

---

## A. Scanner — accuracy roadmap
Source: `probe/main_scripts/RESEARCH_IMPROVEMENTS.md` (items 1–3 ✅ 2026-08-15).

| # | Item | Files | Effort | Impact | Status |
|---|------|-------|:---:|:---:|:---:|
| A4 | **Ground-truth corpus + `accuracy.py` in CI** (harness is unit-tested but has no real lab corpus / merge gate) | new corpus, CI | M | ★★★ | ❌ (was "next") |
| A5 | **AIMD congestion control into TCP paths** + pace SYN sends (today only `udp_scanner` uses AIMD; constant rate → false `filtered` under loss) | scanner_base, port_scanner, syn_scanner | M | ★★★ | ❌ |
| A6 | **Harvest TCP window/MSS → feed `os_fingerprint`** (SYN path harvests MSS; the **connect-scan window/`TCP_INFO` harvest** that lifts OS-ID to p0f-class is not wired) | port_scanner, scan_funnel, os_fingerprint | M | ★★ | ⚠️ partial |
| A7 | **Expand service/version ID** (curated nmap-service-probes subset for top ~200) + **TLS-wrap probe rung** (443/8443 currently get a plaintext GET → "open, no banner") | service_banner | M/L | ★★★ | ❌ |
| A8 | **`select`/epoll SYN receive** (today busy-polls with `sleep(0.005)`; can drop replies under bursts) | syn_scanner | S | ★★ | ❌ |
| A9 | **`resolve()` multi-family fallback** (uses only `getaddrinfo()[0]`; dual-stack v6-first-but-unreachable won't fall back to v4) | scanner_base | XS | ★ | ❌ |
| A10 | **Pace SYN sends** (send loop bursts a whole target; `/24 × top1000` trips RFC-1812 ICMP limits → drops) — folds into A5 | syn_scanner | — | ★★ | ❌ |
| A11 | Robustness: `RateLimiter` single-lock bottleneck (4.2), `expand_targets` full-list materialization (4.3), SMB framing edge fixtures (4.4) | scanner_base, smb_scanner | S | ★ | ❌ |

---

## B. Scanner — coverage / new protocol scanners
Source: `probe/main_scripts/plan.md`.

- **B1 — Service-banner → protocol-scanner handoff** (Step 18, ⚠️ partial): the
  routing table in `scan_funnel.py` isn't exhaustive; 445/3389/135 aren't auto-handed
  to their protocol scanner from `service_banner` itself.
- **B2 — RDP X.224 handshake scanner** (Step 19, ❌ / 🔎): plan says none exists, but
  `rdp_scanner.py` (141 LoC) is present — **reconcile**: confirm it does the X.224
  Connection-Request → `NEG_RSP` security-layer read (TLS/CredSSP/NLA), or finish it.
- **B3 — MSRPC / EPM endpoint mapper** (Step 20, ❌): TCP/135 is found open but no
  DCE/RPC EPM bind + endpoint enumeration exists (read-only).

---

## C. Scanner — offensive / OPSEC (from the offensive-security review)
- **C1 — Evasion #2b: timing jitter + randomized scan order** (❌, was the next
  subtask — paused): `--scan-delay` + jitter, shuffled host×port order.
- **C2 — Evasion #2c: fragmentation + decoys** (❌, deferred; raw-path, higher risk —
  own subtask).
- **C3 — "Unauthenticated/exposed admin dashboard" finding rule** (❌): `web_scanner`
  fingerprints Grafana/Kibana/Jenkins but no `findings` rule emits the exposure
  (highest-value web foothold class). Likely needs `web_scanner` to record auth-state.
- **C4 — IPv6 SYN + ICMP paths** (❌): `syn_scanner` and `os_fingerprint` ICMP are
  IPv4-only → dual-stack estates hide half their surface.
- **C5 — Tarpit / honeypot detection heuristic** (❌): "N>threshold open ports ⇒ likely
  tarpit/IDS, down-weight" — protects accuracy and operator time.
- **C6 — `service_enum.py` UA de-sign** (❌): the last brand string on the wire
  (`User-Agent: service_enum`, line ~477) — one-liner: add `user_agent` to its
  `scanner_base` import + swap the literal (the other 6 modules are done).
- **C7 — `os_fingerprint` queued probes** (❌): (a) send the **ICMP timestamp** probe
  (built, never sent → new intel + a real finding); (b) **address-mask** probe (subnet
  leak); (c) **OS granularity** refinement (macOS/BSD/Windows-version via window+MSS+banner).

---

## D. Autonomous Engagement Agent
Source: `docs/superpowers/specs/2026-08-16-vedha-autonomous-engagement-agent-design.md`
(§7 roadmap) + `docs/superpowers/plans/2026-08-16-agent-policy-engine.md`.
**Only the Phase-0 policy engine is built.**

- **D0 — Rest of Phase 0** (❌): persist Rules-of-Engagement (model + migration),
  kill-switch endpoints + agent-run state, security-RAG index, audit/timeline wiring.
- **D1 — Phase 1** (❌): attack-tree **planner** + external **memory**; auto-authorize
  Tier 0/1; validator loop for scan findings.
- **D2 — Phase 2** (❌): gated **exploitation** — executor drives the exploit engine via
  the existing approval gate (human-approved); planner/executor/critic split.
- **D3 — Phase 3** (❌): bounded **full autonomy** (Tier-2 auto within RoE; Tier-3 always
  human); continuous engagements via the outbox.
- **D4 — Phase 4** (❌): **learning loop** — feed verified outcomes back into RAG/memory.
- **D-decisions (§9, unresolved):** exploit-generation policy (deterministic-only vs
  sandboxed LLM payloads), autonomy ceiling, planner model (Opus vs pinned Sonnet),
  single- vs multi-agent.

---

## E. Probe installer (`probe/install.sh`) — deferred improvements
Source: installer review. (Fixes + safe improvements already shipped.)
- **E1 — Pin + hash pip deps** (❌, ★★ security): `requirements-runtime.txt` uses `>=`;
  move to exact versions + `--require-hashes` (needs `pip-compile` + a test run).
- **E2 — True `--mac-address` fallback** (❌): a MAC-independent enrollment path for
  rootless/Docker-Desktop (currently fails fast with a clear message). Needs an
  `agent/hw_bind.py` redesign.
- **E3 — Container healthcheck** (`--health-cmd`) so a *hung* probe is visible.
- **E4 — LOCAL persistence** (systemd unit / launchd plist) + an in-place image
  **upgrade** flow that preserves identity.

---

## F. Product / portal
- **F1 — Remediation portal view** (❌ frontend): the customer finding view should render
  the structured step-by-step plan (design §6). Backend route exists; the frontend
  consumer is unverified/unwired. 🔎
- **F2 — Notification event triggers** (❌): the delivery worker + `POST /integrations/test`
  exist, but nothing calls `enqueue_notification` on real events (new critical finding,
  SLA-at-risk/breach, report approved). Wire the producers.
- **F3 — User-portal Spec 2: incident IDs** (❌, deferred): per the roadmap/memory.
- **F4 — #2 customer-scans card-parity** (❌, cosmetic): port the operator scanner's
  use-case card catalog to the portal (functionally complete without it).
- **F5 — #5 connected-probe margin** (❌): visual QA fix on the fleet page (needs a
  running UI; can't be judged headless).

---

## G. Operational / housekeeping
- **G1 — Apply migrations** `0029` (portal_password_enc), `0030` (sla_policies),
  `0031` (integrations) on any deployed env: `alembic upgrade head` (or `make migrate`).
- **G2 — Push installer commits** `9e188b8` + `2be040c` to `integration/all-branches`
  (currently local-only).
- **G3 — Commit hygiene:** `fbe7450 "Add comprehensive documentation for Playwright CLI
  features"` bundled the remediation hardening + `probe/.claude/` under a misleading
  message — reword/split if the history matters.
- **G4 — Branch cleanup:** many stale local branches; everything lives on
  `integration/all-branches` — delete/ignore the rest.

---

## Suggested next-up (by leverage)
1. **A4** ground-truth corpus + CI gate — turns "accurate" into a measured number and
   tells you which of A5–A9 to do next (data-driven).
2. **C6** service_enum UA de-sign (2-minute completion of the OPSEC sweep) + **C1**
   timing jitter (the paused evasion subtask).
3. **F2** notification triggers (small; makes the shipped delivery worker actually fire).
4. **D0** finish Phase-0 safety rails before any agent autonomy.
