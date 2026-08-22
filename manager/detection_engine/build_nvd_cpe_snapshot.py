"""
build_nvd_cpe_snapshot.py — generate the NVD/CPE companion vuln snapshot.

WHY A SEPARATE SNAPSHOT: the primary snapshot is OSV's Debian ecosystem, keyed
by Debian *package* versions — correct for credentialed dpkg inventory, but it
cannot match a network banner, which reports an *upstream* version (e.g. Dropbear
"2017.75", not "2020.81-3+deb11u1"). NVD's CPE applicability data uses upstream
version ranges, so it is the right feed for banner-derived findings.

This writes snapshots/nvd_cpe_snapshot.json in the SAME on-disk shape as the OSV
snapshot (records keyed by the CPE product / lookup_key, each an OSV-style vuln
object) so vuln_db.load_snapshot() can merge it and matcher.py can range-match it
unchanged. Records here are transcribed from NVD/CVE (vendor:product CPE +
versionEndExcluding) — the `fixed` event is the first release that is NOT
affected, exactly NVD's versionEndExcluding semantics.

Run out-of-band (never during detection):  python3 build_nvd_cpe_snapshot.py
A real deployment would fetch these from the NVD 2.0 API keyed by the CPE
products in cpe_normalizer._HEADER_PRODUCT_TO_CPE; this curated seed covers the
network daemons we detect today and is the wiring proof.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SNAPSHOT = Path(__file__).parent / "snapshots" / "nvd_cpe_snapshot.json"


def _rec(cve: str, name: str, fixed: str, cvss_vector: str, summary: str) -> dict:
    """One OSV-shaped record: affected below `fixed` (NVD versionEndExcluding)."""
    return {
        "id": cve,
        "summary": summary,
        "affected": [{
            "package": {"ecosystem": "NVD/CPE", "name": name},
            "ranges": [{"type": "SEMVER",
                        "events": [{"introduced": "0"}, {"fixed": fixed}]}],
        }],
        "severity": [{"type": "CVSS_V3", "score": cvss_vector}],
    }


# Keyed by lookup_key (== CPE product) as set in cpe_normalizer._HEADER_PRODUCT_TO_CPE.
RECORDS: dict[str, list[dict]] = {
    "dropbear": [
        _rec("CVE-2018-15599", "dropbear", "2018.76",
             "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N",
             "Dropbear: remote username enumeration via svr-auth.c response timing."),
        _rec("CVE-2017-9078", "dropbear", "2017.75",
             "CVSS:3.0/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H",
             "Dropbear server double-free in TCP listener cleanup (-a) may allow root RCE."),
        _rec("CVE-2016-7406", "dropbear", "2016.74",
             "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
             "Dropbear: format-string vulnerability enabling remote code execution."),
        _rec("CVE-2016-7407", "dropbear", "2016.74",
             "CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
             "Dropbear dropbearconvert OpenSSH key import parsing flaw (RCE)."),
    ],
}


def _content_hash(records: dict) -> str:
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def main() -> None:
    snap = {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ecosystem": "NVD/CPE",
        "products": sorted(RECORDS.keys()),
        "content_hash": _content_hash(RECORDS),
        "records": RECORDS,
    }
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(json.dumps(snap, indent=2) + "\n")
    total = sum(len(v) for v in RECORDS.values())
    print(f"wrote {SNAPSHOT} — {len(RECORDS)} products, {total} CVE records")
    print(f"content_hash={snap['content_hash'][:16]}…")


if __name__ == "__main__":
    main()
