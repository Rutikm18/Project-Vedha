"""
update_snapshot.py — the ONLY module in this package that talks to the
network. Run by hand or from a scheduled job, never imported by ingest.py,
cpe_normalizer.py, matcher.py, or any other part of the detection path —
that separation is what makes "detection never auto-pulls mid-run" a fact
about the import graph, not just a comment someone could violate by
accident later.

Usage:
    python3 update_snapshot.py [--ecosystem Debian:12] [--products a,b,c]

Queries OSV's real API (api.osv.dev — no key required) for each product in
the list, against the Debian ecosystem (see vuln_db.py's module docstring
for why Debian specifically: it gives backport-aware fix tracking by
package name, the same names dpkg emits). Writes a content-hashed,
dated snapshot to snapshots/osv_debian_snapshot.json.
"""
from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import urllib.request
import urllib.error

from vuln_db import DEFAULT_PRODUCTS, DEFAULT_SNAPSHOT_PATH, _content_hash

OSV_QUERY_URL = "https://api.osv.dev/v1/query"


def _ssl_context() -> ssl.SSLContext:
    """Some macOS python.org installs ship expecting `Install Certificates.
    command` to have been run (it populates
    .../Python.framework/.../etc/openssl/cert.pem) and never have been —
    ssl.create_default_context() then fails with CERTIFICATE_VERIFY_FAILED
    even though the system's own CA bundle (the one curl/Security.framework
    use) is right there at /etc/ssl/cert.pem. Fall back to it explicitly
    rather than disabling verification.
    """
    ctx = ssl.create_default_context()
    try:
        ctx.load_verify_locations(cafile="/etc/ssl/cert.pem")
    except (FileNotFoundError, ssl.SSLError):
        pass  # fine elsewhere (Linux etc.) where the default context already works
    return ctx


def _query_osv(product: str, ecosystem: str, timeout: float = 15.0) -> list[dict]:
    """All known vulnerabilities OSV has for this (product, ecosystem) pair,
    with no version filter — we want the full advisory history so the local
    matcher (Phase 1.4) can apply its own range comparison later; filtering
    by version at sync time would mean re-syncing every time a new host
    shows up with a different installed version.
    """
    payload = json.dumps({"package": {"name": product, "ecosystem": ecosystem}}).encode()
    req = urllib.request.Request(
        OSV_QUERY_URL, data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "detection-engine-sync/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_ssl_context()) as resp:
            data = json.loads(resp.read().decode())
            return data.get("vulns", [])
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        print(f"  WARN: {product}: {exc}", file=sys.stderr)
        return []


def sync_snapshot(products: list[str] = None, ecosystem: str = "Debian:12",
                  out_path: str | Path = DEFAULT_SNAPSHOT_PATH,
                  rate_limit_sec: float = 0.5) -> dict:
    """Fetch real OSV records for every product, write a pinned snapshot.

    rate_limit_sec is a small courtesy delay between requests — OSV's API is
    free/unauthenticated, this is good citizenship, not a documented
    requirement of theirs.
    """
    products = products or DEFAULT_PRODUCTS
    records: dict[str, list[dict]] = {}
    for product in products:
        print(f"  fetching {product} ({ecosystem}) ...", file=sys.stderr)
        records[product] = _query_osv(product, ecosystem)
        time.sleep(rate_limit_sec)

    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "ecosystem": ecosystem,
        "products": products,
        "content_hash": _content_hash(records),
        "records": records,
    }

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2)

    total = sum(len(v) for v in records.values())
    print(f"wrote {out_path} — {total} records across {len(products)} products, "
          f"hash {snapshot['content_hash'][:12]}", file=sys.stderr)
    return snapshot


KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL = "https://api.first.org/data/v1/epss"
# Full daily catalog (every scored CVE) as a gzipped CSV — the whole EPSS
# universe in one download, not a per-CVE query. Used by sync_epss_full().
EPSS_FULL_URL = "https://epss.cyentia.com/epss_scores-current.csv.gz"
DEFAULT_KEV_PATH = Path(__file__).parent / "snapshots" / "kev_snapshot.json"
DEFAULT_EPSS_PATH = Path(__file__).parent / "snapshots" / "epss_snapshot.json"
# CISA Vulnrichment: per-CVE SSVC decision points (Exploitation, Automatable,
# Technical Impact) — the inputs BOD 26-04 prioritises on. One JSON file per CVE.
VULNRICHMENT_URL = "https://raw.githubusercontent.com/cisagov/vulnrichment/develop"
DEFAULT_SSVC_PATH = Path(__file__).parent / "snapshots" / "ssvc_snapshot.json"
_SSVC_MAX_BYTES = 2 * 1024 * 1024


def sync_kev_snapshot(out_path: str | Path = DEFAULT_KEV_PATH) -> dict:
    """The full CISA Known Exploited Vulnerabilities catalog — a single flat
    list, not per-product, so this is its own small pinned snapshot."""
    req = urllib.request.Request(KEV_URL, headers={"User-Agent": "detection-engine-sync/1.0"})
    with urllib.request.urlopen(req, timeout=20, context=_ssl_context()) as resp:
        data = json.loads(resp.read().decode())
    cve_ids = sorted({v["cveID"].upper() for v in data.get("vulnerabilities", []) if "cveID" in v})
    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "cve_ids": cve_ids,
        "content_hash": _content_hash({"cve_ids": cve_ids}),
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2)
    print(f"wrote {out_path} — {len(cve_ids)} KEV-listed CVEs, "
          f"hash {snapshot['content_hash'][:12]}", file=sys.stderr)
    return snapshot


def sync_epss_snapshot(cve_ids: list[str], out_path: str | Path = DEFAULT_EPSS_PATH,
                       batch_size: int = 100, rate_limit_sec: float = 0.5) -> dict:
    """EPSS scores for exactly the CVE IDs this detection run actually cares
    about (the ones in the vuln snapshot) — not the entire EPSS universe,
    which is the whole CVE namespace and would be wasteful to mirror in full.
    """
    scores: dict[str, dict] = {}
    batches = [cve_ids[i:i + batch_size] for i in range(0, len(cve_ids), batch_size)]
    for batch in batches:
        url = f"{EPSS_URL}?cve={','.join(batch)}"
        req = urllib.request.Request(url, headers={"User-Agent": "detection-engine-sync/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
                data = json.loads(resp.read().decode())
            for row in data.get("data", []):
                scores[row["cve"].upper()] = {
                    "epss": float(row["epss"]), "percentile": float(row["percentile"])}
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            print(f"  WARN: EPSS batch failed: {exc}", file=sys.stderr)
        time.sleep(rate_limit_sec)

    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "cve_count": len(scores),
        "content_hash": _content_hash(scores),
        "scores": scores,
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2)
    print(f"wrote {out_path} — {len(scores)}/{len(cve_ids)} EPSS scores, "
          f"hash {snapshot['content_hash'][:12]}", file=sys.stderr)
    return snapshot


def sync_epss_full(out_path: str | Path = DEFAULT_EPSS_PATH, min_epss: float = 0.0) -> dict:
    """The ENTIRE EPSS catalog (every scored CVE) from FIRST.org's daily
    gzipped CSV, in one download.

    Replaces sync_epss_snapshot()'s per-CVE API subset, which only covered the
    CVEs already in the Debian vuln snapshot. Once detection started producing
    findings for CVEs outside that set — every network-banner CVE (e.g.
    CVE-2018-15599), every nuclei/service_vuln finding — those scored epss=0,
    silently zeroing the 0.20 EPSS weight in the risk score. A missing CVE is
    already treated as 0 by EpssDB.get, so `min_epss` drops the long ~0 tail to
    keep the pinned snapshot compact without changing any score meaningfully.
    """
    import gzip
    req = urllib.request.Request(EPSS_FULL_URL, headers={"User-Agent": "detection-engine-sync/1.0"})
    with urllib.request.urlopen(req, timeout=60, context=_ssl_context()) as resp:
        raw = resp.read()
    text = gzip.decompress(raw).decode("utf-8", "replace")
    scores: dict[str, dict] = {}
    for line in text.splitlines():
        if not line or line[0] == "#" or line.startswith("cve,"):
            continue  # skip the #model_version header and the column header
        parts = line.split(",")
        if len(parts) < 3:
            continue
        try:
            epss = float(parts[1])
        except ValueError:
            continue
        if epss < min_epss:
            continue
        scores[parts[0].strip().upper()] = {"epss": epss, "percentile": float(parts[2])}
    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "cve_count": len(scores),
        "content_hash": _content_hash(scores),
        "scores": scores,
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, separators=(",", ":"))  # compact: this file is large
    print(f"wrote {out_path} — {len(scores)} EPSS scores (min_epss={min_epss}), "
          f"hash {snapshot['content_hash'][:12]}", file=sys.stderr)
    return snapshot


def vulnrichment_path(cve_id: str) -> str | None:
    """'CVE-2024-6387' -> '2024/6xxx/CVE-2024-6387.json' (the repository layout)."""
    import re
    m = re.fullmatch(r"CVE-(\d{4})-(\d{4,7})", cve_id.strip().upper())
    if not m:
        return None
    return f"{m.group(1)}/{int(m.group(2)) // 1000}xxx/CVE-{m.group(1)}-{m.group(2)}.json"


_SSVC_VALUES = {
    "exploitation": {"none", "poc", "active"},
    "automatable": {"yes", "no"},
    "technical_impact": {"partial", "total"},
}


def parse_vulnrichment(doc: dict) -> dict | None:
    """The CISA ADP SSVC options of one CVE record, validated against the SSVC
    vocabulary: {exploitation, automatable, technical_impact, timestamp} or None."""
    for adp in ((doc or {}).get("containers") or {}).get("adp") or []:
        for metric in adp.get("metrics") or []:
            other = metric.get("other") or {}
            if other.get("type") != "ssvc":
                continue
            content = other.get("content") or {}
            out: dict = {}
            for option in content.get("options") or []:
                for key, value in option.items():
                    k = key.strip().lower().replace(" ", "_")
                    v = str(value).strip().lower()
                    if k in _SSVC_VALUES and v in _SSVC_VALUES[k]:
                        out[k] = v
            if len(out) == 3:
                out["timestamp"] = str(content.get("timestamp") or "")[:40]
                return out
    return None


def sync_ssvc_snapshot(cve_ids: list[str], out_path: str | Path = DEFAULT_SSVC_PATH,
                       workers: int = 8) -> dict:
    """CISA Vulnrichment SSVC decision points for the CVEs the vuln snapshot can
    produce. A CVE CISA has not enriched is simply absent (the engine then derives
    the points from CVSS and says so). Bounded: one small file per CVE, capped size."""
    from concurrent.futures import ThreadPoolExecutor

    def fetch(cve: str) -> tuple[str, dict | None]:
        rel = vulnrichment_path(cve)
        if rel is None:
            return cve, None
        req = urllib.request.Request(f"{VULNRICHMENT_URL}/{rel}",
                                     headers={"User-Agent": "detection-engine-sync/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=15, context=_ssl_context()) as resp:
                body = resp.read(_SSVC_MAX_BYTES + 1)
            if len(body) > _SSVC_MAX_BYTES:
                return cve, None
            return cve, parse_vulnrichment(json.loads(body.decode()))
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                print(f"  WARN: {cve}: HTTP {exc.code}", file=sys.stderr)
            return cve, None
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            print(f"  WARN: {cve}: {exc}", file=sys.stderr)
            return cve, None

    records: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=max(1, min(workers, 16))) as pool:
        for cve, rec in pool.map(fetch, sorted(set(cve_ids))):
            if rec:
                records[cve] = rec
    snapshot = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "cisagov/vulnrichment (CISA ADP SSVC)",
        "cve_count": len(records),
        "content_hash": _content_hash(records),
        "records": records,
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=1, sort_keys=True)
    print(f"wrote {out_path} — SSVC for {len(records)}/{len(set(cve_ids))} CVEs, "
          f"hash {snapshot['content_hash'][:12]}", file=sys.stderr)
    return snapshot


def _all_known_cve_ids(vuln_snapshot_path: str | Path = DEFAULT_SNAPSHOT_PATH) -> list[str]:
    with Path(vuln_snapshot_path).open() as fh:
        snap = json.load(fh)
    cves: set[str] = set()
    for vulns in snap["records"].values():
        for v in vulns:
            cves.update(v.get("upstream") or [v["id"]])
    return sorted(cves)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="vulns",
                        choices=["vulns", "kev", "epss", "ssvc", "all"],
                        help="which snapshot(s) to refresh (default: vulns)")
    parser.add_argument("--ecosystem", default="Debian:12")
    parser.add_argument("--products", default=None,
                        help="comma-separated; default is the curated starter list")
    parser.add_argument("--out", default=str(DEFAULT_SNAPSHOT_PATH))
    parser.add_argument("--epss-min", type=float, default=0.01,
                        help="drop EPSS scores below this (negligible <2 risk pts) to "
                             "keep the snapshot compact; missing == 0 anyway (default 0.01)")
    args = parser.parse_args()
    products = args.products.split(",") if args.products else None

    if args.target in ("vulns", "all"):
        sync_snapshot(products=products, ecosystem=args.ecosystem, out_path=args.out)
    if args.target in ("kev", "all"):
        sync_kev_snapshot()
    if args.target in ("epss", "all"):
        # Full catalog now, not the per-CVE subset — see sync_epss_full().
        sync_epss_full(min_epss=args.epss_min)
    if args.target in ("ssvc", "all"):
        import re
        cves = sorted({c for c in _all_known_cve_ids()
                       if re.fullmatch(r"CVE-\d{4}-\d{4,7}", c)}
                      | set(json.load(DEFAULT_KEV_PATH.open())["cve_ids"]))
        sync_ssvc_snapshot(cves)


if __name__ == "__main__":
    main()
