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


def compute_risk_rank(*, severity: str, cvss_score: float | None, epss_score: float | None,
                      kev: bool, exploit_validated: bool, verification_state: str | None,
                      confidence: int | None, asset_criticality: str | None,
                      internet_facing: bool | None, auth_enforced: bool | None) -> int:
    sev_key = (severity or "info").lower()
    if sev_key not in _SEVERITY_BAND:
        sev_key = "info"
    severity_n = _SEVERITY_WEIGHT[sev_key]
    if cvss_score is None:
        impact_n = severity_n
    else:
        cvss_n = _bounded(float(cvss_score) / 10.0)
        # CVSS carries most of impact, while the Manager severity classification
        # remains a deliberate signal instead of becoming display-only metadata.
        impact_n = cvss_n * 0.8 + severity_n * 0.2

    epss_n = _bounded(float(epss_score)) if epss_score is not None else 0.0
    exploit_n = epss_n * 0.45 + float(bool(kev)) * 0.35 + float(bool(exploit_validated)) * 0.20

    asset_n = _ASSET_WEIGHT.get((asset_criticality or "").lower(), _NEUTRAL)
    exposure_n = _NEUTRAL if internet_facing is None else float(internet_facing)
    auth_gap_n = _NEUTRAL if auth_enforced is None else float(not auth_enforced)
    context_n = asset_n * 0.45 + exposure_n * 0.35 + auth_gap_n * 0.20

    verdict_n = _VERIFICATION_WEIGHT.get(
        (verification_state or "").lower(),
        0.65,
    )
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
    return int(round(floor + position * (ceiling - floor)))
