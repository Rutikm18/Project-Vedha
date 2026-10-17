"""
ssvc.py — CISA SSVC decision for a CVE finding (the prioritisation BOD 26-04 uses).

BOD 26-04 (10 Jun 2026) ranks remediation by asset exposure, KEV status, Exploit
Automation ("Automatable") and Technical Impact — the CISA SSVC decision points.
KEV > EPSS > CVSS alone (enrichment._compute_priority) cannot say "Act" vs "Track";
this module adds that answer next to the existing priority, without changing it.

Inputs, most authoritative first, each recorded with where it came from:
  Exploitation      KEV-listed -> active; else CISA Vulnrichment; else "none"
  Automatable       CISA Vulnrichment; else derived from the CVSS vector
                    (network, low complexity, no privileges, no user interaction)
  Technical Impact  CISA Vulnrichment; else derived (high confidentiality AND
                    integrity impact = total control)
  Mission & Well-being  "high" for an internet-facing asset, else "medium" (the
                    engine has no asset criticality; the manager can re-decide
                    with it from the stored inputs via decide()).

Pure and offline: the Vulnrichment values come from snapshots/ssvc_snapshot.json,
written only by update_snapshot.py. A missing snapshot means every input is
derived, never an error.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

from cvss import parse_vector
from intel_paths import resolve
from update_snapshot import DEFAULT_SSVC_PATH

# CISA SSVC decision tree (CISA "Stakeholder-Specific Vulnerability Categorization
# Guide", Nov 2022): (exploitation, technical_impact, automatable) -> decision for
# mission & well-being (low, medium, high). Track* = track closely.
_TREE: dict[tuple[str, str, str], tuple[str, str, str]] = {
    ("none", "partial", "no"):    ("Track", "Track", "Track"),
    ("none", "partial", "yes"):   ("Track", "Track", "Attend"),
    ("none", "total", "no"):      ("Track", "Track", "Track*"),
    ("none", "total", "yes"):     ("Track", "Track", "Attend"),
    ("poc", "partial", "no"):     ("Track", "Track", "Track*"),
    ("poc", "partial", "yes"):    ("Track", "Track", "Attend"),
    ("poc", "total", "no"):       ("Track", "Track*", "Attend"),
    ("poc", "total", "yes"):      ("Track", "Track*", "Attend"),
    ("active", "partial", "no"):  ("Track", "Track", "Attend"),
    ("active", "partial", "yes"): ("Attend", "Attend", "Act"),
    ("active", "total", "no"):    ("Track", "Attend", "Act"),
    ("active", "total", "yes"):   ("Attend", "Act", "Act"),
}
_MWB_INDEX = {"low": 0, "medium": 1, "high": 2}
DECISIONS = ("Track", "Track*", "Attend", "Act")


def decide(exploitation: str, technical_impact: str, automatable: str,
           mission_wellbeing: str = "medium") -> str:
    """The SSVC decision for the four points. Unknown values fall back to the least
    urgent reading (none / partial / no / medium), so a gap never invents urgency."""
    key = (exploitation if exploitation in ("none", "poc", "active") else "none",
           technical_impact if technical_impact in ("partial", "total") else "partial",
           automatable if automatable in ("yes", "no") else "no")
    return _TREE[key][_MWB_INDEX.get(mission_wellbeing, 1)]


class SsvcDB:
    def __init__(self, records: dict[str, dict], fetched_at: str | None):
        self._records = records
        self.fetched_at = fetched_at

    def get(self, cve_id: str) -> dict | None:
        return self._records.get((cve_id or "").upper())


_cache: dict[tuple[str, int, int], SsvcDB] = {}
_lock = threading.Lock()


def load_ssvc(path: str | Path | None = None) -> SsvcDB:
    """The pinned Vulnrichment snapshot, or an empty DB when there is none."""
    path = Path(path) if path is not None else resolve(DEFAULT_SSVC_PATH.name)
    try:
        st = path.stat()
    except OSError:
        return SsvcDB({}, None)
    key = (str(path.resolve()), st.st_mtime_ns, st.st_size)
    with _lock:
        if key in _cache:
            return _cache[key]
    with path.open() as fh:
        snap = json.load(fh)
    db = SsvcDB(snap.get("records") or {}, snap.get("fetched_at"))
    with _lock:
        return _cache.setdefault(key, db)


def _derived_automatable(metrics: dict) -> str | None:
    if not metrics:
        return None
    return "yes" if (metrics.get("AV") == "N" and metrics.get("AC") == "L"
                     and metrics.get("PR") == "N" and metrics.get("UI") == "N") else "no"


def _derived_impact(metrics: dict) -> str | None:
    if not metrics:
        return None
    return "total" if metrics.get("C") == "H" and metrics.get("I") == "H" else "partial"


def assess(cve_id: str, cvss_vector: str | None, kev: bool | None,
           internet_facing: bool | None, db: SsvcDB | None = None) -> dict:
    """The SSVC decision and every input with its source, for one CVE finding."""
    published = (db.get(cve_id) if db is not None else None) or {}
    metrics = parse_vector(cvss_vector) if cvss_vector else {}

    if kev:
        exploitation, e_src = "active", "CISA KEV"
    elif published.get("exploitation"):
        exploitation, e_src = published["exploitation"], "CISA Vulnrichment"
    else:
        exploitation, e_src = "none", "no exploitation data published"

    if published.get("automatable"):
        automatable, a_src = published["automatable"], "CISA Vulnrichment"
    else:
        automatable = _derived_automatable(metrics)
        a_src = "derived from CVSS vector" if automatable else "unknown (no CVSS vector)"

    if published.get("technical_impact"):
        impact, t_src = published["technical_impact"], "CISA Vulnrichment"
    else:
        impact = _derived_impact(metrics)
        t_src = "derived from CVSS vector" if impact else "unknown (no CVSS vector)"

    mwb = "high" if internet_facing is True else "medium"
    return {
        "decision": decide(exploitation, impact or "partial", automatable or "no", mwb),
        "exploitation": exploitation, "exploitation_source": e_src,
        "automatable": automatable, "automatable_source": a_src,
        "technical_impact": impact, "technical_impact_source": t_src,
        "mission_wellbeing": mwb,
        "mission_wellbeing_source": "internet-facing asset" if mwb == "high"
                                    else "default (asset criticality not known to the engine)",
    }
