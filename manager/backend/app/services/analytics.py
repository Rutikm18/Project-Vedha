"""
Exposure analytics — protocol risk + zone health.

Derives two dashboard aggregates from real data:

- Protocol Risk: for each exposed service (LDAP, SMB, …), the worst open-finding
  severity among the assets exposing it. "If anything speaking this protocol is
  compromised, how bad is it?" — a 0-100 exposure risk.

- Zone Health: assets grouped by `environment` (prod / dmz / corp / …). A zone's
  score is 100 minus the average per-asset finding burden, so a clean zone scores
  high and a zone full of criticals scores low.

Both use one severity→weight scale so the two widgets stay comparable. Findings
not linked to an asset can't be attributed to a protocol/zone and are skipped
(they still count in the global KPIs).
"""
from __future__ import annotations

# Open-finding severity → burden weight (0-100). A single critical maxes a
# protocol's risk / tanks a zone's health, which matches how operators triage.
_SEVERITY_WEIGHT = {
    "critical": 100,
    "high": 70,
    "medium": 40,
    "low": 15,
    "info": 5,
}


def _sev(value) -> str:
    return value.value if hasattr(value, "value") else str(value)


def compute_exposure(
    assets: list,        # objects with .id, .environment
    services: list,      # objects with .asset_id, .service_name, .port
    findings: list,      # objects with .asset_id, .severity (open findings only)
    top_n: int = 6,
) -> dict:
    # Per-asset burden = worst open finding on that asset (0 if none).
    burden: dict = {}
    for f in findings:
        if f.asset_id is None:
            continue
        w = _SEVERITY_WEIGHT.get(_sev(f.severity), 0)
        aid = str(f.asset_id)
        if w > burden.get(aid, 0):
            burden[aid] = w

    # ── Protocol risk ──────────────────────────────────────────────────────────
    # A service_name maps to the set of assets exposing it; its risk is the worst
    # burden across those assets.
    proto_risk: dict = {}
    proto_seen: dict = {}
    for s in services:
        name = (s.service_name or "").strip()
        if not name:
            continue
        name = name.upper()
        aid = str(s.asset_id)
        proto_seen[name] = proto_seen.get(name, 0) + 1
        risk = burden.get(aid, 0)
        if risk > proto_risk.get(name, 0):
            proto_risk[name] = risk

    protocols = [
        {"name": name, "value": proto_risk.get(name, 0)}
        for name in proto_seen
    ]
    # Highest risk first; break ties by how widely the protocol is exposed.
    protocols.sort(key=lambda p: (p["value"], proto_seen[p["name"]]), reverse=True)
    protocols = protocols[:top_n]

    # ── Zone health ────────────────────────────────────────────────────────────
    zones_assets: dict = {}
    for a in assets:
        zone = (a.environment or "Unzoned").strip() or "Unzoned"
        zones_assets.setdefault(zone, []).append(str(a.id))

    zones = []
    for zone, aids in zones_assets.items():
        avg_burden = sum(burden.get(aid, 0) for aid in aids) / len(aids) if aids else 0
        score = max(0, round(100 - avg_burden))
        zones.append({"name": zone.upper(), "score": score})
    # Least healthy first so the riskiest zone is most visible.
    zones.sort(key=lambda z: z["score"])
    zones = zones[:top_n]

    return {"protocols": protocols, "zones": zones}
