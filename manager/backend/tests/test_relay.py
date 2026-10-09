"""Tests for app/detection/relay.py (P3: cross-asset NTLM relay and credential links)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from app.detection.relay import (
    CredentialLink,
    RelayLink,
    _P_CRED_HEURISTIC,
    _P_CRED_LAPS_ABSENT,
    _P_CRED_NAME_AND_LAPS,
    _P_CRED_NAME_MATCH,
    _P_RELAY_CONFIRMED,
    _P_RELAY_DC,
    _P_RELAY_HEURISTIC,
    _P_SNMP_LATERAL,
    derive_credential_links,
    derive_relay_links,
)


# ── minimal Finding stand-in ──────────────────────────────────────────────────


@dataclass
class _F:
    id: str
    asset_id: str
    rule_id: str
    status: str = "open"
    evidence: dict = field(default_factory=dict)


# ── derive_relay_links ─────────────────────────────────────────────────────────


def test_empty_findings_returns_no_relay_links():
    assert derive_relay_links([]) == []


def test_only_relay_targets_no_coercion_source_returns_empty():
    findings = [_F("f1", "a1", "CORR-NTLM-RELAY-PATH")]
    assert derive_relay_links(findings) == []


def test_only_coercion_source_no_relay_target_returns_empty():
    findings = [_F("f1", "a1", "POSTURE-MSRPC-EPMAP-EXPOSED")]
    assert derive_relay_links(findings) == []


def test_confirmed_coercion_to_relay_target_emits_link():
    findings = [
        _F("f1", "coerce_src", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "relay_tgt", "CORR-NTLM-RELAY-PATH"),
    ]
    links = derive_relay_links(findings)
    assert len(links) == 1
    link = links[0]
    assert isinstance(link, RelayLink)
    assert link.source_asset_id == "coerce_src"
    assert link.target_asset_id == "relay_tgt"
    assert link.confidence == _P_RELAY_CONFIRMED
    assert link.basis == "relay_confirmed"
    assert link.technique == "T1557.001"


def test_relay_to_dc_gets_higher_confidence():
    findings = [
        _F("f1", "coerce_src", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "dc_host", "CORR-NTLM-RELAY-PATH", evidence={"domain_controller": True}),
    ]
    links = derive_relay_links(findings)
    assert len(links) == 1
    link = links[0]
    assert link.confidence == _P_RELAY_DC
    assert link.is_dc_target is True


def test_posture_smb_signing_off_also_a_relay_target():
    findings = [
        _F("f1", "coerce_src", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "relay_tgt", "POSTURE-SMB-SIGNING-OFF"),
    ]
    links = derive_relay_links(findings)
    assert len(links) == 1
    assert links[0].target_asset_id == "relay_tgt"


def test_heuristic_coercion_source_lower_confidence():
    findings = [
        _F("f1", "win_host", "CORR-LEGACY-WINDOWS-SURFACE"),  # heuristic coerce source
        _F("f2", "relay_tgt", "CORR-NTLM-RELAY-PATH"),
    ]
    links = derive_relay_links(findings)
    assert len(links) == 1
    assert links[0].confidence == _P_RELAY_HEURISTIC
    assert links[0].basis == "relay_heuristic"


def test_same_asset_coercion_and_relay_skipped():
    """An asset that is both coercible and relay-target should NOT get a self-loop.
    The P2 compound rule handles the single-asset case.
    """
    findings = [
        _F("f1", "a1", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "a1", "CORR-NTLM-RELAY-PATH"),
    ]
    links = derive_relay_links(findings)
    # No cross-asset pair → no links (the self-loop (a1 → a1) is filtered out)
    assert all(lk.source_asset_id != lk.target_asset_id for lk in links)


def test_multiple_coerce_sources_multiple_relay_targets():
    """Two coercion sources × two relay targets = 4 cross-asset pairs."""
    findings = [
        _F("f1", "src1", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "src2", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f3", "tgt1", "CORR-NTLM-RELAY-PATH"),
        _F("f4", "tgt2", "POSTURE-SMB-SIGNING-OFF"),
    ]
    links = derive_relay_links(findings)
    pairs = {(lk.source_asset_id, lk.target_asset_id) for lk in links}
    assert ("src1", "tgt1") in pairs
    assert ("src1", "tgt2") in pairs
    assert ("src2", "tgt1") in pairs
    assert ("src2", "tgt2") in pairs


def test_dedup_keeps_highest_confidence():
    """When both a confirmed and heuristic edge exist for same pair, keep confirmed."""
    findings = [
        _F("f1", "src", "POSTURE-MSRPC-EPMAP-EXPOSED"),   # confirmed
        _F("f2", "src", "CORR-NTLM-RELAY-PATH"),           # heuristic coerce
        _F("f3", "tgt", "CORR-NTLM-RELAY-PATH"),
    ]
    links = derive_relay_links(findings)
    # Both a confirmed (src coerce MSRPC → tgt relay) and heuristic exist for same pair
    pair_links = [lk for lk in links if lk.source_asset_id == "src" and lk.target_asset_id == "tgt"]
    assert len(pair_links) == 1
    assert pair_links[0].confidence == _P_RELAY_CONFIRMED  # confirmed wins


def test_closed_finding_skipped():
    findings = [
        _F("f1", "src", "POSTURE-MSRPC-EPMAP-EXPOSED", status="resolved"),
        _F("f2", "tgt", "CORR-NTLM-RELAY-PATH"),
    ]
    assert derive_relay_links(findings) == []


def test_relay_link_label_contains_asset_ids():
    findings = [
        _F("f1", "coerce_host", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "sign_off_host", "CORR-NTLM-RELAY-PATH"),
    ]
    links = derive_relay_links(findings)
    assert "coerce_host" in links[0].label
    assert "sign_off_host" in links[0].label


# ── derive_credential_links ───────────────────────────────────────────────────


def test_empty_findings_returns_no_cred_links():
    assert derive_credential_links([]) == []


def test_single_windows_host_no_cred_links():
    findings = [_F("f1", "a1", "CORR-NTLM-RELAY-PATH")]
    # Need at least 2 Windows hosts for a CREDENTIAL_REUSE edge
    assert derive_credential_links(findings) == []


def test_two_windows_hosts_heuristic_cred_link():
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH"),
        _F("f2", "win2", "CORR-LEGACY-WINDOWS-SURFACE"),
    ]
    links = derive_credential_links(findings)
    assert len(links) == 1
    link = links[0]
    assert isinstance(link, CredentialLink)
    assert link.confidence == _P_CRED_HEURISTIC
    assert link.basis == "windows_heuristic"
    assert link.laps_confirmed_absent is False
    asset_pair = {link.asset_id_a, link.asset_id_b}
    assert asset_pair == {"win1", "win2"}


def test_laps_absent_on_both_raises_confidence():
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH", evidence={"laps_enabled": False}),
        _F("f2", "win2", "CORR-NTLM-RELAY-PATH", evidence={"laps_enabled": False}),
    ]
    links = derive_credential_links(findings)
    assert len(links) == 1
    link = links[0]
    assert link.confidence == _P_CRED_LAPS_ABSENT
    assert link.laps_confirmed_absent is True


def test_shared_admin_name_raises_confidence():
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH",
           evidence={"local_admin_name": "Administrator"}),
        _F("f2", "win2", "CORR-LEGACY-WINDOWS-SURFACE",
           evidence={"local_admin_name": "Administrator"}),
    ]
    links = derive_credential_links(findings)
    assert len(links) == 1
    assert links[0].confidence == _P_CRED_NAME_MATCH
    assert "administrator" in links[0].label.lower()


def test_shared_admin_name_and_laps_absent_highest_confidence():
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH",
           evidence={"laps_enabled": False, "local_admin_name": "svc-backup"}),
        _F("f2", "win2", "CORR-NTLM-RELAY-PATH",
           evidence={"laps_enabled": False, "local_admin_name": "svc-backup"}),
    ]
    links = derive_credential_links(findings)
    assert len(links) == 1
    link = links[0]
    assert link.confidence == _P_CRED_NAME_AND_LAPS
    assert link.laps_confirmed_absent is True


def test_laps_present_on_one_host_no_cred_link():
    """LAPS present on either host means no shared-admin path."""
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH", evidence={"laps_enabled": True}),
        _F("f2", "win2", "CORR-LEGACY-WINDOWS-SURFACE"),
    ]
    links = derive_credential_links(findings)
    assert len(links) == 0


def test_different_admin_names_no_name_match_link():
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH",
           evidence={"local_admin_name": "admin1"}),
        _F("f2", "win2", "CORR-NTLM-RELAY-PATH",
           evidence={"local_admin_name": "admin2"}),
    ]
    links = derive_credential_links(findings)
    # No name match, no LAPS evidence → heuristic
    assert links[0].confidence == _P_CRED_HEURISTIC


def test_admin_name_list_evidence():
    """local_admin_name may be a list of names."""
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH",
           evidence={"local_admin_name": ["Administrator", "backup_svc"]}),
        _F("f2", "win2", "CORR-NTLM-RELAY-PATH",
           evidence={"local_admin_name": ["backup_svc", "svc_monitor"]}),
    ]
    links = derive_credential_links(findings)
    assert len(links) == 1
    assert links[0].confidence == _P_CRED_NAME_MATCH
    assert "backup_svc" in links[0].label


def test_snmp_lateral_links_between_network_devices():
    findings = [
        _F("f1", "sw1", "CORR-SNMP-PUBLIC-LATERAL"),
        _F("f2", "sw2", "CORR-SNMP-PUBLIC-LATERAL"),
        _F("f3", "sw3", "CORR-SNMP-PUBLIC-LATERAL"),
    ]
    links = derive_credential_links(findings)
    snmp_links = [lk for lk in links if lk.basis == "snmp_default_community"]
    # 3 switches → 3 pairs: (sw1,sw2), (sw1,sw3), (sw2,sw3)
    assert len(snmp_links) == 3
    assert all(lk.confidence == _P_SNMP_LATERAL for lk in snmp_links)
    assert all(lk.technique == "T1602.001" for lk in snmp_links)


def test_snmp_single_device_no_links():
    findings = [_F("f1", "sw1", "CORR-SNMP-PUBLIC-LATERAL")]
    snmp_links = [lk for lk in derive_credential_links(findings)
                  if lk.basis == "snmp_default_community"]
    assert len(snmp_links) == 0


def test_closed_finding_not_counted_for_cred_links():
    findings = [
        _F("f1", "win1", "CORR-NTLM-RELAY-PATH", status="resolved"),
        _F("f2", "win2", "CORR-NTLM-RELAY-PATH"),
    ]
    links = derive_credential_links(findings)
    # win1 is resolved → only win2 is a Windows host → no pair → no links
    assert len(links) == 0


def test_posture_msrpc_also_counts_as_windows_host():
    findings = [
        _F("f1", "win1", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "win2", "CORR-NTLM-RELAY-PATH"),
    ]
    links = derive_credential_links(findings)
    assert len(links) == 1


# ── integration: relay + cred together ───────────────────────────────────────


def test_relay_and_cred_independent():
    """Relay links and credential links are derived independently — both must fire."""
    findings = [
        _F("f1", "src", "POSTURE-MSRPC-EPMAP-EXPOSED"),
        _F("f2", "tgt", "CORR-NTLM-RELAY-PATH"),
        _F("f3", "win3", "CORR-LEGACY-WINDOWS-SURFACE"),
    ]
    relay_links = derive_relay_links(findings)
    cred_links = derive_credential_links(findings)
    # relay: src → tgt
    assert any(lk.source_asset_id == "src" and lk.target_asset_id == "tgt"
               for lk in relay_links)
    # cred: Windows pair (src+tgt, src+win3, tgt+win3) at least one pair
    assert len(cred_links) >= 1
