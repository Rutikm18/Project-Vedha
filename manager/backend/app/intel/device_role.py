"""device_role.py — one dominant device role, with a confidence, from corroborated evidence.

The probe's classifier names a role per host from ports and services. That is a useful
signal, but a port is not an identity: a general-purpose Linux server that merely answers on
BGP, SIP and print ports is not a router, a phone system and a printer. This module keeps the
classifier's claim as one input, checks it against the strongest independent evidence we hold
(the OS fingerprint), and returns ONE role plus how far it can be trusted.

Only a high-confidence role is allowed to *drive* anything — the ``host_type`` tag, the
attack-path severity amplifier, the "this host is a gateway" assumption in the reachability
model. A low-confidence role is still stored and shown, labelled as a candidate.

Pure logic — no DB, no I/O.

Rules, in order:
  1. A dedicated network/printer/IoT claim is CORROBORATED when the OS fingerprint is itself a
     dedicated-device OS (IOS, Junos, RouterOS, FortiOS, PAN-OS, EOS, JetDirect ...): confidence
     rises to at least 0.85.
  2. The same claim is CONTRADICTED when the OS fingerprint is a general-purpose server or
     desktop OS (Ubuntu, Debian, Windows Server ...): the role falls back to ``server`` at 0.65,
     with the original claim kept in ``downgraded_from``. A general-purpose OS can host
     appliance software, but then the host is a server running it.
  3. Otherwise the classifier's own confidence stands; an unrated claim counts as 0.5.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

HIGH_CONFIDENCE = 0.7
UNRATED = 0.5

_DEDICATED_CLAIMS = frozenset({"network_device", "network", "printer", "iot"})

_DEDICATED_OS = re.compile(
    r"cisco|\bios[- ]?xe?\b|junos|juniper|routeros|mikrotik|fortios|fortigate|pan-?os|palo alto|"
    r"arista|\beos\b|netscreen|screenos|sonicos|big-?ip|f5 |aruba|procurve|jetdirect|"
    r"ricoh|kyocera|lexmark|brother|xerox|zebra|vxworks|embedded|openwrt|dd-wrt|ubiquiti|edgeos",
    re.IGNORECASE)
_GENERAL_PURPOSE_OS = re.compile(
    r"ubuntu|debian|centos|red ?hat|rhel|fedora|suse|rocky|alma|amazon linux|oracle linux|"
    r"windows (server|10|11|7|8)|microsoft windows|freebsd|openbsd|netbsd|macos|mac os|"
    r"\blinux\b",
    re.IGNORECASE)


@dataclass(frozen=True)
class RoleVerdict:
    role: str | None
    confidence: float
    basis: str
    high_confidence: bool
    downgraded_from: str | None = None

    def describe(self) -> str:
        if self.downgraded_from:
            return (f"{self.role} ({self.basis}; classifier said {self.downgraded_from} but the "
                    f"OS fingerprint is a general-purpose OS)")
        return f"{self.role} ({self.basis})"


def resolve_role(device_role: str | None, role_confidence: float | None,
                 os_name: str | None) -> RoleVerdict:
    if not device_role:
        return RoleVerdict(None, 0.0, "no_classification", False)
    claimed = float(role_confidence) if role_confidence is not None else UNRATED
    os_text = os_name or ""
    if device_role in _DEDICATED_CLAIMS and os_text:
        if _DEDICATED_OS.search(os_text):
            conf = max(claimed, 0.85)
            return RoleVerdict(device_role, conf, "classifier_corroborated_by_os", True)
        if _GENERAL_PURPOSE_OS.search(os_text):
            return RoleVerdict("server", 0.65, "os_fingerprint_overrides_port_inference",
                               False, downgraded_from=device_role)
    basis = "classifier" if role_confidence is not None else "classifier_unrated"
    return RoleVerdict(device_role, claimed, basis, claimed >= HIGH_CONFIDENCE)


def drives_amplifier(device_role: str | None, role_confidence: float | None,
                     os_name: str | None = None) -> bool:
    """May this role change a finding's severity or the reachability model?

    A role from before confidences were recorded (``role_confidence is None``) keeps its
    previous behaviour, so existing engagements do not change silently; a role with a
    recorded confidence must clear the high-confidence bar and survive the OS check."""
    if not device_role:
        return False
    if role_confidence is None and not os_name:
        return True
    verdict = resolve_role(device_role, role_confidence, os_name)
    return verdict.role == device_role and (verdict.high_confidence or role_confidence is None)
