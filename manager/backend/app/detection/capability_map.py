"""
capability_map.py — what an attacker can DO with a finding (P2).

Attack-path generation used to admit a finding as an attacker step only when its
``exploitable`` flag was set, and that flag is set only by the Active-Directory
modules. So on an ordinary network-VA engagement — SMB signing off, RDP without
NLA, an unauthenticated database, default SNMP — every weakness that actually
chains carried ``exploitable=false`` and produced no step at all (FM-03/12/19 in
manager/docs/ATTACK_PATH_PLAN.md). XM Cyber's own telemetry puts ~80% of real
exposures in exactly this misconfiguration/identity bucket and <1% in CVEs.

This module closes that gap WITHOUT inventing exploitation. It answers one
question per finding: if an attacker reaches the host carrying this weakness,
what does the weakness let them do?

  foothold            gain control of THIS host from outside (unauth shell, unauth
                      datastore, no-auth remote desktop, OOB management bypass)
  lateral             use this host/weakness to move to ANOTHER host (relay, reused
                      session, mgmt-plane pivot)
  priv_esc            escalate once already on the host
  credential_access   harvest credentials usable elsewhere (sniffing, default SNMP)
  recon               information only — enumerate, fingerprint, disclose

Only foothold / lateral / priv_esc GRANT CONTROL of the host the finding sits on
(``CONTROL_CAPABILITIES``). credential_access and recon are classified and
recorded but never, on their own, make a host a compromised pivot — reaching a
host you can only read from is not owning it, and the monotonic-control model
(MulVAL / Ou et al.) forbids a path continuing from a host the attacker does not
control. Credential REUSE as a movement edge is P3, separate from this map.

The classification is by ``rule_id`` first (exact, auditable), then by the rule's
``category``, then by its ATT&CK technique as a last resort, so a rule added to
the engine later still lands somewhere honest rather than silently vanishing from
the graph. Pure and deterministic: no DB, no I/O.
"""
from __future__ import annotations

from typing import Any, Optional

FOOTHOLD = "foothold"
LATERAL = "lateral"
PRIV_ESC = "priv_esc"
CREDENTIAL_ACCESS = "credential_access"
RECON = "recon"

# The capabilities that make a host a COMPROMISED pivot: a path may continue from a
# host only when the attacker gained control of it. The other two are enabling
# steps and information, never ownership, so they never create a control edge here.
CONTROL_CAPABILITIES: frozenset[str] = frozenset({FOOTHOLD, LATERAL, PRIV_ESC})

# ── rule_id → capability (exact, curated) ─────────────────────────────────────
# Each entry is a deliberate statement about what the weakness yields, not a guess.
# A weakness that only discloses information, or only weakens transport crypto
# without granting access, is RECON (or absent) — never a foothold.
_RULE_CAPABILITY: dict[str, str] = {
    # ── foothold: direct control of the host it sits on ──
    "POSTURE-DB-UNAUTHENTICATED-ACCESS": FOOTHOLD,   # read/write the datastore directly
    "POSTURE-VNC-NO-AUTH": FOOTHOLD,                 # interactive desktop, no credential
    "POSTURE-ADB-UNAUTHENTICATED": FOOTHOLD,         # unauthenticated Android shell
    "POSTURE-IPMI-CIPHER-ZERO": FOOTHOLD,            # OOB auth bypass = full host control
    "POSTURE-MQTT-UNAUTHENTICATED": FOOTHOLD,        # broker access without auth
    "POSTURE-AI-ENDPOINT-UNAUTHENTICATED": FOOTHOLD,  # unauth inference/control endpoint
    "POSTURE-FTP-ANONYMOUS-WRITE": FOOTHOLD,         # anonymous upload → planted payload
    "POSTURE-DEFAULT-CRED-CANDIDATE": FOOTHOLD,      # vendor default credentials
    "POSTURE-SMB-V1-ENABLED": FOOTHOLD,              # wormable RCE surface (EternalBlue class)
    "POSTURE-RDP-NO-NLA": FOOTHOLD,                  # pre-auth RDP reach (BlueKeep class)
    "POSTURE-OS-END-OF-LIFE": FOOTHOLD,              # unsupported, unpatchable host
    "POSTURE-CWMP-EXPOSED": FOOTHOLD,                # TR-069 remote management plane
    # ── lateral: move to another host / pivot ──
    "POSTURE-RDP-EXPOSED": LATERAL,                  # reachable RDP for credential attack / pivot
    "POSTURE-RTSP-EXPOSED": LATERAL,                 # streaming/control pivot surface
    # ── credential_access: harvest credentials usable elsewhere ──
    # SMB signing off is a relay PRECONDITION, not a foothold on its own (FM-09):
    # it owns a host only when P3's relay edge finds a coercion source, so it is an
    # enabling step here, never a control capability by itself.
    "POSTURE-SMB-SIGNING-OFF": CREDENTIAL_ACCESS,
    "POSTURE-SNMP-DEFAULT-COMMUNITY": CREDENTIAL_ACCESS,  # config + community strings leak
    "POSTURE-SNMPV3-NOAUTH-USER": CREDENTIAL_ACCESS,      # read SNMP without auth
    "POSTURE-FTP-ANONYMOUS-LOGIN": CREDENTIAL_ACCESS,     # anonymous read of stored data/creds
    "POSTURE-RSYNC-ANONYMOUS-MODULE": CREDENTIAL_ACCESS,  # anonymous read of module contents
    "POSTURE-NFS-WORLD-READABLE-EXPORT": CREDENTIAL_ACCESS,  # read exported data/keys
    # ── recon: information only, no control, no credentials by itself ──
    "POSTURE-LDAP-ANONYMOUS-BIND": RECON,
    "POSTURE-LDAP-ANONYMOUS-SEARCH": RECON,
    "POSTURE-SMB-NULL-SESSION": RECON,
    "POSTURE-MSRPC-EPMAP-EXPOSED": RECON,
    "POSTURE-DNS-ZONE-TRANSFER": RECON,
    "POSTURE-DNS-VERSION-DISCLOSURE": RECON,
    "POSTURE-SMTP-USER-ENUMERATION": RECON,
    "POSTURE-NETBIOS-EXPOSED": RECON,
    "POSTURE-MDNS-EXPOSED": RECON,
    "POSTURE-SIP-EXPOSED": RECON,
    "POSTURE-UNIDENTIFIED-SERVICE": RECON,
    # ── composite CORR-* findings (already a chained weakness) ──
    "CORR-NTLM-RELAY-PATH": LATERAL,
    "CORR-LEGACY-WINDOWS-SURFACE": FOOTHOLD,
    "CORR-DB-UNAUTH-EXPOSED": FOOTHOLD,
    "CORR-MGMT-PLANE-EXPOSED": FOOTHOLD,
    "CORR-SNMP-PUBLIC-LATERAL": LATERAL,
    "CORR-CLEARTEXT-CLUSTER": CREDENTIAL_ACCESS,
    "CORR-AD-EXPOSURE": CREDENTIAL_ACCESS,
}

# ── category → capability (fallback for rules not named above) ────────────────
_CATEGORY_CAPABILITY: dict[str, str] = {
    "default_credentials": FOOTHOLD,
    "information_disclosure": RECON,
    "exposure": RECON,
}

# ATT&CK tactic prefixes, used only when neither rule_id nor category classified the
# finding. Coarse, and deliberately conservative: an unknown technique maps to recon,
# never to a foothold.
_MITRE_CAPABILITY: dict[str, str] = {
    "T1190": FOOTHOLD,     # exploit public-facing application
    "T1133": FOOTHOLD,     # external remote services
    "T1210": FOOTHOLD,     # exploitation of remote services
    "T1021": LATERAL,      # remote services (lateral)
    "T1557": LATERAL,      # adversary-in-the-middle / relay
    "T1078": CREDENTIAL_ACCESS,  # valid accounts
    "T1110": CREDENTIAL_ACCESS,  # brute force
    "T1040": CREDENTIAL_ACCESS,  # network sniffing
    "T1602": CREDENTIAL_ACCESS,  # data from configuration repository
    "T1087": RECON,        # account discovery
    "T1046": RECON,        # network service discovery
    "T1135": RECON,        # network share discovery
    "T1590": RECON,        # gather victim network information
    "T1595": RECON,        # active scanning
    "T1498": None,         # network DoS — not a path step at all
    "T1505": PRIV_ESC,     # server software component (web shell / module)
    "T1574": PRIV_ESC,     # hijack execution flow
    "T1543": PRIV_ESC,     # create or modify system process
    "T1562": PRIV_ESC,     # impair defenses
}


def _mitre_base(technique: Any) -> str:
    """"T1557.001" -> "T1557" (sub-technique dot stripped)."""
    return str(technique or "").split(".", 1)[0].strip().upper()


def capability_for(rule_id: Any, category: Any = None,
                   mitre: Any = None) -> Optional[str]:
    """The attacker capability a finding grants, or None when it is not an attack
    step at all (e.g. a DoS amplifier, or a weakness we cannot place).

    Order: exact rule_id, then category, then ATT&CK technique. Kept narrow so a
    future rule cannot be silently promoted to a foothold by a loose heuristic.
    """
    rid = str(rule_id or "").strip().upper()
    if rid in _RULE_CAPABILITY:
        return _RULE_CAPABILITY[rid]
    cat = str(category or "").strip().lower()
    if cat in _CATEGORY_CAPABILITY:
        return _CATEGORY_CAPABILITY[cat]
    techniques = [mitre] if isinstance(mitre, str) else list(mitre or [])
    for t in techniques:
        base = _mitre_base(t)
        if base in _MITRE_CAPABILITY:
            return _MITRE_CAPABILITY[base]
    return None


def grants_control(capability: Any) -> bool:
    """Does this capability make the host a compromised pivot a path may continue
    from? Only foothold / lateral / priv_esc do."""
    return capability in CONTROL_CAPABILITIES


# ── step likelihood for a capability finding ──────────────────────────────────
# Base success per (capability, state). COARSE and ordinal: these ORDER steps
# (a confirmed foothold ranks above a suspected one, a direct foothold above a
# lateral precondition), they are not calibrated probabilities of compromise.
# A foothold is the surest step; lateral/priv_esc rest on a further precondition,
# so they sit a little lower.
_CAPABILITY_BASE: dict[str, float] = {
    FOOTHOLD: 0.6,
    LATERAL: 0.45,
    PRIV_ESC: 0.45,
}

# State of the finding (posture state, or the verification verdict). A suspected or
# potential weakness is a weaker step than a confirmed one; a contradicted one is
# treated as the floor, never dropped silently.
_STATE_FACTOR: dict[str, float] = {
    "confirmed": 1.0,
    "corroborated": 0.95,
    "suspected": 0.7,
    "potential": 0.55,
    "inferred": 0.7,
    "contradicted": 0.3,
}

# A small, additive sharpening from real-world exploitation evidence, mirroring
# exploitability._TIER_BOOST but on the 0–1 likelihood scale (not the 0–100 risk
# score). KEV-linked evidence raises the step most; it never lowers it.
_EXPLOIT_TIER_BUMP: dict[str, float] = {
    "actively_exploited": 0.25,
    "likely": 0.15,
    "elevated": 0.08,
    "unknown": 0.0,
}

_P_FLOOR = 0.1


def _f(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def step_likelihood_for_capability(data: dict[str, Any]) -> float:
    """Success likelihood (0,1] of a capability step, from a finding node's data.

    Inputs read (all optional, all already on the Finding graph node):
      capability, state / verification_state, confidence, epss, exploitability, kev.

    The estimate is max(capability-and-state base, measured EPSS) sharpened by a
    KEV/EPSS tier bump and scaled by the finding's confidence — the same shape as
    the CVE step model, so a posture step and a CVE step rank on one scale.
    """
    cap = data.get("capability")
    if cap not in CONTROL_CAPABILITIES:
        return 0.0
    base = _CAPABILITY_BASE.get(cap, 0.45)
    state = str(data.get("state") or data.get("verification_state") or "").lower()
    base *= _STATE_FACTOR.get(state, 0.7)

    # EPSS is a measured 30-day exploitation probability; take it as a floor on the
    # estimate when it is higher than the coarse capability base.
    epss = _f(data.get("epss"))
    p = max(base, epss)

    tier = str(data.get("exploitability") or "unknown").lower()
    bump = _EXPLOIT_TIER_BUMP.get(tier, 0.0)
    if not bump and data.get("kev"):
        bump = _EXPLOIT_TIER_BUMP["actively_exploited"]
    p = min(1.0, p + bump)

    conf = data.get("confidence")
    if conf is not None:
        c = _f(conf)
        if 0 < c <= 100:
            p *= c / 100.0
    return max(_P_FLOOR, min(1.0, p))
