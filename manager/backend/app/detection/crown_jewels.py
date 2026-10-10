"""
crown_jewels.py — suggest attack-path targets when the operator marked none (P4b).

Attack paths are built TO crown jewels. Targets are the assets an operator marked
`criticality=critical`, and nothing sets that automatically, so an engagement where
nobody classified an asset produced zero paths and a bare `no_targets` — the model
had nowhere to aim (FM-04). Microsoft's own guidance is explicit that attack-path
results are incomplete until critical assets are defined.

This does not overrule the operator: when any asset is marked critical, those remain
the only targets. Only when NONE is marked does this suggest the assets a defender
would almost always treat as crown jewels, from high-confidence role evidence:

  * a domain controller   — owning it is owning the domain
  * a virtualization host  — owning it is owning every guest
  * a datastore            — it holds the data an attacker is usually after

Every suggestion carries the reason it was picked, and the caller records that the
targets were SUGGESTED, not operator-chosen, so the UI and the report can say so and
never present an auto-picked target as a deliberate scoping decision.

Pure and deterministic: no DB, no I/O, stable ordering.
"""
from __future__ import annotations

from typing import Any, Iterable, Optional

# Role confidence below which a role claim is a candidate, not a basis to act on
# (shared with intel.device_role.HIGH_CONFIDENCE).
_HIGH_CONFIDENCE = 0.7

_DC_DETAILS = frozenset({"domain_controller", "dc", "active_directory"})
# Datastore listener ports: the presence of one makes a host a data crown jewel.
_DATASTORE_PORTS = frozenset({1433, 1521, 3306, 5432, 6379, 9042, 9200, 11211, 27017, 5984, 50000})


def _attr(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _enum(value: Any) -> str:
    return str(_attr(value, "value") if hasattr(value, "value") else value or "").lower()


def _role_is_high_confidence(asset: Any) -> bool:
    """A role claim acts as a crown-jewel basis only when it is trustworthy. A
    missing confidence is treated as acceptable for the strong role signals below
    (domain_controller / hypervisor are high-signal classifications), but a present
    confidence must clear the bar."""
    conf = _attr(asset, "role_confidence")
    return conf is None or float(conf) >= _HIGH_CONFIDENCE


def _datastore_asset_ids(services: Iterable[Any]) -> set[str]:
    out: set[str] = set()
    for s in services:
        if _attr(s, "port") in _DATASTORE_PORTS:
            aid = _attr(s, "asset_id")
            if aid is not None:
                out.add(str(aid))
    return out


def suggest_crown_jewels(assets: Iterable[Any],
                         services: Iterable[Any] = ()) -> list[dict[str, str]]:
    """Suggested crown-jewel targets as [{"asset_id", "reason"}], most important role
    first (domain controller, then hypervisor, then datastore), deterministic by id.
    Empty when nothing high-value is identifiable (the caller then keeps `no_targets`)."""
    assets = list(assets)
    datastores = _datastore_asset_ids(services)
    picked: dict[str, str] = {}

    def consider(aid: str, reason: str) -> None:
        picked.setdefault(aid, reason)       # first (most important) reason wins

    # Pass 1: domain controllers.
    for a in sorted(assets, key=lambda x: str(_attr(x, "id"))):
        aid = str(_attr(a, "id"))
        if _enum(_attr(a, "role_detail")) in _DC_DETAILS and _role_is_high_confidence(a):
            consider(aid, "domain controller")
    # Pass 2: virtualization hosts.
    for a in sorted(assets, key=lambda x: str(_attr(x, "id"))):
        aid = str(_attr(a, "id"))
        if (_enum(_attr(a, "asset_type")) == "hypervisor"
                or _enum(_attr(a, "device_role")) == "hypervisor") and _role_is_high_confidence(a):
            consider(aid, "virtualization host")
    # Pass 3: datastores (by an observed datastore service).
    for a in sorted(assets, key=lambda x: str(_attr(x, "id"))):
        aid = str(_attr(a, "id"))
        if aid in datastores:
            consider(aid, "datastore")

    return [{"asset_id": aid, "reason": picked[aid]} for aid in sorted(picked)]
