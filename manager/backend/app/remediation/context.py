"""
context.py — the facts a remediation plan is grounded in.

Pure (no DB, no network). ``build_context`` reads a finding plus its Asset and
the Service on the finding's port and returns every fact with its provenance:

  * ``scan``          — observed by a scanner (service row, finding evidence)
  * ``asset_record``  — from the asset inventory record
  * ``not_recorded``  — absent; the plan prints "not recorded", never a guess

Nothing is inferred beyond simple, documented normalisation (OS family,
exposure). Banners are attacker-controlled text: they are kept as a short
excerpt for display and only ever reach a model inside the fenced context.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Iterable

from app.intel.fragile import fragile_reasons
from app.intel.tagging import tag_strings

NOT_RECORDED = "not recorded"
_BANNER_MAX = 200


@dataclass(frozen=True)
class Fact:
    value: Any
    source: str   # scan | asset_record | not_recorded

    @property
    def recorded(self) -> bool:
        return self.source != "not_recorded" and self.value not in (None, "")


_MISSING = Fact(None, "not_recorded")


def _fact(value: Any, source: str) -> Fact:
    if value is None or (isinstance(value, str) and not value.strip()):
        return _MISSING
    return Fact(value, source)


@dataclass(frozen=True)
class RemediationContext:
    host: Fact
    ip: Fact
    fqdn: Fact
    os: Fact
    os_version: Fact
    os_family: str                      # linux | windows | macos | network | unknown
    port: Fact
    protocol: Fact
    service_name: Fact
    product: Fact
    version: Fact
    cpe: Fact
    banner_excerpt: Fact
    exposure: str                       # internet | internal | unknown
    criticality: Fact
    environment: Fact
    tags: tuple[str, ...]
    fragile: bool
    fragile_reason: str | None
    kev: bool
    epss: float | None
    exploit_validated: bool
    rule_id: str | None
    cve_ids: tuple[str, ...]
    fixed_version: str | None
    scanner: str | None
    category: str | None
    # services/remediation_os.PlatformResolution — the ONE platform detector
    # (manual os_family tag > asset OS > service banner). None without an asset.
    platform: Any = None

    def text(self, name: str) -> str:
        """The fact's value as display text, or the literal "not recorded"."""
        f = getattr(self, name)
        if isinstance(f, Fact):
            return str(f.value) if f.recorded else NOT_RECORDED
        return str(f) if f not in (None, "") else NOT_RECORDED

    def facts_used(self) -> list[str]:
        """Names of the Fact fields that were actually recorded."""
        return [fl.name for fl in fields(self)
                if isinstance(getattr(self, fl.name), Fact) and getattr(self, fl.name).recorded]

    def as_dict(self) -> dict[str, dict[str, Any]]:
        """``{name: {value, source}}`` for every Fact — the plan's context block."""
        out: dict[str, dict[str, Any]] = {}
        for fl in fields(self):
            v = getattr(self, fl.name)
            if isinstance(v, Fact):
                out[fl.name] = {"value": v.value if v.recorded else None,
                                "source": v.source if v.recorded else "not_recorded"}
        return out


# ── helpers ──────────────────────────────────────────────────────────────────

def _enum(v: Any) -> Any:
    return getattr(v, "value", v)


def _evidence(finding: Any) -> dict:
    ev = getattr(finding, "evidence", None)
    return ev if isinstance(ev, dict) else {}


def _int(v: Any) -> int | None:
    try:
        return int(v) if v is not None and str(v).strip() != "" else None
    except (TypeError, ValueError):
        return None


def evidence_port(finding: Any) -> int | None:
    """The port a finding is about: top-level evidence first (CVE + posture
    dicts), then the nested posture ``evidence`` block."""
    ev = _evidence(finding)
    port = _int(ev.get("port"))
    if port is None and isinstance(ev.get("evidence"), dict):
        port = _int(ev["evidence"].get("port"))
    return port


def pick_service(finding: Any, services: Iterable[Any]) -> Any | None:
    """The asset's Service row on the finding's port, or None."""
    port = evidence_port(finding)
    if port is None:
        return None
    for s in services or ():
        if _int(getattr(s, "port", None)) == port:
            return s
    return None


_NETWORK_TYPES = {"network", "printer", "iot", "hypervisor"}


def os_family(os_name: str | None, os_version: str | None, asset_type: str | None) -> str:
    text = f"{os_name or ''} {os_version or ''}".lower()
    if "windows" in text:
        return "windows"
    if "mac" in text or "darwin" in text or "os x" in text:
        return "macos"
    if any(k in text for k in ("linux", "ubuntu", "debian", "centos", "rhel", "red hat",
                               "fedora", "suse", "alpine", "rocky", "alma", "amazon linux",
                               "unix", "freebsd", "openbsd")):
        return "linux"
    if any(k in text for k in ("ios", "junos", "fortios", "pan-os", "routeros", "firmware",
                               "vxworks", "embedded")):
        return "network"
    if (asset_type or "").lower() in _NETWORK_TYPES:
        return "network"
    return "unknown"


_SERVICE_EXPOSURE = {"external": "internet", "internal_only": "internal", "not_exposed": "internal"}


def _exposure(service: Any, ev: dict, environment: str | None) -> str:
    mapped = _SERVICE_EXPOSURE.get(str(getattr(service, "exposure", "") or "").lower())
    if mapped:
        return mapped
    facing = ev.get("internet_facing")
    if facing is None and isinstance(ev.get("evidence"), dict):
        facing = ev["evidence"].get("internet_facing")
    if facing is True:
        return "internet"
    if facing is False:
        return "internal"
    env = (environment or "").lower()
    if any(k in env for k in ("internet", "dmz", "external", "public", "edge")):
        return "internet"
    if any(k in env for k in ("internal", "corp", "private", "lan", "intranet")):
        return "internal"
    return "unknown"


def _cpe_parts(cpe: str | None) -> tuple[str | None, str | None]:
    """(product, version) from a CPE 2.3 string, or (None, None)."""
    if not cpe or not str(cpe).startswith("cpe:"):
        return None, None
    parts = str(cpe).split(":")
    product = parts[4] if len(parts) > 4 and parts[4] not in ("*", "-", "") else None
    version = parts[5] if len(parts) > 5 and parts[5] not in ("*", "-", "") else None
    return product, version


def _float(v: Any) -> float | None:
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


# ── public ───────────────────────────────────────────────────────────────────

_KB_FAMILY = {"windows": "windows", "linux": "linux", "macos": "macos"}


def build_context(finding: Any, asset: Any | None = None, service: Any | None = None,
                  services: Iterable[Any] | None = None) -> RemediationContext:
    """``services`` = all of the asset's services (for platform detection from
    banners); ``service`` = the one on the finding's port."""
    ev = _evidence(finding)
    nested = ev.get("evidence") if isinstance(ev.get("evidence"), dict) else {}

    cpe_value = getattr(service, "cpe", None) or ev.get("cpe")
    cpe_product, cpe_version = _cpe_parts(cpe_value)

    if service is not None and getattr(service, "product", None):
        product = _fact(service.product, "scan")
    else:
        product = _fact(ev.get("product") or nested.get("observed_product")
                        or nested.get("product") or cpe_product, "scan")
    if service is not None and getattr(service, "version", None):
        version = _fact(service.version, "scan")
    else:
        version = _fact(ev.get("matched_version") or ev.get("version")
                        or nested.get("version") or cpe_version, "scan")

    port_value = _int(getattr(service, "port", None)) if service is not None else None
    if port_value is None:
        port_value = evidence_port(finding)

    banner = getattr(service, "banner", None) or nested.get("banner") or ev.get("banner")
    banner_fact = _fact(str(banner)[:_BANNER_MAX] if banner else None, "scan")

    asset_type = _enum(getattr(asset, "asset_type", None)) if asset is not None else None
    tags = tuple(tag_strings(getattr(asset, "tags", None))) if asset is not None else ()
    reasons = fragile_reasons(tags)

    environment = getattr(asset, "environment", None) if asset is not None else None
    kev = bool(ev.get("kev") or ev.get("kev_listed") or ev.get("actively_exploited"))

    platform = None
    family = "unknown"
    if asset is not None:
        from app.services.remediation_os import resolve_platform
        pool = list(services) if services is not None else ([service] if service is not None else [])
        platform = resolve_platform(asset, pool)
        if platform.source not in ("not_detected", "no_asset"):
            family = _KB_FAMILY.get(platform.os) or "network"   # bsd / network_os → vendor-neutral
    if family == "unknown":
        # Fallback only when the resolver found nothing: device type (printer, iot…).
        family = os_family(None, None, asset_type)

    cves = tuple(str(c).upper() for c in (getattr(finding, "cve_ids", None) or []) if c)
    if not cves and ev.get("cve_id"):
        cves = (str(ev["cve_id"]).upper(),)

    return RemediationContext(
        host=_fact((getattr(asset, "hostname", None) or getattr(asset, "fqdn", None)
                    or getattr(asset, "ip_address", None)) if asset is not None else ev.get("asset_ip"),
                   "asset_record" if asset is not None else "scan"),
        ip=_fact(getattr(asset, "ip_address", None) if asset is not None else ev.get("asset_ip"),
                 "asset_record" if asset is not None else "scan"),
        fqdn=_fact(getattr(asset, "fqdn", None) if asset is not None else None, "asset_record"),
        os=_fact(getattr(asset, "os", None) if asset is not None else None, "asset_record"),
        os_version=_fact(getattr(asset, "os_version", None) if asset is not None else None, "asset_record"),
        os_family=family,
        port=_fact(port_value, "scan"),
        protocol=_fact((getattr(service, "protocol", None) if service is not None else None)
                       or ev.get("proto"), "scan"),
        service_name=_fact((getattr(service, "service_name", None) if service is not None else None)
                           or nested.get("service") or nested.get("observed_service"), "scan"),
        product=product,
        version=version,
        cpe=_fact(cpe_value, "scan"),
        banner_excerpt=banner_fact,
        exposure=_exposure(service, ev, environment),
        criticality=_fact(_enum(getattr(asset, "criticality", None)) if asset is not None else None,
                          "asset_record"),
        environment=_fact(environment, "asset_record"),
        tags=tags,
        fragile=bool(reasons),
        fragile_reason=", ".join(reasons) if reasons else None,
        kev=kev,
        epss=_float(getattr(finding, "epss_score", None)),
        exploit_validated=bool(getattr(finding, "exploit_validated", False)),
        rule_id=str(ev["rule_id"]) if ev.get("rule_id") else None,
        cve_ids=cves,
        fixed_version=str(ev["fixed_version"]) if ev.get("fixed_version") else None,
        scanner=str(ev.get("scanner")) if ev.get("scanner") else None,
        category=str(nested.get("category") or ev.get("category") or "") or None,
        platform=platform,
    )
