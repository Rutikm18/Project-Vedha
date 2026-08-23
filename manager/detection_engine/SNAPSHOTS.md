# Vulnerability-intelligence snapshots

The detection engine matches and prioritizes **offline** against pinned snapshots
in `snapshots/` — no live API call ever happens during a scan, so the same facts
produce the same findings on any machine, any day. The snapshots are refreshed
**out-of-band** and committed, then baked into the image at build time.

## The snapshots

| File | Source | Used for |
|------|--------|----------|
| `osv_debian_snapshot.json` | OSV (`api.osv.dev`), Debian ecosystem | CVE matching for **credentialed / dpkg** package inventory (distro-versioned) |
| `nvd_cpe_snapshot.json` | curated from NVD/CVE | CVE matching for **network-service banners** (upstream versions, e.g. Dropbear 2017.75). Merged into the OSV snapshot at load time. |
| `epss_snapshot.json` | FIRST.org daily EPSS catalog | exploit-probability factor in `risk_score` (full catalog, ~145k CVEs ≥ 0.01) |
| `kev_snapshot.json` | CISA Known Exploited Vulnerabilities | known-exploited factor in `risk_score` |

Prioritization (`app/detection/prioritization.py`) reads EPSS + KEV from these
snapshots to compute each finding's `risk_score`. A CVE **absent** from EPSS is
treated as `epss = 0`, so the catalog must be broad — a narrow subset silently
zeroes the exploit-probability signal for anything outside it (this was a real
bug: the old EPSS snapshot held only 1,416 CVEs and missed Log4Shell/Heartbleed).

## Refresh

```bash
make sync-vuln-snapshots     # OSV + full EPSS + CISA KEV + NVD/CPE companion
# then commit the changed snapshots and rebuild the image:
make api-only                # (or make up)
```

Needs outbound internet on the machine running the sync (the sync is the ONLY
network step; matching is always offline). Tuning:

```bash
cd manager/detection_engine
python3 update_snapshot.py epss --epss-min 0.01   # drop the negligible <2-pt tail (default)
python3 update_snapshot.py kev                    # KEV only
python3 update_snapshot.py vulns --products nginx,openssh   # OSV for specific products
python3 build_nvd_cpe_snapshot.py                 # regenerate the NVD/CPE companion
```

A production deployment runs `make sync-vuln-snapshots` on a schedule (e.g. daily
in CI) and rebuilds, so KEV/EPSS never go stale.
