"""
test_enqueue_intensity.py — the manager's first-class scan-intensity knob.

Operators pick light/standard/deep on the job; the manager validates it at
enqueue (not silently at the probe) and forwards it in the job params.
"""
from __future__ import annotations

import uuid

import pytest
from pydantic import ValidationError

from app.routers.agents import (
    EnqueueJobRequest,
    _USE_CASES,
    _USE_CASE_CODES,
    _INTENSITY_CODES,
    _VALID_INTENSITIES,
    _normalize_intensity_name,
)


def test_valid_intensity_is_accepted():
    for level in ("light", "standard", "deep"):
        req = EnqueueJobRequest(engagement_id=uuid.uuid4(), intensity=level)
        assert req.intensity == level


def test_omitted_intensity_is_none():
    # None → the probe applies the use-case's own default intensity.
    assert EnqueueJobRequest(engagement_id=uuid.uuid4()).intensity is None


def test_invalid_intensity_is_rejected_at_the_schema():
    with pytest.raises(ValidationError):
        EnqueueJobRequest(engagement_id=uuid.uuid4(), intensity="ludicrous")


def test_valid_intensities_mirror_the_probe_set():
    assert _VALID_INTENSITIES == {"light", "standard", "deep"}


def test_use_case_catalog_exposes_intensity_for_new_cases():
    # The GET /use-cases response spreads these, so the UI can preselect a default.
    assert _USE_CASES["uc_full_port_audit"]["intensity"] == "deep"
    assert _USE_CASES["uc_device_inventory"]["intensity"] == "standard"
    assert _USE_CASES["uc_exposure_matrix"]["intensity"] == "standard"


# ── Numeric protocol ─────────────────────────────────────────────────────────
def test_numeric_uc_code_accepted():
    req = EnqueueJobRequest(engagement_id=uuid.uuid4(), uc=80, intensity=3)
    assert req.uc == 80


def test_unknown_uc_code_rejected():
    with pytest.raises(ValidationError):
        EnqueueJobRequest(engagement_id=uuid.uuid4(), uc=999)


def test_intensity_accepts_code_or_name():
    assert EnqueueJobRequest(engagement_id=uuid.uuid4(), intensity=3).intensity == 3
    assert EnqueueJobRequest(engagement_id=uuid.uuid4(), intensity="deep").intensity == "deep"
    with pytest.raises(ValidationError):
        EnqueueJobRequest(engagement_id=uuid.uuid4(), intensity=9)


def test_normalize_intensity_name_maps_codes():
    assert _normalize_intensity_name(1) == "light"
    assert _normalize_intensity_name("2") == "standard"
    assert _normalize_intensity_name("deep") == "deep"
    assert _normalize_intensity_name(None) is None


def test_every_manager_code_maps_to_a_known_use_case():
    for code, uc_id in _USE_CASE_CODES.items():
        assert uc_id in _USE_CASES
    assert _INTENSITY_CODES == {1: "light", 2: "standard", 3: "deep"}
