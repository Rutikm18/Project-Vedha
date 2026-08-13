# 02 · Customer Personas & Pain Points

> Method: for each persona — **who they are**, their **job-to-be-done (JTBD)**, the **pains that
> keep them up**, and **how Vedha's shipping capabilities map to those pains**. Personas are ranked
> by fit-to-Vedha-today. Pains are written in the customer's voice.

---

## Persona A — MSSP / VA-as-a-service provider **(primary ICP — best fit)**

**Who:** a managed security firm running vulnerability assessment for 10–200+ client orgs. Buyers:
Head of Delivery / SOC Manager / vCISO practice lead. Economic buyer cares about **analyst hours
per client** and **clients per platform seat**.

**JTBD:** *"Let me stand up VA for a new client this week, run it safely inside their network, and
hand back a credible, branded report every month — without hiring an analyst per client."*

**Pains (their words):**
- *"Dropping a scanning appliance loaded with a CVE database into a client's network is a hard
  sell and a liability."*
- *"Every client is a tenant — I need isolation, per-client logins, per-client reports, and I need
  it to not be a spreadsheet."*
- *"Half my analyst time is triaging false positives I then have to apologize for."*
- *"When a big CVE drops, my clients email me in an hour. Re-scanning 40 networks is a nightmare."*
- *"My report has to look like *my* product, not a vendor PDF."*

**Vedha fit (today):** trust-boundary probe (dial-out only, no DB) ✅ · multi-tenant + engagement
model ✅ · per-engagement customer portal ✅ (WIP) · anti-FP verification ✅ · re-detect w/o re-scan
✅ · posture/patch reports ✅. **This persona feels ~all of Vedha's USPs at once.**

**Gap that blocks the deal:** authenticated scanning (clients expect it), report branding/compliance
mapping, portal completion. → doc 04 items #1, #3, #4.

**Willingness to pay:** high and recurring — it's cost-of-goods for their service. Price on
**per-engagement / per-active-probe / tiered client count**.

---

## Persona B — Security consultancy / pentest & VA firm **(strong secondary)**

**Who:** boutique-to-mid offensive/assessment shop. Buyer: practice lead / principal consultant.

**JTBD:** *"Ship me into a client engagement, let me scan safely within a tight scope, and
generate the deliverable — fast, defensible, repeatable."*

**Pains:**
- *"Scope creep = liability. I need a hard allowlist I can prove I honored."*
- *"I need a professional deliverable, not raw scanner output."*
- *"Re-tests should not mean re-doing the whole engagement."*

**Vedha fit:** dual-enforced ScopeGuard hard allowlist (manager **and** probe refuse out-of-scope)
✅ — this is a *compliance/defensibility* feature consultants will love · engagement model ✅ ·
AI report + posture ✅ · re-detect for re-tests ✅.

**Willingness to pay:** medium-high, per-engagement or annual seat. Fast sales cycle (practitioners
buy tools they like).

---

## Persona C — OT / ICS / critical-infrastructure security team **(high-value niche)**

**Who:** manufacturing, utilities, energy, healthcare biomed. Buyer: OT security lead / plant
security engineer, usually *terrified* of downtime.

**JTBD:** *"Give me visibility into vulnerabilities on my OT segment without ever risking a device
crash or a plant stop."*

**Pains:**
- *"Active scanning has crashed PLCs before. IT tools are banned on my network."*
- *"I can't send my asset inventory to someone's cloud."*
- *"My IT vuln scanner doesn't understand my environment or my constraints."*

**Vedha fit:** OT profile is **structurally passive-only on both ends** ✅ · probe holds no DB and
dials out only ✅ · local-first AI (data stays put) ✅. This is a *fear-driven* buyer — the passive
guarantee and the no-DB-in-network story are the whole sale.

**Willingness to pay:** high (downtime is catastrophic) but **long sales cycle** and heavy proof
burden. Great logo/reference market, not a fast-revenue beachhead.

---

## Persona D — Internal security team, regulated / data-sovereign enterprise **(opportunistic)**

**Who:** mid-market/enterprise in finance, healthcare, gov, defense supply chain. Buyer: security
engineering lead / CISO.

**JTBD:** *"Run continuous VA across my segmented network, prove to auditors I'm improving, and
keep the data in my control."*

**Pains:**
- *"Compliance says quarterly scans; my board asks 'are we getting better?' and I have no clean
  answer."*
- *"I have 12,000 open findings and no credible way to say which 50 matter."*
- *"SaaS scanners want my whole asset inventory in their cloud."*

**Vedha fit:** posture + patch-comparison scorecard (board-ready trend) ✅ · explainable 0–1000
risk_rank, KEV/EPSS-aware ✅ · self-hostable manager + local AI ✅ · finding lifecycle ✅.

**Gap that blocks the deal:** compliance framework mapping, authenticated scan, brand trust.
→ doc 04. This persona is where you *lose to Nessus/Qualys* on brand+coverage today; enter it via
the data-sovereignty and prioritization angles, not head-on.

---

## Cross-persona pain → capability map (the whole story on one screen)

| Universal VA pain | Who feels it most | Vedha's answer (shipping) | Doc-03 USP |
|---|---|---|---|
| Can't put a scanner+DB inside the network | MSSP, OT, consultant | Dial-out-only probe, DB stays in cloud | **USP-1** |
| New CVE → must re-scan everything | MSSP, enterprise | Facts stored → re-detect, no re-scan | **USP-2** |
| False positives destroy trust & analyst time | everyone | Calibrated confidence + evidence + N-run Wilson-CI consistency | **USP-3** |
| "Which of 10,000 do I fix first?" | enterprise, MSSP | Explainable 0–1000 risk_rank (KEV/EPSS) | **USP-4** |
| "Are we getting better?" (board) | enterprise, MSSP | Posture + patch-comparison scorecard | **USP-5** |
| Active scan will crash my OT | OT/ICS | Structurally passive OT profile | **USP-6** |
| Don't send my vulns to a vendor cloud | regulated, OT | Self-host + local-first AI | **USP-7** |
| Serving many clients doesn't scale | MSSP | Multi-tenant + engagement + per-client portal | **USP-8** |

**Read this way:** Vedha doesn't have one killer feature — it has a **pain cluster that all resolves
to the same architecture**, and the MSSP is the persona standing in the middle of that cluster.
That's why the MSSP is the wedge (doc 05).
