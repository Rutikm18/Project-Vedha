# #7 Price list + partner margin model

`margin_model.xlsx` is one sheet. Edit the **yellow cells** (blue text); everything else is a formula. It opens in Excel or Google Sheets and recalculates on open. Rebuild it from `build_model.py` if needed.

> **All numbers in it are EXAMPLES, not a proposal.** The founders set the real prices. #7 is done when the sheet is signed off (row 41).

## What it models (per client, per tier, plus a mix-weighted "Blended" column)

- Customer price incl. 18% GST (SAC 9983; confirm with your CA)
- **Check margin** for the partner (list − partner buy price)
- **Remediation revenue** for the partner (hours × rate × share of clients who buy it)
- **Renewal margin** for the partner (year-2 check)
- Vedha's net per check after founder hours and infrastructure
- Per partner per year at 5 / 10 / 25 clients, **including the founder hours each scenario needs**

All formulas were verified with an independent formula engine (pycel): 0 errors. I also hand-checked the Starter column.

## Two things the example numbers already show (they hold for most realistic inputs)

1. **For partners, remediation is worth as much as the check margin** (₹7,200 vs ₹4,500 per Starter client in the example). That's the answer to "your report exposes my work" (#17): the report *creates* paid work for the partner.
2. **The small tier lives or dies on founder hours.** At 6 founder-hours per check, Starter nets Vedha about ₹1,000 (9.5%). Measure real hours in the Partner Zero checks (#16) before fixing the Starter price, or cap what Starter includes.

## Next

Once signed off, copy the tiers into the deck (slide 8) and the competitive analysis: see `08-deck-pricing/`.
