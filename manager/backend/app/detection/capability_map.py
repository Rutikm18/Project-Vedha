"""
capability_map.py — what an attacker can DO with a finding (P2).

Attack-path generation used to admit a finding as an attacker step only when its
``exploitable`` flag was set, and that flag is set only by the Active-Directory
modules. So on an ordinary network-VA engagement — SMB signing off, RDP without
NLA, an unauthenticated database, default SNMP — every weakness that actually
chains carried ``exploitable=false`` and produced no step at all (FM-03/12/19 in
manager/docs/ATTACK_PATH_PLAN.md).

This module closes that gap WITHOUT inventing exploitation. It answers one
question per finding: if an attacker reaches the host carrying this weakness,
what does the weakness let them do?

  foothold              gain control of THIS host from outside (unauthenticated
                        shell, datastore or desktop; out-of-band management bypass)
  exploit_precondition  the documented precondition for a known exploit class is
                        present (SMBv1 on, RDP without NLA, an unsupported OS), but
                        whether the host is actually vulnerable is NOT known — a
                        patched host still speaks SMBv1. A low-weight, possible step
  lateral / priv_esc    move to another host / escalate on this one (reserved for
                        curated rules; no rule claims these today)
  credential_access     harvest credentials or enable a relay usable elsewhere
                        (sniffing, default SNMP, SMB signing not required)
  recon                 information or reachability only — enumerate, fingerprint,
                        disclose, "the login screen answers"

CONTROL. A finding makes its host a compromised pivot only when BOTH hold:
  * its capability is a control capability (foothold, exploit_precondition,
    lateral, priv_esc), and
  * that capability came from the CURATED rule table below.
A category or ATT&CK-technique fallback still classifies the finding (so the UI and
report can say what it is) but never grants control: an imported scanner finding
tagged T1190, or a rule added to the engine later, cannot silently become a
foothold. Reaching a host is not owning it (monotonic control, MulVAL / Ou et al.).

Pure and deterministic: no DB, no I/O.
"""
from __future__ import annotations

from typing import Any, Optional

FOOTHOLD = "foothold"
EXPLOIT_PRECONDITION = "exploit_precondition"
LATERAL = "lateral"
PRIV_ESC = "priv_esc"
CREDENTIAL_ACCESS = "credential_access"
RECON = "recon"

# Where a classification came from. Only SOURCE_RULE may grant control.
SOURCE_RULE = "rule"
SOURCE_CATEGORY = "category"
SOURCE_MITRE = "mitre"

# The capabilities that can make a host a COMPROMISED pivot (when curated).
CONTROL_CAPABILITIES: frozenset[str] = frozenset({FOOTHOLD, EXPLOIT_PRECONDITION, LATERAL, PRIV_ESC})

# ── rule_id → capability (exact, curated) ─────────────────────────────────────
# Each entry is a deliberate statement about what the weakness yields. A weakness
# that only discloses information, only weakens transport crypto, or only proves a
# login service answers is RECON (or absent) — never a foothold.
_RULE_CAPABILITY: dict[str, str] = {
    # ── foothold: direct control of the host it sits on, no credential needed ──
    "POSTURE-DB-UNAUTHENTICATED-ACCESS": FOOTHOLD,     # read/write the datastore directly
    "POSTURE-VNC-NO-AUTH": FOOTHOLD,                   # interactive desktop, no credential
    "POSTURE-ADB-UNAUTHENTICATED": FOOTHOLD,           # unauthenticated Android shell
    "POSTURE-IPMI-CIPHER-ZERO": FOOTHOLD,              # out-of-band auth bypass
    "POSTURE-MQTT-UNAUTHENTICATED": FOOTHOLD,          # broker access without auth
    "POSTURE-AI-ENDPOINT-UNAUTHENTICATED": FOOTHOLD,   # unauthenticated inference / tool endpoint
    "POSTURE-FTP-ANONYMOUS-WRITE": FOOTHOLD,           # anonymous upload of attacker content
    "POSTURE-DEFAULT-CRED-CANDIDATE": FOOTHOLD,        # vendor default credentials (candidate: state lowers it)
    "CORR-DB-UNAUTH-EXPOSED": FOOTHOLD,                # exposed datastore + unauthenticated access
    # ── exploit precondition: a known exploit class is reachable, vulnerability unproven ──
    "POSTURE-SMB-V1-ENABLED": EXPLOIT_PRECONDITION,    # EternalBlue-class transport; patch state unknown
    "POSTURE-RDP-NO-NLA": EXPLOIT_PRECONDITION,        # pre-auth RDP reach; patch state unknown
    "POSTURE-OS-END-OF-LIFE": EXPLOIT_PRECONDITION,    # unsupported, so unpatched issues accumulate
    "POSTURE-CWMP-EXPOSED": EXPLOIT_PRECONDITION,      # TR-069 management plane reachable
    "CORR-LEGACY-WINDOWS-SURFACE": EXPLOIT_PRECONDITION,  # SMBv1 + exposed RDP together
    # ── credential access / relay preconditions: enable movement, never ownership alone ──
    # SMB signing off (and the composite built on it) is a RELAY precondition (FM-09):
    # it owns a host only through P3's relay edge, which also needs a coercion source.
    "POSTURE-SMB-SIGNING-OFF": CREDENTIAL_ACCESS,
    "CORR-NTLM-RELAY-PATH": CREDENTIAL_ACCESS,
    "POSTURE-SNMP-DEFAULT-COMMUNITY": CREDENTIAL_ACCESS,   # config + community strings leak (read)
    "POSTURE-SNMPV3-NOAUTH-USER": CREDENTIAL_ACCESS,       # read SNMP without auth
    "CORR-SNMP-PUBLIC-LATERAL": CREDENTIAL_ACCESS,         # topology + credentials from infra SNMP
    "POSTURE-FTP-ANONYMOUS-LOGIN": CREDENTIAL_ACCESS,      # anonymous read of stored data
    "POSTURE-RSYNC-ANONYMOUS-MODULE": CREDENTIAL_ACCESS,   # anonymous read of module contents
    "POSTURE-NFS-WORLD-READABLE-EXPORT": CREDENTIAL_ACCESS,  # read exported data / keys
    "CORR-CLEARTEXT-CLUSTER": CREDENTIAL_ACCESS,           # one sniffing position, many credentials
    "CORR-AD-EXPOSURE": CREDENTIAL_ACCESS,                 # anonymous directory read
    # ── recon: information or reachability only ──
    "POSTURE-RDP-EXPOSED": RECON,          # the login screen answers; a credential is still needed
    "POSTURE-RTSP-EXPOSED": RECON,         # the stream endpoint answers OPTIONS
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
}

# Composite whose meaning depends on which signal fired: IPMI cipher-0 is a takeover,
# while WinRM + RDP both answering is reachability. Its IPMI host is also covered by
# POSTURE-IPMI-CIPHER-ZERO, so the composite itself never needs to grant control.
_EVIDENCE_DEPENDENT = {"CORR-MGMT-PLANE-EXPOSED"}

# ── category → capability (classification only; never grants control) ─────────
_CATEGORY_CAPABILITY: dict[str, str] = {
    "default_credentials": CREDENTIAL_ACCESS,
    "information_disclosure": RECON,
    "exposure": RECON,
}

# ATT&CK technique families, used only when neither rule_id nor category placed the
# finding. Classification only: none of these grants control on its own.
_MITRE_CAPABILITY: dict[str, Optional[str]] = {
    "T1190": FOOTHOLD,     # exploit public-facing application
    "T1133": FOOTHOLD,     # external remote services
    "T1210": FOOTHOLD,     # exploitation of remote services
    "T1021": LATERAL,      # remote services
    "T1557": CREDENTIAL_ACCESS,  # adversary-in-the-middle / relay
    "T1078": CREDENTIAL_ACCESS,  # valid accounts
    "T1110": CREDENTIAL_ACCESS,  # brute force
    "T1040": CREDENTIAL_ACCESS,  # network sniffing
    "T1602": CREDENTIAL_ACCESS,  # data from configuration repository
    "T1087": RECON, "T1046": RECON, "T1135": RECON, "T1590": RECON, "T1595": RECON,
    "T1498": None,         # network DoS — not a path step at all
    "T1505": PRIV_ESC, "T1574": PRIV_ESC, "T1543": PRIV_ESC, "T1562": PRIV_ESC,
}


def _mitre_base(technique: Any) -> str:
    """"T1557.001" -> "T1557" (sub-technique dot stripped)."""
    return str(technique or "").split(".", 1)[0].strip().upper()


def classify(rule_id: Any, category: Any = None, mitre: Any = None,
             evidence: Optional[dict] = None) -> tuple[Optional[str], Optional[str]]:
    """(capability, source) for one finding. `source` is SOURCE_RULE when the curated
    table placed it, SOURCE_CATEGORY / SOURCE_MITRE for a fallback, None when nothing
    did. Only SOURCE_RULE may grant control (see `grants_control`)."""
    rid = str(rule_id or "").strip().upper()
    if rid in _EVIDENCE_DEPENDENT:
        correlated = [str(c).upper() for c in ((evidence or {}).get("correlated") or [])]
        return (FOOTHOLD if "IPMI-CIPHER-ZERO" in correlated else RECON), SOURCE_RULE
    if rid in _RULE_CAPABILITY:
        return _RULE_CAPABILITY[rid], SOURCE_RULE
    cat = str(category or "").strip().lower()
    if cat in _CATEGORY_CAPABILITY:
        return _CATEGORY_CAPABILITY[cat], SOURCE_CATEGORY
    techniques = [mitre] if isinstance(mitre, str) else list(mitre or [])
    for t in techniques:
        base = _mitre_base(t)
        if base in _MITRE_CAPABILITY:
            cap = _MITRE_CAPABILITY[base]
            return cap, (SOURCE_MITRE if cap else None)
    return None, None


def capability_for(rule_id: Any, category: Any = None, mitre: Any = None,
                   evidence: Optional[dict] = None) -> Optional[str]:
    """The attacker capability a finding is classified as (whatever the source)."""
    return classify(rule_id, category, mitre, evidence)[0]


def grants_control(capability: Any, source: Any = SOURCE_RULE) -> bool:
    """Does this classification make the host a compromised pivot? Only a control
    capability that came from the curated rule table does."""
    return capability in CONTROL_CAPABILITIES and source == SOURCE_RULE


# ── step likelihood for a capability finding ──────────────────────────────────
# Base success per capability. COARSE and ordinal: they ORDER steps (an
# unauthenticated datastore above "SMBv1 is on"), they are not calibrated
# probabilities of compromise.
_CAPABILITY_BASE: dict[str, float] = {
    FOOTHOLD: 0.6,
    LATERAL: 0.45,
    PRIV_ESC: 0.45,
    # Vulnerability unproven: low on its own, raised only by real exploitation
    # evidence (a KEV-listed or high-EPSS CVE the precondition leads to).
    EXPLOIT_PRECONDITION: 0.2,
}

# State of the finding (posture state, or the verification verdict).
_STATE_FACTOR: dict[str, float] = {
    "confirmed": 1.0,
    "corroborated": 0.95,
    "suspected": 0.7,
    "potential": 0.55,
    "inferred": 0.7,
    "contradicted": 0.3,
}

# Additive sharpening from real-world exploitation evidence on the 0–1 scale,
# mirroring exploitability._TIER_BOOST. It raises a step; it never lowers it.
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
    """Success likelihood (0,1] of a capability step, from a Finding graph node's data
    (capability, capability_source, state / verification_state, confidence, epss,
    exploitability, kev). 0.0 when the finding does not grant control.

    max(capability-and-state base, measured EPSS), plus a KEV/EPSS tier bump, scaled
    by the finding's confidence — the same shape as the CVE step model."""
    cap = data.get("capability")
    if not grants_control(cap, data.get("capability_source", SOURCE_RULE)):
        return 0.0
    base = _CAPABILITY_BASE.get(cap, 0.45)
    state = str(data.get("state") or data.get("verification_state") or "").lower()
    base *= _STATE_FACTOR.get(state, 0.7)

    p = max(base, _f(data.get("epss")))

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
