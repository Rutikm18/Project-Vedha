# 04 · Product Improvement Roadmap

> **Areas of improvement — with WHY (business reason) and HOW (concrete path).** Prioritized by
> **impact ÷ effort** and grouped **Now / Next / Later**. "Now" = unblocks revenue or de-risks the
> core promise. Grounded in the codebase; open items reference `ARCHITECTURE.md` §7/§10 and memory.

## Scoring key

- **Impact:** ●●●● deal-maker · ●●● meaningful · ●● nice-to-have
- **Effort:** ▲ small · ▲▲ medium · ▲▲▲ large
- **Type:** `PROD` product/eng · `TRUST` security/credibility · `GTM` market/positioning

---

## NOW — unblock revenue & protect the core promise (next 1–2 cycles)

### N1 · Ship authenticated / credentialed collection — Impact ●●●● · Effort ▲▲▲ · `PROD`
- **Why:** unauthenticated-only caps detection accuracy (misses installed-package/patch-level and
  config vulns) and is the **first objection every enterprise & MSSP buyer raises**. It's the single
  biggest gap between Vedha and Nessus/Qualys on coverage.
- **How:** build the **ephemeral secret broker** already scoped in `ARCHITECTURE.md` §7/§10 — deliver
  secrets to the probe at job time, never persist them in `scan_jobs` (the current reject-credentials
  invariant stays). Start with SSH/WinRM/SNMP-authenticated checks for the top OS families.
- **Proof of done:** authenticated Linux patch-level detection with measured precision/recall lift.

### N2 · Encrypt probe identity/token at rest (KMS/keyring envelope key) — Impact ●●● · Effort ▲▲ · `TRUST`
- **Why:** you *sell trust*. "We rely on you to encrypt the host disk" (current state, ARCHITECTURE
  §10 open) is a losing answer in a security RFP and undercuts USP-1.
- **How:** OS keyring / KMS-backed envelope key for the probe identity token; fall back to
  disk-encryption requirement only where no KMS exists. Closes the ARCHITECTURE §10 ⬜ item.

### N3 · Publish an accuracy benchmark (precision/recall vs Nessus/OpenVAS) — Impact ●●●● · Effort ▲▲ · `GTM`
- **Why:** the **anti-FP claim (USP-3) is the moat — but a claim, not a number, doesn't close.** A
  published metric converts your best differentiator into a sales weapon and a content flywheel.
- **How:** the precision/recall harness + dpkg cross-validation already exist (ARCHITECTURE §8). Run
  it against a labeled corpus, write it up, put a number on the homepage. Low new-code, high leverage.

### N4 · Compliance-framework mapping on findings & reports — Impact ●●●● · Effort ▲▲ · `PROD`+`GTM`
- **Why:** compliance is the **budget line that funds VA**. Mapping findings to PCI-DSS / ISO 27001 /
  SOC 2 / NIST 800-53 upgrades the report from "artifact" to "audit deliverable," and for MSSPs it's
  a billable value-add.
- **How:** a mapping layer over findings (CVE/CWE → control IDs) + a report section; start with the
  two frameworks your target buyers name most.

### N5 · Finish the per-engagement customer portal (user→engagement scoping) — Impact ●●●● · Effort ▲▲▲ · `PROD`
- **Why:** it's the **MSSP monetization + stickiness wedge** and already the #2 roadmap item; without
  it, MSSPs bolt their own portal on and switching cost stays low.
- **How:** per the locked pre-decisions in memory — `assigned_agent_id` FK on `Engagement`,
  per-engagement customer credentials, and the missing **user→engagement scoping** so a customer sees
  only their engagement (findings, posture, report, SLA, AI assist). This is the key architectural lift.

---

## NEXT — widen the wedge (following cycle)

### X1 · Single-binary field probe (revive `spike/probe-go`) — Impact ●●● · Effort ▲▲▲ · `PROD`+`TRUST`
- **Why:** the Python probe needs `.venv`/pip in the field; a single static binary is a **materially
  better deployment story** (no runtime, smaller attack surface) — exactly what MSSP field ops and OT
  environments want. Memory flags Go as the better long-term field artifact.
- **How:** bring `spike/probe-go` to capability + security-gate parity (per its README), then make it
  the field artifact while Python stays the dev/reference path.

### X2 · Self-serve PAT / credential management UI — Impact ●● · Effort ▲ · `PROD`
- **Why:** PATs currently have **no dashboard UI** (memory: only SMTP/Slack/Jira/SLA/Notifications in
  settings); operators can't self-serve probe tokens → onboarding friction + support load.
- **How:** add a Tokens section to `settings/page.tsx` over the existing `/auth` PAT endpoints
  (mint/list/revoke, `vpat_`-prefixed). Small, high-DX-return.

### X3 · Closed-loop remediation & SLA workflow depth — Impact ●●● · Effort ▲▲ · `PROD`
- **Why:** buyers want **detection → owner → fix → verified-closed**, not just detection. The recent
  lifecycle work (auto-resolution, reopen, regression-flagging) is the right spine — extend it into
  ownership/assignment, SLA timers, and remediation-verification so the loop visibly closes.
- **How:** build on the resolution-lifecycle columns + coverage ledger already shipped; add assignment
  + SLA state to findings and surface "verified fixed vs regressed" in the portal/report.

### X4 · Integration breadth (SIEM / SOAR / ITSM / webhooks) — Impact ●●● · Effort ▲▲ · `PROD`
- **Why:** Slack/Jira/Email is a start; enterprise & MSSP buyers expect ServiceNow, Splunk/SIEM,
  Teams, and a **first-class outbound webhook + API** to fit existing workflows. Integrations are
  switching-cost and RFP checkboxes.
- **How:** generalize the existing notification dispatch points (SLA breach / new critical / report
  ready) into a pluggable event→destination bus; ship webhook + one ITSM + one SIEM first.

### X5 · Asset business-context / criticality tagging — Impact ●●● · Effort ▲▲ · `PROD`
- **Why:** `risk_rank` scores *technical* exploitability; real prioritization is
  **exploitability × business impact**. Without crown-jewel/asset-criticality context, you're giving
  half the answer, and it's where Vulcan/Nucleus differentiate.
- **How:** asset tags/criticality + ownership on the `assets` model; feed criticality into `risk_rank`
  as an explainable factor (keeps USP-4's "shows its work" promise).

---

## LATER — expand surface / strategic bets (validate demand first)

### L1 · Coverage expansion: web-app / API / cloud (CSPM) — Impact ●●● · Effort ▲▲▲ · `PROD`
- **Why / caution:** buyers increasingly want unified exposure — **but** this is a large scope
  expansion that dilutes the "network VA done right" focus. **Decide deliberately:** integrate/ingest
  (stay focused) vs. build (become a suite). Recommend *integrate first*, build only on proven demand.

### L2 · Continuous / scheduled assessment & drift alerting — Impact ●●● · Effort ▲▲ · `PROD`
- **Why:** the market is drifting from point-in-time scans to continuous monitoring/EASM. Vedha's
  facts-first model is well-suited (cheap re-detection). Turn scans into a schedule + change alerts.

### L3 · Probe fleet management at scale — Impact ●●● · Effort ▲▲ · `PROD`
- **Why:** an MSSP with 100 probes needs fleet health, versioning, and bulk ops. The enrollment/fleet
  work in progress (pre-auth enrollment token, `fleet run`) is the seed; grow it into a fleet console.

### L4 · Published throughput/scale numbers — Impact ●● · Effort ▲ · `GTM`
- **Why:** MSSP buyers ask "how many hosts per probe / concurrent engagements?" A benchmarked answer
  removes a late-stage stall.

---

## Non-product improvements (positioning & DX — cheap, high-return)

- **P1 · Fix positioning drift (`GTM`, ▲):** the homepage/README says "Agentic VA Scanner"; the *value*
  is the trust-boundary + anti-FP + re-detection story. Rewrite the top-of-funnel around the 3
  messaging pillars (doc 03). Nearly free, disproportionate impact.
- **P2 · Harden defaults (`TRUST`, ▲):** memory notes the live `.env` still ships default
  `SEED_ADMIN_PASSWORD=ChangeMe123!` (caught by `make doctor`). For a *security* product, insecure
  defaults are a credibility own-goal — force a secret at first boot.
- **P3 · Time-to-first-finding as the activation metric (`GTM`/`PROD`, ▲):** instrument "probe
  deployed → first verified finding." It's the number that predicts MSSP activation; optimize it.

---

## The prioritization in one line

> **Do N1–N5 now** — they either unlock the enterprise/MSSP deal (auth scan, portal, compliance) or
> *prove* the promise you already deliver (benchmark, at-rest encryption). Everything in Next/Later
> widens a wedge you haven't fully driven in yet.
