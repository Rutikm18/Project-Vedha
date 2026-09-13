"""
Exposure analytics — protocol risk + zone health.

Derives two dashboard aggregates from real data:

- Protocol Risk: for each exposed service (LDAP, SMB, …), the worst open finding
  ATTRIBUTABLE TO THAT SERVICE — matched by the (asset, port) the finding was
  recorded against. "If this protocol is the way in, how bad is it?"

- Zone Health: assets grouped by `environment` (prod / dmz / corp / …). A zone's
  score is driven by its WORST asset, with the spread across the zone as a
  secondary term, so a single critical host cannot hide behind its neighbours.

Findings that cannot be tied to an asset, or to a port with a known service, are
counted in `unattributed_findings` and are deliberately left out of protocol risk
— see _attribute_findings. They still count in the ledger, posture and SLA.

Pure and DB-free (mirrors services/posture.py and services/sla.py): the router
loads rows and passes them in.
"""
from __future__ import annotations

# Open-finding severity → burden weight (0-100). Used for zone burden and for
# the length of the meter bar. The BAND a row is labelled with comes from the
# severity itself, never from thresholding this number — see `severity` in the
# protocol payload.
_SEVERITY_WEIGHT = {
    "critical": 100,
    "high": 70,
    "medium": 40,
    "low": 15,
    "info": 5,
}

_SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}

# How much a zone's worst asset drives its score, versus the average across the
# zone. Weighted to the worst on purpose: the previous formula was a plain mean,
# so one critical host in a zone of a hundred scored 99 and was labelled
# "Healthy". A zone-health number whose whole job is to rank zones by where to
# look first must not average away the reason to look.
_WORST_SHARE = 0.7
_SPREAD_SHARE = 0.3


def _sev(value) -> str:
    return value.value if hasattr(value, "value") else str(value)


def _weight(severity) -> int:
    return _SEVERITY_WEIGHT.get(_sev(severity), 0)


def _evidence_port(finding) -> int | None:
    """Best-effort port for a finding, from its evidence.

    Mirrors discovery.finding_translator._finding_port (explicit `port`, else the
    ':NNN' suffix of a host:port `target`) — duplicated rather than imported to
    keep this module free of DB/model imports.
    """
    ev = getattr(finding, "evidence", None)
    if not isinstance(ev, dict):
        return None
    raw = ev.get("port")
    if raw is not None:
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None
    target = ev.get("target")
    if isinstance(target, str) and target.count(":") == 1:
        _host, _sep, port_s = target.partition(":")
        try:
            return int(port_s)
        except (TypeError, ValueError):
            return None
    return None


def _attribute_findings(services: list, findings: list) -> tuple[dict, int]:
    """Map each service NAME to the severities of findings actually on it.

    Attribution is by (asset, port). The previous implementation attributed an
    asset's single worst finding to EVERY service that asset exposed, so a host
    with a critical Apache RCE reported SSH at maximum risk too — and an operator
    reading that panel would go and harden SSH. A finding that names no port
    cannot be pinned to a protocol, so it is counted as unattributed instead of
    being smeared across all of them.
    """
    # (asset_id, port) → service names listening there. One port can carry both a
    # tcp and a udp row with different names; a finding on that port implicates
    # both, because the evidence does not say which.
    by_port: dict = {}
    for s in services:
        name = (s.service_name or "").strip().upper()
        if not name:
            continue
        by_port.setdefault((str(s.asset_id), s.port), set()).add(name)

    severities: dict = {}
    unattributed = 0
    for f in findings:
        if f.asset_id is None:
            unattributed += 1
            continue
        port = _evidence_port(f)
        if port is None:
            unattributed += 1
            continue
        names = by_port.get((str(f.asset_id), port))
        if not names:
            unattributed += 1
            continue
        for name in names:
            severities.setdefault(name, []).append(_sev(f.severity))
    return severities, unattributed


def compute_exposure(
    assets: list,        # objects with .id, .environment
    services: list,      # objects with .asset_id, .service_name, .port
    findings: list,      # objects with .asset_id, .severity, .evidence (open only)
    top_n: int = 25,
) -> dict:
    # ── Protocol risk ──────────────────────────────────────────────────────────
    attributed, unattributed = _attribute_findings(services, findings)

    # Every exposed service name appears, including clean ones: "this is
    # listening and nothing is wrong with it" is information, and hiding it would
    # make an empty panel ambiguous between "no services" and "no findings".
    exposure_breadth: dict = {}
    for s in services:
        name = (s.service_name or "").strip().upper()
        if not name:
            continue
        exposure_breadth.setdefault(name, set()).add(str(s.asset_id))

    protocols = []
    for name, asset_ids in exposure_breadth.items():
        sevs = attributed.get(name, [])
        worst = min(sevs, key=lambda s: _SEVERITY_RANK.get(s, 99)) if sevs else None
        protocols.append({
            "name": name,
            "severity": worst,                       # None = nothing found on it
            "value": _SEVERITY_WEIGHT.get(worst, 0) if worst else 0,
            "findings": len(sevs),
            "assets": len(asset_ids),
        })
    # Worst first; ties broken by how widely the protocol is exposed, then name
    # so the order is stable between refreshes.
    protocols.sort(key=lambda p: (
        _SEVERITY_RANK.get(p["severity"], 99), -p["assets"], p["name"],
    ))
    protocols = protocols[:top_n]

    # ── Zone health ────────────────────────────────────────────────────────────
    # Per-asset burden = worst open finding on that asset (0 if none).
    burden: dict = {}
    for f in findings:
        if f.asset_id is None:
            continue
        w = _weight(f.severity)
        aid = str(f.asset_id)
        if w > burden.get(aid, 0):
            burden[aid] = w

    zones_assets: dict = {}
    for a in assets:
        zone = (a.environment or "").strip() or "Unzoned"
        zones_assets.setdefault(zone, []).append(str(a.id))

    zones = []
    for zone, aids in zones_assets.items():
        burdens = [burden.get(aid, 0) for aid in aids]
        worst = max(burdens) if burdens else 0
        spread = sum(burdens) / len(burdens) if burdens else 0
        score = max(0, round(100 - (_WORST_SHARE * worst + _SPREAD_SHARE * spread)))
        zones.append({
            "name": zone.upper(),
            "score": score,
            "assets": len(aids),
            "affected": sum(1 for b in burdens if b > 0),
        })
    # Least healthy first so the riskiest zone is most visible.
    zones.sort(key=lambda z: (z["score"], z["name"]))
    zones = zones[:top_n]

    return {
        "protocols": protocols,
        "zones": zones,
        # Open findings that could not be tied to a listening service. Surfaced so
        # the panel can say the protocol view is partial rather than implying
        # these findings do not exist.
        "unattributed_findings": unattributed,
    }
