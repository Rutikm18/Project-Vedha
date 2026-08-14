"""
test_device_profile.py — the probe device_inventory → Asset role mapping.

Pure mapping (no DB) covering: every classifier device_type → AssetType, the
unmappable roles (unknown/ambiguous) that must leave asset_type alone, role_detail
+ confidence pass-through, and malformed input.
"""
from __future__ import annotations

from app.discovery.device_profile import asset_type_for, device_profiles
from app.models.enums import AssetType


def test_every_device_type_maps_to_the_right_asset_type():
    assert asset_type_for("workstation") == AssetType.workstation
    assert asset_type_for("server") == AssetType.server
    assert asset_type_for("network_device") == AssetType.network
    assert asset_type_for("printer") == AssetType.printer
    assert asset_type_for("hypervisor") == AssetType.hypervisor
    assert asset_type_for("iot") == AssetType.iot


def test_unmappable_roles_leave_asset_type_untouched():
    # unknown/ambiguous have no clean enum counterpart → None (keep existing).
    assert asset_type_for("unknown") is None
    assert asset_type_for("ambiguous") is None
    assert asset_type_for(None) is None


def test_device_profiles_extracts_role_detail_and_confidence():
    result = {
        "scan_type": "device_inventory",
        "devices": [
            {"ip": "10.0.0.5", "device_type": "server",
             "role_detail": "domain_controller", "confidence": 0.9},
            {"ip": "10.0.0.6", "device_type": "printer",
             "role_detail": "print_server", "confidence": 0.75},
        ],
    }
    profiles = device_profiles(result)

    dc = profiles["10.0.0.5"]
    assert dc["asset_type"] == AssetType.server
    assert dc["device_role"] == "server"
    assert dc["role_detail"] == "domain_controller"
    assert dc["role_confidence"] == 0.9

    printer = profiles["10.0.0.6"]
    assert printer["asset_type"] == AssetType.printer
    assert printer["role_confidence"] == 0.75


def test_ambiguous_keeps_asset_type_none_but_records_role():
    result = {"devices": [
        {"ip": "10.0.0.7", "device_type": "ambiguous",
         "role_detail": "printer_or_server", "confidence": 0.5},
    ]}
    prof = device_profiles(result)["10.0.0.7"]
    assert prof["asset_type"] is None          # do not overwrite a known type
    assert prof["device_role"] == "ambiguous"  # but keep the honest label
    assert prof["role_detail"] == "printer_or_server"


def test_non_device_inventory_result_yields_no_profiles():
    assert device_profiles({"scan_type": "discovery", "hosts": [{"ip": "1.2.3.4"}]}) == {}
    assert device_profiles({}) == {}
    assert device_profiles(None) == {}


def test_malformed_entries_are_skipped():
    result = {"devices": ["not-a-dict", {"device_type": "server"}, {"ip": "1.1.1.1", "device_type": "iot"}]}
    profiles = device_profiles(result)
    assert set(profiles) == {"1.1.1.1"}   # no ip / not-a-dict entries dropped
    assert profiles["1.1.1.1"]["asset_type"] == AssetType.iot
