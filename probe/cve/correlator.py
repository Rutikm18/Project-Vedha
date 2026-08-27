"""
correlator.py — map probe facts to prioritized CVE findings.

Consumes the CPE identity the probe attached to service_banner facts
(cpe_vendor / cpe_product / cpe_version) and the offline VulnDB, and emits CVE
findings that are:
  * evidence-backed — each cites the exact CPE/version it matched;
  * confidence-tiered — a banner-derived version is `medium` at most (distro
    backports patch without bumping the version), tagged "verify patch level";
    the correlator never ASSERTS a CVE from a banner;
  * risk-scored — CVSS + KEV (actively-exploited) + EPSS (exploit probability) +
    internet-exposure (from vantage data, when supplied) → the 20 that matter,
    not the 10,000 that merely match.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Any, Iterable

from .vulndb import VulnDB

# A mirror older than this is flagged: NVD/KEV/EPSS move daily, so a stale mirror
# silently misses newly-published and newly-exploited CVEs.
STALE_DAYS = 7


def mirror_age_note(db: VulnDB, *, stale_days: int = STALE_DAYS) -> str:
    """Human-readable note on how old the mirror is (from meta.last_ingest_utc),
    prefixed WARNING past `stale_days`. Degrades gracefully when the stamp is
    missing (pre-stamping mirror) or unparseable. Shared by cli.correlate and
    run_all so both surface the same signal."""
    stamp = db.get_meta("last_ingest_utc")
    if not stamp:
        return "mirror age: unknown (built before staleness stamping — re-ingest)"
    try:
        when = datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return f"mirror age: unknown (unparseable stamp {stamp!r})"
    days = (datetime.now(timezone.utc) - when).total_seconds() / 86400
    note = f"mirror last refreshed {stamp} ({days:.1f} days ago)"
    if days >= stale_days:
        note = f"WARNING: STALE — {note}; re-run `cve.cli ingest` (>{stale_days}d old)"
    return note

# Distro/backport markers in a raw banner. When present, the upstream version
# string is unreliable for CVE matching: distributions backport security fixes
# into a pinned upstream version WITHOUT bumping it (e.g. "OpenSSH_7.4p1 Debian-
# 10+deb9u7" carries fixes 7.4p1 never shipped upstream). A match against such a
# version over-reports, so we downgrade confidence and say why.
_BACKPORT_RE = re.compile(r"(?:ubuntu|debian|raspbian|\+dfsg|\+deb|\.el\d)",
                          re.IGNORECASE)


def _backport_marker(banner: str | None) -> str | None:
    """Return the distro-backport token found in the banner, else None."""
    m = _BACKPORT_RE.search(str(banner or ""))
    return m.group(0) if m else None


def risk_score(cvss: float | None, kev: bool, epss: float | None, exposed: bool) -> int:
    """0–100 prioritization score. CVSS is halved so it can't dominate; KEV and
    internet-exposure add fixed weight; EPSS scales exploit likelihood."""
    score = 0.5 * (cvss or 0) * 10          # CVSS 0–10 -> 0–50
    score += 30 if kev else 0               # actively exploited
    score += 20 * (epss or 0)               # 0–20 by exploit probability
    score += 15 if exposed else 0           # reachable from the internet
    return min(100, round(score))


def risk_band(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


@dataclass
class CVEFinding:
    cve_id: str
    target: str | None
    port: int | None
    matched_cpe: str | None
    product: str | None
    version: str | None
    cvss_score: float | None
    cvss_severity: str | None
    kev: bool
    kev_date: str | None
    epss: float | None
    epss_percentile: float | None
    confidence: str
    risk_score: int
    risk_band: str
    evidence: str
    source_scanner: str | None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = {k: getattr(self, k) for k in (
            "cve_id", "target", "port", "matched_cpe", "product", "version",
            "cvss_score", "cvss_severity", "kev", "kev_date", "epss",
            "epss_percentile", "confidence", "risk_score", "risk_band",
            "evidence", "source_scanner")}
        d["type"] = "cve_finding"
        return d


def _as_dict(fact) -> dict:
    if isinstance(fact, dict):
        return fact
    import json
    to_json = getattr(fact, "to_json", None)
    return json.loads(fact.to_json()) if callable(to_json) else {}


def correlate(facts: Iterable[Any], db: VulnDB, *,
              exposed_targets: set[str] | None = None) -> list[CVEFinding]:
    """Correlate facts carrying a CPE identity against the vuln DB. Deduped by
    (cve_id, target, port); returned highest-risk first."""
    exposed = set(exposed_targets or [])
    out: list[CVEFinding] = []
    seen: set[tuple] = set()
    for raw in facts:
        f = _as_dict(raw)
        d = f.get("data") if isinstance(f.get("data"), dict) else {}
        vendor, product, version = d.get("cpe_vendor"), d.get("cpe_product"), d.get("cpe_version")
        if not (vendor and product and version):
            continue
        target, port = f.get("target"), f.get("port")
        is_exposed = target in exposed
        # A distro-backport marker in the banner weakens every version-based
        # match for this fact: confidence drops to "low" and the evidence says so.
        backport = _backport_marker(d.get("banner"))
        confidence = "low" if backport else "medium"
        for cve in db.cves_for_cpe(vendor, product, version):
            key = (cve["cve_id"], target, port)
            if key in seen:
                continue
            seen.add(key)
            rs = risk_score(cve.get("cvss_score"), cve.get("kev"), cve.get("epss"), is_exposed)
            evidence = (
                f"{d.get('cpe')} matches {cve['cve_id']} "
                f"(CVSS {cve.get('cvss_score')}"
                + (", KEV actively-exploited" if cve.get("kev") else "")
                + (f", EPSS {cve.get('epss')}" if cve.get("epss") is not None else "")
                + f"). Version {version} was read from a banner — verify against the "
                "distro patch level before treating as confirmed.")
            if backport:
                evidence += (
                    f" Banner carries a distro-backport marker ('{backport}'): the "
                    "distribution may have patched this without bumping the upstream "
                    "version, so this match likely over-reports — confidence low.")
            out.append(CVEFinding(
                cve_id=cve["cve_id"], target=target, port=port,
                matched_cpe=d.get("cpe"), product=product, version=version,
                cvss_score=cve.get("cvss_score"), cvss_severity=cve.get("cvss_severity"),
                kev=bool(cve.get("kev")), kev_date=cve.get("kev_date"),
                epss=cve.get("epss"), epss_percentile=cve.get("epss_percentile"),
                confidence=confidence, risk_score=rs, risk_band=risk_band(rs),
                evidence=evidence, source_scanner=f.get("scanner")))
    return sorted(out, key=lambda x: x.risk_score, reverse=True)


def summarize(findings: list[CVEFinding]) -> dict:
    bands = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        bands[f.risk_band] = bands.get(f.risk_band, 0) + 1
    return {
        "total": len(findings),
        "by_risk_band": bands,
        "kev": sum(1 for f in findings if f.kev),
        "top_cve": findings[0].cve_id if findings else None,
    }
