"""
relay.py — P3: derive cross-asset NTLM relay edges and LAPS-aware shared-admin
credential links from posture/correlation findings.

Context (ATTACK_PATH_PLAN.md §3.4 / §9 FM-08, FM-09):
  Without explicit cross-asset edges the graph has no NTLM relay paths or shared-admin
  lateral movement paths. This module fills that gap.

  FM-08: shared local admin accounts are a pass-the-hash / pass-the-ticket lateral
  path, but only when LAPS is absent. Without checking LAPS, the old code emitted
  CREDENTIAL_REUSE edges for all Windows host pairs — many false positives. This
  module applies a tiered confidence model based on available evidence.

  FM-09: NTLM relay requires TWO preconditions on DIFFERENT assets: a coercion surface
  (MSRPC epmap exposed, or a host forced to authenticate) AND a relay target (SMB
  signing not required). Without explicit cross-asset edges, the graph treats these as
  independent single-host findings — no path crosses them.

NTLM relay precondition model:
  1. Relay TARGET: asset has SMB signing NOT required (CORR-NTLM-RELAY-PATH or
     POSTURE-SMB-SIGNING-OFF finding, or finding.evidence["domain_controller"]=True).
  2. Coercion SOURCE: asset has a confirmed MSRPC coercion surface
     (POSTURE-MSRPC-EPMAP-EXPOSED = high confidence) or is any Windows host with
     SMB/NTLM findings (heuristic, lower confidence — PrinterBug / PetitPotam).
  3. Source ≠ target.
  4. The P2 compound rule already emits a SyntheticFinding for hosts that are BOTH
     coercible AND relay-vulnerable (single-asset). This module handles the cross-asset
     case where the coercion source and relay target are different machines.

Shared admin precondition model (LAPS-aware):
  Evidence A: finding.evidence["laps_enabled"] is False → LAPS confirmed absent (0.70).
  Evidence B: finding.evidence["local_admin_name"] is the same across hosts (0.75).
  A + B: 0.80. Without evidence: heuristic 0.35 only when ≥2 Windows hosts exist.

SNMP community lateral:
  Network devices sharing the same default SNMP community (CORR-SNMP-PUBLIC-LATERAL)
  can read each other's routing/ARP tables, enabling config-disclosure lateral movement.
  Emitted as CREDENTIAL_REUSE edges between all matching device pairs (0.55 confidence).

Integration:
  GraphBuilder.assemble() calls derive_relay_links() and derive_credential_links()
  after P2 capability map injection. The builder adds CONNECTS_TO (relay) and
  CREDENTIAL_REUSE (credential) edges. Failures are caught by the builder and logged
  — they never sink the graph build.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any


# ── relay target rule IDs ─────────────────────────────────────────────────────
# An asset with any of these findings is a viable relay TARGET (signing off).
_RELAY_TARGET_RULES: frozenset[str] = frozenset({
    "CORR-NTLM-RELAY-PATH",
    "POSTURE-SMB-SIGNING-OFF",
})

# Confirmed coercion surface (MSRPC endpoint manager exposed).
# The COMPOUND-NTLM-RELAY-AND-COERCE synthetic finding covers the single-asset case.
_COERCE_CONFIRMED_RULES: frozenset[str] = frozenset({
    "POSTURE-MSRPC-EPMAP-EXPOSED",
})

# Heuristic coercion sources — any Windows host can potentially be coerced via
# PrinterBug / PetitPotam if the Spooler or EFS is running. Lower confidence.
_COERCE_HEURISTIC_RULES: frozenset[str] = frozenset({
    "CORR-NTLM-RELAY-PATH",
    "CORR-LEGACY-WINDOWS-SURFACE",
    "POSTURE-SMB-SIGNING-OFF",
})

# Windows-bearing host indicators for shared-admin heuristic.
_WINDOWS_RULES: frozenset[str] = frozenset({
    "CORR-NTLM-RELAY-PATH",
    "CORR-LEGACY-WINDOWS-SURFACE",
    "POSTURE-SMB-SIGNING-OFF",
    "POSTURE-MSRPC-EPMAP-EXPOSED",
})

# Network gear with default SNMP community — config-disclosure lateral.
_SNMP_LATERAL_RULE = "CORR-SNMP-PUBLIC-LATERAL"

# Confidence floors
_P_RELAY_CONFIRMED = 0.65   # confirmed MSRPC coercion → relay target
_P_RELAY_DC = 0.80          # confirmed MSRPC coercion → DC relay target (domain compromise)
_P_RELAY_HEURISTIC = 0.50   # heuristic Windows coercion → relay target
_P_CRED_LAPS_ABSENT = 0.70  # LAPS confirmed absent + same engagement Windows hosts
_P_CRED_NAME_MATCH = 0.75   # same local admin name across hosts (LAPS status unknown)
_P_CRED_NAME_AND_LAPS = 0.80  # same name + LAPS confirmed absent
_P_CRED_HEURISTIC = 0.35    # Windows hosts present, no LAPS data
_P_SNMP_LATERAL = 0.55      # default SNMP community shared between network devices

# Attacker technique IDs
_T_NTLM_RELAY = "T1557.001"
_T_PASS_HASH = "T1550.002"
_T_SNMP = "T1602.001"


# ── dataclasses ────────────────────────────────────────────────────────────────

@dataclass
class RelayLink:
    """Directed cross-asset NTLM relay edge: coercion_source → relay_target.

    The attacker, positioned near or on the coercion source, can force that host
    to authenticate and relay its credential to compromise the relay target.
    """
    source_asset_id: str   # coercion source (forced authenticator)
    target_asset_id: str   # relay target (SMB signing not required)
    technique: str = _T_NTLM_RELAY
    basis: str = "relay_inferred"
    confidence: float = _P_RELAY_CONFIRMED
    label: str = ""
    is_dc_target: bool = False  # True when relay target is a domain controller


@dataclass
class CredentialLink:
    """Undirected CREDENTIAL_REUSE edge: two assets share a local admin credential.

    Emitted when LAPS is absent (or heuristically suspected absent) and two Windows
    hosts are in the same engagement. Bidirectional — the builder adds edges in both
    directions.
    """
    asset_id_a: str
    asset_id_b: str
    technique: str = _T_PASS_HASH
    basis: str = "shared_admin"
    confidence: float = _P_CRED_HEURISTIC
    label: str = ""
    laps_confirmed_absent: bool = False


# ── helpers ────────────────────────────────────────────────────────────────────

def _get_rule_id(f: Any) -> str:
    rid = getattr(f, "rule_id", None)
    if rid is None:
        return ""
    return str(getattr(rid, "value", rid) or "")


def _asset_id(f: Any) -> str:
    return str(getattr(f, "asset_id", None) or "")


def _evidence(f: Any) -> dict:
    ev = getattr(f, "evidence", None)
    if isinstance(ev, dict):
        return ev
    return {}


def _is_live(f: Any) -> bool:
    status = str(getattr(getattr(f, "status", None), "value", getattr(f, "status", None)) or "").lower()
    return status in ("open", "confirmed", "")


def _relay_link_id(source: str, target: str) -> str:
    key = f"relay:{source}:{target}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


# ── relay edge derivation ─────────────────────────────────────────────────────

def derive_relay_links(
    findings: list[Any],
    assets: list[Any] = (),  # noqa: ARG001 — reserved for future asset signals
) -> list[RelayLink]:
    """Derive directed NTLM relay edges from cross-asset precondition findings.

    Returns a list of RelayLink objects describing CONNECTS_TO edges the builder
    should add to the attack graph.

    Algorithm:
      1. Partition findings by asset_id into relay targets and coercion sources.
      2. Build cross-product (coercion_source, relay_target) pairs, source ≠ target.
      3. Assign confidence based on coercion evidence strength and DC flag.
      4. Deduplicate by (source, target) — highest confidence wins.
    """
    relay_targets: dict[str, dict] = {}   # asset_id → {is_dc, finding}
    coerce_confirmed: set[str] = set()    # asset_ids with POSTURE-MSRPC-EPMAP-EXPOSED
    coerce_heuristic: set[str] = set()   # asset_ids with Windows bearing rules

    for f in findings:
        if not _is_live(f):
            continue
        rule_id = _get_rule_id(f)
        aid = _asset_id(f)
        if not aid:
            continue

        ev = _evidence(f)

        if rule_id in _RELAY_TARGET_RULES:
            existing = relay_targets.get(aid, {})
            # is_dc from evidence: the attack_paths.py stores domain_controller=True/False
            is_dc = bool(ev.get("domain_controller")) or existing.get("is_dc", False)
            relay_targets[aid] = {"is_dc": is_dc, "rule_id": rule_id}

        if rule_id in _COERCE_CONFIRMED_RULES:
            coerce_confirmed.add(aid)

        if rule_id in _COERCE_HEURISTIC_RULES:
            coerce_heuristic.add(aid)

    if not relay_targets or not (coerce_confirmed | coerce_heuristic):
        return []

    # Build (source, target) pairs. Deduplicate keeping highest confidence.
    best: dict[tuple[str, str], RelayLink] = {}

    all_coerce = coerce_confirmed | coerce_heuristic

    for src in all_coerce:
        is_confirmed = src in coerce_confirmed

        for tgt, tgt_meta in relay_targets.items():
            if src == tgt:
                # Same asset: compound rule handles this (P2 capability_map)
                continue

            is_dc = tgt_meta["is_dc"]
            if is_dc:
                p = _P_RELAY_DC
            elif is_confirmed:
                p = _P_RELAY_CONFIRMED
            else:
                p = _P_RELAY_HEURISTIC

            basis = "relay_confirmed" if is_confirmed else "relay_heuristic"
            dc_suffix = " → DC (domain compromise)" if is_dc else ""
            label = f"NTLM relay{dc_suffix}: {src} → {tgt}"

            pair = (src, tgt)
            existing = best.get(pair)
            if existing is None or p > existing.confidence:
                best[pair] = RelayLink(
                    source_asset_id=src,
                    target_asset_id=tgt,
                    technique=_T_NTLM_RELAY,
                    basis=basis,
                    confidence=p,
                    label=label,
                    is_dc_target=is_dc,
                )

    return list(best.values())


# ── credential link derivation ────────────────────────────────────────────────

def derive_credential_links(
    findings: list[Any],
    assets: list[Any] = (),  # noqa: ARG001 — reserved for future asset signals
) -> list[CredentialLink]:
    """Derive LAPS-aware shared local admin CREDENTIAL_REUSE edges.

    Returns bidirectional CredentialLink objects. The builder adds edges in both
    directions so the analyzer can walk either way.

    Confidence tiers (highest wins for any pair):
      0.80 — same local_admin_name in evidence AND LAPS confirmed absent
      0.75 — same local_admin_name (LAPS status unknown)
      0.70 — LAPS confirmed absent on both hosts (no name match but shared engagement)
      0.35 — heuristic: ≥2 Windows hosts in engagement, no LAPS data

    Also derives SNMP community lateral edges (0.55) for network device pairs
    sharing default SNMP community (CORR-SNMP-PUBLIC-LATERAL).
    """
    # Gather Windows-bearing assets with their evidence metadata.
    # Per-asset: {"laps_absent": bool|None, "admin_names": set[str], "snmp": bool}
    windows_info: dict[str, dict] = {}  # asset_id → meta
    snmp_assets: set[str] = set()

    for f in findings:
        if not _is_live(f):
            continue
        rule_id = _get_rule_id(f)
        aid = _asset_id(f)
        if not aid:
            continue

        ev = _evidence(f)

        if rule_id in _WINDOWS_RULES:
            info = windows_info.setdefault(aid, {"laps_absent": None, "admin_names": set()})

            # LAPS check: engine_bridge does not currently store laps_enabled in evidence,
            # but future enrichment (windows_collector facts) may add it.
            laps_ev = ev.get("laps_enabled")
            if laps_ev is False:
                info["laps_absent"] = True
            elif laps_ev is True:
                # LAPS present → no shared admin risk from this asset
                info["laps_absent"] = False

            # Local admin name from evidence (windows_collector / AD assessment).
            name = ev.get("local_admin_name") or ev.get("admin_name")
            if isinstance(name, str) and name:
                info["admin_names"].add(name.lower().strip())
            elif isinstance(name, list):
                for n in name:
                    if isinstance(n, str) and n:
                        info["admin_names"].add(n.lower().strip())

        if rule_id == _SNMP_LATERAL_RULE:
            snmp_assets.add(aid)

    # ── shared admin links ─────────────────────────────────────────────────────
    asset_ids = list(windows_info)
    best: dict[frozenset, CredentialLink] = {}

    for i, aid_a in enumerate(asset_ids):
        for aid_b in asset_ids[i + 1:]:
            meta_a = windows_info[aid_a]
            meta_b = windows_info[aid_b]

            laps_a = meta_a["laps_absent"]
            laps_b = meta_b["laps_absent"]
            # If LAPS is confirmed PRESENT on either host, no shared-admin risk.
            if laps_a is False or laps_b is False:
                continue

            laps_both_absent = laps_a is True and laps_b is True
            shared_names = meta_a["admin_names"] & meta_b["admin_names"]

            if shared_names and laps_both_absent:
                p = _P_CRED_NAME_AND_LAPS
                basis = "shared_admin_laps_absent"
                label = f"shared admin '{next(iter(shared_names))}' (LAPS absent)"
            elif shared_names:
                p = _P_CRED_NAME_MATCH
                basis = "shared_admin_name"
                label = f"shared admin '{next(iter(shared_names))}'"
            elif laps_both_absent:
                p = _P_CRED_LAPS_ABSENT
                basis = "laps_absent"
                label = "Windows hosts, LAPS confirmed absent"
            else:
                # Heuristic: both Windows, no LAPS data.
                p = _P_CRED_HEURISTIC
                basis = "windows_heuristic"
                label = "Windows hosts (heuristic, no LAPS data)"

            pair = frozenset({aid_a, aid_b})
            existing = best.get(pair)
            if existing is None or p > existing.confidence:
                best[pair] = CredentialLink(
                    asset_id_a=aid_a,
                    asset_id_b=aid_b,
                    technique=_T_PASS_HASH,
                    basis=basis,
                    confidence=p,
                    label=label,
                    laps_confirmed_absent=laps_both_absent,
                )

    cred_links = list(best.values())

    # ── SNMP lateral links ─────────────────────────────────────────────────────
    snmp_list = sorted(snmp_assets)
    for i, aid_a in enumerate(snmp_list):
        for aid_b in snmp_list[i + 1:]:
            cred_links.append(CredentialLink(
                asset_id_a=aid_a,
                asset_id_b=aid_b,
                technique=_T_SNMP,
                basis="snmp_default_community",
                confidence=_P_SNMP_LATERAL,
                label="SNMP default community (config-disclosure lateral)",
                laps_confirmed_absent=False,
            ))

    return cred_links
