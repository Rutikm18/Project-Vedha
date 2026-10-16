"""risk_inputs.py — the ONE place that decides what goes into a finding's risk rank.

Three code paths used to build the rank's inputs differently:

* the findings LIST used neutral asset context (it never looked at the asset),
* the finding DETAIL used asset criticality but read exposure only from evidence,
* the stored ``risk_score`` (what "Highest risk" sorts on, and what the customer
  portal showed) was written by detection-time prioritisation, which passed
  ``cvss=0.0`` when no CVSS exists and took exposure from the asset's services.

So one finding could read 911 in the list, 936 in the detail and 831 in the portal.
Every path now calls :func:`risk_inputs` and then ``compute_risk_rank`` /
``explain_risk_rank``, so the number and its explanation are identical everywhere.

Rules (also what the explanation tells the reader):

* CVSS / EPSS: the recorded value, or ``None`` — never a made-up 0.0.
* Asset criticality: the finding's asset, or ``None`` when it has none.
* Internet exposure: the engine's recorded ``evidence.internet_facing`` when it is a
  boolean; otherwise derived from the asset's strongest service exposure
  (external/internet → exposed, internal/isolated → not exposed, partial/dmz or no
  data → unknown, which the formula treats as neutral).
* Authentication: ``evidence.auth_enforced`` when it is a boolean, else unknown.
"""
from __future__ import annotations

from typing import Any, Iterable

# Exposure strength: which service exposure counts for an asset with several services.
_EXPOSURE_RANK = {"external": 4, "internet": 4, "partial": 3, "dmz": 3,
                  "internal": 2, "isolated": 1}
_EXPOSED = {"external", "internet"}
_NOT_EXPOSED = {"internal", "isolated"}


def strongest_exposure(values: Iterable[str | None]) -> str | None:
    """The most-exposed value among an asset's services (external beats internal)."""
    ranked = [(v, _EXPOSURE_RANK.get((v or "").lower(), 0)) for v in values if v]
    return max(ranked, key=lambda t: t[1])[0] if ranked else None


def internet_facing_from_exposure(exposure: str | None) -> bool | None:
    value = (exposure or "").lower()
    if value in _EXPOSED:
        return True
    if value in _NOT_EXPOSED:
        return False
    return None


def _evidence(finding: Any) -> dict:
    ev = getattr(finding, "evidence", None)
    return ev if isinstance(ev, dict) else {}


def risk_inputs(finding: Any, *, asset_criticality: str | None = None,
                exposure: str | None = None) -> dict:
    """Keyword arguments for ``compute_risk_rank`` / ``explain_risk_rank``."""
    ev = _evidence(finding)
    enr = ev.get("enrichment") if isinstance(ev.get("enrichment"), dict) else {}
    recorded_exposure = ev.get("internet_facing")
    auth = ev.get("auth_enforced")
    cvss = getattr(finding, "cvss_score", None)
    epss = getattr(finding, "epss_score", None)
    return {
        "severity": str(getattr(finding.severity, "value", finding.severity)),
        "cvss_score": float(cvss) if cvss is not None else None,
        "epss_score": float(epss) if epss is not None else None,
        "kev": bool(ev.get("kev") or enr.get("kev")),
        "exploit_validated": bool(getattr(finding, "exploit_validated", False)),
        "verification_state": getattr(finding, "verification_state", None),
        "confidence": getattr(finding, "verification_confidence", None),
        "asset_criticality": asset_criticality,
        "internet_facing": (recorded_exposure if isinstance(recorded_exposure, bool)
                            else internet_facing_from_exposure(exposure)),
        "auth_enforced": auth if isinstance(auth, bool) else None,
    }


def exposure_source(finding: Any, exposure: str | None) -> str:
    """Where the internet-exposure input came from, for the explanation."""
    if isinstance(_evidence(finding).get("internet_facing"), bool):
        return "scan evidence"
    if internet_facing_from_exposure(exposure) is not None:
        return "asset service exposure"
    return "not recorded"
