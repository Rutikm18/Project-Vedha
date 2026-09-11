"""
eol_catalog.py — curated end-of-life / end-of-support dates for fingerprinted OSes.

DATA, not logic: a table an analyst maintains, matched against the `os_release`
string `os_fingerprint` already emits. Dates are the vendor-published END OF
SECURITY SUPPORT — the point after which no patches are issued — not the earlier
"mainstream support" date, because the security consequence is what makes this a
finding.

WHY THIS IS A CURATED TABLE AND NOT AN API CALL
-----------------------------------------------
The detection engine must produce the same verdict for the same facts, offline
and forever. An external EOL API would make findings depend on network reach and
a third party's uptime, and would silently change historical results. The cost is
freshness: an OS absent from this table is treated as SUPPORTED (silent), never
guessed at. That asymmetry is deliberate — see the matching rule below.

MATCHING RULE: LONGEST KEY WINS, NEVER A PREFIX GUESS
-----------------------------------------------------
Keys are matched as substrings of the normalised release string, and the LONGEST
matching key is chosen. That is what keeps `windows server 2012 r2` from being
shadowed by `windows server 2012`, and it is why a still-supported release simply
matches nothing rather than inheriting an ancestor's date.

False positives are expensive here in a way false negatives are not: telling a
customer their supported fleet is end-of-life destroys trust in every other
finding in the report. So the table only contains releases whose EOS date is
published and unambiguous.
"""
from __future__ import annotations

from datetime import date, datetime, timezone

# Normalised release substring -> vendor end-of-SECURITY-support date (ISO).
# Keep entries specific enough that a supported successor never matches.
_EOL: dict[str, str] = {
    # ── Microsoft client ──────────────────────────────────────────────────────
    "windows xp":             "2014-04-08",
    "windows vista":          "2017-04-11",
    "windows 7":              "2020-01-14",
    "windows 8":              "2016-01-12",
    "windows 8.1":            "2023-01-10",
    "windows 10 1507":        "2017-05-09",
    "windows 10 1607":        "2018-04-10",
    "windows 10 1709":        "2019-04-09",
    "windows 10 1803":        "2019-11-12",
    "windows 10 1809":        "2020-11-10",
    "windows 10 1903":        "2020-12-08",
    "windows 10 1909":        "2021-05-11",
    "windows 10 2004":        "2021-12-14",
    "windows 10 20h2":        "2023-05-09",
    "windows 10 21h1":        "2022-12-13",
    "windows 10 21h2":        "2024-06-11",
    "windows 10 22h2":        "2025-10-14",   # final Windows 10 servicing update
    "windows 11 21h2":        "2023-10-10",
    "windows 11 22h2":        "2024-10-08",
    # ── Microsoft server ──────────────────────────────────────────────────────
    "windows server 2003":    "2015-07-14",
    "windows server 2008":    "2020-01-14",
    "windows server 2008 r2": "2020-01-14",
    "windows server 2012":    "2023-10-10",
    "windows server 2012 r2": "2023-10-10",
    # ── Linux ─────────────────────────────────────────────────────────────────
    "ubuntu 14.04":           "2019-04-30",
    "ubuntu 16.04":           "2021-04-30",
    "ubuntu 18.04":           "2023-05-31",
    "centos 6":               "2020-11-30",
    "centos 7":               "2024-06-30",
    "centos 8":               "2021-12-31",
    "debian 8":               "2020-06-30",
    "debian 9":               "2022-06-30",
    "debian 10":              "2024-06-30",
}

_SOURCE = "vendor_published_eos"


def lookup_eol(os_release: str | None, os_version: str | None = None) -> dict | None:
    """EOL info for a fingerprinted OS, or None when supported/unknown.

    `os_version` is accepted for signature stability (callers pass what
    os_fingerprint emits) but is not currently needed to discriminate: the
    release string alone carries the servicing branch. Returns a dict with
    product / eol_date / days_past_eol / source, or None.
    """
    if not os_release or not str(os_release).strip():
        return None

    hay = str(os_release).strip().lower()
    best_key: str | None = None
    for key in _EOL:
        # Longest match wins so a more specific release beats its ancestor.
        if key in hay and (best_key is None or len(key) > len(best_key)):
            best_key = key
    if best_key is None:
        return None

    eol = date.fromisoformat(_EOL[best_key])
    today = datetime.now(timezone.utc).date()
    return {
        "product": str(os_release).strip(),
        "eol_date": _EOL[best_key],
        "days_past_eol": (today - eol).days,
        "source": _SOURCE,
    }
