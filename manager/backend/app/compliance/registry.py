"""
registry.py — regional compliance frameworks, keyed by control THEME.

Finding category (remediation_kb.classify_finding) → control themes → each
framework's controls for those themes. The theme layer keeps packs small and
extensible: a new finding category only needs its themes, and a new framework
only needs one entry per theme.

The five global frameworks (PCI DSS, ISO 27001, NIST 800-53, SOC 2, HIPAA) stay
in ``app.services.finding_compliance``; this module adds the jurisdiction- and
sector-specific ones plus tag-triggered SWIFT CSCF.

Control references are audit POINTERS, not legal advice or an attestation. When
a pack is not certain of a paragraph number it cites the section by name and
says so via ``granularity``; it never fabricates precision.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from app.compliance.profile import EngagementProfile

THEMES: tuple[str, ...] = (
    "asset_inventory", "secure_configuration", "patch_vulnerability_mgmt",
    "access_control", "authentication", "remote_access", "network_security",
    "crypto_in_transit", "data_protection", "logging_monitoring", "incident_response",
)

CATEGORY_THEMES: dict[str, tuple[str, ...]] = {
    "weak_tls": ("crypto_in_transit", "secure_configuration"),
    "smb_signing": ("secure_configuration", "network_security"),
    "exposed_rdp": ("remote_access", "network_security", "authentication"),
    "default_credentials": ("authentication", "access_control"),
    "missing_patch": ("patch_vulnerability_mgmt",),
    "open_mgmt_port": ("network_security", "remote_access", "secure_configuration"),
    "anon_ftp": ("access_control", "data_protection", "secure_configuration"),
    "outdated_ssh": ("patch_vulnerability_mgmt", "crypto_in_transit"),
    "generic": ("patch_vulnerability_mgmt", "secure_configuration"),
}

DISCLAIMER = (
    "Control references are pointers to help auditors and owners locate the relevant "
    "obligation. They are not legal advice or a compliance attestation; confirm "
    "applicability with your compliance/legal team."
)

ALL_SECTORS = "*"
FINANCIAL = ("banking", "payments_fintech", "nbfc", "insurance", "capital_markets")


@dataclass(frozen=True)
class ControlRef:
    controls: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class Reporting:
    authority: str
    deadline_hours: float
    trigger: str
    reference: str


@dataclass(frozen=True)
class Framework:
    id: str
    name: str
    authority: str
    source: str
    jurisdictions: tuple[str, ...]
    sectors: tuple[str, ...] | str          # ALL_SECTORS, or explicit tuple ("" = tag-only)
    themes: dict[str, ControlRef]
    baseline: ControlRef                    # used for any theme not mapped explicitly
    granularity: str = "article"            # article | section | domain | document
    reporting: tuple[Reporting, ...] = ()
    trigger_tags: frozenset[str] = field(default_factory=frozenset)
    note: str = ""

    def controls_for(self, theme: str) -> ControlRef:
        return self.themes.get(theme) or self.baseline

    def applies(self, profile: EngagementProfile, tags: set[str]) -> bool:
        if self.trigger_tags & tags:
            return True
        if not set(self.jurisdictions) & set(profile.jurisdictions):
            return False
        return self.sectors == ALL_SECTORS or profile.sector in self.sectors


def C(*controls: str, why: str) -> ControlRef:
    return ControlRef(tuple(controls), why)


FRAMEWORKS: dict[str, Framework] = {}


def register(*frameworks: Framework) -> None:
    for fw in frameworks:
        if fw.id in FRAMEWORKS:
            raise ValueError(f"duplicate framework id {fw.id}")
        FRAMEWORKS[fw.id] = fw


# ── queries ──────────────────────────────────────────────────────────────────

def applicable_frameworks(profile: EngagementProfile, tags: Iterable[str] = ()) -> list[Framework]:
    tagset = set(tags)
    return [fw for fw in FRAMEWORKS.values() if fw.applies(profile, tagset)]


def reporting_clocks(frameworks: Iterable[Framework]) -> list[dict[str, Any]]:
    """Every incident-reporting obligation, shortest deadline first — the clock
    that starts when a finding turns out to have been exploited."""
    clocks = [
        {"framework_id": fw.id, "framework": fw.name, "authority": r.authority,
         "deadline_hours": r.deadline_hours, "trigger": r.trigger, "reference": r.reference}
        for fw in frameworks for r in fw.reporting
    ]
    return sorted(clocks, key=lambda c: c["deadline_hours"])


def finding_obligations(finding: Any, profile: EngagementProfile,
                        tags: Iterable[str] = ()) -> dict[str, Any]:
    """Which regional obligations a finding implicates for this customer."""
    from app.services.remediation_kb import classify_finding

    category = classify_finding(finding)
    themes = CATEGORY_THEMES.get(category, CATEGORY_THEMES["generic"])
    frameworks = applicable_frameworks(profile, tags)
    out = []
    for fw in frameworks:
        controls: list[str] = []
        rationale: list[str] = []
        for theme in themes:
            ref = fw.controls_for(theme)
            controls += [c for c in ref.controls if c not in controls]
            if ref.rationale not in rationale:
                rationale.append(ref.rationale)
        out.append({
            "framework_id": fw.id, "framework": fw.name, "authority": fw.authority,
            "jurisdictions": list(fw.jurisdictions), "source": fw.source,
            "granularity": fw.granularity, "controls": controls,
            "rationale": " ".join(rationale), "note": fw.note or None,
        })
    return {
        "category": category, "themes": list(themes), "profile": profile.model_dump(),
        "frameworks": out, "reporting": reporting_clocks(frameworks),
        "disclaimer": DISCLAIMER,
    }


def known_control_ids(frameworks: Iterable[Framework] | None = None) -> set[str]:
    """Every control string the packs can cite — the grounding allow-list."""
    ids: set[str] = set()
    for fw in (frameworks if frameworks is not None else FRAMEWORKS.values()):
        for ref in (*fw.themes.values(), fw.baseline):
            ids.update(ref.controls)
    return ids


# Packs self-register on import.
from app.compliance.packs import eu_uk, global_, india, me_apac, us  # noqa: E402,F401
