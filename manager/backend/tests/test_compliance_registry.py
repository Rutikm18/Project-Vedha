"""Regional compliance registry: pack integrity, applicability, per-finding obligations."""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.compliance.profile import EngagementProfile, profile_from_roe
from app.compliance.registry import (
    CATEGORY_THEMES,
    FRAMEWORKS,
    THEMES,
    applicable_frameworks,
    finding_obligations,
    reporting_clocks,
)


def _ids(frameworks) -> set[str]:
    return {f.id for f in frameworks}


def _finding(title: str):
    return SimpleNamespace(title=title, description="", cve_ids=[], remediation="")


# ── pack integrity ───────────────────────────────────────────────────────────

def test_every_category_maps_to_known_themes():
    for category, themes in CATEGORY_THEMES.items():
        assert themes, category
        assert set(themes) <= set(THEMES), category


def test_every_framework_covers_every_theme_with_real_controls():
    for fw in FRAMEWORKS.values():
        assert fw.name and fw.authority and fw.source
        for theme in THEMES:
            ref = fw.controls_for(theme)
            assert ref.controls and all(isinstance(c, str) and c.strip() for c in ref.controls), (fw.id, theme)
            assert ref.rationale, (fw.id, theme)


def test_framework_ids_unique_and_jurisdictions_known():
    known = {"GLOBAL", "IN", "EU", "UK", "US", "SA", "AE", "SG", "HK"}
    for fw in FRAMEWORKS.values():
        assert set(fw.jurisdictions) <= known, fw.id


def test_reporting_obligations_have_positive_deadlines():
    for fw in FRAMEWORKS.values():
        for r in fw.reporting:
            assert r.deadline_hours > 0 and r.authority and r.trigger


# ── profile ──────────────────────────────────────────────────────────────────

def test_profile_validation():
    p = EngagementProfile(sector="banking", jurisdictions=["in", "EU", "IN"])
    assert p.jurisdictions == ["IN", "EU"]
    with pytest.raises(ValidationError):
        EngagementProfile(sector="casino", jurisdictions=["IN"])
    with pytest.raises(ValidationError):
        EngagementProfile(sector="banking", jurisdictions=["XX"])


def test_profile_from_roe_defaults_to_generic_global():
    assert profile_from_roe(None) == EngagementProfile()
    assert profile_from_roe({"profile": {"sector": "bogus"}}) == EngagementProfile()
    assert profile_from_roe({"profile": {"sector": "insurance", "jurisdictions": ["IN"]}}).sector == "insurance"


# ── applicability ────────────────────────────────────────────────────────────

def test_indian_bank():
    ids = _ids(applicable_frameworks(EngagementProfile(sector="banking", jurisdictions=["IN"])))
    assert {"rbi_csf", "rbi_itgov_2023", "certin_2022", "dpdp_2023"} <= ids
    assert not ids & {"sebi_cscrf", "irdai_isg", "nydfs_500", "dora", "gdpr"}


def test_indian_insurer_and_broker():
    ins = _ids(applicable_frameworks(EngagementProfile(sector="insurance", jurisdictions=["IN"])))
    assert {"irdai_isg", "certin_2022", "dpdp_2023"} <= ins and "rbi_csf" not in ins
    cm = _ids(applicable_frameworks(EngagementProfile(sector="capital_markets", jurisdictions=["IN"])))
    assert "sebi_cscrf" in cm


def test_eu_bank_and_us_bank():
    eu = _ids(applicable_frameworks(EngagementProfile(sector="banking", jurisdictions=["EU"])))
    assert {"dora", "gdpr", "nis2"} <= eu
    us = _ids(applicable_frameworks(EngagementProfile(sector="banking", jurisdictions=["US"])))
    assert {"nydfs_500", "glba_safeguards"} <= us


def test_gulf_and_singapore():
    assert "sama_csf" in _ids(applicable_frameworks(EngagementProfile(sector="banking", jurisdictions=["SA"])))
    assert "mas_trm" in _ids(applicable_frameworks(EngagementProfile(sector="payments_fintech", jurisdictions=["SG"])))


def test_swift_cscf_triggered_by_tag_not_sector():
    prof = EngagementProfile(sector="banking", jurisdictions=["IN"])
    assert "swift_cscf" not in _ids(applicable_frameworks(prof))
    assert "swift_cscf" in _ids(applicable_frameworks(prof, tags={"compliance_scope:swift_cscf_scope"}))


def test_generic_profile_gets_no_regional_frameworks():
    assert _ids(applicable_frameworks(EngagementProfile())) == set()


# ── obligations for a finding ────────────────────────────────────────────────

def test_finding_obligations_for_indian_bank_patch_gap():
    prof = EngagementProfile(sector="banking", jurisdictions=["IN"])
    out = finding_obligations(_finding("Outdated OpenSSH 7.2 with known CVEs"), prof)
    by_id = {o["framework_id"]: o for o in out["frameworks"]}
    assert out["category"] == "outdated_ssh"
    assert "patch_vulnerability_mgmt" in out["themes"]
    rbi = by_id["rbi_csf"]
    assert any("Patch" in c for c in rbi["controls"])
    assert rbi["jurisdictions"] == ["IN"]
    assert out["disclaimer"]


def test_reporting_clocks_shortest_first():
    prof = EngagementProfile(sector="banking", jurisdictions=["IN", "EU"])
    clocks = reporting_clocks(applicable_frameworks(prof))
    hours = [c["deadline_hours"] for c in clocks]
    assert hours == sorted(hours)
    assert clocks[0]["deadline_hours"] <= 6


def test_shared_reporting_obligation_is_listed_once():
    prof = EngagementProfile(sector="banking", jurisdictions=["IN"])
    certin = [c for c in reporting_clocks(applicable_frameworks(prof)) if c["authority"] == "CERT-In"]
    assert len(certin) == 1
