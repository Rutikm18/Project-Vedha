"""
ingest.py — build / refresh the offline vulnerability mirror.

Three public feeds populate the SQLite mirror that `correlator.py` reads:

  * NVD API 2.0  — the CVE + CPE-applicability backbone (~382k CVEs, ~192 pages
    of 2000). Paginated, RESUMABLE (progress persisted in `meta.nvd_next_index`
    so a killed run picks up where it stopped), rate-limited (NVD allows 5 req /
    30 s anonymous, 50 with an API key — we sleep accordingly), TLS via certifi.
  * CISA KEV     — the actively-exploited set (~1.7k). One JSON download.
  * EPSS         — daily exploit-probability scores. One gzip CSV download.

Building the mirror is a PRODUCTION ingestion run, not a unit test: a full NVD
pull takes ~20 min at the anonymous rate. `max_pages` bounds it for smoke tests.

No third-party HTTP client — stdlib urllib with a certifi-backed SSL context, so
the mirror can be built from a locked-down box with only the CA bundle trusted.
"""

from __future__ import annotations

import csv
import gzip
import io
import json
import os
import ssl
import time
from datetime import datetime, timezone
import urllib.error
import urllib.parse
import urllib.request

from .vulndb import VulnDB

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
KEV_URL = ("https://www.cisa.gov/sites/default/files/feeds/"
           "known_exploited_vulnerabilities.json")
EPSS_URL = "https://epss.empiricalsecurity.com/epss_scores-current.csv.gz"

NVD_PAGE_SIZE = 2000              # NVD 2.0 hard maximum
_USER_AGENT = "vedha-vulndb-ingest/1.0"


def _ssl_context() -> ssl.SSLContext:
    """certifi CA bundle if present, else the system default. Feeds served TLS
    from behind CDNs fail on some hosts without an explicit modern bundle."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def _get(url: str, *, params: dict | None = None, headers: dict | None = None,
         timeout: float = 60.0, retries: int = 4, ctx: ssl.SSLContext | None = None) -> bytes:
    """GET with backoff on the transient failures NVD/CDNs throw under load
    (403/429/503, connection resets). Raises the last error if all retries fail."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    ctx = ctx or _ssl_context()
    hdrs = {"User-Agent": _USER_AGENT, "Accept": "application/json"}
    hdrs.update(headers or {})
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (403, 429, 500, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** attempt * 3)
                continue
            raise
        except (urllib.error.URLError, ssl.SSLError, OSError) as e:
            last = e
            if attempt < retries - 1:
                time.sleep(2 ** attempt * 3)
                continue
            raise
    if last:
        raise last
    raise RuntimeError("unreachable")


# ── NVD parsing ───────────────────────────────────────────────────────────────
def _cvss(metrics: dict) -> tuple:
    """Best available CVSS: prefer v3.1 > v3.0 > v2. Returns (score, severity,
    vector). v2 keeps severity on the metric, not in cvssData."""
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        arr = metrics.get(key)
        if arr:
            m = arr[0]
            d = m.get("cvssData", {})
            score = d.get("baseScore")
            sev = d.get("baseSeverity") or m.get("baseSeverity")
            return score, (sev.upper() if isinstance(sev, str) else sev), d.get("vectorString")
    return None, None, None


def _iter_cpe_matches(cve: dict):
    for cfg in cve.get("configurations", []):
        for node in cfg.get("nodes", []):
            for m in node.get("cpeMatch", []):
                yield m


def _parse_criteria(criteria: str) -> tuple | None:
    """cpe:2.3:a:vendor:product:version:... -> (part, vendor, product, version)."""
    parts = criteria.split(":")
    if len(parts) < 6 or parts[0] != "cpe" or parts[1] != "2.3":
        return None
    return parts[2], parts[3], parts[4], parts[5]


def ingest_one_cve(db: VulnDB, cve: dict) -> None:
    """Upsert one NVD `cve` object + its CPE-applicability rows. Idempotent:
    existing cpe_match rows for this CVE are replaced so re-ingest never dupes."""
    cid = cve.get("id")
    if not cid:
        return
    score, sev, vec = _cvss(cve.get("metrics", {}))
    desc = ""
    for d in cve.get("descriptions", []):
        if d.get("lang") == "en":
            desc = d.get("value", "")
            break
    db.upsert_cve(cid, score, sev, vec, desc,
                  cve.get("published"), cve.get("lastModified"))
    db.replace_cpe_matches(cid)
    for m in _iter_cpe_matches(cve):
        parsed = _parse_criteria(m.get("criteria", ""))
        if not parsed:
            continue
        part, vendor, product, version = parsed
        if part not in ("a", "o"):          # applications + OS; skip hardware
            continue
        exact = None if version in ("*", "-", "") else version
        db.add_cpe_match(
            cid, vendor, product,
            start_incl=m.get("versionStartIncluding"),
            start_excl=m.get("versionStartExcluding"),
            end_incl=m.get("versionEndIncluding"),
            end_excl=m.get("versionEndExcluding"),
            exact_version=exact,
            vulnerable=bool(m.get("vulnerable", True)))


def ingest_nvd(db: VulnDB, *, api_key: str | None = None, resume: bool = True,
               max_pages: int | None = None, page_size: int = NVD_PAGE_SIZE,
               log=print) -> int:
    """Pull the NVD CVE corpus into the mirror. Resumable via meta.nvd_next_index.
    Returns the number of CVEs ingested this run."""
    ctx = _ssl_context()
    headers = {"apiKey": api_key} if api_key else {}
    delay = 0.6 if api_key else 6.0        # stay under 50/30s (key) or 5/30s (anon)

    total = int(db.get_meta("nvd_total", 0) or 0)
    start = int(db.get_meta("nvd_next_index", 0) or 0) if resume else 0
    if not (resume and total and 0 < start < total):
        start = 0
    ingested = 0
    pages = 0
    while True:
        raw = _get(NVD_URL, params={"resultsPerPage": page_size, "startIndex": start},
                   headers=headers, ctx=ctx)
        page = json.loads(raw)
        total = int(page.get("totalResults", 0))
        vulns = page.get("vulnerabilities", [])
        for v in vulns:
            ingest_one_cve(db, v.get("cve", {}))
            ingested += 1
        got = len(vulns)
        start += got if got else page_size
        db.set_meta("nvd_total", total)
        db.set_meta("nvd_next_index", start)
        db.commit()
        pages += 1
        log(f"  nvd: {min(start, total)}/{total} CVEs ({pages} pages)")
        if got == 0 or start >= total:
            break
        if max_pages and pages >= max_pages:
            log(f"  nvd: stopped at max_pages={max_pages} (resumable)")
            return ingested
        time.sleep(delay)
    db.set_meta("nvd_next_index", 0)       # completed a full pass; next run starts fresh
    db.set_meta("nvd_complete", "1")
    return ingested


# ── CISA KEV ──────────────────────────────────────────────────────────────────
def ingest_kev(db: VulnDB, *, log=print) -> int:
    raw = _get(KEV_URL)
    data = json.loads(raw)
    n = 0
    for v in data.get("vulnerabilities", []):
        cid = v.get("cveID")
        if not cid:
            continue
        db.upsert_kev(cid, v.get("vendorProject"), v.get("product"),
                      v.get("vulnerabilityName"), v.get("dateAdded"))
        n += 1
    db.set_meta("kev_count", n)
    db.commit()
    log(f"  kev: {n} actively-exploited CVEs")
    return n


# ── EPSS ──────────────────────────────────────────────────────────────────────
def ingest_epss(db: VulnDB, *, log=print) -> int:
    raw = _get(EPSS_URL, headers={"Accept": "application/gzip"})
    try:
        text = gzip.decompress(raw).decode("utf-8", "replace")
    except (OSError, EOFError):
        text = raw.decode("utf-8", "replace")   # already-decompressed mirror
    n = 0
    for row in csv.reader(io.StringIO(text)):
        if not row or row[0].startswith("#") or row[0] == "cve":
            continue
        if len(row) < 3:
            continue
        try:
            db.upsert_epss(row[0], float(row[1]), float(row[2]))
            n += 1
        except ValueError:
            continue
    db.set_meta("epss_count", n)
    db.commit()
    log(f"  epss: {n} exploit-probability scores")
    return n


def ingest_all(db: VulnDB, *, nvd: bool = True, kev: bool = True, epss: bool = True,
               api_key: str | None = None, resume: bool = True,
               max_pages: int | None = None, log=print) -> dict:
    """Refresh every enabled feed. KEV/EPSS first (cheap, always fresh); NVD last
    (the long haul). Returns per-feed counts."""
    out: dict[str, int] = {}
    if kev:
        out["kev"] = ingest_kev(db, log=log)
    if epss:
        out["epss"] = ingest_epss(db, log=log)
    if nvd:
        out["nvd"] = ingest_nvd(db, api_key=api_key, resume=resume,
                                max_pages=max_pages, log=log)
    # Stamp when this refresh cycle finished so downstream consumers (correlate)
    # can warn when the mirror is stale — an old mirror silently misses new CVEs.
    db.set_meta("last_ingest_utc",
                datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    return out
