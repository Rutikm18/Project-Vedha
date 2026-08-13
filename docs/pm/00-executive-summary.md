# 00 · Executive Summary

## What Vedha is (one breath)

An **agentic network vulnerability-assessment platform** split by trust boundary: a *thin* probe
that runs inside the client network and does collection **only** (dials out, holds no vuln DB, no
inbound ports), and a *fat* multi-tenant cloud manager that turns raw facts into verified,
prioritized, lifecycle-managed findings. Detection is deterministic and offline; AI is local-first
and optional. Currently v1.0.45.

## The strategic read

Vedha is a *good scanner* wrapped around **three architectural bets that most incumbents cannot
easily copy** because they'd have to re-architect:

1. **Trust-boundary split** — the vuln DB and all client data stay in the cloud manager; the probe
   is a disposable dial-out-only collector. This is exactly the shape an **MSSP or consultancy**
   needs to drop into 50 client networks, and exactly what a **regulated / OT / air-gapped-ish**
   buyer needs to trust.
2. **Facts-first re-detection** — the probe ships *raw facts*, not verdicts. Detection re-runs
   against a newer pinned CVE DB **without re-scanning the network**. (The "log4shell Monday"
   story: answer "am I exposed?" across every past scan in minutes, no re-scan.)
3. **Anti-false-positive by construction** — every finding carries a calibrated `confidence`, an
   evidence tier, an audit of checks, and an N-run consistency score (Wilson CI); the verifier
   *only ever lowers* certainty. This attacks the #1 reason people distrust and abandon scanners.

On top of those sit the features that make it *sellable today*: **explainable 0–1000 risk_rank**
(KEV/EPSS-aware), **posture + patch-comparison scorecards** (board-ready "are we getting
better?"), **finding lifecycle** (auto-resolution, reopen, regression flagging), and an
**OT passive-only profile** that structurally cannot fire an active packet at a PLC.

## The recommended wedge

> **Sell Vedha first as the VA delivery engine for MSSPs & security consultancies**, with
> **data-sovereign / OT** as the strong secondary message.

Why this beachhead: the probe/manager split, multi-tenancy, engagement model, and (in-progress)
per-engagement customer portal are *already* MSSP-shaped. MSSPs feel the deployment,
multi-tenant, false-positive, and per-client-reporting pains **all at once and daily**, and they
buy infrastructure that lets them serve more clients per analyst. That is a sharper, faster-closing
market than trying to unseat Tenable/Qualys inside a single enterprise.

## Top 3 USPs to actually sell (mapped to pain)

| USP | The pain it kills | The line |
|-----|-------------------|----------|
| **The vuln DB never enters the client network** | "I can't put a scanning appliance with a CVE database inside my client's / OT segment." | *"Drop a dial-out-only probe. No inbound ports, no database, nothing to breach — the intelligence stays in your cloud."* |
| **Re-detect without re-scanning** | "A new critical CVE dropped — do I re-scan 40 clients tonight?" | *"New CVE at 9am? Re-run detection against every past scan by 9:15 — zero new packets."* |
| **Findings are anti-FP by construction** | "My scanner cries wolf; my analysts stopped trusting it." | *"Every finding ships with calibrated confidence, evidence, and a cross-run stability score. We only ever lower certainty — never inflate it."* |

Full USP set with objection handling: [`03-usps-and-value-proposition.md`](./03-usps-and-value-proposition.md).

## Top 5 improvements (why they matter — full detail in doc 04)

1. **Ship authenticated/credentialed collection** (via the ephemeral secret broker already
   scoped in ARCHITECTURE §7/§10). *Why:* unauthenticated-only caps detection accuracy and is the
   first objection every enterprise buyer raises. **Highest-leverage gap.**
2. **Encrypt probe identity at rest (KMS/keyring envelope key).** *Why:* you sell trust; "we rely
   on you to encrypt the disk" is a weak answer in a security RFP. (ARCHITECTURE §10, open.)
3. **Add compliance-framework mapping to findings & reports** (PCI/ISO 27001/SOC 2/NIST 800-53).
   *Why:* compliance is the budget line that funds VA; it also upgrades the report from artifact to
   *deliverable* for MSSPs.
4. **Finish the per-engagement customer portal** (user→engagement scoping). *Why:* it's the MSSP
   monetization and stickiness wedge and it's already the #2 roadmap item.
5. **Publish an accuracy benchmark** (precision/recall vs Nessus/OpenVAS on a known corpus). *Why:*
   the anti-FP claim is your moat — *prove it* and it becomes a sales weapon, not a promise. The
   precision/recall harness already exists; turn it into a public number.

## The single biggest risk

**Positioning drift.** "Agentic VA platform" is broad and undifferentiated on a homepage. The
architecture is genuinely differentiated; the *words* aren't yet. Pick the MSSP/data-sovereign
wedge, lead with the three USPs above, and prove the anti-FP claim with a number. Everything else
is execution.
