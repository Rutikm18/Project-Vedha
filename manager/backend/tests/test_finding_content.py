"""finding_content — deterministic, offline per-finding explanation + exploitation.

Pins the epistemic-honesty rule (unvalidated findings say so, in the exact agreed
words), the exploit-maturity derivation, and the criticality scaling of business
impact. Pure module → tested directly with SimpleNamespace stand-ins.
"""
from __future__ import annotations

from types import SimpleNamespace

from app.services.finding_content import (
    NOT_VALIDATED_NOTE,
    exploit_maturity,
    finding_content,
)


def _f(**kw):
    base = dict(
        title="",
        description="",
        remediation="",
        cve_ids=[],
        evidence={},
        cvss_score=None,
        epss_score=None,
        exploit_validated=False,
        severity="high",
    )
    base.update(kw)
    return SimpleNamespace(**base)


# The nine KB categories, one representative title each.
_TITLES = [
    "SSLv3 supported (POODLE)",
    "SMB signing not required",
    "RDP exposed on 3389",
    "Anonymous FTP login allowed",
    "OpenSSH weak ciphers (CBC)",
    "Default password on admin panel",
    "Telnet management interface exposed",
    "Missing security update MS17-010",
    "Something genuinely unusual",
]


def test_every_category_yields_nonempty_prose():
    for title in _TITLES:
        c = finding_content(_f(title=title))
        assert c.technical_details.strip(), title
        assert c.impact.strip(), title
        assert c.business_impact.strip(), title


def test_unvalidated_finding_uses_the_exact_honest_line():
    c = finding_content(_f(exploit_validated=False))
    assert c.exploitation.status == "not_validated"
    assert c.exploitation.note.startswith("Not validated")
    assert NOT_VALIDATED_NOTE in c.exploitation.note


def test_validated_finding_is_stated_plainly_not_hedged():
    c = finding_content(_f(exploit_validated=True))
    assert c.exploitation.status == "validated"
    assert c.exploitation.actively_exploited is True
    assert NOT_VALIDATED_NOTE not in c.exploitation.note


def test_kev_makes_it_weaponized_and_actively_exploited():
    c = finding_content(_f(evidence={"kev": True}))
    assert c.exploit_maturity == "WEAPONIZED"
    assert c.actively_exploited is True


def test_nested_enrichment_kev_is_honoured():
    c = finding_content(_f(evidence={"enrichment": {"kev": True}}))
    assert c.actively_exploited is True


def test_epss_thresholds_map_to_maturity_bands():
    assert exploit_maturity({"kev": False, "validated": False, "epss": 0.7, "poc": False}) == "WEAPONIZED"
    assert exploit_maturity({"kev": False, "validated": False, "epss": 0.2, "poc": False}) == "POC"
    assert exploit_maturity({"kev": False, "validated": False, "epss": 0.0, "poc": False}) == "THEORETICAL"


def test_poc_flag_lifts_theoretical_to_poc():
    assert exploit_maturity({"kev": False, "validated": False, "epss": None, "poc": True}) == "POC"


def test_business_impact_scales_up_for_a_critical_asset():
    low = finding_content(_f(title="RDP exposed"), asset_criticality="low")
    crit = finding_content(_f(title="RDP exposed"), asset_criticality="critical")
    assert len(crit.business_impact) > len(low.business_impact)
    assert "critical" in crit.business_impact.lower()


def test_active_exploitation_adds_urgency_to_business_impact():
    calm = finding_content(_f(title="RDP exposed", severity="high"))
    hot = finding_content(_f(title="RDP exposed", severity="high", evidence={"kev": True}))
    assert len(hot.business_impact) > len(calm.business_impact)


def test_cves_are_woven_into_technical_details():
    c = finding_content(_f(title="Missing patch", cve_ids=["CVE-2017-0144"]))
    assert "CVE-2017-0144" in c.technical_details


def test_overrides_take_precedence_field_by_field():
    c = finding_content(_f(), overrides={"business_impact": "Analyst-authored impact."})
    assert c.business_impact == "Analyst-authored impact."
    # Non-overridden fields still come from the KB.
    assert c.technical_details.strip()


def test_to_dict_is_api_shaped():
    d = finding_content(_f(evidence={"kev": True})).to_dict()
    assert d["exploit_maturity"] == "WEAPONIZED"
    assert d["actively_exploited"] is True
    for key in ("impact", "business_impact", "technical_details", "exploitation"):
        assert key in d
    assert d["exploitation"]["note"]
