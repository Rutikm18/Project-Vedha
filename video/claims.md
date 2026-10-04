# Claims register

Every claim the film makes on screen, where it comes from, and its status. **Unsourced claims need a human sign-off before publishing.**

| # | On-screen claim | Source in repo | Status |
|---|---|---|---|
| 1 | "A 7-day network health check." / "Book your 7-day check" | `PlanPanel.tsx`: POC presets 7/14/30 days (default 14). No product copy says "7-day health check". | **Needs confirmation** |
| 2 | "Delivered by a partner you already trust." | Not found | **Needs confirmation** |
| 3 | "For office networks. Not cloud networks." | Not found as copy. Fits the probe-in-client-network architecture (`README.md`). | **Needs confirmation** |
| 4 | वेध = "TO PIERCE THROUGH" | Not found (brief only) | **Needs confirmation + cultural review** |
| 5 | "Find what's open. Prove what's real. Show the fix worked." | Findings and attack mapping (`README.md`); `verifier.py`; teal = "remediated / verified" (`design-system.md`) | Sourced |
| 6 | "A plain-language report. With proof." | Report pipeline (`lib/report/*`, `prompts/report.ts`: confidence-matched language) | Sourced |
| 7 | Grade C → B | Real scale A–F (`services/posture.py`); the values are illustrative | Sourced scale, illustrative values |
| 8 | Findings rows, IPs, hostnames, "Verified 03 Oct 2026" | Illustrative (RFC 5737 IPs, `.example` hosts); tagged "Illustrative data" | Illustrative |
| 9 | vedhasec.com | `docs/STATUS.md` | Sourced |

Guardrail check: no "secure", "protected", "safe", "hack-proof", "100%", "certified", "compliant" anywhere in `src/copy.*.json`.
