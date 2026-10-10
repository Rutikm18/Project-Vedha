"""P4b — crown-jewel suggestion when the operator marked nothing critical (FM-04).

Operator-marked targets always win; only when none is marked are high-value hosts
(domain controller, hypervisor, datastore) suggested, each with its reason, and the
caller records that the targets were SUGGESTED, not chosen.
"""
from __future__ import annotations

from types import SimpleNamespace as NS

from app.detection.crown_jewels import suggest_crown_jewels


def _asset(aid, asset_type="server", device_role=None, role_detail=None, role_confidence=None):
    return NS(id=aid, asset_type=asset_type, device_role=device_role,
              role_detail=role_detail, role_confidence=role_confidence)


def _svc(aid, port):
    return NS(asset_id=aid, port=port)


def test_a_domain_controller_is_suggested():
    assets = [_asset("a1"), _asset("dc", role_detail="domain_controller", role_confidence=0.9)]
    out = suggest_crown_jewels(assets, [])
    assert out == [{"asset_id": "dc", "reason": "domain controller"}]


def test_a_hypervisor_is_suggested():
    assets = [_asset("h1", asset_type="hypervisor", role_confidence=0.8)]
    out = suggest_crown_jewels(assets, [])
    assert out == [{"asset_id": "h1", "reason": "virtualization host"}]


def test_a_datastore_service_makes_its_host_a_suggested_jewel():
    assets = [_asset("db1")]
    out = suggest_crown_jewels(assets, [_svc("db1", 5432)])
    assert out == [{"asset_id": "db1", "reason": "datastore"}]


def test_most_important_role_wins_when_a_host_matches_several():
    # a DC that also answers on a datastore port is reported as a domain controller
    assets = [_asset("dc", role_detail="domain_controller", role_confidence=0.9)]
    out = suggest_crown_jewels(assets, [_svc("dc", 1433)])
    assert out == [{"asset_id": "dc", "reason": "domain controller"}]


def test_low_confidence_role_is_not_suggested():
    assets = [_asset("x", role_detail="domain_controller", role_confidence=0.4)]
    assert suggest_crown_jewels(assets, []) == []


def test_nothing_high_value_suggests_nothing():
    assets = [_asset("a1"), _asset("a2", asset_type="workstation")]
    assert suggest_crown_jewels(assets, [_svc("a1", 80)]) == []


def test_ordering_is_dc_then_hypervisor_then_datastore_then_by_id():
    assets = [
        _asset("z-db"),
        _asset("m-hv", asset_type="hypervisor", role_confidence=0.9),
        _asset("a-dc", role_detail="domain_controller", role_confidence=0.9),
    ]
    out = suggest_crown_jewels(assets, [_svc("z-db", 27017)])
    reasons = [o["reason"] for o in out]
    assert reasons == ["domain controller", "virtualization host", "datastore"]
