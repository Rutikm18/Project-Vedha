"""
vulndb.py — the offline vulnerability mirror (SQLite) and its query surface.

Holds a full NVD mirror (CVE metadata + CPE applicability ranges) enriched with
CISA KEV (actively-exploited) and EPSS (exploit probability). Used read-write by
`ingest.py` to build/refresh the mirror, and read-only by `correlator.py` to map
an observed (vendor, product, version) to prioritized CVEs.

Version-range membership can't be expressed in SQL (versions aren't lexically
ordered), so `cves_for_cpe` fetches the small candidate set for a product via the
(vendor, product) index, then filters in Python with cve.version.in_range.
"""

from __future__ import annotations

import sqlite3

from .version import in_range

_SCHEMA = """
CREATE TABLE IF NOT EXISTS cve (
    cve_id TEXT PRIMARY KEY,
    cvss_score REAL,
    cvss_severity TEXT,
    cvss_vector TEXT,
    description TEXT,
    published TEXT,
    last_modified TEXT
);
CREATE TABLE IF NOT EXISTS cpe_match (
    cve_id TEXT,
    vendor TEXT,
    product TEXT,
    version_start_incl TEXT,
    version_start_excl TEXT,
    version_end_incl TEXT,
    version_end_excl TEXT,
    exact_version TEXT,
    vulnerable INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_cpe_vp ON cpe_match (vendor, product);
CREATE TABLE IF NOT EXISTS kev (
    cve_id TEXT PRIMARY KEY,
    vendor TEXT,
    product TEXT,
    name TEXT,
    date_added TEXT
);
CREATE TABLE IF NOT EXISTS epss (
    cve_id TEXT PRIMARY KEY,
    epss REAL,
    percentile REAL
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def _norm(s) -> str:
    return str(s or "").strip().lower()


class VulnDB:
    def __init__(self, path: str, *, create: bool = False):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        if create:
            self.conn.executescript(_SCHEMA)
            self.conn.commit()

    # ── ingest-side writers ───────────────────────────────────────────────────
    def upsert_cve(self, cve_id, cvss_score, cvss_severity, cvss_vector,
                   description, published, last_modified) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO cve VALUES (?,?,?,?,?,?,?)",
            (cve_id, cvss_score, cvss_severity, cvss_vector, description,
             published, last_modified))

    def add_cpe_match(self, cve_id, vendor, product, *, start_incl=None,
                      start_excl=None, end_incl=None, end_excl=None,
                      exact_version=None, vulnerable=True) -> None:
        self.conn.execute(
            "INSERT INTO cpe_match (cve_id,vendor,product,version_start_incl,"
            "version_start_excl,version_end_incl,version_end_excl,exact_version,"
            "vulnerable) VALUES (?,?,?,?,?,?,?,?,?)",
            (cve_id, _norm(vendor), _norm(product), start_incl, start_excl,
             end_incl, end_excl, exact_version, 1 if vulnerable else 0))

    def replace_cpe_matches(self, cve_id) -> None:
        self.conn.execute("DELETE FROM cpe_match WHERE cve_id=?", (cve_id,))

    def upsert_kev(self, cve_id, vendor, product, name, date_added) -> None:
        self.conn.execute("INSERT OR REPLACE INTO kev VALUES (?,?,?,?,?)",
                          (cve_id, _norm(vendor), _norm(product), name, date_added))

    def upsert_epss(self, cve_id, epss, percentile) -> None:
        self.conn.execute("INSERT OR REPLACE INTO epss VALUES (?,?,?)",
                          (cve_id, epss, percentile))

    def set_meta(self, key, value) -> None:
        self.conn.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (key, str(value)))

    def get_meta(self, key, default=None):
        row = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row["value"] if row else default

    def commit(self) -> None:
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def counts(self) -> dict:
        c = self.conn.execute
        return {t: c(f"SELECT COUNT(*) n FROM {t}").fetchone()["n"]
                for t in ("cve", "cpe_match", "kev", "epss")}

    # ── correlate-side reader ─────────────────────────────────────────────────
    def cves_for_cpe(self, vendor: str, product: str, version: str) -> list[dict]:
        """All vulnerable CVEs whose CPE applicability covers (vendor, product,
        version), enriched with CVSS + KEV + EPSS. De-duplicated by cve_id."""
        rows = self.conn.execute(
            "SELECT * FROM cpe_match WHERE vendor=? AND product=? AND vulnerable=1",
            (_norm(vendor), _norm(product))).fetchall()
        matched: dict[str, dict] = {}
        for r in rows:
            if not in_range(version, start_incl=r["version_start_incl"],
                            start_excl=r["version_start_excl"],
                            end_incl=r["version_end_incl"],
                            end_excl=r["version_end_excl"],
                            exact=r["exact_version"]):
                continue
            cid = r["cve_id"]
            if cid in matched:
                continue
            matched[cid] = self._enrich(cid, r)
        return sorted(matched.values(),
                      key=lambda d: (d.get("kev", False), d.get("cvss_score") or 0),
                      reverse=True)

    def _enrich(self, cve_id: str, match_row) -> dict:
        cve = self.conn.execute("SELECT * FROM cve WHERE cve_id=?", (cve_id,)).fetchone()
        kev = self.conn.execute("SELECT * FROM kev WHERE cve_id=?", (cve_id,)).fetchone()
        epss = self.conn.execute("SELECT * FROM epss WHERE cve_id=?", (cve_id,)).fetchone()
        return {
            "cve_id": cve_id,
            "cvss_score": cve["cvss_score"] if cve else None,
            "cvss_severity": cve["cvss_severity"] if cve else None,
            "description": (cve["description"] if cve else "") or "",
            "kev": bool(kev),
            "kev_date": kev["date_added"] if kev else None,
            "epss": epss["epss"] if epss else None,
            "epss_percentile": epss["percentile"] if epss else None,
            "matched": {k: match_row[k] for k in (
                "version_start_incl", "version_start_excl", "version_end_incl",
                "version_end_excl", "exact_version")},
        }
