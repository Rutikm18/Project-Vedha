"""
online.py — OPT-IN live enrichment for CVE findings.

The offline mirror (vulndb) is authoritative and is the default path; NOTHING in
this module runs unless the operator explicitly passes `--online`. Two live
sources augment a finding the offline mirror could not fully resolve:

  * NVD 2.0 (by cveId) — authoritative CVSS + references + published date. Used to
    FILL a finding whose CVSS the mirror lacked (a mirror gap, or a CVE published
    since the last ingest) and to cross-check the mirror's score when it is stale.
  * Vulners (by cveId, requires an API key) — whether a public EXPLOIT is
    catalogued, a signal the offline mirror does not carry.

Design invariants:
  * Offline-first. An online pass can only ADD signal to the offline result; it
    never breaks the run and never overwrites a value the mirror already holds
    (on a mismatch it annotates, it does not replace — the mirror stays
    reproducible). A live CVSS only FILLS a gap the mirror left empty.
  * Fail-open. Every network / parse error degrades to a no-op for that CVE, so a
    box with no egress produces exactly the offline result.
  * Probe never does this. Enrichment is a manager-side, CLI-only, explicitly
    opted-into step — it is deliberately NOT wired into the sealed campaign path.

The HTTP getter is injectable (`get=`) so the whole module is unit-testable with
no network: tests pass a fake `get` returning canned feed bytes.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

from .correlator import CVEFinding, risk_band, risk_score
from .ingest import NVD_URL, _cvss, _get

# The default transport reuses ingest's certifi-backed, backoff-retrying getter so
# online lookups honour the same TLS/rate-limit posture as a mirror build. Tests
# monkeypatch these module attributes (or pass get=/sleep=) to stay offline.
DEFAULT_GET: Callable[..., bytes] = _get
DEFAULT_SLEEP: Callable[[float], None] = time.sleep

VULNERS_ID_URL = "https://vulners.com/api/v3/search/id/"
# Vulners bulletin families / types that denote a runnable public exploit.
_EXPLOIT_TYPES = {"exploitdb", "metasploit", "packetstorm", "zdt", "canvas",
                  "saint", "d2", "seebug", "githubexploit"}


@dataclass
class OnlineResult:
    """What a live lookup could establish for one CVE (any field may be None when
    the source did not carry it or the query failed)."""
    cve_id: str
    cvss_score: float | None = None
    cvss_severity: str | None = None
    published: str | None = None
    references: list[str] = field(default_factory=list)
    exploit_available: bool | None = None   # from vulners; None = not queried/unknown
    source: str = ""                          # "nvd" / "vulners" / "nvd+vulners"
    error: str | None = None


# ── single-CVE live lookups (each fail-open: returns None / empty on any error) ─
def lookup_nvd(cve_id: str, *, api_key: str | None = None,
               get: Callable[..., bytes] | None = None,
               timeout: float = 30.0) -> OnlineResult | None:
    """Query live NVD 2.0 for one CVE. Returns an OnlineResult, or None on any
    network/parse failure (fail-open — the offline result stands)."""
    get = get or DEFAULT_GET
    headers = {"apiKey": api_key} if api_key else None
    try:
        raw = get(NVD_URL, params={"cveId": cve_id}, headers=headers, timeout=timeout)
        page = json.loads(raw)
        vulns = page.get("vulnerabilities") or []
        if not vulns:
            return None
        cve = vulns[0].get("cve", {})
        score, sev, _vec = _cvss(cve.get("metrics", {}))
        refs = [r.get("url") for r in cve.get("references", [])
                if isinstance(r, dict) and r.get("url")]
        return OnlineResult(
            cve_id=cve.get("id", cve_id), cvss_score=score, cvss_severity=sev,
            published=cve.get("published"), references=refs, source="nvd")
    except Exception as e:                       # noqa: BLE001 — fail-open by design
        return None if isinstance(e, (KeyboardInterrupt, SystemExit)) else \
            OnlineResult(cve_id=cve_id, source="nvd", error=str(e))


def lookup_vulners(cve_id: str, *, api_key: str | None,
                   get: Callable[..., bytes] | None = None,
                   timeout: float = 30.0) -> bool | None:
    """Ask Vulners whether a public exploit is catalogued for `cve_id`. Returns
    True/False, or None when unknowable (no key, network/parse error). Parsed
    defensively — Vulners' schema is deep and any deviation degrades to None."""
    if not api_key:
        return None
    get = get or DEFAULT_GET
    try:
        raw = get(VULNERS_ID_URL,
                  params={"id": cve_id, "references": "true", "apiKey": api_key},
                  headers={"Accept": "application/json"}, timeout=timeout)
        page = json.loads(raw)
        if page.get("result") not in (None, "OK"):
            return None
        docs = (((page.get("data") or {}).get("documents")) or {})
        entry = docs.get(cve_id) or {}
        # Explicit exploit-reference block is the strongest signal…
        refs = entry.get("references") or {}
        for fam in refs:
            if str(fam).lower() in _EXPLOIT_TYPES:
                return True
        # …else fall back to any related document flagged as an exploit family.
        for rel in entry.get("related", {}).get("all", []) if isinstance(
                entry.get("related"), dict) else []:
            if str(rel.get("type", "")).lower() in _EXPLOIT_TYPES:
                return True
            if str(rel.get("bulletinFamily", "")).lower() == "exploit":
                return True
        return False
    except Exception as e:                       # noqa: BLE001 — fail-open by design
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            raise
        return None


# ── enrichment pass over a batch of already-correlated findings ────────────────
def enrich_findings(findings: list[CVEFinding], *, api_key: str | None = None,
                    vulners_key: str | None = None,
                    get: Callable[..., bytes] | None = None,
                    sleep: Callable[[float], None] | None = None,
                    only_missing: bool = True,
                    log: Callable[[str], None] = lambda _m: None) -> list[CVEFinding]:
    """Enrich CVE findings in place from live sources and return the same list.

    `only_missing` (default) queries ONLY findings whose CVSS the offline mirror
    left empty — the mirror-gap case, where online adds the most and costs the
    least. Set it False to also cross-check findings the mirror DID score (live
    CVSS is compared, never overwritten — a divergence is annotated so a stale
    mirror is visible without breaking reproducibility).

    Lookups are cached and rate-limited per distinct cve_id, so N findings on the
    same CVE cost one request. On any failure the finding is left exactly as the
    offline pass produced it."""
    get = get or DEFAULT_GET
    sleep = sleep or DEFAULT_SLEEP
    delay = 0.6 if api_key else 6.0            # match NVD's keyed / anon rate limits
    cache: dict[str, OnlineResult | None] = {}
    exploit_cache: dict[str, bool | None] = {}
    queried = 0
    enriched = 0

    for f in findings:
        want = only_missing is False or f.cvss_score is None
        if not want:
            continue
        cid = f.cve_id
        if cid not in cache:
            if queried and (cid not in exploit_cache):
                sleep(delay)                   # space out DISTINCT live requests only
            cache[cid] = lookup_nvd(cid, api_key=api_key, get=get)
            if vulners_key:
                exploit_cache[cid] = lookup_vulners(cid, api_key=vulners_key, get=get)
            queried += 1
        res = cache[cid]
        exploit = exploit_cache.get(cid)
        if _apply(f, res, exploit):
            enriched += 1

    log(f"online: queried {queried} CVE(s), enriched {enriched} finding(s)")
    return findings


def _apply(f: CVEFinding, res: OnlineResult | None, exploit: bool | None) -> bool:
    """Fold one CVE's live result into a finding. FILLS a missing CVSS (and
    recomputes risk); ANNOTATES a mismatch rather than overwriting. Returns True
    if anything changed."""
    changed = False
    info: dict[str, Any] = f.extra.setdefault("online", {})
    if res and res.error is None and res.cvss_score is not None:
        if f.cvss_score is None:
            f.cvss_score = res.cvss_score
            f.cvss_severity = res.cvss_severity or f.cvss_severity
            f.risk_score = risk_score(f.cvss_score, f.kev, f.epss, _was_exposed(f))
            f.risk_band = risk_band(f.risk_score)
            f.evidence += (f" Live NVD lookup supplied CVSS {res.cvss_score} "
                           f"({res.cvss_severity or 'n/a'}) — the offline mirror "
                           "lacked this CVE (gap); re-ingest to persist it.")
            info.update(filled_cvss=True, published=res.published,
                        references=res.references[:8], source="nvd")
            changed = True
        elif abs((f.cvss_score or 0) - res.cvss_score) >= 0.1:
            f.evidence += (f" Live NVD CVSS {res.cvss_score} differs from the "
                           f"mirror's {f.cvss_score} — the offline mirror may be "
                           "stale; re-ingest to refresh.")
            info.update(cvss_mismatch=True, live_cvss=res.cvss_score, source="nvd")
            changed = True
        elif res.references:
            info.setdefault("references", res.references[:8])
            info.setdefault("source", "nvd")
    if exploit is True:
        f.evidence += (" Vulners reports a PUBLIC EXPLOIT is catalogued for this "
                       "CVE — treat as actively weaponizable.")
        info["exploit_available"] = True
        info["source"] = ("nvd+vulners" if info.get("source") == "nvd" else "vulners")
        changed = True
    elif exploit is False:
        info.setdefault("exploit_available", False)
    if not info:
        f.extra.pop("online", None)
    return changed


def _was_exposed(f: CVEFinding) -> bool:
    """Recover whether the exposure boost was applied, so a re-scored (gap-filled)
    finding keeps its exposure weighting. The correlator adds +15 for exposure;
    without the original flag we conservatively infer it from the evidence, which
    names the exposure when it was counted."""
    return "exposed" in (f.evidence or "").lower() or bool(
        f.extra.get("exposed") or f.extra.get("internet_exposed"))
