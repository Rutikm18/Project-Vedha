# AI sector expertise

The AI answers as an industry expert when the engagement has a **sector** (and optionally
**jurisdictions**). The Manager builds a trusted "domain brief" (persona, sector vocabulary,
impact lens, best practices, applicable compliance controls, incident-reporting clocks) and
adds it to the system prompt. Code: `app/ai/skills.py`, `app/ai/domain_brief.py`,
`app/services/domain_context.py`, `app/compliance/`.

## How to set it

| What | How |
|---|---|
| Sector + jurisdictions | `PUT /engagements/{id}/profile` (stored in `rules_of_engagement["profile"]`) |
| Asset tags (fallback) | `PUT /engagements/{id}/assets/{asset_id}/tags`, or `POST .../assets/retag` |
| Selection order | profile sector, else the estate's `sector_fn:*` tags, else `generic` |

## Sectors covered

| Sector value | Advisor persona | Also inferred from asset tags |
|---|---|---|
| `generic` | Enterprise security advisor | default |
| `banking` | Banking cyber-risk advisor | `sector_fn:core_banking`, `:swift`, `:atm` |
| `payments_fintech` | Payments and fintech security advisor | `sector_fn:payments`, `:card_processing`, `:hsm` |
| `nbfc` | NBFC and lending cyber-risk advisor | none |
| `insurance` | Insurance cyber-risk advisor | none |
| `capital_markets` | Capital-markets cyber-resilience advisor | `sector_fn:trading` |
| `healthcare` | Healthcare security advisor | none |
| `government` | Public-sector security advisor | none |

Jurisdictions: IN, EU, UK, US, SA, AE, SG, HK. Frameworks applied (by sector and jurisdiction):

| Region | Frameworks |
|---|---|
| India | RBI CSF and RBI IT Governance 2023 (banking), RBI PSO cyber 2024 (payments), SEBI CSCRF (capital markets), IRDAI ISG (insurance), CERT-In 2022 and DPDP 2023 (all sectors) |
| EU / UK | GDPR, NIS2 (all sectors); DORA (financial); UK GDPR (all); UK operational resilience (financial) |
| US | NYDFS Part 500, GLBA Safeguards (financial) |
| Middle East / APAC | SAMA CSF (SA, financial), UAE IAS (all), MAS TRM (SG, financial), HKMA CRF (HK, financial) |
| Global | SWIFT CSCF (when SWIFT assets are tagged) |

`healthcare` and `government` get a sector persona and best practices but no sector-specific
compliance pack; the all-sector packs (GDPR, NIS2, CERT-In, DPDP, UAE IAS) still apply by jurisdiction.

## Where it applies

| Feature | Uses the sector brief |
|---|---|
| AI Brain (engagement selected) | Yes |
| Ask Vedha on a finding (chat and explain) | Yes, via the finding's engagement |
| Customer portal assistant | Yes |
| Engagement AI report, compliance brief, remediation refine | Yes |
| Advisor agent | Yes, loaded when a run starts |
| AI Brain with no engagement; CVE-only lookups with no stored finding | No (generic) |

Lookups fail soft: if the profile cannot be loaded, the plain assistant answers and the log
shows `ai.domain_brief_failed` or `agent.domain_brief_failed`.
