"""Tests for app/detection/crown_jewels.py (P4b: auto crown-jewel selection)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from app.detection.crown_jewels import (
    auto_crown_jewel_ids,
    auto_crown_jewels,
    score_assets,
)


# ── test fixtures ──────────────────────────────────────────────────────────────


@dataclass
class _Asset:
    id: str
    hostname: str | None = None
    ip_address: str | None = None
    device_role: str | None = None
    role_detail: str | None = None
    criticality: str = "medium"


@dataclass
class _Service:
    asset_id: str
    port: int
    service_name: str = ""
    banner: str = ""
    exposure: str = "internal_only"


def _dc(asset_id: str = "dc1", hostname: str = "dc01.corp.local") -> _Asset:
    return _Asset(id=asset_id, hostname=hostname, role_detail="domain_controller")


def _db(asset_id: str = "db1", hostname: str = "db01.corp.local") -> _Asset:
    return _Asset(id=asset_id, hostname=hostname)


def _generic(asset_id: str = "w1", hostname: str = "workstation01") -> _Asset:
    return _Asset(id=asset_id, hostname=hostname)


# ── score_assets ───────────────────────────────────────────────────────────────


def test_dc_by_role_detail_scores_high():
    assets = [_dc()]
    scores = score_assets(assets, [])
    assert scores[0].score >= 50
    assert scores[0].role == "dc"


def test_dc_by_kerberos_port_scores_high():
    assets = [_generic("a1")]
    services = [
        _Service(asset_id="a1", port=88),   # Kerberos
        _Service(asset_id="a1", port=389),  # LDAP
        _Service(asset_id="a1", port=3268), # Global Catalog
    ]
    scores = score_assets(assets, services)
    assert scores[0].score >= 30
    assert scores[0].role == "dc"


def test_dc_by_hostname_pattern():
    assets = [_Asset(id="a1", hostname="dc01.internal")]
    scores = score_assets(assets, [])
    assert any("hostname_pattern" in s for s in scores[0].signals)
    assert scores[0].role == "dc"


def test_hypervisor_by_port_902():
    """VMware vSphere SDK port is a highly specific signal."""
    assets = [_generic("esxi1")]
    services = [_Service(asset_id="esxi1", port=902)]
    scores = score_assets(assets, services)
    assert scores[0].score >= 20
    assert scores[0].role == "hypervisor"


def test_proxmox_port_8006():
    assets = [_generic("prox1")]
    services = [_Service(asset_id="prox1", port=8006)]
    scores = score_assets(assets, services)
    assert scores[0].role == "hypervisor"


def test_database_by_port():
    assets = [_db()]
    services = [
        _Service(asset_id="db1", port=5432),  # PostgreSQL
    ]
    scores = score_assets(assets, services)
    assert scores[0].role == "database"
    assert scores[0].score >= 10


def test_vault_by_port_8200():
    assets = [_Asset(id="v1", hostname="vault.ops.local")]
    services = [_Service(asset_id="v1", port=8200)]
    scores = score_assets(assets, services)
    assert scores[0].role == "iam"
    assert scores[0].score >= 20


def test_ot_port_s7comm_102():
    """S7comm is the highest-confidence OT signal."""
    assets = [_generic("plc1")]
    services = [_Service(asset_id="plc1", port=102)]
    scores = score_assets(assets, services)
    assert scores[0].role == "ot"
    assert scores[0].score >= 25


def test_modbus_port():
    assets = [_generic("rtu1")]
    services = [_Service(asset_id="rtu1", port=502)]
    scores = score_assets(assets, services)
    assert scores[0].role == "ot"


def test_generic_workstation_low_score():
    assets = [_generic()]
    services = [_Service(asset_id="w1", port=80), _Service(asset_id="w1", port=443)]
    scores = score_assets(assets, services)
    assert scores[0].score < 30


def test_banner_confirmation_dc():
    assets = [_generic("srv1")]
    services = [
        _Service(asset_id="srv1", port=389,
                 banner="defaultnamingcontext=dc=corp,dc=local"),
    ]
    scores = score_assets(assets, services)
    assert "banner_confirmed=dc" in scores[0].signals
    assert scores[0].score >= 30


def test_banner_confirmation_hypervisor():
    assets = [_generic("esxi1")]
    services = [
        _Service(asset_id="esxi1", port=443, banner="VMware ESXi 7.0"),
    ]
    scores = score_assets(assets, services)
    assert "banner_confirmed=hypervisor" in scores[0].signals


def test_multiple_assets_sorted_by_score():
    assets = [_dc("dc1"), _db("db1"), _generic("w1")]
    services = [
        _Service(asset_id="db1", port=5432),
    ]
    scores = score_assets(assets, services)
    assert scores[0].asset_id == "dc1"  # DC always ranks first


# ── auto_crown_jewels ─────────────────────────────────────────────────────────


def test_auto_selects_dc_and_db():
    assets = [_dc("dc1"), _db("db1"), _generic("w1")]
    services = [
        _Service(asset_id="dc1", port=88),
        _Service(asset_id="dc1", port=389),
        _Service(asset_id="db1", port=5432),
    ]
    selected = auto_crown_jewels(assets, services)
    selected_ids = {sc.asset_id for sc in selected}
    assert "dc1" in selected_ids


def test_workstations_below_threshold_not_selected():
    assets = [_generic("w1"), _generic("w2")]
    services = [
        _Service(asset_id="w1", port=80),
        _Service(asset_id="w2", port=443),
    ]
    selected = auto_crown_jewels(assets, services)
    assert len(selected) == 0


def test_ot_always_selected_when_present():
    """OT systems are always high-value regardless of other assets."""
    assets = [_Asset(id="plc1"), _generic("w1"), _generic("w2")]
    services = [_Service(asset_id="plc1", port=502)]
    selected = auto_crown_jewels(assets, services)
    assert any(sc.asset_id == "plc1" for sc in selected)


def test_max_targets_cap():
    assets = [_dc(f"dc{i}", f"dc{i}.internal") for i in range(20)]
    services = [_Service(asset_id=f"dc{i}", port=88) for i in range(20)]
    selected = auto_crown_jewels(assets, services, max_targets=5)
    assert len(selected) <= 5


def test_all_selected_are_marked():
    assets = [_dc("dc1"), _db("db1")]
    services = [
        _Service(asset_id="dc1", port=88),
        _Service(asset_id="db1", port=3306),
    ]
    selected = auto_crown_jewels(assets, services)
    for sc in selected:
        assert sc.auto_selected is True


def test_auto_crown_jewel_ids_returns_strings():
    assets = [_dc("dc1")]
    services = [_Service(asset_id="dc1", port=88)]
    ids = auto_crown_jewel_ids(assets, services)
    assert isinstance(ids, list)
    assert all(isinstance(i, str) for i in ids)
    assert "dc1" in ids


def test_empty_assets_returns_empty():
    assert auto_crown_jewels([], []) == []


def test_operator_tagged_critical_scores_max():
    """An operator-tagged critical asset always ranks first."""
    a = _Asset(id="crown", criticality="critical")
    b = _dc("dc1")
    scores = score_assets([a, b], [])
    assert scores[0].asset_id == "crown"
    assert scores[0].score == 200


def test_payment_hostname_detected():
    assets = [_Asset(id="pos1", hostname="pos01.retail.local")]
    scores = score_assets(assets, [])
    assert any("payment" in s for s in scores[0].signals)


def test_hypervisor_hostname_detected():
    assets = [_Asset(id="esxi1", hostname="esxi01.dc.local")]
    scores = score_assets(assets, [])
    assert scores[0].role == "hypervisor"
    assert scores[0].score >= 20
