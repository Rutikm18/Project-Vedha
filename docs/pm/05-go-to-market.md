# 05 · Go-to-Market

> Turns the analysis into a plan: **who to sell to first, how to package/price, what proof to build,
> and a 90-day sequence.** Hypotheses are labeled `[HYP]` — validate with 10 customer conversations
> before betting the roadmap on them.

## 1. Beachhead: land with MSSPs & consultancies

**Why this wedge (recap from doc 00/02):** the MSSP/consultancy feels *all* of Vedha's USPs at once
and daily, buys VA infrastructure as cost-of-goods, has a fast practitioner-led sales cycle, and is a
**channel** — one MSSP puts Vedha in front of dozens of end-customers. Data-sovereign/OT is the
strong secondary message and the reference-logo market, not the fast-revenue entry.

**Sequence:** `Consultancies (fastest to close)` → `MSSPs (highest LTV + channel)` →
`Data-sovereign/OT enterprise (reference logos, slow)`.

## 2. Ideal Customer Profile (early)

- MSSP or VA/pentest consultancy, **5–50 person** security practice.
- Runs VA for **10+ client networks**; deploys collectors into networks they don't own.
- Feels false-positive pain and per-client reporting overhead **today**.
- Has ≥1 client with **OT or data-sovereignty** constraints (where incumbents struggle) — your
  wedge-within-the-wedge.

## 3. Value narrative per buyer (what to actually say)

| Buyer | Lead line | Close line |
|---|---|---|
| MSSP Head of Delivery | "Serve more clients per analyst." | "Dial-out probe, multi-tenant, per-client portal, anti-FP findings — your VA line of business as a product." |
| Consultancy principal | "Scope-safe, defensible, fast deliverables." | "Hard allowlist enforced twice, professional report, re-test without re-doing the engagement." |
| OT security lead | "Visibility without touching the plant." | "Structurally passive, no database in your network, nothing leaves your perimeter." |

## 4. Packaging & pricing hypotheses `[HYP]`

Pricing should track the **unit of value = an engagement / an active probe / a client tenant**, not
raw asset counts (asset-based pricing is incumbent turf and a race to the bottom).

| Tier | For | Meter `[HYP]` | Notes |
|---|---|---|---|
| **Consultant** | boutique firms | per active probe / per engagement | low entry, land-and-expand |
| **MSSP** | managed providers | per client tenant, volume-tiered | includes portal + branding; the core motion |
| **Enterprise / Sovereign** | regulated, OT | annual, self-hosted, support SLA | premium for on-prem + compliance mapping |

**Principle:** price the *outcome the MSSP resells*, and let their client count (not their scan
volume) drive expansion — it aligns your revenue with their growth and rewards, not penalizes, scale.

## 5. Proof assets to build (in priority order)

1. **The accuracy benchmark** (doc 04 · N3) — precision/recall vs Nessus/OpenVAS. *Your single most
   important GTM artifact.* Turns USP-3 from claim to fact.
2. **"10-minute probe" demo** — deploy a dial-out probe, get a verified finding, kill it. Proves
   USP-1 + low activation friction viscerally.
3. **"Log4Shell Monday" story** — a scripted demo of re-detecting a brand-new CVE across past scans
   with zero re-scan. Proves USP-2.
4. **A real branded MSSP report** (posture + patch-comparison + risk_rank) — the deliverable the MSSP
   will resell. Proves USP-5 + USP-8.

## 6. Channels

- **Practitioner-led (primary):** the people who run scans choose tools. Get the probe in their hands
  (free tier / open-core probe `[HYP]`), win on the demo, expand to the org.
- **Community & content:** publish the benchmark + detection methodology; the security community
  rewards accuracy transparency and punishes marketing fluff. This is how an unknown brand earns trust.
- **MSSP partnerships:** each MSSP is a distribution multiplier — co-branded portal, revenue share.
- **Not yet:** enterprise field sales / analyst-relations (expensive, slow; earn the logos first).

## 7. Activation & north-star metrics

- **North star:** *verified findings delivered through Vedha per week* (usage of the thing that
  creates value — not seats).
- **Activation:** **time-to-first-verified-finding** after probe deploy (doc 04 · P3). Instrument and
  drive it down; it predicts MSSP retention.
- **Expansion:** client tenants per MSSP account over time.
- **Trust proxy:** false-positive rate reported by customers (should trend to near-zero — and if it
  does, that *is* the marketing).

## 8. 90-day plan (concrete)

**Days 0–30 — sharpen & prove**
- Rewrite top-of-funnel around the 3 messaging pillars (doc 04 · P1). Kill "Agentic VA Scanner" as the
  lead; lead with the trust-boundary + anti-FP + re-detect story.
- Run and publish the **accuracy benchmark** (N3).
- Harden insecure defaults (doc 04 · P2) — table stakes for a security brand.
- 10 discovery calls with MSSPs/consultancies to validate pricing `[HYP]` and the auth-scan objection.

**Days 30–60 — unblock the deal**
- Ship **authenticated collection** MVP via the ephemeral broker (N1) — kills the #1 objection.
- Ship **compliance mapping** for the two most-named frameworks (N4).
- Build the **10-minute probe** and **branded report** proof assets.

**Days 60–90 — make it sticky**
- Land the **per-engagement customer portal** (N5) — the MSSP lock-in.
- Add **at-rest probe encryption** (N2) to clear security RFPs.
- Convert 2–3 discovery relationships into **design-partner MSSPs** on paid pilots.

## 9. The GTM thesis in one sentence

> **Win the MSSP with an architecture they can't get elsewhere, prove the anti-FP claim with a
> published number, and let each MSSP carry Vedha to their whole client base** — then use those
> reference logos to walk into the data-sovereign and OT enterprise on your own terms.
