# CVE Correlation — System Design

> Decision (2026-08-25): **full offline NVD mirror (air-gap)** + KEV + EPSS.
> Honors the probe invariant: the probe emits facts (incl. CPE) and NEVER a CVE;
> CVE correlation is a SEPARATE interpretation layer that owns the vuln DB.

## Architecture — two layers

### Layer A · Probe: CPE enrichment (thin, no DB)
- `scanner/cpe.py` (+ `main_scripts/` mirror): `to_cpe(service, product, version) -> cpe2.3`
  using a curated **product → CPE vendor:product** table (OpenSSH→openbsd:openssh,
  Apache→apache:http_server, nginx→nginx:nginx, Postfix→postfix:postfix,
  MySQL→oracle:mysql, PostgreSQL→postgresql:postgresql, ...). Deterministic, offline.
- `service_banner.py` attaches a `cpe` field to each service fact. The probe still
  emits NO CVE claim — only the matchable identity.

### Layer B · `cve/` package: correlation (owns the DB)
New top-level package (parallel to `scanner/`). NOT a probe scanner.

| Module | Responsibility |
|---|---|
| `cve/version.py` | Version comparison that tolerates real-world SSH/OpenSSL/distro strings (`8.2p1`, `1.1.1k`, epochs, `-ubuntu`). Accuracy-critical. |
| `cve/vulndb.py` | SQLite schema + `cves_for_cpe(vendor, product, version)` using NVD `versionStart*/versionEnd*` ranges; joins CVSS + KEV + EPSS. |
| `cve/ingest.py` | Build/refresh the offline mirror. NVD API 2.0 (paginated ~192 pages, resumable, rate-limit + certifi TLS), CISA KEV (~1.7k), EPSS CSV. |
| `cve/correlator.py` | facts → CVE findings: match, enrich (CVSS/KEV/EPSS), assign **confidence** + **risk score**. |
| `cve/cli.py` | `ingest` (build mirror) and `correlate` (facts.jsonl → cve_findings.jsonl). |

## SQLite schema (offline mirror)
```
cve(cve_id PK, cvss_score, cvss_severity, cvss_vector, description, published, last_modified)
cpe_match(cve_id, vendor, product, version_start_incl, version_start_excl,
          version_end_incl, version_end_excl, exact_version, vulnerable)   -- idx(vendor,product)
kev(cve_id PK, vendor, product, name, date_added)
epss(cve_id PK, epss REAL, percentile REAL)
meta(key PK, value)   -- feed freshness / counts
```

## Matching + accuracy (the #1 risk: distro backports)
- Observed `(vendor, product, version)` → `cpe_match` rows for that product → version
  in range → candidate CVEs.
- **Confidence tiers**: banner-derived version ⇒ `medium` MAX, tagged
  "verify against distro patch level" (backports patch silently). Never asserted.
- **KEV-first**: actively-exploited CVEs are surfaced top regardless of CVSS.
- **Risk score** = CVSS + KEV(large boost) + EPSS + internet-exposure (vantage) +
  asset-criticality → prioritizes the handful that matter.
- Every CVE finding cites the fact (product/version/CPE) it came from.

## Output — CVE findings (distinct schema; carries cve_id)
`{cve_id, cvss_score, severity, kev, epss, epss_percentile, matched_cpe, product,
  version, target, port, confidence, risk_score, evidence, source_scanner}` →
`cve_findings.jsonl`, alongside (never mixed with) the probe's `findings.jsonl`.

## Build/test plan
Bottom-up, each independently testable: version.py → vulndb.py (synthetic in-memory
DB) → cpe.py + service_banner enrichment → correlator.py (synthetic DB) →
ingest.py (correct + resumable; smoke-test a small NVD slice + full KEV) → CLI.
A full NVD pull (~382k CVEs, ~192 API pages) is a production ingestion run, not a
unit test; the correlator is validated against a crafted mirror.
