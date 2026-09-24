"""
domain_brief.py — compose the domain-expert block of the system prompt.

Built ONLY from trusted, enumerated inputs: the engagement profile, our own
compliance packs, and the sector/scope tag values the tagger emits from a fixed
vocabulary. Scan-derived free text (hostnames, domains, banners) never reaches
it — that stays inside the fenced, untrusted <security_context>.

The block sits between the task rules and the security context, so it is part
of the cached prompt prefix and costs nothing on repeat turns.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from app.ai.skills import select_skill
from app.compliance.profile import JURISDICTIONS, EngagementProfile
from app.compliance.registry import CATEGORY_THEMES, applicable_frameworks, reporting_clocks

# Only these tag namespaces carry enumerated values safe for the system prompt.
_TRUSTED_TAG_KEYS = ("sector_fn:", "compliance_scope:")
_DEFAULT_THEMES = ("patch_vulnerability_mgmt", "secure_configuration", "access_control", "incident_response")
_MAX_CHARS = 9000


@dataclass(frozen=True)
class DomainBrief:
    skill_id: str
    skill_label: str
    reason: str
    jurisdictions: list[str]
    framework_ids: list[str] = field(default_factory=list)
    text: str = ""


def trusted_tags(tags: Iterable[str]) -> set[str]:
    return {t for t in tags if t.startswith(_TRUSTED_TAG_KEYS)}


def _hours(h: float) -> str:
    return f"{h:g}h" if h < 48 else f"{h / 24:g} days"


def build_domain_brief(profile: EngagementProfile, tags: Iterable[str] = (),
                       categories: Iterable[str] = ()) -> DomainBrief:
    safe = trusted_tags(tags)
    skill, reason = select_skill(profile.sector, safe)
    frameworks = applicable_frameworks(profile, safe)
    themes: list[str] = []
    for cat in categories:
        for th in CATEGORY_THEMES.get(cat, ()):
            if th not in themes:
                themes.append(th)
    for th in _DEFAULT_THEMES:
        if th not in themes:
            themes.append(th)

    lines = [f'<domain_expertise skill="{skill.id}">',
             f"ROLE: {skill.persona}",
             "LANGUAGE: speak the customer's industry language. Prefer: "
             + "; ".join(f'"{b}" over "{a}"' for a, b in skill.vocabulary) + ".",
             "FRAME BUSINESS IMPACT THROUGH: " + "; ".join(skill.impact_lens) + ".",
             "SECTOR BEST PRACTICES (recommend only where relevant to the evidence): "
             + "; ".join(skill.best_practices) + "."]

    if profile.jurisdictions:
        names = ", ".join(JURISDICTIONS[j] for j in profile.jurisdictions)
        lines.append(f"REGULATORY LENS: the customer is regulated in {names}.")
    else:
        lines.append("REGULATORY LENS: no jurisdiction is configured for this engagement; refer only to "
                     "global frameworks (ISO 27001, NIST, PCI DSS where card data is involved) and suggest "
                     "the operator set the engagement's jurisdictions for regional guidance.")

    if frameworks:
        lines.append("<compliance_reference>")
        for fw in frameworks:
            lines.append(f"- {fw.name} [{fw.authority}] ({fw.granularity}-level):")
            # Themes that resolve to the same controls (typically the framework
            # baseline) share one line — same facts, far fewer tokens.
            grouped: dict[tuple[str, ...], list[str]] = {}
            for th in themes:
                grouped.setdefault(fw.controls_for(th).controls, []).append(th)
            for controls, ths in grouped.items():
                lines.append(f"    {', '.join(ths)}: " + " | ".join(controls))
        lines.append("</compliance_reference>")
        clocks = reporting_clocks(frameworks)
        if clocks:
            lines.append("INCIDENT-REPORTING CLOCKS (if a weakness is found to have been exploited): "
                         + "; ".join(f"{c['authority']} {_hours(c['deadline_hours'])} — {c['trigger']} ({c['reference']})"
                                     for c in clocks) + ".")

    lines.append("COMPLIANCE CITATION RULES: cite a regulatory control only if it appears verbatim in "
                 "<compliance_reference> above; never invent control numbers, articles, deadlines or "
                 "regulators. Present mappings as pointers for the compliance team, not legal advice or "
                 "an attestation. When unsure whether a rule applies, say so.")
    lines.append("</domain_expertise>")

    text = "\n".join(lines)
    if len(text) > _MAX_CHARS:
        # Drop the per-theme detail before anything else; the rules must survive.
        head, _, rest = text.partition("<compliance_reference>")
        _, _, tail = rest.partition("</compliance_reference>")
        summary = "<compliance_reference>\n" + "\n".join(f"- {fw.name} [{fw.authority}]" for fw in frameworks) \
            + "\n(control detail omitted for length — cite frameworks by name only)\n</compliance_reference>"
        text = head + summary + tail
    return DomainBrief(skill_id=skill.id, skill_label=skill.label, reason=reason,
                       jurisdictions=list(profile.jurisdictions),
                       framework_ids=[fw.id for fw in frameworks], text=text)
