"""
device_profile.py — map a probe device_inventory result onto asset fields.

The probe's device_classifier (probe/scanner/device_classifier.py) infers a
device ROLE from observed OS + ports + services and rides it back in the result
envelope as `result["devices"] = [{ip, device_type, role_detail, confidence, …}]`.
Before this bridge the manager promoted every host as `AssetType.server`
(job_result_service._promote_assets hardcoded it), throwing the role away.

Pure logic — no DB, no I/O — so the mapping is unit-testable in isolation.
"""
from __future__ import annotations

from app.models.enums import AssetType

# device_classifier.device_type → the coarse AssetType enum. A value with no
# clean enum counterpart (unknown / ambiguous) maps to None, meaning "leave the
# existing asset_type untouched" — we never downgrade a known role to a guess.
_DEVICE_TYPE_TO_ASSET_TYPE: dict[str, AssetType] = {
    "workstation": AssetType.workstation,
    "server": AssetType.server,
    "network_device": AssetType.network,
    "printer": AssetType.printer,
    "hypervisor": AssetType.hypervisor,
    "iot": AssetType.iot,
}


def asset_type_for(device_type: str | None) -> AssetType | None:
    """The AssetType for a classifier device_type, or None to keep the existing."""
    if not device_type:
        return None
    return _DEVICE_TYPE_TO_ASSET_TYPE.get(device_type)


def device_profiles(result: dict | None) -> dict[str, dict]:
    """ip → {asset_type, device_role, role_detail, role_confidence} from a probe
    device_inventory result's `devices` rollup.

    `asset_type` is None when the classifier's device_type has no enum counterpart
    (unknown/ambiguous) — the caller then leaves the asset's existing type alone.
    Hosts the classifier could not evidence never appear in `devices` (the probe
    drops device_type == "unknown"), so every entry here is a real classification.
    """
    profiles: dict[str, dict] = {}
    for entry in (result or {}).get("devices") or []:
        if not isinstance(entry, dict):
            continue
        ip = entry.get("ip")
        if not ip:
            continue
        device_type = entry.get("device_type")
        confidence = entry.get("confidence")
        profiles[ip] = {
            "asset_type": asset_type_for(device_type),
            "device_role": device_type,
            "role_detail": entry.get("role_detail"),
            "role_confidence": (
                float(confidence) if isinstance(confidence, (int, float)) else None
            ),
        }
    return profiles
