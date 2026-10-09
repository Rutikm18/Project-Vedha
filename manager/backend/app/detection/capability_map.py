"""
capability_map.py — P2: map persisted findings → attacker capabilities for graph building.

Context (ATTACK_PATH_PLAN.md §3.3 / §9.2 FM-12):
  XM Cyber research: ~80% of real exposures are misconfig/identity; <1% are CVEs.
  The attack graph only creates EXPLOITS edges for findings with exploitable=True,
  which the detection engine sets only for CVEs validated by the AD modules.
  Every CORR-*, POSTURE-*, and POSTURE-EXPOSED-* finding — the bulk of what Vedha
  finds on a real engagement — carries exploitable=False, so zero attack steps exist.

Fix (this module):
  We derive SyntheticFinding objects from the existing persisted findings using a
  capability rule table. Each SyntheticFinding looks like a Finding ORM object to
  GraphBuilder but has exploitable=True and an epss_score set to the base probability
  from the rule table (the analyzer's step_likelihood uses EPSS as the primary signal).

Design:
  * Pure: no DB, no I/O — takes finding-like objects, returns SyntheticFinding list.
  * SyntheticFinding is a dataclass that mirrors the fields GraphBuilder reads.
  * hop_type carried on each SyntheticFinding labels what the capability is:
      foothold        — attacker gains initial control of this host from outside
      lateral         — attacker already inside the network can compromise this host
      credential_access — attacker obtains credentials reusable elsewhere
      priv_esc        — attacker already on the host gains higher privileges
  * Compound rules: when POSTURE-SMB-SIGNING-OFF and POSTURE-MSRPC-EPMAP-EXPOSED
    both exist on one asset, a higher-confidence NTLM-relay-and-coerce capability
    is emitted (stronger than either alone).
  * One SyntheticFinding per (asset, rule_id): deterministic ID prevents duplicate
    graph nodes on repeated calls.

Integration:
  app/graph/builder.py assemble() extends the findings list with derive_capabilities()
  output before passing to build_asset_graph. No other files need to change.
"""
from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from typing import Any

# ── rule table ────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class _Rule:
    hop_type: str          # foothold | lateral | credential_access | priv_esc
    technique_id: str      # MITRE ATT&CK Txxxx or Txxxx.yyy
    technique_name: str    # human label
    base_p: float          # base exploitation probability (0, 1]
    confidence: float      # verification confidence percentage (0–100)
    label: str             # short human-readable label for the synthetic finding


# rule_id → capability. CORR-* and POSTURE-* findings are mapped here.
_RULES: dict[str, _Rule] = {
    # ── CORR composite findings ────────────────────────────────────────────────
    #
    # NTLM relay target: any host on the same segment (an already-compromised
    # peer) can coerce auth and relay it here to gain SYSTEM. The relay target's
    # vulnerability is that SMB signing is not required. Existing SAME_SEGMENT
    # hub edges provide the movement edge; this capability makes the host
    # exploitable from those peers (FM-12 / §3.3).
    "CORR-NTLM-RELAY-PATH": _Rule(
        hop_type="lateral",
        technique_id="T1557.001",
        technique_name="LLMNR/NBT-NS Poisoning and SMB Relay",
        base_p=0.65,
        confidence=70.0,
        label="NTLM relay target — SMB signing not required",
    ),
    # Legacy Windows attack surface. SMBv1 is wormable (EternalBlue class) AND
    # RDP is exposed — the ransomware entry profile.
    "CORR-LEGACY-WINDOWS-SURFACE": _Rule(
        hop_type="lateral",
        technique_id="T1210",
        technique_name="Exploitation of Remote Services (EternalBlue / BlueKeep class)",
        base_p=0.70,
        confidence=72.0,
        label="Legacy Windows surface — SMBv1 + exposed RDP",
    ),
    # Unauthenticated datastore: MySQL with FILE priv → OS RCE; Redis config
    # write → authorised_keys / cron → RCE; any DB → data breach. Foothold
    # because the attacker gains control of the host process.
    "CORR-DB-UNAUTH-EXPOSED": _Rule(
        hop_type="foothold",
        technique_id="T1190",
        technique_name="Exploit Public-Facing Application / Unauthenticated Datastore",
        base_p=0.82,
        confidence=85.0,
        label="Unauthenticated datastore — direct data access or RCE",
    ),
    # Default SNMP community on infrastructure: full MIB read leaks routes,
    # neighbour table, interface configs, and often community strings for
    # downstream devices. On a network device this is a topology pivot.
    "CORR-SNMP-PUBLIC-LATERAL": _Rule(
        hop_type="lateral",
        technique_id="T1602.001",
        technique_name="Network Device Configuration - SNMP MIBs",
        base_p=0.58,
        confidence=65.0,
        label="Default SNMP community — topology / config disclosure",
    ),
    # Multiple cleartext protocols on one host = sniffing position captures
    # credentials across services. Models the attacker's coerce-and-sniff
    # position rather than a direct compromise.
    "CORR-CLEARTEXT-CLUSTER": _Rule(
        hop_type="credential_access",
        technique_id="T1040",
        technique_name="Network Sniffing — cleartext credential capture",
        base_p=0.55,
        confidence=60.0,
        label="Multiple cleartext services — credential capture position",
    ),
    # Anonymous LDAP + SMB: recon path to AD objects (users/groups/SPNs) plus
    # an SMB relay surface. On a DC this is a direct domain-compromise chain.
    "CORR-AD-EXPOSURE": _Rule(
        hop_type="foothold",
        technique_id="T1087.002",
        technique_name="Domain Account Discovery via Anonymous LDAP + SMB Relay",
        base_p=0.62,
        confidence=68.0,
        label="AD exposure — anon LDAP + SMB coercion surface",
    ),
    # IPMI cipher-0 is an authentication bypass (any password accepted) →
    # full out-of-band control; WinRM + RDP is a concentrated cred-attack surface.
    "CORR-MGMT-PLANE-EXPOSED": _Rule(
        hop_type="foothold",
        technique_id="T1078",
        technique_name="Valid Accounts — management plane bypass (IPMI / WinRM / RDP)",
        base_p=0.75,
        confidence=78.0,
        label="Management plane exposed — IPMI cipher-0 / WinRM / RDP",
    ),

    # ── POSTURE individual rules ───────────────────────────────────────────────
    #
    # SMB signing off alone (without the CORR composite) still makes this host
    # a relay target — just with slightly lower confidence because we have no
    # evidence of a coercion source.
    "POSTURE-SMB-SIGNING-OFF": _Rule(
        hop_type="lateral",
        technique_id="T1557.001",
        technique_name="LLMNR/NBT-NS Poisoning and SMB Relay (signing off)",
        base_p=0.58,
        confidence=62.0,
        label="SMB signing not required — relay-target exposure",
    ),
    "POSTURE-SMB-V1-ENABLED": _Rule(
        hop_type="lateral",
        technique_id="T1210",
        technique_name="Exploitation of Remote Services — EternalBlue / WannaCry class",
        base_p=0.62,
        confidence=65.0,
        label="SMBv1 enabled — wormable network protocol",
    ),
    # RDP with no NLA allows pre-auth attack surface (BlueKeep, credential spray
    # without a valid session being established first).
    "POSTURE-RDP-NO-NLA": _Rule(
        hop_type="lateral",
        technique_id="T1110.003",
        technique_name="Password Spraying / Pre-auth RDP Exploit (no NLA)",
        base_p=0.45,
        confidence=50.0,
        label="RDP without NLA — pre-auth attack surface",
    ),
    "POSTURE-RDP-EXPOSED": _Rule(
        hop_type="lateral",
        technique_id="T1021.001",
        technique_name="Remote Desktop Protocol — exposed attack surface",
        base_p=0.40,
        confidence=45.0,
        label="RDP exposed to network — brute-force / session-hijack surface",
    ),
    # The MSRPC endpoint mapper is the coercion entry point for PetitPotam /
    # SpoolSS / DFSCoerce. On a host that also has SMB signing off, this
    # significantly boosts the NTLM relay confidence (handled by the compound
    # rule below). On its own it is a recon and potential RPC exploit surface.
    "POSTURE-MSRPC-EPMAP-EXPOSED": _Rule(
        hop_type="lateral",
        technique_id="T1210",
        technique_name="RPC Endpoint Mapper — coercion surface (PetitPotam / SpoolSS)",
        base_p=0.48,
        confidence=52.0,
        label="MSRPC epmap exposed — RPC coercion surface",
    ),
    "POSTURE-SNMP-DEFAULT-COMMUNITY": _Rule(
        hop_type="lateral",
        technique_id="T1602.001",
        technique_name="Network Device Configuration — SNMP default community",
        base_p=0.52,
        confidence=58.0,
        label="Default SNMP community string — MIB disclosure",
    ),
    "POSTURE-UDP-AMPLIFIER": _Rule(
        hop_type="lateral",
        technique_id="T1498.002",
        technique_name="Reflection Amplification — UDP amplification vector",
        base_p=0.40,
        confidence=45.0,
        label="UDP amplification vector — reflection / DoS pivot",
    ),

    # ── POSTURE-EXPOSED-<CATEGORY> — port-intel exposed service findings ───────
    #
    # A suspected backdoor listener is the strongest possible signal: any open
    # port matching a backdoor pattern (Cobalt Strike, Metasploit, known RATs)
    # is almost certainly a foothold already.
    "POSTURE-EXPOSED-BACKDOOR": _Rule(
        hop_type="foothold",
        technique_id="T1190",
        technique_name="Exploit Public-Facing Application — suspected backdoor",
        base_p=0.88,
        confidence=80.0,
        label="Suspected backdoor listener — potential pre-existing foothold",
    ),
    # Unauthenticated Docker / Kubernetes API: create a privileged container →
    # mount host filesystem → read /etc/shadow or write SSH keys → full host escape.
    "POSTURE-EXPOSED-CONTAINER": _Rule(
        hop_type="foothold",
        technique_id="T1610",
        technique_name="Deploy Container — container API to host escape",
        base_p=0.87,
        confidence=88.0,
        label="Container API exposed — privileged container → host escape",
    ),
    "POSTURE-EXPOSED-DATASTORE": _Rule(
        hop_type="foothold",
        technique_id="T1190",
        technique_name="Exploit Public-Facing Application — exposed datastore",
        base_p=0.75,
        confidence=78.0,
        label="Exposed datastore — direct data access path",
    ),
    "POSTURE-EXPOSED-DATABASE": _Rule(
        hop_type="foothold",
        technique_id="T1190",
        technique_name="Exploit Public-Facing Application — exposed database listener",
        base_p=0.74,
        confidence=76.0,
        label="Exposed database — unauthenticated or default-cred access",
    ),
    "POSTURE-EXPOSED-CLEARTEXT": _Rule(
        hop_type="credential_access",
        technique_id="T1040",
        technique_name="Network Sniffing — cleartext protocol credential capture",
        base_p=0.50,
        confidence=55.0,
        label="Cleartext protocol — credential capture for any sniffing attacker",
    ),
    # Remote-access interfaces (VNC, RDP, WinRM, SSH with weak config) exposed
    # to the network: credential-attack and session-hijack surface.
    "POSTURE-EXPOSED-REMOTE_ACCESS": _Rule(
        hop_type="foothold",
        technique_id="T1021",
        technique_name="Remote Services — exposed remote-administration interface",
        base_p=0.58,
        confidence=60.0,
        label="Remote-access interface exposed — credential attack / session hijack",
    ),
    # Admin UIs (Grafana, Jenkins, Kibana, phpMyAdmin) exposed without auth
    # or with default credentials: direct administrative access to the service.
    "POSTURE-EXPOSED-ADMIN_UI": _Rule(
        hop_type="foothold",
        technique_id="T1078",
        technique_name="Valid Accounts — exposed admin/management web interface",
        base_p=0.60,
        confidence=62.0,
        label="Admin web interface exposed — default or no auth",
    ),
}

# ── compound rule: NTLM relay + coercion surface ──────────────────────────────
# When BOTH a relay target AND a coercion surface exist on the same asset, the
# attack is more confident: the coercion can be triggered locally, so the
# attacker doesn't need a victim to spontaneously authenticate.
_RELAY_RULE_ID = "CORR-NTLM-RELAY-PATH"
_SIGNING_OFF_RULES = frozenset({"CORR-NTLM-RELAY-PATH", "POSTURE-SMB-SIGNING-OFF"})
_COERCE_RULES = frozenset({"POSTURE-MSRPC-EPMAP-EXPOSED"})
_COMPOUND_RELAY_ID = "COMPOUND-NTLM-RELAY-AND-COERCE"
_COMPOUND_RELAY_RULE = _Rule(
    hop_type="lateral",
    technique_id="T1557.001",
    technique_name="NTLM Relay + RPC Coercion (PetitPotam / SpoolSS / DFSCoerce)",
    base_p=0.78,
    confidence=80.0,
    label="NTLM relay + coercion surface — relay can be self-triggered",
)

# ── SyntheticFinding ──────────────────────────────────────────────────────────


@dataclass
class SyntheticFinding:
    """Looks like a Finding ORM object to GraphBuilder.build_asset_graph.

    Set exploitable=True and epss_score=base_p so the analyzer's step_likelihood
    uses the capability rule's probability as the step cost (EPSS is the highest-
    priority evidence signal: EPSS > attack_complexity > severity).
    """
    id: str
    asset_id: Any                    # same type as Asset.id (UUID or str)
    title: str
    severity: str                    # "critical" | "high" | "medium" | "low"
    cvss_score: float
    cvss_vector: None = None
    exploitable: bool = True
    exploit_validated: bool = False
    epss_score: float = 0.0
    mitre_techniques: list[str] = field(default_factory=list)
    verification_confidence: float = 70.0
    status: str = "open"             # must match LIVE_FINDING_STATUSES in builder
    # extra metadata (not read by the graph engine — used for reporting)
    hop_type: str = "foothold"
    capability_label: str = ""
    capability_rule_id: str = ""


# ── helpers ───────────────────────────────────────────────────────────────────


def _get_attr(obj: Any, *names: str, default: Any = None) -> Any:
    """Get the first attribute or dict key that exists."""
    for name in names:
        if isinstance(obj, dict):
            v = obj.get(name)
        else:
            v = getattr(obj, name, None)
        if v is not None:
            return v
    return default


def _str_val(v: Any) -> str:
    """Enum → str (handles SQLAlchemy enum values)."""
    return str(getattr(v, "value", v) or "").lower()


def _synthetic_id(rule_id: str, asset_id: str) -> str:
    """Deterministic UUID from rule + asset so the graph node is stable across runs."""
    raw = f"capability:{rule_id}:{asset_id}".encode()
    return str(uuid.UUID(bytes=hashlib.sha256(raw).digest()[:16], version=4))


def _p_to_cvss(p: float) -> float:
    """Map a probability (0, 1] to a CVSS-like score [0, 10].

    Used only as a fallback if the analyzer falls through to the severity-based
    estimator; EPSS (set to p directly) is the primary signal.
    """
    # Inverse sigmoid approximation: CVSS 10 → p≈0.95, CVSS 5 → p≈0.5
    p = max(0.05, min(0.99, p))
    import math
    return round(5.0 + 5.0 * (2 * p - 1) / (1 + abs(2 * p - 1)), 1)


def _severity_from_p(p: float) -> str:
    if p >= 0.80:
        return "critical"
    if p >= 0.65:
        return "high"
    if p >= 0.45:
        return "medium"
    return "low"


# ── public API ────────────────────────────────────────────────────────────────


def derive_capabilities(
    findings: list[Any],
    assets: list[Any] = (),
) -> list[SyntheticFinding]:
    """Map persisted findings → SyntheticFinding objects with exploitable=True.

    ``findings`` — Finding ORM objects or dicts (as loaded by build_from_db).
    ``assets``   — Asset ORM objects; currently unused but available for future
                   device-role amplification independent of the finding's severity.

    Returns one SyntheticFinding per (asset_id, capability_rule) matched, with
    a compound NTLM-relay-and-coerce finding emitted when both a relay target and
    a coercion surface finding exist on the same asset.

    Idempotent: multiple calls with the same findings produce the same IDs.
    """
    out: list[SyntheticFinding] = []
    # Group all rule_ids found per asset for compound rule evaluation.
    asset_rule_ids: dict[str, set[str]] = {}

    for f in findings:
        rid_raw = _get_attr(f, "rule_id")
        # Preserve original case for the rule table lookup; _str_val is for
        # enum-backed severity/status fields, not for rule ID keys.
        rule_id = str(getattr(rid_raw, "value", rid_raw) or "")
        if not rule_id:
            continue
        rule = _RULES.get(rule_id)
        if rule is None:
            continue

        asset_id = _get_attr(f, "asset_id")
        if asset_id is None:
            continue
        asset_id_str = str(asset_id)

        # Inherit severity from the finding (detection already amplified it for
        # DCs, network devices, etc.) so a DC relay finding keeps its critical.
        finding_severity = _str_val(_get_attr(f, "severity"))
        effective_p = rule.base_p

        # If the finding was amplified to critical by device-role detection,
        # boost the base probability to reflect that higher-confidence signal.
        if finding_severity == "critical" and effective_p < 0.85:
            effective_p = min(0.92, effective_p * 1.15)
        elif finding_severity == "low" and effective_p > 0.50:
            effective_p = max(0.30, effective_p * 0.80)

        # Evidence-based probability adjustment for IPMI cipher-0 specifically:
        # cipher-0 is an authentication BYPASS (any password accepted), so the
        # actual probability is higher than the base CORR-MGMT-PLANE-EXPOSED rule.
        if rule_id == "CORR-MGMT-PLANE-EXPOSED":
            ev = _get_attr(f, "evidence") or {}
            if isinstance(ev, dict) and ev.get("ipmi_cipher_zero"):
                effective_p = min(0.92, effective_p * 1.2)

        # Track this rule for the compound check below.
        asset_rule_ids.setdefault(asset_id_str, set()).add(rule_id)

        out.append(SyntheticFinding(
            id=_synthetic_id(rule_id, asset_id_str),
            asset_id=asset_id,
            title=rule.label,
            severity=finding_severity or _severity_from_p(effective_p),
            cvss_score=_p_to_cvss(effective_p),
            epss_score=round(effective_p, 4),
            mitre_techniques=[rule.technique_id],
            verification_confidence=rule.confidence,
            hop_type=rule.hop_type,
            capability_label=rule.label,
            capability_rule_id=rule_id,
        ))

    # ── compound rule: NTLM relay + coercion surface on the same asset ──────────
    # When a host is both a relay target (SMB signing off) AND has an RPC
    # endpoint mapper exposed (coercion surface), the attack chain is
    # self-contained: the attacker can trigger the auth from the victim and
    # relay it — without needing any external victim authentication event.
    emitted: dict[str, set[str]] = {}  # asset_id → synthetic rule_ids already added
    for sf in out:
        emitted.setdefault(str(sf.asset_id), set()).add(sf.capability_rule_id)

    for asset_id_str, rule_ids in asset_rule_ids.items():
        has_relay = bool(rule_ids & _SIGNING_OFF_RULES)
        has_coerce = bool(rule_ids & _COERCE_RULES)
        if has_relay and has_coerce:
            cid = _synthetic_id(_COMPOUND_RELAY_ID, asset_id_str)
            r = _COMPOUND_RELAY_RULE
            # Find the original asset_id (non-str) from one of the emitted findings.
            original_asset_id = next(
                (sf.asset_id for sf in out if str(sf.asset_id) == asset_id_str), asset_id_str
            )
            out.append(SyntheticFinding(
                id=cid,
                asset_id=original_asset_id,
                title=r.label,
                severity=_severity_from_p(r.base_p),
                cvss_score=_p_to_cvss(r.base_p),
                epss_score=round(r.base_p, 4),
                mitre_techniques=[r.technique_id],
                verification_confidence=r.confidence,
                hop_type=r.hop_type,
                capability_label=r.label,
                capability_rule_id=_COMPOUND_RELAY_ID,
            ))

    return out


def list_rules() -> list[dict[str, Any]]:
    """Return the full rule table as plain dicts (for documentation / API)."""
    rules = []
    for rid, r in sorted(_RULES.items()):
        rules.append({
            "rule_id": rid,
            "hop_type": r.hop_type,
            "technique_id": r.technique_id,
            "technique_name": r.technique_name,
            "base_probability": r.base_p,
            "confidence": r.confidence,
            "label": r.label,
        })
    rules.append({
        "rule_id": _COMPOUND_RELAY_ID,
        "hop_type": _COMPOUND_RELAY_RULE.hop_type,
        "technique_id": _COMPOUND_RELAY_RULE.technique_id,
        "technique_name": _COMPOUND_RELAY_RULE.technique_name,
        "base_probability": _COMPOUND_RELAY_RULE.base_p,
        "confidence": _COMPOUND_RELAY_RULE.confidence,
        "label": _COMPOUND_RELAY_RULE.label,
    })
    return rules
