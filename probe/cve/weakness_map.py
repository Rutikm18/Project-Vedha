"""
weakness_map.py — bridge the probe's deterministic weakness findings to canonical,
globally-tracked CVEs.

The probe's `detect` stage (scanner/findings.py) concludes weaknesses it DIRECTLY
observed — "SMBv1 is enabled", "the SSH transcript is Terrapin-affected", "IPMI
offers cipher suite 0". Those are configuration/protocol facts, deliberately NOT
CVE claims (the collection-layer boundary). But several of those weaknesses ARE the
exact precondition for a NAMED, catalogued vulnerability: SMBv1 is the transport
EternalBlue (CVE-2017-0144 / MS17-010) exploits; a Terrapin-affected transcript IS
CVE-2023-48795; IPMI cipher-0 IS the CVE-2013-4786 class. This module carries that
curated, citable association and — critically — pulls the *live* CVSS / KEV / EPSS
for each canonical CVE from the SAME offline mirror the CPE correlator uses, so the
risk score reflects today's exploitation reality rather than a hard-coded number.

Boundary kept intact:
  * findings.py still emits ONLY weaknesses (no cve_id). This mapping lives in the
    cve/ layer (manager-side), exactly like the CPE correlator.
  * The association starts from an OBSERVED weakness (high structural confidence),
    but whether the specific patch is applied is NOT visible from the wire, so an
    `exploitability` tier is attached per mapping and always explained in evidence.
    A mapping never silently upgrades to "confirmed".
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

from .correlator import CVEFinding, risk_band, risk_score
from .vulndb import VulnDB

_ALWAYS: Callable[[dict], bool] = lambda _d: True


@dataclass(frozen=True)
class _Assoc:
    """One canonical CVE a weakness can map to, optionally gated on the finding's
    structured `data` (e.g. SSLv3 -> POODLE, SSLv2 -> DROWN from the same rule)."""
    cve_id: str
    note: str
    applies: Callable[[dict], bool] = _ALWAYS


@dataclass(frozen=True)
class WeaknessMapping:
    exploitability: str        # confidence the named CVE is actually exploitable here
    rationale: str             # why this observed weakness implies these CVE(s)
    assocs: tuple[_Assoc, ...]


def _has_version(data: dict, token: str) -> bool:
    vers = data.get("accepted_versions") or []
    return token in {str(v).upper().replace(" ", "") for v in vers}


# ── the curated map: weakness rule_id -> canonical CVE(s) ─────────────────────
# Every entry is domain knowledge a version-range CPE match cannot express: the
# weakness IS the exploit precondition for a specifically-named vulnerability.
WEAKNESS_CVES: dict[str, WeaknessMapping] = {
    "SMB-V1-ENABLED": WeaknessMapping(
        exploitability="medium",
        rationale=("SMBv1 is enabled. SMBv1 is the protocol EternalBlue (MS17-010) "
                   "exploits for unauthenticated remote code execution — the vector "
                   "WannaCry and NotPetya weaponised. The surface is confirmed; the "
                   "MS17-010 patch level is not visible from the wire."),
        assocs=(_Assoc("CVE-2017-0144",
                       "EternalBlue / MS17-010 — wormable pre-auth RCE over SMBv1."),),
    ),
    "SSH-TERRAPIN": WeaknessMapping(
        exploitability="high",
        rationale=("The SSH transcript offers a Terrapin-affected mode "
                   "(ChaCha20-Poly1305 or CBC-EtM) without strict key exchange. The "
                   "negotiated algorithms directly prove the prefix-truncation attack "
                   "applies."),
        assocs=(_Assoc("CVE-2023-48795",
                       "Terrapin — SSH prefix-truncation / handshake downgrade."),),
    ),
    "IPMI-CIPHER-ZERO": WeaknessMapping(
        exploitability="high",
        rationale=("The BMC accepted an IPMI 2.0 session with cipher suite 0 (no "
                   "authentication). This is the catalogued IPMI 2.0 authentication "
                   "weakness — an administrative session with no credentials."),
        assocs=(_Assoc("CVE-2013-4786",
                       "IPMI 2.0 cipher-suite-0 / RAKP authentication weakness."),),
    ),
    "TLS-OBSOLETE-PROTO": WeaknessMapping(
        exploitability="medium",
        rationale=("The endpoint negotiates a cryptographically broken SSL/TLS "
                   "version. SSLv3 is exploitable by POODLE; SSLv2 by DROWN."),
        assocs=(
            _Assoc("CVE-2014-3566",
                   "POODLE — SSLv3 CBC padding-oracle plaintext recovery.",
                   applies=lambda d: _has_version(d, "SSLV3")),
            _Assoc("CVE-2016-0800",
                   "DROWN — SSLv2 cross-protocol attack on shared RSA keys.",
                   applies=lambda d: _has_version(d, "SSLV2")),
        ),
    ),
    "UDP-NTP-MONLIST": WeaknessMapping(
        exploitability="medium",
        rationale=("The NTP server answered the monlist query — a very high-factor "
                   "spoofed-source DDoS reflector."),
        assocs=(_Assoc("CVE-2013-5211",
                       "ntpd monlist (MODE 7) traffic-amplification DDoS."),),
    ),
    "SVC-RDP-NO-NLA": WeaknessMapping(
        exploitability="low",
        rationale=("RDP negotiated without Network Level Authentication (CredSSP). "
                   "NLA is the mitigation for BlueKeep; its absence leaves the "
                   "pre-authentication RDP stack reachable. This flags a removed "
                   "mitigation, not a confirmed patch level."),
        assocs=(_Assoc("CVE-2019-0708",
                       "BlueKeep — pre-auth RDP RCE; mitigated by NLA when unpatched."),),
    ),
}


# ── finding extraction (accepts both fact shapes) ─────────────────────────────
def _finding_view(fact: Any) -> dict | None:
    """Return the Finding dict from a fact, or None if the fact is not a finding.

    Two shapes reach us: a raw Finding dict (findings.py `--json`) whose own
    `type` is "finding", or a ScanResult-wrapped finding (the detect stage emits
    `ScanResult("findings", ..., data=Finding.to_dict())`) whose `data.type` is
    "finding". Normalise both to the inner finding view."""
    if isinstance(fact, dict):
        f = fact
    else:
        import json
        to_json = getattr(fact, "to_json", None)
        f = json.loads(fact.to_json()) if callable(to_json) else {}
    if f.get("type") == "finding" and f.get("rule_id"):
        return f
    data = f.get("data")
    if isinstance(data, dict) and data.get("type") == "finding" and data.get("rule_id"):
        return data
    return None


def _mirror_cve(db: VulnDB | None, cve_id: str) -> dict:
    """Pull CVSS/KEV/EPSS for one CVE straight from the mirror tables. Degrades to
    all-None when the mirror is absent or doesn't carry the CVE (we still emit the
    mapping — with a note — because the weakness itself was observed)."""
    if db is None:
        return {"present": False}
    cve = db.conn.execute(
        "SELECT cvss_score, cvss_severity FROM cve WHERE cve_id=?", (cve_id,)).fetchone()
    kev = db.conn.execute("SELECT date_added FROM kev WHERE cve_id=?", (cve_id,)).fetchone()
    epss = db.conn.execute(
        "SELECT epss, percentile FROM epss WHERE cve_id=?", (cve_id,)).fetchone()
    return {
        "present": cve is not None,
        "cvss_score": cve["cvss_score"] if cve else None,
        "cvss_severity": cve["cvss_severity"] if cve else None,
        "kev": kev is not None,
        "kev_date": kev["date_added"] if kev else None,
        "epss": epss["epss"] if epss else None,
        "epss_percentile": epss["percentile"] if epss else None,
    }


def correlate_weaknesses(facts: Iterable[Any], db: VulnDB | None, *,
                         exposed_targets: set[str] | None = None) -> list[CVEFinding]:
    """Map observed weakness findings to their canonical CVE(s), enriched with live
    CVSS/KEV/EPSS from the offline mirror. Complements `correlate()` (the CPE
    version-range path): this path fires on DIRECTLY-observed weaknesses, so it
    reaches vulnerabilities a banner version never reveals. Deduped by
    (cve_id, target, port); highest-risk first."""
    exposed = set(exposed_targets or [])
    out: list[CVEFinding] = []
    seen: set[tuple] = set()
    for raw in facts:
        fnd = _finding_view(raw)
        if fnd is None:
            continue
        mapping = WEAKNESS_CVES.get(fnd["rule_id"])
        if mapping is None:
            continue
        data = fnd.get("data") if isinstance(fnd.get("data"), dict) else {}
        target, port = fnd.get("target"), fnd.get("port")
        is_exposed = target in exposed
        for assoc in mapping.assocs:
            if not assoc.applies(data):
                continue
            key = (assoc.cve_id, target, port)
            if key in seen:
                continue
            seen.add(key)
            m = _mirror_cve(db, assoc.cve_id)
            rs = risk_score(m.get("cvss_score"), m.get("kev"), m.get("epss"), is_exposed)
            evidence = (
                f"Observed weakness {fnd['rule_id']} maps to {assoc.cve_id}: "
                f"{assoc.note} {mapping.rationale}"
                + (f" [CVSS {m['cvss_score']}" if m.get("cvss_score") is not None else "")
                + (", KEV actively-exploited" if m.get("kev") else "")
                + (f", EPSS {m['epss']}" if m.get("epss") is not None else "")
                + ("]" if m.get("cvss_score") is not None else ""))
            if not m.get("present"):
                evidence += (" (this CVE is not in the offline mirror — CVSS/KEV/EPSS "
                             "unavailable; refresh the mirror with `python -m cve.cli "
                             "ingest`.)")
            out.append(CVEFinding(
                cve_id=assoc.cve_id, target=target, port=port,
                matched_cpe=None, product=None, version=None,
                cvss_score=m.get("cvss_score"), cvss_severity=m.get("cvss_severity"),
                kev=bool(m.get("kev")), kev_date=m.get("kev_date"),
                epss=m.get("epss"), epss_percentile=m.get("epss_percentile"),
                confidence=mapping.exploitability, risk_score=rs, risk_band=risk_band(rs),
                evidence=evidence, source_scanner="weakness_map",
                extra={"weakness_rule_id": fnd["rule_id"],
                       "mapping": "weakness->cve"}))
    return sorted(out, key=lambda x: x.risk_score, reverse=True)


def missing_from_mirror(db: VulnDB) -> list[str]:
    """Every canonical CVE referenced by the weakness map that the mirror does NOT
    carry — a concrete coverage gap the `status` verb reports (a stale/partial
    mirror silently drops the CVSS/KEV/EPSS enrichment for these mappings)."""
    wanted = sorted({a.cve_id for m in WEAKNESS_CVES.values() for a in m.assocs})
    return [c for c in wanted
            if db.conn.execute("SELECT 1 FROM cve WHERE cve_id=?", (c,)).fetchone() is None]
