"""Use-case library guards.

FORBIDDEN is a *living* set: a phrase stays here only while the capability it
describes is unbuilt. Each task that builds a capability lifts its own guard
(removes the phrase) and adds a positive assertion below. At the end of the
plan only "modbus" remains forbidden — it is deliberately never built.
"""
from agent.use_cases import USE_CASES, resolve

FORBIDDEN = {
    "uc_windows_estate": ["shares exposed"],
    "uc_iot_device_survey": ["modbus", "banner"],
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
