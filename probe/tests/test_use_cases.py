"""Use-case library guards.

FORBIDDEN is a *living* set: a phrase stays here only while the capability it
describes is unbuilt. Each task that builds a capability lifts its own guard
(removes the phrase) and adds a positive assertion below. At the end of the
plan only "modbus" remains forbidden — it is deliberately never built.
"""
import pytest

from agent.use_cases import (
    USE_CASES,
    USE_CASE_CODES,
    INTENSITY_CODES,
    resolve,
    use_case_for_code,
    normalize_intensity,
)

FORBIDDEN = {
    "uc_windows_estate": ["shares exposed"],
    "uc_iot_device_survey": ["modbus"],
}


def test_descriptions_do_not_overclaim():
    for uc_id, banned in FORBIDDEN.items():
        desc = USE_CASES[uc_id]["description"].lower()
        for phrase in banned:
            assert phrase not in desc, f"{uc_id} still claims '{phrase}'"


def test_windows_estate_claims_signing():
    assert "signing" in USE_CASES["uc_windows_estate"]["description"].lower()


def test_udp_claims_amplification():
    d = USE_CASES["uc_udp_service_exposure"]["description"].lower()
    assert "amplification" in d or "monlist" in d


def test_web_claims_methods():
    assert "method" in USE_CASES["uc_web_app_triage"]["description"].lower()


def test_iot_survey_collects_banners():
    scan_type, profile, intensity = resolve("uc_iot_device_survey", None, {})
    assert scan_type == "service_fingerprint"   # reaches the banner stage
    assert profile == "iot"
    assert intensity == "standard"              # default when the use-case omits it


def test_new_use_cases_resolve():
    for uc_id, expected_type in (
        ("uc_device_inventory", "device_inventory"),
        ("uc_full_port_audit", "full_port_audit"),
        ("uc_exposure_matrix", "exposure_matrix"),
    ):
        scan_type, profile, intensity = resolve(uc_id, None, {})
        assert scan_type == expected_type
        assert profile == "it"
        assert intensity in {"light", "standard", "deep"}


def test_full_port_audit_is_deep():
    _st, _profile, intensity = resolve("uc_full_port_audit", None, {})
    assert intensity == "deep"


def test_params_intensity_overrides_use_case():
    _st, _profile, intensity = resolve(
        "uc_full_port_audit", None, {"intensity": "light"}
    )
    assert intensity == "light"


# ── Numeric protocol ─────────────────────────────────────────────────────────
def test_every_code_maps_to_a_real_use_case():
    for code, uc_id in USE_CASE_CODES.items():
        assert uc_id in USE_CASES, f"code {code} → unknown {uc_id}"


def test_codes_are_unique_and_stable():
    assert len(set(USE_CASE_CODES.values())) == len(USE_CASE_CODES)   # no dup use-cases
    # anchor a few well-known codes so a renumber is caught
    assert USE_CASE_CODES[1] == "uc_discovery_only"
    assert USE_CASE_CODES[80] == "uc_full_port_audit"
    assert USE_CASE_CODES[81] == "uc_exposure_matrix"


def test_resolve_by_numeric_code():
    scan_type, profile, intensity = resolve(None, None, {"uc": 80, "intensity": 3})
    assert (scan_type, profile, intensity) == ("full_port_audit", "it", "deep")


def test_resolve_accepts_string_digits_too():
    scan_type, _profile, intensity = resolve(None, None, {"uc": "1", "intensity": "2"})
    assert scan_type == "discovery" and intensity == "standard"


def test_intensity_code_and_name_equivalent():
    assert normalize_intensity(1) == "light"
    assert normalize_intensity("deep") == "deep"
    assert normalize_intensity(None) is None


def test_unknown_code_is_rejected():
    with pytest.raises(ValueError, match="Unknown use-case code"):
        use_case_for_code(999)
    with pytest.raises(ValueError, match="Unknown intensity code"):
        normalize_intensity(9)


def test_string_use_case_id_still_wins_over_code():
    # An explicit use_case_id takes precedence; the code path is the fallback.
    scan_type, _p, _i = resolve("uc_device_inventory", None, {"uc": 80})
    assert scan_type == "device_inventory"
