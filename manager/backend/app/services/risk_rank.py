"""One explainable, non-saturating 0-1000 Manager risk score.

The score is additive by design. Multiplying every risk amplifier made ordinary
critical findings hit 1000, erasing the distinction between "important" and
"maximum observed risk". The four named dimensions below always sum to 100%:

* impact (CVSS + severity): 40%
* exploit likelihood (EPSS + KEV + validated exploit): 25%
* asset/exposure context: 20%
* evidence quality (verification verdict + confidence): 15%

Severity is authoritative for ordering (FIRST CVSS v4 / SSVC keep severity apart
from priority): the additive score is rescaled into a per-severity band, so the
floor of a Critical is always above the ceiling of a High, and so on. Within a
band the additive score still ranks by exploit likelihood, context and evidence.

Missing contextual and evidence values are neutral, not silently treated as
either safe or dangerous. The function is pure and deterministic so a reviewer
can reconstruct every result.
"""
from __future__ import annotations

_SEVERITY_WEIGHT = {
    "critical": 1.0,
    "high": 0.8,
    "medium": 0.55,
    "low": 0.25,
    "info": 0.05,
}
_ASSET_WEIGHT = {"critical": 1.0, "high": 0.75, "medium": 0.5, "low": 0.25}
_VERIFICATION_WEIGHT = {
    "confirmed": 1.0,
    "corroborated": 0.75,
    "inferred": 0.45,
    "contradicted": 0.0,
}
_NEUTRAL = 0.5

# Inclusive (floor, ceiling) of the final 0-1000 rank per severity. Contiguous and
# non-overlapping, so rank order never contradicts severity order.
_SEVERITY_BAND = {
    "critical": (750, 1000),
    "high": (500, 749),
    "medium": (250, 499),
    "low": (100, 249),
    "info": (0, 99),
}


def _bounded(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def _components(*, severity, cvss_score, epss_score, kev, exploit_validated, verification_state,
                confidence, asset_criticality, internet_facing, auth_enforced) -> dict:
    """Every intermediate value of the rank, computed once. ``compute_risk_rank`` and
    ``explain_risk_rank`` both read this, so the number and its explanation cannot
    drift apart."""
    sev_key = (severity or "info").lower()
    if sev_key not in _SEVERITY_BAND:
        sev_key = "info"
    severity_n = _SEVERITY_WEIGHT[sev_key]
    if cvss_score is None:
        cvss_n = None
        impact_n = severity_n
    else:
        cvss_n = _bounded(float(cvss_score) / 10.0)
        # CVSS carries most of impact, while the Manager severity classification
        # remains a deliberate signal instead of becoming display-only metadata.
        impact_n = cvss_n * 0.8 + severity_n * 0.2

    epss_n = _bounded(float(epss_score)) if epss_score is not None else 0.0
    kev_n = float(bool(kev))
    validated_n = float(bool(exploit_validated))
    exploit_n = epss_n * 0.45 + kev_n * 0.35 + validated_n * 0.20

    asset_n = _ASSET_WEIGHT.get((asset_criticality or "").lower(), _NEUTRAL)
    exposure_n = _NEUTRAL if internet_facing is None else float(internet_facing)
    auth_gap_n = _NEUTRAL if auth_enforced is None else float(not auth_enforced)
    context_n = asset_n * 0.45 + exposure_n * 0.35 + auth_gap_n * 0.20

    verdict_n = _VERIFICATION_WEIGHT.get((verification_state or "").lower(), 0.65)
    confidence_n = _bounded(int(confidence) / 100.0) if confidence is not None else 0.65
    evidence_n = verdict_n * 0.60 + confidence_n * 0.40

    score = (
        impact_n * 0.40
        + exploit_n * 0.25
        + context_n * 0.20
        + evidence_n * 0.15
    ) * 1000.0
    position = _bounded(score / 1000.0)
    floor, ceiling = _SEVERITY_BAND[sev_key]
    return {
        "sev_key": sev_key, "severity_n": severity_n, "cvss_n": cvss_n, "impact_n": impact_n,
        "epss_n": epss_n, "kev_n": kev_n, "validated_n": validated_n, "exploit_n": exploit_n,
        "asset_n": asset_n, "exposure_n": exposure_n, "auth_gap_n": auth_gap_n, "context_n": context_n,
        "verdict_n": verdict_n, "confidence_n": confidence_n, "evidence_n": evidence_n,
        "raw": score, "position": position, "floor": floor, "ceiling": ceiling,
        "rank": int(round(floor + position * (ceiling - floor))),
    }


def compute_risk_rank(*, severity: str, cvss_score: float | None, epss_score: float | None,
                      kev: bool, exploit_validated: bool, verification_state: str | None,
                      confidence: int | None, asset_criticality: str | None,
                      internet_facing: bool | None, auth_enforced: bool | None) -> int:
    return _components(
        severity=severity, cvss_score=cvss_score, epss_score=epss_score, kev=kev,
        exploit_validated=exploit_validated, verification_state=verification_state,
        confidence=confidence, asset_criticality=asset_criticality,
        internet_facing=internet_facing, auth_enforced=auth_enforced,
    )["rank"]


MODEL_VERSION = "risk-rank-v1"
DIMENSION_WEIGHTS = {"impact": 0.40, "exploit": 0.25, "context": 0.20, "evidence": 0.15}


def _input(key: str, label: str, raw, normalized: float, weight: float, source: str, note: str) -> dict:
    """One factor of a dimension. ``source`` is ``recorded`` (a real value was used),
    ``default`` (nothing recorded, the documented neutral value was used instead) or
    ``derived``. Never presented as recorded when it was not."""
    return {"key": key, "label": label, "raw": raw, "normalized": round(normalized, 4),
            "weight": weight, "contribution": round(normalized * weight, 4),
            "source": source, "note": note}


def explain_risk_rank(*, severity: str, cvss_score: float | None, epss_score: float | None,
                      kev: bool, exploit_validated: bool, verification_state: str | None,
                      confidence: int | None, asset_criticality: str | None,
                      internet_facing: bool | None, auth_enforced: bool | None) -> dict:
    """The full, reproducible working of ``compute_risk_rank`` for one finding.

    Reading order: each input is normalised to 0-1 and weighted inside its dimension;
    the four dimensions are weighted (40/25/20/15) into a 0-1000 additive score; that
    score is placed inside the finding's severity band to give the final rank. Inputs
    that were not recorded are marked ``default`` with the neutral value actually used.
    """
    c = _components(
        severity=severity, cvss_score=cvss_score, epss_score=epss_score, kev=kev,
        exploit_validated=exploit_validated, verification_state=verification_state,
        confidence=confidence, asset_criticality=asset_criticality,
        internet_facing=internet_facing, auth_enforced=auth_enforced)
    sev = c["sev_key"]

    impact_inputs = [_input("severity", "Severity class", sev, c["severity_n"],
                            1.0 if cvss_score is None else 0.2, "recorded",
                            "Critical 1.00 · High 0.80 · Medium 0.55 · Low 0.25 · Info 0.05")]
    if cvss_score is None:
        impact_inputs.append(_input("cvss", "CVSS base score", None, 0.0, 0.0, "default",
                                    "No CVSS recorded, so impact is the severity class alone"))
    else:
        impact_inputs.insert(0, _input("cvss", "CVSS base score", float(cvss_score), c["cvss_n"], 0.8,
                                       "recorded", "Score ÷ 10"))
    epss_recorded = epss_score is not None
    exploit_inputs = [
        _input("epss", "EPSS (probability of exploitation)", float(epss_score) if epss_recorded else None,
               c["epss_n"], 0.45, "recorded" if epss_recorded else "default",
               "Probability 0-1" if epss_recorded else "Not recorded; counted as 0, not as safe"),
        _input("kev", "Listed in CISA KEV", bool(kev), c["kev_n"], 0.35, "recorded",
               "1 if the CVE is on the Known Exploited Vulnerabilities list, else 0"),
        _input("exploit_validated", "Exploit validated in this assessment", bool(exploit_validated),
               c["validated_n"], 0.20, "recorded", "1 if a safe exploit check confirmed it, else 0"),
    ]
    crit_known = (asset_criticality or "").lower() in _ASSET_WEIGHT
    context_inputs = [
        _input("asset_criticality", "Asset criticality", asset_criticality if crit_known else None,
               c["asset_n"], 0.45, "recorded" if crit_known else "default",
               "Critical 1.00 · High 0.75 · Medium 0.50 · Low 0.25" if crit_known
               else "Not recorded; neutral 0.50 used"),
        _input("internet_facing", "Internet-facing", internet_facing, c["exposure_n"], 0.35,
               "recorded" if internet_facing is not None else "default",
               "1 if reachable from the internet, else 0" if internet_facing is not None
               else "Not recorded; neutral 0.50 used"),
        _input("auth_gap", "Authentication gap", None if auth_enforced is None else (not auth_enforced),
               c["auth_gap_n"], 0.20, "recorded" if auth_enforced is not None else "default",
               "1 if no authentication is enforced, else 0" if auth_enforced is not None
               else "Not recorded; neutral 0.50 used"),
    ]
    verdict_known = (verification_state or "").lower() in _VERIFICATION_WEIGHT
    evidence_inputs = [
        _input("verification", "Verification verdict", verification_state if verdict_known else None,
               c["verdict_n"], 0.60, "recorded" if verdict_known else "default",
               "Confirmed 1.00 · Corroborated 0.75 · Inferred 0.45 · Contradicted 0.00" if verdict_known
               else "Not verified; 0.65 used"),
        _input("confidence", "Detection confidence", confidence, c["confidence_n"], 0.40,
               "recorded" if confidence is not None else "default",
               "Percent ÷ 100" if confidence is not None else "Not recorded; 0.65 used"),
    ]

    dims = []
    for key, label, value, inputs in (
        ("impact", "Impact", c["impact_n"], impact_inputs),
        ("exploit", "Exploit likelihood", c["exploit_n"], exploit_inputs),
        ("context", "Asset and exposure context", c["context_n"], context_inputs),
        ("evidence", "Evidence quality", c["evidence_n"], evidence_inputs),
    ):
        w = DIMENSION_WEIGHTS[key]
        dims.append({"key": key, "label": label, "weight": w, "value": round(value, 4),
                     "points": round(value * w * 1000.0, 1), "inputs": inputs})

    return {
        "model_version": MODEL_VERSION,
        "score": c["rank"], "max": 1000,
        "severity": sev,
        "dimensions": dims,
        "additive_score": round(c["raw"], 1),
        "band": {"floor": c["floor"], "ceiling": c["ceiling"], "position": round(c["position"], 4)},
        "placement": {
            "formula": "floor + position × (ceiling − floor)",
            "result": c["rank"],
        },
        "defaults_used": [i["key"] for d in dims for i in d["inputs"] if i["source"] == "default"],
    }
