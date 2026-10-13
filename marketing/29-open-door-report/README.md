# #29 Open Door Report, Stage 1 (8 pages, 3 charts, a fix for every finding)

`open-door-report-stage1.pdf` is built by `node 29-open-door-report/build.mjs` from `report_data.json`.

**Status: template ready, data pending.** Charts 1–3 render as labelled "data pending" frames until their rows are filled from the named sources:

| Chart | Source | Depends on |
|---|---|---|
| 1 Internet-exposed services in India | Shadowserver aggregates, with their agreed credit line | #20 licence answer |
| 2 What Vedha checks found | Aggregated check results | #9 clause live (X.4 permission) + checks run |
| 3 Awareness of the 15 controls | The #18 poll, n ≥ 200 | #18 |

**Rules:** fill rows only from the source; never estimate; keep n and the method on the page. If a source doesn't arrive, publish without that chart rather than with a guess.

**Chart design** (dataviz skill): single-series horizontal bars in brand blue (validated: lightness, chroma, contrast ≥ 3:1), no legend (the title names the series), values as direct labels in ink, thin bars with rounded data ends, sorted largest first. The chart code was tested with clearly labelled TEST values in a scratch copy; the committed data file contains no values.

**Done when:** 8 pages, 3 charts with real data, a fix per finding, published (Mon 30 Nov).
