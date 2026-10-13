"""
credentials.py — credential-reuse and NTLM-relay movement edges from facts (P3).

An attacker crosses host boundaries not only by exploiting services but by reusing
credentials and by relaying coerced authentication. These are the edges that make a
path cross a subnet like a real operator would. We derive them ONLY from evidence
the manager already holds, and we label every one with the precondition it rests
on — never asserting a relay or a shared password we cannot see.

What this builds, and the preconditions it checks (FM-08/09):

  * NTLM relay edge  source → target
      target     has SMB signing NOT required (POSTURE-SMB-SIGNING-OFF): the one
                 condition that makes a relayed authentication land.
      source     a DISTINCT host that itself exposes SMB — the vantage from which
                 an attacker coerces/forwards authentication. Reflection to the
                 same host is blocked (a host cannot relay to itself).
      reach      same subnet only. Relay+coercion is a LAN technique; emitting it
                 between every SMB host and every signing-off host across an
                 engagement is the over-connection FM-09 warns against.
      basis      `assumed` — signing-off is observed, but we cannot see the
                 coercion primitive (PetitPotam/PrinterBug), nor whether LDAP
                 channel binding / EPA would block the relay, so the edge is a
                 possibility to verify, never a fact. Relaying to a domain
                 controller is the canonical high-value case and scores a little
                 higher, still `assumed`.

  * Shared default-credential cluster  (INFORMATION, not a movement edge)
      Hosts that each carry the SAME default credential — the same default SNMP
      community, or the same vendor/product default — are reported together so an
      operator fixes them as one, but they create NO attack-graph edge. A read-only
      SNMP community grants no control, a vendor web default is already each host's
      own foothold finding, and the "credential" is public, so there is nothing an
      attacker captures on one host to reuse on another (that would be the FM-08
      shared-password fallacy, and it also exploded the graph with O(k²) edges on a
      estate of identical devices). Shown in the report, absent from the graph.

NOT built here, and why (kept honest rather than faked):
  * Shared LOCAL-ADMIN password reuse (BloodHound's AdminTo): needs a per-host
    local-admin inventory and a LAPS signal to avoid FM-08 (same admin NAME says
    nothing when LAPS randomises each password). The probe collects neither, so no
    such edge is emitted.
  * Reused SSH host/user keys: the probe records the offered host-key ALGORITHMS,
    not the key material, so identical-key reuse cannot be evidenced yet.

Pure and deterministic: no DB, no I/O, stable ordering.
"""
from __future__ import annotations

import ipaddress
from typing import Any, Iterable, Optional

# Relay edge labels + coarse ordering weights (ordinal, not measured rates).
RELAY_TECHNIQUE = "T1557.001"
BASIS_ASSUMED = "assumed"
BASIS_POSSIBLE = "possible"
CONF_RELAY = 0.4          # signing-off observed; coercion + protocol acceptance assumed
CONF_RELAY_TO_DC = 0.5    # relaying to a DC is the canonical case — slightly higher, still assumed
CONF_SHARED_DEFAULT = 0.6  # a working default on one host very likely works on its twins

_SMB_PORTS = frozenset({445, 139})
_V4_SUBNET = 24
_V6_SUBNET = 64


def _attr(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _evidence(finding: Any) -> dict:
    ev = _attr(finding, "evidence")
    return ev if isinstance(ev, dict) else {}


def _rule_id(finding: Any) -> str:
    return str(_evidence(finding).get("rule_id") or _attr(finding, "rule_id") or "").upper()


def _subnet_key(ip_text: Any) -> Optional[str]:
    """The /24 (v4) or /64 (v6) bucket of a host, used only to keep relay edges on
    one subnet. None when the address does not parse."""
    if not ip_text:
        return None
    try:
        ip = ipaddress.ip_address(str(ip_text).split("%", 1)[0].strip())
    except ValueError:
        return None
    plen = _V4_SUBNET if ip.version == 4 else _V6_SUBNET
    return str(ipaddress.ip_network(f"{ip}/{plen}", strict=False))


def _is_domain_controller(asset: Any, findings_by_asset: dict[str, list]) -> bool:
    if str(_attr(asset, "role_detail") or "").lower() == "domain_controller":
        return True
    for f in findings_by_asset.get(str(_attr(asset, "id")), ()):
        if _evidence(f).get("domain_controller") is True:
            return True
    return False


def derive_credential_edges(assets: Iterable[Any], findings: Iterable[Any],
                            services: Iterable[Any] = ()) -> dict[str, Any]:
    """Return {"shared_default_credentials": [...], "relay_edges": [...]} from the
    engagement's assets, findings and services.

    `shared_default_credentials` is INFORMATION for the report, not graph edges:
        {"id", "label", "reused_on": [asset_id...], "basis"}
    `relay_edges` items feed GraphBuilder.add_relay_edges:
        {"src", "dst", "basis", "confidence", "technique", "preconditions": {...}}
    """
    assets = list(assets)
    findings = list(findings)
    services = list(services)
    by_asset: dict[str, list] = {}
    for f in findings:
        aid = _attr(f, "asset_id")
        if aid is not None:
            by_asset.setdefault(str(aid), []).append(f)

    asset_by_id = {str(_attr(a, "id")): a for a in assets}
    subnet_of = {aid: _subnet_key(_attr(a, "ip_address")) for aid, a in asset_by_id.items()}

    # ── which hosts expose SMB, and which have signing OFF ──
    smb_hosts: set[str] = set()
    signing_off: set[str] = set()
    for s in services:
        if _attr(s, "port") in _SMB_PORTS:
            aid = str(_attr(s, "asset_id"))
            if aid in asset_by_id:
                smb_hosts.add(aid)
    for f in findings:
        rid = _rule_id(f)
        aid = str(_attr(f, "asset_id"))
        if aid not in asset_by_id:
            continue
        if "SMB" in rid:
            smb_hosts.add(aid)
        if rid in ("POSTURE-SMB-SIGNING-OFF", "CORR-NTLM-RELAY-PATH"):
            signing_off.add(aid)

    relay_edges: list[dict[str, Any]] = []
    for tgt in sorted(signing_off):
        tgt_subnet = subnet_of.get(tgt)
        is_dc = _is_domain_controller(asset_by_id[tgt], by_asset)
        for src in sorted(smb_hosts):
            # Reflection to the same host is not a relay; both must sit on one subnet.
            if src == tgt or tgt_subnet is None or subnet_of.get(src) != tgt_subnet:
                continue
            relay_edges.append({
                "src": src, "dst": tgt,
                "basis": BASIS_ASSUMED,
                "confidence": CONF_RELAY_TO_DC if is_dc else CONF_RELAY,
                "technique": RELAY_TECHNIQUE,
                "preconditions": {
                    "target_signing_off": True,
                    "coercion_source": True,
                    "same_subnet": True,
                    "target_is_dc": is_dc,
                    "unverified": ["coercion_primitive", "ldap_channel_binding", "epa"],
                },
            })

    # ── shared default-credential clusters ──
    # Key: what credential is shared. Same key on ≥2 hosts = a reuse cluster.
    clusters: dict[tuple[str, str], list[str]] = {}
    labels: dict[tuple[str, str], str] = {}
    for f in findings:
        rid = _rule_id(f)
        aid = _attr(f, "asset_id")
        if aid is None:
            continue
        aid = str(aid)
        ev = _evidence(f)
        key: Optional[tuple[str, str]] = None
        label = ""
        if rid == "POSTURE-SNMP-DEFAULT-COMMUNITY":
            community = str(ev.get("community") or "").lower()
            if community:
                key = ("snmp_community", community)
                label = f"default SNMP community '{community}'"
        elif rid in ("POSTURE-DEFAULT-CRED-CANDIDATE", "POSTURE-SNMPV3-NOAUTH-USER"):
            vendor = str(ev.get("vendor") or ev.get("product") or "").lower()
            if vendor:
                key = ("default_cred", vendor)
                label = f"{vendor} default credentials"
        if key is not None:
            clusters.setdefault(key, [])
            if aid not in clusters[key]:
                clusters[key].append(aid)
            labels[key] = label

    shared: list[dict[str, Any]] = []
    for key in sorted(clusters):
        hosts = sorted(clusters[key])
        if len(hosts) < 2:
            continue                       # a credential one host uses is not "shared"
        shared.append({
            "id": f"{key[0]}:{key[1]}",
            "label": labels[key],
            "reused_on": hosts,
            "basis": BASIS_POSSIBLE,
        })

    return {"shared_default_credentials": shared, "relay_edges": relay_edges}
