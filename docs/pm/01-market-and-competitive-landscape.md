# 01 · Market & Competitive Landscape

## 1. Category

Vedha lives in **network / infrastructure Vulnerability Assessment & Management (VA / VM)**, at
the intersection of three adjacent motions:

- **Classic VM scanners** — Tenable (Nessus / Tenable.io), Qualys VMDR, Rapid7 InsightVM,
  Greenbone / OpenVAS.
- **Risk-based prioritization & aggregation** — Nucleus Security, Vulcan Cyber, Brinqa
  (ingest many scanners → dedupe → prioritize → route).
- **Delivery model** — increasingly *continuous* and *service-delivered* (MSSPs, VA-as-a-service,
  EASM vendors like Intruder.io).

Vedha is unusual in that it is **both a scanner and a prioritization/lifecycle layer**, purpose-shaped
for **multi-tenant delivery**.

## 2. Market sizing (directional — `[VALIDATE]` before external use)

> These are **framing estimates**, not sourced analyst figures. Replace with real numbers
> (Gartner/IDC/analyst report) before any board or fundraising use.

- **TAM** — global vulnerability management market: **~$15–18B by ~2028** `[VALIDATE]`, growing
  low-double-digit CAGR. Broad and incumbent-dominated.
- **SAM** — the slice Vedha can actually serve near-term: **MSSPs + security consultancies +
  mid-market/OT/regulated network VA**. Directionally **~$2–3B** `[VALIDATE]`.
- **SOM (3-yr, realistic beachhead)** — a few hundred MSSP/consultancy accounts each running many
  engagements. Even **200 accounts × modest per-account ARR** is a credible early business; model
  this bottoms-up in doc 05 rather than top-down.

**Takeaway:** don't sell TAM. The story is a **wedge in a large, unhappy market**, entered through
the buyer who feels the most pain per day (the MSSP), where the architecture is a structural fit.

## 3. Tailwinds (why now)

- **KEV/EPSS adoption** — the industry has moved from "CVSS everything" to "what's actually
  exploited." Vedha's risk_rank is already KEV/EPSS-aware → *with the grain of the market.*
- **Data-sovereignty & supply-chain fear** — regulated, gov, defense, and EU buyers increasingly
  refuse to ship asset+vuln inventory to a vendor cloud. Vedha's trust-boundary split is a direct
  answer.
- **OT/ICS security spend** — active scanning crashing industrial gear is a board-level fear;
  passive-first is now table stakes for OT. Vedha's OT profile is *structurally* passive.
- **Alert fatigue / analyst scarcity** — the constraint is analyst hours, not scan coverage.
  Anything that removes false positives and prioritizes credibly sells itself.
- **MSSP consolidation & growth** — MSSPs are scaling and need infrastructure that multiplies
  analyst leverage across clients.

## 4. Headwinds (honest)

- **Incumbent gravity & trust** — Nessus is the default noun for "vuln scan." New scanners face
  "prove your accuracy" skepticism.
- **Coverage expectations** — buyers expect authenticated scanning, web/app, cloud/container.
  Vedha is network-first and authenticated collection is not yet shipping (see doc 04).
- **Compliance checkbox** — many buyers pick whatever their auditor recognizes. Framework mapping
  matters more than technical elegance for that buyer.
- **"Agentic" fatigue** — the word is overused; it earns an eye-roll, not a demo, unless backed by
  a concrete outcome.

## 5. Competitive matrix

Legend: ✅ strong · ➖ partial / adjacent · ❌ weak-absent · ❓ unverified

| Capability | **Vedha** | Nessus / Tenable | Qualys VMDR | Rapid7 InsightVM | OpenVAS / Greenbone | Nucleus / Vulcan |
|---|---|---|---|---|---|---|
| Network/infra scanning | ✅ 13 collectors | ✅ | ✅ | ✅ | ✅ | ❌ (aggregators) |
| **Vuln DB never enters client net** | ✅ **by design** | ❌ (scanner holds it) | ➖ (cloud agents) | ➖ | ❌ | n/a |
| **Re-detect w/o re-scan (facts stored)** | ✅ **differentiator** | ❌ | ➖ | ➖ | ❌ | ➖ (re-scores ingested data) |
| Anti-FP: calibrated confidence + evidence + N-run consistency | ✅ **differentiator** | ➖ | ➖ | ➖ | ❌ | ➖ |
| Explainable KEV/EPSS risk score | ✅ 0–1000 explainable | ✅ VPR | ✅ TruRisk | ✅ RealRisk | ❌ | ✅ |
| Posture / patch-comparison over time | ✅ | ✅ | ✅ | ✅ | ➖ | ✅ |
| Finding lifecycle (auto-resolve/reopen/regression) | ✅ recent | ✅ | ✅ | ✅ | ➖ | ✅ |
| OT passive-only mode | ✅ structural | ➖ (Tenable OT sep. product) | ➖ | ➖ | ❌ | ❌ |
| Authenticated / credentialed scan | ❌ **gap** | ✅ | ✅ | ✅ | ✅ | n/a |
| Web-app / API / cloud (CSPM) scanning | ❌ out of scope today | ➖/sep. | ✅ | ➖ | ➖ | ➖ (ingests) |
| Multi-tenant + per-client portal | ✅ (portal WIP) | ➖ (Tenable.io) | ➖ | ➖ | ❌ | ➖ |
| Local-first / self-hostable AI | ✅ | ❌ | ❌ | ❌ | ✅ (no AI) | ➖ |
| Compliance framework mapping | ❌ **gap** | ✅ | ✅ | ✅ | ➖ | ✅ |
| Brand / trust / install base | ❌ new | ✅✅ | ✅✅ | ✅ | ✅ | ✅ |

## 6. Where Vedha wins vs. loses

**Wins when the buyer cares about:** deploying into networks they don't fully own (MSSP,
consultant, OT), data sovereignty, false-positive fatigue, fast response to new CVEs without
re-scanning, and multi-client delivery economics.

**Loses when the buyer wants:** a single-vendor "scan everything incl. web/cloud/authenticated,"
an auditor-recognized brand for a compliance checkbox, or the safety of the market-default name.

## 7. Moats (defensibility ranked)

1. **Architectural (hard to copy):** trust-boundary split + facts-first re-detection. An incumbent
   whose scanner *is* the database can't casually flip to this.
2. **Accuracy/trust (compounding, if proven):** the anti-FP verification stack + a *published*
   precision/recall number becomes a reputation moat.
3. **MSSP workflow lock-in (once portal ships):** per-engagement portals, lifecycle, and reporting
   embed Vedha in the MSSP's own delivery — high switching cost.
4. **Weakest today:** brand, coverage breadth, ecosystem/integrations. These are execution items,
   not structural — see doc 04.
