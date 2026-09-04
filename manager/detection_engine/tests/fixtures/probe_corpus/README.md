# probe_corpus — captured probe fact shapes (the fact contract's ground truth)

Each `*.json` file is a JSON array of raw ScanResult facts, exactly as the
vedha-agent submits them (`asdict(ScanResult)` — see
`probe/scanner/scanner_base.py`):

```json
{"scanner": "...", "target": "...", "timestamp": "<ISO 8601>",
 "port": 445, "proto": "tcp", "status": "open", "data": {...}}
```

`scanner`, `target`, `timestamp` and `status` are REQUIRED — `ingest.py` rejects
any record missing one, and a rejected record reaches no rule at all. An earlier
version of these seeds omitted `timestamp`, so all 38 of them were quarantined and
the whole corpus produced zero findings while the contract test stayed green.
`test_corpus_survives_ingestion` now runs the corpus through the real ingester so
that cannot recur.

`test_fact_contract.py` reads this corpus and asserts that **every fact path a
posture rule declares in `requires` is actually emitted by some scanner here.** A
rule that reads a path nothing emits is individually correct and globally useless —
it can never fire. Unit-testing the rule passes; testing the scanner passes; only
comparing the two catches it. This is the gate that makes agent-side schema drift
fail in CI instead of silently in production.

## Replace these seeds with REAL captures

The files here are representative seeds derived from the scanners' known output
shapes — enough to make the gate meaningful today. Replace/augment them with real
data: hit `GET /engagements/{id}/raw-facts?scanner=smb_scan` on a real engagement,
save each `facts` entry verbatim, and **redact hostnames/banners**. The more real
shapes captured, the stronger the gate.
