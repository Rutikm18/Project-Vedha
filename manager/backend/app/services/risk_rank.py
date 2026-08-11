"""
risk_rank.py — one explainable 0-1000 priority for a finding.

Blends impact (severity/CVSS), exploit likelihood (EPSS/KEV), how sure we are
it's real (verification_state/confidence/exploit_validated), and where it lives
(asset criticality, exposure). Pure + deterministic: every factor is a named
multiplier a reviewer can reconstruct.
"""
from __future__ import annotations

_SEVERITY_BASE = {"critical": 900.0, "high": 700.0, "medium": 450.0, "low": 200.0, "info": 50.0}
_CRIT_MULT = {"critical": 1.2, "high": 1.1, "medium": 1.0, "low": 0.9}
_VERIFICATION_MULT = {"confirmed": 1.25, "corroborated": 1.0, "inferred": 0.8, "contradicted": 0.2}


def compute_risk_rank(*, severity: str, cvss_score: float | None, epss_score: float | None,
                      kev: bool, exploit_validated: bool, verification_state: str | None,
                      confidence: int | None, asset_criticality: str | None,
                      internet_facing: bool | None, auth_enforced: bool | None) -> int:
    # Impact: prefer CVSS when present, else the severity band.
    if cvss_score is not None:
        base = float(cvss_score) / 10.0 * 900.0
    else:
        base = _SEVERITY_BASE.get((severity or "info").lower(), 50.0)

    score = base

    # Exploit likelihood.
    if epss_score is not None:
        score *= 1.0 + 0.5 * max(0.0, min(1.0, float(epss_score)))
    if kev:
        score *= 1.3
    if exploit_validated:
        score *= 1.2

    # How sure we are it's real.
    score *= _VERIFICATION_MULT.get((verification_state or "corroborated").lower(), 1.0)
    if confidence is not None:
        score *= 0.4 + 0.6 * (max(0, min(100, int(confidence))) / 100.0)

    # Where it lives.
    score *= _CRIT_MULT.get((asset_criticality or "medium").lower(), 1.0)
    if internet_facing:
        score *= 1.15
    if auth_enforced:
        score *= 0.9

    return int(max(0.0, min(1000.0, round(score))))
