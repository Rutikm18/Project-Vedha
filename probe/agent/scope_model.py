"""scope_model.py — the typed-scope model (Phase 1 of the hardened agent).

Pure, dependency-free logic that implements the `Segment` contract
(docs/superpowers/specs/2026-09-10-vedha-agent-interface-contracts.md):
interface classification, the permanent denylist, Segment validation, the
job-scope re-check the agent enforces independently of the Manager, and
container/WSL2 refusal. No network, no root — unit-testable in full.

Design rules (from the threat model + review):
- Unsafe defaults are bugs: the denylist and refusals fail CLOSED.
- Local scope only ever NARROWS the Manager ceiling; it never widens it.
- IPv6 is out of scope for v1 and is therefore denied (documented, not silent).
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass

VALID_TYPES = {"IT", "IoT", "OT", "NEVER"}
VALID_PROFILES = {"it", "iot", None}


@dataclass
class Interface:
    name: str
    addresses: list[str]   # ["ip/prefix", ...] IPv4
    kind: str              # physical | virtual | tunnel | container | loopback


@dataclass
class Segment:
    cidr: str
    type: str                       # IT | IoT | OT | NEVER
    profile: str | None = None      # it | iot | None
    active: bool = True             # OT/NEVER default to inactive in v1
    rate_ceiling_pps: int | None = None
    site: str = ""
    authorized_by: str | None = None


# ── interface classification ─────────────────────────────────────────────────
_TUNNEL = ("tun", "tap", "utun", "ppp", "wg", "ipsec", "tailscale", "zt")
_CONTAINER = ("docker", "veth", "br-", "cni", "flannel", "cali", "kube", "podman")
_VIRTUAL = ("virbr", "vmnet", "vboxnet", "vethernet", "hyper-v", "vmware", "wsl", "vswitch")


def classify_interface(name: str) -> str:
    n = name.lower().strip()
    if n in ("lo", "lo0") or n.startswith("loopback"):
        return "loopback"
    if any(t in n for t in _TUNNEL):
        return "tunnel"
    # virtual before container so "vEthernet (WSL)" classifies as virtual
    if any(v in n for v in _VIRTUAL):
        return "virtual"
    if any(c in n for c in _CONTAINER):
        return "container"
    return "physical"


# ── permanent denylist ───────────────────────────────────────────────────────
def is_denied(target: str, manager_ip: str | None = None) -> bool:
    """True if `target` (an IP or CIDR) must NEVER be scanned. Fail-closed."""
    try:
        net = ipaddress.ip_network(target, strict=False)
    except ValueError:
        return True  # unparseable → deny
    if net.version == 6:
        return True  # IPv6 out of scope for v1
    if (net.is_loopback or net.is_link_local or net.is_multicast
            or net.is_reserved or net.is_unspecified):
        return True  # 127/8, 169.254/16 (incl. 169.254.169.254), 224/4, 240/4, 0.0.0.0
    if net.num_addresses == 1 and net.network_address == ipaddress.ip_address("255.255.255.255"):
        return True  # limited broadcast
    if manager_ip:
        try:
            if ipaddress.ip_address(manager_ip) in net:
                return True
        except ValueError:
            pass
    return False


# ── Segment validation ───────────────────────────────────────────────────────
def validate_segment(seg: Segment) -> list[str]:
    errs: list[str] = []
    if seg.type not in VALID_TYPES:
        errs.append(f"type {seg.type!r} invalid (want one of {sorted(VALID_TYPES)})")
    try:
        ipaddress.ip_network(seg.cidr, strict=False)
    except ValueError:
        errs.append(f"cidr {seg.cidr!r} is not a valid CIDR")
    if seg.profile not in VALID_PROFILES:
        errs.append(f"profile {seg.profile!r} invalid")
    if seg.type == "NEVER" and seg.active:
        errs.append("NEVER segment must be inactive")
    if seg.type == "OT" and seg.active:
        errs.append("OT segment cannot be active in v1 (OT scanning is a separate track)")
    if seg.active and not seg.site:
        errs.append("active segment requires a site key")
    return errs


def validate_scope(segments: list[Segment]) -> list[str]:
    errs: list[str] = []
    for i, seg in enumerate(segments):
        errs.extend(f"segment[{i}]: {e}" for e in validate_segment(seg))
    return errs


# ── job-scope re-check (the agent enforces its own ceiling) ──────────────────
def target_allowed(target: str, segments: list[Segment],
                   manager_ip: str | None = None) -> tuple[bool, str]:
    """Independent of the Manager: a target is allowed only if it is not on the
    denylist AND falls inside an ACTIVE IT/IoT segment. OT/NEVER never match."""
    if is_denied(target, manager_ip):
        return False, "target on permanent denylist"
    try:
        ip = ipaddress.ip_address(target)
    except ValueError:
        return False, "target is not a valid IP"
    for seg in segments:
        if not seg.active or seg.type in ("NEVER", "OT"):
            continue
        try:
            if ip in ipaddress.ip_network(seg.cidr, strict=False):
                return True, seg.type
        except ValueError:
            continue
    return False, "target not in any active IT/IoT segment"


# ── container / WSL2 detection + refusal ─────────────────────────────────────
def detect_container(dockerenv_exists: bool, cgroup_text: str, proc_version: str) -> str | None:
    if dockerenv_exists:
        return "docker"
    low = (cgroup_text or "").lower()
    if any(k in low for k in ("docker", "kubepods", "containerd", "lxc", "podman")):
        return "container"
    pv = (proc_version or "").lower()
    if "microsoft" in pv or "wsl" in pv:
        return "wsl2"
    return None


def refusal_reason(container: str | None) -> str | None:
    """Refuse LAN scanning from inside a container/WSL2 namespace — it would scan
    the virtual bridge, not the real LAN (silently-wrong results)."""
    if container:
        return (f"running inside a {container} namespace — LAN scanning is not "
                f"possible from here (it would target the virtual network, not the "
                f"real LAN); run the agent on the host network")
    return None


# ── IPv6 handling (explicit, not silent) ─────────────────────────────────────
def ipv6_scope_note(primary_ipv4: str | None) -> str | None:
    if primary_ipv4:
        return None
    return ("no IPv4 address detected; IPv6 scanning is out of scope in v1, so this "
            "host has no scan scope — this is expected, not a fault")


# ── linux `ip -j addr` parse (pure) ──────────────────────────────────────────
def parse_linux_ip_json(records: list[dict]) -> list[Interface]:
    out: list[Interface] = []
    for rec in records:
        name = rec.get("ifname", "")
        if not name:
            continue
        addrs = [
            f"{a.get('local')}/{a.get('prefixlen')}"
            for a in rec.get("addr_info", [])
            if a.get("family") == "inet" and a.get("local")
        ]
        out.append(Interface(name=name, addresses=addrs, kind=classify_interface(name)))
    return out
