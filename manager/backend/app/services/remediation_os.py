"""
remediation_os.py — which platform a finding's fix plan should target.

The operator should not have to pick an OS: Vedha already knows it for most
assets. The resolution reuses the asset-tagging os_family rule (one detector,
not two) and reports where the answer came from, in this order:

  1. an operator's manual ``os_family`` tag        → source "manual_tag"
  2. the asset's OS string                         → source "asset_os"
  3. a service banner naming the OS/distro         → source "service_banner"
  4. nothing                                       → "generic", "not_detected"

The KB only carries linux / windows / macos / generic commands. BSD and network
operating systems resolve to ``generic``: the Linux recipes use apt/systemctl and
would be wrong there, so vendor-neutral guidance is the honest answer.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from sqlalchemy import select

from app.intel.tagging import facts_from_records, os_family_tag
from app.services.remediation_kb import os_key

# os_family tag value → remediation KB key.
_FAMILY_TO_KB = {
    "windows": "windows",
    "linux": "linux",
    "macos": "macos",
    "bsd": "generic",
    "network_os": "generic",
}
_RULE_SOURCE = {"os.string": "asset_os", "os.banner": "service_banner"}


@dataclass(frozen=True)
class PlatformResolution:
    os: str                   # KB key actually served: linux | windows | macos | generic
    family: str | None        # detected family, incl. bsd / network_os; None when unknown
    source: str               # manual_tag | asset_os | service_banner | not_detected | no_asset | requested
    evidence: str | None
    confidence: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def _manual_family(tags: Any) -> str | None:
    if not isinstance(tags, dict):
        return None
    for t in tags.get("manual") or []:
        if isinstance(t, dict) and t.get("key") == "os_family":
            value = str(t.get("value") or "").strip().lower()
            if value in _FAMILY_TO_KB:
                return value
    return None


def resolve_platform(asset: Any, services: Iterable[Any]) -> PlatformResolution:
    """Pure: the platform a fix plan for this asset should target."""
    if asset is None:
        return PlatformResolution("generic", None, "no_asset", None, None)

    manual = _manual_family(getattr(asset, "tags", None))
    if manual:
        return PlatformResolution(_FAMILY_TO_KB[manual], manual, "manual_tag",
                                  f"operator tag os_family:{manual}", 1.0)

    tag = os_family_tag(facts_from_records(asset, services))
    if tag is not None and tag.value in _FAMILY_TO_KB:
        return PlatformResolution(_FAMILY_TO_KB[tag.value], tag.value,
                                  _RULE_SOURCE.get(tag.rule, tag.rule),
                                  tag.evidence, tag.confidence)

    return PlatformResolution("generic", None, "not_detected", None, None)


async def resolve_finding_platform(db, finding: Any) -> PlatformResolution:
    """Load the finding's asset (same engagement) and its services, then resolve."""
    asset_id = getattr(finding, "asset_id", None)
    if asset_id is None:
        return resolve_platform(None, ())
    from app.models.asset import Asset
    from app.models.service import Service

    asset = (await db.execute(
        select(Asset).where(Asset.id == asset_id,
                            Asset.engagement_id == finding.engagement_id)
    )).scalar_one_or_none()
    if asset is None:
        return resolve_platform(None, ())
    services = (await db.execute(
        select(Service).where(Service.asset_id == asset.id)
    )).scalars().all()
    return resolve_platform(asset, services)


def is_auto(requested: str | None) -> bool:
    return (requested or "auto").strip().lower() == "auto"


async def platform_for_request(db, finding: Any, requested: str | None) -> PlatformResolution:
    """`auto` (the default) detects; any explicit OS is an operator override."""
    if is_auto(requested):
        return await resolve_finding_platform(db, finding)
    return PlatformResolution(os_key(requested), None, "requested", None, None)
